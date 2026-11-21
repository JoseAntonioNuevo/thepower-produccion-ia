"""PASO 7 · Deep Research + RAG: investigación autónoma, pero acotada.

Una investigación es un TRABAJO con estado, no una respuesta inmediata:

  planificar -> buscar fuentes -> leer -> extraer evidencia -> verificar -> informe

Combina dos orígenes que nunca se mezclan en el informe:
- política interna   -> recuperación propia (RAG sobre la documentación de AetherCloud)
- información pública -> lista blanca de fuentes externas (catalogo.json)

Límites escritos en el código: número de consultas, de fuentes, bytes por fuente y tiempo.
Si falta evidencia, el informe sale como «parcial» y dice qué falta. Eso es un resultado
correcto: lo incorrecto sería rellenar el hueco.
"""

import json
import math
import re
import time

from .config import RAIZ, Config
from .rag import palabras, recuperar

CARPETA = RAIZ / "datos" / "fuentes_publicas"
AVISO = "La información pública no sustituye a una política interna que falte."


def catalogo() -> list[dict]:
    return json.loads((CARPETA / "catalogo.json").read_text(encoding="utf-8"))["fuentes"]


# ------------------------------------------------------------------ 1. planificar
def planificar(tema: str, cfg: Config) -> list[str]:
    """Divide el tema en consultas concretas. Nunca más de `max_consultas`."""
    partes = [p.strip() for p in re.split(r"\s+y\s+|[,;]", tema) if len(p.strip()) > 3]
    return (partes or [tema])[: cfg.max_consultas]


# ------------------------------------------------------------------ 2. buscar
def buscar_fuentes(consulta: str) -> list[dict]:
    """Ordena la lista blanca por coincidencia con la consulta. Sin coincidencia, no hay fuente."""
    terminos = set(palabras(consulta))
    puntuadas = []
    for fuente in catalogo():
        vocabulario = set(palabras(" ".join(fuente["temas"]) + " " + fuente["titulo"]))
        puntos = len(terminos & vocabulario)
        if puntos:
            puntuadas.append((puntos, fuente))
    return [f for _, f in sorted(puntuadas, key=lambda par: par[0], reverse=True)]


# ------------------------------------------------------------------ 3. leer
def leer_fuente(fuente: dict, cfg: Config) -> tuple[str, str]:
    """Devuelve (texto, origen). Solo se leen fuentes del catálogo: no hay URL libre."""
    if cfg.fuentes == "locales":
        return (CARPETA / fuente["copia_local"]).read_text(encoding="utf-8"), "copia_de_aula"
    import httpx

    url = fuente["url"]
    if not url.startswith("https://"):
        raise ValueError("solo se permiten URL https del catálogo")
    recibido = b""
    with httpx.stream(
        "GET", url, timeout=15, follow_redirects=True, headers={"User-Agent": "thepower-s20-aula/0.1"}
    ) as respuesta:
        respuesta.raise_for_status()
        for trozo in respuesta.iter_bytes():
            recibido += trozo
            if len(recibido) >= cfg.max_bytes_fuente:
                break  # límite de bytes: no se descarga más de lo previsto
    texto = recibido.decode("utf-8", errors="replace")
    if "<html" in texto[:2000].lower():
        texto = re.sub(r"(?is)<(script|style).*?</\1>", " ", texto)
        texto = re.sub(r"(?s)<[^>]+>", "\n", texto)
    return texto, "red"


# ------------------------------------------------------------------ 4. extraer
def extraer(texto: str, terminos: set[str], maximo: int = 2) -> list[str]:
    """Elige los párrafos que mejor responden: pesan más los términos poco frecuentes."""
    parrafos = [" ".join(p.split()) for p in re.split(r"\n\s*\n", texto)]
    parrafos = [p for p in parrafos if 80 <= len(p) <= 900 and not p.startswith("COPIA DE AULA")]
    vocabularios = [set(palabras(p)) for p in parrafos]
    frecuencia = {t: sum(t in v for v in vocabularios) for t in terminos}
    peso = {t: math.log(1 + len(parrafos) / n) for t, n in frecuencia.items() if n}
    puntuados = sorted(
        (
            (sum(peso[t] for t in terminos & v if t in peso), p)
            for p, v in zip(parrafos, vocabularios, strict=True)
        ),
        key=lambda par: par[0],
        reverse=True,
    )
    return [p for puntos, p in puntuados[:maximo] if puntos > 0]


