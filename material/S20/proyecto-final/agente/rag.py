"""PASO 6 · RAG: recuperar documentación propia y responder con fuentes, o rechazar.

Ingesta:   documento -> secciones -> embedding -> almacén (pgvector o memoria)
Consulta:  pregunta  -> embedding -> los k fragmentos más parecidos -> ¿hay evidencia?

La decisión importante es la última: si el mejor fragmento no supera el umbral, el
agente NO responde con lo que haya. Devuelve «sin evidencia» y el modelo dice que no consta.
"""

import hashlib
import math
import random
import re
import unicodedata
from functools import cache
from pathlib import Path

from .almacen import Fragmento
from .config import DIM, RAIZ, Config

CORPUS = RAIZ / "datos" / "corpus"

# Palabras sin significado propio: no deben contar como coincidencia en el perfil doble.
VACIAS = set(
    "a al algo ante como con cual cuando de del desde donde el ella en entre era es esa ese esta "
    "este esto ha hay la las le lo los mas me mi no nos o para pero por que se si sin sobre son "
    "su sus te tiene un una uno y ya cuanto cuantos cuanta cuantas puede pueden debe".split()
)


def palabras(texto: str) -> list[str]:
    """Minúsculas, sin tildes y sin palabras vacías: 'Límites de la API' -> ['limites','api']."""
    plano = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return [p for p in re.findall(r"[a-z0-9][a-z0-9_\-]*", plano) if p not in VACIAS and len(p) > 1]


# ------------------------------------------------------------------ embeddings
class EmbeddingsDoble:
    """Vector de 768 posiciones construido SIN modelo. NO entiende el significado.

    Cada palabra recibe un vector pseudoaleatorio fijo (sale de su hash) y el texto es la suma
    de los vectores de sus palabras. Dos textos se parecen solo si comparten palabras: es una
    bolsa de palabras disfrazada de embedding. Sirve para practicar el recorrido completo sin
    claves ni coste; sus cifras no miden ningún modelo de embeddings.
    """

    nombre = "doble-hash-768"

    @staticmethod
    @cache
    def _de_palabra(raiz: str) -> tuple[float, ...]:
        azar = random.Random(int(hashlib.sha256(raiz.encode()).hexdigest(), 16))
        return tuple(azar.gauss(0, 1) for _ in range(DIM))

    def _vector(self, texto: str) -> list[float]:
        vector = [0.0] * DIM
        # Los 6 primeros caracteres hacen de raíz: «límites» y «límite» cuentan como la misma.
        for raiz in {p[:6] for p in palabras(texto)}:
            vector = [a + b for a, b in zip(vector, self._de_palabra(raiz), strict=True)]
        norma = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [x / norma for x in vector]

    def documentos(self, textos: list[str]) -> list[list[float]]:
        return [self._vector(t) for t in textos]

    def consulta(self, texto: str) -> list[float]:
        return self._vector(texto)


class EmbeddingsReales:
    """Modelo de embeddings de Gemini (perfil real). Necesita GOOGLE_API_KEY y cuesta dinero."""

    def __init__(self, modelo: str):
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        self.nombre = modelo
        self._modelo = GoogleGenerativeAIEmbeddings(model=modelo)

    def documentos(self, textos: list[str]) -> list[list[float]]:
        return self._modelo.embed_documents(
            textos, task_type="RETRIEVAL_DOCUMENT", output_dimensionality=DIM
        )

    def consulta(self, texto: str) -> list[float]:
        return self._modelo.embed_query(texto, task_type="RETRIEVAL_QUERY", output_dimensionality=DIM)


def crear_embeddings(cfg: Config):
    return EmbeddingsDoble() if cfg.perfil == "doble" else EmbeddingsReales(cfg.modelo_embeddings)


# ------------------------------------------------------------------ ingesta
def fragmentar(ruta: Path) -> list[Fragmento]:
    """Un fragmento por sección «## »: cada trozo conserva su título y su sección para citar."""
    documento = ruta.stem
    texto = ruta.read_text(encoding="utf-8")
    titulo = next((ln[2:].strip() for ln in texto.splitlines() if ln.startswith("# ")), documento)
    fragmentos = []
    for bloque in re.split(r"\n(?=## )", texto):
        if not bloque.startswith("## "):
            continue  # el título general del documento no es un fragmento
        seccion, _, cuerpo = bloque[3:].partition("\n")
        fragmentos.append(
            Fragmento(
                f"{documento}#{len(fragmentos) + 1}",
                documento,
                titulo,
                seccion.strip(),
                " ".join(cuerpo.split()),
            )
        )
    return fragmentos


def ingestar(almacen, embeddings, carpeta: Path = CORPUS) -> dict:
    """Reconstruye el índice desde cero. Repetirla deja el mismo resultado (sin duplicados)."""
    fragmentos = [f for ruta in sorted(carpeta.glob("[0-9][0-9]-*.md")) for f in fragmentar(ruta)]
    # Se vectoriza título + sección + contenido: el título aporta contexto al fragmento.
    vectores = embeddings.documentos([f"{f.titulo}. {f.seccion}. {f.contenido}" for f in fragmentos])
    almacen.reemplazar_fragmentos(list(zip(fragmentos, vectores, strict=True)), embeddings.nombre)
    return {
        "documentos": len({f.documento for f in fragmentos}),
        "fragmentos": almacen.contar_fragmentos(),
        "modelo_embeddings": embeddings.nombre,
    }


# ------------------------------------------------------------------ consulta
def recuperar(cfg: Config, almacen, embeddings, pregunta: str) -> dict:
    """Devuelve fragmentos con su cita, o `ok: False` si no hay evidencia suficiente."""
    vecinos = almacen.buscar_fragmentos(
        embeddings.consulta(pregunta), cfg.k_fragmentos, embeddings.nombre
    )
    mejor = vecinos[0][1] if vecinos else 0.0
    if mejor < cfg.umbral_evidencia:
        return {
            "ok": False,
            "motivo": "sin_evidencia",
            "mejor_similitud": round(mejor, 3),
            "umbral": cfg.umbral_evidencia,
            "fragmentos": [],
        }
    return {
        "ok": True,
        "mejor_similitud": round(mejor, 3),
        "umbral": cfg.umbral_evidencia,
        "fragmentos": [
            {
                "cita": f"{f.documento} § {f.seccion}",
                "documento": f.documento,
                "texto": f.contenido,
                "similitud": round(similitud, 3),
            }
            for f, similitud in vecinos
            if similitud >= cfg.umbral_evidencia
        ],
    }
