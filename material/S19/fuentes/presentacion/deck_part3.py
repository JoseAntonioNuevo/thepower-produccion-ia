"""S19 · Diapositivas 27–32: bloque 5 (producción y observabilidad), práctica y cierre."""
from deck_lib import *  # noqa: F401,F403


def s24_comparar(deck):
    sl = deck.slide(tag="comparar")
    header(sl, "En vivo 5 · Comparar configuraciones", "Dos configuraciones, una sola variable distinta",
           "Volvemos al caso: chunk_size 320 frente a 900. Si cambian dos cosas a la vez, no se sabe cuál explica la "
           "diferencia. Mismo test, mismos modelos y mismo evaluador.")
    box(sl, 43, 128, 286, 208, fill=CARD)
    text(sl, 55, 136, 260, 12, "ANTES DE COMPARAR, EL COMANDO COMPRUEBA", size=8.5, color=BLUE, bold=True)
    checks = ["Mismo conjunto y misma huella de preguntas.", "Mismo perfil y mismos modelos.",
              "Mismo evaluador: juez, embeddings y versión de Ragas.", "Exactamente una variable distinta.",
              "Todos los casos presentes en las dos ejecuciones."]
    y = 156
    for c in checks:
        badge(sl, 55, y, "✓", fill=MINT, d=14, size=8)
        text(sl, 74, y, 246, 28, c, size=10, color=TEXT)
        y += 34
    term(sl, 43, 344, 286, 122, [
        ("$ python s19.py comparar \\", MINT_L),
        ("    resultados/mi-test-A \\", MINT_L),
        ("    resultados/mi-test-C", MINT_L),
        "",
        ("ERROR · ComparacionInvalida: deben", CORAL),
        ("diferir en exactamente una variable", CORAL),
        ("y difieren en 2: chunk_size, k_contexto", CORAL),
    ], title="SI UNA TERCERA EJECUCIÓN CAMBIA DOS VARIABLES", size=8.5)
    tag(sl, 343, 128, "salida")
    table(sl, 343, 148, 574, [234, 90, 90, 160], [
        ["Métrica · test de 20 preguntas", "A · 320", "B · 900", "B − A"],
        ["precision@5 (techo 0,24)", ("0,24", {"align": "r"}), ("0,24", {"align": "r"}), ("0,00", {"align": "r"})],
        ["recall@5", ("1,00", {"align": "r"}), ("1,00", {"align": "r"}), ("0,00", {"align": "r"})],
        ["Rechazos correctos", ("2/6", {"align": "r"}), ("4/6", {"align": "r"}), ("+2  mejora", {"align": "r", "color": MINT_L, "bold": True})],
        ["Abstenciones incorrectas", ("4/14", {"align": "r"}), ("8/14", {"align": "r"}), ("+4  empeora", {"align": "r", "color": CORAL, "bold": True})],
        ["Aciertos por criterio", ("6/14", {"align": "r"}), ("3/14", {"align": "r"}), ("−3  empeora", {"align": "r", "color": CORAL, "bold": True})],
        ["faithfulness · media (cobertura)", ("1,00 (14/14)", {"align": "r"}), ("1,00 (8/8)", {"align": "r"}), ("0,00", {"align": "r"})],
        ["answer_relevancy · media", ("0,44", {"align": "r"}), ("0,53", {"align": "r"}), ("+0,08", {"align": "r"})],
        ["Coste del sistema y del juez", ("sin dato", {"align": "r"}), ("sin dato", {"align": "r"}), ("sin dato", {"align": "r", "color": MUTED})],
    ], size=9.5, row_h=21, bold_cols=(0,), colors={0: MINT_L})
    box(sl, 343, 346, 281, 120, fill=AMBER_BG)
    text(sl, 355, 354, 260, 12, "CÓMO SE LEE", size=8.5, color=AMBER, bold=True)
    text(sl, 355, 371, 260, 92, "B rechaza mejor, pero se abstiene el doble y acierta la mitad. El umbral de evidencia "
         "se calibró con el índice A; con fragmentos de 900 las similitudes bajan y deja de valer. La media de "
         "fidelidad no se entera: sigue en 1,00.", size=9.5, color=TEXT)
    box(sl, 636, 346, 281, 120, fill=CARD)
    text(sl, 648, 354, 260, 12, "LO QUE LA TABLA NO PERMITE AFIRMAR", size=8.5, color=CORAL, bold=True)
    bullets(sl, 648, 371, 262, 92, ["Perfil doble: no dice cuál es mejor con un modelo real.",
                                     "20 preguntas: una diferencia de 1 o 2 casos puede ser ruido.",
                                     "«Sin dato» en coste: el doble no consume tokens; no es cero."],
            size=9.5, mark_color=CORAL, space=3)
    takeaway(sl, "Una comparación vale si solo cambia una cosa y se publica entera: lo que mejora, lo que empeora y lo que no se pudo medir.",
             label="Idea guía")
    footer(sl, block=5)
    notes(sl, """19:38–19:42. EN VIVO 5. Volver al caso de la diapositiva 6. Ejecutar los lotes de test de A y B (o usar los ya generados), evaluarlos e informar, y después `comparar`. Leer la tabla, que es la salida real del perfil doble: la recuperación no cambia; B rechaza mejor (4/6 frente a 2/6) pero se abstiene el doble en preguntas respondibles (8/14 frente a 4/14) y acierta menos (3/14 frente a 6/14). Explicar la causa: el umbral de evidencia se calibró con el índice A y no vale para fragmentos de 900 caracteres. Señalar que la media de fidelidad no detecta nada. Enseñar que el comando se niega a comparar si cambian dos variables o si el evaluador es distinto. Recordar los tres límites de la derecha.
QUÉ ABRIR: terminal; datos/configuraciones.json; resultados/ejemplo-doble/comparacion-A-B/comparacion.md.
PREGUNTA: ¿por qué no sirve comparar A y B si además he cambiado el prompt?
Fuentes: salida real de `s19.py comparar` (resultados/ejemplo-doble/comparacion-A-B, perfil doble, 17/11/2026); enunciado de S19 («Compara y observa»).""")
    return sl


