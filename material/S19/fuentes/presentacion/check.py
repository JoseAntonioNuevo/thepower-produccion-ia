"""Comprobación del PPTX de S19: notas, límites del lienzo, tipografías, QR y logotipo byte a byte.

Uso: uv run --no-project --with python-pptx --with pillow --with lxml python -I check.py ARCHIVO.pptx
"""
import hashlib
import os
import re
import sys

from pptx import Presentation
from pptx.util import Emu

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))  # material/
QR = os.path.join(REPO, "S16", "assets", "qr-ai-engineer.jpg")
QR_VIEJO = os.path.join(REPO, "S17", "assets", "qr-ai-engineer.jpg")
LOGO = os.path.join(REPO, "S17", "assets", "thepower-logo.png")
FUENTES = {"Georgia", "Arial", "Courier New"}


def sha(ruta):
    return hashlib.sha256(open(ruta, "rb").read()).hexdigest()


prs = Presentation(sys.argv[1])
W, H = prs.slide_width, prs.slide_height
fallos, tablas, imagenes, fuentes = [], 0, 0, set()
blobs = set()
for n, sl in enumerate(prs.slides, 1):
    nota = sl.notes_slide.notes_text_frame.text if sl.has_notes_slide else ""
    if len(nota) < 200:
        fallos.append(f"{n}: nota corta o ausente")
    for marca in (r"1[89]:\d\d", "QUÉ ABRIR", "PREGUNTA", "Fuentes"):
        if not re.search(marca, nota):
            fallos.append(f"{n}: la nota no contiene «{marca}»")
    for s in sl.shapes:
        if s.left < 0 or s.top < 0 or s.left + s.width > W + Emu(12700) or s.top + s.height > H + Emu(12700):
            fallos.append(f"{n}: forma fuera del lienzo ({s.name})")
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.name:
                        fuentes.add(r.font.name)
        if getattr(s, "has_table", False) and s.has_table:
            tablas += 1
            for fila in s.table.rows:
                for c in fila.cells:
                    for p in c.text_frame.paragraphs:
                        for r in p.runs:
                            if r.font.name:
                                fuentes.add(r.font.name)
        if s.shape_type == 13:
            imagenes += 1
            blobs.add(hashlib.sha256(s.image.blob).hexdigest())
if len(prs.slides) != 32:
    fallos.append(f"se esperaban 32 diapositivas y hay {len(prs.slides)}")
if fuentes - FUENTES:
    fallos.append(f"tipografías ajenas al sistema visual: {sorted(fuentes - FUENTES)}")
if sha(QR) not in blobs:
    fallos.append("el QR vigente de S16 no está incrustado byte a byte")
if sha(QR_VIEJO) != sha(QR) and sha(QR_VIEJO) in blobs:
    fallos.append("está incrustado el QR antiguo de S17")
if sha(LOGO) not in blobs:
    fallos.append("el logotipo de thePower no está incrustado byte a byte")
if (W, H) != (Emu(960 * 12700), Emu(540 * 12700)):
    fallos.append("el lienzo no es 960 × 540 pt")
print(f"{len(prs.slides)} diapositivas · {tablas} tablas nativas · {imagenes} imágenes · tipografías {sorted(fuentes)}")
print("QR sha256", sha(QR)[:16], "· logotipo sha256", sha(LOGO)[:16])
for f in fallos:
    print("FALLO", f)
print("CORRECTO" if not fallos else f"{len(fallos)} fallos")
sys.exit(1 if fallos else 0)
