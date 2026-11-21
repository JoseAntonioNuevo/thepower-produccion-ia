"""Prepara los iconos que necesitan fondo claro (pytest y Ragas) como teselas blancas.

Entrada: descargas oficiales (ver README.md). Salida: assets/pytest-tile.png, assets/ragas-tile.png.
Uso: uv run --no-project --with pillow python -I preparar_assets.py <carpeta_descargas>
"""
import os
import sys

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SRC = sys.argv[1]


def tesela(im, lado=320, margen=34):
    fondo = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    ImageDraw.Draw(fondo).rounded_rectangle([0, 0, lado - 1, lado - 1], radius=44, fill="white")
    im = im.convert("RGBA")
    im.thumbnail((lado - 2 * margen, lado - 2 * margen), Image.LANCZOS)
    fondo.paste(im, ((lado - im.width) // 2, (lado - im.height) // 2), im)
    return fondo


pytest_logo = Image.open(os.path.join(SRC, "pytest.png")).convert("RGBA")
tesela(pytest_logo.crop(pytest_logo.getbbox())).save(os.path.join(OUT, "pytest-tile.png"))
ragas = Image.open(os.path.join(SRC, "ragas.png")).convert("RGBA")
tesela(ragas.crop((0, 0, 330, 341)), margen=50).save(os.path.join(OUT, "ragas-tile.png"))
print("teselas creadas en", OUT)
