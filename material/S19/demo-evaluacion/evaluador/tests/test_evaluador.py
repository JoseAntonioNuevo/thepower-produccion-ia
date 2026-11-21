"""Tests del evaluador aislado. Sin red y sin coste: el juez es un doble o HTTP simulado."""

import asyncio
import importlib.metadata as md
import inspect
import json
import os

import evaluar as ev
import httpx
import pytest
from ragas.metrics.collections import AnswerRelevancy, Faithfulness

FILA = {
    "run_id": "r1",
    "caso_id": "T01",
    "user_input": "¿Qué versión de TLS exigen las pasarelas?",
    "response": "Las pasarelas perimetrales exigen TLS 1.3 de forma obligatoria. [01-arquitectura-aethercloud]",
    "retrieved_contexts": ["Las pasarelas perimetrales exigen TLS 1.3 de forma obligatoria."],
    "rechazo": False,
    "error": None,
}
EVALUADOR = ev.descripcion_evaluador("doble", None, "doble-lexico", "doble-hash-256")


def _evaluar(filas, juez=None):
    juez = juez or ev.JuezDoble()
    return asyncio.run(ev.evaluar(filas, juez, ev.EmbeddingsDoble(), EVALUADOR, juez_doble=juez))


# ------------------------------------------------------------ la API que indica el enunciado
def test_versiones_fijadas_por_el_enunciado():
    assert md.version("ragas") == "0.4.3"
    assert md.version("langchain-community") == "0.3.31"


def test_firmas_de_ascore():
    assert list(inspect.signature(Faithfulness.ascore).parameters) == [
        "self",
        "user_input",
        "response",
        "retrieved_contexts",
    ]
    # Discrepancia documentada: AnswerRelevancy NO recibe retrieved_contexts.
    assert list(inspect.signature(AnswerRelevancy.ascore).parameters) == ["self", "user_input", "response"]
    assert {"llm", "embeddings"} <= set(inspect.signature(AnswerRelevancy.__init__).parameters)


def test_la_ruta_sincrona_de_la_guia_falla_en_ascore():
    """Con ragas 0.4.3, llm_factory(provider='google', client=genai.Client()) es síncrono."""
    from google import genai
    from ragas.llms import llm_factory

    llm = llm_factory("gemini-3.8-flash", provider="google", client=genai.Client(api_key="falsa"))
    assert llm.is_async is False
    with pytest.raises(TypeError, match="synchronous client"):  # falla antes de usar la red
        asyncio.run(Faithfulness(llm=llm).ascore(user_input="p", response="r", retrieved_contexts=["c"]))


# ------------------------------------------------------------ recorrido con juez doble
def test_respuesta_apoyada_es_evaluable_y_se_lee_en_value():
    filas = _evaluar([FILA])
    assert [f["metrica"] for f in filas] == ["faithfulness", "answer_relevancy"]
    assert all(f["evaluable"] and 0.0 <= f["valor"] <= 1.0 for f in filas)
    assert filas[0]["valor"] == 1.0
    assert filas[0]["consumo"]["llamadas_llm"] == 2  # afirmaciones + veredictos
    assert filas[1]["consumo"]["llamadas_llm"] == 3  # strictness = 3
    assert filas[0]["consumo"]["coste_usd"] is None  # el doble no tiene coste: desconocido ≠ 0


def test_afirmacion_sin_apoyo_baja_la_fidelidad():
    fila = {**FILA, "response": FILA["response"] + " Además incluyen un cortafuegos cuántico gratuito."}
    assert _evaluar([fila])[0]["valor"] == 0.5


