"""Del grafo a la pantalla: cada paso del grafo de consulta se convierte en filas del chat.

Sin I/O y sin OpenTUI: se prueba en `tests/test_tui.py` sin terminal. La TUI
(`ui/rag_tui.py`) solo pinta lo que devuelven estas funciones.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count
from typing import Literal

from evaluacion.metricas import evaluar_caso
from rag.consulta import Respuesta
from rag.grafo import hay_evidencia

# Papeles que la TUI sabe pintar. human/bot/rechazo/error son globos; paso/dato/criterio, trazas.
Kind = Literal["human", "paso", "dato", "bot", "rechazo", "criterio", "error", "hint"]

_claves = count(1)


@dataclass(frozen=True)
class ChatLine:
    """Una fila del chat: tipo visual, texto y clave estable para que OpenTUI reconcilie la lista."""

    kind: Kind
    text: str
    key: str = field(default_factory=lambda: f"fila-{next(_claves)}")


def _num(valor: float | None, decimales: int = 4) -> str:
    return "sin dato" if valor is None else f"{valor:.{decimales}f}".replace(".", ",")


def _usd(valor: float | None) -> str:
    return "sin dato" if valor is None else f"{valor:.6f} USD".replace(".", ",")


def _tokens(entrada: int | None, salida: int | None) -> str:
    return "sin dato" if entrada is None or salida is None else f"{entrada} → {salida}"


def lineas_de_paso(paso: dict, umbral: float, modelo: str) -> list[ChatLine]:
    """Filas para UN paso del grafo (`{"nodo": cambios}`), en el momento en que termina."""
    nodo, cambios = next(iter(paso.items()))
    if nodo == "recuperar":
        rec = cambios["recuperacion"]
        evidencia = bool(rec.hallazgos) and hay_evidencia(rec.mejor_similitud, umbral)
        signo, siguiente = ("≥", "generar") if evidencia else ("<", "rechazo previo")
        documentos = "\n".join(f"{i}. {doc}" for i, doc in enumerate(rec.documentos, 1)) or "ninguno"
        return [
            ChatLine(
                "paso",
                f"recuperar · mejor similitud {_num(rec.mejor_similitud)} {signo} umbral {_num(umbral)} → {siguiente}",
            ),
            ChatLine("dato", f"documentos recuperados (hasta 5 distintos)\n{documentos}"),
        ]
    if nodo == "rechazo_previo":
        return [
            ChatLine("paso", "rechazo previo · no se llama al modelo · 0 tokens · 0 USD"),
            ChatLine("rechazo", cambios["respuesta"].texto + "\n\n_(evidencia insuficiente: rechazo previo)_"),
        ]
    if nodo == "generar":
        g = cambios["generacion"]
        servido = f" · servido por {g.proveedor_servido}" if g.proveedor_servido else ""
        return [
            ChatLine(
                "paso",
                f"generar · {g.model_version or modelo}{servido} · tokens {_tokens(g.tokens_entrada, g.tokens_salida)}",
            )
        ]
    if nodo == "comprobar":
        r: Respuesta = cambios["respuesta"]
        if r.rechazo:
            return [
                ChatLine("paso", "comprobar · el modelo leyó los fragmentos y dice que no consta → rechazo del modelo"),
                ChatLine("rechazo", r.texto + "\n\n_(rechazo del modelo: sí se llamó y se pagó)_"),
            ]
        avisos = ", ".join(r.avisos) if r.avisos else "ninguno"
        fuentes = ", ".join(r.fuentes) if r.fuentes else "ninguna"
        return [
            ChatLine("paso", f"comprobar · fuentes citadas: {fuentes} · avisos: {avisos}"),
            ChatLine("bot", r.texto),
        ]
    return []


def resumen_turno(r: Respuesta) -> ChatLine:
    """Latencia, tokens y coste de la consulta completa (lo mismo que llega a Langfuse)."""
    lat = r.latencia_ms or {}
    segundos = (lat.get("total") or 0) / 1000
    tokens = _tokens((r.tokens or {}).get("entrada"), (r.tokens or {}).get("salida"))
    return ChatLine(
        "hint",
        f"total {segundos:.2f} s (recuperar {lat.get('recuperacion', 0):.0f} ms · generar "
        f"{lat.get('generacion', 0):.0f} ms) · tokens {tokens} · coste {_usd(r.coste_usd)}".replace(".", ","),
    )


def fila_de_respuesta(r: Respuesta) -> dict:
    """Los campos que `evaluar_caso` necesita, con los mismos nombres que `respuestas.jsonl`."""
    return {
        "response": r.texto,
        "rechazo": r.rechazo,
        "fuentes": r.fuentes,
        "documentos_recuperados": r.documentos_recuperados,
        "error": None,
    }


def lineas_de_criterio(caso: dict, r: Respuesta) -> list[ChatLine]:
    """Para una pregunta del test: qué dice el criterio fijado de antemano y la referencia."""
    e = evaluar_caso(caso, fila_de_respuesta(r))
    if caso["respondible"]:
        if e["acierto"]:
            veredicto = "✓ acierto: datos clave presentes y cita un documento de referencia"
        elif e["abstencion_incorrecta"]:
            veredicto = "✗ se abstuvo en una pregunta respondible (abstención incorrecta)"
        elif e["datos_clave_ausentes"]:
            veredicto = "✗ faltan datos clave: " + ", ".join(e["datos_clave_ausentes"])
        else:
            veredicto = "✗ no cita ningún documento de referencia"
        detalle = (
            f"recall@5 {_num(e['recall_at_5'], 2)} · precision@5 {_num(e['precision_at_5'], 2)}\n"
            f"referencia: {caso['respuesta_referencia']}\n"
            f"documentos de referencia: {', '.join(caso['documentos_relevantes'])}"
        )
    else:
        veredicto = "✓ rechazo correcto" if e["rechazo_correcto"] else "✗ respondió una pregunta sin respuesta"
        detalle = f"no tiene respuesta en el corpus: {caso['motivo_sin_respuesta']}"
    return [ChatLine("criterio", f"{caso['caso_id']} · {veredicto}\n{detalle}")]


AYUDA = """Comandos:
  1 … 7            preguntas del guion del directo (T01, T13, T12, T14, T15, T17, T08)
  T01 … T20        cualquier pregunta del test, con su criterio y su referencia
  /casos           lista las preguntas del test
  /perfil          lista los archivos .env.*; /perfil sol-opus carga .env.sol-opus
  /config A|B      fragmentos de 320 (A) o de 900 (B); también MH|MS
  /ayuda           esta ayuda · salir o esc para terminar
Cualquier otro texto se pregunta tal cual al RAG. El juez de Ragas no actúa aquí: se aplica
a los lotes (`s19.py lote` y después `evaluador/evaluar.py`)."""

# Orden de las preguntas del directo de clase: una de cada tipo de caso (fácil, dos documentos,
# contexto incompleto, criterio frágil, rechazo del modelo, rechazo previo, fragmentación).
GUION = ("T01", "T13", "T12", "T14", "T15", "T17", "T08")


def lista_de_casos(casos: list[dict]) -> str:
    filas = []
    for c in casos:
        marca = "con respuesta" if c["respondible"] else "SIN respuesta"
        filas.append(f"{c['caso_id']} · {marca} · {c['pregunta']}")
    return "\n".join(filas)
