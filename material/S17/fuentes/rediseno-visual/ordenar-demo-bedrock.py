"""Coloca los pasos de la demo antes de mediciones y renumera el pie."""

import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile


def main():
    origen, destino = sys.argv[1:3]
    p = "http://schemas.openxmlformats.org/presentationml/2006/main"
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    orden = list(range(1, 15)) + [24, 25] + list(range(15, 24)) + [26]
    with ZipFile(origen) as zin, ZipFile(destino, "w") as zout:
        presentation = ET.fromstring(zin.read("ppt/presentation.xml"))
        ids = presentation.find(f"{{{p}}}sldIdLst")
        originales = list(ids)
        ids[:] = [originales[i - 1] for i in orden]
        cambios = {
            "ppt/presentation.xml": ET.tostring(
                presentation, encoding="utf-8", xml_declaration=True
            )
        }
        for numero, anterior in enumerate(orden, 1):
            nombre = f"ppt/slides/slide{anterior}.xml"
            raiz = ET.fromstring(zin.read(nombre))
            for shape in raiz.findall(f".//{{{p}}}sp"):
                off = shape.find(f".//{{{a}}}xfrm/{{{a}}}off")
                textos = shape.findall(f".//{{{a}}}t")
                if (
                    off is not None
                    and int(off.get("x", 0)) > 10000000
                    and int(off.get("y", 0)) > 6000000
                ):
                    if len(textos) == 1 and (textos[0].text or "").isdigit():
                        textos[0].text = str(numero)
            cambios[nombre] = ET.tostring(raiz, encoding="utf-8", xml_declaration=True)
        for item in zin.infolist():
            zout.writestr(item, cambios.get(item.filename, zin.read(item.filename)))


if __name__ == "__main__":
    main()