# ------------------------------------------------------------------ 5-6. verificar e informar
def investigar(tema: str, cfg: Config, almacen, embeddings, redactor=None) -> dict:
    """Ejecuta una investigación completa dentro de los límites y devuelve el informe."""
    inicio = time.monotonic()
    consultas = planificar(tema, cfg)
    publicas, faltan, leidas, bytes_leidos, errores = [], [], {}, 0, []

    for consulta in consultas:
        hallado = False
        for fuente in buscar_fuentes(consulta):
            if time.monotonic() - inicio > cfg.max_segundos_investigacion:
                errores.append("limite_de_tiempo")
                break
            if fuente["id"] not in leidas:
                if len(leidas) >= cfg.max_fuentes:
                    continue  # límite de fuentes: no se abre una más
                try:
                    leidas[fuente["id"]] = leer_fuente(fuente, cfg)
                    bytes_leidos += len(leidas[fuente["id"]][0].encode())
                except Exception as exc:  # una fuente caída no tumba el trabajo
                    errores.append(f"{fuente['id']}:{type(exc).__name__}")
                    continue
            texto, origen = leidas[fuente["id"]]
            terminos = set(palabras(consulta)) | set(palabras(" ".join(fuente["temas"])))
            for extracto in extraer(texto, terminos, maximo=1):
                publicas.append(
                    {
                        "consulta": consulta,
                        "fuente_id": fuente["id"],
                        "titulo": fuente["titulo"],
                        "url": fuente["url"],
                        "origen": origen,
                        "extracto": extracto,
                    }
                )
                hallado = True
            if hallado:
                break
        if not hallado:
            faltan.append(consulta)

    # La parte «+ RAG»: la política interna sale de nuestra documentación, no de internet.
    interna = recuperar(cfg, almacen, embeddings, tema)
    informe = {
        "tema": tema,
        "estado": "parcial" if faltan or not publicas else "completo",
        "consultas": consultas,
        "politica_interna": [{"cita": f["cita"], "texto": f["texto"]} for f in interna["fragmentos"]],
        "informacion_publica": publicas,
        "faltan": faltan,
        "aviso": AVISO,
        "errores": errores,
        "limites": {
            "max_consultas": cfg.max_consultas,
            "max_fuentes": cfg.max_fuentes,
            "max_bytes_fuente": cfg.max_bytes_fuente,
            "max_segundos": cfg.max_segundos_investigacion,
        },
        "consumo": {
            "fuentes_leidas": len(leidas),
            "bytes_leidos": bytes_leidos,
            "segundos": round(time.monotonic() - inicio, 2),
            # None = desconocido. En el perfil doble no hay modelo: 0 llamadas.
            "llamadas_modelo": 0,
            "tokens": None,
            "coste_usd": None,
        },
    }
    informe["resumen"] = _resumen(informe)
    if redactor is not None:  # perfil real: el modelo redacta con las evidencias ya reunidas
        informe["resumen"], informe["consumo"]["tokens"] = redactor(informe)
        informe["consumo"]["llamadas_modelo"] = 1
    return informe


def _resumen(informe: dict) -> str:
    lineas = [f"Investigación {informe['estado']} sobre: {informe['tema']}."]
    for p in informe["politica_interna"][:2]:
        lineas.append(f"Política interna [{p['cita']}]: {p['texto']}")
    for e in informe["informacion_publica"]:
        lineas.append(f"Información pública [{e['fuente_id']}]: {e['extracto']}")
    if informe["faltan"]:
        lineas.append("Sin evidencia para: " + "; ".join(informe["faltan"]) + ".")
    lineas.append(informe["aviso"])
    return "\n".join(lineas)


# ------------------------------------------------------------------ ejecutor de trabajos
def procesar_pendientes(cfg: Config, almacen, embeddings, redactor=None, maximo: int = 10) -> list:
    """Toma trabajos pendientes y los ejecuta. Lo llama un proceso aparte de la API."""
    hechos = []
    for _ in range(maximo):
        trabajo = almacen.tomar_pendiente()
        if trabajo is None:
            break
        try:
            informe = investigar(trabajo["tema"], cfg, almacen, embeddings, redactor)
            almacen.guardar_trabajo(trabajo["trabajo_id"], informe["estado"], informe)
        except Exception as exc:
            almacen.guardar_trabajo(
                trabajo["trabajo_id"], "error", {"error": type(exc).__name__, "tema": trabajo["tema"]}
            )
        hechos.append(trabajo["trabajo_id"])
    return hechos
