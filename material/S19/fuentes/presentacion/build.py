"""Genera la presentación de S19. Uso (desde esta carpeta):

    uv run --no-project --with python-pptx --with pillow --with lxml python -I build.py SALIDA.pptx
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I no añade la carpeta del script

import deck_lib  # noqa: E402

deck = deck_lib.Deck()
for nombre in ("deck_part1", "deck_part2", "deck_part3"):
    try:
        modulo = importlib.import_module(nombre)
    except ModuleNotFoundError:
        continue
    for fn in modulo.SLIDES:
        fn(deck)
salida = sys.argv[1]
deck.save(salida)
print(f"{deck.n} diapositivas → {salida}")
for w in deck_lib.WARNINGS:
    print("AVISO", w)
