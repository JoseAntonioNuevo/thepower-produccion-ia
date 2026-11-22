"""Métricas de producción del informe: p95, tasas y coste por consulta.

Se comprueban con el ejemplo real versionado (`resultados/ejemplo-real`), que trae costes
medidos por OpenRouter, y con una ejecución doble, que no tiene coste.
"""

import pytest

from evaluacion import conjuntos
from evaluacion.informe import cargar_ejecucion, construir_informe, tabla_markdown
from evaluacion.metricas import percentil
from rag.config import RAIZ
from tests.test_evaluacion import _ejecutar, _informe

REAL = RAIZ / "resultados" / "ejemplo-real" / "test-A"


def test_percentil_por_rango_mas_cercano():
    latencias = [100.0 * i for i in range(1, 21)]  # 100 … 2000 ms, 20 consultas
    assert percentil(latencias, 95) == 1900.0  # la 19.ª: siempre una latencia medida
    assert percentil(latencias, 50) == 1000.0
    assert percentil([None, float("nan"), 300.0], 95) == 300.0
    assert percentil([], 95) is None


def test_los_rechazos_del_modelo_tambien_cuestan_y_el_rechazo_previo_no():
    respuestas, puntuaciones, manifiesto = cargar_ejecucion(REAL)
    inf = construir_informe(conjuntos.cargar("test"), respuestas, puntuaciones, manifiesto)
    con_modelo = [f for f in respuestas if f["motivo_rechazo"] != "evidencia_insuficiente"]
    solo_respondidas = [f for f in respuestas if not f["rechazo"]]
    esperado = round(sum(f["coste_usd"] for f in con_modelo), 8)
    assert inf["operacion"]["sistema"]["coste_usd_estimado"] == esperado
    assert esperado > sum(f["coste_usd"] for f in solo_respondidas)  # «No consta» del modelo se paga
    pr = inf["operacion"]["produccion"]
    assert pr["llamadas_al_modelo"] == len(con_modelo)
    assert pr["rechazos_sin_llamar_al_modelo"] + pr["llamadas_al_modelo"] == pr["consultas"] == 20


def test_coste_por_consulta_incluye_embeddings_y_se_reparte_entre_todas(tmp_path):
    respuestas, puntuaciones, manifiesto = cargar_ejecucion(REAL)
    inf = construir_informe(conjuntos.cargar("test"), respuestas, puntuaciones, manifiesto)
    pr, o = inf["operacion"]["produccion"], inf["operacion"]
    total = o["sistema"]["coste_usd_estimado"] + manifiesto["coste_embeddings_usd"]
    assert pr["coste_usd_por_consulta"] == pytest.approx(total / 20, abs=1e-8)  # redondeo a 8 decimales
    assert pr["coste_usd_por_1000_consultas"] == pytest.approx(total / 20 * 1000, abs=1e-4)
    juez = o["evaluador"]["coste_usd_estimado"]
    assert pr["peso_del_juez"] == pytest.approx(juez / (juez + total), abs=1e-4)
    assert pr["latencia_ms_p95"] >= pr["latencia_ms_p50"]
    assert "| Producción | latencia p95 |" in tabla_markdown(inf)


def test_en_el_perfil_doble_no_se_inventa_coste(tmp_path):
    inf = _informe(_ejecutar(tmp_path, "test", "doble-A"))
    pr = inf["operacion"]["produccion"]
    assert pr["coste_usd_por_consulta"] is None and pr["peso_del_juez"] is None
    assert pr["tasa_error"] == 0.0 and pr["consultas"] == 20
    assert pr["rechazos_sin_llamar_al_modelo"] + pr["llamadas_al_modelo"] == 20
    assert "1.000 consultas ≈ sin dato" in tabla_markdown(inf)
