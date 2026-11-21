"""Construye un ZIP Lambda en Linux amd64, sin claves ni operaciones de cuenta AWS."""

import base64
import hashlib
import json
import subprocess
import tempfile
import zipfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / ".build/s17"
    folder.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="lambda-", dir=folder))
    image = "thepower-s17:build"
    subprocess.run(
        [
            "docker",
            "build",
            "--platform",
            "linux/amd64",
            "--provenance=false",
            "-f",
            "infra/s17/Dockerfile",
            "-t",
            image,
            ".",
        ],
        cwd=ROOT,
        check=True,
    )
    container = subprocess.check_output(
        ["docker", "create", "--platform", "linux/amd64", "--entrypoint", "/bin/true", image],
        text=True,
    ).strip()
    try:
        subprocess.run(["docker", "cp", f"{container}:/asset/.", str(stage)], check=True)
    finally:
        subprocess.run(["docker", "rm", container], check=True, capture_output=True)
    files = [p for p in stage.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    size = sum(p.stat().st_size for p in files)
    if size > 250 * 1024 * 1024:
        raise ValueError("El paquete supera el límite descomprimido previsto para Lambda")
    archive = folder / "lambda-s17.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for file in sorted(files):
            info = zipfile.ZipInfo(str(file.relative_to(stage)), date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, file.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).digest()
    receipt = {
        "fecha_utc": datetime.now(UTC).isoformat(),
        "archive": archive.name,
        "sha256": digest.hex(),
        "code_sha256_base64": base64.b64encode(digest).decode(),
        "version": f"s17-{digest.hex()[:12]}",
        "platform": "linux/amd64",
        "runtime": "python3.12",
        "uncompressed_bytes": size,
        "compressed_bytes": archive.stat().st_size,
        "files": len(files),
        "build_runtime_demo": True,
        "aws_deployed": False,
        "real_bedrock": False,
    }
    (folder / "package.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
