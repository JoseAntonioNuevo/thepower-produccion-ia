"""El grafo completo con el cerebro doble: rutas, límites, memoria y fallos controlados."""

from langchain_core.messages import AIMessage


def _usadas(r):
    return [h["nombre"] for h in r["herramientas"]]


def test_turno_directo_no_usa_herramientas(servicios):
    r = servicios.conversar(usuario="ana", thread_id="t1", mensaje="Hola, ¿qué puedes hacer?")
    assert _usadas(r) == [] and r["ruta"] == ["inicio", "agente"]


def test_ticket_pasa_por_el_servidor_mcp(servicios):
    r = servicios.conversar(usuario="ana", thread_id="t1", mensaje="¿Cómo está el ticket T-200?")
    assert _usadas(r) == ["consultar_ticket"] and r["fuentes"] == ["ticket:T-200"]
    assert r["ruta"] == ["inicio", "agente", "herramientas", "agente"]


def test_ticket_inexistente_se_dice_sin_inventar(servicios):
    r = servicios.conversar(usuario="ana", thread_id="t1", mensaje="Consulta el ticket T-999")
    assert "no existe" in r["respuesta"] and r["fuentes"] == []
    assert r["herramientas"][0]["ok"] is False


def test_respuesta_con_cita(servicios):
    r = servicios.conversar(
        usuario="ana", thread_id="t1", mensaje="¿Cuál es el límite de peticiones del plan Estándar?"
    )
    assert "120 peticiones por minuto" in r["respuesta"]
    assert "doc:03-limites-y-cuotas-api § Cuotas por plan de suscripción" in r["fuentes"]


def test_rechazo_cuando_no_consta(servicios):
    r = servicios.conversar(
        usuario="ana", thread_id="t1", mensaje="¿Cuál es la política de teletrabajo de los empleados?"
    )
    assert "No consta" in r["respuesta"] and r["fuentes"] == []


def test_limite_de_herramientas_por_turno(con_cfg):
    s = con_cfg(max_herramientas=1)
    r = s.conversar(
        usuario="ana", thread_id="t1", mensaje="Mira el ticket T-100 y consulta la política aplicable"
    )
    assert _usadas(r) == ["consultar_ticket"]  # la segunda ya no se ejecuta
    assert "T-100" in r["respuesta"]


def test_una_herramienta_inventada_por_el_modelo_no_ejecuta_nada(con_cfg):
    class CerebroQueInventa:
        def bind_tools(self, herramientas):
            return self

        def invoke(self, mensajes, config=None):
            if mensajes[-1].type == "tool":
                return AIMessage(content="No he podido hacerlo.")
            return AIMessage(
                content="",
                tool_calls=[
                    {"name": "borrar_base_de_datos", "args": {}, "id": "x1", "type": "tool_call"}
                ],
            )

    r = con_cfg(cerebro=CerebroQueInventa()).conversar(usuario="ana", thread_id="t1", mensaje="hola")
    assert r["errores"] == ["herramienta_desconocida"] and r["herramientas"][0]["ok"] is False


def test_un_fallo_del_modelo_devuelve_un_mensaje_controlado(con_cfg):
    class CerebroCaido:
        def bind_tools(self, herramientas):
            return self

        def invoke(self, mensajes, config=None):
            raise RuntimeError("cuerpo del proveedor con datos internos")

    r = con_cfg(cerebro=CerebroCaido()).conversar(usuario="ana", thread_id="t1", mensaje="hola")
    assert r["respuesta"] == "No puedo completar la consulta ahora."
    assert r["errores"] == ["modelo:RuntimeError"]  # la etiqueta, nunca el cuerpo del error


def test_memoria_por_hilo_e_hilos_independientes(servicios):
    servicios.conversar(usuario="ana", thread_id="hilo-a", mensaje="¿Cómo está el ticket T-200?")
    mismo = servicios.conversar(
        usuario="ana", thread_id="hilo-a", mensaje="¿Qué ticket estábamos viendo?"
    )
    otro = servicios.conversar(
        usuario="ana", thread_id="hilo-b", mensaje="¿Qué ticket estábamos viendo?"
    )
    assert "T-200" in mismo["respuesta"]
    assert "todavía no hemos visto" in otro["respuesta"]
