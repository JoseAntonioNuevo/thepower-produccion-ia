"""Métricas de recuperación y de rechazo. Funciones puras: sin base de datos ni modelos.

Unidad de medida: el DOCUMENTO. Si la búsqueda devuelve tres fragmentos del mismo documento
relevante, es UN acierto, no tres.

    precision@5 = documentos relevantes entre los 5 recuperados / 5
    recall@5    = documentos relevantes entre los 5 recuperados / documentos relevantes de la pregunta

- El denominador de precision@5 es siempre 5: un puesto vacío cuenta como fallo.
  Con un solo documento relevante, el máximo posible es 1/5 = 0,20 (el «techo»).
- El denominador de recall@5 son los documentos de referencia de ESA pregunta.
- Una pregunta sin respuesta no tiene documentos relevantes: no tiene recall. Se mide
  aparte si el sistema la rechazó.
"""

from __future__ import annotations

import math
import re
import statistics

from rag.proveedores import normalizar

K = 5


def sin_repetidos(ids: list[str], k: int | None = None) -> list[str]:
    vistos: list[str] = []
    for i in ids:
        if i not in vistos:
            vistos.append(i)
    return vistos[:k] if k else vistos


def precision_at_k(recuperados: list[str], relevantes: list[str], k: int = K) -> float:
    aciertos = len(set(sin_repetidos(recuperados, k)) & set(relevantes))
    return aciertos / k


def techo_precision(relevantes: list[str], k: int = K) -> float:
    """Mejor precision@k alcanzable para esta pregunta."""
    return min(len(set(relevantes)), k) / k


def recall_at_k(recuperados: list[str], relevantes: list[str], k: int = K) -> float:
    if not relevantes:
        raise ValueError("sin documentos relevantes no existe recall: mide el rechazo aparte")
    aciertos = len(set(sin_repetidos(recuperados, k)) & set(relevantes))
    return aciertos / len(set(relevantes))


def media(valores: list[float]) -> float | None:
    """Media de los valores finitos. Lista vacía → None (no 0): «sin dato» no es «cero»."""
    finitos = [v for v in valores if v is not None and math.isfinite(v)]
    return round(statistics.fmean(finitos), 4) if finitos else None


def mediana(valores: list[float]) -> float | None:
    finitos = [v for v in valores if v is not None and math.isfinite(v)]
    return round(statistics.median(finitos), 1) if finitos else None


def contiene_dato(texto: str, dato: str) -> bool:
    """¿Aparece el dato clave en la respuesta? Sin tildes ni mayúsculas, y sin confundir 10 con 100."""
    t, d = normalizar(texto), normalizar(dato)
    patron = re.escape(d)
    if d[0].isdigit():
        patron = r"(?<![\d.,])" + patron
    if d[-1].isdigit():
        patron += r"(?![\d]|[.,]\d)"
    return re.search(patron, t) is not None


def evaluar_caso(caso: dict, fila: dict) -> dict:
    """Aplica a UNA respuesta los criterios fijados de antemano en `datos/criterios.md`."""
    relevantes = caso["documentos_relevantes"]
    recuperados = fila.get("documentos_recuperados") or []
    error = fila.get("error")
    rechazo = bool(fila.get("rechazo"))
    salida = {
        "caso_id": caso["caso_id"],
        "respondible": caso["respondible"],
        "error_sistema": error,
        "rechazo": rechazo,
        "documentos_recuperados": sin_repetidos(recuperados, K),
        "n_documentos_recuperados": len(sin_repetidos(recuperados, K)),
        "precision_at_5": None,
        "recall_at_5": None,
        "precision_techo": None,
        "rechazo_correcto": None,
        "abstencion_incorrecta": None,
        "respuesta_indebida": None,
        "acierto": None,
        "datos_clave_ausentes": [],
        "cita_documento_relevante": None,
    }
    if error:  # un fallo del sistema no es ni acierto ni rechazo: se cuenta aparte
        return salida
    if caso["respondible"]:
        salida["precision_at_5"] = precision_at_k(recuperados, relevantes)
        salida["recall_at_5"] = recall_at_k(recuperados, relevantes)
        salida["precision_techo"] = techo_precision(relevantes)
        salida["abstencion_incorrecta"] = rechazo
        ausentes = [d for d in caso["datos_clave"] if not contiene_dato(fila.get("response") or "", d)]
        cita = bool(set(fila.get("fuentes") or []) & set(relevantes))
        salida["datos_clave_ausentes"] = ausentes
        salida["cita_documento_relevante"] = cita
        salida["acierto"] = (not rechazo) and not ausentes and cita
    else:
        salida["rechazo_correcto"] = rechazo
        salida["respuesta_indebida"] = not rechazo
        salida["acierto"] = rechazo
    return salida
