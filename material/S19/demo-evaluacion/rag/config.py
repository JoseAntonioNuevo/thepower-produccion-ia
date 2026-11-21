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
DIM = 768  # dimensión de la columna vector(768) del esquema; la misma que en S10

# Variables que una configuración A/B puede cambiar. Cualquier otra clave se rechaza.
VARIABLES_COMPARABLES = ("chunk_size", "chunk_overlap", "k_fragmentos", "k_contexto", "prompt_version")


class ErrorConfiguracion(Exception):
    """Falta un dato de configuración o es incoherente. Nunca se sustituye por un valor inventado."""


def cargar_env(ruta: Path | None = None) -> None:
    """Lee `.env` (CLAVE=valor) sin pisar lo que ya esté en el entorno. No imprime nada."""
    ruta = ruta or RAIZ / ".env"
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class Config:
    perfil: str  # "doble": sin modelos ni coste, rotulado · "real": Gemini, exige --execute
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

    def publica(self) -> dict:
        """Configuración sin la URL de la base (lleva contraseña): es lo que se guarda en resultados."""
        datos = asdict(self)
        datos.pop("database_url")
        return datos


def _entero(nombre: str, defecto: int) -> int:
    try:
        return int(os.environ.get(nombre, defecto))
    except ValueError as exc:
        raise ErrorConfiguracion(f"{nombre} debe ser un entero") from exc


def cargar_config() -> Config:
    cargar_env()
    perfil = os.environ.get("S19_PERFIL", "doble").strip().lower()
    if perfil not in {"doble", "real"}:
        raise ErrorConfiguracion("S19_PERFIL debe ser 'doble' o 'real'")
    doble = perfil == "doble"
    cfg = Config(
        perfil=perfil,
        database_url=os.environ.get("S19_DATABASE_URL", "postgresql://s19:s19_aula_local@127.0.0.1:54519/s19_rag"),
        # En el perfil doble los nombres dicen la verdad: no son modelos de ningún proveedor.
        embedding_modelo="doble-hash-768" if doble else os.environ.get("S19_EMBEDDING_MODEL", "gemini-embedding-2"),
        embedding_dim=_entero("S19_EMBEDDING_DIM", DIM),
        gen_modelo="doble-extractivo" if doble else os.environ.get("S19_GEN_MODEL", "gemini-3.5-flash-lite"),
        chunk_size=_entero("S19_CHUNK_SIZE", 320),
        chunk_overlap=_entero("S19_CHUNK_OVERLAP", 0),
        k_fragmentos=_entero("S19_K_FRAGMENTOS", 12),
        k_documentos=5,
        k_contexto=_entero("S19_K_CONTEXTO", 4),
        umbral_evidencia=float(os.environ.get("S19_UMBRAL_EVIDENCIA", "0")),
        prompt_version=os.environ.get("S19_PROMPT_VERSION", "v1"),
    )
    if cfg.embedding_dim != DIM:
        raise ErrorConfiguracion(f"El esquema usa vector({DIM}); S19_EMBEDDING_DIM debe ser {DIM}")
    return cfg


def aplicar_variante(cfg: Config, config_id: str, ruta: Path | None = None) -> Config:
    """Aplica la variante A o B de `datos/configuraciones.json` sobre la configuración base."""
    ruta = ruta or RAIZ / "datos" / "configuraciones.json"
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    variantes = {**datos["variantes"], **datos.get("alternativa_solo_prompt", {}).get("variantes", {})}
    if config_id not in variantes:
        raise ErrorConfiguracion(f"No existe la variante {config_id!r} en {ruta.name}")
    cambios = variantes[config_id]
    ajenas = set(cambios) - set(VARIABLES_COMPARABLES)
    if ajenas:
        raise ErrorConfiguracion(f"Variables no comparables en {config_id}: {sorted(ajenas)}")
    return replace(cfg, config_id=config_id, **cambios)


def cargar_calibracion(cfg: Config, ruta: Path | None = None) -> Config:
    """Usa el umbral de evidencia elegido con VALIDACIÓN para este perfil, si existe.

    El umbral depende del modelo de embeddings: uno calibrado con el perfil doble no vale
    para el real. Si no hay calibración del perfil, se conserva el valor de entorno.
    """
    ruta = ruta or RAIZ / "datos" / "calibracion.json"
    if "S19_UMBRAL_EVIDENCIA" in os.environ or not ruta.exists():
        return cfg
    datos = json.loads(ruta.read_text(encoding="utf-8")).get(cfg.perfil)
    if not datos or datos.get("embedding_modelo") != cfg.embedding_modelo:
        return cfg
    return replace(cfg, umbral_evidencia=float(datos["umbral_evidencia"]))


def huella(*partes: object) -> str:
    """Huella corta y estable para identificar corpus, índices y ejecuciones."""
    texto = json.dumps(partes, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]
