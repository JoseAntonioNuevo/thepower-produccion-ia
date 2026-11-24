"""El grafo de LangGraph de la consulta: enrutado, trayectoria y pasos en vivo.

Como en los tests de agentes, aquí no se mira el texto final sino el CAMINO: qué nodos
recorre cada pregunta y si llama o no al modelo. Todo sin red: almacén en memoria y
generadores simulados.
"""

import pytest

from rag.consulta import responder
from rag.grafo import NODOS, construir_grafo, ejecutar_consulta, hay_evidencia
from rag.proveedores import NO_CONSTA, Proveedores
from tests.conftest import GeneradorSimulado, config

PREGUNTA = "¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?"


@pytest.mark.parametrize(
    "similitud, umbral, esperado",
    [
        (0.78, 0.5223, True),
        (0.5223, 0.5223, True),  # justo en el umbral cuenta como evidencia
        (0.38, 0.5223, False),
        (None, 0.5223, False),  # la búsqueda no devolvió nada
    ],
)
def test_tabla_de_enrutado_tras_recuperar(similitud, umbral, esperado):
    """Compara la decisión con una tabla que incluye la igualdad y la búsqueda vacía, dos casos límite del umbral."""
    assert hay_evidencia(similitud, umbral) is esperado


def test_el_grafo_tiene_los_nodos_y_las_ramas_del_diagrama(cfg, sistema):
    """Inspecciona los nodos y las aristas del grafo compilado para detectar conexiones distintas de las del diagrama."""
    almacen, prov, indice_id = sistema
    g = construir_grafo(cfg, almacen, prov, indice_id).get_graph()
    assert set(NODOS) <= set(g.nodes)
    aristas = {(a.source, a.target) for a in g.edges}
    assert {
        ("__start__", "recuperar"),
        ("recuperar", "generar"),
        ("recuperar", "rechazo_previo"),
        ("generar", "comprobar"),
        ("comprobar", "__end__"),
        ("rechazo_previo", "__end__"),
    } == aristas


def test_con_evidencia_recorre_recuperar_generar_comprobar(sistema):
    """Pregunta por TLS con un generador simulado y comprueba la ruta y el contador.
    Una respuesta con evidencia debe pasar por la comprobación de fuentes y generar una sola vez."""
    almacen, prov, indice_id = sistema
    generador = GeneradorSimulado("Exigen TLS 1.3 [01-arquitectura-aethercloud].")
    estado = ejecutar_consulta(config(), almacen, Proveedores(prov.embeddings, generador), indice_id, PREGUNTA)
    assert estado["ruta"] == ["recuperar", "generar", "comprobar"]
    assert generador.llamadas == 1 and estado["respuesta"].rechazo is False


def test_sin_evidencia_toma_la_rama_de_rechazo_previo_sin_llamar_al_modelo(sistema):
    """Sube el umbral para forzar el rechazo. Comprueba la ruta, el contador y el coste de generación
    para detectar llamadas innecesarias cuando falta evidencia."""
    almacen, prov, indice_id = sistema
    generador = GeneradorSimulado("no debería ejecutarse")
    estado = ejecutar_consulta(
        config(umbral_evidencia=0.99), almacen, Proveedores(prov.embeddings, generador), indice_id, PREGUNTA
    )
    r = estado["respuesta"]
    assert estado["ruta"] == ["recuperar", "rechazo_previo"]
    assert generador.llamadas == 0
    assert (r.motivo_rechazo, r.coste_usd, r.coste_fuente) == ("evidencia_insuficiente", 0.0, "sin_llamada")
    assert r.latencia_ms["generacion"] == 0.0


def test_el_rechazo_del_modelo_pasa_por_generar_y_lo_detecta_comprobar(sistema):
    """Hace que el generador devuelva NO_CONSTA y verifica que el grafo registra la llamada y el motivo de la abstención."""
    almacen, prov, indice_id = sistema
    generador = GeneradorSimulado(NO_CONSTA)
    estado = ejecutar_consulta(config(), almacen, Proveedores(prov.embeddings, generador), indice_id, PREGUNTA)
    assert estado["ruta"] == ["recuperar", "generar", "comprobar"]
    assert estado["respuesta"].motivo_rechazo == "generador_sin_respuesta" and generador.llamadas == 1


def test_el_stream_entrega_cada_paso_en_orden_y_no_cambia_el_resultado(cfg, sistema):
    """Ejecuta la misma pregunta con y sin streaming. Comprueba los pasos y compara la salida salvo las latencias
    para que mostrar el progreso en la TUI conserve el resultado del RAG."""
    almacen, prov, indice_id = sistema
    pasos = []
    con_stream = responder(cfg, almacen, prov, indice_id, PREGUNTA, al_paso=pasos.append)
    sin_stream = responder(cfg, almacen, prov, indice_id, PREGUNTA)
    assert [next(iter(p)) for p in pasos] == ["recuperar", "generar", "comprobar"]
    assert "respuesta" in pasos[-1]["comprobar"]
    quitar = {"latencia_ms"}
    assert {k: v for k, v in con_stream.como_dict().items() if k not in quitar} == {
        k: v for k, v in sin_stream.como_dict().items() if k not in quitar
    }


def test_el_error_del_proveedor_atraviesa_el_grafo_sin_cambiar_de_tipo(cfg, sistema):
    """Simula un timeout y exige que se propague al llamante para que pueda distinguirlo de un rechazo por falta de evidencia."""
    almacen, prov, indice_id = sistema
    generador = GeneradorSimulado(error=TimeoutError("sin respuesta"))
    with pytest.raises(TimeoutError):
        ejecutar_consulta(cfg, almacen, Proveedores(prov.embeddings, generador), indice_id, PREGUNTA, al_paso=lambda _: None)
