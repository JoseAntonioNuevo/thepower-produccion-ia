"""Informe de una ejecución: recuperación, rechazo, corrección, generación y operación.

Cada bloque lleva su numerador y su denominador. Lo que no se pudo evaluar aparece con su
motivo y resta cobertura: nunca se convierte en acierto ni se elimina en silencio.
"""

from __future__ import annotations

import json
from pathlib import Path

from evaluacion.intercambio import PUNTUACIONES, RESPUESTAS, leer_jsonl
from evaluacion.metricas import evaluar_caso, media, mediana, percentil

INFORME = "s19.informe.v1"
METRICAS_GENERACION = ("faithfulness", "answer_relevancy")


def _tasa(numerador: int, denominador: int) -> float | None:
    return round(numerador / denominador, 4) if denominador else None


def _suma(valores: list) -> float | None:
    """Suma solo si se conocen TODOS los sumandos; si falta uno, el total es desconocido."""
    return None if any(v is None for v in valores) else round(sum(valores), 8)


def construir_informe(casos: list[dict], respuestas: list[dict], puntuaciones: list[dict] | None, manifiesto: dict) -> dict:
    por_caso = {f["caso_id"]: f for f in respuestas}
    faltan = [c["caso_id"] for c in casos if c["caso_id"] not in por_caso]
    if faltan:
        raise ValueError(f"el lote no contiene los casos {faltan}: no se informa de un test parcial")
    detalle = [evaluar_caso(c, por_caso[c["caso_id"]]) for c in casos]
    si = [d for d in detalle if d["respondible"] and not d["error_sistema"]]
    no = [d for d in detalle if not d["respondible"] and not d["error_sistema"]]
    errores = [d for d in detalle if d["error_sistema"]]
    n_si = sum(1 for c in casos if c["respondible"])
    n_no = len(casos) - n_si

    recuperacion = {
        "unidad": "documentos distintos; dos fragmentos del mismo documento = un acierto",
        "n_preguntas": len(si),
        "de_respondibles": n_si,
        "precision_at_5": media([d["precision_at_5"] for d in si]),
        "precision_techo": media([d["precision_techo"] for d in si]),
        "recall_at_5": media([d["recall_at_5"] for d in si]),
        "documentos_recuperados_media": media([float(d["n_documentos_recuperados"]) for d in si]),
        "denominadores": "precision@5: siempre 5 · recall@5: documentos de referencia de cada pregunta",
    }
    correctos = sum(1 for d in no if d["rechazo_correcto"])
    abstenciones = sum(1 for d in si if d["abstencion_incorrecta"])
    rechazo = {
        "rechazos_correctos": correctos,
        "de_sin_respuesta": n_no,
        "tasa_rechazos_correctos": _tasa(correctos, n_no),
        "respuestas_indebidas": sum(1 for d in no if d["respuesta_indebida"]),
        "abstenciones_incorrectas": abstenciones,
        "de_respondibles": n_si,
        "tasa_abstenciones_incorrectas": _tasa(abstenciones, n_si),
    }
    aciertos = sum(1 for d in si if d["acierto"])
    correccion = {
        "criterio": "datos clave presentes + cita de un documento de referencia (datos/criterios.md)",
        "aciertos": aciertos,
        "de_respondibles": n_si,
        "tasa_aciertos": _tasa(aciertos, n_si),
        "aviso": "comprobación automática de cadenas; la revisión manual decide los casos dudosos",
    }

    respondidas = [f for f in respuestas if not f["rechazo"] and not f["error"]]
    # Consultas que sí llamaron al modelo: las respondidas y también los rechazos DEL MODELO
    # («No consta»), que se pagan igual. Solo el rechazo previo (por umbral) no cuesta nada.
    con_modelo = [f for f in respuestas if _llamo_al_modelo(f)]
    latencias = [f["latencia_ms"].get("total") for f in respuestas if f.get("latencia_ms")]
    operacion = {
        "latencia_ms_mediana": mediana(latencias),
        "latencia_ms_maxima": max(latencias) if latencias else None,
        "sistema": {
            "llamadas": manifiesto.get("llamadas"),
            "tokens_entrada": _suma([f["tokens"].get("entrada") for f in con_modelo]),
            "tokens_salida": _suma([f["tokens"].get("salida") for f in con_modelo]),
            "coste_usd_estimado": _suma([f["coste_usd"] for f in con_modelo]),
            **_fuente_coste(con_modelo),
        },
        "evaluador": None,  # se rellena aparte: el consumo de juzgar no se mezcla con el de responder
    }

    generacion = None
    if puntuaciones is not None:
        generacion, operacion["evaluador"] = _generacion(puntuaciones, respondidas)
    operacion["produccion"] = _produccion(respuestas, latencias, len(errores), operacion, manifiesto)

    return {
        "schema_version": INFORME,
        "run_id": manifiesto["run_id"],
        "creado": manifiesto["creado"],
        "conjunto": manifiesto["conjunto"],
        "huella_conjunto": manifiesto["huella_conjunto"],
        "perfil": manifiesto["config"]["perfil"],
        "aviso": manifiesto.get("aviso"),
        "config": manifiesto["config"],
        "modelos": manifiesto["modelos"],
        "versiones": manifiesto["versiones"],
        "indice_id": manifiesto["indice_id"],
        "n_casos": len(casos),
        "n_respondidas": len(respondidas),
        "n_rechazos": sum(1 for f in respuestas if f["rechazo"]),
        "errores_sistema": [{"caso_id": d["caso_id"], "error": d["error_sistema"]} for d in errores],
        "n_errores_sistema": len(errores),
        "recuperacion": recuperacion,
        "rechazo": rechazo,
        "correccion": correccion,
        "generacion": generacion,
        "operacion": operacion,
        "casos": detalle,
    }


