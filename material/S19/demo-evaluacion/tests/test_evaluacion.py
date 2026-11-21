"""Conjuntos, contrato JSONL, informe, control de regresión y comparación A/B."""

import json
from pathlib import Path

import pytest

import s19
from evaluacion import comparar, conjuntos, regresion
from evaluacion.degradar import degradar
from evaluacion.informe import cargar_ejecucion, construir_informe
from evaluacion.intercambio import PUNTUACIONES, RESPUESTAS, ErrorFormato, escribir_jsonl, leer_jsonl
from evaluacion.lote import ejecutar_lote
from rag.almacen import AlmacenMemoria
from rag.ingesta import reconstruir_indice
from rag.proveedores import EmbeddingsDoble, GeneradorDoble, Proveedores
from tests.conftest import config

EVALUADOR = {"modo": "simulado", "ragas": "0.4.3", "llm": "simulado"}


def _puntuar(filas, run_id, valor=0.9):
    """Puntuaciones SIMULADAS con el formato del evaluador (aquí no se ejecuta Ragas)."""
    salida = []
    for f in filas:
        for metrica in ("faithfulness", "answer_relevancy"):
            motivo = "rechazo_sin_respuesta" if f["rechazo"] else None
            salida.append(
                {
                    "run_id": run_id,
                    "caso_id": f["caso_id"],
                    "metrica": metrica,
                    "valor": None if motivo else valor,
                    "evaluable": motivo is None,
                    "motivo": motivo,
                    "evaluador": EVALUADOR,
                    "consumo": {
                        "llamadas_llm": 0 if motivo else 2,
                        "tokens_entrada": None,
                        "tokens_salida": None,
                        "coste_usd": None,
                        "segundos": 0.0,
                    },
                }
            )
    return salida


def _ejecutar(tmp_path, conjunto, nombre, **cambios):
    cfg = config(**cambios)
    almacen, prov = AlmacenMemoria(), Proveedores(EmbeddingsDoble(), GeneradorDoble())
    indice = reconstruir_indice(cfg, almacen, prov.embeddings)
    carpeta = tmp_path / nombre
    casos = conjuntos.cargar(conjunto)
    filas = ejecutar_lote(cfg, almacen, prov, indice.indice_id, casos, conjunto, carpeta, run_id=nombre)
    escribir_jsonl(carpeta / "puntuaciones.jsonl", _puntuar(filas, nombre), PUNTUACIONES)
    return carpeta


def _informe(carpeta):
    respuestas, puntuaciones, manifiesto = cargar_ejecucion(carpeta)
    return construir_informe(conjuntos.cargar(manifiesto["conjunto"]), respuestas, puntuaciones, manifiesto)


@pytest.fixture(scope="module")
def ejecuciones(tmp_path_factory):
    raiz = tmp_path_factory.mktemp("ejecuciones")
    validacion = _ejecutar(raiz, "validacion", "val-A")
    test = _ejecutar(raiz, "test", "test-A")
    return {
        "raiz": raiz,
        "validacion": validacion,
        "test": test,
        "umbrales": regresion.derivar_umbrales(_informe(validacion)),
    }


# ------------------------------------------------------------ conjuntos y contrato
def test_el_test_tiene_14_respondibles_y_6_sin_respuesta():
    casos = conjuntos.cargar("test")
    assert (sum(c["respondible"] for c in casos), sum(not c["respondible"] for c in casos)) == (14, 6)
    assert all(c["respuesta_referencia"] for c in casos if c["respondible"])


def test_test_y_validacion_son_disjuntos_y_no_estan_indexados():
    assert conjuntos.comprobar_separacion()["test"] == 20


def test_un_archivo_de_otra_version_no_se_lee(tmp_path):
    (tmp_path / "r.jsonl").write_text(json.dumps({"schema_version": "s19.respuestas.v0"}) + "\n")
    with pytest.raises(ErrorFormato, match="se esperaba s19.respuestas.v1"):
        leer_jsonl(tmp_path / "r.jsonl", RESPUESTAS)


