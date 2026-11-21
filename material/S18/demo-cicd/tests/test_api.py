"""Tests de la API. Ninguno usa la red ni una clave: el proveedor se sustituye por un doble.

Los tres casos que pide la práctica están marcados: entrada inválida, respuesta
válida y fallo del proveedor.
"""

import asyncio
import json

import httpx
import pytest
from fastapi.testclient import TestClient

from app import Clasificacion, ErrorProveedor, ProveedorOpenRouter, crear_app


class DobleCorrecto:
    """Responde siempre lo mismo y cuenta cuántas veces lo llaman."""

    modelo = "doble-de-test"

    def __init__(self):
        self.llamadas = 0

    async def clasificar(self, texto: str) -> Clasificacion:
        self.llamadas += 1
        return Clasificacion(
            categoria="acceso", prioridad="media", respuesta="Restablece el acceso."
        )


class DobleCaido:
    """Simula que el proveedor no responde a tiempo."""

    modelo = "doble-de-test"

    async def clasificar(self, texto: str) -> Clasificacion:
        raise ErrorProveedor("proveedor_timeout", 504)


class DobleRoto:
    """Simula un error de programación que nadie previó."""

    modelo = "doble-de-test"

    async def clasificar(self, texto: str) -> Clasificacion:
        raise RuntimeError("detalle interno que no debe salir")


def lineas_de_log(salida: str) -> list[dict]:
    return [json.loads(linea) for linea in salida.splitlines() if linea.startswith("{")]


# ------------------------------------------------------------------ salud
def test_health_responde_sin_llamar_al_proveedor(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "commit-de-prueba")
    doble = DobleCorrecto()
    with TestClient(crear_app(doble)) as cliente:
        respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok", "version": "commit-de-prueba", "modo": "doble"}
    assert doble.llamadas == 0


# ------------------------------------------------- caso 1: respuesta válida
def test_respuesta_valida():
    doble = DobleCorrecto()
    with TestClient(crear_app(doble)) as cliente:
        respuesta = cliente.post("/clasificar", json={"texto": "No puedo entrar en mi cuenta"})
    datos = respuesta.json()
    assert respuesta.status_code == 200
    assert datos["resultado"] == {
        "categoria": "acceso",
        "prioridad": "media",
        "respuesta": "Restablece el acceso.",
    }
    assert datos["modelo"] == "doble-de-test"
    assert datos["request_id"] == respuesta.headers["x-request-id"]
    assert doble.llamadas == 1


# ------------------------------------------------- caso 2: entrada inválida
@pytest.mark.parametrize(
    "cuerpo",
    [{"texto": ""}, {"texto": "x" * 1001}, {}, {"texto": 7}, {"mensaje": "campo equivocado"}],
)
def test_entrada_invalida_devuelve_422_sin_llamar_al_proveedor(cuerpo):
    doble = DobleCorrecto()
    with TestClient(crear_app(doble)) as cliente:
        respuesta = cliente.post("/clasificar", json=cuerpo)
    assert respuesta.status_code == 422
    assert set(respuesta.json()) == {"error", "request_id"}
    assert respuesta.json()["error"] == "entrada_invalida"
    assert doble.llamadas == 0


# ---------------------------------------------- caso 3: fallo del proveedor
def test_fallo_del_proveedor_devuelve_error_y_no_inventa_una_respuesta():
    with TestClient(crear_app(DobleCaido())) as cliente:
        respuesta = cliente.post("/clasificar", json={"texto": "Caso ficticio de acceso"})
    assert respuesta.status_code == 504
    assert respuesta.json()["error"] == "proveedor_timeout"
    assert "resultado" not in respuesta.json()


def test_error_no_previsto_devuelve_500_sin_detalles_internos(capsys):
    with TestClient(crear_app(DobleRoto())) as cliente:
        respuesta = cliente.post("/clasificar", json={"texto": "Caso ficticio"})
    assert respuesta.status_code == 500
    assert respuesta.json() == {
        "error": "error_interno",
        "request_id": respuesta.headers["x-request-id"],
    }
    registros = lineas_de_log(capsys.readouterr().out)
    excepcion = next(r for r in registros if r["evento"] == "excepcion")
    assert excepcion["error_tipo"] == "RuntimeError"
    assert excepcion["request_id"] == respuesta.headers["x-request-id"]


# -------------------------------------------------------------------- logs
def test_el_log_identifica_la_peticion_y_no_contiene_el_texto(monkeypatch, capsys):
    monkeypatch.setenv("APP_VERSION", "commit-de-prueba")
    with TestClient(crear_app(DobleCorrecto())) as cliente:
        respuesta = cliente.post("/clasificar", json={"texto": "Texto privado del usuario"})
    salida = capsys.readouterr().out
    peticion = next(r for r in lineas_de_log(salida) if r["evento"] == "peticion")
    assert peticion["request_id"] == respuesta.headers["x-request-id"]
    assert peticion["version"] == "commit-de-prueba"
    assert peticion["ruta"] == "/clasificar"
    assert peticion["estado"] == 200
    assert peticion["duracion_ms"] >= 0
    assert peticion["proveedor_ms"] >= 0
    assert "Texto privado" not in salida


