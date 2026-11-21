"""S19 · Diapositivas 1–14: apertura, bloque 1 (qué medir) y bloque 2 (recuperación)."""
from deck_lib import *  # noqa: F401,F403

F_GMAIL = "Fuentes: temario (Gmail, 17/07/2026) y enunciado de S19 (ejercicios.docx, 29/09/2026)."


def s01_portada(deck):
    def panel(sl):
        img(sl, "python.png", 515, 72, h=28)
        text(sl, 515, 116, 380, 14, "PIEZAS QUE CONECTAMOS EN LA DEMO", size=9, color=MINT, bold=True)
        piezas = [("postgresql.png", "pgvector"), ("ragas-tile.png", "Ragas"), ("pytest-tile.png", "pytest"),
                  ("langfuse.png", "Langfuse"), ("docker-mark-white.png", "Docker")]
        for i, (ic, lab) in enumerate(piezas):
            x = 530 + i * 78
            img(sl, ic, x, 140, w=44, h=44)
            text(sl, x - 19, 188, 82, 14, lab, size=9.5, color=TITLE, bold=True, align="c")
        text(sl, 515, 222, 380, 12, "EL RECORRIDO DE UNA EVALUACIÓN", size=9, color=MINT, bold=True)
        x = 515
        pasos = [("casos", 52), ("recuperar", 74), ("generar", 64), ("evaluar", 64), ("decidir", 60)]
        for i, (t, w) in enumerate(pasos):
            chip(sl, x, 242, w, 22, t, fill=TAKE_BG, color=MINT_L, size=9.5, line="2A5246")
            x += w
            if i < len(pasos) - 1:
                line(sl, x + 2, 253, x + 12, 253, color=MINT)
                x += 14
        img(sl, "g-metrics.png", 515, 280, w=22, h=22)
        text(sl, 545, 283, 350, 16, [[("Recuperación  ", {"bold": True, "color": TITLE}),
                                     ("precision@5 y recall@5 sobre documentos.", {"color": TEXT})]], size=10.5)
        img(sl, "g-shield.png", 515, 310, w=22, h=22)
        text(sl, 545, 313, 350, 16, [[("Regresión  ", {"bold": True, "color": TITLE}),
                                     ("un control que falla cuando el resultado empeora.", {"color": TEXT})]], size=10.5)
        box(sl, 515, 350, 384, 94, fill=CARD)
        text(sl, 527, 358, 360, 12, "Y ADEMÁS", size=8.5, color=MUTED, bold=True)
        extra = [("g-user.png", "Revisión humana"), ("g-alert.png", "No evaluables y cobertura"),
                 ("g-data-table.png", "Comparación A/B"), ("g-logs.png", "Coste del juez aparte")]
        for i, (ic, lab) in enumerate(extra):
            x = 525 + i * 92
            img(sl, ic, x + 30, 376, w=30, h=30)
            text(sl, x, 410, 90, 26, lab, size=8.5, color=TEXT, align="c")

    sl = cover(deck, "S19 · AI ENGINEER", "Evaluación y testing\nde sistemas de IA",
               "Un RAG pequeño reconstruido desde cero, con recuperación y generación medidas por separado, "
               "tests automáticos y un control que avisa cuando un cambio empeora el resultado. "
               "Explicación y demo guiada en local.", panel)
    text(sl, 43, 342, 440, 32, "Martes 24/11/2026 · grupo M/J  ·  Lunes 30/11/2026 · grupo L/X\n18:30–20:00 · hora de Madrid",
         size=10.5, color=MUTED)
    notes(sl, """18:30. Portada mientras entran los alumnos. Presentar el objetivo del temario: cerrar el ciclo de calidad, medir de forma rigurosa si un sistema de IA funciona bien antes y después de cada cambio. Avisar de que toda la demo corre en local, sin claves y sin coste, con un perfil «doble» que no mide ningún modelo: sirve para aprender el método.
QUÉ ABRIR: nada todavía; terminal preparada en demo-evaluacion/.
PREGUNTA: ¿cómo decidís hoy si un cambio de prompt mejora vuestro sistema?
""" + F_GMAIL)
    return sl


def s02_qr(deck):
    sl = deck.slide(tag="qr")
    header_s(sl, "Antes de empezar", "Encuesta de S18 y plan de la sesión")
    img(sl, "qr-ai-engineer.jpg", 390, 149.4, w=180, h=180)
    text(sl, 367.5, 349.9, 225, 41.2, "Encuesta de la sesión anterior ·\nS18", size=13.5, color=TITLE, bold=True,
         align="c")
    # plan de la sesión (izquierda)
    text(sl, 48, 150, 290, 12, "PLAN DE LA SESIÓN · 18:30–20:00", size=9, color=MINT, bold=True)
    plan = [("18:33", "Punto de partida y caso", MUTED), ("18:41", "1 · Qué medir", MINT), ("18:51", "2 · Recuperación", PINK),
            ("19:06", "3 · Generación", AMBER), ("19:24", "4 · Testing automatizado", VIOLET),
            ("19:38", "5 · Producción y observabilidad", BLUE), ("19:51", "Práctica opcional y cierre", MINT_L)]
    y = 172
    for hora, nombre, col in plan:
        box(sl, 48, y, 290, 30, fill=CARD, radius=4)
        box(sl, 48, y, 3.5, 30, fill=col, radius=0)
        text(sl, 60, y, 44, 30, hora, size=10.5, color=col, bold=True, anchor="m", font=MONO)
        text(sl, 106, y, 226, 30, nombre, size=11.5, color=TITLE, anchor="m")
        y += 35
    # qué se valora y cómo trabajamos (derecha)
    text(sl, 622, 150, 290, 12, "QUÉ SESIÓN SE VALORA", size=9, color=MINT, bold=True)
    side_note(sl, 622, 172, 290, 56, "Grupo M/J · directo del 24/11", "S18 del jueves 19/11/2026.", accent=MINT)
    side_note(sl, 622, 236, 290, 56, "Grupo L/X · directo del 30/11", "S18 del miércoles 25/11/2026.", accent=BLUE)
    text(sl, 622, 306, 290, 12, "CÓMO TRABAJAMOS HOY", size=9, color=MINT, bold=True)
    bullets(sl, 622, 326, 290, 70, ["Cada bloque acaba con un momento EN VIVO en la terminal.",
                                     "Todo en local: sin claves y sin coste.",
                                     "La práctica posterior es opcional."], size=10.5, color=TEXT)
    footer_s(sl)
    notes(sl, """18:30–18:33. El QR evalúa la sesión anterior de cada grupo: S18 del 19/11 para M/J (directo del 24/11) y S18 del 25/11 para L/X (directo del 30/11). Mantenerlo dos minutos en pantalla. Explicar el plan: cinco bloques, cada uno con teoría y un momento en vivo. La práctica posterior es opcional (indicación de Laura, 04/11/2026). S19 no depende de la demo de S18.
QUÉ ABRIR: nada; comprobar que el QR se lee desde un móvil.
PREGUNTA: ¿quién ha tenido que defender con números que un sistema de IA «funciona»?
Fuentes: hilo de Gmail «Update Directos…» (Laura, 29/09, 19/10 y 04/11/2026); QR vigente en material/S16/assets.""")
    return sl


