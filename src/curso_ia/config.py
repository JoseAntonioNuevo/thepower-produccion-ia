"""Configuración explícita: importar este módulo no carga archivos ni llama a la red."""

import os
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


class Settings(BaseModel):
    """Una configuración real incompleta falla al arrancar, nunca usa el modo demo."""

    model_config = ConfigDict(extra="forbid")
    mode: Literal["demo", "real"] = "demo"
    app_version: str = Field(default="desarrollo-local", pattern=r"^[A-Za-z0-9._-]{1,80}$")
    model_id: str = Field(default="", max_length=160)
    api_key: SecretStr = SecretStr("")
    timeout_seconds: float = Field(default=15, ge=1, le=25)
    max_output_tokens: int = Field(default=300, ge=50, le=1000)

    @model_validator(mode="after")
    def real_necesita_configuracion(self):
        """No incluir nunca el valor de la clave en los errores de configuración."""
        if self.mode == "real" and (
            not self.model_id.strip() or not self.api_key.get_secret_value()
        ):
            raise ValueError("Modo real requiere MODEL_ID y ANTHROPIC_API_KEY")
        return self

    @classmethod
    def from_env(cls):
        """El lanzador decide si lee .env; el contenedor recibe variables de ECS."""
        return cls(
            mode=os.getenv("API_MODE", "demo"),
            app_version=os.getenv("APP_VERSION", "desarrollo-local"),
            model_id=os.getenv("MODEL_ID", ""),
            api_key=SecretStr(os.getenv("ANTHROPIC_API_KEY", "")),
            timeout_seconds=os.getenv("PROVIDER_TIMEOUT_SECONDS", "15"),
            max_output_tokens=os.getenv("MAX_OUTPUT_TOKENS", "300"),
        )
