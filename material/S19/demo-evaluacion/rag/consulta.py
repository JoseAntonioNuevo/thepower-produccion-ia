"""Consulta: recuperar, decidir si hay evidencia, generar con fuentes o rechazar."""

from __future__ import annotations

import re
import time
from dataclasses import asdict, dataclass, field

from rag.almacen import ErrorIndice, Hallazgo
from rag.config import Config
from rag.costes import coste_usd, desglose_coste_usd
from rag.observabilidad import TrazaNula
from rag.proveedores import NO_CONSTA, componer_prompt

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
    coste_usd: float | None = None  # estimación con tarifas.json; None si faltan tokens
    model_version: str | None = None  # versión de modelo devuelta por la API; None en perfil doble
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


def responder(cfg: Config, almacen, proveedores, indice_id: str, pregunta: str, traza=None) -> Respuesta:
    """Responde una pregunta. Los fallos del proveedor NO se capturan aquí: suben al llamante.

    `traza` es opcional: con Langfuse activo, cada paso queda como observación de la traza.
    """
    traza = traza or TrazaNula()
    t0 = time.perf_counter()
    with traza.paso("recuperacion", "retriever", input=pregunta) as paso:
        rec = recuperar(cfg, almacen, proveedores.embeddings, indice_id, pregunta)
        paso.update(
            output={"documentos": rec.documentos, "mejor_similitud": rec.mejor_similitud},
            metadata={"embedding_modelo": cfg.embedding_modelo, "k_fragmentos": cfg.k_fragmentos},
        )
    t1 = time.perf_counter()
    base = {
        "pregunta": pregunta,
        "documentos_recuperados": rec.documentos,
        "fragmentos_recuperados": [h.fragmento_id for h in rec.hallazgos],
        "mejor_similitud": round(rec.mejor_similitud, 4) if rec.hallazgos else None,
    }
    # 1) Rechazo previo: sin evidencia suficiente no se llama al generador (ni se paga).
    if not rec.hallazgos or rec.mejor_similitud < cfg.umbral_evidencia:
        return Respuesta(
            texto=MENSAJE_RECHAZO,
            rechazo=True,
            motivo_rechazo="evidencia_insuficiente",
            fuentes=[],
            fuentes_invalidas=[],
            contextos=[],
            latencia_ms={"recuperacion": _ms(t0, t1), "generacion": 0.0, "total": _ms(t0, t1)},
            tokens={"entrada": 0, "salida": 0},
            coste_usd=0.0,
            **base,
        )
    contexto = rec.hallazgos[: cfg.k_contexto]
    pares = [(h.documento_id, h.contenido) for h in contexto]
    with traza.paso(
        "generacion",
        "generation",
        model=cfg.gen_modelo,
        input=componer_prompt(pregunta, pares),
        model_parameters={"prompt_version": cfg.prompt_version, "temperature": 0},
    ) as paso:
        gen = proveedores.generador.generar(pregunta, pares, cfg.prompt_version)
        conocidos = gen.tokens_entrada is not None and gen.tokens_salida is not None
        desglose = desglose_coste_usd(cfg.gen_modelo, gen.tokens_entrada, gen.tokens_salida)
        paso.update(
            output=gen.texto,
            # Sin tokens no hay coste: Langfuse no los estima a partir del texto.
            usage_details=({"input": gen.tokens_entrada, "output": gen.tokens_salida} if conocidos else None),
            cost_details=desglose,
            metadata={"model_version": gen.model_version} if gen.model_version else None,
        )
    t2 = time.perf_counter()
    contextos = [
        {
            "fragmento_id": h.fragmento_id,
            "documento_id": h.documento_id,
            "contenido": h.contenido,
            "similitud": round(h.similitud, 4),
        }
        for h in contexto
    ]
    comun = {
        "contextos": contextos,
        "latencia_ms": {"recuperacion": _ms(t0, t1), "generacion": _ms(t1, t2), "total": _ms(t0, t2)},
        "tokens": {"entrada": gen.tokens_entrada, "salida": gen.tokens_salida},
        "coste_usd": coste_usd(cfg.gen_modelo, gen.tokens_entrada, gen.tokens_salida),
        "model_version": gen.model_version,
        **base,
    }
    # 2) Rechazo del generador: leyó el contexto y declaró que no basta.
    if gen.texto.strip().startswith(NO_CONSTA):
        return Respuesta(
            texto=MENSAJE_RECHAZO,
            rechazo=True,
            motivo_rechazo="generador_sin_respuesta",
            fuentes=[],
            fuentes_invalidas=[],
            **comun,
        )
    permitidas = documentos_distintos([h.documento_id for h in contexto], 99)
    fuentes, invalidas = extraer_fuentes(gen.texto, permitidas)
    avisos = []
    if not gen.texto.strip():
        avisos.append("respuesta_vacia")
    if not fuentes:
        avisos.append("sin_fuentes")  # una respuesta sin fuente comprobable no cumple el formato
    if invalidas:
        avisos.append("fuentes_fuera_del_contexto")
    return Respuesta(
        texto=gen.texto.strip(),
        rechazo=False,
        motivo_rechazo=None,
        fuentes=fuentes,
        fuentes_invalidas=invalidas,
        avisos=avisos,
        **comun,
    )


def _ms(a: float, b: float) -> float:
    return round((b - a) * 1000, 1)
