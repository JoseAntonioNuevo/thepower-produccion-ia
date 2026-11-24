"""Langfuse: qué se registra y que el consumo del evaluador va en una traza aparte.

Sin red: se usa un cliente falso que anota las llamadas y un exportador en memoria
para comprobar los atributos que conserva el SDK real de Langfuse.
"""

import json
from contextlib import contextmanager

import pytest

from rag.config import ErrorConfiguracion
from rag.consulta import responder
from rag.observabilidad import Trazador
from rag.proveedores import Proveedores
from tests.conftest import GeneradorSimulado, config

PREGUNTA = "¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?"
EVALUADOR = {"modo": "real", "ragas": "0.4.3", "llm": "anthropic/claude-haiku-5.5"}


class _Obs:
    def __init__(self, registro, campos):
        self.registro, self.campos = registro, campos

    def update(self, **campos):
        self.campos.update({k: v for k, v in campos.items() if v is not None})

    @contextmanager
    def start_as_current_observation(self, **campos):
        """Observación hija: se anota con el nombre de su madre para comprobar la jerarquía."""
        hija = {**campos, "_madre": self.campos.get("name")}
        self.registro.observaciones.append(hija)
        yield _Obs(self.registro, hija)


class ClienteFalso:
    def __init__(self):
        self.observaciones, self.puntuaciones, self.vaciados = [], [], 0

    @contextmanager
    def start_as_current_observation(self, **campos):
        self.observaciones.append(campos)
        yield _Obs(self, campos)

    def create_score(self, **campos):
        self.puntuaciones.append(campos)

    def flush(self):
        self.vaciados += 1


def _puntuacion(metrica, valor, motivo=None, tokens=(1000, 200), coste_usd=0.0015):
    return {
        "metrica": metrica,
        "valor": valor,
        "evaluable": motivo is None,
        "motivo": motivo,
        "evaluador": EVALUADOR,
        "consumo": {"llamadas_llm": 2, "tokens_entrada": tokens[0], "tokens_salida": tokens[1], "coste_usd": coste_usd},
    }


def test_apagado_por_defecto_y_sin_claves_no_arranca(monkeypatch):
    monkeypatch.delenv("S19_LANGFUSE", raising=False)
    assert Trazador.desde_entorno().activo is False
    monkeypatch.setenv("S19_LANGFUSE", "on")
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    with pytest.raises(ErrorConfiguracion, match="LANGFUSE_PUBLIC_KEY"):
        Trazador.desde_entorno()


def test_una_consulta_deja_recuperacion_generacion_y_puntuaciones(cfg, sistema):
    almacen, prov, indice_id = sistema
    cliente = ClienteFalso()
    with Trazador(cliente).consulta("run-1", "T01", cfg, PREGUNTA) as traza:
        r = responder(cfg, almacen, prov, indice_id, PREGUNTA, traza)
        traza.cerrar(
            salida={"respuesta": r.texto, "fuentes": r.fuentes},
            metadatos={"latencia_ms": r.latencia_ms, "coste_usd_estimado": r.coste_usd},
            puntuaciones={"precision_at_5": 0.2, "recall_at_5": 1.0, "acierto_criterio": None},
        )
    nombres = [(o["name"], o["as_type"]) for o in cliente.observaciones]
    assert nombres == [("consulta-rag", "span"), ("recuperacion", "retriever"), ("generacion", "generation")]
    # Cada paso del grafo cuelga de la raíz de la consulta, aunque LangGraph lo ejecute en otro hilo.
    assert [o.get("_madre") for o in cliente.observaciones[1:]] == ["consulta-rag", "consulta-rag"]
    raiz, _, generacion = cliente.observaciones
    assert raiz["output"]["fuentes"] == r.fuentes and "latencia_ms" in raiz["metadata"]
    assert generacion["model"] == cfg.gen_modelo
    assert "usage_details" not in generacion  # el doble no informa tokens: no se envían inventados
    assert "cost_details" not in generacion  # sin tokens ni tarifa: no se envía coste (nunca 0)
    assert "metadata" not in generacion  # el doble no tiene model_version
    # Una métrica sin valor no se publica como 0.
    assert [p["name"] for p in cliente.puntuaciones] == ["precision_at_5", "recall_at_5"]
    assert len({p["trace_id"] for p in cliente.puntuaciones}) == 1


def test_generacion_envia_cost_details_y_model_version_cuando_se_conocen(sistema):
    almacen, prov, indice_id = sistema
    cliente = ClienteFalso()
    cfg_real = config(gen_modelo="google/gemini-3.5-flash-lite")
    gen = GeneradorSimulado(
        "TLS 1.3 [01-arquitectura-aethercloud]", tokens=(1000, 200), model_version="google/gemini-3.5-flash-lite-001"
    )
    with Trazador(cliente).consulta("run-2", "T01", cfg_real, PREGUNTA) as traza:
        responder(cfg_real, almacen, Proveedores(prov.embeddings, gen), indice_id, PREGUNTA, traza)
    generacion = cliente.observaciones[2]
    assert generacion["usage_details"] == {"input": 1000, "output": 200}
    assert generacion["cost_details"] == {"input": 0.0003, "output": 0.0005, "total": 0.0008}
    assert generacion["metadata"] == {"model_version": "google/gemini-3.5-flash-lite-001"}


def test_generacion_sin_tarifa_no_envia_cost_details(sistema):
    almacen, prov, indice_id = sistema
    cliente = ClienteFalso()
    cfg_sin = config(gen_modelo="modelo-sin-precio")
    gen = GeneradorSimulado("TLS 1.3 [01-arquitectura-aethercloud]", tokens=(1000, 200))
    with Trazador(cliente).consulta("run-3", "T01", cfg_sin, PREGUNTA) as traza:
        responder(cfg_sin, almacen, Proveedores(prov.embeddings, gen), indice_id, PREGUNTA, traza)
    generacion = cliente.observaciones[2]
    assert generacion["usage_details"] == {"input": 1000, "output": 200}
    assert "cost_details" not in generacion