def test_el_log_de_un_fallo_guarda_el_codigo_y_el_estado(capsys):
    with TestClient(crear_app(DobleCaido())) as cliente:
        cliente.post("/clasificar", json={"texto": "Caso ficticio"})
    peticion = next(r for r in lineas_de_log(capsys.readouterr().out) if r["evento"] == "peticion")
    assert (peticion["nivel"], peticion["estado"], peticion["error"]) == (
        "ERROR",
        504,
        "proveedor_timeout",
    )


# --------------------------------------------------- configuración por entorno
@pytest.mark.parametrize(
    ("texto", "categoria", "prioridad"),
    [
        ("No puedo entrar en mi cuenta ficticia", "acceso", "media"),
        ("Me han cobrado dos veces una factura ficticia", "facturacion", "media"),
        ("El servicio está caído para todos", "tecnico", "alta"),
    ],
)
def test_modo_demo_clasifica_con_reglas_y_lo_indica(monkeypatch, texto, categoria, prioridad):
    monkeypatch.delenv("API_MODE", raising=False)
    with TestClient(crear_app()) as cliente:
        datos = cliente.post("/clasificar", json={"texto": texto}).json()
    assert datos["modo"] == "demo"
    assert (datos["resultado"]["categoria"], datos["resultado"]["prioridad"]) == (
        categoria,
        prioridad,
    )


def test_modo_real_sin_clave_no_arranca(monkeypatch):
    monkeypatch.setenv("API_MODE", "real")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        crear_app()


def test_modo_desconocido_no_arranca(monkeypatch):
    monkeypatch.setenv("API_MODE", "produccion")
    with pytest.raises(RuntimeError, match="demo o real"):
        crear_app()


# ------------------------------------- adaptador real con respuestas simuladas
def respuesta_del_proveedor(texto_json: str) -> dict:
    return {
        "model": "modelo-simulado",
        "output": [
            {"type": "reasoning", "summary": []},
            {"type": "message", "content": [{"type": "output_text", "text": texto_json}]},
        ],
    }


def llamar_al_adaptador(manejador) -> tuple[Clasificacion, list[httpx.Request]]:
    """Ejecuta el adaptador real contra un transporte simulado: cero llamadas de pago."""
    peticiones: list[httpx.Request] = []

    def transporte(peticion: httpx.Request) -> httpx.Response:
        peticiones.append(peticion)
        return manejador(peticion)

    async def ejecutar():
        async with httpx.AsyncClient(transport=httpx.MockTransport(transporte)) as cliente:
            proveedor = ProveedorOpenRouter("clave-sintetica", "modelo-simulado", "", cliente)
            return await proveedor.clasificar("No puedo entrar")

    return asyncio.run(ejecutar()), peticiones


def test_adaptador_envia_una_peticion_y_valida_la_respuesta():
    valida = json.dumps({"categoria": "acceso", "prioridad": "alta", "respuesta": "Revisa."})
    resultado, peticiones = llamar_al_adaptador(
        lambda _: httpx.Response(200, json=respuesta_del_proveedor(valida))
    )
    assert resultado.prioridad == "alta"
    assert len(peticiones) == 1
    assert peticiones[0].url == "https://openrouter.ai/api/v1/responses"
    cuerpo = json.loads(peticiones[0].content)
    assert cuerpo["model"] == "modelo-simulado"
    assert "provider" not in cuerpo


@pytest.mark.parametrize(
    ("respuesta", "codigo", "estado"),
    [
        (httpx.Response(500, text="detalle remoto"), "proveedor_http", 502),
        (httpx.Response(401, text="clave rechazada"), "proveedor_http", 502),
        (httpx.Response(429), "proveedor_limitado", 503),
        (httpx.Response(200, text="esto no es JSON"), "respuesta_invalida", 502),
        (
            httpx.Response(200, json=respuesta_del_proveedor('{"categoria": "inventada"}')),
            "respuesta_invalida",
            502,
        ),
    ],
)
def test_adaptador_convierte_los_fallos_en_errores_controlados(respuesta, codigo, estado):
    peticiones: list[httpx.Request] = []

    def manejador(peticion: httpx.Request) -> httpx.Response:
        peticiones.append(peticion)
        return respuesta

    with pytest.raises(ErrorProveedor) as error:
        llamar_al_adaptador(manejador)
    assert (error.value.codigo, error.value.estado) == (codigo, estado)
    assert "detalle remoto" not in str(error.value)
    assert len(peticiones) == 1  # sin reintentos automáticos


def test_adaptador_convierte_el_timeout_en_504():
    def manejador(peticion: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("detalle privado", request=peticion)

    with pytest.raises(ErrorProveedor) as error:
        llamar_al_adaptador(manejador)
    assert (error.value.codigo, error.value.estado) == ("proveedor_timeout", 504)
