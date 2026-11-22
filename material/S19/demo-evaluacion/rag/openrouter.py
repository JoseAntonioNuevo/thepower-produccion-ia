"""OpenRouter: el ÚNICO proveedor del perfil real.

OpenRouter expone modelos de OpenAI, Anthropic, Google y otros con una API compatible con la
de OpenAI. Cambiar de modelo es cambiar un nombre en `.env` (por ejemplo
`S19_GEN_MODEL=anthropic/claude-opus-5.5`); el código no cambia.

Este módulo reúne lo que comparten generación, embeddings y catálogo:

- La clave (`OPENROUTER_API_KEY`) y la URL base (`S19_OPENROUTER_BASE_URL`).
- Las preferencias de enrutado. Un mismo modelo puede servirlo más de un proveedor y eso es
  una variable más en una comparación. `S19_*_PROVEEDORES=Google,Vertex` fija el orden y
  desactiva los cambios automáticos, para que dos ejecuciones usen la misma infraestructura.
- Parámetros extra por petición (`S19_*_EXTRA` en JSON), para lo que no tiene variable propia.
- La lectura del uso: tokens, coste real cobrado (`usage.cost`), modelo y proveedor servidos.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

from rag.config import ErrorConfiguracion

URL_BASE = "https://openrouter.ai/api/v1"


def url_base() -> str:
    return os.environ.get("S19_OPENROUTER_BASE_URL", "").strip() or URL_BASE


def clave() -> str:
    valor = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not valor:
        raise ErrorConfiguracion("Falta OPENROUTER_API_KEY en .env para el perfil real")
    return valor


def lista_env(nombre: str) -> tuple[str, ...]:
    """`A, B` → ("A", "B"). Vacío → (): sin preferencia, enrutado por defecto de OpenRouter."""
    return tuple(p.strip() for p in os.environ.get(nombre, "").split(",") if p.strip())


def json_env(nombre: str, defecto: dict | None = None) -> dict:
    """Objeto JSON de .env. Vacío o sin definir → `defecto`; `{}` lo anula expresamente."""
    texto = os.environ.get(nombre, "").strip()
    if not texto:
        return dict(defecto or {})
    try:
        valor = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise ErrorConfiguracion(f"{nombre} debe ser un objeto JSON: {exc}") from exc
    if not isinstance(valor, dict):
        raise ErrorConfiguracion(f"{nombre} debe ser un objeto JSON")
    return valor


def cuerpo_extra(proveedores: tuple[str, ...] = (), extra: dict | None = None) -> dict:
    """Campos propios de OpenRouter que viajan en el cuerpo de la petición."""
    cuerpo = dict(extra or {})
    if proveedores:
        cuerpo["provider"] = {**cuerpo.get("provider", {}), "order": list(proveedores), "allow_fallbacks": False}
    return cuerpo


def cliente(cliente_http=None):
    """Cliente síncrono compatible con OpenAI apuntando a OpenRouter. Un reintento como máximo."""
    from openai import OpenAI

    return OpenAI(base_url=url_base(), api_key=clave(), max_retries=1, timeout=60, http_client=cliente_http)


@dataclass(frozen=True)
class Uso:
    tokens_entrada: int | None
    tokens_salida: int | None
    coste_usd: float | None  # coste total de la llamada (ver coste_total); None si no se informa
    modelo_servido: str | None
    proveedor_servido: str | None
    byok: bool = False  # la cuenta usa su propia clave del proveedor: este lo factura aparte


def coste_total(uso: dict) -> tuple[float | None, bool]:
    """(coste total en USD, ¿BYOK?) a partir del campo `usage` de OpenRouter.

    - Sin BYOK, `cost` es lo que cobra OpenRouter por la inferencia.
    - Con BYOK (la cuenta de OpenRouter usa claves propias de Google, OpenAI, Anthropic…),
      `cost` es solo la comisión de OpenRouter (a menudo 0) y la inferencia la factura el
      proveedor a esa clave: viene en `cost_details.upstream_inference_cost`. Hay que sumarla;
      si no, el coste real quedaría en 0.
    """
    coste = uso.get("cost")
    if not isinstance(coste, (int, float)) or isinstance(coste, bool):
        return None, bool(uso.get("is_byok"))
    byok = bool(uso.get("is_byok"))
    if byok:
        upstream = (uso.get("cost_details") or {}).get("upstream_inference_cost")
        if not isinstance(upstream, (int, float)) or isinstance(upstream, bool):
            return None, True  # BYOK sin el coste del proveedor: desconocido, no 0
        coste += upstream
    return float(coste), byok


def leer_uso(respuesta) -> Uso:
    """Lee el uso de una respuesta de OpenRouter. Lo que falta queda en None, nunca en 0."""
    uso = getattr(respuesta, "usage", None)
    entrada = getattr(uso, "prompt_tokens", None)
    # completion_tokens ya incluye los tokens de razonamiento, que se facturan como salida.
    salida = getattr(uso, "completion_tokens", None)
    if salida is None and entrada is not None and getattr(uso, "total_tokens", None) is not None:
        salida = uso.total_tokens - entrada
    datos = uso.model_dump() if hasattr(uso, "model_dump") else dict(uso or {})
    coste, byok = coste_total(datos)
    return Uso(
        tokens_entrada=entrada,
        tokens_salida=salida,
        coste_usd=coste,
        modelo_servido=getattr(respuesta, "model", None) or None,
        proveedor_servido=getattr(respuesta, "provider", None) or None,
        byok=byok,
    )