def s03_caso(deck):
    sl = deck.slide(tag="caso")
    header_s(sl, "Caso conductor", "Un cambio pequeño y una pregunta difícil",
             "El asistente de soporte de AetherCloud (empresa ficticia) responde con sus diez documentos. "
             "Alguien propone cambiar el tamaño de fragmento.")
    code_panel_s(sl, 48, 153.8, 852.8, 67.5, ["chunk_size: 320  →  900",
                                              "¿El asistente responde mejor, igual o peor?"])
    table_s(sl, 48, 240, [202.5, 315, 335.25], [
        ["Pregunta", "Sin evaluación", "Con evaluación"],
        ["¿Encuentra el documento?", "«Parece que sí»", "recall@5 sobre 14 preguntas"],
        ["¿Responde lo correcto?", "Tres pruebas a mano", "Criterio fijado antes + revisión"],
        ["¿Inventa cuando no sabe?", "No se comprueba", "6 preguntas sin respuesta"],
        ["¿Qué rompe el cambio?", "Lo descubre un cliente", "Control de regresión"],
        ["¿Cuánto cuesta?", "Factura a fin de mes", "Tokens y coste por consulta"],
    ])
    band_s(sl, "Sin un conjunto de preguntas y un criterio previo, «mejor» es una opinión.")
    footer_s(sl)
    notes(sl, """18:39–18:41. Presentar el caso: AetherCloud es una plataforma inventada; su corpus son diez documentos ficticios (SLA, cuotas, incidentes, facturación…). Alguien propone pasar el tamaño de fragmento de 320 a 900 caracteres. Recorrer la tabla: cada fila es una pregunta que hoy contestamos con intuición y que al final de la clase contestaremos con un número y su denominador. Adelantar que la comparación 320 frente a 900 se verá en vivo en el bloque 5.
QUÉ ABRIR: demo-evaluacion/corpus/ para enseñar que son archivos Markdown en bruto.
PREGUNTA: de las cinco filas, ¿cuál os preocupa más en vuestro proyecto?
""" + F_GMAIL)
    return sl


def s04_modelo_sistema(deck):
    sl = deck.slide(tag="modelo-sistema")
    header(sl, "Evaluación de modelos y métricas específicas", "Medir un modelo no es medir tu sistema",
           "Un benchmark dice cómo se comporta un modelo en tareas genéricas. Tu sistema añade documentos, búsqueda, "
           "prompt, reglas de rechazo, latencia y coste: hay que medirlo entero y por piezas.")
    # columna modelo
    box(sl, 43, 128, 285, 190, fill=BLUE_BG)
    text(sl, 55, 138, 260, 12, "MÉTRICAS DE MODELO", size=9, color=BLUE, bold=True)
    text(sl, 55, 154, 262, 34, "¿Qué sabe hacer el modelo, en general?", size=13, font=SERIF, color=TITLE)
    bullets(sl, 55, 192, 262, 120, [
        [("Exactitud, F1: ", {"bold": True, "color": TITLE}), ("clasificación con etiqueta correcta.", {})],
        [("Exact match, ROUGE, BLEU: ", {"bold": True, "color": TITLE}), ("parecido con un texto de referencia.", {})],
        [("Benchmarks públicos: ", {"bold": True, "color": TITLE}), ("comparan modelos, no tu caso.", {})],
        [("Perplejidad: ", {"bold": True, "color": TITLE}), ("cómo predice el texto; no mide utilidad.", {})],
    ], size=10, mark_color=BLUE)
    # columna sistema
    box(sl, 338, 128, 579, 190, fill=GREEN_BG)
    text(sl, 350, 138, 400, 12, "MÉTRICAS DE SISTEMA · LAS DE ESTA SESIÓN", size=9, color=MINT, bold=True)
    text(sl, 350, 154, 555, 20, "¿Funciona mi RAG con mis documentos y mis preguntas?", size=13, font=SERIF, color=TITLE)
    cols = [("g-magnifier.png", "Recuperación", "precision@5 y recall@5 sobre documentos.", PINK),
            ("g-document.png", "Generación", "Faithfulness y Answer Relevancy, con cobertura.", AMBER),
            ("g-shield.png", "Rechazo", "Se abstiene cuando no hay evidencia.", VIOLET),
            ("g-metrics.png", "Operación", "Latencia, tokens, coste y errores.", BLUE)]
    for i, (ic, t, d, col) in enumerate(cols):
        x = 350 + i * 140
        box(sl, x, 184, 132, 124, fill=CARD)
        box(sl, x, 184, 132, 3, fill=col, radius=0)
        img(sl, ic, x + 10, 196, w=26, h=26)
        text(sl, x + 10, 228, 114, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, x + 10, 246, 114, 56, d, size=9.5, color=TEXT)
    table(sl, 43, 328, 874, [150, 362, 362], [
        ["", "Evaluar un modelo", "Evaluar un sistema"],
        ["Qué se prueba", "El modelo aislado, con entradas estándar", "Corpus + búsqueda + prompt + modelo + reglas"],
        ["Con qué datos", "Benchmark público o conjunto etiquetado", "Tus preguntas, tus referencias y tus casos sin respuesta"],
        ["Qué puede fallar", "La predicción", "Encontrar, responder, citar, abstenerse, tardar o costar"],
        ["Para qué sirve", "Elegir modelo", "Decidir si un cambio se despliega"],
    ], size=10, row_h=26, bold_cols=(0,), colors={0: MINT_L})
    takeaway(sl, "Un modelo mejor en un benchmark puede dar un sistema peor: se mide el sistema completo, pieza a pieza.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:41–18:42. Primera parte del temario: «evaluación de modelos y métricas específicas». Distinguir dos niveles. Métricas de modelo: exactitud y F1 en clasificación; exact match, ROUGE o BLEU cuando hay texto de referencia; benchmarks públicos. Sirven para elegir modelo. Métricas de sistema: lo que mide esta sesión, separadas por pieza (recuperación, generación, rechazo, operación). Insistir en que las métricas de solapamiento de texto castigan una respuesta correcta redactada de otra forma; por eso en RAG se usan métricas basadas en afirmaciones y un juez.
QUÉ ABRIR: nada.
PREGUNTA: si cambio de modelo por uno «mejor» y mi tasa de rechazo correcto baja, ¿he mejorado?
Fuentes: temario de S19; documentación de métricas de Ragas (docs.ragas.io/en/stable/concepts/metrics/, consultada el 16/11/2026).""")
    return sl


def s05_anatomia(deck):
    sl = deck.slide(tag="anatomia")
    header(sl, "Anatomía de una evaluación · en la demo", "Cuatro decisiones que se toman antes de ejecutar nada",
           "Lo visto en la 3, aplicado a nuestros archivos. Una evaluación es un experimento: si las reglas se escriben "
           "después de ver el resultado, el número ya no demuestra nada.")
    pasos = [
        ("1", "Casos", "20 preguntas de test: 14 respondibles y 6 sin respuesta en el corpus.",
         "datos/test.jsonl", MINT),
        ("2", "Referencias", "Por cada caso: documentos relevantes, datos clave y respuesta esperada.",
         "documentos_relevantes · datos_clave", PINK),
        ("3", "Criterios", "Qué cuenta como acierto, escrito y fechado antes de mirar el test.",
         "datos/criterios.md", AMBER),
        ("4", "Validación aparte", "8 preguntas distintas para elegir umbral, prompt y configuración.",
         "datos/validacion.jsonl", VIOLET),
    ]
    for i, (n, t, d, f, col) in enumerate(pasos):
        x = 43 + i * 221
        box(sl, x, 126, 211, 142, fill=CARD)
        badge(sl, x + 12, 138, n, fill=col, d=22, size=11)
        text(sl, x + 42, 139, 160, 20, t, size=14, font=SERIF, color=TITLE)
        text(sl, x + 12, 170, 188, 58, d, size=10.5, color=TEXT)
        text(sl, x + 12, 240, 190, 14, f, size=8.5, font=MONO, color=col, bold=True, check=False)
    # validación frente a test
    box(sl, 43, 280, 430, 186, fill=VIOLET_BG)
    text(sl, 55, 290, 400, 12, "VALIDACIÓN: SE PUEDE MIRAR Y REPETIR", size=9, color=VIOLET, bold=True)
    bullets(sl, 55, 310, 406, 80, ["Elegir el umbral de evidencia para rechazar.",
                                    "Comparar prompts y tamaños de fragmento.",
                                    "Fijar los umbrales del control de regresión."], size=10.5, mark_color=VIOLET)
    text(sl, 55, 392, 406, 60, "Cada vez que decides algo mirando un conjunto, tu sistema se adapta un poco a él. "
         "Por eso ese conjunto ya no sirve para la nota final.", size=10, color=MUTED)
    box(sl, 487, 280, 430, 186, fill=GREEN_BG)
    text(sl, 499, 290, 400, 12, "TEST: SE MIDE UNA VEZ, CON TODO DECIDIDO", size=9, color=MINT, bold=True)
    bullets(sl, 499, 310, 406, 80, ["Mismas 20 preguntas para todas las configuraciones.",
                                     "No se indexan preguntas ni respuestas esperadas.",
                                     "No se reajustan las reglas después de verlo."], size=10.5)
    term(sl, 499, 392, 406, 62, [("$ python s19.py preflight", MINT_L),
                                 'Datos: {"test": 20, "validacion": 8, "documentos": 10}',
                                 "Preflight correcto: no se ha llamado a ningún modelo."], size=8.5)
    takeaway(sl, "Primero el conjunto y el criterio; después el sistema. Validación para decidir, test para medir.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:42–18:44. Pasar rápido: es la idea de la diapositiva 3 («casos y criterio antes de ejecutar») concretada en los archivos de la demo. Explicar las cuatro piezas de una evaluación. Casos: el enunciado pide 20 preguntas, 14 respondibles y 6 sin respuesta. Referencias: documentos relevantes y datos clave de cada caso. Criterios: qué cuenta como acierto, fijado antes de ejecutar (en la demo: responde, contiene todos los datos clave y cita un documento de referencia). Validación aparte: ejemplos distintos para elegir prompts, umbrales y configuración. Subrayar dos reglas del enunciado: no indexar preguntas ni respuestas esperadas, y no reajustar reglas después de ver el test. El comando preflight comprueba la separación.
QUÉ ABRIR: datos/test.jsonl (caso T01 y caso T16) y datos/criterios.md.
PREGUNTA: ¿por qué las preguntas del test no pueden estar dentro del corpus?
Fuentes: enunciado de S19 («Prepara datos de evaluación»); salida real de `s19.py preflight` (17/11/2026).""")
    return sl


