"""PASO 5 · Almacén: dónde vive todo lo que el agente debe recordar.

Dos implementaciones con los MISMOS métodos, para poder empezar sin Docker y cambiar
después a PostgreSQL sin tocar el resto del proyecto:

- AlmacenMemoria   -> diccionarios en RAM. Se pierde al cerrar el proceso.
- AlmacenPostgres  -> PostgreSQL + pgvector. Sobrevive a un reinicio.

Guardan tres cosas distintas (ver esquema.sql): de quién es cada conversación, los
fragmentos de documentación con su vector y los trabajos de investigación.
La memoria del grafo (checkpoints) la gestiona LangGraph; aquí solo se le entrega.
"""

import hashlib
import json
import math
import uuid
from dataclasses import dataclass

from .config import DIM, RAIZ


@dataclass(frozen=True)
class Fragmento:
    fragmento_id: str
    documento: str
    titulo: str
    seccion: str
    contenido: str


def clave_trabajo(thread_id: str, tema: str) -> str:
    """Misma conversación + mismo tema = mismo trabajo. Así repetir la petición no duplica."""
    normal = " ".join(tema.lower().split())
    return hashlib.sha256(f"{thread_id}|{normal}".encode()).hexdigest()[:24]


def _coseno(a: list[float], b: list[float]) -> float:
    norma = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b, strict=True)) / norma if norma else 0.0


# ------------------------------------------------------------------ memoria (sin Docker)
class AlmacenMemoria:
    nombre = "memoria"

    def __init__(self):
        self._conversaciones: dict[str, str] = {}
        self._fragmentos: list[tuple[Fragmento, list[float], str]] = []
        self._trabajos: dict[str, dict] = {}
        self._checkpointer = None

    def preparar(self):
        return self

    def cerrar(self):
        pass

    def checkpointer(self):
        from langgraph.checkpoint.memory import InMemorySaver

        self._checkpointer = self._checkpointer or InMemorySaver()
        return self._checkpointer

    # --- conversaciones: thread_id no autoriza, el propietario sí
    def asegurar_conversacion(self, thread_id: str, usuario: str) -> bool:
        """Crea la conversación si no existe. Devuelve False si es de otro usuario."""
        return self._conversaciones.setdefault(thread_id, usuario) == usuario

    def propietario(self, thread_id: str) -> str | None:
        return self._conversaciones.get(thread_id)

    # --- fragmentos (RAG)
    def reemplazar_fragmentos(self, filas: list[tuple[Fragmento, list[float]]], modelo: str):
        self._fragmentos = [(f, v, modelo) for f, v in filas]

    def contar_fragmentos(self) -> int:
        return len(self._fragmentos)

    def buscar_fragmentos(self, vector: list[float], k: int, modelo: str):
        candidatos = [(f, _coseno(vector, v)) for f, v, m in self._fragmentos if m == modelo]
        return sorted(candidatos, key=lambda par: par[1], reverse=True)[:k]

    # --- trabajos de investigación
    def crear_trabajo(self, thread_id: str, usuario: str, tema: str) -> dict:
        clave = clave_trabajo(thread_id, tema)
        for trabajo in self._trabajos.values():
            if trabajo["clave"] == clave:
                return dict(trabajo, nuevo=False)
        trabajo = {
            "trabajo_id": f"INV-{uuid.uuid4().hex[:8]}",
            "clave": clave,
            "thread_id": thread_id,
            "usuario": usuario,
            "tema": tema,
            "estado": "pendiente",
            "informe": None,
        }
        self._trabajos[trabajo["trabajo_id"]] = trabajo
        return dict(trabajo, nuevo=True)

    def leer_trabajo(self, trabajo_id: str) -> dict | None:
        trabajo = self._trabajos.get(trabajo_id)
        return dict(trabajo) if trabajo else None

    def tomar_pendiente(self) -> dict | None:
        for trabajo in self._trabajos.values():
            if trabajo["estado"] == "pendiente":
                trabajo["estado"] = "en_curso"
                return dict(trabajo)
        return None

    def guardar_trabajo(self, trabajo_id: str, estado: str, informe: dict):
        self._trabajos[trabajo_id].update(estado=estado, informe=informe)


# ------------------------------------------------------------------ PostgreSQL + pgvector
def _vector_sql(vector: list[float]) -> str:
    """pgvector acepta el vector como texto '[0.1,0.2,...]' y lo convierte con ::vector."""
    if len(vector) != DIM:
        raise ValueError(f"El esquema usa vector({DIM}); llegó un vector de {len(vector)}")
    return "[" + ",".join(f"{x:.6f}" for x in vector) + "]"


