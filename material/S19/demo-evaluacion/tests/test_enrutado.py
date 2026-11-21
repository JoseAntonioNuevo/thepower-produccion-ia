"""Ampliación opcional: tests de DECISIONES y de límite de llamadas de un bucle CRAG."""

import pytest

from ampliacion.crag import crag, decidir
from rag.proveedores import Proveedores
from tests.conftest import GeneradorSimulado, config


@pytest.mark.parametrize(
    "similitud, intento, esperado",
    [
        (0.60, 1, "responder"),
        (0.28, 1, "responder"),  # justo en el umbral
        (0.10, 1, "reformular"),  # sin evidencia y queda un intento
        (0.10, 2, "rechazar"),  # sin evidencia y sin intentos
        (None, 2, "rechazar"),  # la búsqueda no devolvió nada
    ],
)
def test_tabla_de_decisiones(similitud, intento, esperado):
    assert decidir(similitud, umbral=0.28, intento=intento, max_intentos=2) == esperado


def test_con_evidencia_responde_al_primer_intento(cfg, sistema):
    almacen, prov, indice_id = sistema
    t = crag(cfg, almacen, prov, indice_id, "¿Qué versión de TLS exigen las pasarelas perimetrales?")
    assert t.decisiones == ["responder"]
    assert (t.llamadas_recuperacion, t.llamadas_generacion) == (1, 1)


def test_sin_evidencia_reformula_y_rechaza_sin_generar(sistema):
    almacen, prov, indice_id = sistema
    generador = GeneradorSimulado("no debería ejecutarse")
    t = crag(
        config(umbral_evidencia=0.99),
        almacen,
        Proveedores(prov.embeddings, generador),
        indice_id,
        "¿Cuál es el horario de la cafetería?",
        max_intentos=3,
    )
    assert t.decisiones == ["reformular", "reformular", "rechazar"]
    assert t.llamadas_recuperacion == 3  # límite respetado: ni una más
    assert generador.llamadas == 0 and t.respuesta is None


def test_una_reformulacion_puede_encontrar_evidencia(sistema):
    almacen, prov, indice_id = sistema
    consultas = iter(["¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?"])
    t = crag(
        config(umbral_evidencia=0.30), almacen, prov, indice_id, "tls?", reformular=lambda _: next(consultas), max_intentos=2
    )
    assert t.decisiones == ["reformular", "responder"]
    assert len(t.consultas) == 2 and t.llamadas_generacion == 1


def test_el_limite_de_intentos_es_obligatorio(cfg, sistema):
    almacen, prov, indice_id = sistema
    with pytest.raises(ValueError):
        crag(cfg, almacen, prov, indice_id, "¿hola?", max_intentos=0)