def _generacion(puntuaciones: list[dict], respondidas: list[dict]) -> tuple[dict, dict]:
    esperados = {f["caso_id"] for f in respondidas}  # solo se juzga lo que el sistema respondió
    salida: dict = {"no_evaluables": [], "no_aplica_por_rechazo": 0}
    for metrica in METRICAS_GENERACION:
        filas = [p for p in puntuaciones if p["metrica"] == metrica and p["caso_id"] in esperados]
        evaluables = [p for p in filas if p["evaluable"]]
        sin_fila = esperados - {p["caso_id"] for p in filas}
        salida["no_evaluables"] += [
            {"caso_id": p["caso_id"], "metrica": metrica, "motivo": p["motivo"]} for p in filas if not p["evaluable"]
        ] + [{"caso_id": c, "metrica": metrica, "motivo": "error_evaluador:sin_puntuacion"} for c in sorted(sin_fila)]
        salida[metrica] = {
            "media": media([p["valor"] for p in evaluables]),
            "n_evaluables": len(evaluables),
            "n_esperados": len(esperados),
            "cobertura": _tasa(len(evaluables), len(esperados)),
        }
    salida["no_aplica_por_rechazo"] = len({p["caso_id"] for p in puntuaciones if p["motivo"] == "rechazo_sin_respuesta"})
    salida["evaluador"] = puntuaciones[0]["evaluador"] if puntuaciones else None
    salida["aviso"] = "fidelidad al contexto no demuestra que la respuesta sea correcta"
    consumos = [p["consumo"] for p in puntuaciones]
    consumo = {
        "llamadas_llm": sum(c.get("llamadas_llm", 0) for c in consumos),
        "llamadas_embeddings": sum(c.get("llamadas_embeddings", 0) for c in consumos),
        "tokens_entrada": _suma([c.get("tokens_entrada") for c in consumos if c.get("llamadas_llm")]),
        "tokens_salida": _suma([c.get("tokens_salida") for c in consumos if c.get("llamadas_llm")]),
        "coste_usd_estimado": _suma([c.get("coste_usd") for c in consumos if c.get("llamadas_llm")]),
        "segundos": round(sum(c.get("segundos", 0) for c in consumos), 2),
    }
    return salida, consumo


def _llamo_al_modelo(fila: dict) -> bool:
    """Toda consulta sin error llama al generador salvo el rechazo previo (por umbral)."""
    return not fila["error"] and fila.get("motivo_rechazo") != "evidencia_insuficiente"


