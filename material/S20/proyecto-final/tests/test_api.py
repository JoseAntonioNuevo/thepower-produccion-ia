"""La API: identidad, propiedad de la conversación, validación y salud."""

import pytest
from fastapi.testclient import TestClient

from agente.api import crear_app
from agente.investigacion import procesar_pendientes

ANA = {"Authorization": "Bearer token-ana"}
LUIS = {"Authorization": "Bearer token-luis"}


@pytest.fixture
def cliente(servicios):
    with TestClient(crear_app(servicios)) as c:
        yield c


def test_health_no_llama_al_modelo(con_cfg):
    class CerebroProhibido:
        def bind_tools(self, herramientas):
            return self

        def invoke(self, mensajes, config=None):
            raise AssertionError("/health no debe invocar al modelo")

    with TestClient(crear_app(con_cfg(cerebro=CerebroProhibido()))) as c:
        r = c.get("/health")
    assert r.status_code == 200
    assert r.json() == {
        "estado": "ok",
        "version": "0.1.0",
        "perfil": "doble",
        "almacen": "memoria",
        "fragmentos": 20,
    }


def test_sin_token_no_hay_conversacion(cliente):
    r = cliente.post("/chat", json={"thread_id": "t1", "mensaje": "hola"})
    assert r.status_code == 401


def test_chat_devuelve_respuesta_ruta_y_fuentes(cliente):
    r = cliente.post(
        "/chat", headers=ANA, json={"thread_id": "t1", "mensaje": "Estado del ticket T-300"}
    )
    cuerpo = r.json()
    assert r.status_code == 200 and cuerpo["fuentes"] == ["ticket:T-300"]
    assert cuerpo["perfil"] == "doble" and cuerpo["prompt_version"] == "v1" and cuerpo["request_id"]


def test_thread_id_no_autoriza_a_otro_usuario(cliente):
    cliente.post(
        "/chat", headers=ANA, json={"thread_id": "privado", "mensaje": "Estado del ticket T-100"}
    )
    assert (
        cliente.post("/chat", headers=LUIS, json={"thread_id": "privado", "mensaje": "hola"}).status_code
        == 404
    )
    assert cliente.get("/conversaciones/privado", headers=LUIS).status_code == 404
    historial = cliente.get("/conversaciones/privado", headers=ANA).json()["mensajes"]
    assert [m["rol"] for m in historial] == ["usuario", "agente"]


@pytest.mark.parametrize(
    "cuerpo",
    [
        {"thread_id": "con espacios", "mensaje": "hola"},
        {"thread_id": "t1", "mensaje": ""},
        {"thread_id": "t1", "mensaje": "hola", "usuario": "luis"},  # la identidad no viaja en el cuerpo
    ],
)
def test_entrada_invalida_se_rechaza_antes_del_agente(cliente, cuerpo):
    assert cliente.post("/chat", headers=ANA, json=cuerpo).status_code == 422


def test_investigacion_solo_la_lee_su_propietario_y_leer_no_crea_trabajo(cliente, servicios):
    cliente.post(
        "/chat",
        headers=ANA,
        json={"thread_id": "inv", "mensaje": "Mira el ticket T-100 e investiga la tecnología implicada"},
    )
    trabajo_id = procesar_pendientes(servicios.cfg, servicios.almacen, servicios.embeddings)[0]
    for _ in range(3):  # consultar tres veces el estado
        r = cliente.get(f"/investigaciones/{trabajo_id}", headers=ANA)
    assert r.status_code == 200 and r.json()["estado"] == "completo"
    assert cliente.get(f"/investigaciones/{trabajo_id}", headers=LUIS).status_code == 404
    assert procesar_pendientes(servicios.cfg, servicios.almacen, servicios.embeddings) == []


def test_en_aws_la_url_de_la_base_se_compone_con_la_clave_del_secreto(monkeypatch):
    from agente.config import cargar_config

    monkeypatch.delenv("S20_DATABASE_URL", raising=False)
    monkeypatch.setenv("S20_DB_HOST", "base.interna")
    monkeypatch.setenv("S20_DB_PASSWORD", "c/l@ve:rara")  # caracteres que rompen una URL
    cfg = cargar_config()
    assert cfg.database_url == "postgresql://s20:c%2Fl%40ve%3Arara@base.interna:5432/s20_agente"
    assert "database_url" not in cfg.publica()  # la URL con contraseña nunca sale en evidencias
