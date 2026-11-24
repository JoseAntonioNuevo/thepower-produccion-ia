"""Ampliación opcional: un agente correctivo (CRAG) en LangGraph, con decisiones y límite de llamadas.

No sustituye a los tests del RAG. Sirve para practicar cómo se prueba un AGENTE: no se
comprueba el texto final, sino las DECISIONES que toma, el camino que recorre y cuántas
llamadas gasta.

    START → recuperar ─┬─ responder ──→ END     (hay evidencia: el grafo del RAG genera)
                ↑      ├─ reformular ─┐          (sin evidencia y quedan intentos)
                └──────┼──────────────┘
                       └─ rechazar ───→ END     (sin evidencia y sin intentos)

Dos límites independientes:
1. `decidir` deja de reformular cuando se acaban los intentos (regla de negocio).
2. `recursion_limit` de LangGraph corta el grafo si una regla mal escrita entrase en bucle
   (red de seguridad del framework). Los tests comprueban los dos.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from rag.config import Config
from rag.consulta import MENSAJE_RECHAZO, Respuesta, recuperar, responder
from rag.proveedores import terminos

DECISIONES = ("responder", "reformular", "rechazar")


def decidir(mejor_similitud: float | None, umbral: float, intento: int, max_intentos: int) -> str:
    """Elige la acción según la evidencia y los intentos disponibles. Permite responder con respaldo,
    reformular mientras quede otro intento y rechazar al agotarlos."""
    if mejor_similitud is not None and mejor_similitud >= umbral:
        return "responder"
    return "reformular" if intento < max_intentos else "rechazar"


def reformular_doble(pregunta: str) -> str:
    """Extrae términos de la pregunta y elimina repeticiones conservando el orden para ensayar reintentos sin usar un LLM."""
    return " ".join(dict.fromkeys(terminos(pregunta)))


@dataclass
class Trayectoria:
    decisiones: list[str] = field(default_factory=list)
    consultas: list[str] = field(default_factory=list)
    ruta: list[str] = field(default_factory=list)  # nodos del grafo recorridos, en orden
    llamadas_recuperacion: int = 0
    llamadas_generacion: int = 0
    respuesta: Respuesta | None = None
    texto: str = MENSAJE_RECHAZO


class EstadoCrag(TypedDict, total=False):
    consulta: str
    intento: int
    decisiones: list[str]
    consultas: list[str]
    ruta: list[str]
    llamadas_recuperacion: int
    llamadas_generacion: int
    respuesta: Respuesta | None


def construir_crag(
    cfg: Config,
    almacen,
    proveedores,
    indice_id: str,
    reformular: Callable[[str], str] = reformular_doble,
    max_intentos: int = 2,
    regla: Callable[[float | None, float, int, int], str] = decidir,
):
    """Conecta búsqueda, reformulación, respuesta y rechazo en un grafo. Acepta una regla de decisión
    y un reformulador intercambiables para probar cómo se comporta el agente en cada intento."""

    def nodo_recuperar(e: EstadoCrag) -> EstadoCrag:
        """Busca con la consulta actual, aplica la regla y registra la decisión y el contador de búsquedas.
        Así se puede reconstruir la trayectoria del agente."""
        rec = recuperar(cfg, almacen, proveedores.embeddings, indice_id, e["consulta"])
        decision = regla(rec.mejor_similitud, cfg.umbral_evidencia, e["intento"], max_intentos)
        return {
            "consultas": [*e["consultas"], e["consulta"]],
            "decisiones": [*e["decisiones"], decision],
            "llamadas_recuperacion": e["llamadas_recuperacion"] + 1,
            "ruta": [*e["ruta"], "recuperar"],
        }

    def nodo_reformular(e: EstadoCrag) -> EstadoCrag:
        """Reescribe la consulta e incrementa el número de intento antes de volver a buscar."""
        return {"consulta": reformular(e["consulta"]), "intento": e["intento"] + 1, "ruta": [*e["ruta"], "reformular"]}

    def nodo_responder(e: EstadoCrag) -> EstadoCrag:
        """Ejecuta el RAG con la consulta que encontró evidencia y cuenta si llegó al generador
        para distinguir el coste de responder del coste de reintentar la búsqueda."""
        r = responder(cfg, almacen, proveedores, indice_id, e["consulta"])
        generacion = 0 if r.motivo_rechazo == "evidencia_insuficiente" else 1
        return {
            "respuesta": r,
            "llamadas_generacion": e["llamadas_generacion"] + generacion,
            "ruta": [*e["ruta"], "responder"],
        }

    def nodo_rechazar(e: EstadoCrag) -> EstadoCrag:
        """Añade el rechazo a la trayectoria y conduce al fin del grafo cuando se han agotado los intentos."""
        return {"ruta": [*e["ruta"], "rechazar"]}

    grafo = StateGraph(EstadoCrag)
    grafo.add_node("recuperar", nodo_recuperar)
    grafo.add_node("reformular", nodo_reformular)
    grafo.add_node("responder", nodo_responder)
    grafo.add_node("rechazar", nodo_rechazar)
    grafo.add_edge(START, "recuperar")
    grafo.add_conditional_edges("recuperar", lambda e: e["decisiones"][-1], {d: d for d in DECISIONES})
    grafo.add_edge("reformular", "recuperar")
    grafo.add_edge("responder", END)
    grafo.add_edge("rechazar", END)
    return grafo.compile()


def limite_pasos(max_intentos: int) -> int:
    """Calcula un límite de seguridad para LangGraph a partir del máximo de intentos, para cortar un posible bucle."""
    return 2 * max_intentos + 1


def crag(
    cfg: Config,
    almacen,
    proveedores,
    indice_id: str,
    pregunta: str,
    reformular: Callable[[str], str] = reformular_doble,
    max_intentos: int = 2,
    regla: Callable[[float | None, float, int, int], str] = decidir,
) -> Trayectoria:
    """Inicia el agente en el intento uno y ejecuta el grafo con un límite de pasos.
    Devuelve decisiones, llamadas y respuesta para comprobar cómo terminó cada consulta."""
    if max_intentos < 1:
        raise ValueError("max_intentos debe ser al menos 1")
    grafo = construir_crag(cfg, almacen, proveedores, indice_id, reformular, max_intentos, regla)
    inicial: EstadoCrag = {
        "consulta": pregunta,
        "intento": 1,
        "decisiones": [],
        "consultas": [],
        "ruta": [],
        "llamadas_recuperacion": 0,
        "llamadas_generacion": 0,
        "respuesta": None,
    }
    # recursion_limit: si la regla fallase y no dejase de reformular, LangGraph lanza
    # GraphRecursionError en lugar de seguir gastando llamadas.
    final = grafo.invoke(inicial, {"recursion_limit": limite_pasos(max_intentos)})
    respuesta = final.get("respuesta")
    return Trayectoria(
        decisiones=final["decisiones"],
        consultas=final["consultas"],
        ruta=final["ruta"],
        llamadas_recuperacion=final["llamadas_recuperacion"],
        llamadas_generacion=final["llamadas_generacion"],
        respuesta=respuesta,
        texto=respuesta.texto if respuesta else MENSAJE_RECHAZO,
    )
