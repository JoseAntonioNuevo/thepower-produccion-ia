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
    """Ejecuta la regla con la similitud y el intento de cada fila. Compara la decisión con la esperada
    para detectar cuándo el agente responde, reintenta o abandona antes de tiempo."""
    assert decidir(similitud, umbral=0.28, intento=intento, max_intentos=2) == esperado


def test_con_evidencia_responde_al_primer_intento(cfg, sistema):
    """Pregunta por TLS y verifica una búsqueda del agente y una generación para detectar reintentos innecesarios."""
    almacen, prov, indice_id = sistema
    t = crag(cfg, almacen, prov, indice_id, "¿Qué versión de TLS exigen las pasarelas perimetrales?")
    assert t.decisiones == ["responder"]
    assert (t.llamadas_recuperacion, t.llamadas_generacion) == (1, 1)


def test_sin_evidencia_reformula_y_rechaza_sin_generar(sistema):
    """Fuerza evidencia insuficiente durante tres intentos. Comprueba dos reformulaciones, tres búsquedas
    y cero llamadas al generador para verificar que el agente se detiene al agotar el presupuesto."""
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
    """Sustituye la consulta ambigua por una pregunta concreta sobre TLS y comprueba que el segundo intento llega a generar."""
    almacen, prov, indice_id = sistema
    consultas = iter(["¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?"])
    t = crag(
        config(umbral_evidencia=0.30), almacen, prov, indice_id, "tls?", reformular=lambda _: next(consultas), max_intentos=2
    )
    assert t.decisiones == ["reformular", "responder"]
    assert len(t.consultas) == 2 and t.llamadas_generacion == 1


def test_el_limite_de_intentos_es_obligatorio(cfg, sistema):
    """Pasa cero intentos y espera ValueError para impedir que se inicie un agente sin una primera búsqueda posible."""
    almacen, prov, indice_id = sistema
    with pytest.raises(ValueError):
        crag(cfg, almacen, prov, indice_id, "¿hola?", max_intentos=0)


def test_la_trayectoria_del_grafo_queda_registrada(sistema):
    """Compara la secuencia completa de nodos con la esperada para detectar búsquedas o reformulaciones de más."""
    almacen, prov, indice_id = sistema
    t = crag(config(umbral_evidencia=0.99), almacen, prov, indice_id, "¿Cuál es el horario de la cafetería?", max_intentos=3)
    assert t.ruta == ["recuperar", "reformular", "recuperar", "reformular", "recuperar", "rechazar"]


def test_con_evidencia_la_trayectoria_es_recuperar_y_responder(cfg, sistema):
    """Comprueba la ruta de una pregunta con evidencia para detectar si el grafo da un rodeo antes de responder."""
    almacen, prov, indice_id = sistema
    t = crag(cfg, almacen, prov, indice_id, "¿Qué versión de TLS exigen las pasarelas perimetrales?")
    assert t.ruta == ["recuperar", "responder"]


def test_recursion_limit_corta_una_regla_que_no_deja_de_reformular(sistema):
    """Inyecta una regla que siempre pide reintentar y comprueba que LangGraph lanza GraphRecursionError.
    Así prueba el límite de seguridad incluso cuando falla la regla de negocio."""
    from langgraph.errors import GraphRecursionError

    almacen, prov, indice_id = sistema
    consultas = []

    def reformular(c):
        """Anota cada reintento y devuelve la misma consulta para medir cuánto dura el bucle provocado por el test."""
        consultas.append(c)
        return c

    with pytest.raises(GraphRecursionError):
        crag(
            config(umbral_evidencia=0.99),
            almacen,
            prov,
            indice_id,
            "¿Cuál es el horario de la cafetería?",
            reformular=reformular,
            max_intentos=2,
            regla=lambda *_: "reformular",  # regla rota: nunca decide parar
        )
    assert len(consultas) <= 3  # 2 intentos → como mucho 5 pasos: el corte llega enseguida