def s06_pipeline(deck):
    sl = deck.slide(tag="pipeline")
    header(sl, "Evaluación de RAG", "Dónde se mide: después de recuperar y después de generar",
           "Un RAG encadena dos trabajos distintos. Si solo miramos la respuesta final, no sabemos si falló la "
           "búsqueda o la redacción.")
    # fila de ingesta
    text(sl, 43, 124, 300, 12, "INGESTA · UNA VEZ, DESDE DOCUMENTOS EN BRUTO", size=8.5, color=MUTED, bold=True)
    ing = [("g-document.png", "10 documentos", "Markdown ficticio"), ("g-source-code.png", "Fragmentar", "320 o 900 caracteres"),
           ("g-sdk.png", "Embeddings", "mismo modelo siempre"), ("postgresql.png", "pgvector", "vector(768) · coseno")]
    for i, (ic, t, d) in enumerate(ing):
        x = 43 + i * 222
        node(sl, x, 140, 196, 44, ic, t, d, tsize=10.5, ssize=8.5, icon_s=26)
        if i < 3:
            line(sl, x + 198, 162, x + 220, 162, color=MUTED)
    # fila de consulta
    text(sl, 43, 196, 300, 12, "CONSULTA · CADA PREGUNTA", size=8.5, color=MUTED, bold=True)
    con = [("g-user.png", "Pregunta", "en lenguaje natural", CARD, None),
           ("g-magnifier.png", "Recuperar", "12 fragmentos → 5 documentos", PINK_BG, PINK),
           ("g-shield.png", "¿Hay evidencia?", "si no, «No consta»", VIOLET_BG, VIOLET),
           ("g-json-script.png", "Generar", "respuesta con [fuentes]", AMBER_BG, AMBER)]
    for i, (ic, t, d, fill, ln) in enumerate(con):
        x = 43 + i * 222
        node(sl, x, 212, 196, 46, ic, t, d, fill=fill, line=ln, tsize=10.5, ssize=8.5, icon_s=26)
        if i < 3:
            line(sl, x + 198, 235, x + 220, 235, color=MINT)
    poly(sl, [(807, 186), (807, 199), (363, 199), (363, 210)], color=MUTED, dash=True)  # el índice alimenta la búsqueda
    line(sl, 363, 260, 363, 282, color=PINK)
    line(sl, 585, 260, 585, 282, color=VIOLET)
    line(sl, 807, 260, 807, 282, color=AMBER)
    med = [(265, PINK, PINK_BG, "MEDIDA 1 · RECUPERACIÓN", "precision@5 y recall@5 sobre documentos distintos.",
            "Sin modelo: se calcula con las referencias."),
           (487, VIOLET, VIOLET_BG, "MEDIDA 2 · RECHAZO", "Rechazos correctos y abstenciones incorrectas.",
            "Con las 6 preguntas sin respuesta."),
           (709, AMBER, AMBER_BG, "MEDIDA 3 · GENERACIÓN", "Faithfulness, Answer Relevancy y revisión humana.",
            "Con un juez (Ragas) en entorno aparte.")]
    for x, col, fill, lab, d, pie in med:
        box(sl, x, 284, 208, 104, fill=fill)
        text(sl, x + 10, 292, 190, 12, lab, size=8.5, color=col, bold=True)
        text(sl, x + 10, 309, 190, 44, d, size=10.5, color=TITLE)
        text(sl, x + 10, 356, 190, 28, pie, size=9, color=MUTED)
    box(sl, 43, 284, 208, 104, fill=BLUE_BG)
    text(sl, 53, 292, 190, 12, "MEDIDA 4 · OPERACIÓN", size=8.5, color=BLUE, bold=True)
    text(sl, 53, 309, 190, 44, "Latencia por paso, tokens, coste y errores.", size=10.5, color=TITLE)
    text(sl, 53, 356, 190, 28, "En todas las consultas.", size=9, color=MUTED)
    table(sl, 43, 398, 874, [210, 332, 332], [
        ["Síntoma en la respuesta final", "Si falla la recuperación", "Si falla la generación"],
        ["Respuesta incompleta o incorrecta", "recall@5 bajo: el documento no llegó", "recall@5 alto y aun así falla: mirar el prompt y la fidelidad"],
        ["Respuesta inventada", "Contexto pobre o vacío", "Faithfulness baja con buen contexto"],
    ], size=9.5, row_h=22, bold_cols=(0,), colors={0: MINT_L})
    takeaway(sl, "Medir por separado convierte «responde mal» en un diagnóstico: no encontró, no supo redactar o no se abstuvo.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:44–18:47. Recorrer el diagrama de izquierda a derecha. Ingesta: documentos en bruto, fragmentación, embeddings y PostgreSQL con pgvector; el índice se reconstruye desde vacío y cada configuración tiene el suyo. Consulta: se piden 12 fragmentos, se agrupan en un máximo de 5 documentos distintos, se decide si hay evidencia suficiente y, solo entonces, se genera con 4 fragmentos y citas. Señalar las cuatro medidas y en qué punto se toma cada una. La tabla inferior es la razón de separar: el mismo síntoma tiene causas distintas.
QUÉ ABRIR: nada; a continuación viene el primer momento en vivo.
PREGUNTA: si recall@5 es 1,00 y la respuesta es mala, ¿qué pieza reviso?
Fuentes: enunciado de S19 («medir recuperación y generación por separado»); código de demo-evaluacion/rag/consulta.py.""")
    return sl


def s07_vivo1(deck):
    sl = deck.slide(tag="vivo1")
    header_s(sl, "En vivo 1 · Reconstruir desde cero", "De diez archivos a un índice que responde o rechaza",
             "Documentos en bruto e índice vacío. Repetir la ingesta sustituye el índice: no duplica.")
    code_panel_s(sl, 48, 153.8, 852.8, 110, [
        "python s19.py preflight",
        "python s19.py ingestar --config A",
        'python s19.py preguntar "¿Qué versión de TLS exigen las pasarelas?"',
        'python s19.py preguntar "¿Cuál es el horario de la cafetería?"',
    ], size=14.5)
    kv_rows_s(sl, 276, [
        ("preflight", "20 casos de test, 8 de validación, 10 documentos; nada de ello indexado."),
        ("ingestar", "Índice idx-1ad9… con 41 fragmentos; al repetir, las mismas 41 filas."),
        ("preguntar", "TLS 1.3 con la cita [01-arquitectura-aethercloud]; la cafetería, «No consta»."),
    ], pitch=44, size=14.5)
    tag(sl, 48, 418, "doble")
    text(sl, 258, 419, 640, 26, "Embeddings por hash de palabras y generador que copia frases. Comprueba el recorrido; "
         "no dice nada de la calidad de un modelo real.", size=9.5, color=MUTED)
    band_s(sl, "El índice se identifica por corpus + fragmentación + modelo de embeddings: si cambia uno, es otro índice.")
    footer_s(sl)
    notes(sl, """18:47–18:51. EN VIVO 1. Ejecutar los cuatro comandos en orden (docs/comandos.md, «Vivo 1»). 1) preflight: leer la línea de datos y la de las variantes A y B (41 y 13 fragmentos). 2) ingestar --config A y repetirlo: mismo identificador de índice y mismas 41 filas. 3) preguntar por TLS: enseñar documentos recuperados, mejor similitud, umbral y la cita entre corchetes. 4) preguntar por la cafetería: rechazo por evidencia insuficiente, sin llamar al generador. Decir en voz alta que es el perfil doble: no mide ningún modelo.
