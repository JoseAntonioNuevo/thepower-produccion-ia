"""Contratos HTTP relevantes: salud sin gasto, validación, rotulado y errores."""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from curso_ia.api import create_app
from curso_ia.config import Settings
from curso_ia.proveedores import ErrorProveedor


def test_demo_y_salud_no_confunden_simulacion_con_modelo(caplog):
    with TestClient(create_app(Settings(app_version="prueba-1"))) as client:
        health = client.get("/health").json()
        assert health["provider_check"] == "no_ejecutado"
        response = client.post(
            "/clasificar", json={"texto": "La factura ficticia tiene dos cobros"}
        )
        data = response.json()
        assert response.status_code == 200
        assert data["resultado"]["categoria"] == "facturacion"
        assert data["metadata"]["execution"] == "demo"
        assert data["metadata"]["consumo"]["coste_usd"] is None
        assert data["metadata"]["request_id"] == response.headers["x-request-id"]
        assert "La factura ficticia" not in caplog.text
        assert "prueba-1" in caplog.text


@pytest.mark.parametrize(
    "payload", [{"texto": ""}, {"texto": "x" * 2001}, {"texto": "Caso válido", "modelo": "otro"}]
)
def test_entrada_invalida_no_echo_del_texto(payload):
    with TestClient(create_app()) as client:
        response = client.post("/clasificar", json=payload)
        assert response.status_code == 422
        assert set(response.json()) == {"error", "request_id"}


def test_limite_de_bytes_antes_de_parsear():
    with TestClient(create_app()) as client:
        response = client.post("/clasificar", content=b"x" * 20000)
        assert response.status_code == 413


def test_real_sin_configuracion_no_arranca():
    with pytest.raises(ValidationError, match="Modo real requiere"):
        Settings(mode="real")


def test_salud_no_invoca_y_error_real_no_usa_demo():
    class Fallo:
        async def clasificar(self, texto):
            raise ErrorProveedor("proveedor_timeout", 504)

    cfg = Settings(mode="real", model_id="modelo-test", api_key="clave-sintetica")
    with TestClient(create_app(cfg, Fallo())) as client:
        assert client.get("/health").status_code == 200
        response = client.post("/clasificar", json={"texto": "Caso ficticio de acceso"})
        assert response.status_code == 504
        assert response.json()["error"] == "proveedor_timeout"
        assert "resultado" not in response.json()
