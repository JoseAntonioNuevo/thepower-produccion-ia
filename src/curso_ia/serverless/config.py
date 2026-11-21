"""Configuración pequeña, sin cargar credenciales ni abrir conexiones al importar."""

import os
import re
from dataclasses import dataclass

REFERENCE_MODEL = "eu.amazon.nova-2-lite-v1:0"


@dataclass(frozen=True)
class Settings:
    """La referencia del ejercicio es europea. No hay sustitución a un perfil global."""

    model_id: str = REFERENCE_MODEL
    region: str = "eu-west-1"
    mode: str = "real"
    version: str = "s17-desarrollo"
    max_tokens: int = 300

    def __post_init__(self):
        if not re.fullmatch(r"eu\.[a-zA-Z0-9.:-]{1,140}", self.model_id):
            raise ValueError("BEDROCK_MODEL_ID debe identificar un perfil europeo explícito")
        if not re.fullmatch(r"eu-[a-z]+-\d", self.region):
            raise ValueError("La región de este laboratorio debe ser europea")
        if self.mode not in {"real", "demo"} or not 50 <= self.max_tokens <= 1000:
            raise ValueError("Modo o límite de tokens inválido")
        if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", self.version):
            raise ValueError("Versión inválida")

    @classmethod
    def from_env(cls):
        return cls(
            model_id=os.getenv("BEDROCK_MODEL_ID", REFERENCE_MODEL),
            region=os.getenv("AWS_REGION", "eu-west-1"),
            mode=os.getenv("S17_MODE", "real"),
            version=os.getenv("APP_VERSION", "s17-desarrollo"),
            max_tokens=int(os.getenv("S17_MAX_OUTPUT_TOKENS", "300")),
        )