QUÉ ABRIR: terminal; después datos/test.jsonl para ver un caso respondible y uno sin respuesta.
PREGUNTA: ¿qué pasaría si indexara con un modelo de embeddings y consultara con otro?
Fuentes: salida real de los comandos con el perfil doble (17/11/2026); demo-evaluacion/README.md, paso 1.""")
    return sl


def s08_formulas(deck):
    sl = deck.slide(tag="formulas")
    header(sl, "Métricas de recuperación", "precision@5 y recall@5: mismo numerador, distinto denominador",
           "Las dos cuentan cuántos documentos relevantes hay entre los cinco primeros. Cambia entre qué se divide, "
           "y por eso responden a preguntas distintas.")
    for x, col, fill, nombre, preg, den, lectura in [
        (43, PINK, PINK_BG, "precision@5", "De lo que traje, ¿cuánto sirve?", "5",
         "Siempre 5: un puesto vacío o irrelevante cuenta como fallo. Mide el ruido que recibe el generador."),
        (487, MINT, GREEN_BG, "recall@5", "De lo que hacía falta, ¿cuánto traje?", "documentos relevantes de esa pregunta",
         "Cambia en cada pregunta: 1 si basta un documento, 2 si hay que combinar dos. Mide lo que se pierde."),
    ]:
        box(sl, x, 128, 430, 176, fill=fill)
        text(sl, x + 14, 138, 300, 24, nombre, size=17, font=MONO, color=col, bold=True)
        text(sl, x + 14, 164, 400, 18, preg, size=12.5, font=SERIF, color=TITLE)
        box(sl, x + 14, 190, 402, 58, fill=BG, radius=5)
        text(sl, x + 22, 195, 386, 18, "documentos relevantes entre los 5 recuperados", size=10.5, color=TITLE,
             align="c", bold=True)
        box(sl, x + 60, 217, 310, 1.2, fill=col, radius=0)
        text(sl, x + 22, 223, 386, 18, den, size=10.5, color=col, align="c", bold=True)
        text(sl, x + 14, 256, 402, 44, lectura, size=10, color=TEXT)
    # reglas
    reglas = [("Unidad: el documento", "Tres fragmentos del mismo documento ocupan un puesto y son un acierto, no tres.", AMBER),
              ("El techo de precision@5", "Con un solo documento relevante, lo máximo es 1/5 = 0,20. No es un mal resultado.", VIOLET),
              ("k fija y declarada", "Se piden 12 fragmentos para poder reunir hasta 5 documentos distintos.", BLUE),
              ("Sin relevantes no hay recall", "En una pregunta sin respuesta el denominador sería 0: se mide el rechazo.", CORAL)]
    for i, (t, d, col) in enumerate(reglas):
        x = 43 + i * 221
        side_note(sl, x, 316, 211, 92, t, d, accent=col, size=9.5)
    code_block(sl, 43, 420, 874, [
        "aciertos = len(set(sin_repetidos(recuperados, k)) & set(relevantes))     # evaluacion/metricas.py",
        "precision_at_k = aciertos / k              recall_at_k = aciertos / len(set(relevantes))",
    ], size=9.5, color=MINT_L)
    takeaway(sl, "Un número sin denominador no se puede interpretar: precision@5 divide entre 5; recall@5, entre lo que había que encontrar.",
             label="Idea guía")
    footer(sl, block=2)
    notes(sl, """18:51–18:54. Definir las dos métricas con la misma frase y cambiar solo el denominador. precision@5: relevantes entre los cinco recuperados, dividido entre 5 siempre. recall@5: el mismo numerador dividido entre los documentos de referencia de esa pregunta. Explicar las cuatro reglas del enunciado: se mide sobre documentos, sin contar dos fragmentos del mismo documento como dos aciertos; hay que explicar los denominadores; y no se inventa un recall cuando no hay documentos relevantes. Añadir el techo: con un solo documento relevante, precision@5 no pasa de 0,20; el informe de la demo lo enseña al lado.
