"""S19 · Diapositivas 1–6: portada, QR y recorrido, y repaso breve del sistema."""
from deck_lib import *  # noqa: F401,F403

F_GMAIL = "Fuentes: temario (Gmail, 17/07/2026) y enunciado de S19 (ejercicios.docx, 29/09/2026)."
LOGOS = ("Logotipos: OpenTUI (opentui.com/opentui-logo-auto.svg, enlazado desde github.com/anomalyco/opentui), "
         "LangGraph (github.com/langchain-ai/langgraph, .github/images/logo-dark.svg), OpenRouter (openrouter.ai/brand, "
         "glyph-cloud y horizontal-cloud), PostgreSQL (kit de prensa de postgresql.org), Ragas (github.com/vibrantlabsai/ragas), "
         "Langfuse (github.com/langfuse/langfuse, icon256.png), Python (python.org), Docker (copia de S17) y pytest "
         "(github.com/pytest-dev/pytest). pgvector no publica logotipo: se rotula con su nombre e icono genérico. "
         "Descargas del 17/11 y 22/11/2026; detalle en fuentes/presentacion/README.md.")


def s01_portada(deck):
    def panel(sl):
        x0 = 517
        label(sl, x0, 70, 380, "Objetivo del temario")
        text(sl, x0, 88, 380, 58, "«Cerrar el ciclo de calidad: medir de forma rigurosa si un sistema de IA funciona bien "
             "antes y después de cada cambio.»", size=13, font=SERIF, color=TITLE)
        label(sl, x0, 158, 380, "Las cuatro partes y dónde las veremos")
        partes = [("Evaluación de modelos y métricas específicas", "Pruebas 1 y 2", AMBER),
                  ("Análisis avanzado y métricas de producción", "Langfuse: latencia, tokens, coste", BLUE),
                  ("Testing automatizado de agentes y pipelines RAG", "Grafo y prueba 3", CORAL),
                  ("Integración de la evaluación con la observabilidad", "Scores y consumo del juez", BLUE)]
        y = 178
        for t, d, col in partes:
            box(sl, x0, y, 380, 38, fill=CARD, radius=4)
            box(sl, x0, y, 3.5, 38, fill=col, radius=0)
            text(sl, x0 + 12, y + 5, 360, 14, t, size=10.5, color=TITLE, bold=True)
            text(sl, x0 + 12, y + 21, 360, 13, d, size=9.5, color=col)
            y += 43
        label(sl, x0, 356, 380, "Práctica asociada · opcional")
        text(sl, x0, 373, 380, 30, "Construir un sistema RAG completo desde cero con evaluación y testing integrados.",
             size=10.5, color=TEXT)
        x = x0
        for nombre in ("python.png", "langgraph-icon.png", "postgresql.png", "openrouter-glyph.png", "ragas-tile.png",
                       "langfuse.png", "docker-mark-white.png"):
            w, _ = logo(sl, nombre, x, 414, 60, 28)
            x += w + 14

    sl = cover(deck, "S19 · AI ENGINEER", "Evaluación y testing\nde sistemas de IA",
               "¿Cómo comprobamos qué ha cambiado y si empeoró el sistema? Repasamos el RAG de AetherCloud "
               "y hacemos tres pruebas reales: cambiar el generador, cambiar el juez y detectar una regresión.", panel)
    text(sl, 43, 342, 440, 32, "Martes 24/11/2026 · grupo M/J  ·  Lunes 30/11/2026 · grupo L/X\n18:30–20:00 · hora de Madrid",
         size=10.5, color=MUTED)
    notes(sl, """18:30. Portada mientras entran los alumnos. Presentar la pregunta que conduce la clase: «¿Cómo comprobamos qué ha cambiado y si empeoró el sistema?». El objetivo del temario es cerrar el ciclo de calidad. La clase es un repaso breve del sistema (cuatro diapositivas) y tres pruebas reales con modelos vía OpenRouter: cambiar el generador (T01 y T12), cambiar el juez (V02) y detectar una regresión del evaluador (T09). En cada prueba el grupo predice antes de ver el resultado.
Las cuatro partes del temario aparecen a lo largo de las pruebas: métricas específicas (recall@5, Faithfulness, Answer Relevancy), métricas de producción (latencia, tokens y coste en Langfuse), testing de agentes y pipelines RAG (trayectorias del grafo y la comprobación de T09) e integración con observabilidad (scores en la traza y consumo del juez aparte).
QUÉ ABRIR: nada todavía; terminal preparada en demo-evaluacion/ con Docker arrancado (checklist del guion del directo).
PREGUNTA: ¿cómo decidís hoy si un cambio de modelo o de prompt empeora vuestro sistema?
""" + F_GMAIL)
    return sl


