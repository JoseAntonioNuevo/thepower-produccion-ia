"""Ejecuta el handler local con un doble de Bedrock, sin credenciales ni llamadas remotas."""

import json
from pathlib import Path

from curso_ia.serverless.config import Settings
from curso_ia.serverless.demo import DemoClient, DemoContext, event_for
from curso_ia.serverless.handler import handle


def main():
    valid = handle(event_for(), DemoContext(), cfg=Settings(mode="demo"), client=DemoClient())
    invalid = handle(event_for(""), DemoContext(), cfg=Settings(mode="demo"), client=DemoClient())
    if valid["statusCode"] != 200 or invalid["statusCode"] != 422:
        raise RuntimeError("La demostración no produjo los resultados esperados")
    folder = Path("evidencias/local")
    folder.mkdir(parents=True, exist_ok=True)
    result = {
        "execution": "demo",
        "aws_verificado": False,
        "bedrock_real": False,
        "respuesta": json.loads(valid["body"]),
        "entrada_invalida": invalid["statusCode"],
    }
    (folder / "s17-demo.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
