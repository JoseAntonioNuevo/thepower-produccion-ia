"""Proveedores de embeddings y de generación.

Hay dos perfiles y NUNCA se mezclan ni se sustituyen entre sí:

- `doble`: código local determinista, sin red ni coste. Sirve para tests y para seguir la
  práctica sin claves. Sus resultados NO miden ningún modelo y van rotulados como tales.
- `real`: SIEMPRE OpenRouter (API compatible con OpenAI). Solo se construye con `--execute`
  y con OPENROUTER_API_KEY. Los modelos se eligen en .env y se cambian sin tocar el código.

Si el perfil real falla, el error se registra. No se cae al doble para «completar» el lote.
"""

from __future__ import annotations

import hashlib
import json
import math
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
    model_version: str | None = None  # modelo exacto que sirvió la API; None en perfil doble
    coste_usd: float | None = None  # coste real informado por OpenRouter; None si no lo dice
    proveedor_servido: str | None = None  # quién ejecutó el modelo dentro de OpenRouter
    fin: str | None = None  # finish_reason: "length" = se agotó el máximo de tokens


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


# ----------------------------------------------------------------- perfil real (OpenRouter)
class EmbeddingsOpenRouter:
    """Embeddings de cualquier modelo de OpenRouter (`S19_EMBEDDING_MODEL`).

    - Pide `dimensions` = S19_EMBEDDING_DIM si S19_EMBEDDING_ENVIAR_DIM=true. Si el modelo no
      admite reducir la dimensión, pon false y S19_EMBEDDING_DIM con su dimensión nativa.
    - Comprueba SIEMPRE la longitud recibida: un vector de otra dimensión es un error, no se recorta.
    - Las plantillas de .env deciden cómo se presenta el texto (algunos modelos esperan prefijos).
    """

    proveedor = "OpenRouter"

    def __init__(self, cfg: Config, cliente=None):
        self.nombre, self.dim, self.cfg = cfg.embedding_modelo, cfg.embedding_dim, cfg
        from rag.openrouter import cliente as crear_cliente
        from rag.openrouter import cuerpo_extra, json_env

        self._cliente = cliente or crear_cliente()
        self._extra = cuerpo_extra(cfg.embedding_proveedores or (), json_env("S19_EMBEDDING_EXTRA"))
        self.llamadas, self.coste_usd, self.coste_conocido = 0, 0.0, True

    def _incrustar(self, texto: str) -> list[float]:
        from rag.openrouter import leer_uso

        opciones = {"dimensions": self.dim} if self.cfg.embedding_enviar_dim else {}
        try:
            r = self._cliente.embeddings.create(
                model=self.nombre, input=texto, encoding_format="float", extra_body=self._extra or None, **opciones
            )
        except Exception as exc:  # el error del proveedor sube tal cual, con su tipo
            raise ErrorProveedor(f"embeddings: {type(exc).__name__}: {exc}") from exc
        self.llamadas += 1
        uso = leer_uso(r)
        if uso.coste_usd is None:
            self.coste_conocido = False
        else:
            self.coste_usd += uso.coste_usd
        if not getattr(r, "data", None):
            raise ErrorProveedor("embeddings: la respuesta no trae ningún vector")
        valores = list(r.data[0].embedding)
        if len(valores) != self.dim:
            raise ErrorProveedor(
                f"embeddings: {self.nombre} devolvió {len(valores)} dimensiones y S19_EMBEDDING_DIM={self.dim}. "
                f"Pon S19_EMBEDDING_DIM={len(valores)} (y S19_EMBEDDING_ENVIAR_DIM=false si el modelo no "
                "admite reducirla) y vuelve a ingestar."
            )
        return valores

    def incrustar_documento(self, titulo: str, texto: str) -> list[float]:
        return self._incrustar(self.cfg.plantilla_documento.format(titulo=titulo, texto=texto))

    def incrustar_consulta(self, texto: str) -> list[float]:
        return self._incrustar(self.cfg.plantilla_consulta.format(texto=texto))