def s25_produccion(deck):
    sl = deck.slide(tag="produccion")
    header(sl, "Análisis avanzado y métricas de producción", "En producción no hay respuestas de referencia",
           "El conjunto de test mide lo que previmos. Los usuarios preguntan otras cosas. En producción se observa "
           "el comportamiento y se analiza por segmentos, no con una sola media.")
    metricas = [("g-metrics.png", "Latencia", "p50 y p95 por paso: recuperar, generar, total.", BLUE),
                ("g-logs.png", "Tokens y coste", "Por consulta y por versión; el del juez, aparte.", AMBER),
                ("g-shield.png", "Tasa de rechazo", "Si sube de golpe, falta contenido o cambió el umbral.", VIOLET),
                ("g-alert.png", "Errores", "Proveedor, tiempo agotado, respuesta sin fuentes.", CORAL),
                ("g-user.png", "Opinión del usuario", "Valoración positiva o negativa y motivo.", MINT),
                ("g-magnifier.png", "Deriva", "Preguntas nuevas que el corpus no cubre.", PINK)]
    for i, (ic, t, d, col) in enumerate(metricas):
        x = 43 + (i % 3) * 196
        y = 128 + (i // 3) * 88
        box(sl, x, y, 188, 80, fill=CARD)
        box(sl, x, y, 3.5, 80, fill=col, radius=0)
        img(sl, ic, x + 12, y + 10, w=24, h=24)
        text(sl, x + 44, y + 12, 136, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, x + 12, y + 40, 168, 36, d, size=9.5, color=TEXT)
    # percentiles
    box(sl, 631, 128, 286, 168, fill=CARD)
    tag(sl, 643, 137, "ilustrativo")
    text(sl, 643, 158, 262, 18, "La media esconde la cola", size=12.5, font=SERIF, color=TITLE)
    for i, (lab, v, frac, col) in enumerate([("p50", "0,8 s", 0.13, MINT), ("media", "1,2 s", 0.20, MUTED),
                                             ("p95", "2,9 s", 0.48, AMBER), ("máximo", "6,1 s", 1.0, CORAL)]):
        yy = 184 + i * 21
        text(sl, 643, yy, 50, 14, lab, size=9.5, color=TITLE, bold=True, check=False)
        bar(sl, 696, yy + 3, 156, 8, frac, color=col)
        text(sl, 858, yy, 50, 14, v, size=9.5, color=col, bold=True, font=MONO, check=False)
    text(sl, 643, 270, 262, 24, "Uno de cada veinte usuarios espera más que el p95.", size=9, color=MUTED)
    # análisis avanzado
    table(sl, 43, 306, 874, [170, 352, 352], [
        ["Análisis", "Qué se hace", "Qué decisión permite"],
        ["Segmentar", "Separar por tipo de pregunta, documento citado, versión y configuración", "Encontrar dónde falla en vez de una media que lo tapa"],
        ["Comparar versiones", "Etiquetar cada traza con config_id y versión del prompt", "Saber si el cambio de ayer empeoró algo hoy"],
        ["Muestrear con juez", "Puntuar una muestra de respuestas reales, con su cobertura", "Estimar fidelidad sin evaluar todo el tráfico"],
        ["Analizar errores", "Leer los peores casos y clasificarlos por causa", "Convertir fallos reales en casos nuevos del conjunto"],
        ["Alertar", "Umbrales sobre p95, coste, rechazo y errores", "Enterarse antes que el usuario"],
    ], size=9.5, row_h=26.5, bold_cols=(0,), colors={0: MINT_L})
    takeaway(sl, "Antes de desplegar se mide contra referencias; después se observa sin ellas. Lo que falla en producción vuelve al conjunto.",
             label="Idea guía")
    footer(sl, block=5)
    notes(sl, """19:42–19:45. Segunda parte del temario: análisis avanzado y métricas de producción. La diferencia clave: en producción no hay respuesta de referencia, así que no se puede calcular recall ni acierto. Se observan seis señales: latencia en percentiles y por paso; tokens y coste por consulta; tasa de rechazo; errores; opinión del usuario; y deriva de las preguntas. Explicar por qué percentiles y no medias con el gráfico ilustrativo: la media esconde la cola. Recorrer la tabla de análisis: segmentar, comparar versiones, muestrear con juez (siempre con cobertura), analizar errores y alertar. La demo ya registra por consulta latencia de recuperación y generación, tokens, coste, rechazo y la configuración usada, y el informe resume el bloque «Producción»: p50 y p95, tasas de error y de rechazo (separando las que no llaman al modelo), coste por consulta y por 1.000 consultas, y peso del juez en el coste. El gráfico es ilustrativo; cifras reales en resultados/ejemplo-real/modelos (Sol: p95 1,9 s; Hydrogen: 3,6 s).
QUÉ ABRIR: un respuestas.jsonl para ver latencia_ms, tokens y coste_usd por caso.
PREGUNTA: ¿qué nos dice una tasa de rechazo que pasa del 10 % al 35 % en una semana?
Fuentes: temario de S19; campos registrados por demo-evaluacion/rag/grafo.py e informe de evaluacion/informe.py; documentación de Langfuse sobre tokens y coste (consultada el 16/11/2026).""")
    return sl


def s26_langfuse(deck):
    sl = deck.slide(tag="langfuse")
    header(sl, "Evaluación y observabilidad", "Cada consulta deja una traza; cada métrica, una puntuación",
           "La evaluación se integra con la observabilidad cuando la nota se guarda junto a la traza que la produjo. "
           "En Langfuse: respuesta, fuentes, latencia, tokens, coste y métricas en el mismo sitio.")
    tag(sl, 43, 124, "esquema")
    tag(sl, 215, 124, "pendiente", t="NO EJECUTADO CONTRA UN SERVIDOR LANGFUSE")
    # traza de consulta
    box(sl, 43, 146, 560, 232, fill=CARD, line=BLUE)
    img(sl, "langfuse.png", 55, 155, w=24, h=24)
    text(sl, 86, 156, 300, 12, "TRAZA · consulta-rag", size=9, color=BLUE, bold=True)
    text(sl, 86, 169, 500, 12, "sesión = ejecución · etiquetas: s19, config:A, perfil · id determinista por caso", size=8.5, color=MUTED)
    obs = [("recuperacion", "retriever", "entrada: pregunta\nsalida: documentos, mejor similitud\nmetadatos: modelo de embeddings, k", PINK, PINK_BG),
           ("generacion", "generation", "modelo y versión del prompt\nusage_details: tokens de entrada y salida\ncoste: lo calcula Langfuse con el precio del modelo", AMBER, AMBER_BG)]
    for i, (nombre, tipo, d, col, fill) in enumerate(obs):
        x = 55 + i * 270
        box(sl, x, 190, 262, 88, fill=fill)
        text(sl, x + 10, 197, 150, 14, nombre, size=10.5, font=MONO, color=TITLE, bold=True, check=False)
        chip(sl, x + 178, 196, 74, 15, tipo, fill=col, color=DARK, size=8, radius=3)
        text(sl, x + 10, 216, 244, 60, d, size=9, color=TEXT)
    text(sl, 55, 288, 300, 12, "SALIDA Y METADATOS", size=8.5, color=MUTED, bold=True)
    text(sl, 55, 303, 262, 40, "respuesta, fuentes, rechazo, documentos recuperados, latencia por paso, coste estimado",
         size=9.5, color=TEXT)
    text(sl, 325, 288, 270, 12, "PUNTUACIONES (create_score)", size=8.5, color=MUTED, bold=True)
    xs, ys = 325, 303
    for i, s_ in enumerate(["precision_at_5", "recall_at_5", "rechazo", "acierto_criterio", "faithfulness", "answer_relevancy"]):
        col = AMBER if i >= 4 else MINT
        w = len(s_) * 4.9 + 12
        if xs + w > 595:
            xs, ys = 325, ys + 20
        chip(sl, xs, ys, w, 16, s_, fill=CARD2, color=col, size=8, line=col, radius=3, font=MONO)
        xs += w + 5
    text(sl, 55, 354, 540, 20, "Una métrica que no se pudo calcular no se publica como 0: simplemente no hay puntuación.",
         size=9, color=MUTED)
    # traza del evaluador
    box(sl, 43, 388, 560, 78, fill=CARD, line=AMBER)
    img(sl, "ragas-tile.png", 55, 398, w=24, h=24)
    text(sl, 86, 397, 300, 12, "OTRA TRAZA · evaluador-ragas", size=9, color=AMBER, bold=True)
    chip(sl, 510, 396, 82, 15, "evaluator", fill=AMBER, color=DARK, size=8, radius=3)
    text(sl, 86, 412, 506, 50, "Modelo del juez, tokens y llamadas del juez, y la traza de consulta a la que puntúa. "
         "Va aparte para que el coste de juzgar no se sume al coste de responder.", size=9.5, color=TEXT)
    # derecha
    box(sl, 617, 124, 300, 150, fill=BLUE_BG)
    text(sl, 629, 133, 280, 12, "LO QUE PIDE EL ENUNCIADO REGISTRAR", size=8.5, color=BLUE, bold=True)
    bullets(sl, 629, 151, 280, 120, ["Respuesta y fuentes.", "Métricas de recuperación y de generación.",
                                      "Latencia, tokens y coste por consulta.",
                                      "El consumo del evaluador, separado."], size=10, mark_color=BLUE, space=4)
    box(sl, 617, 284, 300, 182, fill=AMBER_BG)
    text(sl, 629, 293, 280, 12, "SI FALTA EL COSTE", size=8.5, color=AMBER, bold=True)
    text(sl, 629, 311, 280, 150, [
        {"runs": [("1 · ¿Llegan los tokens? ", {"bold": True, "color": TITLE}),
                  ("Sin usage_details no hay coste: Langfuse no lo estima a partir del texto.", {})], "space": 5},
        {"runs": [("2 · ¿Coincide el modelo? ", {"bold": True, "color": TITLE}),
                  ("El nombre debe casar con una definición de modelo.", {})], "space": 5},
        {"runs": [("3 · ¿Tiene precio? ", {"bold": True, "color": TITLE}),
                  ("Si no existe, se define en Project Settings → Models con su precio por tipo de uso.", {})]},
    ], size=9.5, color=TEXT, space=5)
    takeaway(sl, "La nota vive junto a la traza: desde una puntuación baja se llega a la pregunta, los documentos y el coste exactos.",
             label="Idea guía")
    footer(sl, block=5)
    notes(sl, """19:45–19:49. Cuarta parte del temario: integración de la evaluación con las herramientas de observabilidad. Enlazar con S6 (Langfuse). Explicar el esquema, que describe lo que hace rag/observabilidad.py: una traza por consulta con dos observaciones (recuperación, de tipo retriever; generación, de tipo generation, con modelo y tokens) y las métricas publicadas como puntuaciones numéricas sobre esa traza. El identificador de traza es determinista por ejecución y caso, así el evaluador, que corre después y en otro entorno, puntúa la misma traza. El consumo del juez va en otra traza para separar el coste de juzgar del de responder, como pide el enunciado. Si falta el coste: comprobar tokens, nombre del modelo y definición de precio. IMPORTANTE: es un esquema, no una captura; en esta preparación Langfuse está apagado y no se ha enviado nada a ningún servidor. Sí se han probado las llamadas al SDK sin red.
QUÉ ABRIR: rag/observabilidad.py (consulta y registrar_evaluador).
PREGUNTA: ¿por qué no sumar el coste del juez al coste por consulta?
Fuentes: Langfuse, «Token and cost tracking» y «Scores via SDK» (langfuse.com/docs, consultadas el 16/11/2026); tests/test_observabilidad.py con langfuse==5.2.0 (17/11/2026); enunciado de S19.""")
    return sl


def s27_ciclo(deck):
    sl = deck.slide(tag="ciclo")
    header(sl, "Cerrar el ciclo de calidad", "De la traza de producción al siguiente caso de test",
           "Evaluar no es un paso final: es un circuito. Lo que se observa en producción alimenta el conjunto con el "
           "que se decide el siguiente cambio.")
    nodos = [("1", "Cambio", "prompt, fragmento,\nmodelo o umbral", MINT, 43),
             ("2", "Tests con dobles", "segundos · en cada\ncambio", VIOLET, 191),
             ("3", "Evaluar en validación", "recuperación, rechazo,\ngeneración", PINK, 339),
             ("4", "Control de regresión", "pasa o falla · código\nde salida", AMBER, 487),
             ("5", "Medir en test", "una vez · tabla\ncomparativa", BLUE, 635),
             ("6", "Desplegar y observar", "trazas, coste,\nrechazo, opinión", MINT_L, 783)]
    for n, t, d, col, x in nodos:
        box(sl, x, 132, 134, 96, fill=CARD)
        box(sl, x, 132, 134, 3, fill=col, radius=0)
        badge(sl, x + 10, 144, n, fill=col, d=18, size=9.5)
        text(sl, x + 10, 168, 118, 16, t, size=10.5, color=TITLE, bold=True)
        text(sl, x + 10, 188, 118, 36, d, size=9, color=TEXT)
        if x < 783:
            line(sl, x + 136, 180, x + 146, 180, color=MUTED)
    # retorno
    poly(sl, [(850, 230), (850, 252), (110, 252), (110, 232)], color=MINT, dash=True)
    chip(sl, 330, 242, 300, 20, "los fallos reales se convierten en casos nuevos", fill=TAKE_BG, color=MINT_L, size=9,
         line="2A5246")
    table(sl, 43, 276, 560, [120, 220, 220], [
        ["", "Antes de desplegar (offline)", "En producción (online)"],
        ["Datos", "Conjunto fijo con referencias", "Tráfico real, sin referencias"],
        ["Qué responde", "¿Este cambio empeora algo?", "¿Sigue funcionando para los usuarios?"],
        ["Métricas", "precision, recall, rechazo, juez, aciertos", "latencia, coste, rechazo, errores, opinión"],
        ["Quién decide", "El control de regresión", "Alertas y revisión de trazas"],
        ["Riesgo", "Conjunto pequeño o envejecido", "Ver el problema cuando ya ocurrió"],
    ], size=9.5, row_h=31.5, bold_cols=(0,), colors={0: MINT_L})
    box(sl, 617, 276, 300, 190, fill=GREEN_BG)
    text(sl, 629, 285, 280, 12, "CÓMO CRECE EL CONJUNTO", size=8.5, color=MINT, bold=True)
    bullets(sl, 629, 303, 278, 160, [
        "Una traza con mala valoración se convierte en un caso con su referencia.",
        "Entra primero en validación; al test solo en una versión nueva del conjunto.",
        "La huella del conjunto cambia: los resultados antiguos dejan de ser comparables.",
        "Los datos reales se anonimizan antes de guardarse.",
    ], size=9.5, space=5)
    takeaway(sl, "Cada fallo real que entra en el conjunto es una regresión que no volverá a pasar inadvertida.", label="Idea guía")
    footer(sl, block=5)
    notes(sl, """19:49–19:51. Unir todo en un circuito, que es el objetivo del temario: cerrar el ciclo de calidad. Seis pasos: cambio; tests con dobles; evaluación en validación; control de regresión; medición en test; despliegue y observación. La flecha de retorno es la clave: las trazas con mala valoración, los rechazos inesperados y los errores se convierten en casos nuevos con su referencia. Entran primero en validación; el test solo cambia en una versión nueva del conjunto, y entonces su huella cambia y los resultados anteriores dejan de ser comparables (la demo lo comprueba con la huella del conjunto). Recorrer la tabla offline frente a online. Recordar que los datos reales se anonimizan.
QUÉ ABRIR: nada.
PREGUNTA: un usuario reporta una respuesta inventada. ¿Cuáles son los tres pasos siguientes?
Fuentes: temario de S19 («cerrar el ciclo de calidad… antes y después de cada cambio»); evaluacion/conjuntos.py (huella del conjunto).""")
    return sl


def s28_practica(deck):
    sl = deck.slide(tag="practica")
    header_s(sl, "Práctica opcional", "Construir un RAG con evaluación y tests desde el inicio",
             "Enunciado de S19: reconstruir desde documentos en bruto, medir por separado y demostrar si un cambio mejora o empeora.")
    kv_rows_s(sl, 150, [
        ("Construir", "Ocho documentos ficticios tuyos → fragmentos → pgvector; respuesta con fuentes y rechazo."),
        ("Preparar", "20 preguntas (14 + 6), validación aparte y criterios fechados antes de ejecutar."),
        ("Medir", "precision@5 y recall@5 sobre documentos; rechazo aparte; Ragas aislado con cobertura."),
        ("Comprobar", "Cinco respuestas revisadas a mano; no evaluables con su motivo."),
        ("Comparar", "Dos configuraciones con una sola variable distinta; trazas, tokens y coste."),
        ("Automatizar", "pytest con dobles, marcador llm y un control de regresión que falla cuando debe."),
    ], pitch=44, size=13.5, kw=150)
    tag(sl, 48, 422, "real")
    text(sl, 290, 423, 610, 26, "Gemini 4 Hydrogen genera y Claude Opus 5.5 juzga, vía OpenRouter: una pasada completa costó 1,29 USD "
         "medidos (1,20 el juez). Test A: 13/14 aciertos y 6/6 rechazos. Con el perfil doble, 0.", size=9.5, color=MUTED)
    band_s(sl, "Guía paso a paso en demo-evaluacion/docs/ejercicio.md · 7–9 horas · se entrega código, datos, tests y tabla comparativa.")
    footer_s(sl)
    notes(sl, """19:51–19:55. Presentar la práctica, que es opcional (indicación de la escuela del 04/11/2026). Leer las seis filas, que resumen el enunciado: construir desde documentos en bruto e índice vacío; preparar 20 preguntas y validación aparte con criterios fijados antes; medir recuperación y generación por separado; comprobar puntuaciones con revisión manual y no evaluables; comparar dos configuraciones cambiando una variable y registrar en Langfuse; automatizar con pytest y demostrar la regresión. Entrega: implementación, datos, entorno bloqueado, tests y tabla comparativa con fallos y cobertura. Se valoran la reconstrucción completa, las métricas separadas, la trazabilidad y las regresiones útiles. Ejecutar `python s19.py estimar` para enseñar el gasto previsto del perfil real (2,91 USD estimados con supuestos de tamaño) y compararlo con lo medido el 22/11/2026: 1,29 USD por pasada completa, casi todo del juez Opus. Resultados en resultados/ejemplo-real/. El perfil real va siempre por OpenRouter: con una sola clave se eligen en .env los modelos de generación, embeddings y juez (OpenAI, Anthropic, Google…), y `python s19.py catalogo` actualiza sus precios. Se puede hacer entera con el perfil doble, sin gastar.
QUÉ ABRIR: docs/ejercicio.md y la salida de `python s19.py estimar`.
PREGUNTA: ¿qué parte os parece más difícil de hacer bien: los datos, las métricas o los tests?
Fuentes: enunciado de S19 (ejercicios.docx, 29/09/2026); tarifas.json (catálogo público de OpenRouter, openrouter.ai/api/v1/models, 22/11/2026).""")
    return sl


def s29_cierre(deck):
    sl = closing(deck, [
        "Se mide el sistema, no solo el modelo: recuperación, generación, rechazo y operación por separado.",
        "precision@5 divide entre 5; recall@5, entre los documentos que hacían falta. Siempre sobre documentos.",
        "Fiel no es correcta: Faithfulness y Answer Relevancy van con cobertura y con revisión humana.",
        "Lo que no se pudo puntuar se registra con su motivo; nunca se convierte en acierto ni en cero.",
        "Muchos tests con dobles, pocos con modelo, y un control de regresión que se ha visto fallar.",
        "La nota se guarda junto a la traza, y los fallos de producción vuelven al conjunto.",
    ], ["¿Cuál es el denominador de recall@5?", "¿Qué no detecta Faithfulness?",
        "¿Por qué el consumo del juez va aparte?", "¿De dónde salen los umbrales?"],
        ("PRÓXIMA SESIÓN · S20", "Proyecto final: agente conversacional. Lo de hoy es su red de seguridad."),
        ("MATERIALES DE S19", "demo-evaluacion: README paso a paso, guion, comandos, ejercicio opcional, "
                              "131 tests y resultados de ejemplo del perfil doble y del real."))
    notes(sl, """19:55–20:00. Cierre. Leer las seis ideas, una por bloque más la de no evaluables. Lanzar las cuatro preguntas de comprobación y dejar que respondan los alumnos: denominador de recall@5 (los documentos relevantes de esa pregunta); qué no detecta Faithfulness (respuesta incompleta o incorrecta apoyada en el contexto); por qué el consumo del juez va aparte (para no confundir el coste de responder con el de juzgar); de dónde salen los umbrales (de validación, con margen, nunca del test). Recordar que la práctica es opcional y dónde está la guía. Anunciar S20: proyecto final. Turno de preguntas.
QUÉ ABRIR: nada; dejar la terminal a mano por si hay dudas sobre algún comando.
PREGUNTA: ¿qué vais a medir primero en vuestro proyecto final?
Fuentes: temario de AI Engineer (Gmail, 17/07/2026); material/S19/README.md.""")
    return sl


SLIDES = [s24_comparar, s25_produccion, s26_langfuse, s27_ciclo, s28_practica, s29_cierre]