@pytest.mark.parametrize(
    "cambio, motivo_f, motivo_r",
    [
        ({"rechazo": True}, "rechazo_sin_respuesta", "rechazo_sin_respuesta"),
        ({"error": "ErrorProveedor: x", "response": None}, "error_sistema", "error_sistema"),
        ({"response": "  "}, "respuesta_vacia", "respuesta_vacia"),
        ({"retrieved_contexts": []}, "contexto_vacio", None),
    ],
)
def test_no_evaluables_con_motivo(cambio, motivo_f, motivo_r):
    fidelidad, relevancia = _evaluar([{**FILA, **cambio}])
    assert (fidelidad["evaluable"], fidelidad["valor"], fidelidad["motivo"]) == (False, None, motivo_f)
    assert relevancia["motivo"] == motivo_r
    assert relevancia["evaluable"] is (motivo_r is None)


def test_fallo_del_juez_no_es_acierto():
    class JuezCaido(ev.JuezDoble):
        async def agenerate(self, prompt, response_model):
            raise TimeoutError("el juez no responde")

    filas = _evaluar([FILA], JuezCaido())
    assert all(not f["evaluable"] and f["valor"] is None for f in filas)
    assert {f["motivo"] for f in filas} == {"error_evaluador:TimeoutError"}


def test_nan_del_juez_es_no_evaluable():
    class JuezSinAfirmaciones(ev.JuezDoble):
        async def agenerate(self, prompt, response_model):
            if response_model.__name__ == "StatementGeneratorOutput":
                return response_model(statements=[])  # Ragas devuelve NaN en este caso
            return await super().agenerate(prompt, response_model)

    fidelidad = _evaluar([FILA], JuezSinAfirmaciones())[0]
    assert (fidelidad["evaluable"], fidelidad["motivo"]) == (False, "nan")


def test_cobertura_cuenta_solo_lo_que_habia_que_juzgar(tmp_path):
    filas = _evaluar(
        [FILA, {**FILA, "caso_id": "T02", "retrieved_contexts": []}, {**FILA, "caso_id": "T15", "rechazo": True}]
    )
    r = ev.resumen(filas)
    assert (r["faithfulness"]["evaluables"], r["faithfulness"]["esperados"]) == (1, 2)
    assert r["faithfulness"]["cobertura"] == 0.5
    assert r["answer_relevancy"]["cobertura"] == 1.0
    ev.intercambio.escribir_jsonl(tmp_path / "p.jsonl", filas, ev.intercambio.PUNTUACIONES)
    assert len(ev.intercambio.leer_jsonl(tmp_path / "p.jsonl", ev.intercambio.PUNTUACIONES)) == 6


def test_el_contrato_rechaza_un_nan_escrito_como_valor(tmp_path):
    mala = {**_evaluar([FILA])[0], "valor": float("nan")}
    with pytest.raises(ValueError):
        ev.intercambio.escribir_jsonl(tmp_path / "p.jsonl", [mala], ev.intercambio.PUNTUACIONES)


def test_modo_real_exige_clave_y_execute(tmp_path, monkeypatch, capsys):
    ev.intercambio.escribir_jsonl(
        tmp_path / "respuestas.jsonl",
        [{**FILA, "config_id": "A", "perfil": "doble", "conjunto": "test", "documentos_recuperados": []}],
        ev.intercambio.RESPUESTAS,
    )
    monkeypatch.setenv("GEMINI_API_KEY", "")
    assert ev.main([str(tmp_path), "--modo", "real"]) == 2
    assert not (tmp_path / "puntuaciones.jsonl").exists()  # no cae al juez doble
    assert "No se usa el juez doble" in capsys.readouterr().err


