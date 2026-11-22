"""Perfil real sobre OpenRouter, sin red ni coste.

Se usa el cliente `openai` de verdad con un transporte HTTP simulado: así se comprueba
lo que viaja en cada petición (modelo, dimensión, proveedores, parámetros) y cómo se lee
la respuesta (vector, texto, tokens, coste cobrado, modelo y proveedor servidos).
"""

import json
import re
from pathlib import Path

import httpx
import pytest
from openai import OpenAI

from evaluacion.comparar import ComparacionInvalida, variable_cambiada
from rag import catalogo
from rag.config import (
    EVAL_EMBEDDING_MODELO_DEFECTO,
    EVAL_LLM_MODELO_DEFECTO,
    GEN_MODELO_DEFECTO,
    RAIZ,
    ErrorConfiguracion,
    aplicar_variante,
    calibracion_vale,
    cargar_config,
)
from rag.consulta import responder
from rag.ingesta import indice_esperado
from rag.proveedores import EmbeddingsOpenRouter, ErrorProveedor, GeneradorOpenRouter, Proveedores
from tests.conftest import config

PETICIONES: list[dict] = []


def _openrouter(peticion: httpx.Request) -> httpx.Response:
    cuerpo = json.loads(peticion.content)
    PETICIONES.append({"ruta": peticion.url.path, **cuerpo})
    if peticion.url.path.endswith("/embeddings"):
        dim = cuerpo.get("dimensions", 1536)
        return httpx.Response(
            200,
            json={
                "object": "list",
                "model": cuerpo["model"],
                "data": [{"object": "embedding", "index": 0, "embedding": [0.1] * dim}],
                "usage": {"prompt_tokens": 7, "total_tokens": 7, "cost": 0.00000014},
            },
        )
    return httpx.Response(
        200,
        json={
            "id": "gen-1",
            "object": "chat.completion",
            "created": 0,
            "model": cuerpo["model"] + "-20261101",
            "provider": "Google",
            "choices": [
                {
                    "index": 0,
                    "finish_reason": "stop",
                    "message": {"role": "assistant", "content": "Del 25 % [05-sla-y-creditos-servicio]."},
                }
            ],
            "usage": {"prompt_tokens": 900, "completion_tokens": 40, "total_tokens": 940, "cost": 0.00037},
        },
    )


def _cliente() -> OpenAI:
    PETICIONES.clear()
    http = httpx.Client(transport=httpx.MockTransport(_openrouter))
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key="clave-falsa", http_client=http, max_retries=0)


def _real(**cambios):
    base = dict(
        perfil="real",
        embedding_modelo="openai/text-embedding-3-small",
        gen_modelo="google/gemini-3.5-flash-lite",
        gen_max_tokens=512,
        gen_temperatura=None,
        gen_proveedores=("Google",),
        embedding_proveedores=(),
        embedding_enviar_dim=True,
        plantilla_documento="title: {titulo} | text: {texto}",
        plantilla_consulta="query: {texto}",
    )
    return config(**{**base, **cambios})


# ------------------------------------------------------------ embeddings
def test_embeddings_piden_modelo_dimension_y_plantilla_de_env():
    emb = EmbeddingsOpenRouter(_real(), _cliente())
    vector = emb.incrustar_documento("SLA", "La disponibilidad es del 99,95 %.")
    assert len(vector) == 768
    peticion = PETICIONES[-1]
    assert peticion["ruta"] == "/api/v1/embeddings"
    assert peticion["model"] == "openai/text-embedding-3-small"
    assert peticion["dimensions"] == 768
    assert peticion["input"] == "title: SLA | text: La disponibilidad es del 99,95 %."
    emb.incrustar_consulta("¿Qué SLA?")
    assert PETICIONES[-1]["input"] == "query: ¿Qué SLA?"
    assert emb.coste_conocido and emb.coste_usd == pytest.approx(0.00000028)


