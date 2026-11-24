"""Chat del RAG en la terminal (`python s19.py chat`), con la TUI de S5/S6.

A la izquierda, el chat: la pregunta, cada paso del grafo al terminar (recuperar, generar,
comprobar o rechazo previo), la respuesta con sus fuentes y, si la pregunta es del test, lo
que dice el criterio fijado de antemano. A la derecha, el grafo con el nodo activo y los
datos que se vigilan: similitud frente al umbral, latencia, tokens y coste.

Como en S5/S6: cada mensaje ejecuta el grafo UNA vez en un hilo aparte; el hilo encola los
cambios y OpenTUI los pinta. La lógica (comandos, perfiles, trazas) está en `ui/motor.py`.
"""

from __future__ import annotations

import asyncio
import sys
import threading

from opentui import Box, Signal, Text, render, use_renderer

from rag.grafo import hay_evidencia
from ui.lineas import AYUDA, ChatLine, lineas_de_criterio, lineas_de_paso, resumen_turno
from ui.motor import MotorChat, Orden
from ui.tui import ACTIVE, BRIGHT, DATO, DIM, SURFACE, TOOL, ColaUI, build_app

# Filas del dibujo del grafo: (texto, nodo cuyo estado colorea la fila o None).
_DIBUJO = (
    ("{m} START", None),
    ("│", None),
    ("{m} recuperar", "recuperar"),
    ("├─ ≥ umbral ─▶ {m} generar", "generar"),
    ("│              │", None),
    ("│              {m} comprobar ─▶ END", "comprobar"),
    ("│", None),
    ("└─ < umbral ─▶ {m} rechazo previo", "rechazo_previo"),
    ("                 ─▶ END  (sin modelo)", None),
)


def _marca(nodo: str | None, estado: dict) -> str:
    if nodo is None:
        return "○"
    if estado.get("activo") == nodo:
        return "◉"
    return "●" if nodo in estado.get("ruta", []) else "○"


def _color(nodo: str | None, estado: dict) -> str:
    if nodo is None:
        return DIM
    if estado.get("activo") == nodo:
        return ACTIVE
    return DATO if nodo in estado.get("ruta", []) else DIM


