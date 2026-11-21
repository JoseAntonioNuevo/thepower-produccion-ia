"""Coste estimado a partir de tokens y de `tarifas.json` (fuente y fecha dentro del archivo).

Si no se conocen los tokens o el modelo no tiene tarifa, el coste es `None` (desconocido).
Un coste desconocido no es cero: no se rellena.
"""

from __future__ import annotations

import json
from functools import lru_cache

from rag.config import RAIZ


@lru_cache(maxsize=1)
def tarifas() -> dict:
    return json.loads((RAIZ / "tarifas.json").read_text(encoding="utf-8"))


def desglose_coste_usd(modelo: str, tokens_entrada: int | None, tokens_salida: int | None) -> dict[str, float] | None:
    """Desglose en USD (`input`, `output`, `total`) para Langfuse; None si falta tarifa o tokens."""
    precio = tarifas()["modelos"].get(modelo)
    if precio is None or tokens_entrada is None or tokens_salida is None:
        return None
    entrada = round(tokens_entrada * precio["entrada"] / 1e6, 8)
    salida = round(tokens_salida * precio["salida"] / 1e6, 8)
    total = round((tokens_entrada * precio["entrada"] + tokens_salida * precio["salida"]) / 1e6, 8)
    return {"input": entrada, "output": salida, "total": total}


def coste_usd(modelo: str, tokens_entrada: int | None, tokens_salida: int | None) -> float | None:
    desglose = desglose_coste_usd(modelo, tokens_entrada, tokens_salida)
    return None if desglose is None else desglose["total"]
