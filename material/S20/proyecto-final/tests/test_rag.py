"""Ingesta y recuperación con el almacén en memoria y el embedding doble."""

from agente.almacen import AlmacenMemoria
from agente.config import DIM
from agente.rag import CORPUS, EmbeddingsDoble, fragmentar, ingestar, recuperar


def test_fragmentar_conserva_titulo_y_seccion_para_poder_citar():
    fragmentos = fragmentar(CORPUS / "03-limites-y-cuotas-api.md")
    assert [f.fragmento_id for f in fragmentos] == [
        "03-limites-y-cuotas-api#1",
        "03-limites-y-cuotas-api#2",
    ]
    assert fragmentos[0].seccion == "Cuotas por plan de suscripción"
    assert "120 peticiones por minuto" in fragmentos[0].contenido


def test_el_embedding_doble_tiene_la_dimension_del_esquema():
    vector = EmbeddingsDoble().consulta("límite de peticiones")
    assert len(vector) == DIM


def test_ingestar_dos_veces_no_duplica():
    almacen, embeddings = AlmacenMemoria(), EmbeddingsDoble()
    primera = ingestar(almacen, embeddings)
    segunda = ingestar(almacen, embeddings)
    assert (
        primera == segunda == {"documentos": 10, "fragmentos": 20, "modelo_embeddings": "doble-hash-768"}
    )


def test_recupera_con_cita(servicios):
    r = recuperar(
        servicios.cfg,
        servicios.almacen,
        servicios.embeddings,
        "¿Cuál es el límite de peticiones del plan Estándar?",
    )
    assert r["ok"] is True
    assert r["fragmentos"][0]["cita"] == "03-limites-y-cuotas-api § Cuotas por plan de suscripción"


def test_sin_evidencia_no_devuelve_fragmentos(servicios):
    r = recuperar(
        servicios.cfg,
        servicios.almacen,
        servicios.embeddings,
        "¿Cuál es la política de teletrabajo de los empleados?",
    )
    assert r["ok"] is False and r["motivo"] == "sin_evidencia" and r["fragmentos"] == []
    assert r["mejor_similitud"] < r["umbral"]


def test_un_indice_de_otro_modelo_no_se_mezcla(servicios):
    # Regla de oro: mismo modelo al indexar y al consultar. Otro modelo no encuentra nada.
    vecinos = servicios.almacen.buscar_fragmentos(servicios.embeddings.consulta("SLA"), 3, "otro-modelo")
    assert vecinos == []