class AlmacenPostgres:
    nombre = "postgres"

    def __init__(self, database_url: str):
        self.database_url = database_url
        self._pool = None
        self._checkpointer = None

    def preparar(self):
        """Abre el pool, aplica esquema.sql (idempotente) y crea las tablas de checkpoints."""
        from psycopg.rows import dict_row
        from psycopg_pool import ConnectionPool

        # autocommit y prepare_threshold=0 son lo que pide el checkpointer de LangGraph.
        self._pool = ConnectionPool(
            conninfo=self.database_url,
            max_size=5,
            kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},
            open=True,
        )
        # Con prepare_threshold=0 cada orden se envía preparada y solo admite UNA sentencia:
        # por eso el esquema se aplica sentencia a sentencia (sin los comentarios «--»).
        esquema = (RAIZ / "esquema.sql").read_text(encoding="utf-8")
        sin_comentarios = "\n".join(ln.split("--")[0] for ln in esquema.splitlines())
        with self._pool.connection() as con:
            for sentencia in filter(str.strip, sin_comentarios.split(";")):
                con.execute(sentencia)
        self.checkpointer().setup()
        return self

    def cerrar(self):
        if self._pool:
            self._pool.close()

    def checkpointer(self):
        from langgraph.checkpoint.postgres import PostgresSaver

        self._checkpointer = self._checkpointer or PostgresSaver(self._pool)
        return self._checkpointer

    def _uno(self, sql: str, parametros=()):
        with self._pool.connection() as con:
            return con.execute(sql, parametros).fetchone()

    # --- conversaciones
    def asegurar_conversacion(self, thread_id: str, usuario: str) -> bool:
        with self._pool.connection() as con:
            con.execute(
                "INSERT INTO conversaciones (thread_id, usuario) VALUES (%s, %s) "
                "ON CONFLICT (thread_id) DO NOTHING",
                (thread_id, usuario),
            )
        return self.propietario(thread_id) == usuario

    def propietario(self, thread_id: str) -> str | None:
        fila = self._uno("SELECT usuario FROM conversaciones WHERE thread_id = %s", (thread_id,))
        return fila["usuario"] if fila else None

    # --- fragmentos (RAG)
    def reemplazar_fragmentos(self, filas: list[tuple[Fragmento, list[float]]], modelo: str):
        """Borra e inserta en una sola transacción: reingestar nunca deja duplicados."""
        with self._pool.connection() as con, con.transaction():
            con.execute("DELETE FROM fragmentos")
            for f, vector in filas:
                con.execute(
                    "INSERT INTO fragmentos (fragmento_id, documento, titulo, seccion, contenido,"
                    " modelo, embedding) VALUES (%s, %s, %s, %s, %s, %s, %s::vector)",
                    (
                        f.fragmento_id,
                        f.documento,
                        f.titulo,
                        f.seccion,
                        f.contenido,
                        modelo,
                        _vector_sql(vector),
                    ),
                )

    def contar_fragmentos(self) -> int:
        return self._uno("SELECT count(*) AS n FROM fragmentos")["n"]

    def buscar_fragmentos(self, vector: list[float], k: int, modelo: str):
        """<=> es la distancia coseno de pgvector; similitud = 1 - distancia."""
        v = _vector_sql(vector)
        with self._pool.connection() as con:
            filas = con.execute(
                "SELECT fragmento_id, documento, titulo, seccion, contenido,"
                " 1 - (embedding <=> %s::vector) AS similitud"
                " FROM fragmentos WHERE modelo = %s ORDER BY embedding <=> %s::vector LIMIT %s",
                (v, modelo, v, k),
            ).fetchall()
        return [
            (
                Fragmento(f["fragmento_id"], f["documento"], f["titulo"], f["seccion"], f["contenido"]),
                float(f["similitud"]),
            )
            for f in filas
        ]

    # --- trabajos de investigación
    def crear_trabajo(self, thread_id: str, usuario: str, tema: str) -> dict:
        clave = clave_trabajo(thread_id, tema)
        fila = self._uno(
            "INSERT INTO trabajos (trabajo_id, clave, thread_id, usuario, tema, estado)"
            " VALUES (%s, %s, %s, %s, %s, 'pendiente') ON CONFLICT (clave) DO NOTHING"
            " RETURNING trabajo_id",
            (f"INV-{uuid.uuid4().hex[:8]}", clave, thread_id, usuario, tema),
        )
        trabajo = self._uno("SELECT * FROM trabajos WHERE clave = %s", (clave,))
        return dict(self._limpio(trabajo), nuevo=fila is not None)

    def leer_trabajo(self, trabajo_id: str) -> dict | None:
        fila = self._uno("SELECT * FROM trabajos WHERE trabajo_id = %s", (trabajo_id,))
        return self._limpio(fila) if fila else None

    def tomar_pendiente(self) -> dict | None:
        """SKIP LOCKED: dos ejecutores a la vez nunca toman el mismo trabajo."""
        fila = self._uno(
            "UPDATE trabajos SET estado = 'en_curso', actualizado_en = NOW()"
            " WHERE trabajo_id = (SELECT trabajo_id FROM trabajos WHERE estado = 'pendiente'"
            " ORDER BY creado_en LIMIT 1 FOR UPDATE SKIP LOCKED) RETURNING *"
        )
        return self._limpio(fila) if fila else None

    def guardar_trabajo(self, trabajo_id: str, estado: str, informe: dict):
        with self._pool.connection() as con:
            con.execute(
                "UPDATE trabajos SET estado = %s, informe = %s::jsonb, actualizado_en = NOW()"
                " WHERE trabajo_id = %s",
                (estado, json.dumps(informe, ensure_ascii=False), trabajo_id),
            )

    @staticmethod
    def _limpio(fila: dict) -> dict:
        campos = ("trabajo_id", "clave", "thread_id", "usuario", "tema", "estado", "informe")
        return {c: fila[c] for c in campos}


def crear_almacen(cfg):
    almacen = AlmacenMemoria() if cfg.almacen == "memoria" else AlmacenPostgres(cfg.database_url)
    return almacen.preparar()
