"""Montaje: construye una sola vez las piezas del agente y ofrece `conversar`.

Lo usan por igual la API (api.py), la línea de comandos (cli.py) y los tests, de modo que
los tres ejecutan exactamente el mismo agente.
"""

import json
import time
from dataclasses import dataclass

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from . import observabilidad
from .almacen import crear_almacen
from .cerebro import crear_cerebro
from .config import Config, cargar_config
from .grafo import construir_grafo
from .herramientas import crear_herramientas
from .investigacion import procesar_pendientes
from .prompts import INFORME
from .rag import crear_embeddings, ingestar


class ConversacionAjena(PermissionError):
    """El thread_id existe y pertenece a otro usuario."""


def crear_redactor(cfg: Config, cerebro):
    """Perfil real: el modelo redacta el informe con las evidencias YA reunidas (una llamada).

    En el perfil doble no hay redactor: el informe usa una plantilla y cuesta cero.
    """
    if cfg.perfil == "doble":
        return None

    def redactar(informe: dict) -> tuple[str, dict | None]:
        evidencias = {
            k: informe[k] for k in ("tema", "politica_interna", "informacion_publica", "faltan")
        }
        respuesta = cerebro.invoke(
            [
                SystemMessage(content=INFORME[cfg.prompt_version]),
                HumanMessage(content=json.dumps(evidencias, ensure_ascii=False)),
            ]
        )
        # usage_metadata trae los tokens si el proveedor los informa; None = desconocido.
        return str(respuesta.content), getattr(respuesta, "usage_metadata", None)

    return redactar


@dataclass
class Servicios:
    cfg: Config
    almacen: object
    embeddings: object
    cerebro: object
    grafo: object
    redactor: object = None

    def conversar(
        self, *, usuario: str, thread_id: str, mensaje: str, request_id: str | None = None
    ) -> dict:
        """Un turno completo: autoriza, ejecuta el grafo y resume lo ocurrido."""
        request_id = request_id or observabilidad.nuevo_request_id()
        # thread_id NO autoriza: se comprueba quién es el dueño antes de leer la memoria.
        if not self.almacen.asegurar_conversacion(thread_id, usuario):
            raise ConversacionAjena(thread_id)
        t0 = time.perf_counter()
        with observabilidad.turno(
            self.cfg, thread_id=thread_id, usuario=usuario, request_id=request_id
        ) as config:
            estado = self.grafo.invoke({"messages": [HumanMessage(content=mensaje)]}, config)
        salida = {
            "request_id": request_id,
            "thread_id": thread_id,
            "respuesta": str(estado["messages"][-1].content),
            "ruta": estado.get("ruta", []),
            "herramientas": estado.get("herramientas", []),
            "fuentes": estado.get("fuentes", []),
            "errores": estado.get("errores", []),
            "perfil": self.cfg.perfil,
            "modelo": self.cfg.modelo_chat,
            "prompt_version": self.cfg.prompt_version,
            "duracion_ms": round((time.perf_counter() - t0) * 1000),
        }
        observabilidad.anotar(
            "turno", **{k: v for k, v in salida.items() if k != "respuesta"}, usuario=usuario
        )
        return salida

    def historial(self, *, usuario: str, thread_id: str) -> list[dict]:
        if self.almacen.propietario(thread_id) != usuario:
            raise ConversacionAjena(thread_id)
        estado = self.grafo.get_state({"configurable": {"thread_id": thread_id}})
        visibles = [
            m
            for m in estado.values.get("messages", [])
            if isinstance(m, HumanMessage) or (isinstance(m, AIMessage) and m.content)
        ]
        return [
            {"rol": "usuario" if isinstance(m, HumanMessage) else "agente", "texto": str(m.content)}
            for m in visibles
        ]

    def investigar_pendientes(self) -> list[str]:
        """Lo que hace el ejecutor: toma los trabajos pendientes y los termina."""
        return procesar_pendientes(self.cfg, self.almacen, self.embeddings, self.redactor)

    def cerrar(self):
        self.almacen.cerrar()


def crear_servicios(cfg: Config | None = None, cerebro=None) -> Servicios:
    cfg = cfg or cargar_config()
    almacen = crear_almacen(cfg)
    embeddings = crear_embeddings(cfg)
    # En memoria no hay índice entre ejecuciones: se reconstruye al arrancar.
    if cfg.almacen == "memoria":
        ingestar(almacen, embeddings)
    cerebro = cerebro or crear_cerebro(cfg)
    herramientas = crear_herramientas(cfg, almacen, embeddings)
    grafo = construir_grafo(cfg, cerebro, herramientas, almacen.checkpointer())
    return Servicios(cfg, almacen, embeddings, cerebro, grafo, crear_redactor(cfg, cerebro))
