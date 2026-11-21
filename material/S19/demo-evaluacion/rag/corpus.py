"""Documentos en bruto → fragmentos con identificadores estables.

El identificador del documento es el nombre del archivo; el del fragmento, `documento#NN`.
La evaluación de recuperación trabaja con DOCUMENTOS: dos fragmentos del mismo documento
son un solo acierto.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Documento:
    documento_id: str
    titulo: str
    texto: str
    contenido_hash: str


@dataclass(frozen=True)
class Fragmento:
    fragmento_id: str
    documento_id: str
    ordinal: int
    titulo: str
    contenido: str
    contenido_hash: str


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def limpiar(texto: str) -> str:
    """Normaliza saltos y espacios. El hash se calcula sobre el texto limpio."""
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"[ \t]+", " ", texto).strip()


def cargar_documentos(carpeta: Path) -> list[Documento]:
    """Lee los `.md` de la carpeta en orden. Ignora archivos que no son corpus (PROCEDENCIA.md)."""
    documentos = []
    for ruta in sorted(carpeta.glob("*.md")):
        if not ruta.stem[:2].isdigit():
            continue
        texto = limpiar(ruta.read_text(encoding="utf-8"))
        titulo = next((ln[2:].strip() for ln in texto.splitlines() if ln.startswith("# ")), ruta.stem)
        documentos.append(Documento(ruta.stem, titulo, texto, _hash(texto)))
    return documentos


def _unidades(texto: str) -> list[str]:
    """Trocea en párrafos y viñetas. Un encabezado `##` se une al párrafo que introduce."""
    unidades: list[str] = []
    pendiente = ""
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("# "):  # el título va aparte, en `titulo`
            continue
        if linea.startswith("## "):
            pendiente = linea[3:].strip() + ": "
            continue
        unidades.append(pendiente + linea)
        pendiente = ""
    return unidades


def _partir_larga(unidad: str, maximo: int) -> list[str]:
    """Si un párrafo no cabe, se corta por frases; nunca por la mitad de una palabra."""
    if len(unidad) <= maximo:
        return [unidad]
    trozos, actual = [], ""
    for frase in re.split(r"(?<=[.;])\s+", unidad):
        if actual and len(actual) + 1 + len(frase) > maximo:
            trozos.append(actual)
            actual = frase
        else:
            actual = f"{actual} {frase}".strip()
    if actual:
        trozos.append(actual)
    return trozos


def fragmentar(doc: Documento, chunk_size: int, chunk_overlap: int = 0) -> list[Fragmento]:
    """Empaqueta unidades hasta `chunk_size` caracteres. `chunk_overlap` repite la cola anterior."""
    if chunk_size < 80:
        raise ValueError("chunk_size demasiado pequeño para contener una frase")
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("chunk_overlap debe ser menor que chunk_size")
    piezas = [p for u in _unidades(doc.texto) for p in _partir_larga(u, chunk_size)]
    textos, actual = [], ""
    for pieza in piezas:
        if actual and len(actual) + 1 + len(pieza) > chunk_size:
            textos.append(actual)
            cola = actual[-chunk_overlap:] if chunk_overlap else ""
            cola = cola[cola.find(" ") + 1 :] if " " in cola else ""  # no empezar a media palabra
            actual = f"{cola} {pieza}".strip()
        else:
            actual = f"{actual} {pieza}".strip()
    if actual:
        textos.append(actual)
    return [
        Fragmento(f"{doc.documento_id}#{i:02d}", doc.documento_id, i, doc.titulo, t, _hash(t))
        for i, t in enumerate(textos, 1)
    ]


def preparar(carpeta: Path, chunk_size: int, chunk_overlap: int) -> tuple[list[Documento], list[Fragmento]]:
    """Carga y fragmenta el corpus eliminando duplicados exactos (mismo texto limpio)."""
    documentos, vistos_doc = [], set()
    for doc in cargar_documentos(carpeta):
        if doc.contenido_hash in vistos_doc:  # el mismo documento copiado con otro nombre
            continue
        vistos_doc.add(doc.contenido_hash)
        documentos.append(doc)
    fragmentos, vistos = [], set()
    for doc in documentos:
        for frag in fragmentar(doc, chunk_size, chunk_overlap):
            if frag.contenido_hash in vistos:
                continue
            vistos.add(frag.contenido_hash)
            fragmentos.append(frag)
    return documentos, fragmentos