def test_sin_enviar_dimension_un_vector_de_otra_longitud_es_un_error_claro():
    emb = EmbeddingsOpenRouter(_real(embedding_enviar_dim=False), _cliente())
    with pytest.raises(ErrorProveedor, match="S19_EMBEDDING_DIM=1536"):
        emb.incrustar_consulta("hola")
    assert "dimensions" not in PETICIONES[-1]


# ------------------------------------------------------------ generación
def test_generacion_envia_lo_de_env_y_lee_coste_modelo_y_proveedor():
    gen = GeneradorOpenRouter(_real(gen_temperatura=0.2), _cliente())
    g = gen.generar("¿Qué crédito?", [("05-sla-y-creditos-servicio", "Crédito del 25 %.")], "v1")
    peticion = PETICIONES[-1]
    assert peticion["ruta"] == "/api/v1/chat/completions"
    assert peticion["model"] == "google/gemini-3.5-flash-lite"
    assert peticion["max_tokens"] == 512 and peticion["temperature"] == 0.2
    assert peticion["provider"] == {"order": ["Google"], "allow_fallbacks": False}
    assert [m["role"] for m in peticion["messages"]] == ["system", "user"]
    assert (g.tokens_entrada, g.tokens_salida, g.coste_usd) == (900, 40, 0.00037)
    assert (g.model_version, g.proveedor_servido) == ("google/gemini-3.5-flash-lite-20261101", "Google")


def test_temperatura_vacia_no_se_envia_y_el_extra_si():
    gen = GeneradorOpenRouter(_real(gen_proveedores=(), gen_extra='{"reasoning": {"effort": "low"}}'), _cliente())
    gen.generar("p", [("01-arquitectura-aethercloud", "c")], "v1")
    assert "temperature" not in PETICIONES[-1] and "provider" not in PETICIONES[-1]
    assert PETICIONES[-1]["reasoning"] == {"effort": "low"}


def test_razonamiento_bajo_por_defecto_y_se_puede_anular(monkeypatch):
    _entorno(monkeypatch, S19_PERFIL="real")
    assert json.loads(cargar_config().gen_extra) == {"reasoning": {"effort": "low"}}
    _entorno(monkeypatch, S19_PERFIL="real", S19_GEN_EXTRA="{}")
    assert json.loads(cargar_config().gen_extra) == {}


def test_agotar_max_tokens_queda_avisado(sistema):
    def corto(peticion):
        datos = _openrouter(peticion).json()
        datos["choices"][0].update(finish_reason="length", message={"role": "assistant", "content": ""})
        return httpx.Response(200, json=datos)

    almacen, prov, indice_id = sistema
    http = httpx.Client(transport=httpx.MockTransport(corto))
    cliente = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="clave-falsa", http_client=http, max_retries=0)
    r = responder(
        config(gen_modelo="google/gemini-4-hydrogen"),
        almacen,
        Proveedores(prov.embeddings, GeneradorOpenRouter(_real(), cliente)),
        indice_id,
        "¿Qué crédito corresponde si la disponibilidad mensual es inferior al 99,00 %?",
    )
    assert {"respuesta_vacia", "max_tokens_agotado"} <= set(r.avisos)


def test_una_consulta_real_registra_el_coste_cobrado(sistema):
    almacen, prov, indice_id = sistema
    gen = GeneradorOpenRouter(_real(), _cliente())
    r = responder(
        config(gen_modelo="google/gemini-3.5-flash-lite"),
        almacen,
        Proveedores(prov.embeddings, gen),
        indice_id,
        "¿Qué crédito corresponde si la disponibilidad mensual es inferior al 99,00 %?",
    )
    assert (r.coste_usd, r.coste_fuente, r.proveedor_servido) == (0.00037, "openrouter", "Google")


