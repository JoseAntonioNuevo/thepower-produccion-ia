"""Resultados DEGRADADOS A PROPÓSITO para probar que el control de regresión falla cuando debe.

Un control que nunca se ha visto fallar no demuestra nada. Este módulo copia una ejecución
buena y le introduce un fallo conocido; después se le pasa el mismo control.

    recuperacion  el buscador pierde su mejor documento en todas las preguntas
    sin-rechazo   el sistema deja de abstenerse y responde sin fuentes
    juez-caido    el evaluador falla en la mitad de las respuestas (baja la cobertura)
    incompleto    faltan los tres últimos casos del conjunto
"""

from __future__ import annotations

import json
from pathlib import Path

from evaluacion.intercambio import PUNTUACIONES, RESPUESTAS, escribir_jsonl, leer_jsonl

MODOS = ("recuperacion", "sin-rechazo", "juez-caido", "incompleto")


def degradar(origen: Path, destino: Path, modo: str) -> dict:
    if modo not in MODOS:
        raise ValueError(f"modo desconocido: {modo} (opciones: {', '.join(MODOS)})")
    respuestas = leer_jsonl(origen / "respuestas.jsonl", RESPUESTAS)
    ruta_p = origen / "puntuaciones.jsonl"
    puntuaciones = leer_jsonl(ruta_p, PUNTUACIONES) if ruta_p.exists() else None
    manifiesto = json.loads((origen / "manifiesto.json").read_text(encoding="utf-8"))
    run_id = f"{manifiesto['run_id']}-DEGRADADO-{modo}"

    if modo == "recuperacion":
        for f in respuestas:
            perdido = f["documentos_recuperados"][:1]
            f["documentos_recuperados"] = f["documentos_recuperados"][1:]
            f["fuentes"] = [d for d in f.get("fuentes", []) if d not in perdido]
    elif modo == "sin-rechazo":
        for f in respuestas:
            if f["rechazo"]:
                f.update(
                    rechazo=False,
                    motivo_rechazo=None,
                    fuentes=[],
                    avisos=["sin_fuentes"],
                    response="Según la documentación, sí está incluido en todos los planes.",
                )
    elif modo == "juez-caido":
        if puntuaciones is None:
            raise ValueError("juez-caido necesita puntuaciones.jsonl: evalúa antes la ejecución")
        juzgadas = sorted({p["caso_id"] for p in puntuaciones if p["evaluable"]})
        caidas = set(juzgadas[::2])  # uno de cada dos casos juzgados
        for p in puntuaciones:
            if p["caso_id"] in caidas:
                p.update(valor=None, evaluable=False, motivo="error_evaluador:TimeoutError")
    elif modo == "incompleto":
        respuestas = respuestas[:-3]

    for f in respuestas:
        f["run_id"] = run_id
    escribir_jsonl(destino / "respuestas.jsonl", _sin_version(respuestas), RESPUESTAS)
    if puntuaciones is not None:
        for p in puntuaciones:
            p["run_id"] = run_id
        if modo == "sin-rechazo":  # no se inventan notas para respuestas que el juez no vio
            puntuaciones = [p for p in puntuaciones if p["motivo"] != "rechazo_sin_respuesta"]
        escribir_jsonl(destino / "puntuaciones.jsonl", _sin_version(puntuaciones), PUNTUACIONES)
    manifiesto.update(
        run_id=run_id,
        degradado=modo,
        origen=manifiesto["run_id"],
        aviso=f"RESULTADO DEGRADADO A PROPÓSITO ({modo}) para probar el control de regresión. "
        "No es una medición. " + (manifiesto.get("aviso") or ""),
    )
    (destino / "manifiesto.json").write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifiesto


def _sin_version(filas: list[dict]) -> list[dict]:
    return [{k: v for k, v in f.items() if k != "schema_version"} for f in filas]