class GeneradorOpenRouter:
    """Generación con cualquier modelo de chat de OpenRouter (`S19_GEN_MODEL`)."""

    proveedor = "OpenRouter"

    def __init__(self, cfg: Config, cliente=None):
        from rag.openrouter import cliente as crear_cliente
        from rag.openrouter import cuerpo_extra, json_env

        self.nombre, self.cfg = cfg.gen_modelo, cfg
        self._cliente = cliente or crear_cliente()
        extra = json.loads(cfg.gen_extra) if cfg.gen_extra else json_env("S19_GEN_EXTRA")
        self._extra = cuerpo_extra(cfg.gen_proveedores or (), extra)
        self.llamadas = 0

    def generar(self, pregunta: str, contextos: list[tuple[str, str]], prompt_version: str) -> Generacion:
        from rag.openrouter import leer_uso

        if prompt_version not in INSTRUCCIONES:
            raise ErrorConfiguracion(f"prompt_version desconocida: {prompt_version}")
        opciones = {"max_tokens": self.cfg.gen_max_tokens or 2048}
        if self.cfg.gen_temperatura is not None:
            opciones["temperature"] = self.cfg.gen_temperatura
        try:
            r = self._cliente.chat.completions.create(
                model=self.nombre,
                messages=[
                    {"role": "system", "content": INSTRUCCIONES[prompt_version]},
                    {"role": "user", "content": componer_prompt(pregunta, contextos)},
                ],
                extra_body=self._extra or None,
                **opciones,
            )
        except Exception as exc:
            raise ErrorProveedor(f"generación: {type(exc).__name__}: {exc}") from exc
        self.llamadas += 1
        if not getattr(r, "choices", None):
            raise ErrorProveedor("generación: la respuesta no trae ninguna opción")
        uso = leer_uso(r)
        return Generacion(
            (r.choices[0].message.content or "").strip(),
            uso.tokens_entrada,
            uso.tokens_salida,
            fin=getattr(r.choices[0], "finish_reason", None),
            model_version=uso.modelo_servido,
            coste_usd=uso.coste_usd,
            proveedor_servido=uso.proveedor_servido,
        )


INSTRUCCIONES = {
    "v1": (
        "Eres el asistente de soporte de AetherCloud, una plataforma ficticia. Responde en "
        "español y solo con la información de los fragmentos. Tras cada dato cita su fuente "
        "con el identificador del documento entre corchetes, por ejemplo "
        "[05-sla-y-creditos-servicio]. Si los fragmentos no contienen la respuesta, responde "
        f"exactamente {NO_CONSTA} y nada más."
    ),
    # Variante deliberadamente defectuosa para ensayar el control de regresión de S19.
    "regresion-rechazo": f"Ante cualquier pregunta, responde exactamente {NO_CONSTA} y nada más.",
}
# v2 = v1 + UNA instrucción. Es la única diferencia entre los prompts de la comparación A/B.
INSTRUCCIONES["v2"] = INSTRUCCIONES["v1"] + (
    " Si solo puedes responder una parte de la pregunta, responde esa parte y di "
    "expresamente qué dato no aparece en los fragmentos."
)


def componer_prompt(pregunta: str, contextos: list[tuple[str, str]]) -> str:
    bloques = "\n\n".join(f"[{doc}]\n{contenido}" for doc, contenido in contextos)
    return f"FRAGMENTOS\n{bloques}\n\nPREGUNTA\n{pregunta}"


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
            "El perfil real consume la API de OpenRouter: repite el comando con --execute "
            "cuando el gasto esté autorizado. No se usa el doble en su lugar."
        )
    from rag.openrouter import cliente

    compartido = cliente()
    return Proveedores(EmbeddingsOpenRouter(cfg, compartido), GeneradorOpenRouter(cfg, compartido))
