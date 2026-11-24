"""Prepara los logotipos de la presentación a partir de las descargas oficiales (ver README.md).

- pytest y Ragas necesitan fondo claro: se colocan sobre una tesela blanca.
- LangGraph y OpenTUI llegan en SVG: se rasterizan con resvg (sin dependencias del sistema).
  El SVG de OpenTUI trae dos colores por `prefers-color-scheme`; se usa su variante oscura
  (blanca), la misma que el proyecto muestra sobre fondo oscuro.
- OpenRouter llega en PNG del kit de marca: se reduce sin alterar proporciones.

Las descargas son datos: solo se leen como imágenes, nunca se ejecutan.
Uso: uv run --no-project --with pillow --with resvg-py python -I preparar_assets.py <carpeta_descargas>
"""
import io
import os
import sys

import resvg_py
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


def svg(nombre, ancho, sustituir=None):
    texto = open(os.path.join(SRC, nombre), encoding="utf-8").read()
    for a, b in (sustituir or {}).items():
        texto = texto.replace(a, b)
    datos = resvg_py.svg_to_bytes(svg_string=texto, width=ancho)
    im = Image.open(io.BytesIO(bytes(datos))).convert("RGBA")
    return im.crop(im.getbbox())


def reducir(im, maximo):
    im = im.copy()
    im.thumbnail((maximo, maximo), Image.LANCZOS)
    return im


# pytest y Ragas (17/11/2026)
pytest_logo = Image.open(os.path.join(SRC, "pytest.png")).convert("RGBA")
tesela(pytest_logo.crop(pytest_logo.getbbox())).save(os.path.join(OUT, "pytest-tile.png"))
ragas = Image.open(os.path.join(SRC, "ragas.png")).convert("RGBA")
tesela(ragas.crop((0, 0, 330, 341)), margen=50).save(os.path.join(OUT, "ragas-tile.png"))

# LangGraph (22/11/2026): logotipo completo para fondo oscuro y su símbolo (el cuadrado de la izquierda).
lg = svg("langgraph-logo-dark.svg", 1416)
lg.save(os.path.join(OUT, "langgraph-logo.png"))
lg.crop((0, 0, lg.height, lg.height)).save(os.path.join(OUT, "langgraph-icon.png"))

# OpenTUI (22/11/2026): marca de píxeles en su variante oscura.
svg("opentui-logo-auto.svg", 1080, {"fill: #000000;": "fill: #ffffff;"}).save(os.path.join(OUT, "opentui-logo.png"))

# OpenRouter (22/11/2026): glifo y logotipo horizontal «cloud» (claros, para fondo oscuro).
glifo = Image.open(os.path.join(SRC, "openrouter-glyph-cloud@2x.png")).convert("RGBA")
reducir(glifo.crop(glifo.getbbox()), 512).save(os.path.join(OUT, "openrouter-glyph.png"))
horizontal = Image.open(os.path.join(SRC, "openrouter-horizontal-cloud@2x.png")).convert("RGBA")
reducir(horizontal.crop(horizontal.getbbox()), 1200).save(os.path.join(OUT, "openrouter-logo.png"))

for n in sorted(os.listdir(OUT)):
    if n.endswith(".png"):
        print(f"{n:28s} {Image.open(os.path.join(OUT, n)).size}")