class RagTUI:
    def __init__(self, motor: MotorChat):
        self.motor = motor
        self.cola = ColaUI()
        self.busy = Signal(False, name="busy")
        self.status = Signal("listo", name="status")
        self.turnos = Signal(0, name="turnos")
        self.grafo = Signal({"activo": None, "ruta": []}, name="grafo")
        self.info = Signal(self._texto_info(), name="info")
        self.ultimo = Signal("Aún no hay consultas.", name="ultimo")
        inicio = [ChatLine("hint", AYUDA)]
        if motor.cfg.perfil == "doble":
            inicio.append(
                ChatLine("hint", "⚠ PERFIL DOBLE: embeddings por hash y generador extractivo. NO mide ningún modelo.")
            )
        self.lines = Signal(inicio, name="lines")
        self._hilo: threading.Thread | None = None

    # ------------------------------------------------------------ pintado
    def _append(self, filas: list[ChatLine]) -> None:
        if filas:
            self.lines.set([*self.lines(), *filas])

    def _texto_info(self) -> str:
        m, c = self.motor, self.motor.cfg
        langfuse = f"on · sesión {m.sesion}" if m.trazador.activo else "off"
        umbral = f"{c.umbral_evidencia:.4f}".replace(".", ",")
        return (
            f"perfil   {m.perfil} ({c.perfil})\n"
            f"genera   {c.gen_modelo}\n"
            f"juez     {m.juez}\n"
            f"config   {m.config_id} · fragmentos {c.chunk_size}\n"
            f"corpus   {m.corpus}\n"
            f"umbral   {umbral}\n"
            f"langfuse {langfuse}"
        )

    def _sidebar(self) -> Box:
        filas = [
            Text(
                lambda t=texto, n=nodo: t.format(m=_marca(n, self.grafo())),
                fg=self.grafo.map(lambda e, n=nodo: _color(n, e)),
                wrap_mode="none",
            )
            for texto, nodo in _DIBUJO
        ]
        return Box(
            Text("Grafo de consulta · LangGraph", fg=BRIGHT, bold=True),
            *filas,
            Text(" ", fg=DIM),
            Text(lambda: self.info(), fg=DIM, wrap_mode="word"),
            Text(" ", fg=DIM),
            Text("última consulta", fg=TOOL, bold=True),
            Text(lambda: self.ultimo(), fg=BRIGHT, wrap_mode="word"),
            flex_direction="column",
            gap=0,
            width=44,
            flex_shrink=0,
            border=True,
            border_style="round",
            background_color=SURFACE,
            padding=1,
            title="recorrido",
        )

    def _subtitulo(self) -> str:
        self.info()  # leer la señal hace que la cabecera se repinte al cambiar de perfil o de config
        return f"{self.motor.perfil} · {self.motor.cfg.gen_modelo} · config {self.motor.config_id}"

    # ------------------------------------------------------------ entrada
    def submit(self, texto: str) -> None:
        if self.busy():
            return
        orden: Orden = self.motor.interpretar(texto)
        if orden.tipo == "salir":
            self.quit()
            return
        if orden.tipo != "pregunta":
            self._append(self.motor.comando(orden))
            self.info.set(self._texto_info())
            return
        etiqueta = f"{orden.caso['caso_id']} · " if orden.caso else ""
        self._append([ChatLine("human", etiqueta + orden.pregunta)])
        self.busy.set(True)
        self.turnos.set(self.turnos() + 1)
        self.status.set("recuperar…")
        self.grafo.set({"activo": "recuperar", "ruta": []})
        self._hilo = threading.Thread(target=self._turno, args=(orden,), daemon=True)
        self._hilo.start()

    # ------------------------------------------------------------ hilo del grafo
    def _al_paso(self, paso: dict) -> None:
        """Llega desde el hilo del grafo cada vez que termina un nodo."""
        nodo, cambios = next(iter(paso.items()))
        cfg = self.motor.cfg
        filas = lineas_de_paso(paso, cfg.umbral_evidencia, cfg.gen_modelo)
        if nodo == "recuperar":
            rec = cambios["recuperacion"]
            evidencia = bool(rec.hallazgos) and hay_evidencia(rec.mejor_similitud, cfg.umbral_evidencia)
            siguiente = "generar" if evidencia else "rechazo_previo"
        elif nodo == "generar":
            siguiente = "comprobar"
        else:
            siguiente = None
        ruta = list(cambios.get("ruta", []))

        def aplicar() -> None:
            self.grafo.set({"activo": siguiente, "ruta": ruta})
            self.status.set(f"{siguiente.replace('_', ' ')}…" if siguiente else "termina")
            self._append(filas)

        self.cola.ui(aplicar)

    def _turno(self, orden: Orden) -> None:
        try:
            r = self.motor.preguntar(orden.pregunta, orden.caso, self._al_paso)
            filas = [resumen_turno(r)]
            if orden.caso:
                filas += lineas_de_criterio(orden.caso, r)
            sim = "sin dato" if r.mejor_similitud is None else f"{r.mejor_similitud:.4f}".replace(".", ",")
            coste = "sin dato" if not self.motor.coste_completo else f"{self.motor.coste_sesion:.6f} USD".replace(".", ",")
            ultimo = (
                f"similitud {sim}\n"
                f"{'rechazo: ' + r.motivo_rechazo if r.rechazo else 'fuentes: ' + (', '.join(r.fuentes) or 'ninguna')}\n"
                f"{filas[0].text}\n"
                f"consultas en la sesión: {self.motor.n_preguntas} · generación: {coste}"
            )

            def aplicar() -> None:
                self._append(filas)
                self.ultimo.set(ultimo)

            self.cola.ui(aplicar)
        except Exception as exc:  # se muestra el tipo y el mensaje; nunca se inventa una respuesta
            mensaje = f"No se pudo completar la consulta: {type(exc).__name__}: {exc}"
            self.cola.ui(lambda: self._append([ChatLine("error", mensaje)]))
        finally:
            self.cola.ui(self._reposo)

    def _reposo(self) -> None:
        self.busy.set(False)
        self.status.set("listo")
        self.grafo.set({"activo": None, "ruta": self.grafo().get("ruta", [])})

    def quit(self) -> None:
        renderer = use_renderer()
        if renderer is not None:
            renderer.stop()

    def app(self) -> Box:
        renderer = use_renderer()
        if renderer is not None and self.cola.drain not in renderer._post_process_fns:
            renderer.add_post_process_fn(self.cola.drain)
        return build_app(
            titulo="S19 · RAG con LangGraph",
            subtitulo=self._subtitulo,
            lines=self.lines,
            busy=self.busy,
            status=self.status,
            turnos=self.turnos,
            on_submit=self.submit,
            on_quit=self.quit,
            sidebar=self._sidebar(),
        )


def abrir_chat(motor: MotorChat) -> None:
    """Abre la TUI. Necesita una terminal real (no una tubería ni la salida de un IDE)."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise SystemExit("El chat necesita una terminal interactiva (abre una terminal y repite el comando).")
    tui = RagTUI(motor)
    try:
        asyncio.run(render(tui.app))
    finally:
        if tui._hilo is not None:
            tui._hilo.join(timeout=30)
        motor.trazador.cerrar()