QUÉ ABRIR: evaluacion/metricas.py (funciones precision_at_k y recall_at_k).
PREGUNTA: precision@5 = 0,20 y recall@5 = 1,00 en una pregunta con un documento relevante: ¿es bueno o malo?
Fuentes: enunciado de S19 («Mide recuperación»); código y tests de la demo (tests/test_metricas.py).""")
    return sl


def s09_ejemplo(deck):
    sl = deck.slide(tag="ejemplo-pr")
    header(sl, "Ejemplo trabajado", "De doce fragmentos a cinco documentos, y de ahí a dos números",
           "Pregunta: «Una organización del plan Empresa sufre un SEV-1: ¿qué soporte incluye y cuál es el tiempo "
           "máximo de primera respuesta?». Hacen falta dos documentos: 07 y 06.")
    tag(sl, 43, 124, "ilustrativo")
    # paso 1: fragmentos
    text(sl, 43, 148, 420, 12, "1 · LA BÚSQUEDA DEVUELVE FRAGMENTOS, EN ORDEN DE SIMILITUD", size=8.5, color=MUTED, bold=True)
    frs = ["07#02", "07#01", "05#01", "07#03", "03#02", "05#02", "09#01", "06#01", "06#03", "…"]
    for i, f in enumerate(frs):
        rel = f[:2] in ("07", "06")
        doc_chip(sl, 43 + i * 87.6, 166, 81, 26, f, ok=rel if f != "…" else None, size=9)
    # paso 2: documentos
    text(sl, 43, 206, 520, 12, "2 · SE QUEDAN LOS CINCO PRIMEROS DOCUMENTOS DISTINTOS", size=8.5, color=MUTED, bold=True)
    docs = [("07", "facturación y planes", True), ("05", "SLA y créditos", False), ("03", "límites y cuotas", False),
            ("09", "observabilidad", False), ("06", "respuesta a incidentes", True)]
    for i, (d, nombre, rel) in enumerate(docs):
        x = 43 + i * 176
        doc_chip(sl, x, 224, 166, 52, f"documento {d}", ok=rel, sub=nombre + (" · relevante" if rel else ""), size=10.5)
        badge(sl, x + 6, 229, i + 1, fill=MINT if rel else BORDER, color=DARK if rel else TITLE, d=16)
    # paso 3: cálculo
    box(sl, 43, 290, 280, 118, fill=PINK_BG)
    text(sl, 55, 298, 250, 12, "PRECISION@5", size=9, color=PINK, bold=True)
    text(sl, 55, 314, 256, 40, "2 / 5 = 0,40", size=27, font=SERIF, color=TITLE)
    text(sl, 55, 356, 256, 46, "Dos de los cinco puestos son útiles. El techo de esta pregunta es 2/5: no se puede mejorar.",
         size=9.5, color=TEXT)
    box(sl, 335, 290, 280, 118, fill=GREEN_BG)
    text(sl, 347, 298, 250, 12, "RECALL@5", size=9, color=MINT, bold=True)
    text(sl, 347, 314, 256, 40, "2 / 2 = 1,00", size=27, font=SERIF, color=TITLE)
    text(sl, 347, 356, 256, 46, "Llegaron los dos documentos que hacían falta. El generador tiene todo lo necesario.",
         size=9.5, color=TEXT)
    box(sl, 627, 290, 290, 118, fill=CORAL_BG, line=CORAL)
    text(sl, 639, 298, 260, 12, "EL ERROR HABITUAL: CONTAR FRAGMENTOS", size=9, color=CORAL, bold=True)
    text(sl, 639, 314, 266, 40, "3 / 5 = 0,60", size=27, font=SERIF, color=CORAL)
    text(sl, 639, 356, 266, 46, "Tres de los cinco primeros fragmentos son del 07. Contarlos premia trocear más, no buscar mejor.",
         size=9.5, color=TEXT)
    table(sl, 43, 418, 874, [250, 156, 156, 312], [
        ["Si el 06 hubiera quedado en el puesto…", "precision@5", "recall@5", "Lectura"],
        ["5 (como arriba)", "0,40", "1,00", "El orden dentro de los cinco no cambia estas dos métricas"],
        ["6 o posterior", "0,20", "0,50", "Falta medio contexto: la respuesta saldrá incompleta"],
    ], size=9.5, row_h=17, bold_cols=(0,), colors={0: MINT_L})
    takeaway(sl, "Primero se agrupa por documento y después se cuenta. Contar fragmentos infla la precisión sin recuperar nada nuevo.",
             label="Idea guía")
    footer(sl, block=2)
    notes(sl, """18:54–18:58. Recorrer el ejemplo en tres pasos. Es ilustrativo: la pregunta existe en el test (T12) pero el orden de fragmentos está construido para explicar el cálculo. 1) La búsqueda devuelve fragmentos; varios son del mismo documento. 2) Se recorre la lista y se guardan los cinco primeros documentos distintos: 07, 05, 03, 09 y 06. 3) Numerador: dos relevantes (07 y 06). precision@5 = 2/5 = 0,40; recall@5 = 2/2 = 1,00. Enseñar el error habitual: contar los tres fragmentos del 07 daría 3/5. La tabla inferior muestra qué pasa si el segundo documento se queda fuera de los cinco.
QUÉ ABRIR: tests/test_metricas.py, test «dos fragmentos del mismo documento son un acierto».
PREGUNTA: ¿por qué pedimos 12 fragmentos si solo vamos a contar 5 documentos?
Fuentes: enunciado de S19; caso T12 de datos/test.jsonl; función documentos_distintos de rag/consulta.py.""")
    return sl


def s10_rechazo(deck):
    sl = deck.slide(tag="rechazo")
    header(sl, "Preguntas sin respuesta", "El rechazo se mide aparte: cuatro resultados posibles",
           "Seis preguntas del test no tienen respuesta en el corpus. Ahí no hay documentos relevantes ni recall: "
           "lo correcto es abstenerse.")
    # matriz 2x2
    text(sl, 205, 126, 210, 14, "EL SISTEMA RESPONDE", size=9, color=MUTED, bold=True, align="c")
    text(sl, 425, 126, 210, 14, "EL SISTEMA SE ABSTIENE", size=9, color=MUTED, bold=True, align="c")
    filas = [("Pregunta\nrespondible", "14 del test",
              ("Respuesta emitida", "10", "Se evalúa su contenido: 6 aciertos por criterio.", GREEN_BG, MINT),
              ("Abstención incorrecta", "4", "La respuesta estaba en el corpus. Se cuenta aparte.", CORAL_BG, CORAL)),
             ("Pregunta sin\nrespuesta", "6 del test",
              ("Respuesta indebida", "4", "Contesta algo que no consta: el fallo más grave.", CORAL_BG, CORAL),
              ("Rechazo correcto", "2", "«No consta en la documentación».", GREEN_BG, MINT))]
    for r, (lab, n, a, b) in enumerate(filas):
        y = 146 + r * 108
        box(sl, 43, y, 152, 100, fill=CARD)
        text(sl, 53, y + 22, 132, 36, lab, size=12, font=SERIF, color=TITLE)
        text(sl, 53, y + 66, 132, 14, n, size=9.5, color=MUTED)
        for c, (t, num, d, fill, col) in enumerate((a, b)):
            x = 205 + c * 220
            box(sl, x, y, 210, 100, fill=fill)
            text(sl, x + 12, y + 8, 150, 14, t.upper(), size=8.5, color=col, bold=True)
            text(sl, x + 12, y + 24, 60, 40, num, size=30, font=SERIF, color=TITLE)
            text(sl, x + 62, y + 30, 138, 60, d, size=9.5, color=TEXT)
    tag(sl, 43, 366, "doble")
    text(sl, 252, 367, 390, 26, "Test A de resultados/ejemplo-doble (17/11/2026). Un sistema real debe dar otras cifras.",
         size=9, color=MUTED)
    # derecha: cómo decide
    box(sl, 655, 126, 262, 266, fill=VIOLET_BG)
    text(sl, 667, 136, 240, 12, "CÓMO DECIDE EL SISTEMA", size=9, color=VIOLET, bold=True)
    text(sl, 667, 154, 240, 34, "Dos barreras antes de inventar", size=13, font=SERIF, color=TITLE)
    bullets(sl, 667, 192, 240, 120, [
        [("Umbral de evidencia. ", {"bold": True, "color": TITLE}),
         ("Si la mejor similitud no llega al umbral, se rechaza sin llamar al modelo.", {})],
        [("Instrucción al generador. ", {"bold": True, "color": TITLE}),
         ("Si los fragmentos no contienen el dato, responde NO_CONSTA.", {})],
    ], size=10, mark_color=VIOLET, space=6)
    text(sl, 667, 318, 240, 66, "El umbral se elige con validación y depende del modelo de embeddings y del tamaño "
         "de fragmento: no se copia de otro índice.", size=9.5, color=MUTED)
    table(sl, 43, 400, 874, [230, 190, 454], [
        ["Métrica", "Denominador", "Por qué va aparte"],
        ["Rechazos correctos · 2/6", "Preguntas sin respuesta", "Un RAG que nunca rechaza tendría recall alto e inventaría en las seis"],
        ["Abstenciones incorrectas · 4/14", "Preguntas respondibles", "Un RAG que rechaza siempre acertaría las seis y no serviría para nada"],
    ], size=9.5, row_h=21, bold_cols=(0,), colors={0: MINT_L})
    takeaway(sl, "Rechazar bien y responder bien se miden con preguntas distintas y denominadores distintos; nunca se mezclan en una media.",
             label="Idea guía")
    footer(sl, block=2)
    notes(sl, """18:58–19:01. El enunciado pide medir el rechazo correcto por separado y contar aparte las abstenciones incorrectas. Recorrer la matriz: filas = tipo de pregunta; columnas = lo que hizo el sistema. Las celdas verdes son el comportamiento deseado; las rojas, los dos errores, que no pesan lo mismo: una respuesta indebida es información inventada; una abstención incorrecta es una oportunidad perdida. Las cifras son del perfil doble (test A): 10 respuestas emitidas en respondibles, 4 abstenciones incorrectas, 4 respuestas indebidas y 2 rechazos correctos. Explicar las dos barreras de la demo: umbral de evidencia y la marca NO_CONSTA del generador.
