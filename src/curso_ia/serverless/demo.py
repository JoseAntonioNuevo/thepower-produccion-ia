"""Dobles docentes explícitos: no acreditan ejecución de Bedrock o API Gateway."""

import json

from curso_ia.serverless.bedrock import TOOL_NAME


class DemoClient:
    """Respuesta fija sin tokens inventados; permite estudiar el contrato de Converse."""

    def converse(self, **request):
        return {
            "stopReason": "tool_use",
            "output": {
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "toolUse": {
                                "toolUseId": "demo-1",
                                "name": TOOL_NAME,
                                "input": {
                                    "categoria": "facturacion",
                                    "prioridad": "media",
                                    "respuesta": "Simulación S17: revisa la factura ficticia.",
                                },
                            }
                        }
                    ],
                }
            },
            "usage": {},
            "metrics": {},
        }


class DemoContext:
    aws_request_id = "00000000-0000-0000-0000-000000000017"
    function_version = "local-demo"

    def get_remaining_time_in_millis(self):
        return 24000


def event_for(text="Me han cobrado dos veces una factura ficticia"):
    """Evento compatible con la integración HTTP API v2; no incluye identidad IAM ficticia."""
    return {
        "version": "2.0",
        "rawPath": "/clasificar",
        "headers": {"content-type": "application/json"},
        "requestContext": {"http": {"method": "POST"}, "requestId": "demo-http"},
        "isBase64Encoded": False,
        "body": json.dumps({"texto": text}),
    }
