"""Contrato de intercambio entre el RAG y el evaluador: JSONL con versión.

El RAG y Ragas viven en entornos distintos y no se importan entre sí. Solo comparten
archivos: una línea JSON por caso, con `schema_version`. Si el formato cambia, cambia la
versión y el lector antiguo falla con un mensaje claro en vez de leer mal.

    respuestas.jsonl    RAG → evaluador   (s19.respuestas.v1)
    puntuaciones.jsonl  evaluador → RAG   (s19.puntuaciones.v1)

Este archivo no depende de nada externo: el evaluador lo carga por ruta.
"""

from __future__ import annotations

import json
from pathlib import Path

RESPUESTAS = "s19.respuestas.v1"
PUNTUACIONES = "s19.puntuaciones.v1"
CASOS = "s19.casos.v1"

CAMPOS = {
    CASOS: {"caso_id", "pregunta", "respondible", "documentos_relevantes", "datos_clave"},
    # Campos obligatorios de s19.respuestas.v1. Los campos aditivos opcionales (como tokens,
    # coste_usd, model_version o traza_id) no rompen la lectura de archivos v1 existentes.
    RESPUESTAS: {
        "run_id",
        "config_id",
        "perfil",
        "conjunto",
        "caso_id",
        "user_input",
        "response",
        "retrieved_contexts",
        "rechazo",
        "documentos_recuperados",
        "error",
    },
    PUNTUACIONES: {"run_id", "caso_id", "metrica", "valor", "evaluable", "motivo", "evaluador", "consumo"},
}

# Motivos por los que una puntuación NO es evaluable. Ninguno se convierte en acierto ni en 0.
MOTIVOS_NO_EVALUABLE = (
    "rechazo_sin_respuesta",  # el sistema se abstuvo: no hay texto que juzgar (se mide aparte)
    "error_sistema",  # el RAG falló en ese caso
    "respuesta_vacia",
    "contexto_vacio",  # Faithfulness no existe sin contexto
    "error_evaluador",  # el juez falló: excepción, timeout, salida no válida…
    "nan",  # el juez devolvió «no es un número»
)


class ErrorFormato(Exception):
    """El archivo no cumple el contrato. No se intenta adivinar ni reparar."""


def escribir_jsonl(ruta: Path, filas: list[dict], esquema: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as f:
        for fila in filas:
            completa = {"schema_version": esquema, **fila}
            validar_fila(completa, esquema, origen=ruta.name)
            # allow_nan=False: un NaN no es JSON. Debe haberse convertido antes en «no evaluable».
            f.write(json.dumps(completa, ensure_ascii=False, allow_nan=False) + "\n")


def leer_jsonl(ruta: Path, esquema: str) -> list[dict]:
    if not ruta.exists():
        raise ErrorFormato(f"no existe {ruta}")
    filas = []
    for n, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip():
            continue
        try:
            fila = json.loads(linea)
        except json.JSONDecodeError as exc:
            raise ErrorFormato(f"{ruta.name}:{n} no es JSON válido") from exc
        validar_fila(fila, esquema, origen=f"{ruta.name}:{n}")
        filas.append(fila)
    return filas


def validar_fila(fila: dict, esquema: str, origen: str = "") -> None:
    version = fila.get("schema_version")
    if version != esquema:
        raise ErrorFormato(f"{origen}: se esperaba {esquema} y llegó {version!r}")
    faltan = CAMPOS[esquema] - fila.keys()
    if faltan:
        raise ErrorFormato(f"{origen}: faltan campos {sorted(faltan)}")
    if esquema == PUNTUACIONES:
        if fila["evaluable"] and not isinstance(fila["valor"], (int, float)):
            raise ErrorFormato(f"{origen}: una puntuación evaluable necesita un valor numérico")
        if not fila["evaluable"]:
            if fila["valor"] is not None:
                raise ErrorFormato(f"{origen}: una puntuación no evaluable no lleva valor")
            if str(fila["motivo"]).split(":")[0] not in MOTIVOS_NO_EVALUABLE:
                raise ErrorFormato(f"{origen}: motivo desconocido {fila['motivo']!r}")
