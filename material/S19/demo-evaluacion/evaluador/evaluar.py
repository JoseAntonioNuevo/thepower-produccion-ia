"""Evaluador AISLADO de S19: Ragas 0.4.3 lee `respuestas.jsonl` y escribe `puntuaciones.jsonl`.

    uv run python evaluar.py ../resultados/mi-test-A                 juez doble (sin coste)
    uv run python evaluar.py ../resultados/mi-test-A --modo real --execute

Este entorno no importa el RAG ni el RAG importa Ragas: solo comparten archivos JSONL con
versión (`../evaluacion/intercambio.py`, que se carga por ruta y no depende de nada).

Dos modos que nunca se sustituyen entre sí:

- `doble`: las métricas son las clases REALES de `ragas.metrics.collections`, pero el juez y
  los embeddings son dobles locales deterministas. Comprueba el recorrido (formato, no
  evaluables, cobertura); sus cifras NO miden la calidad de ninguna respuesta.
- `real`: juez y embeddings de pago, SIEMPRE a través de OpenRouter. Exige `--execute` y
  OPENROUTER_API_KEY. Los modelos se eligen en `../.env` (S19_EVAL_LLM_MODEL, S19_EVAL_EMBEDDING_MODEL).

Lo que no se puede puntuar (rechazo, error, respuesta o contexto vacío, fallo del juez, NaN)
se escribe como NO EVALUABLE con su motivo. Nunca se convierte en acierto ni en cero.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.metadata as md
import importlib.util
import json
import math
import os
import platform
import re
import sys
import time
import unicodedata
from pathlib import Path

import httpx

os.environ.setdefault("RAGAS_DO_NOT_TRACK", "true")  # sin telemetría de uso desde el aula

from ragas.embeddings.base import BaseRagasEmbedding  # noqa: E402
from ragas.llms.base import InstructorBaseRagasLLM  # noqa: E402
from ragas.metrics.collections import AnswerRelevancy, Faithfulness  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
METRICAS = ("faithfulness", "answer_relevancy")
URL_OPENROUTER = "https://openrouter.ai/api/v1"
# Valores por defecto del juez; deben coincidir con rag/config.py (lo comprueba un test del RAG).
EVAL_LLM_MODELO_DEFECTO = "anthropic/claude-opus-5.5"
EVAL_EMBEDDING_MODELO_DEFECTO = "openai/text-embedding-3-small"
AVISO_DOBLE = (
    "JUEZ DOBLE: métricas de Ragas ejecutadas con un juez y unos embeddings locales "
    "deterministas. Comprueban el recorrido de la evaluación; NO miden ninguna respuesta."
)


def _cargar_intercambio():
    """Carga el contrato JSONL por ruta: es el único código compartido con el RAG."""
    ruta = RAIZ / "evaluacion" / "intercambio.py"
    spec = importlib.util.spec_from_file_location("s19_intercambio", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


intercambio = _cargar_intercambio()


def cargar_env(ruta: Path | None = None) -> None:
    """Lee `../.env` (o el archivo de S19_ENV_FILE / `--env`) sin pisar el entorno ni imprimir nada."""
    elegido = os.environ.get("S19_ENV_FILE", "").strip()
    if ruta is None and elegido:
        ruta = Path(elegido).expanduser()
        ruta = ruta if ruta.is_absolute() else RAIZ / ruta
        if not ruta.exists():
            raise SystemExit(f"No existe el archivo de entorno {ruta} (S19_ENV_FILE)")
    ruta = ruta or RAIZ / ".env"
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#") and "=" in linea:
            clave, valor = linea.split("=", 1)
            os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


# ------------------------------------------------------------------ juez doble
def _palabras(texto: str) -> list[str]:
    plano = unicodedata.normalize("NFKD", texto.lower())
    plano = "".join(c for c in plano if not unicodedata.combining(c))
    return [p for p in re.findall(r"[a-z0-9]+", plano) if len(p) > 3 or p.isdigit()]


def _sin_citas(texto: str) -> str:
    return re.sub(r"\s*\[\d{2}-[a-z0-9-]+\]", "", texto).strip()


class JuezDoble(InstructorBaseRagasLLM):
    """Doble del juez: devuelve las estructuras que Ragas pide, sin modelo ni red.

    - Afirmaciones = frases de la respuesta. Una afirmación «se apoya» en el contexto si al
      menos el 80 % de sus palabras aparecen en él. No entiende paráfrasis ni negaciones.
    - Pregunta generada = el propio texto de la respuesta.
    """

    def __init__(self):
        self.llamadas = 0
        self.fila: dict = {}

    def generate(self, prompt, response_model):
        raise TypeError("el juez doble solo se usa con agenerate()")

    async def agenerate(self, prompt, response_model):
        self.llamadas += 1
        nombre = response_model.__name__
        respuesta = _sin_citas(self.fila.get("response") or "")
        if nombre == "StatementGeneratorOutput":
            frases = [f.strip() for f in re.split(r"(?<=[.;:])\s+", respuesta) if len(f.strip()) > 12]
            self._afirmaciones = frases
            return response_model(statements=frases)
        if nombre == "NLIStatementOutput":
            contexto = set(_palabras(" ".join(self.fila.get("retrieved_contexts") or [])))
            veredictos = []
            for frase in self._afirmaciones:
                palabras = _palabras(frase)
                apoyo = sum(p in contexto for p in palabras) / len(palabras) if palabras else 0.0
                veredictos.append({"statement": frase, "reason": f"apoyo léxico {apoyo:.2f}", "verdict": int(apoyo >= 0.8)})
            return response_model(statements=veredictos)
        if nombre == "AnswerRelevanceOutput":
            return response_model(question=respuesta, noncommittal=0)
        raise ValueError(f"el juez doble no conoce {nombre}")


class EmbeddingsDoble(BaseRagasEmbedding):
    """Vector por hash de palabras. NO es un modelo semántico."""

    def __init__(self, dim: int = 256):
        super().__init__()
        self.dim, self.llamadas = dim, 0

    def embed_text(self, text: str, **_) -> list[float]:
        self.llamadas += 1
        v = [0.0] * self.dim
        for p in _palabras(text):
            h = int.from_bytes(hashlib.sha256(p.encode()).digest()[:8], "big")
            v[h % self.dim] += 1.0 if (h >> 40) & 1 else -1.0
        if not any(v):
            v[0] = 1.0  # texto sin palabras útiles: vector no nulo para que el coseno exista
        return v

    async def aembed_text(self, text: str, **kw) -> list[float]:
        return self.embed_text(text, **kw)


# ------------------------------------------------------------------ juez real
class ContadorUso:
    """Cuenta llamadas, tokens y coste leyendo el campo `usage` de cada respuesta de OpenRouter.

    Ragas no devuelve el consumo del juez. Sin este contador, el coste de evaluar quedaría
    invisible o mezclado con el del RAG. OpenRouter añade `usage.cost`: lo que cobró.
    """

    def __init__(self):
        self.llamadas_llm = self.llamadas_embeddings = 0
        self.tokens_entrada = self.tokens_salida = 0
        self.sin_uso = 0  # respuestas del LLM que llegaron sin `usage`: el total deja de conocerse
        self.coste_usd = 0.0
        self.sin_coste = 0  # respuestas (LLM o embeddings) sin `usage.cost`

    async def al_responder(self, respuesta) -> None:
        await respuesta.aread()
        try:
            uso = (respuesta.json() or {}).get("usage") or {}
        except (ValueError, AttributeError):
            uso = {}
        # Con BYOK, `cost` es solo la comisión de OpenRouter y la inferencia la factura el
        # proveedor: viene en cost_details.upstream_inference_cost y se suma (ver rag/openrouter.py).
        coste = uso.get("cost")
        if uso.get("is_byok") and isinstance(coste, (int, float)):
            upstream = (uso.get("cost_details") or {}).get("upstream_inference_cost")
            coste = coste + upstream if isinstance(upstream, (int, float)) else None
        if isinstance(coste, (int, float)) and not isinstance(coste, bool):
            self.coste_usd += float(coste)
        else:
            self.sin_coste += 1
        if "/embeddings" in str(respuesta.request.url):
            self.llamadas_embeddings += 1
            return
        self.llamadas_llm += 1
        if "prompt_tokens" not in uso:
            self.sin_uso += 1
            return
        self.tokens_entrada += int(uso.get("prompt_tokens") or 0)
        # total − entrada incluye los tokens de razonamiento, que se facturan como salida.
        total = uso.get("total_tokens")
        salida = (total - uso["prompt_tokens"]) if total else uso.get("completion_tokens") or 0
        self.tokens_salida += int(salida)

    def foto(self) -> dict:
        return {
            "llamadas_llm": self.llamadas_llm,
            "llamadas_embeddings": self.llamadas_embeddings,
            "tokens_entrada": self.tokens_entrada,
            "tokens_salida": self.tokens_salida,
            "sin_uso": self.sin_uso,
            "coste_usd": self.coste_usd,
            "sin_coste": self.sin_coste,
        }


def _lista(texto: str) -> list[str]:
    return [p.strip() for p in (texto or "").split(",") if p.strip()]


def _json(nombre: str) -> dict:
    texto = os.environ.get(nombre, "").strip()
    if not texto:
        return {}
    valor = json.loads(texto)
    if not isinstance(valor, dict):
        raise SystemExit(f"{nombre} debe ser un objeto JSON")
    return valor


def ajustes_desde_entorno() -> dict:
    """Todo lo que cambia el comportamiento del juez real, leído de ../.env."""
    return {
        "llm_proveedores": _lista(os.environ.get("S19_EVAL_LLM_PROVEEDORES", "")),
        "embedding_proveedores": _lista(os.environ.get("S19_EVAL_EMBEDDING_PROVEEDORES", "")),
        "llm_extra": _json("S19_EVAL_LLM_EXTRA"),
        "quitar_parametros": _lista(os.environ.get("S19_EVAL_QUITAR_PARAMETROS", "")),
    }


def _con_proveedores(cuerpo: dict, proveedores: list[str]) -> dict:
    if proveedores:
        cuerpo["provider"] = {**cuerpo.get("provider", {}), "order": proveedores, "allow_fallbacks": False}
    return cuerpo


class TransporteOpenRouter(httpx.AsyncBaseTransport):
    """Ajusta cada petición antes de enviarla a OpenRouter.

    Ragas construye las peticiones por dentro y no deja añadir campos propios de OpenRouter.
    Este transporte añade el orden de proveedores y los campos extra de .env, y quita los
    parámetros que el modelo no admita (Ragas siempre envía temperature y top_p).
    """

    def __init__(self, interno: httpx.AsyncBaseTransport, ajustes: dict):
        self._interno, self._ajustes = interno, ajustes

    async def handle_async_request(self, peticion: httpx.Request) -> httpx.Response:
        ruta = peticion.url.path
        if peticion.method == "POST" and (ruta.endswith("/chat/completions") or ruta.endswith("/embeddings")):
            cuerpo = json.loads(peticion.content or b"{}")
            if ruta.endswith("/embeddings"):
                cuerpo = _con_proveedores(cuerpo, self._ajustes.get("embedding_proveedores") or [])
            else:
                cuerpo = _con_proveedores(
                    {**cuerpo, **self._ajustes.get("llm_extra", {})}, self._ajustes.get("llm_proveedores") or []
                )
                for parametro in self._ajustes.get("quitar_parametros") or []:
                    cuerpo.pop(parametro, None)
            contenido = json.dumps(cuerpo).encode("utf-8")
            cabeceras = [(k, v) for k, v in peticion.headers.raw if k.lower() != b"content-length"]
            peticion = httpx.Request(
                peticion.method, peticion.url, headers=cabeceras, content=contenido, extensions=peticion.extensions
            )
        return await self._interno.handle_async_request(peticion)

    async def aclose(self) -> None:
        await self._interno.aclose()


def crear_real(
    modelo: str,
    modelo_emb: str,
    max_tokens: int,
    clave: str,
    ajustes: dict | None = None,
    transporte=None,
    url_base: str | None = None,
):
    """Construye juez y embeddings reales sobre OpenRouter. `transporte` solo se usa en tests.

    Ragas recibe un cliente `AsyncOpenAI` apuntando a OpenRouter: con ragas==0.4.3 la llamada
    asíncrona es obligatoria en `ascore`, y el adaptador de OpenAI pide la salida en JSON.
    """
    from openai import AsyncOpenAI
    from ragas.embeddings.base import embedding_factory
    from ragas.llms import llm_factory

    contador = ContadorUso()
    http = httpx.AsyncClient(
        transport=TransporteOpenRouter(transporte or httpx.AsyncHTTPTransport(), ajustes or {}),
        timeout=60,
        event_hooks={"response": [contador.al_responder]},
    )
    cliente = AsyncOpenAI(
        api_key=clave,
        http_client=http,
        max_retries=1,
        base_url=url_base or os.environ.get("S19_OPENROUTER_BASE_URL", "").strip() or URL_OPENROUTER,
    )
    llm = llm_factory(modelo, provider="openai", client=cliente, max_tokens=max_tokens)
    emb = embedding_factory("openai", model=modelo_emb, client=cliente, interface="modern")
    return llm, emb, contador


# ------------------------------------------------------------------ evaluación
def _tarifa(modelo: str) -> dict | None:
    return json.loads((RAIZ / "tarifas.json").read_text(encoding="utf-8"))["modelos"].get(modelo)


# Parámetros que Ragas envía siempre al juez (InstructorModelArgs de ragas 0.4.3).
PARAMETROS_RAGAS = ("temperature", "top_p")


def parametros_no_admitidos(modelo: str) -> list[str]:
    """Los que el catálogo de OpenRouter (tarifas.json) dice que el modelo no admite.

    Algunos modelos (por ejemplo varios de Anthropic) rechazan temperature y top_p. Sin ficha
    o sin lista de parámetros no se quita nada: no se adivina.
    """
    ficha = _tarifa(modelo) or {}
    admitidos = ficha.get("parametros") or []
    return [p for p in PARAMETROS_RAGAS if admitidos and p not in admitidos]


def motivo_previo(fila: dict, metrica: str) -> str | None:
    """Casos que no se envían al juez: no hay nada que juzgar o falta una entrada obligatoria."""
    if fila.get("error"):
        return "error_sistema"
    if fila.get("rechazo"):
        return "rechazo_sin_respuesta"
    if not (fila.get("response") or "").strip():
        return "respuesta_vacia"
    if metrica == "faithfulness" and not [c for c in fila.get("retrieved_contexts") or [] if c.strip()]:
        return "contexto_vacio"
    return None


async def puntuar(metrica, nombre: str, fila: dict, timeout: float) -> tuple[float | None, str | None]:
    """Llama a Ragas y lee `.value`. Devuelve (valor, None) o (None, motivo)."""
    try:
        if nombre == "faithfulness":
            llamada = metrica.ascore(
                user_input=fila["user_input"],
                response=fila["response"],
                retrieved_contexts=fila["retrieved_contexts"],
            )
        else:  # AnswerRelevancy no recibe contextos: compara la respuesta con la pregunta
            llamada = metrica.ascore(user_input=fila["user_input"], response=fila["response"])
        resultado = await asyncio.wait_for(llamada, timeout)
        valor = resultado.value
    except Exception as exc:  # el fallo del juez se registra con su tipo; no se reintenta en bucle
        return None, f"error_evaluador:{type(exc).__name__}"
    if not isinstance(valor, (int, float)) or isinstance(valor, bool) or not math.isfinite(valor):
        return None, "nan"
    return round(float(valor), 4), None


async def evaluar(
    filas: list[dict],
    llm,
    embeddings,
    evaluador: dict,
    contador=None,
    juez_doble: JuezDoble | None = None,
    timeout: float = 90.0,
) -> list[dict]:
    metricas = {
        "faithfulness": Faithfulness(llm=llm),
        "answer_relevancy": AnswerRelevancy(llm=llm, embeddings=embeddings),
    }
    tarifa = _tarifa(evaluador["llm"])
    salida = []
    for fila in filas:
        for nombre in METRICAS:
            base = {"run_id": fila["run_id"], "caso_id": fila["caso_id"], "metrica": nombre, "evaluador": evaluador}
            motivo = motivo_previo(fila, nombre)
            if motivo:
                salida.append(
                    {
                        **base,
                        "valor": None,
                        "evaluable": False,
                        "motivo": motivo,
                        "consumo": {
                            "llamadas_llm": 0,
                            "llamadas_embeddings": 0,
                            "tokens_entrada": 0,
                            "tokens_salida": 0,
                            "coste_usd": 0.0,
                            "segundos": 0.0,
                        },
                    }
                )
                continue
            antes = contador.foto() if contador else None
            if juez_doble is not None:
                juez_doble.fila, n_llm, n_emb = fila, juez_doble.llamadas, embeddings.llamadas
            t0 = time.perf_counter()
            valor, motivo = await puntuar(metricas[nombre], nombre, fila, timeout)
            consumo = {"segundos": round(time.perf_counter() - t0, 3)}
            if contador:  # juez real: llamadas, tokens y coste medidos en cada respuesta HTTP
                ahora = contador.foto()
                d = {k: ahora[k] - antes[k] for k in ahora}
                conocidos = d["sin_uso"] == 0
                entrada = d["tokens_entrada"] if conocidos else None
                salida_t = d["tokens_salida"] if conocidos else None
                coste, fuente = None, None
                if d["sin_coste"] == 0:  # lo que cobró OpenRouter (juez + embeddings del juez)
                    coste, fuente = round(d["coste_usd"], 8), "openrouter"
                elif tarifa and conocidos:  # sin usage.cost: estimación con tarifas.json (solo LLM)
                    coste = round((entrada * tarifa["entrada"] + salida_t * tarifa["salida"]) / 1e6, 8)
                    fuente = "tarifa"
                consumo |= {
                    "llamadas_llm": d["llamadas_llm"],
                    "llamadas_embeddings": d["llamadas_embeddings"],
                    "tokens_entrada": entrada,
                    "tokens_salida": salida_t,
                    "coste_usd": coste,
                    "coste_fuente": fuente,
                }
            else:  # doble: llamadas contadas, sin tokens ni coste
                consumo |= {
                    "llamadas_llm": juez_doble.llamadas - n_llm,
                    "llamadas_embeddings": embeddings.llamadas - n_emb,
                    "tokens_entrada": None,
                    "tokens_salida": None,
                    "coste_usd": None,
                }
            salida.append({**base, "valor": valor, "evaluable": motivo is None, "motivo": motivo, "consumo": consumo})
    return salida


def resumen(puntuaciones: list[dict]) -> dict:
    """Cobertura por métrica: evaluables / respuestas que había que juzgar."""
    datos = {}
    for nombre in METRICAS:
        filas = [p for p in puntuaciones if p["metrica"] == nombre]
        juzgables = [p for p in filas if p["motivo"] not in ("rechazo_sin_respuesta", "error_sistema")]
        ok = [p for p in juzgables if p["evaluable"]]
        motivos: dict[str, int] = {}
        for p in filas:
            if not p["evaluable"]:
                motivos[p["motivo"]] = motivos.get(p["motivo"], 0) + 1
        datos[nombre] = {
            "evaluables": len(ok),
            "esperados": len(juzgables),
            "cobertura": round(len(ok) / len(juzgables), 4) if juzgables else None,
            "media": round(sum(p["valor"] for p in ok) / len(ok), 4) if ok else None,
            "no_evaluables_por_motivo": motivos,
        }
    return datos


def descripcion_evaluador(modo: str, ruta: str | None, llm: str, emb: str, ajustes: dict | None = None) -> dict:
    """Identidad del evaluador. Va en cada puntuación: dos ejecuciones solo son comparables
    si este bloque es idéntico. `ruta` es "openrouter" en el modo real y None en el doble."""
    datos = {
        "modo": modo,
        "ruta": ruta,
        "llm": llm,
        "embeddings": emb,
        "ragas": md.version("ragas"),
        "langchain_community": md.version("langchain-community"),
        "python": platform.python_version(),
        "aviso": AVISO_DOBLE if modo == "doble" else None,
    }
    if ajustes:  # solo en el modo real: también cambian lo que puntúa el juez
        datos["ajustes"] = ajustes
    return datos


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Evaluador aislado de S19 (Ragas 0.4.3)")
    p.add_argument("carpeta", help="carpeta de una ejecución, con respuestas.jsonl")
    p.add_argument("--modo", choices=("doble", "real"), default="doble")
    p.add_argument("--execute", action="store_true", help="autoriza llamadas de pago (modo real)")
    p.add_argument("--timeout", type=float, default=90.0, help="segundos por métrica y caso")
    p.add_argument("--env", help="archivo de entorno en lugar de ../.env (p. ej. ../.env.sol-opus)")
    args = p.parse_args(argv)
    if args.env:
        os.environ["S19_ENV_FILE"] = str(Path(args.env).expanduser().resolve())
    cargar_env()
    carpeta = Path(args.carpeta)
    try:
        filas = intercambio.leer_jsonl(carpeta / "respuestas.jsonl", intercambio.RESPUESTAS)
    except intercambio.ErrorFormato as exc:
        print(f"ERROR · {exc}", file=sys.stderr)
        return 2

    contador = juez = None
    if args.modo == "doble":
        juez, emb = JuezDoble(), EmbeddingsDoble()
        llm = juez
        evaluador = descripcion_evaluador("doble", None, "doble-lexico", "doble-hash-256")
        print(f"⚠  {AVISO_DOBLE}\n")
    else:
        clave = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not args.execute or not clave:
            print(
                "ERROR · el modo real consume la API del juez en OpenRouter: hace falta "
                "OPENROUTER_API_KEY y --execute. No se usa el juez doble en su lugar.",
                file=sys.stderr,
            )
            return 2
        modelo = os.environ.get("S19_EVAL_LLM_MODEL", "").strip() or EVAL_LLM_MODELO_DEFECTO
        modelo_emb = os.environ.get("S19_EVAL_EMBEDDING_MODEL", "").strip() or EVAL_EMBEDDING_MODELO_DEFECTO
        max_tokens = int(os.environ.get("S19_EVAL_MAX_TOKENS", "").strip() or "4096")
        ajustes = {**ajustes_desde_entorno(), "max_tokens": max_tokens}
        automaticos = parametros_no_admitidos(modelo)
        if automaticos:
            print(f"Según tarifas.json, {modelo} no admite {automaticos}: se quitan de sus peticiones.")
            ajustes["quitar_parametros"] = sorted(set(ajustes["quitar_parametros"]) | set(automaticos))
        llm, emb, contador = crear_real(modelo, modelo_emb, max_tokens, clave, ajustes)
        evaluador = descripcion_evaluador("real", "openrouter", modelo, modelo_emb, ajustes)

    puntuaciones = asyncio.run(evaluar(filas, llm, emb, evaluador, contador, juez, args.timeout))
    intercambio.escribir_jsonl(carpeta / "puntuaciones.jsonl", puntuaciones, intercambio.PUNTUACIONES)
    datos = resumen(puntuaciones)
    (carpeta / "evaluador.json").write_text(
        json.dumps({"evaluador": evaluador, "resumen": datos}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Evaluador: ragas {evaluador['ragas']} · langchain-community "
        f"{evaluador['langchain_community']} · juez {evaluador['llm']}"
    )
    for nombre, d in datos.items():
        media = "sin dato" if d["media"] is None else f"{d['media']:.2f}"
        print(
            f"  {nombre:<17} media {media} · evaluables {d['evaluables']}/{d['esperados']} "
            f"· no evaluables: {d['no_evaluables_por_motivo'] or 'ninguno'}"
        )
    print(f"→ {carpeta}/puntuaciones.jsonl ({len(puntuaciones)} filas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
