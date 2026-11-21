"""Evaluador AISLADO de S19: Ragas 0.4.3 lee `respuestas.jsonl` y escribe `puntuaciones.jsonl`.

    uv run python evaluar.py ../resultados/mi-test-A                 juez doble (sin coste)
    uv run python evaluar.py ../resultados/mi-test-A --modo real --execute

Este entorno no importa el RAG ni el RAG importa Ragas: solo comparten archivos JSONL con
versión (`../evaluacion/intercambio.py`, que se carga por ruta y no depende de nada).

Dos modos que nunca se sustituyen entre sí:

- `doble`: las métricas son las clases REALES de `ragas.metrics.collections`, pero el juez y
  los embeddings son dobles locales deterministas. Comprueba el recorrido (formato, no
  evaluables, cobertura); sus cifras NO miden la calidad de ninguna respuesta.
- `real`: juez y embeddings de pago. Exige `--execute` y GEMINI_API_KEY.

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

os.environ.setdefault("RAGAS_DO_NOT_TRACK", "true")  # sin telemetría de uso desde el aula

from ragas.embeddings.base import BaseRagasEmbedding  # noqa: E402
from ragas.llms.base import InstructorBaseRagasLLM  # noqa: E402
from ragas.metrics.collections import AnswerRelevancy, Faithfulness  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
METRICAS = ("faithfulness", "answer_relevancy")
ENDPOINT_GEMINI_OPENAI = "https://generativelanguage.googleapis.com/v1beta/openai/"
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
    """Lee `../.env` sin pisar el entorno y sin imprimir nada."""
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
    """Cuenta llamadas y tokens leyendo el campo `usage` de cada respuesta HTTP del proveedor.

    Ragas no devuelve el consumo del juez. Sin este contador, el coste de evaluar quedaría
    invisible o mezclado con el del RAG.
    """

    def __init__(self):
        self.llamadas_llm = self.llamadas_embeddings = 0
        self.tokens_entrada = self.tokens_salida = 0
        self.sin_uso = 0  # respuestas del LLM que llegaron sin `usage`: el total deja de conocerse

    async def al_responder(self, respuesta) -> None:
        await respuesta.aread()
        try:
            uso = (respuesta.json() or {}).get("usage") or {}
        except (ValueError, AttributeError):
            uso = {}
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
        }


def crear_real(ruta: str, modelo: str, modelo_emb: str, max_tokens: int, clave: str, transporte=None):
    """Construye juez y embeddings reales. `transporte` solo se usa en tests (HTTP simulado).

    Hallazgo con ragas==0.4.3 (ver README): `llm_factory(provider="google", client=genai.Client())`
    devuelve un cliente SÍNCRONO y `ascore` falla con TypeError. Por eso las dos rutas de aquí
    son asíncronas.
    """
    from ragas.embeddings.base import embedding_factory
    from ragas.llms import llm_factory

    contador = ContadorUso()
    if ruta == "openai_compat":
        import httpx
        from openai import AsyncOpenAI

        http = httpx.AsyncClient(transport=transporte, timeout=60, event_hooks={"response": [contador.al_responder]})
        cliente = AsyncOpenAI(
            api_key=clave,
            http_client=http,
            max_retries=1,
            base_url=os.environ.get("S19_EVAL_BASE_URL", ENDPOINT_GEMINI_OPENAI),
        )
        llm = llm_factory(modelo, provider="openai", client=cliente, max_tokens=max_tokens)
        emb = embedding_factory("openai", model=modelo_emb, client=cliente, interface="modern")
        return llm, emb, contador
    if ruta == "google_genai":
        import instructor
        from google import genai
        from ragas.embeddings import GoogleEmbeddings
        from ragas.llms.base import InstructorLLM

        cliente = genai.Client(api_key=clave)
        llm = InstructorLLM(
            client=instructor.from_genai(cliente, use_async=True),
            model=modelo,
            provider="google",
            max_tokens=max_tokens,
        )
        emb = GoogleEmbeddings(client=cliente, model=modelo_emb)
        # Esta ruta no expone `usage`: se cuentan las llamadas, pero tokens y coste quedan
        # como desconocidos (None), no como cero.
        juzgar, incrustar, incrustar_varios = llm.agenerate, emb.aembed_text, emb.aembed_texts

        async def juzgar_contado(prompt, response_model):
            contador.llamadas_llm += 1
            contador.sin_uso += 1
            return await juzgar(prompt, response_model)

        async def incrustar_contado(text, **kw):
            contador.llamadas_embeddings += 1
            return await incrustar(text, **kw)

        async def incrustar_varios_contado(texts, **kw):
            contador.llamadas_embeddings += 1
            return await incrustar_varios(texts, **kw)

        llm.agenerate, emb.aembed_text, emb.aembed_texts = (juzgar_contado, incrustar_contado, incrustar_varios_contado)
        return llm, emb, contador
    raise SystemExit(f"S19_EVAL_RUTA desconocida: {ruta!r} (openai_compat | google_genai)")


# ------------------------------------------------------------------ evaluación
def _tarifa(modelo: str) -> dict | None:
    return json.loads((RAIZ / "tarifas.json").read_text(encoding="utf-8"))["modelos"].get(modelo)


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
            if contador:  # ruta con `usage`: llamadas y tokens medidos
                ahora = contador.foto()
                d = {k: ahora[k] - antes[k] for k in ahora}
                conocidos = d["sin_uso"] == 0
                entrada = d["tokens_entrada"] if conocidos else None
                salida_t = d["tokens_salida"] if conocidos else None
                coste = None
                if tarifa and conocidos:
                    coste = round((entrada * tarifa["entrada"] + salida_t * tarifa["salida"]) / 1e6, 8)
                consumo |= {
                    "llamadas_llm": d["llamadas_llm"],
                    "llamadas_embeddings": d["llamadas_embeddings"],
                    "tokens_entrada": entrada,
                    "tokens_salida": salida_t,
                    "coste_usd": coste,
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


def descripcion_evaluador(modo: str, ruta: str | None, llm: str, emb: str) -> dict:
    """Identidad del evaluador. Va en cada puntuación: dos ejecuciones solo son comparables
    si este bloque es idéntico."""
    return {
        "modo": modo,
        "ruta": ruta,
        "llm": llm,
        "embeddings": emb,
        "ragas": md.version("ragas"),
        "langchain_community": md.version("langchain-community"),
        "python": platform.python_version(),
        "aviso": AVISO_DOBLE if modo == "doble" else None,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Evaluador aislado de S19 (Ragas 0.4.3)")
    p.add_argument("carpeta", help="carpeta de una ejecución, con respuestas.jsonl")
    p.add_argument("--modo", choices=("doble", "real"), default="doble")
    p.add_argument("--execute", action="store_true", help="autoriza llamadas de pago (modo real)")
    p.add_argument("--timeout", type=float, default=90.0, help="segundos por métrica y caso")
    args = p.parse_args(argv)
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
        clave = os.environ.get("GEMINI_API_KEY", "").strip()
        if not args.execute or not clave:
            print(
                "ERROR · el modo real consume la API del juez: hace falta GEMINI_API_KEY y "
                "--execute. No se usa el juez doble en su lugar.",
                file=sys.stderr,
            )
            return 2
        ruta = os.environ.get("S19_EVAL_RUTA", "openai_compat")
        modelo = os.environ.get("S19_EVAL_LLM_MODEL", "gemini-3.8-flash")
        modelo_emb = os.environ.get("S19_EVAL_EMBEDDING_MODEL", "gemini-embedding-001")
        max_tokens = int(os.environ.get("S19_EVAL_MAX_TOKENS", "4096"))
        llm, emb, contador = crear_real(ruta, modelo, modelo_emb, max_tokens, clave)
        evaluador = descripcion_evaluador("real", ruta, modelo, modelo_emb)

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
