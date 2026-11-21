"""Deep Research acotado: trabajos idempotentes, límites e informe parcial."""

import dataclasses

from agente.investigacion import buscar_fuentes, investigar, procesar_pendientes

TEMA = "HTTP 429 Too Many Requests y cabecera Retry-After"


def test_pedir_dos_veces_lo_mismo_devuelve_el_mismo_trabajo(servicios):
    a = servicios.almacen.crear_trabajo("hilo-1", "ana", TEMA)
    b = servicios.almacen.crear_trabajo(
        "hilo-1", "ana", "  http 429 too many requests y cabecera retry-after "
    )
    otro_hilo = servicios.almacen.crear_trabajo("hilo-2", "ana", TEMA)
    assert a["nuevo"] is True and b["nuevo"] is False and a["trabajo_id"] == b["trabajo_id"]
    assert otro_hilo["trabajo_id"] != a["trabajo_id"]


def test_informe_completo_separa_politica_interna_e_informacion_publica(servicios):
    informe = investigar(TEMA, servicios.cfg, servicios.almacen, servicios.embeddings)
    assert informe["estado"] == "completo" and informe["faltan"] == []
    assert {e["fuente_id"] for e in informe["informacion_publica"]} == {
        "rfc6585-429",
        "rfc9110-retry-after",
    }
    assert informe["politica_interna"][0]["cita"].startswith("03-limites-y-cuotas-api")
    assert informe["consumo"]["llamadas_modelo"] == 0 and informe["consumo"]["tokens"] is None


def test_informe_parcial_cuando_falta_evidencia(servicios):
    informe = investigar(
        "computación cuántica y cabecera Retry-After",
        servicios.cfg,
        servicios.almacen,
        servicios.embeddings,
    )
    assert informe["estado"] == "parcial"
    assert informe["faltan"] == ["computación cuántica"]
    assert "Sin evidencia para: computación cuántica" in informe["resumen"]


def test_el_limite_de_fuentes_se_respeta(servicios):
    cfg = dataclasses.replace(servicios.cfg, max_fuentes=1)
    informe = investigar(TEMA, cfg, servicios.almacen, servicios.embeddings)
    assert informe["consumo"]["fuentes_leidas"] == 1


def test_un_tema_ajeno_no_encuentra_fuentes_en_la_lista_blanca():
    assert buscar_fuentes("receta de tortilla de patatas") == []


def test_el_ejecutor_procesa_cada_trabajo_una_sola_vez(servicios):
    trabajo = servicios.almacen.crear_trabajo("hilo-1", "ana", TEMA)
    primera = procesar_pendientes(servicios.cfg, servicios.almacen, servicios.embeddings)
    segunda = procesar_pendientes(servicios.cfg, servicios.almacen, servicios.embeddings)
    assert primera == [trabajo["trabajo_id"]] and segunda == []
    assert servicios.almacen.leer_trabajo(trabajo["trabajo_id"])["estado"] == "completo"


def test_el_agente_registra_el_trabajo_y_luego_devuelve_el_informe(servicios):
    pregunta = "Mira el ticket T-100 e investiga la tecnología implicada"
    antes = servicios.conversar(usuario="ana", thread_id="h", mensaje=pregunta)
    procesar_pendientes(servicios.cfg, servicios.almacen, servicios.embeddings)
    despues = servicios.conversar(usuario="ana", thread_id="h", mensaje=pregunta)
    assert "estado: pendiente" in antes["respuesta"]
    assert "web:rfc6585-429" in despues["fuentes"]
    # Repetir la pregunta no ha creado un segundo trabajo.
    assert procesar_pendientes(servicios.cfg, servicios.almacen, servicios.embeddings) == []


def test_en_el_perfil_real_el_modelo_redacta_con_las_evidencias_y_se_cuentan_sus_tokens(con_cfg):
    from langchain_core.messages import AIMessage

    from agente.servicios import crear_redactor

    class ModeloSimulado:  # no es un modelo: devuelve un texto fijo y unos tokens de ejemplo
        def invoke(self, mensajes, config=None):
            assert "informacion_publica" in mensajes[-1].content  # recibe evidencias, no la web
            return AIMessage(
                content="Informe redactado.",
                usage_metadata={"input_tokens": 300, "output_tokens": 40, "total_tokens": 340},
            )

    s = con_cfg()
    redactor = crear_redactor(dataclasses.replace(s.cfg, perfil="real"), ModeloSimulado())
    informe = investigar(TEMA, s.cfg, s.almacen, s.embeddings, redactor)
    assert informe["resumen"] == "Informe redactado."
    assert informe["consumo"]["llamadas_modelo"] == 1
    assert informe["consumo"]["tokens"]["total_tokens"] == 340
    assert crear_redactor(s.cfg, ModeloSimulado()) is None  # en el perfil doble no hay redactor
