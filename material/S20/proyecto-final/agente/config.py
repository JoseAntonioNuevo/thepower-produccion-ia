"""PASO 1 · Configuración del agente.

Todo lo que cambia entre el aula, tu portátil y AWS vive aquí y llega por variables de
entorno (prefijo S20_). La lógica del agente nunca lleva un modelo, una clave ni un límite
escritos a mano: así dos ejecuciones se pueden comparar y el despliegue no toca el código.

Dos interruptores independientes explican casi todo:

- S20_PERFIL   = doble  -> sin modelo ni coste: reglas escritas a mano, rotuladas como tales.
                 real   -> modelo de chat y de embeddings de un proveedor (necesita clave).
- S20_ALMACEN  = memoria  -> todo en RAM: sirve para empezar sin Docker, se pierde al cerrar.
                 postgres -> PostgreSQL + pgvector: memoria que sobrevive a un reinicio.
"""

import os
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
DIM = 768  # dimensión de la columna vector(768) del esquema; el modelo debe coincidir
VERSION = "0.1.0"


class ErrorConfiguracion(ValueError):
    """La configuración es incoherente: se detiene el arranque en vez de improvisar."""


@dataclass(frozen=True)
class Config:
    perfil: str  # "doble" | "real"
    almacen: str  # "memoria" | "postgres"
    database_url: str
    modelo_chat: str
    modelo_embeddings: str
    prompt_version: str
    # Límites del agente: son parte del diseño, no un detalle.
    max_herramientas: int  # llamadas a herramientas permitidas en un turno
    k_fragmentos: int  # fragmentos que devuelve la recuperación
    umbral_evidencia: float  # similitud mínima para considerar que hay evidencia
    mcp_timeout_s: float  # espera máxima de una llamada MCP
    # Límites de la investigación (Deep Research acotado).
    fuentes: str  # "locales" (copias de aula) | "red" (descarga la lista blanca)
    max_consultas: int
    max_fuentes: int
    max_bytes_fuente: int
    max_segundos_investigacion: float
    # Identidad de laboratorio: token -> usuario. No es un sistema de autenticación real.
    usuarios: dict
    langfuse: bool

    def publica(self) -> dict:
        """Configuración sin secretos: lo que se puede guardar en evidencias y trazas."""
        datos = asdict(self)
        datos.pop("database_url")  # lleva contraseña
        datos["usuarios"] = sorted(self.usuarios.values())  # nombres, nunca tokens
        return datos


def _numero(nombre: str, defecto, tipo=int):
    try:
        return tipo(os.environ.get(nombre, defecto))
    except ValueError as exc:
        raise ErrorConfiguracion(f"{nombre} debe ser de tipo {tipo.__name__}") from exc


def _usuarios(texto: str) -> dict:
    """'token-ana:ana,token-luis:luis' -> {'token-ana': 'ana', 'token-luis': 'luis'}"""
    pares = [p.split(":", 1) for p in texto.split(",") if ":" in p]
    return {token.strip(): usuario.strip() for token, usuario in pares}


def _database_url() -> str:
    """En local se da la URL entera. En AWS llegan las piezas: la contraseña viene de
    Secrets Manager en su propia variable y nunca se escribe en la plantilla."""
    if os.environ.get("S20_DATABASE_URL"):
        return os.environ["S20_DATABASE_URL"]
    if os.environ.get("S20_DB_HOST"):
        usuario = quote(os.environ.get("S20_DB_USER", "s20"), safe="")
        clave = quote(os.environ.get("S20_DB_PASSWORD", ""), safe="")
        destino = f"{os.environ['S20_DB_HOST']}:{os.environ.get('S20_DB_PORT', '5432')}"
        return f"postgresql://{usuario}:{clave}@{destino}/{os.environ.get('S20_DB_NAME', 's20_agente')}"
    return "postgresql://s20:s20_aula_local@127.0.0.1:54520/s20_agente"


def cargar_config() -> Config:
    perfil = os.environ.get("S20_PERFIL", "doble").strip().lower()
    almacen = os.environ.get("S20_ALMACEN", "memoria").strip().lower()
    fuentes = os.environ.get("S20_FUENTES", "locales").strip().lower()
    if perfil not in {"doble", "real"}:
        raise ErrorConfiguracion("S20_PERFIL debe ser 'doble' o 'real'")
    if almacen not in {"memoria", "postgres"}:
        raise ErrorConfiguracion("S20_ALMACEN debe ser 'memoria' o 'postgres'")
    if fuentes not in {"locales", "red"}:
        raise ErrorConfiguracion("S20_FUENTES debe ser 'locales' o 'red'")
    doble = perfil == "doble"
    return Config(
        perfil=perfil,
        almacen=almacen,
        database_url=_database_url(),
        # En el perfil doble los nombres dicen la verdad: no son modelos de ningún proveedor.
        modelo_chat="doble-reglas"
        if doble
        else os.environ.get("S20_MODELO_CHAT", "google_genai:gemini-3.5-flash-lite"),
        modelo_embeddings="doble-hash-768"
        if doble
        else os.environ.get("S20_MODELO_EMBEDDINGS", "gemini-embedding-2"),
        prompt_version=os.environ.get("S20_PROMPT_VERSION", "v1"),
        max_herramientas=_numero("S20_MAX_HERRAMIENTAS", 4),
        k_fragmentos=_numero("S20_K_FRAGMENTOS", 3),
        umbral_evidencia=_numero("S20_UMBRAL_EVIDENCIA", 0.20 if doble else 0.55, float),
        mcp_timeout_s=_numero("S20_MCP_TIMEOUT_S", 10, float),
        fuentes=fuentes,
        max_consultas=_numero("S20_MAX_CONSULTAS", 3),
        max_fuentes=_numero("S20_MAX_FUENTES", 3),
        max_bytes_fuente=_numero("S20_MAX_BYTES_FUENTE", 1_500_000),
        max_segundos_investigacion=_numero("S20_MAX_SEGUNDOS_INVESTIGACION", 30, float),
        usuarios=_usuarios(os.environ.get("S20_USUARIOS", "token-ana:ana,token-luis:luis")),
        langfuse=os.environ.get("S20_LANGFUSE", "0") == "1",
    )
