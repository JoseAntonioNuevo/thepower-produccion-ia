"""Preflight offline: informa presencia y versiones sin imprimir secretos ni llamar AWS."""

import importlib.metadata
import json
import platform
import shutil

from curso_ia.config import Settings


def main():
    """Una configuración real incompleta produce salida 2 y un mensaje saneado."""
    try:
        cfg = Settings.from_env()
    except ValueError:
        print("Configuración inválida: revisa API_MODE, MODEL_ID, límites y ANTHROPIC_API_KEY.")
        raise SystemExit(2) from None
    print(
        json.dumps(
            {
                "python": platform.python_version(),
                "execution": cfg.mode,
                "version": cfg.app_version,
                "modelo_configurado": bool(cfg.model_id),
                "clave_presente": bool(cfg.api_key.get_secret_value()),
                "docker_cli": shutil.which("docker") is not None,
                "fastapi": importlib.metadata.version("fastapi"),
                "comprobaciones_remotas": "no_ejecutadas",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
