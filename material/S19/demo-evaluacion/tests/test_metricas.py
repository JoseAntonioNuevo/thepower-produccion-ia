"""precision@5 y recall@5 sobre DOCUMENTOS, con sus denominadores."""

import pytest

from evaluacion.metricas import (
    contiene_dato,
    evaluar_caso,
    media,
    precision_at_k,
    recall_at_k,
    techo_precision,
)
from rag.consulta import documentos_distintos


def test_dos_fragmentos_del_mismo_documento_son_un_acierto():
    fragmentos = ["05-sla", "05-sla", "07-fact", "05-sla", "03-lim"]
    assert documentos_distintos(fragmentos, 5) == ["05-sla", "07-fact", "03-lim"]
    assert precision_at_k(fragmentos, ["05-sla"]) == pytest.approx(1 / 5)  # no 3/5
    assert recall_at_k(fragmentos, ["05-sla"]) == 1.0


def test_denominadores():
    recuperados = ["a", "b", "c", "d", "e"]
    relevantes = ["a", "c", "z"]
    assert precision_at_k(recuperados, relevantes) == pytest.approx(2 / 5)  # entre 5 puestos
    assert recall_at_k(recuperados, relevantes) == pytest.approx(2 / 3)  # entre 3 relevantes


def test_un_puesto_vacio_cuenta_como_fallo_en_precision():
    assert precision_at_k(["a"], ["a"]) == pytest.approx(0.2)
    assert techo_precision(["a"]) == pytest.approx(0.2)  # con 1 relevante no se puede pasar de 0,20


def test_solo_cuentan_los_cinco_primeros_documentos():
    assert recall_at_k(["a", "b", "c", "d", "e", "z"], ["z"]) == 0.0


def test_sin_documentos_relevantes_no_existe_recall():
    with pytest.raises(ValueError, match="rechazo"):
        recall_at_k(["a"], [])


def test_media_sin_datos_es_none_y_no_cero():
    assert media([]) is None
    assert media([None, float("nan")]) is None
    assert media([0.5, None, 1.0]) == 0.75


@pytest.mark.parametrize(
    "texto, dato, esperado",
    [
        ("admite 100 peticiones", "10", False),
        ("admite 10 peticiones", "10", True),
        ("crédito del 25 %", "25 %", True),
        ("disponibilidad del 99,95 %", "99,9", False),
        ("usa Tls 1.3.", "TLS 1.3", True),
        ("Rotación automática", "rotacion", True),
    ],
)
def test_contiene_dato(texto, dato, esperado):
    assert contiene_dato(texto, dato) is esperado


CASO = {"caso_id": "T", "respondible": True, "documentos_relevantes": ["05-sla"], "datos_clave": ["25 %"]}


def test_acierto_exige_dato_clave_y_cita_de_referencia():
    fila = {
        "documentos_recuperados": ["05-sla"],
        "rechazo": False,
        "error": None,
        "response": "El crédito es del 25 % [05-sla]",
        "fuentes": ["05-sla"],
    }
    assert evaluar_caso(CASO, fila)["acierto"] is True
    assert evaluar_caso(CASO, {**fila, "fuentes": ["07-fact"]})["acierto"] is False
    assert evaluar_caso(CASO, {**fila, "response": "Es del 10 % [05-sla]"})["datos_clave_ausentes"] == ["25 %"]


def test_abstencion_incorrecta_y_rechazo_correcto_se_cuentan_aparte():
    rechazo = {"documentos_recuperados": ["05-sla"], "rechazo": True, "error": None, "response": "No consta", "fuentes": []}
    e = evaluar_caso(CASO, rechazo)
    assert (e["abstencion_incorrecta"], e["acierto"], e["recall_at_5"]) == (True, False, 1.0)
    sin = {"caso_id": "N", "respondible": False, "documentos_relevantes": [], "datos_clave": []}
    e = evaluar_caso(sin, rechazo)
    assert (e["rechazo_correcto"], e["recall_at_5"], e["precision_at_5"]) == (True, None, None)


def test_un_error_del_sistema_no_es_acierto_ni_rechazo():
    e = evaluar_caso(CASO, {"error": "ErrorProveedor: x", "rechazo": False, "documentos_recuperados": []})
    assert (e["acierto"], e["recall_at_5"], e["abstencion_incorrecta"]) == (None, None, None)
