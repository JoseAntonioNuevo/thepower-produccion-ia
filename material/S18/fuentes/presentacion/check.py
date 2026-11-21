"""Comprobación geométrica y de contenido del PPTX de S18: python check.py archivo.pptx"""
import hashlib
import os
import sys

from pptx import Presentation

HERE = os.path.dirname(os.path.abspath(__file__))
S18 = os.path.normpath(os.path.join(HERE, "..", ".."))
p = Presentation(sys.argv[1])
W, H = p.slide_width, p.slide_height
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()  # noqa: E731
qr = sha(os.path.join(S18, "..", "S16", "assets", "qr-ai-engineer.jpg"))
old_qr = sha(os.path.join(S18, "..", "S17", "assets", "qr-ai-engineer.jpg"))
logo = sha(os.path.join(S18, "assets", "thepower-logo.png"))
print("diapositivas", len(p.slides), "tamaño", W / 12700, H / 12700)
qr_n = old_n = logo_n = issues = words = tables = 0
fonts = set()
for i, s in enumerate(p.slides, 1):
    n = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
    if len(n) < 300:
        print("notas cortas", i, len(n)); issues += 1
    if not n[:5].replace(":", "").isdigit():
        print("las notas no empiezan por la franja horaria", i); issues += 1
    if "Fuentes" not in n:
        print("notas sin fuentes", i); issues += 1
    if "Pregunta" not in n and i not in (2,):
        print("notas sin pregunta", i); issues += 1
    for sh in s.shapes:
        if sh.left < 0 or sh.top < 0 or sh.left + sh.width > W + 12700 or sh.top + sh.height > H + 12700:
            print("fuera del lienzo", i, sh.name, round(sh.left / 12700), round(sh.top / 12700)); issues += 1
        if sh.shape_type == 13:
            h = hashlib.sha256(sh.image.blob).hexdigest()
            qr_n += h == qr; old_n += h == old_qr; logo_n += h == logo
        if sh.has_table:
            tables += 1
        if sh.has_text_frame:
            words += len(sh.text_frame.text.split())
            for para in sh.text_frame.paragraphs:
                for r in para.runs:
                    fonts.add(r.font.name)
print(f"QR vigente: {qr_n} | QR antiguo: {old_n} | logotipo: {logo_n} | tablas nativas: {tables} | "
      f"palabras visibles: {words} | fuentes: {sorted(f for f in fonts if f)} | incidencias: {issues}")
sys.exit(1 if issues or qr_n != 1 or old_n or logo_n < 2 else 0)
