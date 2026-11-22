"""Catálogo de OpenRouter: precios y parámetros admitidos de los modelos que usa la demo.

    python s19.py catalogo                     modelos de .env, de las variantes y del juez
    python s19.py catalogo --modelo openai/gpt-6-luna

Lee la API PÚBLICA de OpenRouter (`/models` y `/embeddings/models`): no necesita clave ni
gasta nada. Escribe `tarifas.json` con fecha y fuente. Ese archivo sirve para:

- `estimar`: prever llamadas y coste ANTES de autorizar el gasto.
- Estimar el coste si una respuesta llega sin `usage.cost` (OpenRouter suele informarlo).
- `preflight`: avisar si un modelo no existe o no admite un parámetro que se le va a enviar
  (por ejemplo `temperature`, o `response_format`, que el juez de Ragas necesita).

Cada vez que se cambia un modelo en .env hay que volver a ejecutar `catalogo`.
"""

from __future__ import annotations

import datetime as dt
import difflib
import json
from pathlib import Path

from rag.config import RAIZ, ErrorConfiguracion

TARIFAS = RAIZ / "tarifas.json"
AVISO = (
    "Precios de OpenRouter leídos en la fecha indicada. Son los que OpenRouter publica para cada "
    "modelo; el coste real de cada llamada es el que devuelve la API en usage.cost. Vuelve a "
    "ejecutar `python s19.py catalogo` antes de gastar y cada vez que cambies un modelo."
)


def descargar(url_base: str, cliente_http=None) -> dict[str, dict]:
    """{id: ficha} con los modelos de chat y de embeddings del catálogo público."""
    import httpx

    http = cliente_http or httpx.Client(timeout=30)
    fichas: dict[str, dict] = {}
    for ruta, tipo in (("/models", "chat"), ("/embeddings/models", "embeddings")):
        try:
            r = http.get(url_base.rstrip("/") + ruta)
            r.raise_for_status()
        except httpx.HTTPError as exc:
            raise ErrorConfiguracion(f"No se pudo leer el catálogo de OpenRouter ({ruta}): {exc}") from exc
        for m in r.json().get("data", []):
            precio = m.get("pricing") or {}
            fichas[m["id"]] = {
                "tipo": "embeddings" if tipo == "embeddings" or "embeddings" in _salidas(m) else "chat",
                "entrada": _por_millon(precio.get("prompt")),
                "salida": _por_millon(precio.get("completion")) or 0.0,
                "contexto": m.get("context_length"),
                "parametros": sorted(m.get("supported_parameters") or []),
            }
    return fichas


def _salidas(m: dict) -> list[str]:
    return (m.get("architecture") or {}).get("output_modalities") or []


def _por_millon(valor) -> float | None:
    try:
        return round(float(valor) * 1_000_000, 6)
    except (TypeError, ValueError):
        return None


def actualizar(modelos: list[str], fichas: dict[str, dict], ruta: Path = TARIFAS) -> dict:
    """Añade o actualiza en `tarifas.json` las fichas de `modelos`. Un modelo que no existe es un error."""
    faltan = [m for m in modelos if m not in fichas]
    if faltan:
        pistas = {m: difflib.get_close_matches(m, list(fichas), n=3, cutoff=0.6) for m in faltan}
        detalle = "; ".join(f"{m} (¿quizá {', '.join(p) or 'ninguno parecido'}?)" for m, p in pistas.items())
        raise ErrorConfiguracion(f"OpenRouter no tiene estos modelos: {detalle}")
    actual = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    datos = {
        "consultado": dt.date.today().isoformat(),
        "fuente": "https://openrouter.ai/api/v1/models y /embeddings/models",
        "proveedor": "OpenRouter",
        "moneda": "USD",
        "unidad": "por 1.000.000 de tokens",
        "aviso": AVISO,
        "modelos": {**actual.get("modelos", {}), **{m: fichas[m] for m in modelos}},
    }
    datos["modelos"] = dict(sorted(datos["modelos"].items()))
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return datos


def avisos_parametros(ficha: dict | None, enviados: list[str]) -> list[str]:
    """Parámetros que se van a enviar y que el catálogo dice que el modelo no admite."""
    if not ficha or not ficha.get("parametros"):
        return []
    return [p for p in enviados if p not in ficha["parametros"]]
