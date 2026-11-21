"""PASO 4 · Herramientas: lo único que el agente puede HACER.

El modelo no ejecuta nada: propone «llama a X con estos argumentos» y este código decide
si se ejecuta. Cada herramienta tiene un contrato: nombre, descripción (la lee el modelo),
argumentos validados con Pydantic y una salida JSON que siempre dice `ok`.

  consultar_ticket      -> sistema de tickets, a través del servidor MCP
  buscar_documentacion  -> documentación propia (RAG)
  investigar            -> registra o consulta un trabajo de investigación
"""

import json

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict, Field

from . import mcp_cliente
from .config import Config
from .rag import recuperar


class ArgsTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ticket_id: str = Field(pattern=r"^T-\d{3}$", description="Identificador del ticket, p. ej. T-100")


class ArgsPregunta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pregunta: str = Field(min_length=3, max_length=500, description="Qué se quiere saber")


class ArgsTema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tema: str = Field(min_length=3, max_length=300, description="Tecnología o tema público")


def _texto(datos: dict) -> str:
    return json.dumps(datos, ensure_ascii=False)


def crear_herramientas(cfg: Config, almacen, embeddings) -> list:
    @tool(args_schema=ArgsTicket)
    def consultar_ticket(ticket_id: str) -> str:
        """Consulta un ticket de soporte por su identificador (T- y tres dígitos). Solo lectura."""
        return _texto(mcp_cliente.llamar_herramienta("consultar_ticket", {"ticket_id": ticket_id}, cfg))

    @tool(args_schema=ArgsPregunta)
    def buscar_documentacion(pregunta: str) -> str:
        """Busca políticas y documentación interna de AetherCloud. Devuelve fragmentos con su cita."""
        return _texto(recuperar(cfg, almacen, embeddings, pregunta))

    @tool(args_schema=ArgsTema)
    def investigar(tema: str, config: RunnableConfig) -> str:
        """Registra una investigación sobre información pública de una tecnología, o devuelve su
        estado si ya existe. El informe llega cuando el ejecutor termina el trabajo."""
        # La identidad no la decide el modelo: viene de la configuración del turno.
        contexto = config.get("configurable", {})
        trabajo = almacen.crear_trabajo(contexto["thread_id"], contexto["usuario"], tema)
        salida = {
            "ok": True,
            "trabajo_id": trabajo["trabajo_id"],
            "estado": trabajo["estado"],
            "nuevo": trabajo["nuevo"],
        }
        if trabajo["informe"]:
            salida["resumen"] = trabajo["informe"].get("resumen")
            salida["fuentes"] = [
                e["fuente_id"] for e in trabajo["informe"].get("informacion_publica", [])
            ]
        return _texto(salida)

    return [consultar_ticket, buscar_documentacion, investigar]


def fuentes_de(nombre: str, resultado: dict) -> list[str]:
    """Qué fuentes aporta el resultado de una herramienta (para devolverlas al cliente)."""
    if nombre == "consultar_ticket" and resultado.get("ok"):
        return [f"ticket:{resultado['ticket_id']}"]
    if nombre == "buscar_documentacion":
        return [f"doc:{f['cita']}" for f in resultado.get("fragmentos", [])]
    if nombre == "investigar":
        return [f"web:{f}" for f in resultado.get("fuentes", [])]
    return []
