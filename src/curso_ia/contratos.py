"""Contrato compartido de S16: la API valida tanto al cliente como al proveedor.

La taxonomía viene de S7/S8. Las métricas y la identidad de ejecución se colocan
fuera de la respuesta redactada por el modelo para que este no pueda inventarlas.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Incidencia(BaseModel):
    """Entrada acotada, sin campos que permitan cambiar proveedor o instrucciones."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    texto: str = Field(min_length=5, max_length=2000, description="Incidencia ficticia de soporte")


class Clasificacion(BaseModel):
    """La salida del modelo debe cumplir este esquema, aunque el prompt pida JSON."""

    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)
    categoria: Literal["acceso", "facturacion", "tecnico", "consulta"]
    prioridad: Literal["alta", "media", "baja"]
    respuesta: str = Field(min_length=1, max_length=1000)


class Consumo(BaseModel):
    """Solo guardamos cantidades observadas; nulo significa desconocido."""

    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    cache_creation_input_tokens: int | None = Field(default=None, ge=0)
    cache_read_input_tokens: int | None = Field(default=None, ge=0)
    coste_usd: None = None
    metodo_coste: Literal["no_disponible", "sin_llamada"] = "no_disponible"


class ResultadoProveedor(BaseModel):
    """Resultado normalizado independiente del transporte HTTP de nuestra API."""

    clasificacion: Clasificacion
    modelo_devuelto: str
    consumo: Consumo
