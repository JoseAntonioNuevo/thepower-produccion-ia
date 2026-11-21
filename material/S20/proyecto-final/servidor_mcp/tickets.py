"""PASO 3 · Servidor MCP propio: el sistema de tickets, de solo lectura.

El agente NO abre tickets.json. Solo conoce los tickets a través de este servidor, que
habla el Model Context Protocol por stdio (entrada y salida estándar del proceso).

Expone las dos primitivas que vimos en la sesión de MCP:
- una HERRAMIENTA  `consultar_ticket`   -> la invoca el modelo, con argumentos validados
- un RECURSO       `tickets://abiertos` -> dato de contexto que la aplicación puede leer

Probarlo a mano:  uv run python servidor_mcp/tickets.py   (queda esperando mensajes JSON-RPC)
Regla de stdio:   nunca usar print() aquí; la salida estándar es el canal del protocolo.
"""

import json
from pathlib import Path
from typing import Annotated

from mcp.server.mcpserver import MCPServer
from pydantic import Field

TICKETS = Path(__file__).resolve().parent.parent / "datos" / "tickets.json"

servidor = MCPServer(
    "tickets-aethercloud",
    instructions="Consulta de tickets ficticios de AetherCloud. Solo lectura.",
    # Los avisos del servidor salen por stderr, mezclados con la terminal del agente. Solo errores:
    # un argumento inválido ya vuelve al cliente como error de la herramienta.
    log_level="ERROR",
)


def _tickets() -> dict:
    return json.loads(TICKETS.read_text(encoding="utf-8"))


@servidor.tool()
def consultar_ticket(
    ticket_id: Annotated[str, Field(pattern=r"^T-\d{3}$", description="Identificador, p. ej. T-100")],
) -> dict:
    """Devuelve los datos de un ticket ficticio de soporte. No modifica nada."""
    ticket = _tickets().get(ticket_id)
    if ticket is None:
        # Un recurso que no existe no es una excepción: es una respuesta válida y explícita.
        return {"ok": False, "ticket_id": ticket_id, "error": "no_encontrado"}
    return {"ok": True, "ticket_id": ticket_id, "ticket": ticket}


@servidor.resource("tickets://abiertos")
def tickets_abiertos() -> str:
    """Lista de tickets que no están resueltos (identificador y asunto)."""
    abiertos = {k: v["asunto"] for k, v in _tickets().items() if v["estado"] != "resuelto"}
    return json.dumps(abiertos, ensure_ascii=False)


if __name__ == "__main__":
    servidor.run()  # transporte stdio por defecto
