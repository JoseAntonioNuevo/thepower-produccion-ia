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


def test_sin_dependencias_de_un_proveedor_concreto():
    """El juez real va siempre por OpenRouter: no se instala ningún SDK de proveedor."""
    with pytest.raises(md.PackageNotFoundError):
        md.version("google-genai")
    assert md.version("openai") == "3.3.0"


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
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    assert ev.main([str(tmp_path), "--modo", "real"]) == 2
    assert not (tmp_path / "puntuaciones.jsonl").exists()  # no cae al juez doble
    assert "No se usa el juez doble" in capsys.readouterr().err


# ------------------------------------------------------------ juez real (OpenRouter) con HTTP simulado
PETICIONES: list[dict] = []


def _servidor_simulado(peticion: httpx.Request) -> httpx.Response:
    """Imita a OpenRouter: responde en formato OpenAI y añade `usage.cost` (lo cobrado)."""
    cuerpo = json.loads(peticion.content)
    PETICIONES.append({"ruta": peticion.url.path, **cuerpo})
    if peticion.url.path.endswith("/embeddings"):
        textos = cuerpo["input"] if isinstance(cuerpo["input"], list) else [cuerpo["input"]]
        datos = [{"object": "embedding", "index": i, "embedding": [1.0, 0.0, 0.5]} for i, _ in enumerate(textos)]
        return httpx.Response(
            200,
            json={
                "object": "list",
                "data": datos,
                "model": cuerpo["model"],
                "usage": {"prompt_tokens": 9, "total_tokens": 9, "cost": 0.000001},
            },
        )
    texto = json.dumps(cuerpo)
    if "StatementGeneratorOutput" in texto:
        args = {"statements": ["Las pasarelas exigen TLS 1.3.", "Incluyen un cortafuegos cuántico."]}
    elif "NLIStatementOutput" in texto:
        args = {
            "statements": [
                {"statement": "Las pasarelas exigen TLS 1.3.", "reason": "consta", "verdict": 1},
                {"statement": "Incluyen un cortafuegos cuántico.", "reason": "no consta", "verdict": 0},
            ]
        }
    else:
        args = {"question": "¿Qué TLS exigen las pasarelas?", "noncommittal": 0}
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
            "provider": "Anthropic",
            "choices": [{"index": 0, "finish_reason": "stop", "message": mensaje}],
            # total > entrada + salida visible: la diferencia son tokens de razonamiento
            "usage": {"prompt_tokens": 1000, "completion_tokens": 100, "total_tokens": 1300, "cost": 0.0012},
        },
    )


def _juez_simulado(ajustes=None):
    PETICIONES.clear()
    return ev.crear_real(
        "anthropic/claude-haiku-5.5",
        "openai/text-embedding-3-small",
        4096,
        "clave-falsa",
        ajustes,
        transporte=httpx.MockTransport(_servidor_simulado),
        url_base="https://openrouter.ai/api/v1",
    )


def test_juez_openrouter_mide_tokens_y_el_coste_cobrado():
    llm, emb, contador = _juez_simulado()
    assert llm.is_async is True
    evaluador = ev.descripcion_evaluador("real", "openrouter", "anthropic/claude-haiku-5.5", "openai/text-embedding-3-small")
    fidelidad, relevancia = asyncio.run(ev.evaluar([FILA], llm, emb, evaluador, contador))
    assert fidelidad["valor"] == 0.5 and relevancia["evaluable"]
    assert all(p["ruta"].startswith("/api/v1/") for p in PETICIONES)  # todo va a OpenRouter
    assert fidelidad["consumo"]["llamadas_llm"] == 2
    assert fidelidad["consumo"]["tokens_entrada"] == 2000
    assert fidelidad["consumo"]["tokens_salida"] == 600  # incluye razonamiento
    # Coste: el que devuelve OpenRouter en usage.cost (2 × 0,0012), no una estimación.
    assert fidelidad["consumo"]["coste_usd"] == pytest.approx(0.0024)
    assert fidelidad["consumo"]["coste_fuente"] == "openrouter"
    assert relevancia["consumo"]["llamadas_llm"] == 3
    assert relevancia["consumo"]["llamadas_embeddings"] >= 1


