"""Comparación A/B: dos configuraciones que difieren en UNA sola variable.

Si cambian dos cosas a la vez no se puede saber cuál explica la diferencia. Antes de
construir la tabla se comprueba: mismo test, mismo perfil, mismos modelos, mismo evaluador
y exactamente una variable distinta.
"""

from __future__ import annotations

from evaluacion.informe import _f
from evaluacion.regresion import leer_ruta
from rag.config import VARIABLES_COMPARABLES

FILAS = (
    ("precision@5", "recuperacion.precision_at_5"),
    ("recall@5", "recuperacion.recall_at_5"),
    ("rechazos correctos (tasa)", "rechazo.tasa_rechazos_correctos"),
    ("abstenciones incorrectas (tasa)", "rechazo.tasa_abstenciones_incorrectas"),
    ("aciertos por criterio (tasa)", "correccion.tasa_aciertos"),
    ("faithfulness (media)", "generacion.faithfulness.media"),
    ("faithfulness (cobertura)", "generacion.faithfulness.cobertura"),
    ("answer_relevancy (media)", "generacion.answer_relevancy.media"),
    ("answer_relevancy (cobertura)", "generacion.answer_relevancy.cobertura"),
    ("latencia mediana (ms)", "operacion.latencia_ms_mediana"),
    ("latencia p95 (ms)", "operacion.produccion.latencia_ms_p95"),
    ("coste por consulta (USD)", "operacion.produccion.coste_usd_por_consulta"),
    ("coste del sistema (USD)", "operacion.sistema.coste_usd_estimado"),
    ("coste del evaluador (USD)", "operacion.evaluador.coste_usd_estimado"),
)


class ComparacionInvalida(Exception):
    pass


def variable_cambiada(a: dict, b: dict) -> str:
    for campo in ("conjunto", "huella_conjunto", "perfil", "n_casos"):
        if a[campo] != b[campo]:
            raise ComparacionInvalida(f"las dos ejecuciones no comparten {campo}")
    # El modelo de embeddings debe ser el mismo (otro modelo = otro índice y otro umbral).
    # El de generación puede ser LA variable comparada: lo comprueba la configuración de abajo.
    if a["modelos"].get("embeddings") != b["modelos"].get("embeddings"):
        raise ComparacionInvalida("las dos ejecuciones no comparten el modelo de embeddings")
    ev_a = (a.get("generacion") or {}).get("evaluador")
    ev_b = (b.get("generacion") or {}).get("evaluador")
    if ev_a != ev_b:
        raise ComparacionInvalida("las dos ejecuciones no usan el mismo evaluador")
    distintas = [v for v in VARIABLES_COMPARABLES if a["config"][v] != b["config"][v]]
    otras = [
        k for k in a["config"] if k not in VARIABLES_COMPARABLES + ("config_id",) and a["config"][k] != b["config"].get(k)
    ]
    if otras:
        raise ComparacionInvalida(f"cambian parámetros que deben ser comunes: {otras}")
    if len(distintas) != 1:
        raise ComparacionInvalida(f"deben diferir en exactamente una variable y difieren en {len(distintas)}: {distintas}")
    return distintas[0]


def comparar(a: dict, b: dict) -> dict:
    variable = variable_cambiada(a, b)
    filas = []
    for nombre, ruta in FILAS:
        va, vb = leer_ruta(a, ruta), leer_ruta(b, ruta)
        delta = round(vb - va, 4) if va is not None and vb is not None else None
        filas.append({"metrica": nombre, "A": va, "B": vb, "delta": delta})
    estado_a = {d["caso_id"]: d["acierto"] for d in a["casos"]}
    cambios = [
        {"caso_id": d["caso_id"], "A": estado_a[d["caso_id"]], "B": d["acierto"]}
        for d in b["casos"]
        if estado_a[d["caso_id"]] != d["acierto"]
    ]
    return {
        "variable": variable,
        "valor_A": a["config"][variable],
        "valor_B": b["config"][variable],
        "run_A": a["run_id"],
        "run_B": b["run_id"],
        "conjunto": a["conjunto"],
        "n_casos": a["n_casos"],
        "perfil": a["perfil"],
        "aviso": a.get("aviso"),
        "filas": filas,
        "casos_que_cambian": cambios,
        "no_evaluables": {
            "A": (a.get("generacion") or {}).get("no_evaluables", []),
            "B": (b.get("generacion") or {}).get("no_evaluables", []),
        },
    }


def tabla_markdown(c: dict) -> str:
    lineas = [f"# Comparación A/B · variable `{c['variable']}`", ""]
    if c["aviso"]:
        lineas += [f"> **{c['aviso']}**", ""]
    lineas += [
        f"A = `{c['valor_A']}` (`{c['run_A']}`) · B = `{c['valor_B']}` (`{c['run_B']}`) · mismo "
        f"conjunto `{c['conjunto']}` de {c['n_casos']} casos, mismos modelos y mismo evaluador.",
        "",
        "| Métrica | A | B | B − A |",
        "|---|---:|---:|---:|",
    ]
    for f in c["filas"]:
        dec = "{:.1f}" if "ms" in f["metrica"] else "{:.6f}" if "USD" in f["metrica"] else "{:.2f}"
        signo = "sin dato" if f["delta"] is None else ("+" if f["delta"] > 0 else "") + _f(f["delta"], dec)
        lineas.append(f"| {f['metrica']} | {_f(f['A'], dec)} | {_f(f['B'], dec)} | {signo} |")
    lineas += ["", "## Casos cuyo resultado cambia", ""]
    if c["casos_que_cambian"]:
        lineas += ["| Caso | A | B |", "|---|---|---|"]
        lineas += [f"| {x['caso_id']} | {_ok(x['A'])} | {_ok(x['B'])} |" for x in c["casos_que_cambian"]]
    else:
        lineas.append("Ninguno.")
    for lado in ("A", "B"):
        if c["no_evaluables"][lado]:
            lineas += ["", f"## No evaluables en {lado}", ""]
            lineas += [f"- {n['caso_id']} · {n['metrica']} · {n['motivo']}" for n in c["no_evaluables"][lado]]
    lineas += [
        "",
        f"Con {c['n_casos']} preguntas, una diferencia pequeña puede ser ruido: es evidencia de "
        "laboratorio, no una prueba estadística.",
    ]
    return "\n".join(lineas) + "\n"


def _ok(valor) -> str:
    return {True: "acierta", False: "falla", None: "error del sistema"}[valor]
