"""Paquetes S17 autocontenidos. Reutiliza la lista de exclusiones de la base común."""

import hashlib
import json
import shutil
import zipfile

from scripts.empaquetar import ROOT, eligible


def main():
    output = ROOT / "material/S17/paquetes"
    output.mkdir(parents=True, exist_ok=True)
    root_names = [
        "pyproject.toml",
        "uv.lock",
        "requirements.lock",
        ".python-version",
        ".gitignore",
        ".env.example",
    ]
    starter = [ROOT / n for n in root_names]
    starter += list((ROOT / "src/curso_ia").glob("*.py"))
    starter += [ROOT / "tests/test_api.py", ROOT / "tests/test_proveedor.py"]
    starter += [ROOT / "scripts" / n for n in ["preflight.py", "ensayo_local.py", "__init__.py"]]
    starter += list((ROOT / "datos").glob("peticion*.json"))
    solution = [
        ROOT / n
        for n in root_names
        + ["README.md", "AGENTS.md", "Dockerfile", ".dockerignore", "compose.yaml"]
    ]
    for folder in [
        "src",
        "scripts",
        "tests",
        "datos",
        "infra",
        "docs",
        "material/S16",
        "material/S17",
    ]:
        solution += [p for p in (ROOT / folder).rglob("*") if eligible(p)]
    manifest = []
    for name, paths in [("S17-inicio", starter), ("S17-referencia", solution)]:
        dest = output / f"{name}.zip"
        with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for file in sorted(set(paths)):
                if eligible(file):
                    z.write(file, str(file.relative_to(ROOT)))
            if name == "S17-inicio":
                z.writestr(
                    "README.md",
                    """# Punto de partida S17

Contiene la API y contratos de soporte para alumnos que no tienen nuestra S16.
El trabajo autónomo es construir Lambda, Bedrock, la HTTP API IAM, firma, medidas,
costes y retirada según el enunciado. El paquete S17-referencia contiene la solución
y la guía completa; sus comandos AWS requieren esa versión resuelta.

Desde esta carpeta:
    uv sync --frozen --all-extras
    uv run pytest
    uv run python scripts/preflight.py
    uv run uvicorn curso_ia.api:create_app --factory --host 127.0.0.1 --port 8016

En otra terminal:
    uv run python scripts/ensayo_local.py

Es una demostración local, sin AWS ni modelos de pago.
""",
                )
            else:
                link = zipfile.ZipInfo("CLAUDE.md")
                link.create_system = 3
                link.external_attr = 0o120777 << 16
                z.writestr(link, "AGENTS.md")
        with zipfile.ZipFile(dest) as z:
            names = z.namelist()
            if any(n.startswith(("evidencias/", ".build/", ".venv/", ".git/")) for n in names):
                raise ValueError("Paquete con contenido privado inesperado")
        manifest.append(
            {
                "archivo": dest.name,
                "archivos": len(names),
                "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
            }
        )
    # El ZIP desplegable se entrega aparte para evitar archivos comprimidos anidados.
    package = ROOT / ".build/s17/lambda-s17.zip"
    if package.exists():
        data = json.loads((ROOT / ".build/s17/package.json").read_text())
        if hashlib.sha256(package.read_bytes()).hexdigest() != data["sha256"]:
            raise ValueError("El ZIP Lambda y el manifiesto no coinciden")
        shutil.copyfile(package, output / "lambda-s17.zip")
        shutil.copyfile(ROOT / ".build/s17/package.json", output / "lambda-manifiesto.json")
        manifest.append(
            {
                "archivo": "lambda-s17.zip",
                "sha256": data["sha256"],
                "platform": "linux/amd64",
                "aws_deployed": False,
            }
        )
    (output / "manifiesto.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