QUÉ ABRIR: datos/calibracion.json para ver el umbral elegido con validación.
PREGUNTA: ¿qué métrica mejoraría un sistema que se abstiene siempre? ¿Y cuál se hundiría?
Fuentes: enunciado de S19; resultados/ejemplo-doble/test-A/informe.md (perfil doble, 17/11/2026).""")
    return sl


def s11_vivo2(deck):
    sl = deck.slide(tag="vivo2")
    header_s(sl, "En vivo 2 · Recuperación y rechazo", "Calibrar con validación y leer el primer informe",
             "El umbral se elige con las ocho preguntas de validación. El test sigue sin tocarse.")
    code_panel_s(sl, 48, 153.8, 420, 96, [
        "python s19.py calibrar --config A",
        "python s19.py lote --conjunto validacion \\",
        "    --config A --salida resultados/mi-val-A",
        "python s19.py informe resultados/mi-val-A",
    ], size=11.5)
    term(sl, 480, 153.8, 420.8, 96, [
        "  V06  sin respuesta 0.3706",
        "  V07  sin respuesta 0.0967",
        ("Umbral calculado = 0.2787 (7/8 correctas)", MINT_L),
        ("umbral fijado = 0.2787 (2026-11-17)", MINT_L),
        ("Sin cambios: --fijar para sobrescribir", AMBER),
    ], size=9.5)
    table_s(sl, 48, 262, [150, 250, 120, 332.8], [
        ["Bloque", "Métrica", "Valor", "Sobre"],
        ["Recuperación", "precision@5", "0,24", "5 respondibles · techo 0,24"],
        ["Recuperación", "recall@5", "1,00", "5 respondibles"],
        ["Rechazo", "rechazos correctos", "2/3", "preguntas sin respuesta"],
        ["Rechazo", "abstenciones incorrectas", "0/5", "preguntas respondibles"],
        ["Corrección", "aciertos por criterio", "3/5", "preguntas respondibles"],
    ], row_h=26, size=12.5)
    tag(sl, 48, 428, "salida")
    text(sl, 290, 429, 610, 26, "Perfil doble: comprueba el sistema de evaluación, no mide ningún modelo. "
         "V06 supera el umbral y se responde: es el rechazo que falla.", size=9.5, color=MUTED)
    band_s(sl, "recall@5 = 1,00 y solo 3 de 5 aciertos: los documentos llegan; el fallo está al generar.")
    footer_s(sl)
    notes(sl, """19:01–19:06. EN VIVO 2. 1) calibrar --config A: imprime la mejor similitud de cada pregunta de validación y elige el umbral que más decisiones acierta (0,2787; 7 de 8) y lo compara con el fijado el 17/11. No sobrescribe datos/calibracion.json: el umbral se congeló antes del test y solo se recalibra a propósito con --fijar. Enseñar que V06, sin respuesta, queda por encima: el umbral no es perfecto. 2) lote sobre validación: crea respuestas.jsonl y manifiesto.json. 3) informe: leer cada fila con su denominador. precision@5 0,24 con techo 0,24 significa que la recuperación es todo lo buena que puede ser; recall@5 1,00; aun así solo acierta 3 de 5, porque el generador doble copia frases incompletas. Esa lectura solo es posible porque las métricas están separadas.