def test_una_puntuacion_no_evaluable_no_puede_llevar_valor(tmp_path):
    fila = {
        "run_id": "r",
        "caso_id": "T01",
        "metrica": "faithfulness",
        "valor": 1.0,
        "evaluable": False,
        "motivo": "nan",
        "evaluador": {},
        "consumo": {},
    }
    with pytest.raises(ErrorFormato, match="no lleva valor"):
        escribir_jsonl(tmp_path / "p.jsonl", [fila], PUNTUACIONES)
    with pytest.raises(ErrorFormato, match="motivo desconocido"):
        escribir_jsonl(tmp_path / "p.jsonl", [{**fila, "valor": None, "motivo": "porque sí"}], PUNTUACIONES)


# ------------------------------------------------------------ informe
def test_el_informe_separa_recuperacion_rechazo_y_generacion(ejecuciones):
    inf = _informe(ejecuciones["test"])
    assert inf["n_casos"] == 20 and inf["recuperacion"]["de_respondibles"] == 14
    assert inf["rechazo"]["de_sin_respuesta"] == 6
    assert 0 <= inf["recuperacion"]["precision_at_5"] <= inf["recuperacion"]["precision_techo"]
    g = inf["generacion"]["faithfulness"]
    assert g["n_esperados"] == inf["n_respondidas"] and g["cobertura"] == 1.0
    assert inf["operacion"]["evaluador"]["coste_usd_estimado"] is None  # desconocido, no 0
    assert "NO miden" in inf["aviso"]


def test_los_no_evaluables_restan_cobertura_y_no_entran_en_la_media(ejecuciones, tmp_path):
    respuestas, puntuaciones, manifiesto = cargar_ejecucion(ejecuciones["test"])
    juzgadas = [p for p in puntuaciones if p["evaluable"] and p["metrica"] == "faithfulness"]
    juzgadas[0].update(valor=None, evaluable=False, motivo="nan")
    juzgadas[1].update(valor=None, evaluable=False, motivo="error_evaluador:TimeoutError")
    inf = construir_informe(conjuntos.cargar("test"), respuestas, puntuaciones, manifiesto)
    g = inf["generacion"]["faithfulness"]
    assert g["n_evaluables"] == g["n_esperados"] - 2 and g["cobertura"] < 1.0
    assert g["media"] == 0.9  # la media no baja ni sube por los no evaluables: baja la cobertura
    assert {n["motivo"] for n in inf["generacion"]["no_evaluables"]} == {"nan", "error_evaluador:TimeoutError"}


def test_una_respuesta_sin_puntuacion_cuenta_como_fallo_del_evaluador(ejecuciones):
    respuestas, puntuaciones, manifiesto = cargar_ejecucion(ejecuciones["test"])
    victima = next(p["caso_id"] for p in puntuaciones if p["evaluable"])
    resto = [p for p in puntuaciones if p["caso_id"] != victima]
    inf = construir_informe(conjuntos.cargar("test"), respuestas, resto, manifiesto)
    assert {"caso_id": victima, "metrica": "faithfulness", "motivo": "error_evaluador:sin_puntuacion"} in inf["generacion"][
        "no_evaluables"
    ]


# ------------------------------------------------------------ control de regresión
def test_los_umbrales_salen_de_validacion_con_margen(ejecuciones):
    u = ejecuciones["umbrales"]
    assert u["origen"]["conjunto"] == "validacion" and u["margen"] == 0.10
    recall = next(r for r in u["reglas"] if r["metrica"] == "recuperacion.recall_at_5")
    assert recall["minimo"] == pytest.approx(recall["validacion"] - 0.10, abs=0.011)
    with pytest.raises(ValueError, match="nunca con el test"):
        regresion.derivar_umbrales(_informe(ejecuciones["test"]))


def test_el_control_pasa_con_una_ejecucion_equivalente_a_la_de_referencia(ejecuciones):
    """El control se pasa sobre VALIDACIÓN: el test se reserva para la medición final."""
    repeticion = _ejecutar(ejecuciones["raiz"], "validacion", "val-A-repetida")
    assert regresion.comprobar(_informe(repeticion), ejecuciones["umbrales"], 8) == []