def test_el_consumo_del_evaluador_va_en_otra_traza(cfg):
    cliente, trazador = ClienteFalso(), Trazador(ClienteFalso())
    trazador._cliente = cliente
    filas = [
        _puntuacion("faithfulness", 0.75, coste_usd=0.0015),
        _puntuacion("answer_relevancy", None, "nan", coste_usd=0.002),
    ]
    trazador.registrar_evaluador("run-1", "T01", cfg, filas)
    traza_consulta = trazador.id_traza("run-1", "T01")
    # La nota evaluable se cuelga de la traza de la CONSULTA; la no evaluable no se publica.
    assert [(p["name"], p["value"], p["trace_id"]) for p in cliente.puntuaciones] == [("faithfulness", 0.75, traza_consulta)]
    assert cliente.puntuaciones[0]["score_id"] == trazador.id_traza("run-1", "T01", ":ragas:faithfulness")
    (obs,) = cliente.observaciones
    assert (obs["name"], obs["as_type"], obs["model"]) == ("consumo-juez", "generation", EVALUADOR["llm"])
    assert obs["trace_context"]["trace_id"] == trazador.id_traza("run-1", "T01", ":evaluador")
    assert obs["usage_details"] == {"input": 2000, "output": 400}
    assert obs["cost_details"] == {"total": 0.0035}
    assert obs["output"] == {"faithfulness": 0.75, "answer_relevancy": "nan"}


def test_tokens_y_coste_desconocidos_del_evaluador_no_se_envian_como_cero(cfg):
    cliente, trazador = ClienteFalso(), Trazador(None)
    trazador._cliente = cliente
    trazador.registrar_evaluador(
        "run-1",
        "T01",
        cfg,
        [_puntuacion("faithfulness", 1.0, tokens=(None, None), coste_usd=None)],
    )
    assert cliente.observaciones[0]["usage_details"] is None
    assert cliente.observaciones[0]["cost_details"] is None
    # Si falta coste en una sola fila del caso, tampoco se envía coste parcial.
    trazador.registrar_evaluador(
        "run-1",
        "T02",
        cfg,
        [_puntuacion("faithfulness", 1.0, coste_usd=0.0015), _puntuacion("answer_relevancy", 0.8, coste_usd=None)],
    )
    assert cliente.observaciones[1]["cost_details"] is None


def test_republicar_solo_consumo_omite_las_puntuaciones_y_los_rechazos(cfg):
    cliente = ClienteFalso()
    trazador = Trazador(cliente)
    rechazo = _puntuacion("faithfulness", None, "rechazo_sin_respuesta", tokens=(0, 0), coste_usd=0.0)
    rechazo["consumo"]["llamadas_llm"] = 0

    trazador.registrar_evaluador("run-1", "T01", cfg, [rechazo])
    trazador.registrar_evaluador("run-1", "T01", cfg, [rechazo], solo_consumo=True)
    trazador.registrar_evaluador("run-1", "T02", cfg, [_puntuacion("faithfulness", 1.0)], solo_consumo=True)

    assert not cliente.puntuaciones
    rechazo_obs, consumo_obs = cliente.observaciones
    assert rechazo_obs["as_type"] == "evaluator"
    assert "model" not in rechazo_obs
    assert consumo_obs["as_type"] == "generation"
    assert consumo_obs["trace_context"]["trace_id"] == trazador.id_traza("run-1", "T02", ":evaluador")


def test_el_sdk_real_exporta_los_campos_de_consumo_del_juez(sistema, monkeypatch):
    """El SDK acepta los parámetros aunque descarte algunos según el tipo de observación."""
    from langfuse import Langfuse
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

    almacen, prov, indice_id = sistema
    cfg = config(gen_modelo="google/gemini-3.5-flash-lite")
    gen = GeneradorSimulado(
        "TLS 1.3 [01-arquitectura-aethercloud]", tokens=(1000, 200), model_version="google/gemini-3.5-flash-lite-001"
    )
    exportador = InMemorySpanExporter()
    cliente = Langfuse(public_key="pk-lf-prueba", secret_key="sk-lf-prueba", span_exporter=exportador)
    monkeypatch.setattr(cliente, "create_score", lambda **_: None)
    trazador = Trazador(cliente)
    with trazador.consulta("run-sdk", "T01", cfg, PREGUNTA) as traza:
        r = responder(cfg, almacen, Proveedores(prov.embeddings, gen), indice_id, PREGUNTA, traza)
        traza.cerrar(salida={"respuesta": r.texto}, metadatos={}, puntuaciones={"recall_at_5": 1.0})
    trazador.registrar_evaluador("run-sdk", "T01", cfg, [_puntuacion("faithfulness", 0.5, coste_usd=0.0015)])
    trazador.cerrar()
    (juez,) = [span for span in exportador.get_finished_spans() if span.name == "consumo-juez"]
    assert juez.attributes["langfuse.observation.type"] == "generation"
    assert juez.attributes["langfuse.observation.model.name"] == EVALUADOR["llm"]
    assert json.loads(juez.attributes["langfuse.observation.usage_details"]) == {"input": 1000, "output": 200}
    assert json.loads(juez.attributes["langfuse.observation.cost_details"]) == {"total": 0.0015}
    assert len(trazador.id_traza("run-sdk", "T01")) == 32
    assert trazador.id_traza("run-sdk", "T01") == trazador.id_traza("run-sdk", "T01")
