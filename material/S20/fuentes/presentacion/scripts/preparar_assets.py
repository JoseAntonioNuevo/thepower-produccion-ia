"""Convierte a PNG los logotipos oficiales descargados y copia los iconos reutilizados de S16/S17.

Uso (desde material/S20/fuentes/presentacion):
    uv run --no-project --with resvg-py --with pillow python scripts/preparar_assets.py

Los SVG se renderizan con resvg (sin dependencias del sistema). Los archivos de `descargas/`
son datos descargados: solo se leen como imágenes, nunca se ejecutan.
"""

import io
import shutil
from pathlib import Path

import resvg_py
from PIL import Image

AQUI = Path(__file__).resolve().parent.parent
DESCARGAS, SALIDA = AQUI / "descargas", AQUI / "assets"
MATERIAL = AQUI.parent.parent.parent  # material/
S16 = MATERIAL / "S16" / "fuentes" / "rediseno-visual" / "assets"
S17 = MATERIAL / "S17" / "fuentes" / "rediseno-visual" / "assets"


def svg(origen: str, destino: str, ancho: int = 640):
    datos = resvg_py.svg_to_bytes(svg_path=str(DESCARGAS / origen), width=ancho)
    Image.open(io.BytesIO(bytes(datos))).convert("RGBA").save(SALIDA / destino)


def png(origen: str, destino: str, caja=None, maximo: int = 640):
    imagen = Image.open(DESCARGAS / origen).convert("RGBA")
    if caja:
        imagen = imagen.crop(caja)
    imagen.thumbnail((maximo, maximo), Image.LANCZOS)
    imagen.save(SALIDA / destino)


def marca(origen: str, destino: str, hueco: int = 14):
    """Recorta el símbolo de un logotipo con texto: el primer grupo de columnas con tinta."""
    imagen = Image.open(SALIDA / origen).convert("RGBA")
    alfa = imagen.getchannel("A")
    con_tinta = [alfa.crop((x, 0, x + 1, imagen.height)).getbbox() is not None for x in range(imagen.width)]
    inicio = con_tinta.index(True)
    fin, vacias = inicio, 0
    for x in range(inicio, imagen.width):
        vacias = 0 if con_tinta[x] else vacias + 1
        if vacias >= hueco:
            break
        fin = x if con_tinta[x] else fin
    recorte = imagen.crop((inicio, 0, fin + 1, imagen.height))
    recorte.crop(recorte.getbbox()).save(SALIDA / destino)


def main():
    SALIDA.mkdir(exist_ok=True)
    svg("langgraph-dark.svg", "langgraph-logo.png", 1200)
    svg("langchain-dark.svg", "langchain-logo.png", 1200)
    svg("mcp-dark.svg", "mcp-logo.png", 1600)
    svg("langfuse-logo-white.svg", "langfuse-logo.png")
    png("langfuse-icon256.png", "langfuse-icon.png")
    png("postgresql-elephant.png", "postgresql.png")
    png("fastapi-logo-teal.png", "fastapi-logo.png", maximo=1024)
    png("python-logo.png", "python-logo.png")
    for logo, simbolo in (("fastapi-logo.png", "fastapi-icon.png"), ("langgraph-logo.png", "langgraph-icon.png"),
                          ("langchain-logo.png", "langchain-icon.png"), ("mcp-logo.png", "mcp-icon.png"),
                          ("python-logo.png", "python-icon.png")):
        marca(logo, simbolo)
    # Iconos oficiales ya preparados en S16 y S17 (AWS Architecture Icons, Docker): se copian tal cual.
    for nombre in ("aws-ecs.png aws-fargate.png aws-rds.png aws-secrets.png aws-ecr.png aws-cloudwatch.png "
                   "aws-logo-dark.png aws-logo-light.png aws-vpc.png aws-iam.png docker-mark-white.png "
                   "g-user.png g-client.png g-server.png g-document.png g-data-table.png g-gear.png "
                   "g-logs.png g-metrics.png g-source-code.png g-json-script.png g-internet.png "
                   "g-credentials.png g-alert.png g-generic-application.png r-ecs-task.png "
                   "r-ecs-container.png r-cw-logs.png r-iam-role.png").split():
        shutil.copyfile(S16 / nombre, SALIDA / nombre)
    for nombre in "g-magnifier.png g-padlock.png g-shield.png g-globe.png g-sdk.png g-authuser.png g-servers.png".split():
        shutil.copyfile(S17 / nombre, SALIDA / nombre)
    for ruta in sorted(SALIDA.glob("*.png")):
        print(f"{ruta.name:32s} {Image.open(ruta).size}")


if __name__ == "__main__":
    main()
