"""Consulta con respuestas simuladas: formato, fuentes, rechazo y errores."""

import json

import pytest

from evaluacion.intercambio import RESPUESTAS, leer_jsonl
from evaluacion.lote import ejecutar_lote
from rag.consulta import MENSAJE_RECHAZO, extraer_fuentes, responder
from rag.costes import desglose_coste_usd
from rag.proveedores import NO_CONSTA, ErrorProveedor, Proveedores
from tests.conftest import GeneradorSimulado, config

PREGUNTA = "¿Qué crédito corresponde si la disponibilidad mensual es inferior al 99,00 %?"


def test_respuesta_con_fuentes_y_formato_completo(cfg, sistema):
    almacen, prov, indice_id = sistema
    r = responder(cfg, almacen, prov, indice_id, "¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?")
    assert not r.rechazo and "TLS 1.3" in r.texto
    assert r.fuentes[0] == "01-arquitectura-aethercloud"
    assert set(r.fuentes) <= {c["documento_id"] for c in r.contextos}  # solo cita lo que recibió
    assert 1 <= len(r.documentos_recuperados) <= 5
    assert len(r.documentos_recuperados) == len(set(r.documentos_recuperados))
    assert len(r.contextos) == cfg.k_contexto
    assert set(r.latencia_ms) == {"recuperacion", "generacion", "total"}
    assert r.coste_usd is None  # el doble no informa tokens: coste desconocido, no cero
    assert r.model_version is None  # el doble no devuelve versión servida por API


def test_sin_evidencia_se_rechaza_sin_llamar_al_generador(sistema):
    almacen, prov, indice_id = sistema
    generador = GeneradorSimulado("no debería ejecutarse")
    r = responder(config(umbral_evidencia=0.99), almacen, Proveedores(prov.embeddings, generador), indice_id, PREGUNTA)
    assert (r.rechazo, r.motivo_rechazo, r.texto) == (True, "evidencia_insuficiente", MENSAJE_RECHAZO)
    assert generador.llamadas == 0 and r.contextos == [] and r.coste_usd == 0.0


def test_el_generador_puede_declarar_que_no_consta(cfg, sistema):
    almacen, prov, indice_id = sistema
    r = responder(cfg, almacen, Proveedores(prov.embeddings, GeneradorSimulado(NO_CONSTA)), indice_id, PREGUNTA)
    assert (r.rechazo, r.motivo_rechazo, r.fuentes) == (True, "generador_sin_respuesta", [])


@pytest.mark.parametrize(
    "texto, avisos",
    [
        ("El crédito es del 25 %.", ["sin_fuentes"]),
        ("El crédito es del 25 % [99-documento-inventado]", ["sin_fuentes", "fuentes_fuera_del_contexto"]),
        ("", ["respuesta_vacia", "sin_fuentes"]),
    ],
)
def test_respuestas_mal_formadas_quedan_avisadas(cfg, sistema, texto, avisos):
    almacen, prov, indice_id = sistema
    r = responder(cfg, almacen, Proveedores(prov.embeddings, GeneradorSimulado(texto)), indice_id, PREGUNTA)
    assert r.avisos == avisos and r.fuentes == []


def test_citas_validas_e_inventadas_se_separan():
    validas, inventadas = extraer_fuentes("a [05-sla] b [99-falso] c [05-sla]", ["05-sla", "07-fact"])
    assert (validas, inventadas) == (["05-sla"], ["99-falso"])


def test_tokens_y_coste_estimado_con_tarifa(sistema):
    almacen, prov, indice_id = sistema
    generador = GeneradorSimulado("Es del 25 % [05-sla-y-creditos-servicio]", tokens=(1000, 200))
    r = responder(
        config(gen_modelo="google/gemini-3.5-flash-lite"),
        almacen,
        Proveedores(prov.embeddings, generador),
        indice_id,
        PREGUNTA,
    )
    assert r.tokens == {"entrada": 1000, "salida": 200}
    assert r.coste_usd == pytest.approx((1000 * 0.30 + 200 * 2.50) / 1e6)


def test_modelo_sin_tarifa_deja_el_coste_sin_dato(sistema):
    almacen, prov, indice_id = sistema
    generador = GeneradorSimulado("Es del 25 % [05-sla-y-creditos-servicio]", tokens=(1000, 200))
    r = responder(
        config(gen_modelo="modelo-sin-precio"), almacen, Proveedores(prov.embeddings, generador), indice_id, PREGUNTA
    )
    assert r.coste_usd is None


def test_el_error_del_proveedor_sube_y_no_se_sustituye(cfg, sistema):
    almacen, prov, indice_id = sistema
    roto = Proveedores(prov.embeddings, GeneradorSimulado(error=ErrorProveedor("generación: Timeout")))
    with pytest.raises(ErrorProveedor):
        responder(cfg, almacen, roto, indice_id, PREGUNTA)


