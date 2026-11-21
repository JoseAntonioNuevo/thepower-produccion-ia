"""Handler de API Gateway HTTP API v2.0: validar, invocar una vez y medir.

IAM se aplica en la ruta de API Gateway. Una ejecución local del handler no
demuestra firma, permisos, TLS, escalado ni un cold start de AWS.
"""

import base64
import binascii
import json
import time

from pydantic import ValidationError

from curso_ia.contratos import Incidencia
from curso_ia.serverless.bedrock import PROMPT_VERSION, FalloBedrock, classify
from curso_ia.serverless.config import Settings

FIRST_IN_ENVIRONMENT = True
MAX_BODY_BYTES = 8192


class EntradaError(Exception):
    def __init__(self, code, status):
        self.code, self.status = code, status


def parse_event(event):
    """Acota el cuerpo incluso en base64, y rechaza antes de gastar en Bedrock."""
    if not isinstance(event, dict) or event.get("version") != "2.0":
        raise EntradaError("evento_invalido", 400)
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if method != "POST" or event.get("rawPath") != "/clasificar":
        raise EntradaError("ruta_no_admitida", 404)
    headers = {str(k).lower(): v for k, v in (event.get("headers") or {}).items()}
    if str(headers.get("content-type", "")).split(";", 1)[0].strip().lower() != "application/json":
        raise EntradaError("content_type_invalido", 415)
    body = event.get("body")
    if not isinstance(body, str):
        raise EntradaError("json_invalido", 400)
    if len(body) > MAX_BODY_BYTES * 2:
        raise EntradaError("entrada_demasiado_grande", 413)
    try:
        raw = (
            base64.b64decode(body, validate=True) if event.get("isBase64Encoded") else body.encode()
        )
        if len(raw) > MAX_BODY_BYTES:
            raise EntradaError("entrada_demasiado_grande", 413)
        value = json.loads(raw)
        return Incidencia.model_validate(value)
    except ValidationError as exc:
        raise EntradaError("entrada_invalida", 422) from exc
    except (ValueError, UnicodeError, binascii.Error, RecursionError) as exc:
        raise EntradaError("json_invalido", 400) from exc


def handle(event, context, *, cfg=None, client=None, first=False):
    """Función inyectable: pruebas y demo usan un transporte explícitamente simulado."""
    started = time.perf_counter()
    request_id = context.aws_request_id
    status, payload, model_ms = 200, {}, None
    cfg = cfg or Settings.from_env()
    try:
        incoming = parse_event(event)
        # 2 s de conexión + 15 s de lectura + margen; no empezar si queda poco tiempo.
        remaining = context.get_remaining_time_in_millis()
        gateway_start = event.get("requestContext", {}).get("timeEpoch")
        if type(gateway_start) is int:
            # La inicialización fría ya ha consumido parte del plazo HTTP antes del handler.
            elapsed = max(0, time.time() * 1000 - gateway_start)
            remaining = min(remaining, 29000 - elapsed)
        if remaining < 20000:
            raise FalloBedrock("presupuesto_tiempo_agotado", 504)
        if cfg.mode == "demo" and client is None:
            raise FalloBedrock("demo_requiere_transporte_explicito", 500)
        model_started = time.perf_counter()
        try:
            result, usage, provider_ms = classify(incoming.texto, cfg, client)
        finally:
            model_ms = round((time.perf_counter() - model_started) * 1000, 3)
        payload = {
            "resultado": result,
            "metadata": {
                "request_id": request_id,
                "api_request_id": event.get("requestContext", {}).get("requestId"),
                "execution": cfg.mode,
                "version": cfg.version,
                "prompt_version": PROMPT_VERSION,
                "modelo_solicitado": cfg.model_id,
                "region_origen": cfg.region,
                "first_in_environment": first,
                "lambda_version": context.function_version,
                "model_duration_ms": model_ms,
                "provider_latency_ms": provider_ms,
                "consumo": {**usage, "coste_usd": None},
            },
        }
    except (EntradaError, FalloBedrock) as exc:
        status, payload = exc.status, {"error": exc.code, "request_id": request_id}
    duration = round((time.perf_counter() - started) * 1000, 3)
    if status == 200:
        payload["metadata"]["duration_ms"] = duration
    # RequestId permite cruzar con REPORT, que contiene duración facturada e Init Duration.
    print(
        json.dumps(
            {
                "request_id": request_id,
                "version": cfg.version,
                "execution": cfg.mode,
                "status": status,
                "duration_ms": duration,
                "model_duration_ms": model_ms,
                "first_in_environment": first,
                "error": payload.get("error"),
            },
            ensure_ascii=False,
        )
    )
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json; charset=utf-8", "x-request-id": request_id},
        "isBase64Encoded": False,
        "body": json.dumps(payload, ensure_ascii=False),
    }


def lambda_handler(event, context):
    """Entrada de AWS. Primera ejecución del entorno es una pista, no la medición de init."""
    global FIRST_IN_ENVIRONMENT
    first, FIRST_IN_ENVIRONMENT = FIRST_IN_ENVIRONMENT, False
    return handle(event, context, first=first)
