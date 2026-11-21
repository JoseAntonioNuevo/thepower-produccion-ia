"""Construye ZIPs por lista permitida; excluye claves, entornos y evidencia operativa."""

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "material/S16/paquetes"


def eligible(path):
    """No recorrer archivos privados aunque aparezcan dentro de una carpeta permitida."""
    relative = path.relative_to(ROOT)
    allowed_hidden = {".gitignore", ".dockerignore", ".python-version", ".env.example"}
    if any(part.startswith(".") for part in relative.parts) and str(relative) not in allowed_hidden:
        return False
    if any(
        x in {"__pycache__", ".venv", "node_modules", "paquetes", ".build"} for x in relative.parts
    ):
        return False
    return path.is_file() and not path.is_symlink() and path.suffix not in {".pyc", ".pem", ".key"}


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    root_files = [
        "pyproject.toml",
        "uv.lock",
        "requirements.lock",
        ".python-version",
        ".gitignore",
        ".env.example",
    ]
    common = [ROOT / name for name in root_files]
    common += list((ROOT / "src/curso_ia").glob("*.py"))
    common += [ROOT / "tests/test_api.py", ROOT / "tests/test_proveedor.py"]
    common += [
        ROOT / "scripts" / name for name in ["__init__.py", "preflight.py", "ensayo_local.py"]
    ]
    common += list((ROOT / "datos").glob("peticion*.json"))
    solution = [
        ROOT / name
        for name in root_files + ["AGENTS.md", "Dockerfile", ".dockerignore", "compose.yaml"]
    ]
    # El paquete de S16 no arrastra Lambda/Bedrock ni la planificación de otras clases.
    solution += list((ROOT / "src/curso_ia").glob("*.py"))
    solution += [
        ROOT / "scripts" / name
        for name in ["__init__.py", "preflight.py", "ensayo_local.py", "aws_lab.py", "costes.py"]
    ]
    solution += [
        ROOT / "tests" / name
        for name in ["test_api.py", "test_proveedor.py", "test_operaciones.py"]
    ]
    solution += list((ROOT / "datos").glob("*.json"))
    solution += [
        ROOT / "docs/arquitectura.md",
        ROOT / "docs/fuentes/temario-ai-engineer.txt",
        ROOT / "docs/fuentes/tarifas-aws-2026-10-17.json",
    ]
    for folder in ("infra/s16", "material/S16"):
        solution += [p for p in (ROOT / folder).rglob("*") if eligible(p)]
    manifest = []
    for label, paths in (("S16-inicio", common), ("S16-referencia", solution)):
        dest = OUTPUT / f"{label}.zip"
        with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(set(paths)):
                if eligible(file):
                    archive.write(file, str(file.relative_to(ROOT)))
            if label == "S16-inicio":
                archive.writestr(
                    "README.md",
                    """# Punto de partida S16

Versión común para el 12 y 18 de noviembre de 2026. Práctica opcional.
Incluye la API y sus tests. Si decides hacerla, construirás Docker y desplegarás en AWS.
También protegerás secretos y prepararás evidencias, coste y limpieza conforme al enunciado.
Sigue la guía paso a paso entregada junto a este ZIP. El paquete S16-referencia
contiene la solución docente para consultar cada paso sin recorrer otras sesiones.

Desde esta carpeta:
    uv sync --frozen --all-extras
    uv run pytest
    uv run python scripts/preflight.py
    uv run uvicorn curso_ia.api:create_app --factory --host 127.0.0.1 --port 8016

En otra terminal:
    uv run python scripts/ensayo_local.py

El modo inicial es demo y no consume modelos. No incluye un Dockerfile resuelto.
""",
                )
            else:
                # Reemplazar el índice general por la entrada específica de esta sesión.
                archive.writestr(
                    "README.md",
                    """# Referencia S16

Versión común para el 12 y 18 de noviembre de 2026. La práctica es opcional.
Empieza por material/S16/README.md y sigue material/S16/guia-alumno.md.
Este ZIP contiene la API, Docker, scripts, plantillas AWS y materiales de S16.
Para practicar desde una API preparada, usa S16-inicio.zip y la guía entregada.
Los comandos AWS de creación, publicación, inferencia y retirada generan operaciones
reales; ejecuta solo dentro de la cuenta y presupuesto autorizados del laboratorio.
""",
                )
                # Las herramientas que respetan enlaces Unix restauran CLAUDE.md como symlink.
                link = zipfile.ZipInfo("CLAUDE.md")
                link.create_system = 3
                link.external_attr = 0o120777 << 16
                archive.writestr(link, "AGENTS.md")
        with zipfile.ZipFile(dest) as archive:
            names = archive.namelist()
            assert ".env" not in names and not any(n.startswith("evidencias/") for n in names)
            assert not any("serverless" in n or "/s17/" in n or "_s17" in n for n in names)
        manifest.append(
            {
                "archivo": dest.name,
                "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
                "archivos": len(names),
            }
        )
    (OUTPUT / "manifiesto.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
