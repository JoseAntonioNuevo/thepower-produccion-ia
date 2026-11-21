"""El servidor MCP propio y el cliente del agente (llamadas MCP reales por stdio, sin red)."""

import asyncio
import json

import pytest
from mcp import Client

from agente import mcp_cliente


def test_descubre_la_herramienta_que_publica_el_servidor(cfg):
    catalogo = mcp_cliente.descubrir_herramientas(cfg)
    assert [h["nombre"] for h in catalogo] == ["consultar_ticket"]
    # El contrato viaja con la herramienta: el patrón del identificador está en el esquema.
    assert catalogo[0]["argumentos"]["properties"]["ticket_id"]["pattern"] == r"^T-\d{3}$"


def test_ticket_existente(cfg):
    r = mcp_cliente.llamar_herramienta("consultar_ticket", {"ticket_id": "T-100"}, cfg)
    assert r["ok"] is True and r["ticket"]["plan"] == "Estándar"


def test_ticket_inexistente_es_respuesta_explicita_no_excepcion(cfg):
    r = mcp_cliente.llamar_herramienta("consultar_ticket", {"ticket_id": "T-999"}, cfg)
    assert r == {"ok": False, "ticket_id": "T-999", "error": "no_encontrado"}


def test_argumento_invalido_lo_rechaza_el_servidor(cfg):
    with pytest.raises(mcp_cliente.ErrorMCP, match="error_de_herramienta"):
        mcp_cliente.llamar_herramienta("consultar_ticket", {"ticket_id": "T-1"}, cfg)


def test_herramienta_fuera_de_la_lista_blanca_no_se_llama(cfg):
    with pytest.raises(mcp_cliente.ErrorMCP, match="herramienta_no_permitida"):
        mcp_cliente.llamar_herramienta("borrar_ticket", {"ticket_id": "T-100"}, cfg)


def test_recurso_de_tickets_abiertos():
    async def leer():
        async with Client(mcp_cliente._parametros()) as cliente:
            recurso = await cliente.read_resource("tickets://abiertos")
            return json.loads(recurso.contents[0].text)

    abiertos = asyncio.run(leer())
    assert set(abiertos) == {"T-100", "T-200"}  # T-300 está resuelto
