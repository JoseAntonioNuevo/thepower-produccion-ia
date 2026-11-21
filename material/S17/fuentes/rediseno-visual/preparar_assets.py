"""Convierte a PNG los iconos oficiales y recorta las capturas de documentación usadas en S17.

Uso:
    python preparar_assets.py AWS_PKG AZURE_PKG GOOGLE_LEGACY DOCIMGS

AWS_PKG       carpeta descomprimida del paquete AWS Architecture Icons (07/31/2026)
AZURE_PKG     carpeta descomprimida de Azure_Public_Service_Icons_V25.zip
GOOGLE_LEGACY carpeta descomprimida de google-cloud-legacy-icons.zip
DOCIMGS       carpeta con las imágenes descargadas de docs.aws.amazon.com/images/...

Los iconos reutilizados de S16 se copian tal cual desde material/S16/fuentes/rediseno-visual/assets.
Requiere cairosvg (renderiza SVG con degradados; en macOS, libcairo de Homebrew y
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib) y Pillow. Los iconos heredados de Google Cloud
se toman de los PNG oficiales del mismo paquete.
"""

import os
import sys

import cairosvg
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")


def svg_png(src, dst, px=320):
    if src.endswith(".png"):
        im = Image.open(src).convert("RGBA")
        im.thumbnail((px, px), Image.LANCZOS)
        im.save(os.path.join(OUT, dst))
        return
    cairosvg.svg2png(url=src, write_to=os.path.join(OUT, dst), output_width=px, output_height=px)


def main(aws, azure, google, docimgs):
    arch = os.path.join(aws, "Architecture-Service-Icons_07312026")
    res = os.path.join(aws, "Resource-Icons_07312026")
    icons = {
        "aws-apigw.png": f"{arch}/Arch_Networking-Content-Delivery/64/Arch_Amazon-API-Gateway_64.svg",
        "aws-agentcore.png": f"{arch}/Arch_Artificial-Intelligence/64/Arch_Amazon-Bedrock-AgentCore_64.svg",
        "aws-stepfunctions.png": f"{arch}/Arch_Application-Integration/64/Arch_AWS-Step-Functions_64.svg",
        "aws-sqs.png": f"{arch}/Arch_Application-Integration/64/Arch_Amazon-Simple-Queue-Service_64.svg",
        "r-lambda-fn.png": f"{res}/Res_Compute/Res_AWS-Lambda_Lambda-Function_48.svg",
        "r-apigw-endpoint.png": f"{res}/Res_Networking-Content-Delivery/Res_Amazon-API-Gateway_Endpoint_48.svg",
        "r-iam-sts.png": f"{res}/Res_Security-Identity/Res_AWS-Identity-Access-Management_AWS-STS_48.svg",
        "r-iam-temp.png": f"{res}/Res_Security-Identity/Res_AWS-Identity-Access-Management_Temporary-Security-Credential_48.svg",
        "g-sdk.png": f"{res}/Res_General-Icons/Res_48_Dark/Res_SDK_48_Dark.svg",
        "g-padlock.png": f"{res}/Res_General-Icons/Res_48_Dark/Res_SSL-padlock_48_Dark.svg",
        "g-shield.png": f"{res}/Res_General-Icons/Res_48_Dark/Res_Shield_48_Dark.svg",
        "g-authuser.png": f"{res}/Res_General-Icons/Res_48_Dark/Res_Authenticated-User_48_Dark.svg",
        "g-globe.png": f"{res}/Res_General-Icons/Res_48_Dark/Res_Globe_48_Dark.svg",
        "g-servers.png": f"{res}/Res_General-Icons/Res_48_Dark/Res_Servers_48_Dark.svg",
        "g-magnifier.png": f"{res}/Res_General-Icons/Res_48_Dark/Res_Magnifying-Glass_48_Dark.svg",
        "az-apim.png": f"{azure}/Icons/devops/10042-icon-service-API-Management-Services.svg",
        "az-monitor.png": f"{azure}/Icons/management + governance/00001-icon-service-Monitor.svg",
        "az-appinsights.png": f"{azure}/Icons/monitor/00012-icon-service-Application-Insights.svg",
        "gc-apigw.png": f"{google}/cloud_api_gateway/cloud_api_gateway.png",
        "gc-logging.png": f"{google}/cloud_logging/cloud_logging.png",
        "gc-monitoring.png": f"{google}/cloud_monitoring/cloud_monitoring.png",
    }
    for dst, src in icons.items():
        svg_png(src, dst)
    # Capturas y diagramas oficiales de la documentación de AWS (sin modificar su contenido).
    shots = {
        "shot-lifecycle.png": ("Overview-Successful-Invokes.png", None),
        "shot-coldstart.png": ("perf-optimize-figure-1.png", None),
        "shot-conc.png": ("concurrency-7-reserved-vs-provisioned.png", None),
        "shot-lambda-code.png": ("python_code_editor.png", None),
        # Recortes legibles de las capturas del tutorial oficial de HTTP API (valores del tutorial).
        "shot-apigw-routes.png": ("ddb-create-routes.png", (790, 200, 2092, 1020)),
        "shot-apigw-integ.png": ("ddb-attach-integrations.png", (828, 330, 2204, 1280)),
        "shot-apigw-api.png": ("ddb-invoke-url.png", (120, 200, 1400, 640)),
        "shot-apigw-stage.png": ("ddb-invoke-url.png", (120, 720, 1280, 1030)),
        "shot-cw-streams.png": ("log-stream.png", None),
    }
    for dst, (src, box) in shots.items():
        im = Image.open(os.path.join(docimgs, src)).convert("RGB")
        if box:
            im = im.crop(box)
        im.save(os.path.join(OUT, dst), optimize=True)


if __name__ == "__main__":
    main(*sys.argv[1:5])
