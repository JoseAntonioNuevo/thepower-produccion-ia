"""Conjuntos de evaluación: test reservado (14 + 6) y validación aparte.

Reglas que este módulo comprueba al cargar, antes de ejecutar nada:

- El test tiene 20 casos: 14 respondibles (con documentos de referencia y datos clave) y
  6 sin respuesta (sin documentos de referencia).
- Validación y test no comparten ningún caso ni ninguna pregunta.
- Las preguntas y respuestas esperadas NO están en el corpus que se indexa.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from evaluacion.intercambio import CASOS, ErrorFormato, leer_jsonl
from rag.config import RAIZ
from rag.corpus import cargar_documentos
from rag.proveedores import normalizar

DATOS = RAIZ / "datos"
TAMANOS = {"test": (14, 6)}  # (respondibles, sin respuesta) exigidos por el enunciado


def cargar(conjunto: str, carpeta: Path = DATOS) -> list[dict]:
    if conjunto not in {"test", "validacion"}:
        raise ErrorFormato("el conjunto debe ser 'test' o 'validacion'")
    casos = leer_jsonl(carpeta / f"{conjunto}.jsonl", CASOS)
    ids = [c["caso_id"] for c in casos]
    if len(ids) != len(set(ids)):
        raise ErrorFormato(f"{conjunto}: hay caso_id repetidos")
    for c in casos:
        if c["respondible"] and not (c["documentos_relevantes"] and c["datos_clave"]):
            raise ErrorFormato(f"{c['caso_id']}: un caso respondible necesita referencias y datos clave")
        if not c["respondible"] and c["documentos_relevantes"]:
            raise ErrorFormato(f"{c['caso_id']}: un caso sin respuesta no tiene documentos relevantes")
    si = sum(1 for c in casos if c["respondible"])
    if conjunto in TAMANOS and (si, len(casos) - si) != TAMANOS[conjunto]:
        raise ErrorFormato(f"{conjunto}: se esperaban {TAMANOS[conjunto]} y hay {(si, len(casos) - si)}")
    return casos


def huella_conjunto(casos: list[dict]) -> str:
    """Identifica el contenido exacto del conjunto: si alguien lo edita, la huella cambia."""
    texto = "\n".join(f"{c['caso_id']}|{c['pregunta']}|{c['documentos_relevantes']}" for c in casos)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]


def comprobar_separacion(carpeta_datos: Path = DATOS, carpeta_corpus: Path = RAIZ / "corpus") -> dict:
    """Comprueba que test y validación son disjuntos y que nada de ellos está indexado."""
    test, validacion = cargar("test", carpeta_datos), cargar("validacion", carpeta_datos)
    documentos = cargar_documentos(carpeta_corpus)
    ids_corpus = {d.documento_id for d in documentos}
    texto_corpus = normalizar(" ".join(d.texto for d in documentos))
    problemas = []
    comunes = {normalizar(c["pregunta"]) for c in test} & {normalizar(c["pregunta"]) for c in validacion}
    if comunes or {c["caso_id"] for c in test} & {c["caso_id"] for c in validacion}:
        problemas.append("test y validación comparten casos")
    for c in test + validacion:
        if normalizar(c["pregunta"]) in texto_corpus:
            problemas.append(f"{c['caso_id']}: la pregunta aparece en el corpus")
        ref = c.get("respuesta_referencia")
        if ref and normalizar(ref) in texto_corpus:
            problemas.append(f"{c['caso_id']}: la respuesta de referencia está copiada en el corpus")
        ajenos = set(c["documentos_relevantes"]) - ids_corpus
        if ajenos:
            problemas.append(f"{c['caso_id']}: referencia a documentos inexistentes {sorted(ajenos)}")
    if problemas:
        raise ErrorFormato("; ".join(problemas))
    return {
        "test": len(test),
        "validacion": len(validacion),
        "documentos": len(documentos),
        "huella_test": huella_conjunto(test),
        "huella_validacion": huella_conjunto(validacion),
    }