QUÉ ABRIR: terminal; resultados/mi-val-A/informe.md; evaluacion/metricas.py.
PREGUNTA: si recall@5 es 1,00, ¿por qué solo acierta 3 de 5?
Fuentes: salida real de calibrar e informe (resultados/ejemplo-doble/validacion-A, perfil doble, 17/11/2026).""")
    return sl





# ================================================================ introducción 20/11/2026 (petición de José)
F_INTRO = ("Fuentes: Anthropic, «Define success criteria and build evaluations» (docs.claude.com/en/docs/test-and-evaluate/develop-tests); "
           "Langfuse, «Evaluation overview» (langfuse.com/docs/evaluation/overview); documentación de Ragas "
           "(docs.ragas.io/en/stable/concepts/). Consultadas el 20/11/2026 con Firecrawl; copias en .build/s19/research/.")


def _label(sl, x, y, w, t, color=AMBER):
    text(sl, x, y, w, 12.2, t.upper(), size=9, color=color, bold=True)


def _tagchip(sl, x, y, t):
    fill, col = {"TEST": (VIOLET_BG, VIOLET), "EVALUACIÓN": (AMBER_BG, AMBER), "PRODUCCIÓN": (BLUE_BG, BLUE)}[t]
    w = len(t) * 4.9 + 16
    chip(sl, x, y, w, 15, t, fill=fill, color=col, size=7, radius=3)
    return w


def s02a_que_es_evaluar(deck):
    sl = deck.slide(tag="que-es-evaluar")
    header(sl, "Punto de partida · qué es evaluar", "Evaluar: decidir con datos si un cambio mejora o empeora",
           "Evaluar es pasar el sistema por un conjunto de casos fijado de antemano, puntuar cada respuesta con un criterio "
           "y comparar el resultado con un umbral. Sustituye «parece que va mejor» por un número con su denominador.")
    steps = [("g-data-table.png", "Casos", "preguntas y respuesta esperada, fijadas antes", MINT),
             ("g-server.png", "Ejecutar", "el sistema responde a cada caso", BLUE),
             ("g-magnifier.png", "Puntuar", "con código, un juez LLM o una persona", AMBER),
             ("g-metrics.png", "Agregar", "media, cobertura y resultado por tipo de caso", VIOLET),
             ("g-shield.png", "Decidir", "¿supera el umbral? se publica o no", PINK)]
    sw = 160
    gap = (874 - 5 * sw) / 4
    for i, (ic, t, b, col) in enumerate(steps):
        x = 43 + i * (sw + gap)
        box(sl, x, 140, sw, 96, fill=CARD)
        box(sl, x, 140, sw, 3.5, fill=col, radius=0)
        circle(sl, x + 12, 152, 36, CARD2, line=col, lw=1.5)
        img(sl, ic, x + 20, 160, w=20, h=20)
        badge(sl, x + sw - 26, 150, i + 1, fill=col, d=16, size=8.5)
        text(sl, x + 56, 158, sw - 84, 18, t, size=13, font=SERIF, color=TITLE)
        text(sl, x + 12, 196, sw - 24, 36, b, size=9, color=TEXT)
        if i < 4:
            line(sl, x + sw + 2, 188, x + sw + gap - 2, 188, color=col, w=1.75)
    # bucle de vuelta
    line(sl, 43 + 4 * (sw + gap) + sw / 2, 237, 43 + 4 * (sw + gap) + sw / 2, 250, color=MUTED, w=1.25, head="none", dash=True)
    line(sl, 43 + 4 * (sw + gap) + sw / 2, 250, 43 + sw / 2, 250, color=MUTED, w=1.25, head="none", dash=True)
    line(sl, 43 + sw / 2, 250, 43 + sw / 2, 238, color=MUTED, w=1.25, dash=True)
    chip(sl, 330, 243, 300, 14, "los casos que fallan se añaden al conjunto y se vuelve a empezar",
         fill=BG, color=MUTED, size=7.5, bold=True, line=BORDER)
    # tabla clásico frente a IA
    _label(sl, 43, 266, 430, "Por qué la IA necesita evaluación, no solo tests")
    table(sl, 43, 283, 430, [1.2, 1.4], [
        ["Software clásico", "Sistema con IA"],
        ["Misma entrada, misma salida", "La misma pregunta puede dar respuestas distintas"],
        ["Correcto = igual al esperado", "Hay muchas formas correctas de responder"],
        ["Un test pasa o falla", "Una puntuación que se compara con un umbral"],
        ["Un fallo se reproduce siempre", "Un fallo aparece en un % de los casos"],
    ], size=9.3, row_h=36, colors={0: MUTED, 1: TITLE})
    # tres formas de puntuar
    _label(sl, 487, 266, 430, "Tres formas de puntuar una respuesta")
    graders = [("g-source-code.png", "Código", MINT, "Comparar con lo esperado: formato, cita, documento recuperado.",
                "Rápido y fiable; no capta matices."),
               ("g-gear.png", "Juez LLM", AMBER, "Otro modelo puntúa con una rúbrica: fidelidad, relevancia.",
                "Flexible y escalable; hay que validarlo antes."),
               ("g-user.png", "Persona", BLUE, "Alguien revisa una muestra con criterios escritos.",
                "La mejor calidad; lenta y cara.")]
    y = 283
    for ic, t, col, b, pc in graders:
        box(sl, 487, y, 430, 58, fill=CARD)
        box(sl, 487, y, 3.5, 58, fill=col, radius=0)
        img(sl, ic, 499, y + 15, w=26, h=26)
        text(sl, 535, y + 7, 120, 14, t, size=11, color=col, bold=True)
        text(sl, 535, y + 23, 372, 15, b, size=9, color=TEXT)
        text(sl, 535, y + 39, 372, 15, pc, size=8.8, color=MUTED, bold=True)
        y += 62
    takeaway(sl, "Primero se decide qué es una buena respuesta y cómo se puntúa; después se ejecuta. Si no, el número se adapta al resultado.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:33–18:35. Antes de entrar en RAG, qué significa evaluar. Recorrer los cinco pasos de izquierda a derecha: un conjunto de casos fijado de antemano (en la demo, 20 preguntas de test y 8 de validación), ejecutar el sistema sobre todos, puntuar cada respuesta, agregar (media, cobertura, resultado por tipo de caso) y decidir comparando con un umbral. La flecha de vuelta: los casos que fallan, o los que aparecen en producción, se incorporan al conjunto.
Tabla de la izquierda: por qué en IA no bastan los tests clásicos. La salida no es determinista, hay muchas respuestas correctas, el resultado es una puntuación con umbral y los fallos son estadísticos.
Tres formas de puntuar, según la guía de evaluación de Anthropic: con código (la más rápida y fiable, pero sin matices), con un juez LLM (rápida y flexible, pero hay que comprobar que es fiable antes de escalarla) y con personas (la más flexible y de más calidad, pero lenta y cara). En la clase se usan las tres: precision@5 y recall@5 con código, Faithfulness y Answer Relevancy con Ragas como juez y una revisión manual de cinco respuestas.
QUÉ ABRIR: nada; diapositiva conceptual.
PREGUNTA: ¿cómo decidís hoy si un cambio de prompt es mejor? ¿Con cuántos ejemplos?
""" + F_INTRO)
    return sl


