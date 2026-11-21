"""PASO 8 · Observabilidad: poder explicar después qué hizo el agente en un turno.

Dos niveles, del más simple al más completo:

1. Log estructurado (siempre): una línea JSON por turno con request_id, ruta, herramientas,
   duración y perfil. Se lee en la terminal y, en AWS, en CloudWatch Logs.
2. Langfuse (opcional, S20_LANGFUSE=1): la traza completa API -> grafo -> modelo ->
   herramienta, con tokens y coste cuando el proveedor los informa.

Regla de privacidad: en los logs van identificadores y contadores, nunca el texto del
usuario, tokens de acceso ni cuerpos de respuesta del proveedor.
"""

import json
import logging
import os
import uuid
from contextlib import contextmanager

from .config import VERSION, Config

registro = logging.getLogger("agente")


def nuevo_request_id() -> str:
    return str(uuid.uuid4())


def anotar(evento: str, **campos):
    """Una línea JSON por evento: fácil de filtrar por request_id."""
    registro.info(json.dumps({"evento": evento, **campos}, ensure_ascii=False))


def langfuse_activo(cfg: Config) -> bool:
    claves = all(os.environ.get(k) for k in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"))
    return cfg.langfuse and claves


@contextmanager
def turno(cfg: Config, *, thread_id: str, usuario: str, request_id: str):
    """Prepara la `config` de LangGraph para un turno y cierra la traza al terminar."""
    config = {
        # thread_id selecciona la memoria; usuario viaja para las herramientas (no lo elige el modelo).
        "configurable": {"thread_id": thread_id, "usuario": usuario},
        "metadata": {
            "request_id": request_id,
            "perfil": cfg.perfil,
            "modelo": cfg.modelo_chat,
            "prompt_version": cfg.prompt_version,
            "version": VERSION,
        },
        "run_name": "agente-soporte",
        "recursion_limit": 2 * cfg.max_herramientas + 6,  # freno ante bucles
        "callbacks": [],
    }
    if not langfuse_activo(cfg):
        yield config
        return
    from langfuse import get_client, propagate_attributes
    from langfuse.langchain import CallbackHandler

    # El CallbackHandler convierte cada nodo, llamada al modelo y herramienta en un span.
    config["callbacks"] = [CallbackHandler()]
    cliente = get_client()
    try:
        # Un span que envuelve el turno + atributos que heredan todos los spans de dentro:
        # así la traza queda agrupada por conversación (session) y por usuario.
        with (
            cliente.start_as_current_observation(name="turno-agente", as_type="agent"),
            propagate_attributes(
                session_id=thread_id,
                user_id=usuario,
                tags=["thepower", "s20", cfg.perfil],
                metadata={"request_id": request_id, "prompt_version": cfg.prompt_version},
            ),
        ):
            yield config
    finally:
        cliente.flush()  # las trazas se envían en segundo plano: vaciar antes de responder