def _produccion(respuestas: list[dict], latencias: list, n_errores: int, operacion: dict, manifiesto: dict) -> dict:
    """Las cifras que se vigilan en producción, por consulta y no por caso del test.

    Coste por consulta = generación + embeddings de la pregunta, repartido entre TODAS las
    consultas (los rechazos previos cuentan con coste 0). Si falta un sumando, sin dato.
    """
    n = len(respuestas)
    generacion = operacion["sistema"]["coste_usd_estimado"]
    embeddings = manifiesto.get("coste_embeddings_usd")
    if manifiesto.get("config", {}).get("perfil") == "doble":
        embeddings = None  # el doble no tiene coste: no se inventa un 0 que parezca medido
    total = None if generacion is None or embeddings is None else generacion + embeddings
    por_consulta = round(total / n, 8) if total is not None and n else None
    juez = (operacion.get("evaluador") or {}).get("coste_usd_estimado")

    def _peso(juez: float | None, sistema: float | None) -> float | None:
        if juez is None or sistema is None or juez + sistema == 0:
            return None
        return round(juez / (juez + sistema), 4)

    return {
        "consultas": n,
        "latencia_ms_p50": mediana(latencias),
        "latencia_ms_p95": percentil(latencias, 95),
        "tasa_error": _tasa(n_errores, n),
        "tasa_rechazo": _tasa(sum(1 for f in respuestas if f["rechazo"]), n),
        "rechazos_sin_llamar_al_modelo": sum(1 for f in respuestas if f.get("motivo_rechazo") == "evidencia_insuficiente"),
        "llamadas_al_modelo": sum(1 for f in respuestas if _llamo_al_modelo(f)),
        "coste_usd_por_consulta": por_consulta,
        "coste_usd_por_1000_consultas": round(por_consulta * 1000, 4) if por_consulta is not None else None,
        "peso_del_juez": _peso(juez, total),
        "nota": "p95 por rango más cercano; coste = generación + embeddings de las preguntas; el juez va aparte",
    }


_ROTULO_COSTE = {
    "openrouter": "medido en cada respuesta de OpenRouter (con BYOK, lo factura el proveedor)",
    "tarifa": "estimación con tarifas.json",
    "mixta": "parte cobrado y parte estimado",
}


def _fuente_coste(respondidas: list[dict]) -> dict:
    """De dónde sale el coste del sistema. Sin datos (perfil doble) no se añade nada."""
    fuentes = {f.get("coste_fuente") for f in respondidas} - {None, "sin_llamada"}
    if not fuentes:
        return {}
    return {"coste_fuente": fuentes.pop() if len(fuentes) == 1 else "mixta"}


def cargar_ejecucion(carpeta: Path) -> tuple[list[dict], list[dict] | None, dict]:
    respuestas = leer_jsonl(carpeta / "respuestas.jsonl", RESPUESTAS)
    ruta = carpeta / "puntuaciones.jsonl"
    puntuaciones = leer_jsonl(ruta, PUNTUACIONES) if ruta.exists() else None
    manifiesto = json.loads((carpeta / "manifiesto.json").read_text(encoding="utf-8"))
    return respuestas, puntuaciones, manifiesto


def _f(valor, formato="{:.2f}") -> str:
    return "sin dato" if valor is None else formato.format(valor).replace(".", ",")


