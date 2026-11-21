"""Construye la presentación S17 con las partes indicadas (por defecto, todas).

Uso: python build.py SALIDA.pptx [deck_part1 deck_part2 ...]
"""
import importlib
import sys

sys.path.insert(0, ".")
from deck_lib import WARNINGS, Deck  # noqa: E402

DEFAULT = ["deck_part1", "deck_part2", "deck_part3", "deck_part4", "deck_part5", "deck_part6"]


def main(out, mods):
    parts = []
    for m in mods:
        mod = importlib.import_module(m)
        parts += [v for k, v in vars(mod).items() if k.startswith("PART")][0]
    d = Deck()
    d.prs.core_properties.title = "S17 · Serverless AI: AWS Bedrock y Lambda"
    d.prs.core_properties.author = "José Antonio Nuevo"
    d.prs.core_properties.subject = "thePower · AI Engineer · S17 · 17 y 23 de noviembre de 2026"
    for f in parts:
        f(d)
    d.save(out)
    print("slides", d.n)
    for w in WARNINGS:
        print("WARN", w)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:] or DEFAULT)