@pytest.mark.parametrize(
    "uso,esperado",
    [
        ({"cost": 0.0004}, (0.0004, False)),  # crédito de OpenRouter: cost es la inferencia
        # BYOK: cost es la comisión de OpenRouter; la inferencia la factura el proveedor.
        ({"cost": 0, "is_byok": True, "cost_details": {"upstream_inference_cost": 0.000915}}, (0.000915, True)),
        ({"cost": 0.00001, "is_byok": True, "cost_details": {"upstream_inference_cost": 0.001}}, (0.00101, True)),
        ({"cost": 0, "is_byok": True, "cost_details": {}}, (None, True)),  # falta el dato: desconocido, no 0
        ({}, (None, False)),
    ],
)
def test_coste_total_suma_lo_que_factura_el_proveedor_con_byok(uso, esperado):
    from rag.openrouter import coste_total

    coste, byok = coste_total(uso)
    assert byok == esperado[1]
    assert coste == pytest.approx(esperado[0]) if esperado[0] is not None else coste is None


def test_generacion_con_byok_no_registra_coste_cero():
    def byok(peticion):
        respuesta = _openrouter(peticion).json()
        respuesta["usage"].update(cost=0, is_byok=True, cost_details={"upstream_inference_cost": 0.00412})
        return httpx.Response(200, json=respuesta)

    http = httpx.Client(transport=httpx.MockTransport(byok))
    cliente = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="clave-falsa", http_client=http, max_retries=0)
    g = GeneradorOpenRouter(_real(), cliente).generar("p", [("01-arquitectura-aethercloud", "c")], "v1")
    assert g.coste_usd == pytest.approx(0.00412)


# ------------------------------------------------------------ configuración desde .env
def _entorno(monkeypatch, **valores):
    monkeypatch.setattr("rag.config.cargar_env", lambda ruta=None: None)
    for clave in [k for k in __import__("os").environ if k.startswith("S19_")]:
        monkeypatch.delenv(clave, raising=False)
    for clave, valor in valores.items():
        monkeypatch.setenv(clave, valor)


def test_todo_el_perfil_real_sale_de_env(monkeypatch):
    _entorno(
        monkeypatch,
        S19_PERFIL="real",
        S19_GEN_MODEL="anthropic/claude-haiku-5.5",
        S19_GEN_TEMPERATURE="",
        S19_GEN_PROVEEDORES="Anthropic, Amazon Bedrock",
        S19_EMBEDDING_MODEL="qwen/qwen3-embedding-8b",
        S19_EMBEDDING_DIM="4096",
        S19_EMBEDDING_ENVIAR_DIM="false",
        S19_EMBEDDING_PLANTILLA_DOCUMENTO="{titulo}\\n\\n{texto}",
    )
    cfg = cargar_config()
    assert cfg.gen_modelo == "anthropic/claude-haiku-5.5" and cfg.gen_temperatura is None
    assert cfg.gen_proveedores == ("Anthropic", "Amazon Bedrock")
    assert (cfg.embedding_modelo, cfg.embedding_dim, cfg.embedding_enviar_dim) == ("qwen/qwen3-embedding-8b", 4096, False)
    assert cfg.plantilla_documento == "{titulo}\n\n{texto}"
    assert cfg.publica()["gen_proveedores"] == ["Anthropic", "Amazon Bedrock"]


def test_variables_vacias_toman_el_valor_por_defecto(monkeypatch):
    _entorno(monkeypatch, S19_PERFIL="real", S19_GEN_MODEL="", S19_EMBEDDING_DIM="")
    cfg = cargar_config()
    assert cfg.gen_modelo == "google/gemini-4-hydrogen" and cfg.embedding_dim == 768 and cfg.gen_max_tokens == 2048


