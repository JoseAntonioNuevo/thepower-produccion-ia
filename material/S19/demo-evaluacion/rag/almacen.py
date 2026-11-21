"""Índice vectorial: PostgreSQL + pgvector, y un almacén en memoria con la misma interfaz.

El de memoria existe para que los tests normales no necesiten Docker. La lógica que se
quiere comprobar (identidad del índice, duplicados, orden) es la misma en los dos.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from rag.corpus import Fragmento

ESQUEMA = Path(__file__).resolve().parent.parent / "esquema.sql"


class ErrorIndice(Exception):
    """El índice no existe, está incompleto o no corresponde al modelo de la consulta."""


@dataclass(frozen=True)
class Indice:
    indice_id: str
    perfil: str
    embedding_modelo: str
    embedding_dim: int
    chunk_size: int
    chunk_overlap: int
    n_documentos: int
    n_fragmentos: int


@dataclass(frozen=True)
class Hallazgo:
    fragmento_id: str
    documento_id: str
    titulo: str
    contenido: str
    similitud: float  # coseno: 1 = misma dirección


def _validar(indice: Indice, filas: list[tuple[Fragmento, list[float]]]) -> None:
    hashes = [f.contenido_hash for f, _ in filas]
    if len(hashes) != len(set(hashes)):
        raise ErrorIndice("hay fragmentos duplicados: el mismo texto no puede indexarse dos veces")
    if any(len(v) != indice.embedding_dim for _, v in filas):
        raise ErrorIndice(f"todos los vectores deben tener {indice.embedding_dim} dimensiones")
    if len(filas) != indice.n_fragmentos:
        raise ErrorIndice("el número de vectores no coincide con el declarado en el índice")


class AlmacenMemoria:
    """Mismo contrato que `AlmacenPg`, en un diccionario. Solo para tests y ejemplos."""

    def __init__(self):
        self._indices: dict[str, Indice] = {}
        self._filas: dict[str, list[tuple[Fragmento, list[float]]]] = {}

    def preparar_esquema(self) -> None:
        return None

    def reconstruir(self, indice: Indice, filas: list[tuple[Fragmento, list[float]]]) -> None:
        _validar(indice, filas)
        self._indices[indice.indice_id] = indice  # sustituye: no se acumula sobre lo anterior
        self._filas[indice.indice_id] = list(filas)

    def leer_indice(self, indice_id: str) -> Indice | None:
        return self._indices.get(indice_id)

    def contar(self, indice_id: str) -> int:
        return len(self._filas.get(indice_id, []))

    def buscar(self, indice_id: str, vector: list[float], k: int) -> list[Hallazgo]:
        def coseno(a: list[float], b: list[float]) -> float:
            na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
            return sum(x * y for x, y in zip(a, b, strict=True)) / (na * nb) if na and nb else 0.0

        puntuados = [
            Hallazgo(f.fragmento_id, f.documento_id, f.titulo, f.contenido, coseno(vector, v))
            for f, v in self._filas.get(indice_id, [])
        ]
        puntuados.sort(key=lambda h: (-h.similitud, h.fragmento_id))
        return puntuados[:k]

    def vaciar(self) -> None:
        self._indices.clear()
        self._filas.clear()


def _literal(vector: list[float]) -> str:
    """pgvector acepta el vector como texto: '[0.1,0.2,...]'."""
    return "[" + ",".join(f"{x:.7f}" for x in vector) + "]"


class AlmacenPg:
    def __init__(self, database_url: str):
        import psycopg

        self._psycopg = psycopg
        self._url = database_url

    def _conectar(self):
        try:
            return self._psycopg.connect(self._url, connect_timeout=5)
        except self._psycopg.OperationalError as exc:
            raise ErrorIndice("No se puede conectar a PostgreSQL. ¿Está arrancado `docker compose up -d`?") from exc

    def preparar_esquema(self) -> None:
        with self._conectar() as con:
            con.execute(ESQUEMA.read_text(encoding="utf-8"))

    def reconstruir(self, indice: Indice, filas: list[tuple[Fragmento, list[float]]]) -> None:
        """Borra el índice y lo vuelve a crear en UNA transacción: o entra entero o no cambia nada."""
        _validar(indice, filas)
        with self._conectar() as con, con.cursor() as cur:
            cur.execute("DELETE FROM indices WHERE indice_id = %s", (indice.indice_id,))
            cur.execute(
                "INSERT INTO indices (indice_id, perfil, embedding_modelo, embedding_dim, "
                "chunk_size, chunk_overlap, n_documentos, n_fragmentos) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    indice.indice_id,
                    indice.perfil,
                    indice.embedding_modelo,
                    indice.embedding_dim,
                    indice.chunk_size,
                    indice.chunk_overlap,
                    indice.n_documentos,
                    indice.n_fragmentos,
                ),
            )
            cur.executemany(
                "INSERT INTO fragmentos (indice_id, fragmento_id, documento_id, ordinal, titulo, "
                "contenido, contenido_hash, embedding) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::vector)",
                [
                    (
                        indice.indice_id,
                        f.fragmento_id,
                        f.documento_id,
                        f.ordinal,
                        f.titulo,
                        f.contenido,
                        f.contenido_hash,
                        _literal(v),
                    )
                    for f, v in filas
                ],
            )

    def leer_indice(self, indice_id: str) -> Indice | None:
        with self._conectar() as con:
            fila = con.execute(
                "SELECT indice_id, perfil, embedding_modelo, embedding_dim, chunk_size, "
                "chunk_overlap, n_documentos, n_fragmentos FROM indices WHERE indice_id = %s",
                (indice_id,),
            ).fetchone()
        return Indice(*fila) if fila else None

    def contar(self, indice_id: str) -> int:
        with self._conectar() as con:
            return con.execute("SELECT count(*) FROM fragmentos WHERE indice_id = %s", (indice_id,)).fetchone()[0]

    def buscar(self, indice_id: str, vector: list[float], k: int) -> list[Hallazgo]:
        """Vecinos más cercanos por coseno. Búsqueda EXACTA: al evaluar no queremos que la
        aproximación del índice HNSW sea otra variable que explique una diferencia."""
        literal = _literal(vector)
        with self._conectar() as con, con.cursor() as cur:
            cur.execute("SET LOCAL enable_indexscan = off")
            cur.execute("SET LOCAL enable_bitmapscan = off")
            cur.execute(
                "SELECT fragmento_id, documento_id, titulo, contenido, "
                "1 - (embedding <=> %s::vector) AS similitud FROM fragmentos "
                "WHERE indice_id = %s ORDER BY embedding <=> %s::vector, fragmento_id LIMIT %s",
                (literal, indice_id, literal, k),
            )
            return [Hallazgo(*fila) for fila in cur.fetchall()]

    def vaciar(self) -> None:
        with self._conectar() as con:
            con.execute("TRUNCATE indices CASCADE")