def s02_qr(deck):
    sl = deck.slide(tag="qr")
    header_s(sl, "Antes de empezar", "Encuesta de S18 y recorrido de hoy")
    img(sl, "qr-ai-engineer.jpg", 390, 149.4, w=180, h=180)
    text(sl, 367.5, 336, 225, 41.2, "Encuesta de la sesión anterior ·\nS18", size=13.5, color=TITLE, bold=True,
         align="c")
    # qué se valora (izquierda)
    label(sl, 48, 150, 290, "Qué sesión valora el QR")
    side_note(sl, 48, 172, 300, 66, "Grupo M/J · directo del 24/11", "Valora la S18 del jueves 19/11/2026.", accent=MINT,
              size=11.5)
    side_note(sl, 48, 248, 300, 66, "Grupo L/X · directo del 30/11", "Valora la S18 del miércoles 25/11/2026.", accent=BLUE,
              size=11.5)
    # pregunta guía (derecha)
    label(sl, 612, 150, 300, "La pregunta de hoy")
    text(sl, 612, 170, 300, 80, "¿Cómo comprobamos qué ha cambiado y si empeoró el sistema?", size=19, font=SERIF,
         color=TITLE)
    pasos = [("1", "Predecís", MINT_L), ("2", "Ejecutamos", AMBER), ("3", "Contrastamos", MINT)]
    x = 612
    for n, t, col in pasos:
        badge(sl, x, 266, n, fill=col, d=20, size=10)
        text(sl, x + 25, 268, 80, 16, t, size=11, color=TITLE, bold=True)
        x += 100
    text(sl, 612, 294, 300, 30, "En cada prueba, la predicción va antes de la salida.", size=10.5, color=MUTED)
    # recorrido en una línea
    box(sl, 43, 392, 874, 104, fill=CARD, radius=6)
    label(sl, 57, 400, 400, "Recorrido · 18:30–20:00", color=MINT)
    etapas = [("Sistema", "herramientas · RAG\ngrafo · Langfuse", "3–6", MINT, False),
              ("Prueba 1 · Generador", "Hydrogen → Terra\nT01 y T12", "7–10", AMBER, True),
              ("Prueba 2 · Juez", "Sol → Opus\nV02 congelada", "11–12", VIOLET, True),
              ("Prueba 3 · Regresión", "¿coinciden los\njueces en T09?", "13–14", CORAL, True),
              ("Cierre", "evidencia y\npráctica opcional", "15", MINT_L, False)]
    xs = [57 + i * 172 for i in range(5)]
    box(sl, 70, 432, 790, 2, fill=BORDER, radius=0)
    for (t, d, rango, col, pred), x in zip(etapas, xs):
        circle(sl, x + 6, 425, 16, col)
        text(sl, x + 28, 422, 140, 14, t, size=10.5, color=col, bold=True)
        text(sl, x + 28, 438, 140, 30, d, size=9, color=TEXT)
        text(sl, x + 28, 470, 60, 12, f"diap. {rango}", size=8.5, color=MUTED, check=False)
        if pred:
            chip(sl, x + 86, 468, 70, 15, "? predicción", fill=MINT_L, color=DARK, size=7.5, radius=3)
    footer(sl)
    notes(sl, """18:30–18:33. El QR evalúa la sesión anterior de cada grupo: S18 del jueves 19/11 para M/J (directo del 24/11) y S18 del miércoles 25/11 para L/X (directo del 30/11). Mantenerlo dos minutos en pantalla.
Presentar el recorrido de abajo: cuatro diapositivas para repasar el sistema y tres pruebas reales. Las pruebas cambian una sola pieza cada vez: el generador (Gemini 4 Hydrogen frente a GPT‑6.1 Terra), el juez (GPT‑6.2 Sol frente a Claude Opus 5.5) y, en la tercera, el mismo cambio de juez sobre T09. En la línea solo se pregunta si los jueces coinciden en T09: no adelantar que falla, se revela en la diapositiva 14. En cada una el grupo hace una predicción antes de ver la salida («predecís, ejecutamos, contrastamos»), como pidió Laura: teoría mientras se hacen cosas. La práctica posterior es opcional.
QUÉ ABRIR: nada; comprobar que el QR se lee desde un móvil.
PREGUNTA: si cambiáis el modelo de vuestro sistema, ¿qué miraríais primero para saber si empeoró?
Fuentes: hilo de Gmail «Update Directos…» (Laura, 29/09, 19/10 y 04/11/2026; resumen en fuentes/indicaciones-laura.md); QR vigente copiado byte a byte de material/S16/assets.""")
    return sl


def _tool(sl, x, y, w, h, n, logos, nombre, funcion, detalle, accent, etapa):
    box(sl, x, y, w, h, fill=CARD, line=BORDER)
    box(sl, x, y, w, 3.5, fill=accent, radius=0)
    badge(sl, x + w - 26, y + 12, n, fill=accent, d=17, size=9)
    lx = x + 12
    for nm, wmax in logos:
        lw_, _ = logo(sl, nm, lx, y + 12, wmax, 26)
        lx += lw_ + 10
    if nombre:
        text(sl, lx, y + 15, x + w - 32 - lx, 20, nombre, size=12.5, color=TITLE, bold=True)
    text(sl, x + 12, y + 46, w - 24, 34, funcion, size=11, color=TITLE)
    text(sl, x + 12, y + h - 22, w - 70, 13, detalle, size=8.5, color=MUTED, font=MONO, bold=True, check=False)
    text(sl, x + w - 112, y + h - 22, 100, 13, etapa, size=8, color=accent, bold=True, align="r", check=False)


