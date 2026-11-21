"""Proveedores de embeddings y de generación.

Hay dos perfiles y NUNCA se mezclan ni se sustituyen entre sí:

- `doble`: código local determinista, sin red ni coste. Sirve para tests y para seguir la
  práctica sin claves. Sus resultados NO miden ningún modelo y van rotulados como tales.
- `real`: API de Gemini. Solo se construye con `--execute` y con GEMINI_API_KEY.

Si el perfil real falla, el error se registra. No se cae al doble para «completar» el lote.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
import unicodedata
from dataclasses import dataclass

from rag.config import Config, ErrorConfiguracion

NO_CONSTA = "NO_CONSTA"  # marca exacta que el generador devuelve cuando el contexto no basta


class ErrorProveedor(Exception):
    """El proveedor falló o devolvió algo que no se puede usar."""


@dataclass(frozen=True)
class Generacion:
    texto: str
    tokens_entrada: int | None  # None = desconocido; nunca se inventa
    tokens_salida: int | None
    model_version: str | None = None  # versión servida por la API; None en perfil doble


# ----------------------------------------------------------------- utilidades de texto
_VACIAS = frozenset(
    "a al algo ante cada como con cual cuales cuando cuanta cuantas cuanto cuantos de del desde "
    "donde dos el ella en entre era es esa ese esta este esto ha hay la las le lo los mas me mi "
    "ni no nos o para pero por que quien se sea segun si sin sobre son su sus tambien tiene un "
    "una uno unos y ya tras hasta debe puede se".split()
)


def normalizar(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in sin_tildes if not unicodedata.combining(c))


def terminos(texto: str) -> list[str]:
    """Palabras útiles para comparar textos: sin tildes, sin palabras vacías y sin plural."""
    salida = []
    for bruto in re.findall(r"[a-z0-9]+(?:[-_.,/][a-z0-9]+)*", normalizar(texto)):
        partes = {bruto, *re.split(r"[-_.,/]", bruto)} if re.search(r"[-_.,/]", bruto) else {bruto}
        for t in partes:
            if t in _VACIAS or (len(t) < 2 and not t.isdigit()):
                continue
            if t.isalpha() and len(t) > 4:  # plural simple: peticiones → peticion
                t = t[:-2] if t.endswith("es") else t[:-1] if t.endswith("s") else t
            salida.append(t)
    return salida


def frases(texto: str) -> list[str]:
    return [f.strip() for f in re.split(r"(?<=[.;:])\s+", texto) if len(f.strip()) > 12]


# ----------------------------------------------------------------- perfil doble
class EmbeddingsDoble:
    """Vector de 768 posiciones construido con hashes de palabras. NO es un modelo semántico.

    Dos textos se parecen si comparten palabras. No entiende sinónimos ni paráfrasis: por eso
    sus cifras de recuperación no se pueden presentar como las de un modelo de embeddings.
    """

    nombre = "doble-hash-768"
    proveedor = "local (doble)"

    def __init__(self, dim: int = 768):
        self.dim = dim
        self.llamadas = 0

    def _vector(self, texto: str) -> list[float]:
        self.llamadas += 1
        v = [0.0] * self.dim
        cuenta: dict[str, int] = {}
        for t in terminos(texto):
            cuenta[t] = cuenta.get(t, 0) + 1
        for t, n in cuenta.items():
            h = int.from_bytes(hashlib.sha256(t.encode()).digest()[:8], "big")
            v[h % self.dim] += (1.0 if (h >> 40) & 1 else -1.0) * (1.0 + math.log(n))
        norma = math.sqrt(sum(x * x for x in v))
        return [x / norma for x in v] if norma else v

    def incrustar_documento(self, titulo: str, texto: str) -> list[float]:
        return self._vector(f"{titulo}. {texto}")

    def incrustar_consulta(self, texto: str) -> list[float]:
        return self._vector(texto)


class GeneradorDoble:
    """Copia del contexto las dos frases que más palabras comparten con la pregunta.

    No redacta ni razona. Permite probar formato, fuentes, rechazo y errores sin gastar.
    """

    nombre = "doble-extractivo"
    proveedor = "local (doble)"

    def __init__(self):
        self.llamadas = 0

    def generar(self, pregunta: str, contextos: list[tuple[str, str]], prompt_version: str) -> Generacion:
        self.llamadas += 1
        buscados = set(terminos(pregunta))
        candidatas = []
        for orden, (documento_id, contenido) in enumerate(contextos):
            for frase in frases(contenido):
                comunes = len(buscados & set(terminos(frase)))
                candidatas.append((comunes, -orden, frase, documento_id))
        candidatas.sort(reverse=True)
        elegidas = [c for c in candidatas[:2] if c[0] >= 2]
        if not elegidas:
            return Generacion(NO_CONSTA, None, None)
        texto = " ".join(f"{frase} [{doc}]" for _, _, frase, doc in elegidas)
        return Generacion(texto, None, None)


# ----------------------------------------------------------------- perfil real (Gemini)
def _cliente_gemini():
    clave = os.environ.get("GEMINI_API_KEY", "").strip()
    if not clave:
        raise ErrorConfiguracion("Falta GEMINI_API_KEY para el perfil real")
    from google import genai

    return genai.Client(api_key=clave)


class EmbeddingsGemini:
    """Embeddings de Gemini. Una petición por texto y siempre con la dimensión del esquema."""

    proveedor = "Gemini API"

    def __init__(self, modelo: str, dim: int, cliente=None):
        self.nombre, self.dim = modelo, dim
        self._cliente = cliente or _cliente_gemini()
        self.llamadas = 0

    def _incrustar(self, texto: str, tarea: str | None) -> list[float]:
        from google.genai import types

        opciones = {"output_dimensionality": self.dim}
        if tarea:  # solo gemini-embedding-001 admite task_type
            opciones["task_type"] = tarea
        try:
            r = self._cliente.models.embed_content(
                model=self.nombre, contents=texto, config=types.EmbedContentConfig(**opciones)
            )
        except Exception as exc:  # el error del proveedor sube tal cual, con su tipo
            raise ErrorProveedor(f"embeddings: {type(exc).__name__}") from exc
        self.llamadas += 1
        valores = list(r.embeddings[0].values)
        if len(valores) != self.dim:
            raise ErrorProveedor(f"embeddings: llegaron {len(valores)} dimensiones, no {self.dim}")
        return valores

    def incrustar_documento(self, titulo: str, texto: str) -> list[float]:
        if self.nombre.startswith("gemini-embedding-2"):
            # Embedding 2 no acepta task_type: la tarea va como prefijo (documentación de Google).
            return self._incrustar(f"title: {titulo} | text: {texto}", None)
        return self._incrustar(f"{titulo}\n{texto}", "RETRIEVAL_DOCUMENT")

    def incrustar_consulta(self, texto: str) -> list[float]:
        if self.nombre.startswith("gemini-embedding-2"):
            return self._incrustar(f"task: question answering | query: {texto}", None)
        return self._incrustar(texto, "RETRIEVAL_QUERY")


INSTRUCCIONES = {
    "v1": (
        "Eres el asistente de soporte de AetherCloud, una plataforma ficticia. Responde en "
        "español y solo con la información de los fragmentos. Tras cada dato cita su fuente "
        "con el identificador del documento entre corchetes, por ejemplo "
        "[05-sla-y-creditos-servicio]. Si los fragmentos no contienen la respuesta, responde "
        f"exactamente {NO_CONSTA} y nada más."
    ),
}
# v2 = v1 + UNA instrucción. Es la única diferencia entre los prompts de la comparación A/B.
INSTRUCCIONES["v2"] = INSTRUCCIONES["v1"] + (
    " Si solo puedes responder una parte de la pregunta, responde esa parte y di "
    "expresamente qué dato no aparece en los fragmentos."
)


def componer_prompt(pregunta: str, contextos: list[tuple[str, str]]) -> str:
    bloques = "\n\n".join(f"[{doc}]\n{contenido}" for doc, contenido in contextos)
    return f"FRAGMENTOS\n{bloques}\n\nPREGUNTA\n{pregunta}"


class GeneradorGemini:
    proveedor = "Gemini API"

    def __init__(self, modelo: str, cliente=None, max_tokens: int = 1024):
        self.nombre, self.max_tokens = modelo, max_tokens
        self._cliente = cliente or _cliente_gemini()
        self.llamadas = 0

    def generar(self, pregunta: str, contextos: list[tuple[str, str]], prompt_version: str) -> Generacion:
        from google.genai import types

        if prompt_version not in INSTRUCCIONES:
            raise ErrorConfiguracion(f"prompt_version desconocida: {prompt_version}")
        try:
            r = self._cliente.models.generate_content(
                model=self.nombre,
                contents=componer_prompt(pregunta, contextos),
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCCIONES[prompt_version],
                    temperature=0,
                    max_output_tokens=self.max_tokens,
                ),
            )
        except Exception as exc:
            raise ErrorProveedor(f"generación: {type(exc).__name__}") from exc
        self.llamadas += 1
        uso = getattr(r, "usage_metadata", None)
        entrada = getattr(uso, "prompt_token_count", None)
        salida = getattr(uso, "candidates_token_count", None)
        pensamiento = getattr(uso, "thoughts_token_count", None)
        if salida is not None and pensamiento:
            salida += pensamiento  # los tokens de razonamiento se facturan como salida
        model_version = getattr(r, "model_version", None) or None
        return Generacion((r.text or "").strip(), entrada, salida, model_version)


# ----------------------------------------------------------------- fábrica
@dataclass
class Proveedores:
    embeddings: object
    generador: object


def crear_proveedores(cfg: Config, execute: bool = False) -> Proveedores:
    """Construye los proveedores del perfil configurado. El real exige `--execute`."""
    if cfg.perfil == "doble":
        return Proveedores(EmbeddingsDoble(cfg.embedding_dim), GeneradorDoble())
    if not execute:
        raise ErrorConfiguracion(
            "El perfil real consume la API de Gemini: repite el comando con --execute "
            "cuando el gasto esté autorizado. No se usa el doble en su lugar."
        )
    cliente = _cliente_gemini()
    return Proveedores(
        EmbeddingsGemini(cfg.embedding_modelo, cfg.embedding_dim, cliente),
        GeneradorGemini(cfg.gen_modelo, cliente),
    )