# ------------------------------------------------------------ ruta real con HTTP simulado
def _servidor_simulado(peticion: httpx.Request) -> httpx.Response:
    cuerpo = json.loads(peticion.content)
    if peticion.url.path.endswith("/embeddings"):
        textos = cuerpo["input"] if isinstance(cuerpo["input"], list) else [cuerpo["input"]]
        datos = [{"object": "embedding", "index": i, "embedding": [1.0, 0.0, 0.5]} for i, _ in enumerate(textos)]
        return httpx.Response(
            200,
            json={
                "object": "list",
                "data": datos,
                "model": cuerpo["model"],
                "usage": {"prompt_tokens": 9, "total_tokens": 9},
            },
        )
    texto = json.dumps(cuerpo)
    if "StatementGeneratorOutput" in texto:
        args = {"statements": ["Las pasarelas exigen TLS 1.3.", "Incluyen un cortafuegos cuántico."]}
        nombre = "StatementGeneratorOutput"
    elif "NLIStatementOutput" in texto:
        args = {
            "statements": [
                {"statement": "Las pasarelas exigen TLS 1.3.", "reason": "consta", "verdict": 1},
                {"statement": "Incluyen un cortafuegos cuántico.", "reason": "no consta", "verdict": 0},
            ]
        }
        nombre = "NLIStatementOutput"
    else:
        args, nombre = {"question": "¿Qué TLS exigen las pasarelas?", "noncommittal": 0}, "AnswerRelevanceOutput"
    mensaje = {"role": "assistant", "content": json.dumps(args)}
    if cuerpo.get("tools"):
        mensaje = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "c1",
                    "type": "function",
                    "function": {"name": cuerpo["tools"][0]["function"]["name"], "arguments": json.dumps(args)},
                }
            ],
        }
    return httpx.Response(
        200,
        json={
            "id": "x",
            "object": "chat.completion",
            "created": 0,
            "model": cuerpo["model"],
            "choices": [{"index": 0, "finish_reason": "stop", "message": mensaje}],
            # total > entrada + salida visible: la diferencia son tokens de razonamiento
            "usage": {"prompt_tokens": 1000, "completion_tokens": 100, "total_tokens": 1300},
            "_esquema": nombre,
        },
    )


def test_ruta_openai_compat_mide_tokens_y_coste_del_juez():
    llm, emb, contador = ev.crear_real(
        "openai_compat",
        "gemini-3.8-flash",
        "gemini-embedding-001",
        4096,
        "clave-falsa",
        transporte=httpx.MockTransport(_servidor_simulado),
    )
    assert llm.is_async is True
    evaluador = ev.descripcion_evaluador("real", "openai_compat", "gemini-3.8-flash", "gemini-embedding-001")
    fidelidad, relevancia = asyncio.run(ev.evaluar([FILA], llm, emb, evaluador, contador))
    assert fidelidad["valor"] == 0.5 and relevancia["evaluable"]
    assert fidelidad["consumo"]["llamadas_llm"] == 2
    assert fidelidad["consumo"]["tokens_entrada"] == 2000
    assert fidelidad["consumo"]["tokens_salida"] == 600  # incluye razonamiento
    # 2000 × 0,75 + 600 × 3,75 = 3750 → 0,00375 USD (tarifas.json)
    assert fidelidad["consumo"]["coste_usd"] == pytest.approx(0.00375)
    assert relevancia["consumo"]["llamadas_llm"] == 3
    assert relevancia["consumo"]["llamadas_embeddings"] >= 1


# ------------------------------------------------------------ evaluación real (de pago)
@pytest.mark.llm
def test_juez_real_puntua_una_respuesta():
    if os.environ.get("S19_EJECUTAR_REAL") != "1" or not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("evaluación real: exige GEMINI_API_KEY y S19_EJECUTAR_REAL=1")
    llm, emb, contador = ev.crear_real(
        os.environ.get("S19_EVAL_RUTA", "openai_compat"),
        os.environ.get("S19_EVAL_LLM_MODEL", "gemini-3.8-flash"),
        os.environ.get("S19_EVAL_EMBEDDING_MODEL", "gemini-embedding-001"),
        4096,
        os.environ["GEMINI_API_KEY"],
    )
    evaluador = ev.descripcion_evaluador("real", "openai_compat", "gemini-3.8-flash", "gemini-embedding-001")
    filas = asyncio.run(ev.evaluar([FILA], llm, emb, evaluador, contador))
    assert all(f["evaluable"] for f in filas), [f["motivo"] for f in filas]