@pytest.mark.parametrize(
    "variable,valor",
    [
        ("S19_EMBEDDING_PLANTILLA_CONSULTA", "sin marcador"),
        ("S19_EMBEDDING_PLANTILLA_DOCUMENTO", "{texto} {otro}"),
        ("S19_EMBEDDING_ENVIAR_DIM", "quizás"),
        ("S19_GEN_TEMPERATURE", "fría"),
        ("S19_EMBEDDING_DIM", "0"),
    ],
)
def test_valores_invalidos_se_rechazan(monkeypatch, variable, valor):
    _entorno(monkeypatch, S19_PERFIL="real", **{variable: valor})
    with pytest.raises(ErrorConfiguracion):
        cargar_config()


def test_el_perfil_doble_no_cambia_con_los_ajustes_del_real(monkeypatch):
    _entorno(monkeypatch, S19_PERFIL="doble", S19_EMBEDDING_DIM="3072", S19_GEN_MODEL="openai/gpt-6-luna")
    cfg = cargar_config()
    assert (cfg.embedding_modelo, cfg.embedding_dim, cfg.gen_modelo) == ("doble-hash-768", 768, "doble-extractivo")
    assert "plantilla_documento" not in cfg.publica()  # el formato del doble no cambia


def test_cambiar_modelo_o_plantilla_crea_otro_indice_y_anula_la_calibracion():
    base = _real()
    otro_modelo = _real(embedding_modelo="google/gemini-embedding-2")
    otra_plantilla = _real(plantilla_documento="{texto}")
    ids = {indice_esperado(c) for c in (base, otro_modelo, otra_plantilla)}
    assert len(ids) == 3
    calibrada = {
        "embedding_modelo": base.embedding_modelo,
        "embedding_dim": 768,
        "plantilla_documento": base.plantilla_documento,
        "plantilla_consulta": base.plantilla_consulta,
    }
    assert calibracion_vale(base, calibrada)
    assert not calibracion_vale(otro_modelo, calibrada)
    assert not calibracion_vale(otra_plantilla, calibrada)


def test_el_modelo_de_generacion_puede_ser_la_variable_comparada():
    cfg = _real()
    a = aplicar_variante(cfg, "A")
    b = a.__class__(**{**a.__dict__, "gen_modelo": "anthropic/claude-haiku-5.5", "config_id": "M2"})

    def informe(c, modelo):
        return {
            "conjunto": "test",
            "huella_conjunto": "x",
            "perfil": "real",
            "n_casos": 20,
            "modelos": {"generacion": modelo, "embeddings": c.embedding_modelo},
            "config": c.publica(),
        }

    assert variable_cambiada(informe(a, a.gen_modelo), informe(b, b.gen_modelo)) == "gen_modelo"
    otro_emb = b.__class__(**{**b.__dict__, "embedding_modelo": "google/gemini-embedding-2"})
    with pytest.raises(ComparacionInvalida, match="embeddings"):
        variable_cambiada(informe(a, a.gen_modelo), informe(otro_emb, otro_emb.gen_modelo))


def test_una_variante_de_modelo_no_vale_en_el_perfil_doble(tmp_path):
    ruta = tmp_path / "configuraciones.json"
    ruta.write_text(json.dumps({"variantes": {"M": {"gen_modelo": "openai/gpt-6-luna"}}}), encoding="utf-8")
    with pytest.raises(ErrorConfiguracion, match="perfil real"):
        aplicar_variante(config(), "M", ruta)
    assert aplicar_variante(_real(), "M", ruta).gen_modelo == "openai/gpt-6-luna"


def test_los_valores_por_defecto_del_juez_coinciden_con_el_evaluador():
    texto = (RAIZ / "evaluador" / "evaluar.py").read_text(encoding="utf-8")
    assert re.search(rf'EVAL_LLM_MODELO_DEFECTO = "{re.escape(EVAL_LLM_MODELO_DEFECTO)}"', texto)
    assert re.search(rf'EVAL_EMBEDDING_MODELO_DEFECTO = "{re.escape(EVAL_EMBEDDING_MODELO_DEFECTO)}"', texto)