def tabla_markdown(inf: dict) -> str:
    r, z, c, g = inf["recuperacion"], inf["rechazo"], inf["correccion"], inf["generacion"]
    lineas = [f"# Informe · {inf['run_id']}", ""]
    if inf["aviso"]:
        lineas += [f"> **{inf['aviso']}**", ""]
    lineas += [
        f"Conjunto `{inf['conjunto']}` ({inf['n_casos']} casos, huella `{inf['huella_conjunto']}`) · "
        f"configuración `{inf['config']['config_id']}` · perfil `{inf['perfil']}` · "
        f"generación `{inf['modelos']['generacion']}` · embeddings `{inf['modelos']['embeddings']}`.",
        "",
        "| Bloque | Métrica | Valor | Sobre |",
        "|---|---|---:|---|",
        f"| Recuperación | precision@5 | {_f(r['precision_at_5'])} | {r['n_preguntas']} respondibles "
        f"(techo {_f(r['precision_techo'])}) |",
        f"| Recuperación | recall@5 | {_f(r['recall_at_5'])} | {r['n_preguntas']} respondibles |",
        f"| Rechazo | rechazos correctos | {z['rechazos_correctos']}/{z['de_sin_respuesta']} | sin respuesta |",
        f"| Rechazo | abstenciones incorrectas | {z['abstenciones_incorrectas']}/{z['de_respondibles']} | respondibles |",
        f"| Corrección | aciertos por criterio | {c['aciertos']}/{c['de_respondibles']} | respondibles |",
    ]
    if g:
        for m in METRICAS_GENERACION:
            lineas.append(
                f"| Generación | {m} | {_f(g[m]['media'])} | {g[m]['n_evaluables']}/{g[m]['n_esperados']} "
                f"evaluables (cobertura {_f(g[m]['cobertura'])}) |"
            )
    else:
        lineas.append("| Generación | faithfulness / answer_relevancy | sin dato | falta `puntuaciones.jsonl` |")
    o = inf["operacion"]
    lineas += [
        f"| Operación | latencia mediana | {_f(o['latencia_ms_mediana'], '{:.1f}')} ms | {inf['n_casos']} consultas |",
        f"| Operación | coste del sistema | {_f(o['sistema']['coste_usd_estimado'], '{:.6f}')} USD | "
        f"{_ROTULO_COSTE.get(o['sistema'].get('coste_fuente'), 'estimación')} |",
        f"| Operación | errores del sistema | {inf['n_errores_sistema']} | {inf['n_casos']} casos |",
    ]
    pr = o.get("produccion")
    if pr:
        pct = "sin dato" if pr["peso_del_juez"] is None else f"{pr['peso_del_juez'] * 100:.0f} %".replace(".", ",")
        lineas += [
            f"| Producción | latencia p95 | {_f(pr['latencia_ms_p95'], '{:.1f}')} ms | "
            f"{pr['consultas']} consultas (máxima {_f(o['latencia_ms_maxima'], '{:.1f}')} ms) |",
            f"| Producción | tasa de error | {_f(pr['tasa_error'])} | "
            f"{inf['n_errores_sistema']}/{pr['consultas']} consultas |",
            f"| Producción | tasa de rechazo | {_f(pr['tasa_rechazo'])} | {pr['rechazos_sin_llamar_al_modelo']} sin llamar "
            f"al modelo · {pr['llamadas_al_modelo']} llamadas al modelo |",
            f"| Producción | coste por consulta | {_f(pr['coste_usd_por_consulta'], '{:.6f}')} USD | generación + "
            f"embeddings · 1.000 consultas ≈ {_f(pr['coste_usd_por_1000_consultas'], '{:.2f}')} USD |",
            f"| Producción | peso del juez en el coste | {pct} | evaluar frente a responder |",
        ]
    if g and g["no_evaluables"]:
        lineas += ["", "## No evaluables", "", "| Caso | Métrica | Motivo |", "|---|---|---|"]
        lineas += [f"| {n['caso_id']} | {n['metrica']} | {n['motivo']} |" for n in g["no_evaluables"]]
    fallos = [d for d in inf["casos"] if d["acierto"] is False]
    if fallos:
        lineas += ["", "## Casos fallados (se conservan todos)", "", "| Caso | Qué pasó |", "|---|---|"]
        for d in fallos:
            if not d["respondible"]:
                que = "respondió una pregunta sin respuesta"
            elif d["rechazo"]:
                que = "se abstuvo en una pregunta respondible"
            elif d["datos_clave_ausentes"]:
                que = "faltan datos clave: " + ", ".join(d["datos_clave_ausentes"])
            else:
                que = "no cita ningún documento de referencia"
            lineas.append(f"| {d['caso_id']} | {que} |")
    return "\n".join(lineas) + "\n"
