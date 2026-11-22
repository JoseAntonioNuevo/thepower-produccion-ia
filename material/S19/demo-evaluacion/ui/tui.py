"""Piezas visuales de la TUI (OpenTUI 0.1.2), reutilizadas de la TUI de S5/S6.

Origen: repositorio `1-langGraph`, `ui/chat_tui.py`. Se conservan el chat con globos y
markdown, el editor con historial y los ajustes necesarios para opentui 0.1.2 (cursor,
eventos de soltar tecla, colores Tokyo Night). Se quitan el panel del juez, el validador y
las herramientas del agente de soporte: aquí el panel lateral lo aporta `ui/rag_tui.py`
con los nodos del grafo del RAG.

Regla de hilos (igual que en S5/S6): el grafo corre en un hilo aparte y NUNCA toca la
pantalla; deja funciones en una cola y `drain()` las ejecuta en el hilo de OpenTUI.
"""

from __future__ import annotations

import queue
import time
from collections.abc import Callable
from typing import Any

from opentui import (
    Box,
    For,
    ScrollBox,
    ScrollContent,
    Signal,
    Text,
    TextareaRenderable,
    hooks,
    on_cleanup,
    use_cursor,
    use_cursor_style,
    use_renderer,
)
from opentui.animation import create_timeline, engine
from opentui.components.markdown import MarkdownRenderable
from opentui.input.keymapping import KeyBinding

from ui.chat_input import HistorialComposer, indice_cursor
from ui.lineas import ChatLine

# Paleta Tokyo Night de S5/S6: no cambiar los hex.
BG = "#16161e"
SURFACE = "#1a1b26"
BORDER = "#414868"
DIM = "#565f89"
BRIGHT = "#c0caf5"
USER = "#7aa2f7"
THINK = "#9d7cd8"
TOOL = "#e0af68"
DATO = "#9ece6a"
BOT = "#c0caf5"
ERROR = "#f7768e"
ACTIVE = "#7aa2f7"
_SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧"

# kind → (etiqueta en pantalla, color, estilo). human/bot = globo; meta = traza; tarjeta = caja.
_KIND = {
    "human": ("tú", USER, "human"),
    "paso": ("grafo", TOOL, "meta"),
    "dato": ("recuperación", DATO, "tarjeta"),
    "criterio": ("criterio", THINK, "tarjeta"),
    "bot": ("rag", BOT, "bot"),
    "rechazo": ("rechazo", TOOL, "bot"),
    "error": ("error", ERROR, "bot"),
    "hint": ("", DIM, "hint"),
}

SALIR = {"salir", "exit", "q"}


def _envolver_markdown(nodo: Any) -> None:
    """MarkdownTextBlock nace con wrap_mode=none; sin wrap el globo recorta."""
    if hasattr(nodo, "wrap_mode"):
        nodo.wrap_mode = "word"
    for hijo in getattr(nodo, "get_children", lambda: ())():
        _envolver_markdown(hijo)


def _cuerpo_globo(line: ChatLine, color: str, *, lado: str) -> Text | MarkdownRenderable:
    """La respuesta del RAG entra como markdown; tú y error se quedan en texto plano."""
    if lado == "bot" and line.kind in {"bot", "rechazo"}:
        cuerpo = MarkdownRenderable(
            content=line.text,
            conceal=True,
            fg=color,
            background_color=SURFACE,
            flex_shrink=0,
            align_self="stretch",
        )
        _envolver_markdown(cuerpo)
        return cuerpo
    return Text(line.text, fg=color, bg=SURFACE, wrap_mode="word")


def _globo(line: ChatLine, etiqueta: str, color: str, *, lado: str) -> Box:
    """Caja de diálogo (tú a la derecha, RAG/rechazo/error a la izquierda)."""
    dialogo = Box(
        _cuerpo_globo(line, color, lado=lado),
        title=etiqueta,
        title_alignment="right" if lado == "human" else "left",
        border=True,
        border_style="round",
        border_color=color,
        background_color=SURFACE,
        padding_left=2,
        padding_right=2,
        padding_top=1,
        padding_bottom=1,
        flex_shrink=0,
        max_width=56 if lado == "human" else None,
        align_self="stretch" if lado != "human" else None,
    )
    if lado == "human":
        return Box(
            dialogo,
            key=line.key,
            background_color=SURFACE,
            margin_left=10,
            margin_right=2,
            margin_top=1,
            flex_shrink=0,
            align_self="stretch",
            align_items="flex-end",
        )
    return Box(
        dialogo,
        key=line.key,
        background_color=SURFACE,
        margin_left=2,
        margin_right=3,
        margin_top=1,
        margin_bottom=1,
        flex_shrink=0,
        align_self="stretch",
        align_items="stretch",
    )


