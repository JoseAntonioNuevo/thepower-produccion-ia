"""Construye la presentación S20 a partir de las partes indicadas (por defecto, todas).

Uso (desde esta carpeta):
    uv run --no-project --with python-pptx --with pillow --with lxml python build.py SALIDA.pptx [deck_part1 ...]
"""

import importlib
import sys

sys.path.insert(0, ".")
from deck_lib import WARNINGS, Deck  # noqa: E402

DEFAULT = ["deck_part1", "deck_part2", "deck_part3", "deck_part4"]

# Diapositiva → paso de proyecto-final/demo_clase.py que la acompaña (el «EN VIVO»).
MODO_CLASE = {6: 1, 7: 2, 8: 3, 9: 4, 10: 5, 11: 6, 12: 7, 13: 8, 14: 9, 15: 10, 16: 11, 17: 12, 18: 12,
              19: 13, 22: 14}


def anotar_modo_clase(prs):
    """Añade al principio de las notas qué paso del modo clase se ejecuta en esa diapositiva."""
    for numero, diapositiva in enumerate(prs.slides, 1):
        marco = diapositiva.notes_slide.notes_text_frame
        if numero == 2:
            linea = ("MODO CLASE: en la diapositiva 6 se lanza «uv run python demo_clase.py» y se avanza con Enter; "
                     "cada franja EN VIVO es un paso. «--solo N» repite un paso.")
        elif numero in MODO_CLASE:
            n = MODO_CLASE[numero]
            linea = f"MODO CLASE: paso {n} de 14 (Enter en demo_clase.py; repetirlo: --solo {n})."
        else:
            continue
        marco.text = linea + "\n" + marco.text


def main(salida, modulos):
    partes = []
    for m in modulos:
        mod = importlib.import_module(m)
        partes += [v for k, v in vars(mod).items() if k.startswith("PART")][0]
    d = Deck()
    d.prs.core_properties.title = "S20 · Proyecto final: agente conversacional"
    d.prs.core_properties.author = "José Antonio Nuevo"
    d.prs.core_properties.subject = "thePower · AI Engineer · S20 · 2 de diciembre de 2026"
    for f in partes:
        f(d)
    if len(d.prs.slides) == 24:
        anotar_modo_clase(d.prs)
    d.save(salida)
    print("diapositivas", d.n)
    for w in WARNINGS:
        print("AVISO", w)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:] or DEFAULT)
