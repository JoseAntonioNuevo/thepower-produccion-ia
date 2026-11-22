"""Configuración de S19: todo lo que puede cambiar un resultado se lee de variables de entorno.

Ningún modelo, clave ni umbral va escrito en la lógica. Así dos ejecuciones se pueden
comparar sabiendo exactamente qué variable cambió (ver `datos/configuraciones.json`).
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, replace
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIM_DOBLE = 768  # dimensión fija de los embeddings dobles; la del perfil real la decide .env

# Valores por defecto del perfil real. Todos se pueden cambiar en .env sin tocar el código.
# Los nombres son los de OpenRouter (proveedor/modelo): https://openrouter.ai/models
GEN_MODELO_DEFECTO = "google/gemini-4-hydrogen"
EMBEDDING_MODELO_DEFECTO = "openai/text-embedding-3-small"
# Juez de Ragas: de OTRA familia que el generador, para que no puntúe mejor su propio estilo.
# Deben coincidir con los de evaluador/evaluar.py (lo comprueba un test).
EVAL_LLM_MODELO_DEFECTO = "anthropic/claude-opus-5.5"
EVAL_EMBEDDING_MODELO_DEFECTO = "openai/text-embedding-3-small"
PLANTILLA_DOCUMENTO_DEFECTO = "{titulo}\n{texto}"
# Razonamiento bajo: con el máximo por defecto, Gemini 4 Hydrogen llegó a gastar los 2048 tokens
# pensando y devolvió respuestas vacías (prueba real del 22/11/2026). `S19_GEN_EXTRA={}` lo quita.
GEN_EXTRA_DEFECTO = '{"reasoning": {"effort": "low"}}'
PLANTILLA_CONSULTA_DEFECTO = "{texto}"

# Variables que una configuración A/B puede cambiar. Cualquier otra clave se rechaza.
# `gen_modelo` permite comparar dos modelos de generación con el mismo índice y el mismo juez.
VARIABLES_COMPARABLES = ("chunk_size", "chunk_overlap", "k_fragmentos", "k_contexto", "prompt_version", "gen_modelo")


class ErrorConfiguracion(Exception):
    """Falta un dato de configuración o es incoherente. Nunca se sustituye por un valor inventado."""


# Archivo de entorno alternativo: `python s19.py <comando> --env .env.sol-opus` lo fija aquí.
# Sin él se lee `.env`. Una ruta relativa se entiende desde la carpeta de la demo.
VARIABLE_ARCHIVO_ENV = "S19_ENV_FILE"
# Claves que puso cargar_env (no las que ya traía el entorno): permite cambiar de archivo en
# caliente, como hace `/perfil` en la TUI, sin mezclar valores de dos archivos.
_CARGADAS: dict[str, str] = {}


def ruta_env() -> Path:
    """El archivo de entorno elegido con S19_ENV_FILE, o `.env` si no se eligió ninguno."""
    elegido = os.environ.get(VARIABLE_ARCHIVO_ENV, "").strip()
    if not elegido:
        return RAIZ / ".env"
    ruta = Path(elegido).expanduser()
    return ruta if ruta.is_absolute() else RAIZ / ruta


def cargar_env(ruta: Path | None = None, sustituir: bool = False) -> None:
    """Lee el archivo de entorno (CLAVE=valor) sin pisar lo que ya esté en el entorno. No imprime nada.

    Con `sustituir=True` primero retira las claves que cargó la vez anterior (si nadie las ha
    cambiado desde entonces): así se pasa de un archivo a otro sin arrastrar valores.
    """
    elegido = ruta is None and bool(os.environ.get(VARIABLE_ARCHIVO_ENV, "").strip())
    ruta = ruta or ruta_env()
    if sustituir:
        for clave, valor in list(_CARGADAS.items()):
            if os.environ.get(clave) == valor:
                os.environ.pop(clave)
        _CARGADAS.clear()
    if not ruta.exists():
        if elegido:  # un archivo pedido expresamente que no existe es un error, no un silencio
            raise ErrorConfiguracion(f"No existe el archivo de entorno {ruta} ({VARIABLE_ARCHIVO_ENV})")
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        clave, valor = clave.strip(), valor.strip().strip('"').strip("'")
        if clave not in os.environ:
            os.environ[clave] = valor
            _CARGADAS[clave] = valor


@dataclass(frozen=True)
class Config:
    perfil: str  # "doble": sin modelos ni coste, rotulado · "real": OpenRouter, exige --execute
    database_url: str
    embedding_modelo: str
    embedding_dim: int
    gen_modelo: str
    chunk_size: int  # caracteres máximos por fragmento
    chunk_overlap: int  # caracteres que un fragmento repite del anterior
    k_fragmentos: int  # candidatos que se piden a pgvector
    k_documentos: int  # la k de precision@5 y recall@5 (documentos distintos)
    k_contexto: int  # fragmentos que recibe el generador
    umbral_evidencia: float  # similitud mínima del mejor fragmento para intentar responder
    prompt_version: str
    config_id: str = "base"
    # Ajustes que solo existen en el perfil real (None en el doble). Cambian el resultado,
    # así que se guardan con cada ejecución y cuentan al comparar.
    gen_max_tokens: int | None = None
    gen_temperatura: float | None = None  # None = no se envía (hay modelos que no la admiten)
    gen_proveedores: tuple[str, ...] | None = None  # orden fijo de proveedores en OpenRouter
    gen_extra: str | None = None  # campos extra de OpenRouter para la generación (JSON canónico)
    embedding_proveedores: tuple[str, ...] | None = None
    embedding_enviar_dim: bool | None = None  # pedir `dimensions` al modelo de embeddings
    plantilla_documento: str | None = None  # cómo se presenta cada fragmento al indexar
    plantilla_consulta: str | None = None  # cómo se presenta la pregunta al buscar

    def publica(self) -> dict:
        """Configuración sin la URL de la base (lleva contraseña): es lo que se guarda en resultados.

        Los ajustes que no aplican (None) no se escriben: el perfil doble conserva su formato.
        """
        datos = {k: v for k, v in asdict(self).items() if v is not None}
        datos.pop("database_url")
        return {k: list(v) if isinstance(v, tuple) else v for k, v in datos.items()}


def _entero(nombre: str, defecto: int) -> int:
    try:
        return int(os.environ.get(nombre, "").strip() or defecto)
    except ValueError as exc:
        raise ErrorConfiguracion(f"{nombre} debe ser un entero") from exc


def _texto(nombre: str, defecto: str) -> str:
    """Valor de .env; una variable vacía cuenta como no definida."""
    return os.environ.get(nombre, "").strip() or defecto


def _decimal_opcional(nombre: str) -> float | None:
    texto = os.environ.get(nombre, "").strip()
    if not texto:
        return None
    try:
        return float(texto)
    except ValueError as exc:
        raise ErrorConfiguracion(f"{nombre} debe ser un número o quedar vacío") from exc


def _booleano(nombre: str, defecto: bool) -> bool:
    texto = os.environ.get(nombre, "").strip().lower()
    if not texto:
        return defecto
    if texto in {"1", "true", "si", "sí", "on"}:
        return True
    if texto in {"0", "false", "no", "off"}:
        return False
    raise ErrorConfiguracion(f"{nombre} debe ser true o false")


def _plantilla(nombre: str, defecto: str, campos: set[str]) -> str:
    """Plantilla con {texto} (y {titulo} al indexar). Admite \\n para saltos de línea."""
    valor = _texto(nombre, defecto).replace("\\n", "\n")
    if "{texto}" not in valor:
        raise ErrorConfiguracion(f"{nombre} debe contener {{texto}}")
    try:
        valor.format(**{c: "" for c in campos})
    except (KeyError, IndexError, ValueError) as exc:
        raise ErrorConfiguracion(f"{nombre} solo admite {sorted(campos)}: {exc}") from exc
    return valor


def cargar_config() -> Config:
    cargar_env()
    perfil = os.environ.get("S19_PERFIL", "doble").strip().lower()
    if perfil not in {"doble", "real"}:
        raise ErrorConfiguracion("S19_PERFIL debe ser 'doble' o 'real'")
    doble = perfil == "doble"
    from rag.openrouter import json_env, lista_env  # import local: openrouter importa este módulo

    real = {}
    if not doble:
        real = dict(
            # Margen para modelos con razonamiento: sus tokens de pensar cuentan dentro del máximo.
            gen_max_tokens=_entero("S19_GEN_MAX_TOKENS", 2048),
            gen_temperatura=_decimal_opcional("S19_GEN_TEMPERATURE"),
            gen_proveedores=lista_env("S19_GEN_PROVEEDORES"),
            gen_extra=json.dumps(json_env("S19_GEN_EXTRA", json.loads(GEN_EXTRA_DEFECTO)), sort_keys=True),
            embedding_proveedores=lista_env("S19_EMBEDDING_PROVEEDORES"),
            embedding_enviar_dim=_booleano("S19_EMBEDDING_ENVIAR_DIM", True),
            plantilla_documento=_plantilla(
                "S19_EMBEDDING_PLANTILLA_DOCUMENTO", PLANTILLA_DOCUMENTO_DEFECTO, {"titulo", "texto"}
            ),
            plantilla_consulta=_plantilla("S19_EMBEDDING_PLANTILLA_CONSULTA", PLANTILLA_CONSULTA_DEFECTO, {"texto"}),
        )
    cfg = Config(
        perfil=perfil,
        database_url=_texto("S19_DATABASE_URL", "postgresql://s19:s19_aula_local@127.0.0.1:54519/s19_rag"),
        # En el perfil doble los nombres dicen la verdad: no son modelos de ningún proveedor.
        embedding_modelo="doble-hash-768" if doble else _texto("S19_EMBEDDING_MODEL", EMBEDDING_MODELO_DEFECTO),
        embedding_dim=DIM_DOBLE if doble else _entero("S19_EMBEDDING_DIM", 768),
        gen_modelo="doble-extractivo" if doble else _texto("S19_GEN_MODEL", GEN_MODELO_DEFECTO),
        chunk_size=_entero("S19_CHUNK_SIZE", 320),
        chunk_overlap=_entero("S19_CHUNK_OVERLAP", 0),
        k_fragmentos=_entero("S19_K_FRAGMENTOS", 12),
        k_documentos=5,
        k_contexto=_entero("S19_K_CONTEXTO", 4),
        umbral_evidencia=_decimal_opcional("S19_UMBRAL_EVIDENCIA") or 0.0,
        prompt_version=_texto("S19_PROMPT_VERSION", "v1"),
        **real,
    )
    if cfg.embedding_dim <= 0:
        raise ErrorConfiguracion("S19_EMBEDDING_DIM debe ser un entero positivo")
    return cfg


def modelos_evaluador() -> tuple[str, str]:
    """(LLM juez, embeddings del juez) según .env. El evaluador aislado lee las mismas variables."""
    cargar_env()
    return (
        _texto("S19_EVAL_LLM_MODEL", EVAL_LLM_MODELO_DEFECTO),
        _texto("S19_EVAL_EMBEDDING_MODEL", EVAL_EMBEDDING_MODELO_DEFECTO),
    )


def aplicar_variante(cfg: Config, config_id: str, ruta: Path | None = None) -> Config:
    """Aplica la variante A o B de `datos/configuraciones.json` sobre la configuración base."""
    ruta = ruta or RAIZ / "datos" / "configuraciones.json"
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    # Además de A/B, cada bloque `alternativa_*` (solo prompt, solo modelo) aporta sus variantes.
    variantes = dict(datos["variantes"])
    for clave, bloque in datos.items():
        if clave.startswith("alternativa_"):
            variantes.update(bloque.get("variantes", {}))
    if config_id not in variantes:
        raise ErrorConfiguracion(f"No existe la variante {config_id!r} en {ruta.name}")
    cambios = variantes[config_id]
    ajenas = set(cambios) - set(VARIABLES_COMPARABLES)
    if ajenas:
        raise ErrorConfiguracion(f"Variables no comparables en {config_id}: {sorted(ajenas)}")
    if "gen_modelo" in cambios and cfg.perfil == "doble":
        raise ErrorConfiguracion(f"La variante {config_id} cambia gen_modelo: solo tiene sentido en el perfil real")
    return replace(cfg, config_id=config_id, **cambios)


def cargar_calibracion(cfg: Config, ruta: Path | None = None) -> Config:
    """Usa el umbral de evidencia elegido con VALIDACIÓN para este perfil, si existe.

    El umbral depende del modelo de embeddings y de cómo se le presentan los textos: uno
    calibrado con otro modelo no vale. Si no hay calibración válida se conserva el valor de
    entorno (0 por defecto) y `estado_calibracion` lo avisa.
    """
    if os.environ.get("S19_UMBRAL_EVIDENCIA", "").strip():
        return cfg
    datos = leer_calibracion(cfg, ruta)
    if not datos or not calibracion_vale(cfg, datos):
        return cfg
    return replace(cfg, umbral_evidencia=float(datos["umbral_evidencia"]))


def leer_calibracion(cfg: Config, ruta: Path | None = None) -> dict | None:
    ruta = ruta or RAIZ / "datos" / "calibracion.json"
    if not ruta.exists():
        return None
    return json.loads(ruta.read_text(encoding="utf-8")).get(cfg.perfil)


def calibracion_vale(cfg: Config, datos: dict) -> bool:
    """La calibración vale si se hizo con el mismo modelo, dimensión y plantillas de embeddings."""
    return (
        datos.get("embedding_modelo") == cfg.embedding_modelo
        and datos.get("embedding_dim", cfg.embedding_dim) == cfg.embedding_dim
        and datos.get("plantilla_documento") == cfg.plantilla_documento
        and datos.get("plantilla_consulta") == cfg.plantilla_consulta
    )


def estado_calibracion(cfg: Config) -> str:
    """Texto para el operador: de dónde sale el umbral de evidencia que se va a usar."""
    if os.environ.get("S19_UMBRAL_EVIDENCIA", "").strip():
        return f"umbral {cfg.umbral_evidencia} fijado a mano en S19_UMBRAL_EVIDENCIA"
    datos = leer_calibracion(cfg)
    if not datos:
        return f"SIN CALIBRAR para el perfil {cfg.perfil}: umbral {cfg.umbral_evidencia}; ejecuta `calibrar`"
    if not calibracion_vale(cfg, datos):
        return (
            f"SIN CALIBRAR para {cfg.embedding_modelo}: la calibración fijada es de "
            f"{datos.get('embedding_modelo')}; ejecuta `calibrar --fijar`"
        )
    return f"umbral {datos['umbral_evidencia']} calibrado el {datos.get('fijado')} con validación"


def huella(*partes: object) -> str:
    """Huella corta y estable para identificar corpus, índices y ejecuciones."""
    texto = json.dumps(partes, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]
