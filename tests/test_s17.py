"""S17 sin red: contrato Lambda, SDK, IAM/SigV4, perfiles y evidencia de cold/warm."""

import base64
import json
import time
from pathlib import Path
from types import SimpleNamespace

import boto3
import pytest
from botocore.credentials import Credentials
from botocore.exceptions import ClientError, ReadTimeoutError
from botocore.stub import Stubber

from curso_ia.serverless.bedrock import TOOL_NAME, classify, request_for
from curso_ia.serverless.config import REFERENCE_MODEL, Settings
from curso_ia.serverless.demo import DemoClient, DemoContext, event_for
from curso_ia.serverless.evidencia import parse_report, resumir_mediciones, validar_perfil
from curso_ia.serverless.firma import signed_headers
from curso_ia.serverless.handler import handle
from scripts import aws_s17
from scripts.costes_s17 import estimar, incorporar_mediciones


def run(event=None, client=None, context=None):
    return handle(
        event or event_for(),
        context or DemoContext(),
        cfg=Settings(mode="demo"),
        client=client or DemoClient(),
    )


def test_handler_reutiliza_contrato_y_rotula_demo(capsys):
    result = run()
    data = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert data["resultado"]["categoria"] == "facturacion"
    assert data["metadata"]["execution"] == "demo"
    assert data["metadata"]["consumo"]["inputTokens"] is None
    assert "Me han cobrado" not in capsys.readouterr().out


@pytest.mark.parametrize(
    "case,status",
    [("vacia", 422), ("grande", 413), ("base64", 400), ("tipo", 415), ("ruta", 404), ("json", 400)],
)
def test_rechazo_antes_de_inferencia(case, status):
    event = event_for()
    if case == "vacia":
        event["body"] = '{"texto":""}'
    if case == "grande":
        event["body"] = "x" * 20000
    if case == "base64":
        event.update(body="%%%", isBase64Encoded=True)
    if case == "tipo":
        event["headers"] = {"content-type": "text/plain"}
    if case == "ruta":
        event["rawPath"] = "/otra"
    if case == "json":
        event["body"] = "{"

    class NoCall:
        def converse(self, **kwargs):
            pytest.fail("No se debe invocar Bedrock")

    assert run(event, NoCall())["statusCode"] == status


def test_base64_valida_y_tiempo_insuficiente():
    event = event_for()
    event["headers"] = {"Content-Type": "Application/JSON; charset=utf-8"}
    event.update(body=base64.b64encode(event["body"].encode()).decode(), isBase64Encoded=True)
    assert run(event)["statusCode"] == 200
    context = SimpleNamespace(
        aws_request_id="demo", function_version="local", get_remaining_time_in_millis=lambda: 19000
    )
    result = run(context=context)
    assert result["statusCode"] == 504
    assert json.loads(result["body"])["error"] == "presupuesto_tiempo_agotado"
    event = event_for()
    event["requestContext"]["timeEpoch"] = int(time.time() * 1000) - 10000
    assert run(event)["statusCode"] == 504


@pytest.mark.parametrize(
    "case,status",
    [("throttle", 503), ("timeout", 504), ("permiso", 502), ("invalida", 502), ("sin_tool", 502)],
)
def test_fallos_no_se_reintentan_ni_se_convierten_en_demo(case, status):
    calls = []

    class Client:
        def converse(self, **kwargs):
            calls.append(kwargs)
            if case == "timeout":
                raise ReadTimeoutError(endpoint_url="https://example.invalid")
            if case in {"throttle", "permiso"}:
                raise ClientError(
                    {
                        "Error": {
                            "Code": "ThrottlingException"
                            if case == "throttle"
                            else "AccessDeniedException",
                            "Message": "privado",
                        }
                    },
                    "Converse",
                )
            result = DemoClient().converse()
            if case == "invalida":
                result["output"]["message"]["content"][0]["toolUse"]["input"]["prioridad"] = (
                    "inventada"
                )
            if case == "sin_tool":
                result["stopReason"] = "end_turn"
            return result

    result = run(client=Client())
    assert result["statusCode"] == status and len(calls) == 1
    assert "privado" not in result["body"] and "resultado" not in result["body"]


def test_converse_valido_con_stubber_del_sdk_instalado():
    cfg = Settings()
    client = boto3.client(
        "bedrock-runtime",
        region_name="eu-west-1",
        aws_access_key_id="demo",
        aws_secret_access_key="demo",
        aws_session_token="demo",
    )
    response = DemoClient().converse()
    response["usage"] = {"inputTokens": 10, "outputTokens": 20, "totalTokens": 30}
    response["metrics"] = {"latencyMs": 400}
    request = request_for("Factura ficticia duplicada", cfg)
    assert request["toolConfig"]["toolChoice"] == {"tool": {"name": TOOL_NAME}}
    with Stubber(client) as stub:
        stub.add_response("converse", response, request)
        result, tokens, latency = classify("Factura ficticia duplicada", cfg, client)
        assert (
            result["categoria"] == "facturacion" and tokens["totalTokens"] == 30 and latency == 400
        )