def s02b_tests_y_evaluacion(deck):
    sl = deck.slide(tag="tests-y-evaluacion")
    header(sl, "Punto de partida · testing y evaluación", "Tests, evaluación y producción: tres redes a distinta altura",
           "Los tests comprueban el código que rodea al modelo. La evaluación mide la calidad de las respuestas antes de "
           "publicar. En producción se sigue midiendo con tráfico real, y lo que falla vuelve al conjunto de casos.")
    cols = [("g-source-code.png", "Desarrollo", "escribir el cambio", MUTED),
            ("pytest-tile.png", "Pull request", "tests con dobles", VIOLET),
            ("ragas-tile.png", "Antes de publicar", "evaluación offline", AMBER),
            ("langfuse.png", "Producción", "evaluación online", BLUE)]
    cw = (874 - 3 * 26) / 4
    for i, (ic, t, s, col) in enumerate(cols):
        x = 43 + i * (cw + 26)
        box(sl, x, 132, cw, 56, fill=CARD, line=col, lw=1.25)
        iw, ih = img_size(ic, h=32)
        if iw > 60:
            iw, ih = img_size(ic, w=60)
        img(sl, ic, x + 12, 132 + (56 - ih) / 2, w=iw, h=ih)
        text(sl, x + 82, 140, cw - 90, 16, t, size=12, font=SERIF, color=TITLE)
        text(sl, x + 82, 160, cw - 90, 14, s, size=9, color=col, bold=True)
        if i < 3:
            line(sl, x + cw + 3, 160, x + cw + 23, 160, color=MUTED, w=1.75)
    # carriles
    lanes = [(VIOLET, VIOLET_BG, 1, "TESTS · el código hace lo que debe: formato, fuentes, errores, ingesta sin duplicados. Sin llamar al modelo."),
             (AMBER, AMBER_BG, 2, "EVALUACIÓN OFFLINE · calidad sobre un conjunto fijo, con modelo y juez reales. Un umbral decide si sale."),
             (BLUE, BLUE_BG, 3, "EVALUACIÓN ONLINE · trazas, puntuaciones y muestras revisadas.")]
    y = 198
    for col, bg, ci, t in lanes:
        x = 43 + ci * (cw + 26)
        box(sl, 43, y, 874, 26, fill=CARD, radius=4)
        box(sl, x - 6, y + 2, 917 - x + 4, 22, fill=bg, line=col, lw=1, radius=11)
        text(sl, 51, y, x - 64, 26, t.split(" · ")[0], size=8.5, color=col, bold=True, anchor="m", align="r")
        text(sl, x + 6, y + 2, 917 - x - 14, 22, t.split(" · ")[1], size=8.4, color=TITLE, anchor="m")
        y += 31
    poly(sl, [(890, 288), (890, 300), (220, 300), (220, 292)], color=MUTED, w=1.25, dash=True)
    chip(sl, 400, 293, 290, 14, "lo que falla en producción se convierte en un caso nuevo", fill=BG, color=MUTED,
         size=7.5, bold=True, line=BORDER)
    table(sl, 43, 314, 874, [1.0, 1.7, 1.9, 1.9], [
        ["", "Tests", "Evaluación offline", "Evaluación online"],
        ["Qué comprueba", "El código que rodea al modelo", "La calidad de las respuestas", "El comportamiento con usuarios reales"],
        ["Con qué", "Dobles del modelo; sin llamadas", "Conjunto de test y validación; modelo y juez", "Trazas, feedback y muestras revisadas"],
        ["Cuándo", "En cada pull request, en segundos", "Antes de publicar un cambio", "De forma continua"],
        ["Coste", "Prácticamente nulo", "Llamadas al modelo y al juez", "Según el muestreo"],
        ["Si falla", "La PR no se integra", "El cambio no se publica", "Alerta, revisión y caso nuevo"],
    ], size=9, row_h=24.5, bold_cols=(0,), colors={0: MINT_L})
    takeaway(sl, "Cada red atrapa fallos distintos: ninguna sustituye a las otras dos.", label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:35–18:37. Situar la evaluación en el ciclo que vieron en S18. Arriba, el recorrido de un cambio: desarrollo, pull request, antes de publicar y producción. Cada carril marca dónde actúa cada red.
Tests: comprueban el código determinista que rodea al modelo (formato de salida, fuentes citadas, manejo de errores, ingesta sin duplicados) con dobles del modelo; son baratos y se ejecutan en cada PR (en la demo, 73 tests con pytest).
Evaluación offline: mide la calidad sobre un conjunto fijo antes de publicar, con el modelo y el juez reales; un umbral elegido con validación decide si el cambio sale (control de regresión, bloque 4).
Evaluación online: en producción, sobre trazas reales; Langfuse la describe como puntuar trazas en vivo y convertir ejemplos interesantes en datasets para los experimentos offline. La flecha de vuelta es esa idea.
La pirámide de tests de la diapositiva 22 detalla la primera red; el bloque 5 trata la tercera.
QUÉ ABRIR: nada; diapositiva conceptual.
PREGUNTA: si solo pudierais tener una de las tres redes, ¿cuál elegiríais y qué fallos se os escaparían?
""" + F_INTRO)
    return sl


CASOS_S19 = [
    ("g-metrics.png", "Pasar a un modelo más barato", ["EVALUACIÓN"], AMBER,
     "«Parece igual» y la calidad baja en silencio.",
     "Mismo conjunto, dos configuraciones: se comparan calidad y coste por consulta."),
    ("g-document.png", "Cambiar el tamaño de fragmento", ["EVALUACIÓN"], AMBER,
     "Se prueba con tres preguntas elegidas a mano.",
     "recall@5 y precision@5 antes y después, sobre las mismas 14 preguntas."),
    ("g-alert.png", "Inventa cuando no sabe", ["EVALUACIÓN"], AMBER,
     "Responde con seguridad algo que no está en los documentos.",
     "Casos sin respuesta en el conjunto; se mide el rechazo y la fidelidad."),
    ("g-sdk.png", "Actualizar una librería", ["TEST"], VIOLET,
     "Cambia el formato de salida y la aplicación se rompe.",
     "Tests con dobles en cada PR comprueban formato, fuentes y errores."),
    ("g-user.png", "Preguntas nuevas en producción", ["PRODUCCIÓN"], BLUE,
     "Los usuarios preguntan cosas que el conjunto no cubre.",
     "Se muestrean trazas, se revisan y pasan a ser casos del conjunto."),
    ("g-gear.png", "El juez también se equivoca", ["EVALUACIÓN", "PRODUCCIÓN"], PINK,
     "Se confía a ciegas en la nota del LLM.",
     "Revisión humana de una muestra y registro de los casos no evaluables."),
]


def s02c_casos_de_uso(deck):
    sl = deck.slide(tag="casos-de-uso")
    header(sl, "Punto de partida · casos de uso", "Para qué sirve en la vida real: seis situaciones",
           "Situaciones típicas de un equipo con un asistente RAG en producción. En cada una, sin evaluación se decide por "
           "intuición; con ella, con un número comparable antes y después del cambio.")
    cw, ch = (874 - 20) / 3, 117
    for i, (ic, t, tags, acc, sin, con) in enumerate(CASOS_S19):
        x = 43 + (i % 3) * (cw + 10)
        y = 132 + (i // 3) * (ch + 8)
        box(sl, x, y, cw, ch, fill=CARD)
        box(sl, x, y, cw, 3.5, fill=acc, radius=0)
        circle(sl, x + 10, y + 12, 32, BG, line=acc, lw=1.25)
        img(sl, ic, x + 17, y + 19, w=18, h=18)
        text(sl, x + 50, y + 12, cw - 60, 15, t, size=11, color=TITLE, bold=True)
        tx = x + 50
        for tg in tags:
            tx += _tagchip(sl, tx, y + 29, tg) + 5
        text(sl, x + 12, y + 52, cw - 24, 26, [[("Sin  ", {"bold": True, "color": CORAL}), (sin, {})]], size=8.8, color=TEXT)
        text(sl, x + 12, y + 80, cw - 24, 34, [[("Con  ", {"bold": True, "color": MINT}), (con, {})]], size=8.8, color=TITLE)
    # herramientas
    y0 = 382
    box(sl, 43, y0, 874, 86, fill=CARD, line=BORDER)
    _label(sl, 55, y0 + 8, 500, "Herramientas del ecosistema · las tres primeras, en la demo")
    tools = [("pytest-tile.png", "pytest", "tests deterministas con dobles"),
             ("ragas-tile.png", "Ragas", "métricas de RAG con un juez LLM"),
             ("langfuse.png", "Langfuse", "trazas, datasets y puntuaciones")]
    x = 55
    for ic, t, b in tools:
        box(sl, x, y0 + 27, 200, 50, fill=CARD2)
        iw, ih = img_size(ic, h=30)
        if iw > 40:
            iw, ih = img_size(ic, w=40)
        img(sl, ic, x + 8, y0 + 27 + (50 - ih) / 2, w=iw, h=ih)
        text(sl, x + 56, y0 + 33, 140, 14, t, size=10.5, color=TITLE, bold=True)
        text(sl, x + 56, y0 + 50, 140, 24, b, size=8.3, color=TEXT)
        x += 208
    box(sl, x, y0 + 27, 917 - 12 - x, 50, fill=BG, line=BORDER)
    text(sl, x + 10, y0 + 31, 917 - 32 - x, 12, "OTRAS QUE VERÉIS", size=8, color=MUTED, bold=True)
    text(sl, x + 10, y0 + 46, 917 - 32 - x, 28, "DeepEval · promptfoo · LangSmith · Arize Phoenix · OpenAI Evals",
         size=9, color=TITLE)
    takeaway(sl, "Cada caso es una pregunta con respuesta medible: ¿es mejor, peor o igual, y cuánto cuesta averiguarlo?",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """18:37–18:39. Bajar la idea a situaciones reconocibles. Las seis tarjetas son casos típicos, no empresas concretas. Leer dos o tres y preguntar cuál les ha pasado. Etiquetas: TEST (lo para un test con dobles), EVALUACIÓN (lo mide el conjunto con métricas), PRODUCCIÓN (aparece con tráfico real).
1 Modelo más barato: comparación de dos configuraciones cambiando una sola variable (bloque 5). 2 Tamaño de fragmento: es el caso conductor de la clase (320 frente a 900). 3 Inventar: los 6 casos sin respuesta del conjunto y las métricas de rechazo y Faithfulness. 4 Librería: tests con dobles (bloque 4). 5 Preguntas nuevas: evaluación online y Langfuse (bloque 5). 6 El juez se equivoca: revisión manual de al menos cinco respuestas y registro de no evaluables (bloque 3).
Abajo, herramientas: pytest, Ragas y Langfuse son las de la demo. Las otras se citan solo para que las reconozcan; no se comparan ni se usan en clase.
QUÉ ABRIR: nada; diapositiva conceptual.
PREGUNTA: ¿cuál de estas seis situaciones os ha pasado ya?
""" + F_INTRO)
    return sl


SLIDES = [s01_portada, s02_qr, s02a_que_es_evaluar, s02b_tests_y_evaluacion, s02c_casos_de_uso, s03_caso, s04_modelo_sistema, s05_anatomia, s06_pipeline, s07_vivo1, s08_formulas,
          s09_ejemplo, s10_rechazo, s11_vivo2]
