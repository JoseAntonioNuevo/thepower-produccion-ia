"""Pruebas del límite con Anthropic: transporte simulado, cero llamadas de pago."""

import asyncio
import json

import httpx
import pytest

from curso_ia.config import Settings
from curso_ia.proveedores import AnthropicProvider, ErrorProveedor


def respuesta():
    return {
        "model": "modelo-test",
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 10},
        "content": [
            {
                "type": "text",
                "text": json.dumps(
                    {
                        "categoria": "acceso",
                        "prioridad": "media",
                        "respuesta": "Revisa el código ficticio.",
                    }
                ),
            }
        ],
    }


def ejecutar(handler):
    async def run():
        cfg = Settings(mode="real", model_id="modelo-test", api_key="clave-sintetica")
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            return await AnthropicProvider(cfg, client).clasificar("No puedo entrar al ejemplo")

    return asyncio.run(run())


def test_peticion_contrato_y_consumo_desconocido():
    def handler(request):
        assert request.url == "https://api.anthropic.com/v1/messages"
        data = json.loads(request.content)
        assert data["model"] == "modelo-test"
        assert data["max_tokens"] == 300
        assert "temperature" not in data
        return httpx.Response(200, json=respuesta())

    result = ejecutar(handler)
    assert result.clasificacion.categoria == "acceso"
    assert result.consumo.input_tokens == 10
    assert result.consumo.output_tokens is None


@pytest.mark.parametrize(
    "status,code",
    [
        (302, "proveedor_http"),
        (401, "proveedor_http"),
        (429, "proveedor_limitado"),
        (500, "proveedor_http"),
    ],
)
def test_rechaza_http_sin_reintento_ni_redireccion(status, code):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(status, headers={"location": "https://otro.test"})

    with pytest.raises(ErrorProveedor, match=code):
        ejecutar(handler)
    assert len(calls) == 1


@pytest.mark.parametrize("kind", ["truncada", "formato", "tamano", "timeout"])
def test_salida_y_tiempo_acotados(kind):
    def handler(request):
        data = respuesta()
        if kind == "timeout":
            raise httpx.ReadTimeout("detalle privado", request=request)
        if kind == "truncada":
            data["stop_reason"] = "max_tokens"
        if kind == "formato":
            data["content"][0]["text"] = '{"categoria":"inventada"}'
        if kind == "tamano":
            return httpx.Response(200, content=b"x" * 66000)
        return httpx.Response(200, json=data)

    with pytest.raises(ErrorProveedor) as error:
        ejecutar(handler)
    assert "detalle privado" not in str(error.value)
