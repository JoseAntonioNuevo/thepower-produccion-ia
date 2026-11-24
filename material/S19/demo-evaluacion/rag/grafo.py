"""La consulta del RAG como grafo de LangGraph.

    START → recuperar ─┬─ mejor similitud ≥ umbral → generar → comprobar → END
                       └─ sin evidencia suficiente → rechazo_previo → END

Cada nodo hace UN paso y deja su resultado en el estado. El grafo no añade lógica nueva:
los nodos llaman a las mismas funciones que antes (`recuperar`, el generador de OpenRouter o
el doble, `extraer_fuentes`), así que la salida es idéntica a la versión sin LangGraph y la
evaluación (lote, informe, Ragas, regresión) no cambia.

Qué aporta el grafo:
- Las dos formas de rechazar quedan a la vista. `rechazo_previo` es una rama: no se llama al
  generador y su coste de generación es cero. El rechazo del modelo («No consta») lo detecta `comprobar`.
- La decisión de enrutado es una función pura (`hay_evidencia`) que se prueba con una tabla.
- `stream` entrega cada paso al terminar: la TUI (`python s19.py chat`) los pinta en vivo.

Como en S5, las dependencias se inyectan al construir el grafo (configuración, almacén y
proveedores) y la traza de Langfuse viaja en `config["configurable"]`, igual que los
callbacks. Sin Langfuse se usa una traza nula: el código es el mismo.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

from rag.config import Config
from rag.consulta import (
    MENSAJE_RECHAZO,
    Recuperacion,
    Respuesta,
    _coste,
    _ms,
    _parametros,
    documentos_distintos,
    extraer_fuentes,
    recuperar,
)
from rag.observabilidad import TrazaNula
from rag.proveedores import NO_CONSTA, Generacion, componer_prompt

NODOS = ("recuperar", "rechazo_previo", "generar", "comprobar")


class EstadoConsulta(TypedDict, total=False):
    """Lo que se va acumulando en una consulta. Cada nodo devuelve solo lo que añade."""

    pregunta: str
    recuperacion: Recuperacion
    generacion: Generacion
    respuesta: Respuesta  # resultado final: el mismo objeto que devolvía `responder`
    ruta: list[str]  # nodos recorridos, en orden: la trayectoria que comprueban los tests
    t0: float  # marcas de tiempo (perf_counter) para la latencia de cada paso
    t1: float
    t2: float


def hay_evidencia(mejor_similitud: float | None, umbral: float) -> bool:
    """Compara la mejor similitud con el umbral. La igualdad basta para generar y una búsqueda vacía devuelve False."""
    return mejor_similitud is not None and mejor_similitud >= umbral


def _traza(config: RunnableConfig):
    """Obtiene la traza de la consulta o usa una traza nula para que los nodos funcionen también con Langfuse apagado."""
    return (config.get("configurable") or {}).get("traza") or TrazaNula()


def construir_grafo(cfg: Config, almacen, proveedores, indice_id: str):
    """Conecta la recuperación con las ramas de generación y rechazo. Recibe el almacén y los proveedores
    para que la TUI y los tests ejecuten el mismo grafo con dependencias distintas."""

    def nodo_recuperar(estado: EstadoConsulta, config: RunnableConfig) -> EstadoConsulta:
        """Busca fragmentos usando el embedding de la pregunta y guarda documentos, similitud y tiempos.
        El siguiente nodo usa esa evidencia para decidir si procede generar."""
        t0 = time.perf_counter()
        with _traza(config).paso("recuperacion", "retriever", input=estado["pregunta"]) as paso:
            rec = recuperar(cfg, almacen, proveedores.embeddings, indice_id, estado["pregunta"])
            paso.update(
                output={"documentos": rec.documentos, "mejor_similitud": rec.mejor_similitud},
                metadata={"embedding_modelo": cfg.embedding_modelo, "k_fragmentos": cfg.k_fragmentos},
            )
        return {"recuperacion": rec, "t0": t0, "t1": time.perf_counter(), "ruta": [*estado["ruta"], "recuperar"]}

    def ruta_tras_recuperar(estado: EstadoConsulta) -> str:
        """Elige la siguiente rama. Solo pasa a generar si hay fragmentos y el mejor alcanza el umbral."""
        rec = estado["recuperacion"]
        evidencia = bool(rec.hallazgos) and hay_evidencia(rec.mejor_similitud, cfg.umbral_evidencia)
        return "generar" if evidencia else "rechazo_previo"

    def nodo_rechazo_previo(estado: EstadoConsulta) -> EstadoConsulta:
        """Devuelve «No consta» al faltar evidencia. Registra la búsqueda ya realizada y cero tokens de generación."""
        t0, t1 = estado["t0"], estado["t1"]
        respuesta = Respuesta(
            texto=MENSAJE_RECHAZO,
            rechazo=True,
            motivo_rechazo="evidencia_insuficiente",
            fuentes=[],
            fuentes_invalidas=[],
            contextos=[],
            latencia_ms={"recuperacion": _ms(t0, t1), "generacion": 0.0, "total": _ms(t0, t1)},
            tokens={"entrada": 0, "salida": 0},
            coste_usd=0.0,
            coste_fuente="sin_llamada",
            **_base(estado),
        )
        return {"respuesta": respuesta, "ruta": [*estado["ruta"], "rechazo_previo"]}

    def nodo_generar(estado: EstadoConsulta, config: RunnableConfig) -> EstadoConsulta:
        """Envía al generador la pregunta y los primeros k_contexto fragmentos. Registra la respuesta y el consumo
        disponible en la traza para poder comparar qué recibió y cuánto costó cada llamada."""
        contexto = estado["recuperacion"].hallazgos[: cfg.k_contexto]
        pares = [(h.documento_id, h.contenido) for h in contexto]
        with _traza(config).paso(
            "generacion",
            "generation",
            model=cfg.gen_modelo,
            input=componer_prompt(estado["pregunta"], pares),
            model_parameters=_parametros(cfg),
        ) as paso:
            gen = proveedores.generador.generar(estado["pregunta"], pares, cfg.prompt_version)
            conocidos = gen.tokens_entrada is not None and gen.tokens_salida is not None
            _, _, desglose = _coste(cfg.gen_modelo, gen)
            servido = {"model_version": gen.model_version, "proveedor_servido": gen.proveedor_servido}
            servido = {k: v for k, v in servido.items() if v}
            paso.update(
                output=gen.texto,
                # Sin tokens no hay coste: Langfuse no los estima a partir del texto.
                usage_details=({"input": gen.tokens_entrada, "output": gen.tokens_salida} if conocidos else None),
                cost_details=desglose,
                metadata=servido or None,
            )
        return {"generacion": gen, "t2": time.perf_counter(), "ruta": [*estado["ruta"], "generar"]}

    def nodo_comprobar(estado: EstadoConsulta) -> EstadoConsulta:
        """Detecta la abstención del generador y contrasta sus citas con los documentos enviados.
        Guarda contexto, avisos y consumo para explicar y evaluar la respuesta."""
        gen = estado["generacion"]
        contexto = estado["recuperacion"].hallazgos[: cfg.k_contexto]
        t0, t1, t2 = estado["t0"], estado["t1"], estado["t2"]
        coste, fuente, _ = _coste(cfg.gen_modelo, gen)
        comun = {
            "contextos": [
                {
                    "fragmento_id": h.fragmento_id,
                    "documento_id": h.documento_id,
                    "contenido": h.contenido,
                    "similitud": round(h.similitud, 4),
                }
                for h in contexto
            ],
            "latencia_ms": {"recuperacion": _ms(t0, t1), "generacion": _ms(t1, t2), "total": _ms(t0, t2)},
            "tokens": {"entrada": gen.tokens_entrada, "salida": gen.tokens_salida},
            "coste_usd": coste,
            "coste_fuente": fuente,
            "model_version": gen.model_version,
            "proveedor_servido": gen.proveedor_servido,
            **_base(estado),
        }
        ruta = [*estado["ruta"], "comprobar"]
        # Rechazo del generador: leyó el contexto y declaró que no basta.
        if gen.texto.strip().startswith(NO_CONSTA):
            respuesta = Respuesta(
                texto=MENSAJE_RECHAZO,
                rechazo=True,
                motivo_rechazo="generador_sin_respuesta",
                fuentes=[],
                fuentes_invalidas=[],
                **comun,
            )
            return {"respuesta": respuesta, "ruta": ruta}
        permitidas = documentos_distintos([h.documento_id for h in contexto], 99)
        fuentes, invalidas = extraer_fuentes(gen.texto, permitidas)
        avisos = []
        if not gen.texto.strip():
            avisos.append("respuesta_vacia")
        if getattr(gen, "fin", None) == "length":
            # El modelo agotó S19_GEN_MAX_TOKENS (con razonamiento, a veces antes de escribir nada).
            avisos.append("max_tokens_agotado")
        if not fuentes:
            avisos.append("sin_fuentes")  # una respuesta sin fuente comprobable no cumple el formato
        if invalidas:
            avisos.append("fuentes_fuera_del_contexto")
        respuesta = Respuesta(
            texto=gen.texto.strip(),
            rechazo=False,
            motivo_rechazo=None,
            fuentes=fuentes,
            fuentes_invalidas=invalidas,
            avisos=avisos,
            **comun,
        )
        return {"respuesta": respuesta, "ruta": ruta}

    grafo = StateGraph(EstadoConsulta)
    grafo.add_node("recuperar", nodo_recuperar)
    grafo.add_node("rechazo_previo", nodo_rechazo_previo)
    grafo.add_node("generar", nodo_generar)
    grafo.add_node("comprobar", nodo_comprobar)
    grafo.add_edge(START, "recuperar")
    grafo.add_conditional_edges("recuperar", ruta_tras_recuperar, {"generar": "generar", "rechazo_previo": "rechazo_previo"})
    grafo.add_edge("generar", "comprobar")
    grafo.add_edge("comprobar", END)
    grafo.add_edge("rechazo_previo", END)
    return grafo.compile()


def _base(estado: EstadoConsulta) -> dict:
    """Reúne pregunta, documentos, fragmentos y mejor similitud para evaluar la recuperación en ambas ramas."""
    rec = estado["recuperacion"]
    return {
        "pregunta": estado["pregunta"],
        "documentos_recuperados": rec.documentos,
        "fragmentos_recuperados": [h.fragmento_id for h in rec.hallazgos],
        "mejor_similitud": round(rec.mejor_similitud, 4) if rec.hallazgos else None,
    }


def ejecutar_consulta(
    cfg: Config,
    almacen,
    proveedores,
    indice_id: str,
    pregunta: str,
    traza=None,
    al_paso: Callable[[dict], None] | None = None,
) -> EstadoConsulta:
    """Ejecuta el grafo y devuelve el estado final. Si recibe al_paso, entrega cada actualización a la TUI.
    Los errores del proveedor se propagan al llamante para que pueda registrarlos."""
    grafo = construir_grafo(cfg, almacen, proveedores, indice_id)
    config: RunnableConfig = {"configurable": {"traza": traza or TrazaNula()}}
    entrada: EstadoConsulta = {"pregunta": pregunta, "ruta": []}
    if al_paso is None:
        return grafo.invoke(entrada, config)
    final: EstadoConsulta = {}
    for modo, datos in grafo.stream(entrada, config, stream_mode=["updates", "values"]):
        if modo == "updates":
            al_paso(datos)
        else:
            final = datos
    return final
