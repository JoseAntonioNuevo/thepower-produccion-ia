"""Piezas comunes de los tests.

Por defecto todo corre en el perfil doble, en memoria y con las copias de aula: sin red de
pago, sin Docker y sin claves. Los tests marcados `db` necesitan `docker compose up -d --wait`.
"""

import dataclasses

import pytest

from agente.config import cargar_config
from agente.servicios import crear_servicios


@pytest.fixture
def cfg(monkeypatch):
    # Se ignora cualquier variable S20_ del entorno: los tests no dependen de tu .env.
    for nombre in list(__import__("os").environ):
        if nombre.startswith("S20_") or nombre.startswith("LANGFUSE_"):
            monkeypatch.delenv(nombre)
    return cargar_config()


@pytest.fixture
def servicios(cfg):
    s = crear_servicios(cfg)
    yield s
    s.cerrar()


@pytest.fixture
def con_cfg(cfg):
    """Crea servicios cambiando campos de la configuración: con_cfg(max_herramientas=1)."""
    creados = []

    def _crear(cerebro=None, **cambios):
        s = crear_servicios(dataclasses.replace(cfg, **cambios), cerebro=cerebro)
        creados.append(s)
        return s

    yield _crear
    for s in creados:
        s.cerrar()
