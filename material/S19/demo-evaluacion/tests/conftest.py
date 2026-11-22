"""Piezas comunes de los tests: configuración doble, índice en memoria y generadores simulados."""

import pytest

from rag.almacen import AlmacenMemoria
from rag.config import Config
from rag.ingesta import reconstruir_indice
from rag.proveedores import EmbeddingsDoble, Generacion, GeneradorDoble, Proveedores


def config(**cambios) -> Config:
    base = dict(
        perfil="doble",
        database_url="no-se-usa",
        embedding_modelo="doble-hash-768",
        embedding_dim=768,
        gen_modelo="doble-extractivo",
        chunk_size=320,
        chunk_overlap=0,
        k_fragmentos=12,
        k_documentos=5,
        k_contexto=4,
        umbral_evidencia=0.2787,
        prompt_version="v1",
        config_id="A",
    )
    return Config(**{**base, **cambios})


class GeneradorSimulado:
    """Devuelve un texto fijo o lanza una excepción: prueba formato y errores sin modelo."""

    nombre = "simulado"

    def __init__(
        self, texto="", error=None, tokens=(None, None), model_version=None, coste_usd=None, proveedor_servido=None
    ):
        self.texto, self.error, self.tokens, self.llamadas = texto, error, tokens, 0
        self.model_version, self.coste_usd, self.proveedor_servido = model_version, coste_usd, proveedor_servido

    def generar(self, pregunta, contextos, prompt_version):
        self.llamadas += 1
        if self.error:
            raise self.error
        return Generacion(
            self.texto,
            *self.tokens,
            model_version=self.model_version,
            coste_usd=self.coste_usd,
            proveedor_servido=self.proveedor_servido,
        )


@pytest.fixture
def cfg():
    return config()


@pytest.fixture
def sistema(cfg):
    """(almacén en memoria con el corpus indexado, proveedores dobles, id del índice)."""
    almacen, prov = AlmacenMemoria(), Proveedores(EmbeddingsDoble(), GeneradorDoble())
    indice = reconstruir_indice(cfg, almacen, prov.embeddings)
    return almacen, prov, indice.indice_id