def test_el_lote_conserva_el_caso_fallido_con_su_error(cfg, sistema, tmp_path):
    almacen, prov, indice_id = sistema
    roto = Proveedores(prov.embeddings, GeneradorSimulado(error=ErrorProveedor("generación: Timeout")))
    casos = [
        {
            "caso_id": "X1",
            "pregunta": PREGUNTA,
            "respondible": True,
            "documentos_relevantes": ["05-sla-y-creditos-servicio"],
            "datos_clave": ["25 %"],
        }
    ]
    filas = ejecutar_lote(cfg, almacen, roto, indice_id, casos, "test", tmp_path, run_id="r")
    assert filas[0]["response"] is None and filas[0]["error"].startswith("ErrorProveedor")
    assert filas[0]["model_version"] is None
    assert leer_jsonl(tmp_path / "respuestas.jsonl", RESPUESTAS)[0]["caso_id"] == "X1"


def test_desglose_coste_usd_con_tarifa_y_sin_ella():
    assert desglose_coste_usd("google/gemini-3.5-flash-lite", 1000, 200) == {
        "input": 0.0003,
        "output": 0.0005,
        "total": 0.0008,
    }
    assert desglose_coste_usd("modelo-sin-precio", 1000, 200) is None
    assert desglose_coste_usd("google/gemini-3.5-flash-lite", None, 200) is None
    assert desglose_coste_usd("google/gemini-3.5-flash-lite", 1000, None) is None


def test_model_version_proveedor_y_coste_llegan_a_respuesta_lote_y_manifiesto(sistema, tmp_path):
    almacen, prov, indice_id = sistema
    gen = GeneradorSimulado(
        "El crédito es del 25 % [05-sla-y-creditos-servicio].",
        tokens=(100, 50),
        model_version="google/gemini-3.5-flash-lite-001",
        coste_usd=0.000155,
        proveedor_servido="Google",
    )
    cfg_real = config(gen_modelo="google/gemini-3.5-flash-lite")
    casos = [
        {
            "caso_id": "X1",
            "pregunta": PREGUNTA,
            "respondible": True,
            "documentos_relevantes": ["05-sla-y-creditos-servicio"],
            "datos_clave": ["25 %"],
        }
    ]

    r = responder(cfg_real, almacen, Proveedores(prov.embeddings, gen), indice_id, PREGUNTA)
    assert r.model_version == "google/gemini-3.5-flash-lite-001"
    assert r.tokens == {"entrada": 100, "salida": 50}
    assert (r.coste_usd, r.coste_fuente, r.proveedor_servido) == (0.000155, "openrouter", "Google")

    carpeta_real = tmp_path / "lote-real"
    ejecutar_lote(cfg_real, almacen, Proveedores(prov.embeddings, gen), indice_id, casos, "test", carpeta_real, run_id="r1")
    fila_real = leer_jsonl(carpeta_real / "respuestas.jsonl", RESPUESTAS)[0]
    manifiesto_real = json.loads((carpeta_real / "manifiesto.json").read_text(encoding="utf-8"))
    assert fila_real["model_version"] == "google/gemini-3.5-flash-lite-001"
    assert fila_real["coste_fuente"] == "openrouter"
    assert manifiesto_real["versiones_modelo"] == ["google/gemini-3.5-flash-lite-001"]
    assert manifiesto_real["proveedores_servidos"] == ["Google"]

    carpeta_doble = tmp_path / "lote-doble"
    ejecutar_lote(config(), almacen, prov, indice_id, casos, "test", carpeta_doble, run_id="r2")
    fila_doble = leer_jsonl(carpeta_doble / "respuestas.jsonl", RESPUESTAS)[0]
    manifiesto_doble = json.loads((carpeta_doble / "manifiesto.json").read_text(encoding="utf-8"))
    assert fila_doble["model_version"] is None
    assert manifiesto_doble["versiones_modelo"] == [] and manifiesto_doble["proveedores_servidos"] == []
    assert manifiesto_doble["coste_embeddings_usd"] is None


def test_sin_coste_de_openrouter_se_estima_con_la_tarifa(sistema):
    almacen, prov, indice_id = sistema
    gen = GeneradorSimulado("Del 25 % [05-sla-y-creditos-servicio].", tokens=(1000, 200))
    r = responder(
        config(gen_modelo="google/gemini-3.5-flash-lite"), almacen, Proveedores(prov.embeddings, gen), indice_id, PREGUNTA
    )
    assert (r.coste_usd, r.coste_fuente) == (0.0008, "tarifa")
