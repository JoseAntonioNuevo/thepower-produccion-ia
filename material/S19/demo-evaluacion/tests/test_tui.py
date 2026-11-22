"""El chat de la terminal sin terminal: órdenes, perfiles, filas del chat y trazas.

La parte visual (OpenTUI) solo pinta; aquí se prueba todo lo demás con el perfil doble,
un almacén en memoria y archivos de entorno temporales. Ningún test abre la pantalla.
"""

import os
from dataclasses import replace

import pytest

from rag import config as configuracion
from rag.almacen import AlmacenMemoria
from rag.ingesta import reconstruir_indice
from rag.observabilidad import Trazador
from rag.proveedores import EmbeddingsDoble
from tests.conftest import config
from tests.test_observabilidad import ClienteFalso
from ui.lineas import lineas_de_criterio, lineas_de_paso
from ui.motor import MotorChat
from ui.rag_tui import RagTUI

DOBLE = "S19_PERFIL=doble\nS19_LANGFUSE=off\n"


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    """Archivo de entorno propio del test; al terminar se deja os.environ como estaba."""
    copia = dict(os.environ)
    for clave in [k for k in os.environ if k.startswith(("S19_", "LANGFUSE_", "OPENROUTER_"))]:
        monkeypatch.delenv(clave)
    configuracion._CARGADAS.clear()
    (tmp_path / ".env.uno").write_text(DOBLE + "S19_K_CONTEXTO=3\n", encoding="utf-8")
    (tmp_path / ".env.dos").write_text(DOBLE + "S19_PROMPT_VERSION=v2\n", encoding="utf-8")
    (tmp_path / ".env.real").write_text("S19_PERFIL=real\nOPENROUTER_API_KEY=sk-falsa\n", encoding="utf-8")
    monkeypatch.setenv(configuracion.VARIABLE_ARCHIVO_ENV, str(tmp_path / ".env.uno"))
    yield tmp_path
    os.environ.clear()
    os.environ.update(copia)
    configuracion._CARGADAS.clear()


@pytest.fixture
def almacen():
    """Índices dobles A (320) y B (900) en memoria, como si se hubiera ejecutado `ingestar`."""
    a = AlmacenMemoria()
    for chunk in (320, 900):
        reconstruir_indice(config(chunk_size=chunk), a, EmbeddingsDoble())
    return a


def _motor(entorno, almacen, **opciones):
    return MotorChat(False, "A", fabrica_almacen=lambda _url: almacen, sesion="chat-test", carpeta_env=entorno, **opciones)


def test_ordenes_del_chat(entorno, almacen):
    m = _motor(entorno, almacen)
    assert m.interpretar("3").caso["caso_id"] == "T12"  # tercera pregunta del guion
    assert m.interpretar("t14").caso["caso_id"] == "T14"
    assert m.interpretar("/perfil dos").tipo == "perfil" and m.interpretar("/perfil dos").argumento == "dos"
    assert m.interpretar("salir").tipo == "salir"
    libre = m.interpretar("¿Qué es AetherCloud?")
    assert (libre.tipo, libre.caso, libre.pregunta) == ("pregunta", None, "¿Qué es AetherCloud?")
    assert m.interpretar("/inventado").tipo == "desconocido"


def test_cambiar_de_perfil_no_arrastra_valores_del_archivo_anterior(entorno, almacen):
    m = _motor(entorno, almacen)
    assert (m.perfil, m.cfg.k_contexto, m.cfg.prompt_version) == (".env.uno", 3, "v1")
    m.comando(m.interpretar("/perfil dos"))
    assert (m.perfil, m.cfg.k_contexto, m.cfg.prompt_version) == (".env.dos", 4, "v2")  # k_contexto vuelve al defecto


def test_un_perfil_imposible_no_cambia_nada(entorno, almacen):
    m = _motor(entorno, almacen)
    error = m.comando(m.interpretar("/perfil real"))  # perfil real sin --execute
    assert error[0].kind == "error" and "--execute" in error[0].text
    assert m.perfil == ".env.uno" and m.cfg.perfil == "doble"
    assert m.comando(m.interpretar("/perfil noexiste"))[0].kind == "error"


def test_cambiar_de_configuracion_usa_otro_indice(entorno, almacen):
    m = _motor(entorno, almacen)
    indice_a = m.indice_id
    m.comando(m.interpretar("/config B"))
    assert m.config_id == "B" and m.cfg.chunk_size == 900 and m.indice_id != indice_a


def test_cada_paso_del_grafo_se_convierte_en_filas(entorno, almacen):
    m = _motor(entorno, almacen)
    pasos = []
    r = m.preguntar(m.casos["T01"]["pregunta"], m.casos["T01"], pasos.append)
    filas = [f for p in pasos for f in lineas_de_paso(p, m.cfg.umbral_evidencia, m.cfg.gen_modelo)]
    assert [f.kind for f in filas] == ["paso", "dato", "paso", "paso", "bot"]
    assert "≥ umbral" in filas[0].text and filas[-1].text == r.texto


def test_la_rama_de_rechazo_previo_se_ve_en_el_chat(entorno, almacen):
    m = _motor(entorno, almacen)
    m.cfg = replace(m.cfg, umbral_evidencia=0.99)
    pasos = []
    m.preguntar("¿Cuál es el horario de la cafetería?", None, pasos.append)
    filas = [f for p in pasos for f in lineas_de_paso(p, 0.99, m.cfg.gen_modelo)]
    assert [f.kind for f in filas] == ["paso", "dato", "paso", "rechazo"]
    assert "no se llama al modelo" in filas[2].text


def test_el_criterio_se_muestra_con_su_referencia(entorno, almacen):
    m = _motor(entorno, almacen)
    caso = m.casos["T14"]
    r = m.preguntar(caso["pregunta"], caso, lambda _p: None)
    texto = lineas_de_criterio(caso, r)[0].text
    assert texto.startswith("T14 · ") and "referencia:" in texto


def test_cada_pregunta_del_chat_deja_una_traza_como_las_del_lote(entorno, almacen):
    m = _motor(entorno, almacen)
    cliente = ClienteFalso()
    m.trazador = Trazador(cliente)
    m.preguntar(m.casos["T01"]["pregunta"], m.casos["T01"], lambda _p: None)
    nombres = [o["name"] for o in cliente.observaciones]
    assert nombres == ["consulta-rag", "recuperacion", "generacion"]
    assert {p["name"] for p in cliente.puntuaciones} >= {"rechazo", "recall_at_5", "acierto_criterio"}
    assert cliente.vaciados >= 1  # se envía al terminar cada pregunta, no al cerrar el chat


def test_el_controlador_pinta_el_turno_completo_sin_pantalla(entorno, almacen):
    tui = RagTUI(_motor(entorno, almacen))
    tui.submit("1")  # T01, primera pregunta del guion
    tui._hilo.join(timeout=10)
    tui.cola.drain()
    tipos = [f.kind for f in tui.lines()]
    assert tipos[-8:] == ["human", "paso", "dato", "paso", "paso", "bot", "hint", "criterio"]
    assert tui.busy() is False and tui.grafo()["ruta"] == ["recuperar", "generar", "comprobar"]
    assert "sesión: 1 preguntas" in tui.ultimo()


def test_un_comando_no_lanza_el_grafo(entorno, almacen):
    tui = RagTUI(_motor(entorno, almacen))
    tui.submit("/casos")
    assert tui._hilo is None and "T20" in tui.lines()[-1].text