@pytest.mark.parametrize(
    "modo, regla_que_debe_saltar",
    [
        ("recuperacion", "recuperacion.recall_at_5"),
        ("sin-rechazo", "rechazo.tasa_rechazos_correctos"),
        ("juez-caido", "generacion.faithfulness.cobertura"),
    ],
)
def test_el_control_FALLA_con_resultados_degradados(ejecuciones, modo, regla_que_debe_saltar):
    mala = ejecuciones["raiz"] / f"mala-{modo}"
    manifiesto = degradar(ejecuciones["validacion"], mala, modo)
    assert "DEGRADADO A PROPÓSITO" in manifiesto["aviso"]
    fallos = regresion.comprobar(_informe(mala), ejecuciones["umbrales"], 8)
    assert any(f.startswith(regla_que_debe_saltar) for f in fallos), fallos


def test_un_conjunto_incompleto_no_se_informa(ejecuciones):
    mala = ejecuciones["raiz"] / "mala-incompleto"
    degradar(ejecuciones["validacion"], mala, "incompleto")
    with pytest.raises(ValueError, match="test parcial"):
        _informe(mala)


def test_sin_dato_no_aprueba(ejecuciones):
    inf = _informe(ejecuciones["validacion"])
    inf["generacion"] = None  # no se ejecutó el evaluador
    fallos = regresion.comprobar(inf, ejecuciones["umbrales"], 8)
    assert any("sin dato" in f for f in fallos)


def test_umbrales_de_otro_perfil_y_errores_del_sistema_hacen_fallar(ejecuciones):
    inf, u = _informe(ejecuciones["validacion"]), ejecuciones["umbrales"]
    assert any("perfil" in f for f in regresion.comprobar({**inf, "perfil": "real"}, u, 8))
    assert any("error del sistema" in f for f in regresion.comprobar({**inf, "n_errores_sistema": 1}, u, 8))
    assert any("se esperaban" in f for f in regresion.comprobar(inf, u, 9))


# ------------------------------------------------------------ comparación A/B
def test_comparar_exige_una_sola_variable(ejecuciones):
    a = _informe(ejecuciones["test"])
    b = _informe(_ejecutar(ejecuciones["raiz"], "test", "test-B", chunk_size=900, config_id="B"))
    c = comparar.comparar(a, b)
    assert (c["variable"], c["valor_A"], c["valor_B"]) == ("chunk_size", 320, 900)
    assert "| precision@5 |" in comparar.tabla_markdown(c)
    dos = _informe(_ejecutar(ejecuciones["raiz"], "test", "test-C", chunk_size=900, k_contexto=2, config_id="C"))
    with pytest.raises(comparar.ComparacionInvalida, match="exactamente una variable"):
        comparar.comparar(a, dos)
    with pytest.raises(comparar.ComparacionInvalida, match="exactamente una variable"):
        comparar.comparar(a, a)


def test_no_se_comparan_conjuntos_ni_evaluadores_distintos(ejecuciones):
    a, v = _informe(ejecuciones["test"]), _informe(ejecuciones["validacion"])
    with pytest.raises(comparar.ComparacionInvalida, match="conjunto"):
        comparar.comparar(a, v)
    otro = json.loads(json.dumps(a))
    otro["config"]["chunk_size"] = 900
    otro["generacion"]["evaluador"] = {**EVALUADOR, "llm": "otro-juez"}
    with pytest.raises(comparar.ComparacionInvalida, match="mismo evaluador"):
        comparar.comparar(a, otro)


# ------------------------------------------------------------ compatibilidad y protección --fijar
def test_leer_respuestas_v1_sin_model_version_conserva_compatibilidad():
    ejemplo = Path(__file__).resolve().parent.parent / "resultados" / "ejemplo-doble" / "test-A" / "respuestas.jsonl"
    filas = leer_jsonl(ejemplo, RESPUESTAS)
    assert len(filas) == 20 and "model_version" not in filas[0]


