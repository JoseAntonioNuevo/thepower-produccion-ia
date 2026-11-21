"""Control de regresión: compara un informe con umbrales fijados de antemano.

Los umbrales se eligen con VALIDACIÓN y con margen, y se congelan antes de mirar el test.
Reglas del control:

- Un dato que falta, un NaN o una cobertura baja NO aprueban: «no lo sé» es un fallo.
- Los umbrales de un perfil no valen para otro (doble ≠ real).
- El informe debe contener todos los casos de su conjunto y ningún error del sistema.
"""

from __future__ import annotations

import datetime as dt
import math

UMBRALES = "s19.umbrales.v1"
MARGEN = 0.10
# Reglas que se derivan de la validación: (ruta en el informe, sentido).
REGLAS = (
    ("recuperacion.recall_at_5", "minimo"),
    ("recuperacion.precision_at_5", "minimo"),
    ("rechazo.tasa_rechazos_correctos", "minimo"),
    ("rechazo.tasa_abstenciones_incorrectas", "maximo"),
    ("correccion.tasa_aciertos", "minimo"),
    ("generacion.faithfulness.media", "minimo"),
    ("generacion.faithfulness.cobertura", "minimo"),
    ("generacion.answer_relevancy.media", "minimo"),
    ("generacion.answer_relevancy.cobertura", "minimo"),
)


def leer_ruta(informe: dict, ruta: str):
    valor = informe
    for clave in ruta.split("."):
        if not isinstance(valor, dict) or clave not in valor:
            return None
        valor = valor[clave]
    return valor


def derivar_umbrales(informe_validacion: dict, margen: float = MARGEN) -> dict:
    """Umbral = valor medido en validación ± margen. El margen absorbe la variación normal."""
    if informe_validacion["conjunto"] != "validacion":
        raise ValueError("los umbrales se eligen con validación, nunca con el test")
    reglas = []
    for ruta, sentido in REGLAS:
        valor = leer_ruta(informe_validacion, ruta)
        if valor is None:  # p. ej. sin evaluador no hay reglas de generación
            continue
        if sentido == "minimo":
            limite = max(0.0, math.floor((valor - margen) * 100) / 100)
        else:
            limite = min(1.0, math.ceil((valor + margen) * 100) / 100)
        reglas.append({"metrica": ruta, sentido: limite, "validacion": valor})
    return {
        "schema_version": UMBRALES,
        "perfil": informe_validacion["perfil"],
        "margen": margen,
        "fijado": dt.date.today().isoformat(),
        "origen": {
            "run_id": informe_validacion["run_id"],
            "conjunto": "validacion",
            "huella_conjunto": informe_validacion["huella_conjunto"],
            "n_casos": informe_validacion["n_casos"],
            "modelos": informe_validacion["modelos"],
        },
        "aviso": informe_validacion.get("aviso"),
        "reglas": reglas,
    }


def comprobar(informe: dict, umbrales: dict, n_casos_esperados: int | None = None) -> list[str]:
    """Devuelve la lista de fallos. Vacía = el control pasa."""
    fallos = []
    if umbrales.get("schema_version") != UMBRALES:
        return [f"umbrales con versión desconocida: {umbrales.get('schema_version')!r}"]
    if informe["perfil"] != umbrales["perfil"]:
        fallos.append(f"perfil del informe ({informe['perfil']}) ≠ perfil de los umbrales ({umbrales['perfil']})")
    if n_casos_esperados is not None and informe["n_casos"] != n_casos_esperados:
        fallos.append(f"el informe tiene {informe['n_casos']} casos y se esperaban {n_casos_esperados}")
    if informe["n_errores_sistema"]:
        fallos.append(f"{informe['n_errores_sistema']} casos con error del sistema")
    for regla in umbrales["reglas"]:
        ruta = regla["metrica"]
        valor = leer_ruta(informe, ruta)
        if valor is None or (isinstance(valor, float) and not math.isfinite(valor)):
            fallos.append(f"{ruta}: sin dato (no se puede dar por bueno lo que no se ha medido)")
        elif "minimo" in regla and valor < regla["minimo"]:
            fallos.append(f"{ruta}: {valor:.2f} < mínimo {regla['minimo']:.2f}")
        elif "maximo" in regla and valor > regla["maximo"]:
            fallos.append(f"{ruta}: {valor:.2f} > máximo {regla['maximo']:.2f}")
    return fallos