def test_firma_temporal_sin_filtrar_fuera_de_execute_api():
    url = "https://abcdef1234.execute-api.eu-west-1.amazonaws.com/clasificar"
    headers = signed_headers(
        url, b'{"texto":"demo"}', "eu-west-1", Credentials("demo", "demo", "temporal")
    )
    assert headers["X-Amz-Security-Token"] == "temporal"
    assert "/eu-west-1/execute-api/aws4_request" in headers["Authorization"]
    for bad in [
        "http://abcdef1234.execute-api.eu-west-1.amazonaws.com/clasificar",
        "https://api.example.com/clasificar",
        url + "?otra=1",
    ]:
        with pytest.raises(ValueError):
            signed_headers(bad, b"{}", "eu-west-1", Credentials("d", "d", "d"))
    with pytest.raises(ValueError):
        signed_headers(url, b"{}", "eu-west-1", Credentials("d", "d"))


def test_perfil_europeo_y_modelo_origen_con_permisos_acotados():
    account = "123456789012"
    data = {
        "status": "ACTIVE",
        "inferenceProfileArn": (
            f"arn:aws:bedrock:eu-west-1:{account}:inference-profile/{REFERENCE_MODEL}"
        ),
        "models": [
            {"modelArn": "arn:aws:bedrock:eu-central-1::foundation-model/amazon.nova-2-lite-v1:0"}
        ],
    }
    out = validar_perfil(data, account=account, region="eu-west-1", model_id=REFERENCE_MODEL)
    assert len(out["model_arns"]) == 2
    data["models"][0]["modelArn"] = data["models"][0]["modelArn"].replace(
        "eu-central-1", "us-east-1"
    )
    with pytest.raises(ValueError):
        validar_perfil(data, account=account, region="eu-west-1", model_id=REFERENCE_MODEL)


def test_primera_peticion_no_prueba_cold_y_report_si():
    rows = []
    for i in range(6):
        rows.append(
            {
                "status": 200,
                "http_duration_ms": 1000 + i,
                "body": {
                    "metadata": {
                        "execution": "real",
                        "request_id": f"req-{i}",
                        "first_in_environment": i == 0,
                    }
                },
            }
        )
    initial = resumir_mediciones(rows, [])
    assert initial["warm_observed"] == 5 and initial["cold_confirmed_by_report"] == 0
    report = parse_report(
        "REPORT RequestId: req-0\tDuration: 100.2 ms\tBilled Duration: 240 ms"
        "\tMemory Size: 512 MB\tMax Memory Used: 80 MB\tInit Duration: 139.8 ms"
    )
    assert report["duration_ms"] == 100.2 and report["init_ms"] == 139.8
    final = resumir_mediciones(rows, [report])
    assert final["cold_confirmed_by_report"] == 1 and final["five_warm_complete"]


def test_cli_mutacion_sin_execute_no_carga_cuenta(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["aws_s17", "medir"])
    monkeypatch.setattr(aws_s17, "ServerlessLab", lambda _: pytest.fail("No debe usar AWS"))
    aws_s17.main()
    assert "PLAN SIN RED" in capsys.readouterr().out


def test_costes_1000_no_confunden_unidades_ni_simulacion():
    data = json.loads(Path("datos/s17/costes-ejemplo.json").read_text())
    prices = json.loads(Path("docs/fuentes/tarifas-s17-2026-10-17.json").read_text())
    result = estimar(data, prices)
    assert result["total_usd"] == "0.4249"
    assert result["peticiones_ejecutadas_por_calculadora"] == 0
    fake = {"rows": [{"status": 200, "body": {"metadata": {"execution": "demo"}}}]}
    with pytest.raises(ValueError, match="No se mezclan"):
        incorporar_mediciones(data, fake, 0)


def test_version_publicada_cambia_si_cambia_configuracion_con_el_mismo_zip():
    artifact = {"sha256": "a" * 64}
    profile = {"profile_id": REFERENCE_MODEL}
    first = aws_s17.version_despliegue(artifact, profile, "plantilla-original")
    assert first == aws_s17.version_despliegue(artifact, profile, "plantilla-original")
    assert first != aws_s17.version_despliegue(artifact, profile, "plantilla-modificada")
    assert first != aws_s17.version_despliegue(
        artifact, {"profile_id": "eu.otro"}, "plantilla-original"
    )


def test_limpieza_no_borra_objetos_inesperados_aunque_bucket_sea_del_lab():
    class S3:
        def get_bucket_tagging(self, **kwargs):
            return {
                "TagSet": [
                    {"Key": "Project", "Value": "thepower-produccion-ia"},
                    {"Key": "Lab", "Value": "s17-prueba"},
                ]
            }

        def get_paginator(self, name):
            return self

        def paginate(self, **kwargs):
            return [{"Versions": [{"Key": "documento-ajeno.txt", "VersionId": "1"}]}]

        def delete_objects(self, **kwargs):
            pytest.fail("No puede borrar un objeto ajeno")

    lab = aws_s17.ServerlessLab.__new__(aws_s17.ServerlessLab)
    lab.args = SimpleNamespace(lab="s17-prueba")
    lab.stack = lambda name: None if name == "servicio" else {"StackId": "propio"}
    lab.outputs = lambda _: {"Bucket": "propio"}
    lab.client = lambda _: S3()
    with pytest.raises(ValueError, match="objetos ajenos"):
        lab.limpiar()
