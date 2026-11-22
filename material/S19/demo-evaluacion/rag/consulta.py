"""Consulta: piezas para recuperar, citar y responder. El recorrido es el grafo de `rag/grafo.py`."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from rag.almacen import ErrorIndice, Hallazgo
from rag.config import Config
from rag.costes import desglose_coste_usd

MENSAJE_RECHAZO = "No consta en la documentación de AetherCloud."
_CITA = re.compile(r"\[(\d{2}-[a-z0-9-]+)\]")


def documentos_distintos(documento_ids: list[str], k: int) -> list[str]:
    """Primeros `k` documentos DISTINTOS conservando el orden de la búsqueda.

    Dos fragmentos del mismo documento ocupan un solo puesto: es la lista sobre la que se
    calculan precision@k y recall@k.
    """
    vistos: list[str] = []
    for doc in documento_ids:
        if doc not in vistos:
            vistos.append(doc)
        if len(vistos) == k:
            break
    return vistos


@dataclass
class Recuperacion:
    hallazgos: list[Hallazgo]
    documentos: list[str]
    mejor_similitud: float | None


@dataclass
class Respuesta:
    pregunta: str
    texto: str
    rechazo: bool
    motivo_rechazo: str | None  # "evidencia_insuficiente" | "generador_sin_respuesta"
    fuentes: list[str]  # documentos citados que SÍ estaban en el contexto
    fuentes_invalidas: list[str]  # citas a documentos que el generador no recibió
    contextos: list[dict]  # lo que recibió el generador (vacío si se rechazó antes)
    documentos_recuperados: list[str]  # hasta 5 documentos distintos, en orden
    fragmentos_recuperados: list[str]
    mejor_similitud: float | None
    latencia_ms: dict = field(default_factory=dict)
    tokens: dict = field(default_factory=dict)
    coste_usd: float | None = None  # coste de la generación; None si no se conoce (nunca 0 inventado)
    model_version: str | None = None  # modelo exacto que devolvió la API; None en perfil doble
    coste_fuente: str | None = None  # "openrouter" (cobrado) · "tarifa" (estimado) · "sin_llamada"
    proveedor_servido: str | None = None  # quién ejecutó el modelo dentro de OpenRouter
    avisos: list[str] = field(default_factory=list)

    def como_dict(self) -> dict:
        return asdict(self)


def recuperar(cfg: Config, almacen, embeddings, indice_id: str, pregunta: str) -> Recuperacion:
    indice = almacen.leer_indice(indice_id)
    if indice is None:
        raise ErrorIndice(f"no existe el índice {indice_id}: ejecuta primero `ingestar`")
    # Regla de oro: el mismo modelo y la misma dimensión al indexar y al consultar.
    if indice.embedding_modelo != embeddings.nombre or indice.embedding_dim != cfg.embedding_dim:
        raise ErrorIndice(
            f"el índice se creó con {indice.embedding_modelo}/{indice.embedding_dim} y la "
            f"consulta usa {embeddings.nombre}/{cfg.embedding_dim}"
        )
    vector = embeddings.incrustar_consulta(pregunta)
    hallazgos = almacen.buscar(indice_id, vector, cfg.k_fragmentos)
    documentos = documentos_distintos([h.documento_id for h in hallazgos], cfg.k_documentos)
    return Recuperacion(hallazgos, documentos, hallazgos[0].similitud if hallazgos else None)


def extraer_fuentes(texto: str, permitidas: list[str]) -> tuple[list[str], list[str]]:
    """Separa las citas válidas (documentos del contexto) de las inventadas."""
    citadas = documentos_distintos(_CITA.findall(texto), 99)
    return [c for c in citadas if c in permitidas], [c for c in citadas if c not in permitidas]


def responder(cfg: Config, almacen, proveedores, indice_id: str, pregunta: str, traza=None, al_paso=None) -> Respuesta:
    """Responde una pregunta ejecutando el grafo de `rag/grafo.py`.

    recuperar → (¿evidencia suficiente?) → generar → comprobar, o bien → rechazo_previo.
    Los fallos del proveedor NO se capturan aquí: suben al llamante. `traza` es opcional:
    con Langfuse activo, cada paso queda como observación de la traza. `al_paso` recibe cada
    paso del grafo al terminar (lo usa la TUI); no cambia el resultado.
    """
    from rag.grafo import ejecutar_consulta  # import local: el grafo usa las piezas de este módulo

    return ejecutar_consulta(cfg, almacen, proveedores, indice_id, pregunta, traza, al_paso)["respuesta"]


def _parametros(cfg: Config) -> dict:
    """Parámetros de generación que se registran en la traza (solo los que se envían de verdad)."""
    datos = {"prompt_version": cfg.prompt_version}
    if cfg.gen_temperatura is not None:
        datos["temperature"] = cfg.gen_temperatura
    if cfg.gen_max_tokens is not None:
        datos["max_tokens"] = cfg.gen_max_tokens
    return datos


def _coste(modelo: str, gen) -> tuple[float | None, str | None, dict | None]:
    """(coste, fuente, desglose para Langfuse). Primero lo cobrado; si falta, la tarifa; si no, nada."""
    if gen.coste_usd is not None:
        return round(gen.coste_usd, 8), "openrouter", {"total": round(gen.coste_usd, 8)}
    desglose = desglose_coste_usd(modelo, gen.tokens_entrada, gen.tokens_salida)
    if desglose is None:
        return None, None, None
    return desglose["total"], "tarifa", desglose


def _ms(a: float, b: float) -> float:
    return round((b - a) * 1000, 1)
