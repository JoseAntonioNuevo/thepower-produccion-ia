"""Integración con PostgreSQL + pgvector. Necesita:  docker compose up -d --wait

Se ejecutan con:  uv run pytest -m db
"""

import uuid

import pytest

from agente.rag import ingestar

pytestmark = pytest.mark.db


@pytest.fixture
def pg(con_cfg):
    def _crear():
        s = con_cfg(almacen="postgres")
        ingestar(s.almacen, s.embeddings)
        return s

    return _crear


def test_la_conversacion_continua_tras_reiniciar_el_proceso(pg):
    hilo = f"reinicio-{uuid.uuid4().hex[:8]}"
    antes = pg()
    antes.conversar(usuario="ana", thread_id=hilo, mensaje="¿Cómo está el ticket T-200?")
    antes.cerrar()  # se cierra el pool: es lo más parecido a parar el proceso
    despues = pg()  # servicios nuevos, grafo nuevo, misma base de datos
    r = despues.conversar(usuario="ana", thread_id=hilo, mensaje="¿Qué ticket estábamos viendo?")
    assert "T-200" in r["respuesta"]


def test_la_propiedad_de_la_conversacion_se_guarda_en_la_base(pg):
    hilo = f"dueno-{uuid.uuid4().hex[:8]}"
    s = pg()
    assert s.almacen.asegurar_conversacion(hilo, "ana") is True
    assert s.almacen.asegurar_conversacion(hilo, "luis") is False
    assert s.almacen.propietario(hilo) == "ana"


def test_pgvector_devuelve_el_mismo_fragmento_que_la_memoria(pg, servicios):
    pregunta = "¿Cuál es el límite de peticiones del plan Estándar?"
    s = pg()
    en_pg = s.almacen.buscar_fragmentos(s.embeddings.consulta(pregunta), 1, s.embeddings.nombre)
    en_ram = servicios.almacen.buscar_fragmentos(
        servicios.embeddings.consulta(pregunta), 1, servicios.embeddings.nombre
    )
    assert en_pg[0][0].fragmento_id == en_ram[0][0].fragmento_id == "03-limites-y-cuotas-api#1"
    assert abs(en_pg[0][1] - en_ram[0][1]) < 1e-3


def test_reingestar_no_duplica_fragmentos(pg):
    s = pg()
    ingestar(s.almacen, s.embeddings)
    assert s.almacen.contar_fragmentos() == 20


def test_dos_ejecutores_no_toman_el_mismo_trabajo(pg):
    s = pg()
    # Se vacía la cola para que el test no dependa de trabajos de otras ejecuciones.
    while s.almacen.tomar_pendiente():
        pass
    trabajo = s.almacen.crear_trabajo(f"cola-{uuid.uuid4().hex[:8]}", "ana", "cabecera Retry-After")
    primero, segundo = s.almacen.tomar_pendiente(), s.almacen.tomar_pendiente()
    assert primero["trabajo_id"] == trabajo["trabajo_id"] and segundo is None