def s03_herramientas(deck):
    sl = deck.slide(tag="herramientas")
    header(sl, "Repaso del sistema · 1/4", "Qué vamos a usar y para qué",
           "Seis piezas, en el orden en que las recorre una pregunta. El color de cada etapa es el mismo en todo el deck.")
    cw, ch = 280, 112
    xs = [43, 340, 637]
    fila1 = [("1", [("opentui-logo.png", 110)], None, "Chat en terminal. Muestra el recorrido de cada pregunta por el grafo.",
              "python s19.py chat", MINT_L, "INTERFAZ"),
             ("2", [("langgraph-logo.png", 150)], None, "Ejecuta los pasos y elige la rama: generar o rechazo previo.",
              "rag/grafo.py", MINT_L, "ORQUESTA"),
             ("3", [("postgresql.png", 26), ("g-data-table.png", 24)], "PostgreSQL + pgvector",
              "Guarda los fragmentos con su vector y busca los más parecidos.", "índice A · 41 filas", ST_DATOS, "DATOS")]
    fila2 = [("4", [("openrouter-logo.png", 140)], None, "Da acceso a los modelos de generación, embeddings y juez.",
              "una clave · coste por llamada", ST_GEN, "MODELOS"),
             ("5", [("ragas-tile.png", 26)], "Ragas", "Puntúa respuestas ya guardadas: Faithfulness y Answer Relevancy.",
              "evaluador/ · ragas 0.4.3", ST_JUEZ, "JUEZ"),
             ("6", [("langfuse.png", 26)], "Langfuse", "Muestra trazas, puntuaciones y consumo de cada pregunta.",
              "consulta-rag · evaluador-ragas", ST_OBS, "OBSERVA")]
    for fila, y in ((fila1, 126), (fila2, 262)):
        for (n, lg, nom, fn, det, col, et), x in zip(fila, xs):
            _tool(sl, x, y, cw, ch, n, lg, nom, fn, det, col, et)
    for y in (182, 318):
        line(sl, 325, y, 338, y, color=MUTED, w=1.5)
        line(sl, 622, y, 635, y, color=MUTED, w=1.5)
    poly(sl, [(777, 239), (777, 250), (183, 250), (183, 260)], color=MUTED, w=1.25)
    # base
    box(sl, 43, 388, 874, 76, fill=BG, line=BORDER)
    label(sl, 55, 396, 300, "La base que lo sostiene", color=MUTED, size=8.5)
    base = [("python.png", 78, "Todo el código: s19.py, el grafo y el evaluador aislado (Python 3.12)."),
            ("docker-mark-white.png", 44, "PostgreSQL 17 + pgvector en un contenedor local."),
            ("pytest-tile.png", 30, "Tests con dobles: recorrido del grafo sin claves ni coste.")]
    for i, (nm, wm, t) in enumerate(base):
        x = 55 + i * 290
        w_, _ = logo(sl, nm, x, 416, wm, 30)
        text(sl, x + w_ + 10, 414, 270 - w_ - 10, 36, t, size=10, color=TEXT)
    # leyenda de color
    box(sl, 43, 476, 874, 26, fill=TAKE_BG, radius=4)
    text(sl, 54, 476, 140, 26, "COLOR POR ETAPA", size=9, color=MINT, bold=True, anchor="m")
    ley = [("Datos e índice", ST_DATOS), ("Recuperar", ST_RECUP), ("Generar", ST_GEN), ("Juzgar", ST_JUEZ),
           ("Observar", ST_OBS), ("Fallo", ST_FALLO)]
    x = 190
    for t, col in ley:
        box(sl, x, 485, 10, 10, fill=col, radius=2)
        text(sl, x + 15, 476, 100, 26, t, size=10.5, color=TITLE, anchor="m")
        x += 120
    footer(sl, block=1)
    notes(sl, """18:33–18:37. Recorrer las seis tarjetas en orden; son las piezas que tocará una pregunta en las pruebas. 1 OpenTUI: el chat de terminal (`python s19.py chat`); usa la librería Python opentui 0.1.2, enlace del motor OpenTUI, y pinta el grafo con el nodo activo. 2 LangGraph: ejecuta los nodos `recuperar`, `generar`, `comprobar` o `rechazo_previo` y decide la rama. 3 PostgreSQL + pgvector: una fila por fragmento con su vector; la búsqueda es exacta por coseno (sin HNSW, para no añadir otra variable). 4 OpenRouter: una sola clave da acceso a los modelos de generación (Hydrogen, Terra), embeddings (text-embedding-3-small) y juez (Sol, Opus); además devuelve el coste de cada llamada, que la demo guarda y envía a Langfuse. 5 Ragas: corre en un entorno aparte y puntúa respuestas guardadas en respuestas.jsonl. 6 Langfuse: trazas por pregunta, scores y consumo.
Abajo, la base: Python, Docker para PostgreSQL y pytest para los tests con dobles. La leyenda de colores se mantiene en todos los diagramas.
QUÉ ABRIR: el árbol de demo-evaluacion/ (rag/, evaluador/, datos/, tests/) para que vean que es un repositorio pequeño.
PREGUNTA: ¿qué pieza cambiaríais para abaratar el sistema y cuál para medirlo mejor?
Fuentes: demo-evaluacion/README.md y pyproject.toml (langgraph 1.2.11, opentui 0.1.2, langfuse 5.2.0, psycopg 3.3.9); esquema.sql; evaluador/pyproject.toml (ragas 0.4.3). """ + LOGOS)
    return sl


