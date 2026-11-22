"""Reconstrucción del índice desde documentos en bruto y un índice vacío."""

from __future__ import annotations

from pathlib import Path

from rag.almacen import ErrorIndice, Indice
from rag.config import RAIZ, Config, huella
from rag.corpus import Documento, preparar

CORPUS = RAIZ / "corpus"
MIN_DOCUMENTOS = 8  # el enunciado pide al menos ocho documentos ficticios


def identidad_indice(cfg: Config, documentos: list[Documento]) -> str:
    """El índice se identifica por lo que determina sus vectores: corpus, fragmentación y modelo.

    En el perfil real también cuentan la plantilla con la que se presenta cada fragmento y si
    se pidió reducir la dimensión: cambiar cualquiera de las dos en .env crea OTRO índice.
    """
    partes = [
        sorted(d.contenido_hash for d in documentos),
        cfg.chunk_size,
        cfg.chunk_overlap,
        cfg.embedding_modelo,
        cfg.embedding_dim,
    ]
    if cfg.perfil == "real":
        partes += [cfg.plantilla_documento, cfg.embedding_enviar_dim]
    return "idx-" + huella(*partes)


def reconstruir_indice(cfg: Config, almacen, embeddings, carpeta: Path = CORPUS) -> Indice:
    """Lee, limpia, fragmenta, calcula embeddings y sustituye el índice de esta configuración.

    Ejecutarla dos veces deja el mismo índice con las mismas filas: no acumula duplicados.
    """
    if embeddings.nombre != cfg.embedding_modelo:
        raise ErrorIndice("el proveedor de embeddings no es el de la configuración")
    documentos, fragmentos = preparar(carpeta, cfg.chunk_size, cfg.chunk_overlap)
    if len(documentos) < MIN_DOCUMENTOS:
        raise ErrorIndice(f"hacen falta al menos {MIN_DOCUMENTOS} documentos; hay {len(documentos)}")
    # Los embeddings se calculan ANTES de tocar la base: si el proveedor falla, el índice
    # anterior sigue intacto.
    filas = [(f, embeddings.incrustar_documento(f.titulo, f.contenido)) for f in fragmentos]
    indice = Indice(
        identidad_indice(cfg, documentos),
        cfg.perfil,
        cfg.embedding_modelo,
        cfg.embedding_dim,
        cfg.chunk_size,
        cfg.chunk_overlap,
        len(documentos),
        len(fragmentos),
    )
    almacen.preparar_esquema()
    almacen.reconstruir(indice, filas)
    if almacen.contar(indice.indice_id) != len(fragmentos):  # se comprueba leyendo, no suponiendo
        raise ErrorIndice("la base no contiene las filas que se acaban de insertar")
    return indice


def indice_esperado(cfg: Config, carpeta: Path = CORPUS) -> str:
    """Id del índice que corresponde a esta configuración, sin calcular embeddings."""
    documentos, _ = preparar(carpeta, cfg.chunk_size, cfg.chunk_overlap)
    return identidad_indice(cfg, documentos)