def _traza(line: ChatLine, etiqueta: str, color: str) -> Box:
    """Paso del grafo: riel con sangría, para no confundirlo con la respuesta."""
    return Box(
        Text("│", fg=color, bg=SURFACE),
        Box(
            Text(etiqueta, fg=color, bg=SURFACE),
            Text(line.text, fg=color, bg=SURFACE, wrap_mode="word"),
            flex_direction="column",
            flex_grow=1,
            flex_shrink=1,
            gap=0,
        ),
        key=line.key,
        background_color=SURFACE,
        padding_left=3,
        padding_right=3,
        flex_direction="row",
        gap=1,
        flex_shrink=0,
        align_self="stretch",
    )


def _tarjeta(line: ChatLine, etiqueta: str, color: str) -> Box:
    """Documentos recuperados o veredicto del criterio: tarjeta corta."""
    return Box(
        Box(
            Text(line.text, fg=color, bg=SURFACE, wrap_mode="word"),
            title=etiqueta,
            title_alignment="left",
            border=True,
            border_style="round",
            border_color=color,
            background_color=SURFACE,
            padding_left=2,
            padding_right=2,
            flex_shrink=0,
            align_self="stretch",
        ),
        key=line.key,
        background_color=SURFACE,
        margin_left=2,
        margin_right=3,
        margin_top=1,
        flex_shrink=0,
        align_self="stretch",
    )


def linea(line: ChatLine) -> Box:
    """Una fila del chat según su tipo."""
    etiqueta, color, estilo = _KIND[line.kind]
    if estilo == "hint":
        return Box(
            Text(line.text, fg=color, bg=SURFACE, wrap_mode="word"),
            key=line.key,
            background_color=SURFACE,
            padding_left=3,
            padding_right=3,
            padding_top=1,
            flex_shrink=0,
            align_self="stretch",
        )
    if estilo == "human":
        return _globo(line, etiqueta, color, lado="human")
    if estilo == "meta":
        return _traza(line, etiqueta, color)
    if estilo == "tarjeta":
        return _tarjeta(line, etiqueta, color)
    return _globo(line, etiqueta, color, lado="bot")


def _posicion_cursor_en_textarea(textarea: Any) -> tuple[int, int]:
    """Columna y fila visuales (0-based) del caret dentro del widget."""
    try:
        visual = textarea._editor_view.get_visual_cursor()
        return int(visual.visual_col), int(visual.visual_row)
    except Exception:
        texto = getattr(textarea, "plain_text", "") or ""
        offset = int(getattr(textarea, "cursor_offset", 0) or 0)
        fila, columna = indice_cursor(texto, offset)
        return max(0, columna - 1), max(0, fila - 1)


def _mostrar_cursor_textarea(textarea: Any, *, encendido: bool) -> None:
    """Pide el cursor del terminal en el punto de inserción (TextareaRenderable no lo hace)."""
    if not encendido or not getattr(textarea, "_focused", False):
        return
    x = int(getattr(textarea, "_x", 0) or 0)
    y = int(getattr(textarea, "_y", 0) or 0)
    w = int(getattr(textarea, "_layout_width", 0) or 0)
    h = int(getattr(textarea, "_layout_height", 0) or 1)
    col, row = _posicion_cursor_en_textarea(textarea)
    if w > 0:
        col = max(0, min(col, w - 1))
    if h > 0:
        row = max(0, min(row, h - 1))
    use_cursor(x + col, y + row)
    use_cursor_style("block", USER)


def _ms(delta: float) -> float:
    """El renderer pasa segundos (~0.016); Timeline espera milisegundos."""
    return delta if delta > 5 else delta * 1000.0


