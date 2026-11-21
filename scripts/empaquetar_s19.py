"""Paquete de S19 para los alumnos: la demo `demo-evaluacion` autocontenida en un ZIP.

    uv run python -m scripts.empaquetar_s19

Qué entra y por qué:

- Los archivos de `material/S19/demo-evaluacion` que Git versionaría (respeta los
  `.gitignore`): así no viajan `.venv`, `.env`, cachés ni ejecuciones propias de `resultados/`.
- `ENUNCIADO.md` en la raíz, generado desde `material/S19/enunciado.md` sin la cabecera de
  procedencia (lleva identificadores de correo que no son para los alumnos).

Qué no entra: `docs/guion-clase.md`, que es el guion del profesor y enlaza con material interno.

El ZIP es determinista (fechas fijas y orden alfabético): si el contenido no cambia, la huella
SHA-256 tampoco. La huella se guarda en `material/S19/paquetes/manifiesto.json`.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile

from scripts.empaquetar import ROOT

DEMO = ROOT / "material/S19/demo-evaluacion"
SALIDA = ROOT / "material/S19/paquetes"
NOMBRE = "S19-demo-evaluacion.zip"
CARPETA_ZIP = "s19-demo-evaluacion"
EXCLUIDOS = {"docs/guion-clase.md"}
FECHA_FIJA = (2026, 11, 21, 0, 0, 0)


def archivos_versionables() -> list[str]:
    """Rutas relativas a la demo que Git versionaría, en orden estable."""
    salida = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "."],
        cwd=DEMO,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    rutas = sorted(r for r in salida.split("\0") if r)
    return [r for r in rutas if r not in EXCLUIDOS and (DEMO / r).is_file()]


def enunciado_para_alumnos() -> str:
    """El enunciado sin la cita de procedencia del principio (líneas que empiezan por «>»)."""
    lineas = (ROOT / "material/S19/enunciado.md").read_text(encoding="utf-8").splitlines()
    titulo, resto = lineas[0], lineas[1:]
    while resto and (not resto[0].strip() or resto[0].startswith(">")):
        resto.pop(0)
    aviso = "> La práctica es **opcional**. La guía paso a paso está en `docs/ejercicio.md`."
    return "\n".join([titulo, "", aviso, "", *resto]) + "\n"


def _anadir(zf: zipfile.ZipFile, nombre: str, datos: bytes) -> None:
    info = zipfile.ZipInfo(f"{CARPETA_ZIP}/{nombre}", date_time=FECHA_FIJA)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, datos)


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    rutas = archivos_versionables()
    destino = SALIDA / NOMBRE
    with zipfile.ZipFile(destino, "w") as zf:
        _anadir(zf, "ENUNCIADO.md", enunciado_para_alumnos().encode("utf-8"))
        for ruta in rutas:
            _anadir(zf, ruta, (DEMO / ruta).read_bytes())
    huella = hashlib.sha256(destino.read_bytes()).hexdigest()
    manifiesto = [{"archivo": NOMBRE, "archivos": len(rutas) + 1, "sha256": huella}]
    (SALIDA / "manifiesto.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{destino.relative_to(ROOT)} · {len(rutas) + 1} archivos · sha256 {huella}")


if __name__ == "__main__":
    main()
