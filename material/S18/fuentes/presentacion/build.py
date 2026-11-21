"""Genera la presentación de S18.

Uso (desde esta carpeta):
    uv run --no-project --with python-pptx --with pillow --with lxml python build.py SALIDA.pptx
"""
import importlib
import sys

import deck_lib
from deck_lib import Deck

PARTES = ["deck_part1", "deck_part2", "deck_part3"]


def main(salida):
    d = Deck()
    for nombre in PARTES:
        try:
            mod = importlib.import_module(nombre)
        except ModuleNotFoundError:
            print(f"(falta {nombre}; se omite)")
            continue
        for fn in sorted(n for n in dir(mod) if n.startswith("s") and n[1:3].isdigit()):
            getattr(mod, fn)(d)
    d.save(salida)
    print(f"{d.n} diapositivas -> {salida}")
    for w in deck_lib.WARNINGS:
        print("AVISO", w)


if __name__ == "__main__":
    main(sys.argv[1])