def s04_rag(deck):
    sl = deck.slide(tag="rag")
    header(sl, "Repaso del sistema · 2/4", "Qué es un RAG y qué guarda el nuestro",
           "Un RAG busca fragmentos de tus documentos y se los da al modelo para que responda citando. "
           "Del documento al índice hay tres pasos.")
    # 1 · documento
    label(sl, 43, 124, 260, "1 · Documento", color=ST_DATOS, size=9)
    box(sl, 43, 142, 262, 214, fill="F4F6F6", line=BORDER, radius=4)
    box(sl, 43, 142, 262, 20, fill="DDE3E5", radius=0)
    text(sl, 51, 146, 248, 12, "01-arquitectura-aethercloud.md", size=8.5, font=MONO, color=UI_TEXT, bold=True, check=False)
    text(sl, 53, 170, 244, 34, "# Arquitectura general de AetherCloud", size=11, font=SERIF, color=UI_TEXT, bold=True)
    text(sl, 53, 204, 244, 30, "AetherCloud opera en dos regiones europeas…", size=10, color=UI_MUTED)
    box(sl, 49, 234, 250, 72, fill="DDF3EA", line=ST_DATOS, lw=1.5, radius=3)
    text(sl, 57, 240, 236, 62, [[("El tráfico entrante atraviesa pasarelas perimetrales con terminación ", {"color": UI_TEXT}),
                                 ("TLS 1.3", {"bold": True, "color": "0B6E4F"}), (" obligatoria…", {"color": UI_TEXT})]],
         size=11)
    text(sl, 53, 314, 244, 34, "## Plano de control y plano de datos…", size=10, color=UI_MUTED)
    text(sl, 43, 360, 262, 14, "1 de 10 documentos ficticios", size=9.5, color=MUTED)
    line(sl, 309, 270, 337, 270, color=ST_DATOS, w=2)
    # 2 · fragmento
    label(sl, 341, 124, 260, "2 · Fragmento", color=ST_DATOS, size=9)
    for i in range(5):
        on = i == 2
        chip(sl, 341 + i * 53, 142, 49, 22, f"#0{i + 1}", fill=GREEN_BG if on else CARD2, color=MINT_L if on else MUTED,
             size=9.5, line=ST_DATOS if on else BORDER, radius=3, font=MONO)
    box(sl, 341, 174, 262, 182, fill=GREEN_BG, line=ST_DATOS, lw=1.5)
    text(sl, 353, 182, 240, 14, "01-arquitectura-aethercloud#03", size=9, font=MONO, color=MINT, bold=True)
    text(sl, 353, 202, 240, 150, [[("El tráfico entrante atraviesa pasarelas perimetrales Anycast con terminación ", {}),
                                   hl("TLS 1.3"), (" obligatoria. Ningún servicio de aplicación expone puertos "
                                                   "directamente a internet pública sin pasar por la pasarela regional.", {})]],
         size=12.5, color=TITLE)
    text(sl, 341, 360, 262, 14, "5 fragmentos de este documento · 41 en el índice A", size=9.5, color=MUTED)
    line(sl, 607, 270, 635, 270, color=ST_DATOS, w=2)
    # 3 · vector y fila
    label(sl, 639, 124, 278, "3 · Vector en PostgreSQL", color=ST_DATOS, size=9)
    box(sl, 639, 142, 278, 214, fill=CARD, line=ST_DATOS, lw=1.5)
    logo(sl, "postgresql.png", 651, 150, 26, 26)
    text(sl, 685, 154, 224, 18, "tabla fragmentos · una fila", size=10.5, color=TITLE, bold=True)
    filas = [("documento_id", "01-arquitectura-aethercloud", MONO, MINT_L),
             ("contenido", "el texto del fragmento #03", SANS, TITLE)]
    y = 186
    for k, v, f, col in filas:
        text(sl, 651, y, 254, 12, k, size=9, font=MONO, color=MUTED, bold=True)
        text(sl, 651, y + 14, 254, 16, v, size=11, font=f, color=col, bold=f == MONO)
        y += 40
    text(sl, 651, y, 254, 12, "embedding", size=9, font=MONO, color=MUTED, bold=True)
    for i in range(14):
        box(sl, 651 + i * 18, y + 16, 15, 24, fill=["2F6E5B", "3F8F74", "4FD1A1", "2A5246"][i % 4], radius=2)
    text(sl, 651 + 14 * 18, y + 18, 20, 20, "…", size=12, color=MINT_L, bold=True, check=False)
    text(sl, 651, y + 46, 254, 14, "768 números · valores no mostrados", size=9.5, color=MINT_L)
    text(sl, 639, 360, 278, 14, "La pregunta también se vectoriza para buscar.", size=9.5,
         color=MUTED)
    # fuera del índice
    box(sl, 43, 386, 874, 78, fill=BG, line=CORAL, lw=1.25, dash=True)
    chip(sl, 55, 379, 230, 15, "FUERA DEL ÍNDICE · NUNCA SE INDEXAN", fill=CORAL, color=DARK, size=8, radius=3)
    for i, (f, d) in enumerate([("validacion.jsonl", "8 preguntas · para elegir umbral y prompt"),
                                ("test.jsonl", "20 preguntas · para medir")]):
        x = 57 + i * 300
        img(sl, "g-json-script.png", x, 404, w=28, h=28)
        text(sl, x + 36, 402, 250, 16, f, size=12, font=MONO, color=TITLE, bold=True)
        text(sl, x + 36, 421, 250, 14, d, size=10, color=TEXT)
    text(sl, 660, 398, 246, 60, "Cada pregunta lleva sus documentos relevantes y su respuesta de referencia.",
         size=10.5, color=MUTED, anchor="m")
    takeaway(sl, "El índice guarda documentos troceados con su vector; preguntas y referencias quedan fuera para poder medir.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:37–18:42. Qué es un RAG en una frase: antes de responder, el sistema busca en tus documentos los fragmentos más parecidos a la pregunta y se los da al modelo, que debe citar de dónde saca cada dato. Tres pasos con un documento real del corpus (AetherCloud es una empresa inventada; los 10 documentos son ficticios): 1 el documento 01-arquitectura-aethercloud.md; 2 con chunk_size 320 se trocea en 5 fragmentos (41 en todo el índice A) y el #03 es el que contiene TLS 1.3; 3 cada fragmento es una fila de la tabla fragmentos con su documento, su texto y su vector de 768 números (los valores no se muestran). La pregunta se convierte en otro vector con el mismo modelo y pgvector busca los más parecidos.
La fila tiene más columnas, para quien pregunte: fragmento_id (01-arquitectura-aethercloud#03), ordinal 3, título del documento, contenido_hash (b97267ced40ffc3c…, evita duplicados) e indice_id, huella de corpus + fragmentación + modelo de embeddings: si cambia cualquiera de los tres, es otro índice.
Abajo, la separación: validacion.jsonl (8 preguntas: 5 + 3 sin respuesta) y test.jsonl (20: 14 + 6) guardan pregunta, documentos relevantes, datos clave y respuesta de referencia, y no se indexan nunca. Enseñar T01 en el archivo: será la primera prueba.
EN VIVO (opcional, sin coste): `uv run python s19.py preflight --env .env.hydrogen-sol` y buscar «índice presente (41 fragmentos)».
QUÉ ABRIR: corpus/01-arquitectura-aethercloud.md; esquema.sql (tabla fragmentos); datos/test.jsonl (T01).
PREGUNTA: ¿qué pasaría con la evaluación si test.jsonl estuviera dentro del corpus?
Fuentes: demo-evaluacion/esquema.sql; rag/corpus.py ejecutado sin red el 22/11/2026 sobre corpus/ (10 documentos, 41 fragmentos con chunk_size 320; contenido y huella del fragmento #03); datos/test.jsonl y datos/validacion.jsonl. La tira del vector es un dibujo: no representa valores reales.""")
    return sl


def _flujo(sl, y, titulo, nota, items, w=48, gap=4, x=43):
    text(sl, x, y, 260, 13, titulo, size=9.5, color=TITLE, bold=True)
    text(sl, x + 262, y, 360, 13, nota, size=8.5, color=MUTED, check=False)
    return chip_row(sl, x, y + 16, items, w=w, gap=gap)


def s05_grafo(deck):
    sl = deck.slide(tag="grafo")
    header(sl, "Repaso del sistema · 3/4", "Cómo funciona una pregunta: el grafo real",
           "rag/grafo.py en LangGraph: cuatro nodos y una decisión. Si la evidencia no llega al umbral, el generador ni se llama.")
    # grafo
    circle(sl, 43, 194, 18, TITLE)
    text(sl, 30, 214, 44, 12, "pregunta", size=8, color=MUTED, align="c", check=False)
    line(sl, 62, 203, 84, 203, color=MUTED, w=1.5)
    box(sl, 86, 176, 168, 56, fill=ST_RECUP_BG, line=ST_RECUP, lw=1.25)
    text(sl, 96, 182, 150, 16, "recuperar", size=12, font=MONO, color=ST_RECUP, bold=True)
    text(sl, 96, 200, 152, 28, "embedding de la pregunta → 12 fragmentos", size=9, color=TEXT)
    line(sl, 256, 204, 282, 204, color=MUTED, w=1.5)
    d = box(sl, 284, 164, 142, 80, fill=CARD2, line=MUTED, radius=0, shape=MSO_SHAPE.DIAMOND)
    shape_text(d, "¿mejor similitud\n≥ 0,5223?", size=9, color=TITLE)
    # rama sí
    poly(sl, [(355, 164), (355, 156), (450, 156)], color=ST_GEN, w=1.75)
    text(sl, 362, 140, 30, 12, "sí", size=9, color=ST_GEN, bold=True, check=False)
    box(sl, 452, 130, 170, 52, fill=ST_GEN_BG, line=ST_GEN, lw=1.25)
    text(sl, 462, 135, 150, 16, "generar", size=12, font=MONO, color=ST_GEN, bold=True)
    text(sl, 462, 153, 156, 26, "4 fragmentos + prompt v1 → modelo vía OpenRouter", size=9, color=TEXT)
    line(sl, 624, 156, 646, 156, color=ST_GEN, w=1.75)
    box(sl, 648, 130, 160, 52, fill=ST_GEN_BG, line=ST_GEN, lw=1.25)
    text(sl, 658, 135, 140, 16, "comprobar", size=12, font=MONO, color=ST_GEN, bold=True)
    text(sl, 658, 153, 146, 26, "NO_CONSTA del modelo, fuentes válidas y avisos", size=9, color=TEXT)
    line(sl, 810, 156, 830, 156, color=ST_GEN, w=1.75)
    chip(sl, 832, 140, 85, 32, "respuesta\n+ [fuente]", fill=CARD, color=TITLE, size=9, line=ST_GEN, radius=4)
    # rama no
    poly(sl, [(355, 244), (355, 252), (450, 252)], color=ST_SIN, w=1.75)
    text(sl, 362, 254, 30, 12, "no", size=9, color=ST_SIN, bold=True, check=False)
    box(sl, 452, 228, 356, 48, fill=CARD2, line=ST_SIN, lw=1.25)
    text(sl, 462, 233, 200, 16, "rechazo_previo", size=12, font=MONO, color=TITLE, bold=True)
    text(sl, 462, 251, 340, 22, "«No consta» sin llamar al generador: 0 tokens de generación", size=9.5, color=TEXT)
    line(sl, 810, 252, 830, 252, color=ST_SIN, w=1.75)
    chip(sl, 832, 236, 85, 32, "No consta", fill=CARD, color=TITLE, size=9, line=ST_SIN, radius=4)
    text(sl, 43, 250, 230, 40, "Los tests comprueban la trayectoria: qué nodos se recorren, no el texto.", size=9.5,
         color=MUTED)
    # embudo 12 → 5 → 4 (T01 real)
    box(sl, 43, 292, 874, 1, fill=BORDER, radius=0)
    label(sl, 43, 298, 600, "Dónde puede perderse un dato · T01 del ensayo del 22/11/2026", color=ST_RECUP, size=8.5)
    tag(sl, 640, 297, "ensayo")
    frs = ["01#03", "02#01", "02#02", "01#02", "01#01", "02#04", "01#04", "04#01", "09#01", "03#01", "01#05", "10#01"]
    rel = lambda f: f.startswith("01")  # noqa: E731
    it = [(f, GREEN_BG if rel(f) else CARD2, ST_DATOS if rel(f) else BORDER, MINT_L if rel(f) else MUTED) for f in frs]
    _flujo(sl, 316, "12 fragmentos candidatos", "orden de similitud · verde = documento relevante (01)", it)
    docs = [("01", True), ("02", False), ("04", False), ("09", False), ("03", False)]
    it = [(f"doc {d}", GREEN_BG if r else CARD2, ST_RECUP if r else BORDER, MINT_L if r else MUTED) for d, r in docs]
    _flujo(sl, 364, "hasta 5 documentos distintos", "con ellos se calculan recall@5 y precision@5", it, w=66)
    it = [(f, GREEN_BG if rel(f) else CARD2, ST_GEN, MINT_L if rel(f) else MUTED) for f in frs[:4]]
    _flujo(sl, 412, "4 fragmentos al prompt", "lo único que lee el generador (k_contexto = 4)", it)
    box(sl, 670, 316, 247, 146, fill=ST_FALLO_BG, line=ST_FALLO)
    label(sl, 682, 324, 225, "Ojo: recuperar ≠ leer", color=ST_FALLO, size=8.5)
    text(sl, 682, 342, 226, 116, [[("04, 09 y 03 cuentan entre los 5 documentos", {"bold": True, "color": TITLE}),
                                   (", pero ninguno de sus fragmentos entra en el prompt. Si un dato necesario "
                                    "estuviera solo ahí, recall@5 seguiría alto y el modelo no lo vería.", {})]],
         size=10.5, color=TEXT)
    text(sl, 682, 426, 226, 30, "En la prueba de T12 le pasa a un documento necesario.", size=9.5, color=ST_FALLO, bold=True)
    takeaway(sl, "Dos formas de no responder: por umbral, sin generar, o porque el modelo lee y dice NO_CONSTA, pagando la generación.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:42–18:47. Dibujar el recorrido real de rag/grafo.py. START → `recuperar`: se calcula el embedding de la pregunta y se piden 12 fragmentos a pgvector. Decisión `hay_evidencia`: si la mejor similitud es ≥ 0,5223 (umbral calibrado con validación) va a `generar` con los 4 primeros fragmentos y el prompt v1, y después a `comprobar`, que detecta el «NO_CONSTA» del modelo, valida que las fuentes citadas estén en el contexto y añade avisos. Si no llega, `rechazo_previo`: «No consta» sin llamar al generador, con 0 tokens de generación. Ojo: no es gratis del todo; `recuperar` ya calculó el embedding de la pregunta (rag/consulta.py, función recuperar) y con el perfil real esa llamada a OpenRouter puede tener coste. Los tests (tests/test_grafo.py y tests/test_enrutado.py) comprueban la trayectoria y la regla de enrutado, no el texto.
Abajo, el embudo con los datos reales de T01 en el ensayo: 12 fragmentos → 5 documentos distintos (01, 02, 04, 09, 03) → 4 fragmentos al prompt (01#03, 02#01, 02#02, 01#02). Lo importante: recall@5 cuenta documentos entre los cinco primeros, pero el generador solo lee 4 fragmentos. Aquí no hace daño porque el dato está en 01#03, el primero. Anunciar que en T12 veremos qué pasa cuando le ocurre a un documento necesario.
EN VIVO (sin coste): en el chat, escribir `6` (T17, región eu-par-1 que no existe): similitud 0,38 < 0,5223 → rama rechazo_previo; en el panel, generar y comprobar quedan sin recorrer.
QUÉ ABRIR: rag/grafo.py (construir_grafo y hay_evidencia); tests/test_grafo.py.
PREGUNTA: ¿qué rama es más barata y cuál puede equivocarse sin que lo notemos?
Fuentes: demo-evaluacion/rag/grafo.py y README.md (S19_K_FRAGMENTOS=12, S19_K_CONTEXTO=4); umbral 0,5223 de datos/calibracion.json y del guion del directo; fragmentos de T01 en resultados/ensayo-tres-pruebas-20261122/gemini-4-hydrogen-T01.txt (22/11/2026).""")
    return sl


def _lf_card(sl, x, y, w, h, n, titulo, obs, accent, fill):
    box(sl, x, y, w, h, fill=fill, line=accent, lw=1.25)
    badge(sl, x + 12, y + 12, n, fill=accent, color=DARK, d=22, size=11)
    text(sl, x + 42, y + 12, w - 54, 22, titulo, size=16, font=SERIF, color=TITLE)
    text(sl, x + 42, y + 36, w - 54, 14, obs, size=9.5, font=MONO, color=accent, bold=True)


def s06_langfuse(deck):
    sl = deck.slide(tag="langfuse")
    header(sl, "Repaso del sistema · 4/4", "Qué es Langfuse y cómo lo usaremos",
           "Una plataforma de observabilidad para aplicaciones con LLM: cada pregunta deja una traza. "
           "En el directo miraremos tres cosas; el detalle, en Brave.")
    tag(sl, 43, 122, "recreacion")
    text(sl, 220, 122, 520, 14, "Datos de V02 en la sesión langfuse-prueba-hydrogen, comprobados en Brave el 22/11/2026",
         size=8.5, color=MUTED, check=False)
    # migas de la traza
    box(sl, 43, 142, 874, 30, fill=UI_BG, line="AEB5BD", radius=4)
    text(sl, 55, 142, 600, 30, "Sessions  ›  langfuse-prueba-hydrogen  ›  traza consulta-rag (V02)", size=11,
         color=UI_BLUE, bold=True, anchor="m")
    text(sl, 660, 142, 246, 30, "s19 · config:A · perfil:real", size=9, color=UI_LABEL, align="r", anchor="m")
    W, G, Y, H = 280, 17, 184, 190
    x1, x2, x3 = 43, 43 + W + G, 43 + 2 * (W + G)
    _lf_card(sl, x1, Y, W, H, 1, "Qué recuperó", "observación recuperacion", ST_RECUP, ST_RECUP_BG)
    chip(sl, x1 + 14, Y + 62, W - 28, 26, "03-limites-y-cuotas-api", fill=GREEN_BG, color=MINT_L, size=11, font=MONO,
         line=ST_DATOS, radius=4)
    text(sl, x1 + 14, Y + 94, W - 28, 40, "y 4 documentos más (09, 10, 06, 08)", size=11, color=TEXT)
    text(sl, x1 + 14, Y + 140, W - 28, 40, [[("mejor similitud ", {}), ("0,78", {"bold": True, "color": TITLE, "size": 18})]],
         size=11, color=TEXT)
    _lf_card(sl, x2, Y, W, H, 2, "Qué respondió", "observación generacion", ST_GEN, ST_GEN_BG)
    text(sl, x2 + 14, Y + 62, W - 28, 84, [[("«El tamaño máximo de cuerpo permitido en cualquier petición POST es de ", {}),
                                             hl("4 MiB", TITLE), (" ", {}), hl("[03-limites-y-cuotas-api]", ST_GEN), ("»", {})]],
         size=12.5, color=TEXT)
    text(sl, x2 + 14, Y + 160, W - 28, 16, "google/gemini-4-hydrogen", size=10, font=MONO, color=MUTED, bold=True)
    _lf_card(sl, x3, Y, W, H, 3, "Cuánto costó", "generacion · usage y cost", ST_OBS, ST_OBS_BG)
    text(sl, x3 + 14, Y + 62, W - 28, 36, "0,001793 USD", size=26, font=SERIF, color=TITLE)
    text(sl, x3 + 14, Y + 104, W - 28, 20, "390 → 161 tokens · 1,66 s", size=13, color=TITLE, bold=True)
    text(sl, x3 + 14, Y + 132, W - 28, 50, "Coste devuelto por OpenRouter; la demo lo envía a Langfuse tal cual.",
         size=10.5, color=TEXT)
    for xa in (x1 + W, x2 + W):
        line(sl, xa + 2, Y + H / 2, xa + G - 2, Y + H / 2, color=MUTED, w=1.5)
    # detalle y juez aparte
    box(sl, 43, 386, 560, 78, fill=CARD)
    label(sl, 55, 394, 540, "En Brave, para quien quiera el detalle", color=ST_OBS, size=8.5)
    text(sl, 55, 412, 540, 48, [[("Metadata: ", {"bold": True, "color": TITLE}), ("caso y configuración (modelo, k, prompt).  ", {}),
                                 ("Scores: ", {"bold": True, "color": TITLE}),
                                 ("recall_at_5, acierto_criterio, faithfulness 1,0000 y answer_relevancy 0,9566.", {})]],
         size=10.5, color=TEXT)
    box(sl, 615, 386, 302, 78, fill=ST_JUEZ_BG, line=ST_JUEZ)
    label(sl, 627, 394, 280, "Aparte: evaluador-ragas → consumo-juez", color=ST_JUEZ, size=8.5)
    text(sl, 627, 412, 280, 48, [[("Sol juzga V02: ", {}), ("0,010643 USD", {"bold": True, "color": TITLE}),
                                  (". No se suma al coste de responder.", {})]], size=10.5, color=TEXT)
    takeaway(sl, "Una traza por pregunta: qué recuperó, qué respondió y cuánto costó. El juez, en su propia traza.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:47–18:52. Qué es Langfuse: una plataforma de observabilidad para aplicaciones con LLM. Guarda trazas (una por pregunta), observaciones (los pasos), metadatos y puntuaciones (scores). La diapositiva es una RECREACIÓN con los datos comprobados en Brave el 22/11/2026 en la sesión langfuse-prueba-hydrogen del proyecto s19-evaluacion (región UE); no es una captura, para no exponer claves ni otros metadatos de la cuenta.
En pantalla, solo tres cosas de la traza consulta-rag de V02: 1 qué recuperó (observación recuperacion, tipo retriever): 03-limites-y-cuotas-api y otros cuatro documentos, mejor similitud 0,78, 677 ms; 2 qué respondió (observación generacion): «4 MiB» con la cita, modelo google/gemini-4-hydrogen; 3 cuánto costó: 390 → 161 tokens, 1,66 s y 0,001793 USD. El coste no lo calcula Langfuse con su catálogo: la demo toma el que devuelve OpenRouter (coste_fuente = openrouter) y lo envía en cost_details.
Después abrir Brave para el detalle: sesión, etiquetas s19 · config:A · perfil:real, Metadata (caso_id V02, config_id A, gen_modelo, embedding_modelo, k_fragmentos 12, k_contexto 4, prompt_version v1) y Scores (recall_at_5 1,00, precision_at_5 0,20, acierto_criterio 1, rechazo 0 y, tras publicar el evaluador, faithfulness 1,0000 y answer_relevancy 0,9566). Aparte, la traza evaluador-ragas con la observación consumo-juez: openai/gpt-6.2-sol, 3.745 → 253 tokens, 0,010643 USD. Va aparte para no mezclar el coste de responder con el de juzgar.
QUÉ ABRIR: Langfuse → Sessions → langfuse-prueba-hydrogen → V02 (pantalla compartida sin .env ni ajustes de claves); rag/observabilidad.py (consulta y registrar_evaluador).
PREGUNTA: ¿por qué no sumar el coste del juez al coste por consulta?
Fuentes: verificacion.md, secciones «Langfuse Cloud · 22/11/2026» y «Corrección del consumo del juez»; resultados/langfuse-prueba-hydrogen (respuestas.jsonl, puntuaciones.jsonl e informe.json, caso V02); rag/observabilidad.py; rag/config.py (Config.publica).""")
    return sl


SLIDES = [s01_portada, s02_qr, s03_herramientas, s04_rag, s05_grafo, s06_langfuse]