def _arrancar_efectos(ocupado: Signal, pulso: Signal, segundos: Signal) -> None:
    """Pulso del spinner y cronómetro del turno mientras el grafo trabaja (como en S5/S6)."""
    renderer = use_renderer()
    if renderer is None:
        return
    pulso_obj = type("_Pulso", (), {"v": 0.0})()
    pulso_tl = create_timeline(duration=400, loop=True, autoplay=False)
    pulso_tl.add(
        pulso_obj,
        {
            "v": 1.0,
            "duration": 400,
            "ease": "linear",
            "alternate": True,
            "loop": True,
            "on_update": lambda anim: pulso.set(float(anim.targets[0].v)),
        },
    )
    reloj: dict[str, Any] = {"inicio": None, "ultimo": -1}

    def _tick(delta: float) -> None:
        engine.update(_ms(delta))
        if ocupado() and not pulso_tl.is_playing:
            pulso_tl.play()
        elif not ocupado() and pulso_tl.is_playing:
            pulso_tl.pause()
            pulso.set(0.0)
        if ocupado():
            if reloj["inicio"] is None:
                reloj["inicio"] = time.monotonic()
            actual = int(time.monotonic() - reloj["inicio"])
            if actual != reloj["ultimo"]:
                reloj["ultimo"] = actual
                segundos.set(actual)
        elif reloj["inicio"] is not None:
            reloj["inicio"], reloj["ultimo"] = None, -1
            segundos.set(0)

    renderer.set_frame_callback(_tick)


