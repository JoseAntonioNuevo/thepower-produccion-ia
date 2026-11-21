"""Ejecuta un conjunto de preguntas y deja `respuestas.jsonl` + `manifiesto.json`.

Un caso que falla NO detiene el lote ni desaparece: queda con `error` y sin respuesta, y el
informe lo cuenta como error del sistema.
"""

from __future__ import annotations

import datetime as dt
import importlib.metadata as md
import json
from pathlib import Path

from evaluacion.conjuntos import huella_conjunto
from evaluacion.intercambio import RESPUESTAS, escribir_jsonl
from evaluacion.metricas import evaluar_caso
from rag.config import Config
from rag.consulta import responder
from rag.observabilidad import Trazador


def versiones() -> dict:
    """Versiones de las librerías que intervienen: forman parte del resultado."""
    salida = {}
    for paquete in ("psycopg", "google-genai", "langfuse"):
        try:
            salida[paquete] = md.version(paquete)
        except md.PackageNotFoundError:
            salida[paquete] = None
    return salida


def ejecutar_lote(
    cfg: Config,
    almacen,
    proveedores,
    indice_id: str,
    casos: list[dict],
    conjunto: str,
    carpeta: Path,
    run_id: str | None = None,
    trazador: Trazador | None = None,
) -> list[dict]:
    trazador = trazador or Trazador(None)
    run_id = run_id or f"{conjunto}-{cfg.config_id}-{cfg.perfil}-{dt.datetime.now():%Y%m%d-%H%M%S}"
    modelos = {"generacion": cfg.gen_modelo, "embeddings": cfg.embedding_modelo}
    filas = []
    for caso in casos:
        base = {
            "run_id": run_id,
            "config_id": cfg.config_id,
            "perfil": cfg.perfil,
            "conjunto": conjunto,
            "caso_id": caso["caso_id"],
            "user_input": caso["pregunta"],
            "modelos": modelos,
        }
        with trazador.consulta(run_id, caso["caso_id"], cfg, caso["pregunta"]) as traza:
            try:
                r = responder(cfg, almacen, proveedores, indice_id, caso["pregunta"], traza)
            except Exception as exc:  # se registra el tipo de fallo; no se sustituye la respuesta
                filas.append(
                    {
                        **base,
                        "response": None,
                        "retrieved_contexts": [],
                        "rechazo": False,
                        "motivo_rechazo": None,
                        "fuentes": [],
                        "fuentes_invalidas": [],
                        "avisos": [],
                        "documentos_recuperados": [],
                        "fragmentos_recuperados": [],
                        "mejor_similitud": None,
                        "latencia_ms": {},
                        "tokens": {},
                        "coste_usd": None,
                        "model_version": None,
                        "error": f"{type(exc).__name__}: {exc}",
                        "traza_id": traza.trace_id,
                    }
                )
                continue
            filas.append(
                {
                    **base,
                    "response": r.texto,
                    "retrieved_contexts": [c["contenido"] for c in r.contextos],
                    "rechazo": r.rechazo,
                    "motivo_rechazo": r.motivo_rechazo,
                    "fuentes": r.fuentes,
                    "fuentes_invalidas": r.fuentes_invalidas,
                    "avisos": r.avisos,
                    "documentos_recuperados": r.documentos_recuperados,
                    "fragmentos_recuperados": r.fragmentos_recuperados,
                    "mejor_similitud": r.mejor_similitud,
                    "latencia_ms": r.latencia_ms,
                    "tokens": r.tokens,
                    "coste_usd": r.coste_usd,
                    "model_version": r.model_version,
                    "error": None,
                    "traza_id": traza.trace_id,
                }
            )
            # Las métricas por caso se publican como puntuaciones de la traza.
            e = evaluar_caso(caso, filas[-1])
            traza.cerrar(
                salida={"respuesta": r.texto, "fuentes": r.fuentes, "rechazo": r.rechazo},
                metadatos={
                    "documentos_recuperados": r.documentos_recuperados,
                    "latencia_ms": r.latencia_ms,
                    "coste_usd_estimado": r.coste_usd,
                    "respondible": caso["respondible"],
                },
                puntuaciones={
                    "precision_at_5": e["precision_at_5"],
                    "recall_at_5": e["recall_at_5"],
                    "rechazo": float(r.rechazo),
                    "acierto_criterio": _num(e["acierto"]),
                },
            )
    escribir_jsonl(carpeta / "respuestas.jsonl", filas, RESPUESTAS)
    manifiesto = {
        "run_id": run_id,
        "creado": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "conjunto": conjunto,
        "huella_conjunto": huella_conjunto(casos),
        "n_casos": len(casos),
        "indice_id": indice_id,
        "config": cfg.publica(),
        "modelos": modelos,
        "versiones_modelo": sorted({f["model_version"] for f in filas if f.get("model_version")}),
        "versiones": versiones(),
        "llamadas": {"embeddings": proveedores.embeddings.llamadas, "generacion": proveedores.generador.llamadas},
        "langfuse": trazador.activo,
        "aviso": AVISO_DOBLE if cfg.perfil == "doble" else None,
    }
    (carpeta / "manifiesto.json").write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    trazador.cerrar()
    return filas


AVISO_DOBLE = (
    "PERFIL DOBLE: embeddings por hash de palabras y generador extractivo locales. "
    "Estas cifras comprueban el funcionamiento del sistema de evaluación; NO miden ningún modelo."
)


def _num(valor) -> float | None:
    return None if valor is None else float(valor)