def test_ajustes_de_env_llegan_a_cada_peticion():
    ajustes = {
        "llm_proveedores": ["Anthropic"],
        "embedding_proveedores": ["OpenAI"],
        "llm_extra": {"usage": {"include": True}},
        "quitar_parametros": ["temperature", "top_p"],
    }
    llm, emb, contador = _juez_simulado(ajustes)
    evaluador = ev.descripcion_evaluador("real", "openrouter", "x", "y", ajustes)
    asyncio.run(ev.evaluar([FILA], llm, emb, evaluador, contador))
    chat = [p for p in PETICIONES if p["ruta"].endswith("/chat/completions")]
    embeddings = [p for p in PETICIONES if p["ruta"].endswith("/embeddings")]
    assert chat and embeddings
    assert all(p["provider"] == {"order": ["Anthropic"], "allow_fallbacks": False} for p in chat)
    assert all("temperature" not in p and "top_p" not in p for p in chat)
    assert all(p["usage"] == {"include": True} for p in chat)
    assert all(p["provider"] == {"order": ["OpenAI"], "allow_fallbacks": False} for p in embeddings)
    assert evaluador["ajustes"] == ajustes  # forman parte de la identidad del evaluador


def test_con_byok_el_coste_del_juez_incluye_lo_que_factura_el_proveedor():
    def byok(peticion):
        datos = _servidor_simulado(peticion).json()
        datos["usage"].update(cost=0, is_byok=True, cost_details={"upstream_inference_cost": 0.002})
        return httpx.Response(200, json=datos)

    PETICIONES.clear()
    llm, emb, contador = ev.crear_real(
        "anthropic/claude-opus-5.5",
        "openai/text-embedding-3-small",
        4096,
        "clave-falsa",
        transporte=httpx.MockTransport(byok),
        url_base="https://openrouter.ai/api/v1",
    )
    evaluador = ev.descripcion_evaluador("real", "openrouter", "anthropic/claude-opus-5.5", "openai/text-embedding-3-small")
    fidelidad, _ = asyncio.run(ev.evaluar([FILA], llm, emb, evaluador, contador))
    assert fidelidad["consumo"]["coste_usd"] == pytest.approx(0.004)  # 2 llamadas × 0,002, no 0
    assert fidelidad["consumo"]["coste_fuente"] == "openrouter"


def test_los_parametros_que_el_juez_no_admite_se_quitan_segun_el_catalogo():
    # anthropic/claude-opus-5.5 no admite temperature ni top_p según tarifas.json (OpenRouter).
    assert ev.parametros_no_admitidos("anthropic/claude-opus-5.5") == ["temperature", "top_p"]
    assert ev.parametros_no_admitidos("google/gemini-4-hydrogen") == []
    assert ev.parametros_no_admitidos("modelo/desconocido") == []  # sin ficha no se adivina


def test_sin_coste_informado_se_estima_con_la_tarifa_y_se_dice():
    def sin_coste(peticion):
        respuesta = _servidor_simulado(peticion)
        datos = respuesta.json()
        datos["usage"].pop("cost", None)
        return httpx.Response(200, json=datos)

    PETICIONES.clear()
    llm, emb, contador = ev.crear_real(
        "anthropic/claude-haiku-5.5",
        "openai/text-embedding-3-small",
        4096,
        "clave-falsa",
        transporte=httpx.MockTransport(sin_coste),
        url_base="https://openrouter.ai/api/v1",
    )
    evaluador = ev.descripcion_evaluador("real", "openrouter", "anthropic/claude-haiku-5.5", "openai/text-embedding-3-small")
    fidelidad, _ = asyncio.run(ev.evaluar([FILA], llm, emb, evaluador, contador))
    # 2000 × 0,10 + 600 × 0,50 = 500 → 0,0005 USD con tarifas.json (precios de OpenRouter)
    assert fidelidad["consumo"]["coste_usd"] == pytest.approx(0.0005)
    assert fidelidad["consumo"]["coste_fuente"] == "tarifa"


# ------------------------------------------------------------ evaluación real (de pago)
@pytest.mark.llm
def test_juez_real_puntua_una_respuesta():
    ev.cargar_env()  # la clave está en ../.env, igual que en evaluar.py
    if os.environ.get("S19_EJECUTAR_REAL") != "1" or not os.environ.get("OPENROUTER_API_KEY"):
        pytest.skip("evaluación real: exige OPENROUTER_API_KEY y S19_EJECUTAR_REAL=1")
    modelo = os.environ.get("S19_EVAL_LLM_MODEL") or ev.EVAL_LLM_MODELO_DEFECTO
    modelo_emb = os.environ.get("S19_EVAL_EMBEDDING_MODEL") or ev.EVAL_EMBEDDING_MODELO_DEFECTO
    ajustes = ev.ajustes_desde_entorno()
    llm, emb, contador = ev.crear_real(modelo, modelo_emb, 4096, os.environ["OPENROUTER_API_KEY"], ajustes)
    evaluador = ev.descripcion_evaluador("real", "openrouter", modelo, modelo_emb, ajustes)
    filas = asyncio.run(ev.evaluar([FILA], llm, emb, evaluador, contador))
    assert all(f["evaluable"] for f in filas), [f["motivo"] for f in filas]
    assert all(f["consumo"]["coste_fuente"] == "openrouter" for f in filas)