def build_app(
    *,
    titulo: str,
    subtitulo: Callable[[], str],
    lines: Signal,
    busy: Signal,
    status: Signal,
    turnos: Signal,
    on_submit: Callable[[str], None],
    on_quit: Callable[[], None],
    sidebar: Box,
) -> Box:
    """Árbol visual: cabecera + (chat | panel lateral) + editor + pie."""
    pulso = Signal(0.0, name="pulso")
    segundos = Signal(0, name="segundos")
    composer_height = Signal(3, name="composer_height")
    historial = HistorialComposer()
    textarea: TextareaRenderable | None = None

    def _on_composer_change(texto: str) -> None:
        composer_height.set(min(6, max(3, 3 + texto.count("\n"))))

    def _submit_composer(texto: str) -> None:
        texto = texto.strip()
        if busy() or not texto or textarea is None:
            return
        historial.push(texto)
        textarea.set_text("")
        on_submit(texto)

    def _set_composer_text(texto: str) -> None:
        if textarea is None:
            return
        textarea.set_text(texto)
        textarea.cursor_offset = len(texto)

    def _on_composer_key(event: Any) -> None:
        if textarea is None:
            return
        if getattr(event, "event_type", "press") == "release":
            # Kitty keyboard mode informa de pulsar y soltar: soltar no debe escribir otra vez.
            event.prevent_default()
            return
        key = event.key.lower()
        if key in {"escape", "esc"}:
            event.prevent_default()
            on_quit()
            return
        if key == "up" and not event.shift:
            if historial.navegando or not textarea.plain_text or textarea.line_count == 1:
                event.prevent_default()
                _set_composer_text(historial.anterior(textarea.plain_text))
            return
        if key == "down" and not event.shift and historial.navegando:
            event.prevent_default()
            _set_composer_text(historial.siguiente())

    # wrap_mode="none": en opentui 0.1.2 varios Text en una fila se despintan con el modo nativo.
    header = Box(
        Text(f" {titulo}", fg=USER, bg=BG, bold=True, wrap_mode="none"),
        Text(lambda: f"  {subtitulo()}", fg=DIM, bg=BG, wrap_mode="none"),
        Text(
            lambda: f"  ·  {status()}" + (f" · {segundos()}s" if busy() and segundos() > 0 else ""),
            fg=busy.map(lambda b: ACTIVE if b else DATO),
            bg=BG,
            bold=True,
            wrap_mode="none",
        ),
        flex_direction="row",
        background_color=BG,
        height=1,
    )

    transcript = Box(
        ScrollBox(
            content=ScrollContent(
                For(linea, each=lines, key_fn=lambda e: e.key, flex_shrink=0, flex_grow=0),
                gap=0,
                padding_x=3,
                padding_top=1,
                padding_bottom=2,
                align_self="stretch",
            ),
            sticky_scroll=True,
            sticky_start="bottom",
            scroll_y=True,
            flex_grow=1,
            background_color=SURFACE,
        ),
        border=True,
        border_style="round",
        border_color=BORDER,
        title="chat",
        title_alignment="left",
        background_color=SURFACE,
        flex_grow=1,
    )
    _arrancar_efectos(busy, pulso, segundos)

    cuerpo = Box(
        transcript,
        sidebar,
        flex_direction="row",
        flex_grow=1,
        flex_shrink=1,
        flex_basis=0,
        gap=1,
        overflow="hidden",
    )

    textarea = TextareaRenderable(
        initial_value="",
        placeholder="Escribe una pregunta, un número del guion (1-7) o /ayuda…",
        wrap_mode="word",
        text_color=BRIGHT,
        placeholder_color=DIM,
        focused_background_color=SURFACE,
        focused_text_color=BRIGHT,
        cursor_color=USER,
        flex_grow=1,
        flex_shrink=1,
        align_self="stretch",
        on_submit=_submit_composer,
        on_key_down=_on_composer_key,
        on_content_change=_on_composer_change,
        key_bindings=[
            KeyBinding(name="return", action="submit"),
            KeyBinding(name="return", action="newline", shift=True),
        ],
    )
    textarea.focus()
    # En 0.1.2 el handler llega por dos canales: dejamos solo el del renderer (si no, dobles letras).
    hooks.unregister_keyboard_handler(textarea._key_handler)
    _pintar_textarea = type(textarea).render

    def _render_con_caret(buffer: Any, delta_time: float = 0) -> None:
        _pintar_textarea(textarea, buffer, delta_time)
        _mostrar_cursor_textarea(textarea, encendido=not busy.peek())

    textarea.render = _render_con_caret

    def _sync_placeholder() -> None:
        if textarea is not None:
            textarea.placeholder = (
                f"{_SPINNER[int(pulso.peek() * 8) % len(_SPINNER)]} el grafo está trabajando…"
                if busy.peek()
                else "Escribe una pregunta, un número del guion (1-7) o /ayuda…"
            )

    _sync_placeholder()
    quitar_busy = busy.subscribe(lambda _v: _sync_placeholder())
    quitar_pulso = pulso.subscribe(lambda _v: _sync_placeholder())
    on_cleanup(lambda: (quitar_busy(), quitar_pulso()))
    composer = Box(
        textarea,
        background_color=SURFACE,
        padding_left=2,
        padding_right=2,
        height=composer_height,
        min_height=3,
        max_height=6,
        flex_shrink=0,
        flex_grow=0,
        border=True,
        border_style="round",
        border_color=busy.map(lambda b: ACTIVE if b else BORDER),
        title="pregunta",
    )
    pie = Box(
        Text("enter envía · ↑ historial · 1-7 guion · T01-T20 test · /ayuda · esc sale", fg=DIM, bg=BG, wrap_mode="none"),
        Text(lambda: f"turno {turnos()}", fg=DIM, bg=BG, wrap_mode="none"),
        flex_direction="row",
        justify_content="space-between",
        padding_left=1,
        padding_right=1,
        height=1,
        flex_shrink=0,
        background_color=BG,
    )
    return Box(
        header,
        cuerpo,
        Box(composer, pie, flex_direction="column", gap=0, flex_shrink=0),
        flex_direction="column",
        flex_grow=1,
        background_color=BG,
        padding=1,
        gap=1,
        overflow="hidden",
    )


class ColaUI:
    """Puente hilo del grafo → hilo de OpenTUI: el grafo encola, `drain` pinta."""

    def __init__(self) -> None:
        self._pendientes: queue.Queue[Callable[[], None]] = queue.Queue()

    def ui(self, fn: Callable[[], None]) -> None:
        self._pendientes.put(fn)

    def drain(self, _buffer: Any = None) -> None:
        """OpenTUI la llama tras cada pintado (post_process); vacía la cola."""
        while True:
            try:
                fn = self._pendientes.get_nowait()
            except queue.Empty:
                return
            fn()
