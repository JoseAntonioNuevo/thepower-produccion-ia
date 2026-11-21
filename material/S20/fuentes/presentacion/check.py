"""Comprobación geométrica y de contenido de la presentación S20.

- Notas: al menos 200 caracteres, con TIEMPO, FUENTES e IMÁGENES.
- Ninguna forma fuera del lienzo.
- QR vigente (material/S20/assets, idéntico al de S16) y logotipo de thePower, byte a byte.
- El QR antiguo de material/S17/assets no aparece.
Uso: python check.py PRESENTACION.pptx
"""

import hashlib
import os
import sys

from pptx import Presentation

AQUI = os.path.dirname(os.path.abspath(__file__))
MATERIAL = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))


def sha(ruta):
    return hashlib.sha256(open(ruta, "rb").read()).hexdigest()


p = Presentation(sys.argv[1])
W, H = p.slide_width, p.slide_height
qr = sha(os.path.join(MATERIAL, "S20", "assets", "qr-ai-engineer.jpg"))
assert qr == sha(os.path.join(MATERIAL, "S16", "assets", "qr-ai-engineer.jpg")), "el QR de S20 no es el vigente de S16"
qr_viejo = sha(os.path.join(MATERIAL, "S17", "assets", "qr-ai-engineer.jpg"))
logo = sha(os.path.join(MATERIAL, "S20", "assets", "thepower-logo.png"))
print("diapositivas", len(p.slides), "tamaño", W, H)
n_qr = n_viejo = n_logo = problemas = palabras = 0
for i, s in enumerate(p.slides, 1):
    n = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
    if len(n) < 200:
        print("notas cortas", i, len(n)); problemas += 1
    for clave in ("TIEMPO", "FUENTES", "IMÁGENES"):
        if clave not in n:
            print("falta", clave, "en notas", i); problemas += 1
    for sh in s.shapes:
        if sh.left < 0 or sh.top < 0 or sh.left + sh.width > W + 12700 or sh.top + sh.height > H + 12700:
            print("fuera del lienzo", i, sh.name, sh.left / 12700, sh.top / 12700,
                  (sh.left + sh.width) / 12700, (sh.top + sh.height) / 12700); problemas += 1
        if sh.shape_type == 13:
            h = hashlib.sha256(sh.image.blob).hexdigest()
            n_qr += h == qr
            n_viejo += h == qr_viejo
            n_logo += h == logo
        if sh.has_text_frame:
            palabras += len(sh.text_frame.text.split())
print(f"QR vigente: {n_qr} | QR antiguo de S17: {n_viejo} | logotipo thePower: {n_logo} | "
      f"palabras visibles: {palabras} | problemas: {problemas}")
sys.exit(1 if problemas or n_qr != 1 or n_viejo or n_logo < 2 else 0)
