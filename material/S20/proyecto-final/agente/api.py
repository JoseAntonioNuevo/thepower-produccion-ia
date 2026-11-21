"""PASO 9 · Exponer el agente con FastAPI.

  GET  /health                     -> ¿está vivo el proceso? NO llama al modelo.
  POST /chat                       -> un turno de conversación
  GET  /conversaciones/{thread_id} -> historial (solo su propietario)
  GET  /investigaciones/{id}       -> estado e informe de una investigación (solo lectura)

Identidad de laboratorio: cabecera `Authorization: Bearer <token>`. Los tokens se definen en
S20_USUARIOS. No es un sistema de autenticación de producción: enseña la idea de que la
identidad viene de la petición autenticada y NO del thread_id ni de lo que diga el modelo.

Arrancar:  uv run uvicorn agente.api:app --port 8020
"""

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from .config import VERSION
from .servicios import ConversacionAjena, Servicios, crear_servicios


class EntradaChat(BaseModel):
    model_config = ConfigDict(extra="forbid")
    thread_id: str = Field(pattern=r"^[A-Za-z0-9_-]{1,64}$", description="Identifica la conversación")
    mensaje: str = Field(min_length=1, max_length=2000)


def crear_app(servicios: Servicios | None = None) -> FastAPI:
    @asynccontextmanager
    async def ciclo(app: FastAPI):
        # Las piezas se construyen una vez al arrancar y se cierran al parar.
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        app.state.servicios = servicios or crear_servicios()
        yield
        if servicios is None:
            app.state.servicios.cerrar()

    app = FastAPI(title="Agente de soporte AetherCloud · S20", version=VERSION, lifespan=ciclo)

    def piezas(request: Request) -> Servicios:
        return request.app.state.servicios

    def usuario_actual(request: Request, authorization: str | None = Header(default=None)) -> str:
        """Traduce el token de laboratorio a un usuario. Sin token válido: 401."""
        token = (authorization or "").removeprefix("Bearer ").strip()
        usuario = piezas(request).cfg.usuarios.get(token)
        if usuario is None:
            raise HTTPException(status_code=401, detail="Falta un token de laboratorio válido")
        return usuario

    @app.get("/health")
    def health(s: Servicios = Depends(piezas)):
        # Salud del proceso: responde aunque el proveedor del modelo esté caído.
        return {
            "estado": "ok",
            "version": VERSION,
            "perfil": s.cfg.perfil,
            "almacen": s.cfg.almacen,
            "fragmentos": s.almacen.contar_fragmentos(),
        }

    # Las rutas son `def` (no `async def`): FastAPI las ejecuta en un hilo aparte y el grafo,
    # que es síncrono, no bloquea al resto de peticiones.
    @app.post("/chat")
    def chat(
        entrada: EntradaChat, usuario: str = Depends(usuario_actual), s: Servicios = Depends(piezas)
    ):
        try:
            return s.conversar(usuario=usuario, thread_id=entrada.thread_id, mensaje=entrada.mensaje)
        except ConversacionAjena:
            # 404 y no 403: no se confirma que exista una conversación de otra persona.
            raise HTTPException(status_code=404, detail="Conversación no encontrada") from None

    @app.get("/conversaciones/{thread_id}")
    def conversacion(
        thread_id: str, usuario: str = Depends(usuario_actual), s: Servicios = Depends(piezas)
    ):
        try:
            return {
                "thread_id": thread_id,
                "mensajes": s.historial(usuario=usuario, thread_id=thread_id),
            }
        except ConversacionAjena:
            raise HTTPException(status_code=404, detail="Conversación no encontrada") from None

    @app.get("/investigaciones/{trabajo_id}")
    def investigacion(
        trabajo_id: str, usuario: str = Depends(usuario_actual), s: Servicios = Depends(piezas)
    ):
        # Consultar el estado solo LEE: repetir esta llamada nunca crea otro trabajo.
        trabajo = s.almacen.leer_trabajo(trabajo_id)
        if trabajo is None or trabajo["usuario"] != usuario:
            raise HTTPException(status_code=404, detail="Investigación no encontrada")
        return {k: trabajo[k] for k in ("trabajo_id", "tema", "estado", "informe")}

    return app


app = crear_app()