def test_calibrar_no_sobrescribe_sin_fijar_y_escribe_si_falta_o_con_fijar(tmp_path, monkeypatch, capsys):
    cfg = config()
    almacen, prov = AlmacenMemoria(), Proveedores(EmbeddingsDoble(), GeneradorDoble())
    reconstruir_indice(cfg, almacen, prov.embeddings)
    monkeypatch.setattr(s19, "DATOS", tmp_path)
    monkeypatch.setattr(s19, "AlmacenPg", lambda _url: almacen)
    monkeypatch.setattr(s19, "crear_proveedores", lambda _cfg, _ex: prov)
    monkeypatch.delenv("S19_PERFIL", raising=False)
    ruta = tmp_path / "calibracion.json"

    # 1) Si no existe todavía la entrada del perfil, escribe como siempre.
    assert s19.main(["calibrar", "--config", "A"]) == 0
    primera = json.loads(ruta.read_text(encoding="utf-8"))
    assert primera["doble"]["umbral_evidencia"] == pytest.approx(0.2787)
    capsys.readouterr()

    # 2) Si ya existe la entrada del perfil, muestra calculado y fijado, pero NO escribe.
    primera["doble"]["umbral_evidencia"] = 0.1111
    primera["doble"]["fijado"] = "2026-11-17"
    primera["real"] = {"umbral_evidencia": 0.5, "fijado": "2026-11-17"}
    ruta.write_text(json.dumps(primera, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert s19.main(["calibrar", "--config", "A"]) == 0
    salida = capsys.readouterr().out
    assert "0.2787" in salida and "0.1111" in salida and "--fijar" in salida and "Sin cambios" in salida
    tras_consulta = json.loads(ruta.read_text(encoding="utf-8"))
    assert tras_consulta["doble"]["umbral_evidencia"] == 0.1111
    assert tras_consulta["doble"]["fijado"] == "2026-11-17"

    # 3) Con --fijar sobrescribe el perfil actual y conserva los demás perfiles.
    assert s19.main(["calibrar", "--config", "A", "--fijar"]) == 0
    tras_fijar = json.loads(ruta.read_text(encoding="utf-8"))
    assert tras_fijar["doble"]["umbral_evidencia"] == pytest.approx(0.2787)
    assert tras_fijar["real"]["umbral_evidencia"] == 0.5


def test_umbrales_no_sobrescribe_sin_fijar_y_escribe_si_falta_o_con_fijar(ejecuciones, tmp_path, monkeypatch, capsys):
    carpeta_val = tmp_path / "val"
    carpeta_val.mkdir()
    inf = _informe(ejecuciones["validacion"])
    (carpeta_val / "informe.json").write_text(json.dumps(inf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    datos_dir = tmp_path / "datos"
    monkeypatch.setattr(s19, "DATOS", datos_dir)
    ruta = datos_dir / "umbrales.doble.json"

    # 1) Si no existe todavía el archivo del perfil, escribe como siempre.
    assert s19.main(["umbrales", str(carpeta_val)]) == 0
    assert ruta.exists()
    primero = json.loads(ruta.read_text(encoding="utf-8"))
    capsys.readouterr()

    # 2) Si ya existe, muestra el valor calculado junto al fijado y NO sobrescribe.
    primero["fijado"] = "2026-11-17"
    for r in primero["reglas"]:
        if r["metrica"] == "recuperacion.recall_at_5":
            r["minimo"] = 0.85
    ruta.write_text(json.dumps(primero, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert s19.main(["umbrales", str(carpeta_val)]) == 0
    salida = capsys.readouterr().out
    assert "fijado 0.85" in salida and "0.90" in salida and "--fijar" in salida and "Sin cambios" in salida
    tras_consulta = json.loads(ruta.read_text(encoding="utf-8"))
    recall = next(r for r in tras_consulta["reglas"] if r["metrica"] == "recuperacion.recall_at_5")
    assert recall["minimo"] == 0.85 and tras_consulta["fijado"] == "2026-11-17"

    # 3) Con --fijar sobrescribe el archivo.
    assert s19.main(["umbrales", str(carpeta_val), "--fijar"]) == 0
    tras_fijar = json.loads(ruta.read_text(encoding="utf-8"))
    recall_nuevo = next(r for r in tras_fijar["reglas"] if r["metrica"] == "recuperacion.recall_at_5")
    assert recall_nuevo["minimo"] == 0.90
