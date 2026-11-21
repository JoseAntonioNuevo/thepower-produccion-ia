"""PASO 3 · Cliente MCP: cómo consume el agente un servidor MCP.

Cada llamada hace el recorrido completo del protocolo, a la vista:
  1. arrancar el servidor como subproceso (transporte stdio) e inicializar la sesión
  2. DESCUBRIR las herramientas que publica (`tools/list`)
  3. comprobar que la herramienta pedida está en NUESTRA lista blanca
  4. LLAMAR a la herramienta (`tools/call`) con un tiempo máximo

Abrir un proceso por llamada es lento pero fácil de seguir en clase. En producción se
mantiene una sesión abierta o se usa un servidor remoto (Streamable HTTP).
"""

import asyncio
import json
import sys

from mcp import Client, StdioServerParameters

from .config import RAIZ, Config

SERVIDOR = RAIZ / "servidor_mcp" / "tickets.py"
# Lista blanca: aunque el servidor publique más herramientas, el agente solo usa estas.
PERMITIDAS = {"consultar_ticket"}


class ErrorMCP(RuntimeError):
    """Fallo controlado al hablar con el servidor MCP (no permitido, timeout, protocolo)."""


def _parametros() -> StdioServerParameters:
    return StdioServerParameters(command=sys.executable, args=[str(SERVIDOR)])


async def _descubrir() -> list[dict]:
    async with Client(_parametros()) as cliente:
        catalogo = await cliente.list_tools()
        return [
            {"nombre": t.name, "descripcion": t.description, "argumentos": t.input_schema}
            for t in catalogo.tools
        ]


async def _llamar(nombre: str, argumentos: dict, timeout_s: float) -> dict:
    if nombre not in PERMITIDAS:
        raise ErrorMCP(f"herramienta_no_permitida:{nombre}")
    async with Client(_parametros(), read_timeout_seconds=timeout_s) as cliente:
        publicadas = {t.name for t in (await cliente.list_tools()).tools}
        if nombre not in publicadas:
            raise ErrorMCP(f"herramienta_no_publicada:{nombre}")
        resultado = await cliente.call_tool(nombre, argumentos)
    if resultado.is_error:
        # Por ejemplo, argumentos que no cumplen el esquema (T-1 en vez de T-100).
        detalle = " ".join(getattr(c, "text", "") for c in resultado.content)[:200]
        raise ErrorMCP(f"error_de_herramienta:{detalle}")
    if resultado.structured_content is not None:
        return resultado.structured_content
    return json.loads(resultado.content[0].text)


def descubrir_herramientas(cfg: Config) -> list[dict]:
    return asyncio.run(asyncio.wait_for(_descubrir(), cfg.mcp_timeout_s))


def llamar_herramienta(nombre: str, argumentos: dict, cfg: Config) -> dict:
    """Versión síncrona para el grafo. Convierte cualquier fallo en ErrorMCP."""
    try:
        return asyncio.run(
            asyncio.wait_for(_llamar(nombre, argumentos, cfg.mcp_timeout_s), cfg.mcp_timeout_s + 2)
        )
    except ErrorMCP:
        raise
    except TimeoutError as exc:
        raise ErrorMCP("timeout") from exc
    except Exception as exc:  # protocolo, proceso que no arranca, etc.
        raise ErrorMCP(f"fallo_mcp:{type(exc).__name__}") from exc