def test_env_example_documenta_todas_las_variables_del_perfil_real():
    ejemplo = (RAIZ / ".env.example").read_text(encoding="utf-8")
    usadas = set()
    for archivo in [*(RAIZ / "rag").glob("*.py"), RAIZ / "evaluador" / "evaluar.py"]:
        usadas |= set(re.findall(r'"(S19_[A-Z_]+|OPENROUTER_API_KEY)"', archivo.read_text(encoding="utf-8")))
    faltan = sorted(v for v in usadas if v not in ejemplo)
    assert not faltan, f"variables sin documentar en .env.example: {faltan}"


# ------------------------------------------------------------ catálogo
def _catalogo(peticion: httpx.Request) -> httpx.Response:
    if peticion.url.path.endswith("/embeddings/models"):
        datos = [{"id": "openai/text-embedding-3-small", "pricing": {"prompt": "0.00000002"}, "context_length": 8192}]
    else:
        datos = [
            {
                "id": "google/gemini-3.5-flash-lite",
                "pricing": {"prompt": "0.0000003", "completion": "0.0000025"},
                "context_length": 1048576,
                "supported_parameters": ["max_tokens", "temperature", "response_format"],
            },
            {
                "id": "anthropic/claude-haiku-5.5",
                "pricing": {"prompt": "0.0000001", "completion": "0.0000005"},
                "supported_parameters": ["max_tokens", "response_format"],
            },
        ]
    return httpx.Response(200, json={"data": datos})


def test_catalogo_guarda_precios_por_millon_y_parametros(tmp_path: Path):
    fichas = catalogo.descargar("https://openrouter.ai/api/v1", httpx.Client(transport=httpx.MockTransport(_catalogo)))
    datos = catalogo.actualizar(
        ["google/gemini-3.5-flash-lite", "openai/text-embedding-3-small"], fichas, tmp_path / "tarifas.json"
    )
    gen = datos["modelos"]["google/gemini-3.5-flash-lite"]
    assert (gen["tipo"], gen["entrada"], gen["salida"]) == ("chat", 0.3, 2.5)
    assert datos["modelos"]["openai/text-embedding-3-small"]["tipo"] == "embeddings"
    assert catalogo.avisos_parametros(fichas["anthropic/claude-haiku-5.5"], ["max_tokens", "temperature"]) == ["temperature"]


def test_catalogo_rechaza_un_modelo_inexistente_y_sugiere_el_nombre(tmp_path: Path):
    fichas = catalogo.descargar("https://openrouter.ai/api/v1", httpx.Client(transport=httpx.MockTransport(_catalogo)))
    with pytest.raises(ErrorConfiguracion, match="google/gemini-3.5-flash-lite"):
        catalogo.actualizar(["gemini-3.5-flash-lite"], fichas, tmp_path / "tarifas.json")
    assert not (tmp_path / "tarifas.json").exists()


def test_tarifas_tiene_los_modelos_por_defecto():
    precios = json.loads((RAIZ / "tarifas.json").read_text(encoding="utf-8"))["modelos"]
    for modelo in (
        GEN_MODELO_DEFECTO,
        "openai/text-embedding-3-small",
        EVAL_LLM_MODELO_DEFECTO,
        EVAL_EMBEDDING_MODELO_DEFECTO,
    ):
        assert modelo in precios, modelo


def test_las_variantes_de_modelo_solo_cambian_el_generador():
    """Evaluación de modelos: MH y MS comparten índice, prompt, parámetros y juez; solo cambia el modelo."""
    a, b = aplicar_variante(_real(), "MH").publica(), aplicar_variante(_real(), "MS").publica()
    distintas = sorted(k for k in a if a[k] != b[k] and k != "config_id")
    assert distintas == ["gen_modelo"]
    assert (a["gen_modelo"], b["gen_modelo"]) == ("google/gemini-4-hydrogen", "openai/gpt-6.2-sol")
