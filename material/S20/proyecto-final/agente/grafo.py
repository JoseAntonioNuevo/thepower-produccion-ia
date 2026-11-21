"""PASO 4 · El grafo: el agente como máquina de estados (LangGraph).

        START -> inicio -> agente --(pide herramientas)--> herramientas
                              ^                                  |
                              +----------------------------------+
                           agente --(responde)--> END

- `inicio`        reinicia los contadores del turno (no los mensajes: esos son la memoria).
- `agente`        llama al cerebro con el historial. Devuelve una respuesta o peticiones.
- `herramientas`  ejecuta las peticiones respetando la lista blanca y el límite por turno.

El checkpointer guarda el estado por `thread_id` al terminar cada nodo: por eso la
conversación continúa en otro proceso si el checkpointer es PostgreSQL.
"""

import json
import time
from typing import Annotated, Required, TypedDict

from langchain_core.messages import AIMessage, AnyMessage, SystemMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph, add_messages

from .config import Config
from .herramientas import fuentes_de
from .prompts import prompt_sistema


class Estado(TypedDict, total=False):
    # add_messages AÑADE al historial en vez de sustituirlo: es la memoria de la conversación.
    messages: Required[Annotated[list[AnyMessage], add_messages]]
    # Los campos siguientes describen solo el turno actual y se reinician en `inicio`.
    llamadas: int  # herramientas ejecutadas en este turno
    ruta: list[str]  # nodos recorridos, para poder explicar el turno
    herramientas: list[dict]  # registro: nombre, ok y milisegundos
    fuentes: list[str]  # de dónde sale cada dato de la respuesta
    errores: list[str]  # etiquetas de fallos controlados (sin datos sensibles)


def construir_grafo(cfg: Config, cerebro, herramientas: list, checkpointer=None):
    """Recibe sus dependencias ya construidas: en los tests se inyectan dobles."""
    por_nombre = {h.name: h for h in herramientas}
    con_herramientas = cerebro.bind_tools(herramientas)
    sistema = SystemMessage(content=prompt_sistema(cfg.prompt_version))

    def inicio(estado: Estado):
        return {"llamadas": 0, "ruta": ["inicio"], "herramientas": [], "fuentes": [], "errores": []}

    def agente(estado: Estado, config: RunnableConfig):
        # Agotado el presupuesto, se llama al cerebro SIN herramientas: tiene que responder ya.
        agotado = estado.get("llamadas", 0) >= cfg.max_herramientas
        modelo = cerebro if agotado else con_herramientas
        try:
            respuesta = modelo.invoke([sistema, *estado["messages"]], config)
        except Exception as exc:
            # Nunca se devuelve el error del proveedor: puede contener datos sensibles.
            return {
                "messages": [AIMessage(content="No puedo completar la consulta ahora.")],
                "ruta": [*estado.get("ruta", []), "agente"],
                "errores": [*estado.get("errores", []), f"modelo:{type(exc).__name__}"],
            }
        if agotado and getattr(respuesta, "tool_calls", None):
            respuesta = AIMessage(
                content="He alcanzado el límite de herramientas de este turno. "
                "Acota la consulta y vuelve a preguntar."
            )
        return {"messages": [respuesta], "ruta": [*estado.get("ruta", []), "agente"]}

    def ejecutar_herramientas(estado: Estado, config: RunnableConfig):
        llamadas = estado.get("llamadas", 0)
        registro = list(estado.get("herramientas", []))
        fuentes = list(estado.get("fuentes", []))
        errores = list(estado.get("errores", []))
        resultados = []
        for peticion in estado["messages"][-1].tool_calls:
            nombre, t0 = peticion["name"], time.perf_counter()
            if llamadas >= cfg.max_herramientas:
                cuerpo, ok = json.dumps({"ok": False, "error": "limite_de_herramientas"}), False
                errores.append("limite_de_herramientas")
            elif nombre not in por_nombre:
                # El modelo solo puede usar el catálogo: un nombre inventado no ejecuta nada.
                cuerpo, ok = json.dumps({"ok": False, "error": "herramienta_desconocida"}), False
                errores.append("herramienta_desconocida")
            else:
                llamadas += 1  # el intento cuenta aunque falle
                try:
                    cuerpo = por_nombre[nombre].invoke(peticion["args"], config)
                    datos = json.loads(cuerpo)
                    ok = bool(datos.get("ok", True))
                    fuentes += [f for f in fuentes_de(nombre, datos) if f not in fuentes]
                except Exception as exc:
                    cuerpo = json.dumps(
                        {"ok": False, "error": type(exc).__name__, "detalle": str(exc)[:120]},
                        ensure_ascii=False,
                    )
                    ok = False
                    errores.append(f"{nombre}:{type(exc).__name__}")
            registro.append({"nombre": nombre, "ok": ok, "ms": round((time.perf_counter() - t0) * 1000)})
            # Cada petición recibe su ToolMessage, también si se rechazó.
            resultados.append(ToolMessage(content=cuerpo, tool_call_id=peticion["id"], name=nombre))
        return {
            "messages": resultados,
            "llamadas": llamadas,
            "herramientas": registro,
            "fuentes": fuentes,
            "errores": errores,
            "ruta": [*estado.get("ruta", []), "herramientas"],
        }

    def siguiente(estado: Estado):
        return "herramientas" if getattr(estado["messages"][-1], "tool_calls", None) else END

    grafo = StateGraph(Estado)
    grafo.add_node("inicio", inicio)
    grafo.add_node("agente", agente)
    grafo.add_node("herramientas", ejecutar_herramientas)
    grafo.add_edge(START, "inicio")
    grafo.add_edge("inicio", "agente")
    grafo.add_conditional_edges("agente", siguiente, {"herramientas": "herramientas", END: END})
    grafo.add_edge("herramientas", "agente")
    return grafo.compile(checkpointer=checkpointer)
