"""Ampliación opcional: un bucle correctivo (CRAG) con decisiones y límite de llamadas.

No sustituye a los tests del RAG. Sirve para practicar cómo se prueba un AGENTE: no se
comprueba el texto final, sino las DECISIONES que toma y cuántas llamadas gasta.

    recuperar → ¿evidencia suficiente? → responder
                      │ no
                      ├─ ¿quedan intentos? → reformular la consulta → recuperar
                      └─ no → rechazar
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rag.config import Config
from rag.consulta import MENSAJE_RECHAZO, Respuesta, recuperar, responder
from rag.proveedores import terminos

DECISIONES = ("responder", "reformular", "rechazar")


def decidir(mejor_similitud: float | None, umbral: float, intento: int, max_intentos: int) -> str:
    """Regla de enrutado. Pura y sin modelo: se prueba con una tabla de casos."""
    if mejor_similitud is not None and mejor_similitud >= umbral:
        return "responder"
    return "reformular" if intento < max_intentos else "rechazar"


def reformular_doble(pregunta: str) -> str:
    """Reformulador de prueba: deja solo las palabras con contenido. Uno real usaría un modelo."""
    return " ".join(dict.fromkeys(terminos(pregunta)))


@dataclass
class Trayectoria:
    decisiones: list[str] = field(default_factory=list)
    consultas: list[str] = field(default_factory=list)
    llamadas_recuperacion: int = 0
    llamadas_generacion: int = 0
    respuesta: Respuesta | None = None
    texto: str = MENSAJE_RECHAZO


def crag(
    cfg: Config, almacen, proveedores, indice_id: str, pregunta: str, reformular=reformular_doble, max_intentos: int = 2
) -> Trayectoria:
    """Como mucho `max_intentos` recuperaciones y UNA generación. Nunca un bucle sin límite."""
    if max_intentos < 1:
        raise ValueError("max_intentos debe ser al menos 1")
    t, consulta = Trayectoria(), pregunta
    for intento in range(1, max_intentos + 1):
        t.consultas.append(consulta)
        rec = recuperar(cfg, almacen, proveedores.embeddings, indice_id, consulta)
        t.llamadas_recuperacion += 1
        decision = decidir(rec.mejor_similitud, cfg.umbral_evidencia, intento, max_intentos)
        t.decisiones.append(decision)
        if decision == "responder":
            # Se responde a la pregunta ORIGINAL con la consulta que encontró evidencia.
            t.respuesta = responder(cfg, almacen, proveedores, indice_id, consulta)
            t.llamadas_generacion += 0 if t.respuesta.motivo_rechazo == "evidencia_insuficiente" else 1
            t.texto = t.respuesta.texto
            return t
        if decision == "rechazar":
            return t
        consulta = reformular(consulta)
    return t
