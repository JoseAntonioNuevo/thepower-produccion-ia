"""FastAPI para S16: salud, clasificación y evidencia mínima sin registrar el texto.

`create_app` admite configuración y proveedor inyectados. La aplicación real se crea
con `uvicorn curso_ia.api:create_app --factory`, sin efectos de red al importar.
"""

import json
import logging
import time
import uuid
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from curso_ia.config import Settings
from curso_ia.contratos import Incidencia
from curso_ia.proveedores import (
    PROMPT_VERSION,
    AnthropicProvider,
    DemoProvider,
    ErrorProveedor,
    Proveedor,
)

LOG = logging.getLogger("curso_ia.peticiones")


class LimiteCuerpo:
    """Acota bytes antes del parser JSON, incluso si falta Content-Length."""

    def __init__(self, app, max_bytes=16384):
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] != "POST":
            await self.app(scope, receive, send)
            return
        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            body.extend(message.get("body", b""))
            if len(body) > self.max_bytes:
                response = JSONResponse({"error": "entrada_demasiado_grande"}, status_code=413)
                await response(scope, receive, send)
                return
            if not message.get("more_body", False):
                break
        delivered = False

        async def buffered_receive():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}
            return await receive()

        await self.app(scope, buffered_receive, send)


def create_app(settings: Settings | None = None, proveedor: Proveedor | None = None) -> FastAPI:
    """Construye una API nueva; el lifespan administra el pool HTTP del proveedor."""
    cfg = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(app):
        async with httpx.AsyncClient(
            timeout=cfg.timeout_seconds, follow_redirects=False, trust_env=False
        ) as client:
            app.state.proveedor = proveedor or (
                DemoProvider() if cfg.mode == "demo" else AnthropicProvider(cfg, client)
            )
            yield

    app = FastAPI(
        title="thePower · API de soporte S16",
        description="Laboratorio con datos ficticios. El campo execution identifica demo o real.",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.add_middleware(LimiteCuerpo)

    @app.middleware("http")
    async def evidencia(request: Request, call_next):
        # Generamos la identidad en el servidor: nunca escribimos una cabecera arbitraria en logs.
        request.state.request_id = str(uuid.uuid4())
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["x-request-id"] = request.state.request_id
        LOG.warning(
            json.dumps(
                {
                    "request_id": request.state.request_id,
                    "version": cfg.app_version,
                    "execution": cfg.mode,
                    "status": response.status_code,
                    "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                }
            )
        )
        return response

    @app.exception_handler(RequestValidationError)
    async def entrada_invalida(request, exc):
        # FastAPI puede incluir el valor recibido en sus errores; omitimos ese contenido.
        return JSONResponse(
            {"error": "entrada_invalida", "request_id": request.state.request_id}, status_code=422
        )

    @app.exception_handler(ErrorProveedor)
    async def fallo_proveedor(request, exc):
        return JSONResponse(
            {"error": exc.codigo, "request_id": request.state.request_id}, status_code=exc.status
        )

    @app.get("/health")
    async def health():
        """Salud del proceso y configuración; no consulta ni factura al proveedor."""
        return {
            "status": "ok",
            "execution": cfg.mode,
            "version": cfg.app_version,
            "provider_check": "no_ejecutado",
        }

    @app.post("/clasificar")
    async def clasificar(incidencia: Incidencia, request: Request):
        """Devuelve la clasificación validada y los metadatos medidos por el servidor."""
        started = time.perf_counter()
        result = await app.state.proveedor.clasificar(incidencia.texto)
        return {
            "resultado": result.clasificacion.model_dump(),
            "metadata": {
                "request_id": request.state.request_id,
                "execution": cfg.mode,
                "version": cfg.app_version,
                "prompt_version": PROMPT_VERSION,
                "modelo_solicitado": "reglas-demo-v1" if cfg.mode == "demo" else cfg.model_id,
                "modelo_devuelto": result.modelo_devuelto,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                "consumo": result.consumo.model_dump(),
            },
        }

    return app
