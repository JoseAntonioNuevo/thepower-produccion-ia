"""S19 · Diapositivas 15–26: bloque 3 (generación) y bloque 4 (testing automatizado)."""
from deck_lib import *  # noqa: F401,F403

F_RAGAS = "código de ragas==0.4.3 instalado en evaluador/.venv (inspeccionado el 17/11/2026)"


def _paso(sl, x, y, w, h, n, titulo, cuerpo, col, fill=CARD):
    box(sl, x, y, w, h, fill=fill)
    badge(sl, x + 10, y + 10, n, fill=col, d=18, size=9.5)
    text(sl, x + 36, y + 10, w - 46, 18, titulo, size=11, color=TITLE, bold=True)
    text(sl, x + 10, y + 34, w - 20, h - 40, cuerpo, size=9.5, color=TEXT)


def s12_faithfulness(deck):
    sl = deck.slide(tag="faithfulness")
    header(sl, "Métricas de generación · Faithfulness", "Faithfulness: ¿cada afirmación se apoya en el contexto?",
           "Mide si la respuesta se deduce de los fragmentos que recibió el generador. Detecta lo inventado; "
           "no comprueba que la respuesta sea correcta ni que esté completa.")
    tag(sl, 43, 124, "ilustrativo")
    # entradas
    box(sl, 43, 146, 430, 100, fill=CARD)
    text(sl, 55, 154, 400, 12, "ENTRADAS: PREGUNTA, RESPUESTA Y CONTEXTO", size=8.5, color=MUTED, bold=True)
    text(sl, 55, 170, 408, 72, [
        [("Pregunta  ", {"bold": True, "color": MINT_L}), ("¿A qué hora es la copia completa y cada cuánto se prueba la restauración?", {})],
        [("Respuesta  ", {"bold": True, "color": MINT_L}), ("«La copia completa es a las 02:00 UTC. La restauración se prueba cada día.»", {})],
        [("Contexto  ", {"bold": True, "color": MINT_L}), ("«…copia completa diaria a las 02:00 UTC… prueba de restauración semanal…»", {})],
    ], size=9.5, color=TEXT, space=3)
    _paso(sl, 43, 256, 210, 108, 1, "Extraer afirmaciones",
          "El juez parte la respuesta en afirmaciones atómicas:\nA1 · la copia es a las 02:00 UTC\nA2 · la restauración se prueba cada día", AMBER)
    _paso(sl, 263, 256, 210, 108, 2, "Veredicto por afirmación",
          "¿Se deduce del contexto?\nA1 · sí  → 1\nA2 · no  → 0  (el contexto dice «semanal»)", AMBER)
    line(sl, 255, 310, 262, 310, color=AMBER, head="end")
    # resultado
    box(sl, 43, 374, 430, 92, fill=AMBER_BG)
    text(sl, 55, 382, 300, 12, "FAITHFULNESS", size=9, color=AMBER, bold=True)
    text(sl, 55, 398, 200, 36, "1 / 2 = 0,50", size=26, font=SERIF, color=TITLE)
    text(sl, 255, 384, 208, 30, "afirmaciones apoyadas", size=10, color=TITLE, align="c", bold=True)
    box(sl, 275, 402, 168, 1.2, fill=AMBER, radius=0)
    text(sl, 255, 408, 208, 16, "afirmaciones de la respuesta", size=10, color=AMBER, align="c", bold=True)
    text(sl, 55, 438, 408, 24, "Dos llamadas al juez por respuesta. Sin afirmaciones, Ragas devuelve NaN.", size=9.5, color=TEXT)
    # derecha: lo que no mide
    box(sl, 487, 124, 430, 178, fill=CORAL_BG, line=CORAL)
    text(sl, 499, 134, 400, 12, "LO QUE NO MIDE: FIEL NO ES CORRECTA", size=9, color=CORAL, bold=True)
    text(sl, 499, 152, 406, 36, "La misma pregunta, otra respuesta", size=13, font=SERIF, color=TITLE)
    text(sl, 499, 176, 406, 30, "«La copia completa es a las 02:00 UTC.»", size=10.5, color=MINT_L, font=MONO, bold=True, check=False)
    text(sl, 499, 200, 150, 30, "1 / 1 = 1,00", size=19, font=SERIF, color=TITLE)
    text(sl, 655, 200, 250, 44, "Todo lo que dice está en el contexto. Pero no contesta cada cuánto se prueba la restauración.",
         size=9.5, color=TEXT)
    text(sl, 499, 250, 406, 46, "Una respuesta puede ser fiel e incompleta, fiel a un fragmento equivocado, o fiel a un "
         "documento desactualizado. Por eso hay criterio de acierto y revisión humana.", size=9.5, color=TEXT)
    table(sl, 487, 312, 430, [150, 280], [
        ["Faithfulness…", ""],
        ["Sí detecta", "Datos que no están en el contexto entregado"],
        ["No detecta", "Respuesta incompleta o que no contesta la pregunta"],
        ["No detecta", "Contexto equivocado: recuperación mal hecha"],
        ["Necesita", "Contexto no vacío; si no, no es evaluable"],
        ["Rango", "0 a 1. Más alto, más apoyada"],
    ], size=9.5, row_h=25.5, bold_cols=(0,), colors={0: MINT_L})
    takeaway(sl, "Faithfulness responde «¿se lo ha inventado?». No responde «¿es verdad?» ni «¿está completo?».", label="Idea guía")
    footer(sl, block=3)
    notes(sl, """19:06–19:09. Definir Faithfulness como lo hace Ragas 0.4.3: dos pasos con el juez. Primero descompone la respuesta en afirmaciones atómicas; después decide, afirmación por afirmación, si se deduce del contexto. La puntuación es el cociente. Recorrer el ejemplo ilustrativo: dos afirmaciones, una apoyada: 0,50. Pasar al recuadro de la derecha: una respuesta más corta obtiene 1,00 y sin embargo no contesta media pregunta. Es la frase del enunciado: la fidelidad al contexto no demuestra por sí sola que la respuesta sea correcta. Mencionar que con cero afirmaciones Ragas devuelve NaN y que con contexto vacío lanza un error: ambos casos se registran como no evaluables.
QUÉ ABRIR: nada; el caso real equivalente (T07) se ve en el vivo 3.
PREGUNTA: ¿qué puntuación tendría una respuesta que copia literalmente un fragmento que no tiene nada que ver con la pregunta?
Fuentes: """ + F_RAGAS + """; enlace del enunciado a faithfulness/metric.py (v0.4.3).""")
    return sl


def s13_relevancy(deck):
    sl = deck.slide(tag="relevancy")
    header(sl, "Métricas de generación · Answer Relevancy", "Answer Relevancy: ¿la respuesta habla de lo que se preguntó?",
           "El enunciado la llama Response Relevancy y se implementa con AnswerRelevancy. No usa el contexto: "
           "compara la pregunta original con las preguntas que el juez deduce de la respuesta.")
    tag(sl, 43, 124, "ilustrativo")
    y = 148
    _paso(sl, 43, y, 205, 124, 1, "Respuesta del sistema",
          "«La copia completa es a las 02:00 UTC y la restauración se prueba cada semana.»", AMBER)
    _paso(sl, 266, y, 205, 124, 2, "El juez inventa 3 preguntas",
          "¿A qué hora es la copia completa?\n¿Cada cuánto se prueba la restauración?\n¿Cuándo se hacen las copias?", AMBER)
    _paso(sl, 489, y, 205, 124, 3, "Embeddings y coseno",
          "Cada pregunta generada se compara con la pregunta original:\n0,91 · 0,88 · 0,85", AMBER)
    for x in (250, 473, 696):
        line(sl, x, y + 62, x + 14, y + 62, color=AMBER)
    box(sl, 712, y, 205, 124, fill=AMBER_BG)
    text(sl, 724, y + 8, 180, 12, "ANSWER RELEVANCY", size=9, color=AMBER, bold=True)
    text(sl, 724, y + 26, 180, 36, "0,88", size=30, font=SERIF, color=TITLE)
    text(sl, 724, y + 68, 184, 50, "Media de los tres cosenos. Si el juez marca la respuesta como evasiva, la nota es 0.",
         size=9.5, color=TEXT)
    # cómo leerla
    casos = [("Respuesta que contesta lo preguntado", 0.88, MINT, "Las preguntas deducidas se parecen a la original."),
             ("Respuesta correcta pero sobre otro tema", 0.35, AMBER, "Fiel al contexto, pero no es lo que se pidió."),
             ("«No lo sé», «depende»", 0.0, CORAL, "Evasiva: el juez la marca y la nota se anula.")]
    text(sl, 43, 284, 500, 12, "CÓMO LEERLA · VALORES DE EJEMPLO", size=8.5, color=MUTED, bold=True)
    for i, (t, v, col, d) in enumerate(casos):
        yy = 302 + i * 36
        text(sl, 43, yy, 250, 14, t, size=10.5, color=TITLE, bold=True)
        text(sl, 43, yy + 15, 250, 14, d, size=9, color=MUTED)
        bar(sl, 300, yy + 6, 200, 12, v, color=col)
        text(sl, 508, yy + 3, 40, 16, f"{v:.2f}".replace(".", ","), size=11, color=col, bold=True, font=MONO, check=False)
    # derecha
    box(sl, 566, 284, 351, 124, fill=CORAL_BG, line=CORAL)
    text(sl, 578, 292, 330, 12, "LO QUE NO MIDE", size=9, color=CORAL, bold=True)
    bullets(sl, 578, 310, 330, 94, [
        "Si lo que dice la respuesta es verdad.",
        "Si se apoya en los documentos (eso es Faithfulness).",
        "Depende del modelo de embeddings: dos jueces distintos no dan notas comparables.",
    ], size=10, mark_color=CORAL)
    box(sl, 43, 416, 874, 50, fill=CARD, line=BORDER)
    text(sl, 55, 423, 300, 12, "DETALLE DE LA API · RAGAS 0.4.3", size=8.5, color=MINT, bold=True)
    code_block(sl, 55, 439, 850, [
        "AnswerRelevancy(llm=juez, embeddings=emb).ascore(user_input=…, response=…)   # sin retrieved_contexts",
    ], size=9.5, color=MINT_L)
    takeaway(sl, "Faithfulness mira hacia el contexto; Answer Relevancy mira hacia la pregunta. Ninguna de las dos mira hacia la verdad.",
             label="Idea guía")
    footer(sl, block=3)
    notes(sl, """19:09–19:11. Explicar el mecanismo real de AnswerRelevancy en Ragas 0.4.3: el juez genera tres preguntas a partir de la respuesta (strictness=3) e indica si la respuesta es evasiva; después se calcula el coseno entre el embedding de cada pregunta generada y el de la pregunta original; la nota es la media, o 0 si es evasiva. Por eso necesita un evaluador y unos embeddings inicializados, como avisa el enunciado. Señalar el detalle comprobado al instalar: ascore recibe user_input y response; no acepta retrieved_contexts. Los valores de las barras son de ejemplo. Contrastar con Faithfulness: una mira al contexto y otra a la pregunta.
QUÉ ABRIR: evaluador/README.md, tabla «Lo que pide el enunciado y lo que hay en ragas 0.4.3».
PREGUNTA: una respuesta perfecta a una pregunta distinta de la que se hizo, ¿qué nota de fidelidad y de relevancia tendría?
Fuentes: """ + F_RAGAS + """ (answer_relevancy/metric.py); enunciado de S19.""")
    return sl


def s14_juez(deck):
    sl = deck.slide(tag="juez")
    header(sl, "LLM como juez", "El juez también es un modelo: qué aporta y qué límites tiene",
           "Un modelo que evalúa a otro permite puntuar miles de respuestas libres. Pero tiene coste, variación y "
           "sesgos propios: es un instrumento de medida que también hay que controlar.")
    box(sl, 43, 126, 270, 150, fill=GREEN_BG)
    img(sl, "ragas-tile.png", 55, 136, w=30, h=30)
    text(sl, 94, 138, 210, 12, "QUÉ APORTA", size=9, color=MINT, bold=True)
    text(sl, 94, 152, 210, 18, "Escala y matiz", size=13, font=SERIF, color=TITLE)
    bullets(sl, 55, 178, 250, 96, ["Evalúa texto libre sin una respuesta única.",
                                    "Entiende paráfrasis: no castiga otra redacción.",
                                    "Se repite en cada cambio, de forma automática."], size=10)
    box(sl, 323, 126, 594, 150, fill=CARD)
    text(sl, 335, 136, 400, 12, "TRES REGLAS PARA FIARSE DEL NÚMERO", size=9, color=AMBER, bold=True)
    reglas = [("Mismo juez", "Mismo modelo, misma versión de Ragas y mismos embeddings en las dos ejecuciones que se comparan."),
              ("Con cobertura", "Junto a la media, cuántas respuestas se pudieron puntuar y por qué fallaron las demás."),
              ("Con una persona", "Al menos cinco respuestas revisadas a mano para ver si el juez acierta.")]
    for i, (t, d) in enumerate(reglas):
        x = 335 + i * 192
        box(sl, x, 156, 184, 110, fill=CARD2)
        badge(sl, x + 10, 166, i + 1, fill=AMBER, d=18, size=9.5)
        text(sl, x + 36, 167, 140, 16, t, size=11, color=TITLE, bold=True)
        text(sl, x + 10, 192, 166, 70, d, size=9.5, color=TEXT)
    table(sl, 43, 286, 874, [150, 330, 394], [
        ["Límite del juez", "Qué provoca", "Cómo lo controla la demo"],
        ["No es determinista", "La misma respuesta puede recibir notas distintas", "Versión y modelo fijados; margen de 0,10 en los umbrales"],
        ["Se equivoca", "Da por apoyado algo que no lo está, o al revés", "Revisión manual de seis casos elegidos de antemano"],
        ["Falla o no responde", "Timeout, salida no válida o NaN", "«No evaluable» con motivo; baja la cobertura, no la media"],
        ["Cuesta dinero", "5 llamadas al juez por respuesta evaluada", "Tokens y coste del juez en una traza aparte"],
        ["Cambia con el tiempo", "Otro modelo u otra versión: otra escala", "La identidad del evaluador viaja en cada puntuación"],
        ["Sesgos propios", "Prefiere textos largos o de su mismo estilo", "No se usa como única prueba: hay criterio de acierto"],
    ], size=10, row_h=25.5, bold_cols=(0,), colors={0: MINT_L})
    takeaway(sl, "Una nota del juez es una medición con error. Se acompaña de su versión, de su cobertura y de una revisión humana.",
             label="Idea guía")
    footer(sl, block=3)
    notes(sl, """19:11–19:13. Presentar el patrón «LLM como juez» y sus límites. Aporta escala y comprensión de paráfrasis: permite evaluar texto libre en cada cambio. Recorrer la tabla fila a fila enlazando cada límite con su control en la demo: no determinismo (versiones fijadas y margen), errores del juez (revisión manual), fallos (no evaluables con motivo), coste (5 llamadas por respuesta: 2 de Faithfulness y 3 de AnswerRelevancy; consumo separado), cambio de versión (la identidad del evaluador viaja en cada fila de puntuaciones.jsonl y `comparar` se niega a mezclar evaluadores) y sesgos (no es la única prueba).
QUÉ ABRIR: nada.
PREGUNTA: si mañana cambio el modelo del juez, ¿puedo comparar la nota de hoy con la de ayer?
Fuentes: """ + F_RAGAS + """; enunciado de S19 («Comprueba las puntuaciones»).""")
    return sl


def s15_aislado(deck):
    sl = deck.slide(tag="aislado")
    header(sl, "Evaluador aislado", "Dos entornos que solo se hablan con archivos",
           "El enunciado pide aislar el evaluador y fijar ragas==0.4.3 y langchain-community==0.3.31. El RAG no "
           "importa Ragas ni Ragas importa el RAG: intercambian JSONL con versión.")
    # entorno RAG
    box(sl, 43, 128, 262, 150, fill=BLUE_BG)
    img(sl, "postgresql.png", 55, 138, w=28, h=28)
    text(sl, 92, 138, 205, 12, "ENTORNO DEL RAG", size=9, color=BLUE, bold=True)
    text(sl, 92, 152, 205, 16, "demo-evaluacion/.venv", size=10, font=MONO, color=TITLE, bold=True, check=False)
    bullets(sl, 55, 178, 242, 96, ["psycopg, openai, langfuse", "46 paquetes bloqueados en uv.lock",
                                    "python s19.py lote · informe"], size=9.5, mark_color=BLUE)
    # archivos
    for y, nombre, ver, col, direc in [(138, "respuestas.jsonl", "s19.respuestas.v1", MINT, "→"),
                                       (212, "puntuaciones.jsonl", "s19.puntuaciones.v1", AMBER, "←")]:
        box(sl, 345, y, 270, 58, fill=CARD, line=col)
        img(sl, "g-json-script.png", 355, y + 15, w=28, h=28)
        text(sl, 392, y + 10, 215, 16, nombre, size=11, font=MONO, color=TITLE, bold=True, check=False)
        text(sl, 392, y + 30, 215, 14, f"schema_version: {ver}", size=8.5, font=MONO, color=col, check=False)
    line(sl, 307, 167, 343, 167, color=MINT)
    line(sl, 617, 167, 653, 167, color=MINT)
    line(sl, 653, 241, 617, 241, color=AMBER)
    line(sl, 343, 241, 307, 241, color=AMBER)
    # entorno evaluador
    box(sl, 655, 128, 262, 150, fill=AMBER_BG)
    img(sl, "ragas-tile.png", 667, 138, w=28, h=28)
    text(sl, 704, 138, 205, 12, "ENTORNO DEL EVALUADOR", size=9, color=AMBER, bold=True)
    text(sl, 704, 152, 205, 16, "evaluador/.venv", size=10, font=MONO, color=TITLE, bold=True, check=False)
    bullets(sl, 667, 178, 242, 96, ["ragas==0.4.3, langchain-community==0.3.31", "100 paquetes bloqueados en su uv.lock",
                                     "python evaluar.py <carpeta>"], size=9.5, mark_color=AMBER)
    # código
    tag(sl, 43, 288, "codigo")
    term(sl, 43, 306, 520, 160, [
        ("from ragas.metrics.collections import AnswerRelevancy, Faithfulness", MINT_L),
        "",
        "r = await Faithfulness(llm=juez).ascore(",
        "        user_input=fila[\"user_input\"],",
        "        response=fila[\"response\"],",
        "        retrieved_contexts=fila[\"retrieved_contexts\"])",
        ("valor = r.value          # float entre 0 y 1, o NaN", AMBER),
        "",
        "r = await AnswerRelevancy(llm=juez, embeddings=emb).ascore(",
        "        user_input=fila[\"user_input\"], response=fila[\"response\"])",
    ], size=9)
    # hallazgos
    box(sl, 575, 288, 342, 178, fill=CARD, line=CORAL)
    text(sl, 587, 297, 320, 12, "COMPROBADO AL INSTALAR LAS VERSIONES FIJADAS", size=8.5, color=CORAL, bold=True)
    text(sl, 587, 315, 320, 146, [
        {"runs": [("Coincide con el enunciado. ", {"bold": True, "color": MINT_L}),
                  ("ragas.metrics.collections, Faithfulness, AnswerRelevancy, la firma de ascore y .value.", {})], "space": 5},
        {"runs": [("AnswerRelevancy ", {"bold": True, "color": TITLE}),
                  ("no acepta retrieved_contexts: solo pregunta y respuesta.", {})], "space": 5},
        {"runs": [("Guía «Ragas con Gemini». ", {"bold": True, "color": TITLE}),
                  ("Su cliente síncrono falla en ascore con TypeError. La demo usa un cliente asíncrono, vía OpenRouter, y lo declara.", {})], "space": 5},
        {"runs": [("Telemetría. ", {"bold": True, "color": TITLE}),
                  ("Ragas envía datos de uso salvo RAGAS_DO_NOT_TRACK=true.", {})]},
    ], size=9.5, color=TEXT, space=5)
    takeaway(sl, "Aislar el evaluador permite actualizarlo o sustituirlo sin tocar el sistema evaluado, y deja escrito con qué versión se midió.",
             label="Idea guía")
    footer(sl, block=3)
    notes(sl, """19:13–19:15. Explicar por qué se aísla: Ragas arrastra más de cien dependencias; mezcladas con las del RAG, actualizar el evaluador podría cambiar el sistema evaluado. Cada entorno tiene su pyproject.toml y su uv.lock. Solo comparten dos archivos JSONL con schema_version; si el formato cambia, el lector antiguo falla con un mensaje claro. Leer el código: es exactamente lo que indica el enunciado (ragas.metrics.collections, Faithfulness.ascore con user_input, response y retrieved_contexts, lectura en .value). Comentar los hallazgos al instalar las versiones fijadas: AnswerRelevancy no recibe contextos; la llamada de la guía «Ragas con Gemini» devuelve un cliente síncrono y ascore falla con TypeError (comprobado el 17/11/2026); por eso el juez usa un cliente asíncrono compatible con OpenAI contra OpenRouter, que también puede usar modelos de Gemini. Ragas envía telemetría salvo que se desactive. El juez real se elige en .env; el 22/11/2026 se ejecutó con Claude Opus 5.5 y puntuó todas las respuestas emitidas del test.
QUÉ ABRIR: evaluador/pyproject.toml y evaluador/README.md.
PREGUNTA: ¿qué ganamos al intercambiar archivos en vez de importar el evaluador como una librería más?
Fuentes: """ + F_RAGAS + """; guía «Ragas con Gemini» (docs.ragas.io, consultada el 16/11/2026); evaluador/README.md.""")
    return sl


def s16_no_evaluables(deck):
    sl = deck.slide(tag="no-evaluables")
    header(sl, "No evaluables y cobertura", "Lo que no se pudo puntuar no es un acierto ni un cero",
           "A veces el juez falla, el contexto está vacío o la nota es NaN. Esos casos se registran con su motivo "
           "y se informa de cuántas respuestas cubre la media.")
    table(sl, 43, 126, 520, [150, 170, 200], [
        ["Motivo registrado", "Cuándo ocurre", "Qué se hace"],
        [("rechazo_sin_respuesta", {"font": MONO}), "El sistema se abstuvo", "No se juzga: se mide como rechazo"],
        [("error_sistema", {"font": MONO}), "El RAG falló en ese caso", "Cuenta como error del sistema"],
        [("respuesta_vacia", {"font": MONO}), "Texto vacío", "No se envía al juez"],
        [("contexto_vacio", {"font": MONO}), "Sin fragmentos", "Faithfulness no existe"],
        [("error_evaluador:Tipo", {"font": MONO}), "Timeout o salida no válida", "Se anota el tipo de fallo"],
        [("nan", {"font": MONO}), "El juez no extrae afirmaciones", "Se anota; nunca se escribe NaN"],
    ], size=10, row_h=26, colors={0: MINT_L})
    text(sl, 43, 316, 520, 12, "COBERTURA = RESPUESTAS PUNTUADAS / RESPUESTAS QUE HABÍA QUE PUNTUAR", size=8.5, color=MINT, bold=True)
    text(sl, 43, 334, 520, 44, "Los rechazos no cuentan en el denominador: no había texto que juzgar. Los fallos del juez "
         "sí cuentan: había que puntuar y no se pudo.", size=10.5, color=TEXT)
    term(sl, 43, 384, 520, 82, [
        ('{"caso_id": "T09", "metrica": "faithfulness", "valor": null,', TEXT),
        (' "evaluable": false, "motivo": "error_evaluador:TimeoutError",', CORAL),
        (' "evaluador": {"ragas": "0.4.3", "llm": "…"}, "consumo": {…}}', TEXT),
    ], title="puntuaciones.jsonl · una fila no evaluable", size=9)
    # derecha: el mismo lote contado de tres formas
    box(sl, 577, 126, 340, 340, fill=CARD)
    tag(sl, 589, 136, "ilustrativo")
    text(sl, 589, 158, 316, 36, "14 respuestas emitidas: 11 puntuadas, 2 timeouts del juez y 1 NaN", size=12.5,
         font=SERIF, color=TITLE)
    formas = [("Fallos contados como acierto", 0.96, CORAL, "Infla la nota: un juez caído «aprueba»."),
              ("Fallos contados como cero", 0.75, CORAL, "Hunde la nota por un problema del juez."),
              ("Media de lo puntuado", 0.95, MINT, "Honesta solo si va con su cobertura."),
              ("Cobertura · 11 de 14", 0.79, AMBER, "Por debajo del mínimo: el control falla.")]
    y = 204
    for t, v, col, d in formas:
        text(sl, 589, y, 220, 14, t, size=10.5, color=TITLE, bold=True)
        text(sl, 860, y - 1, 45, 16, f"{v:.2f}".replace(".", ","), size=12, color=col, bold=True, font=MONO, align="r", check=False)
        bar(sl, 589, y + 18, 316, 9, v, color=col)
        text(sl, 589, y + 31, 316, 14, d, size=9.5, color=MUTED)
        y += 62
    takeaway(sl, "Toda media de un juez se publica con su cobertura y con la lista de motivos. Una cobertura baja también es un fallo.",
             label="Idea guía")
    footer(sl, block=3)
    notes(sl, """19:15–19:17. El enunciado: registrar errores del evaluador, contexto vacío y valores NaN como no evaluables, con el motivo y la cobertura; no convertirlos en aciertos. Recorrer los seis motivos de la tabla, que son los del contrato de la demo. Definir cobertura: puntuadas entre las que había que puntuar; los rechazos no entran en el denominador, los fallos del juez sí. El panel de la derecha es un ejemplo ilustrativo con el mismo lote contado de tres formas: como acierto (0,96), como cero (0,75) o fuera de la media (0,95, con cobertura 0,79). Ninguna de las dos primeras es verdad. En la demo, una cobertura por debajo del umbral hace fallar el control de regresión aunque la media sea perfecta.
QUÉ ABRIR: evaluacion/intercambio.py (MOTIVOS_NO_EVALUABLE).
PREGUNTA: el juez falla en 3 de 14 respuestas y la media sale 0,95. ¿Qué número falta para poder fiarse?
Fuentes: enunciado de S19; contrato s19.puntuaciones.v1 de la demo y sus tests.""")
    return sl


def s17_revision(deck):
    sl = deck.slide(tag="revision")
    header(sl, "Revisión humana", "Seis respuestas leídas a mano: dónde discrepa el juez",
           "El enunciado pide revisar al menos cinco respuestas. Los casos se eligen antes de ejecutar el test, para "
           "no escoger después solo los que confirman lo que queremos ver.")
    tag(sl, 43, 124, "doble")
    text(sl, 252, 125, 660, 14, "Revisión de ejemplo hecha por el agente de preparación sobre el test A. No sustituye a la de una persona con resultados reales.",
         size=9, color=MUTED)
    table(sl, 43, 146, 874, [44, 250, 60, 76, 444], [
        ["Caso", "Qué respondió el sistema", "Fidelidad", "Revisión", "Qué ve la persona"],
        ["T02", "Rechazo con HTTP 403 y TENANT_MISMATCH, con su fuente", ("1,00", {"align": "c"}), ("Correcta", {"color": MINT_L, "bold": True}),
         "Coincide con el juez. Añade un encabezado copiado: ruido, no error."],
        ["T07", "Copia completa a las 02:00 UTC", ("1,00", {"align": "c"}), ("Parcial", {"color": AMBER, "bold": True}),
         "Fiel pero incompleta: no dice que la restauración se prueba cada semana."],
        ["T12", "Soporte 24x7 para SEV-1 y un encabezado sin dato", ("1,00", {"align": "c"}), ("Parcial", {"color": AMBER, "bold": True}),
         "Falta el dato clave: 15 minutos de primera respuesta."],
        ["T14", "«No consta…»", ("—", {"align": "c"}), ("Incorrecta", {"color": CORAL, "bold": True}),
         "Abstención incorrecta: la respuesta estaba en los documentos 09 y 10."],
        ["T16", "Un encabezado repetido, sin contenido", ("1,00", {"align": "c"}), ("Incorrecta", {"color": CORAL, "bold": True}),
         "Respuesta indebida: SEV-4 no existe. El juez le da fidelidad máxima."],
        ["T18", "«No consta…»", ("—", {"align": "c"}), ("Correcta", {"color": MINT_L, "bold": True}),
         "Rechazo correcto: el corpus no habla de compresión."],
    ], size=9.5, row_h=28, bold_cols=(0,), colors={0: MINT_L})
    box(sl, 43, 352, 430, 114, fill=CARD)
    text(sl, 55, 360, 400, 12, "LA PLANTILLA · python s19.py revision", size=8.5, color=MINT, bold=True)
    bullets(sl, 55, 378, 410, 86, ["¿Es correcta? sí / no / parcial",
                                    "¿Las fuentes citadas la respaldan?",
                                    "¿Es fiel pero incompleta?",
                                    "¿Discrepa del juez? Si discrepa, manda la persona y se anota."], size=10, space=3)
    box(sl, 487, 352, 430, 114, fill=CORAL_BG, line=CORAL)
    text(sl, 499, 360, 400, 12, "LO QUE ENSEÑA ESTE EJEMPLO", size=8.5, color=CORAL, bold=True)
    text(sl, 499, 378, 406, 84, "Cuatro respuestas con fidelidad 1,00 y solo una correcta del todo. La fidelidad dice "
         "que el texto sale del contexto; no dice que conteste la pregunta. Sin la lectura humana, T16 pasaría "
         "por una buena respuesta.", size=10.5, color=TEXT)
    takeaway(sl, "El juez da escala; la persona da criterio. El enunciado pide cinco lecturas; aquí, seis: ya se ve si el número mide lo que creemos.",
             label="Idea guía")
    footer(sl, block=3)
    notes(sl, """19:17–19:19. El enunciado pide revisar manualmente al menos cinco respuestas. En la demo los seis casos se fijan en datos/revision-casos.json antes de ejecutar el test: cuatro respondibles y dos sin respuesta. La tabla resume la revisión de ejemplo del test A del perfil doble (archivo revision-manual-EJEMPLO-rellena.csv), hecha por el agente de preparación para tener material que enseñar; no sustituye a la revisión humana de una ejecución real. Leer T07 y T16: fidelidad 1,00 en una respuesta incompleta y en una respuesta indebida. Recordar que el juez de este ejemplo es el doble léxico: con un juez real las notas cambiarán, el método no.
QUÉ ABRIR: resultados/ejemplo-doble/test-A/revision-manual-EJEMPLO-rellena.csv.
PREGUNTA: ¿por qué elegimos los casos de revisión antes de ver los resultados?
Fuentes: enunciado de S19 («Revisa manualmente al menos cinco respuestas»); resultados/ejemplo-doble/test-A (perfil doble, 17/11/2026).""")
    return sl


def s18_vivo3(deck):
    sl = deck.slide(tag="vivo3")
    header_s(sl, "En vivo 3 · Generación", "Puntuar en el entorno aislado y leer a mano",
             "El evaluador lee respuestas.jsonl, escribe puntuaciones.jsonl y el informe añade media y cobertura.")
    code_panel_s(sl, 48, 153.8, 852.8, 64, [
        "cd evaluador && uv run python evaluar.py ../resultados/mi-val-A",
        "cd .. && python s19.py informe resultados/mi-val-A",
    ], size=14.5)
    term(sl, 48, 228, 852.8, 74, [
        ("⚠  JUEZ DOBLE: métricas de Ragas con un juez local determinista. NO miden ninguna respuesta.", AMBER),
        "Evaluador: ragas 0.4.3 · langchain-community 0.3.31 · juez doble-lexico",
        "  faithfulness      media 1.00 · evaluables 6/6 · no evaluables: {'rechazo_sin_respuesta': 2}",
        "  answer_relevancy  media 0.41 · evaluables 6/6 · no evaluables: {'rechazo_sin_respuesta': 2}",
    ], size=9.5)
    kv_rows_s(sl, 314, [
        ("6/6", "Seis respuestas emitidas y seis puntuadas: cobertura 1,00."),
        ("2 rechazos", "No se juzgan: no hay texto. Se miden como rechazo, aparte."),
        ("Revisión", "Abrir el CSV de ejemplo: T16 tiene fidelidad 1,00 y es una respuesta indebida."),
    ], pitch=44, size=14.5)
    band_s(sl, "Las clases de Ragas son las reales; el juez es un doble. Con juez real: evaluar.py --modo real --execute.")
    footer_s(sl)
    notes(sl, """19:19–19:24. EN VIVO 3. 1) Entrar en evaluador/ y ejecutar evaluar.py sobre la carpeta de validación. La primera importación de Ragas tarda; haberla ejecutado antes de clase. Leer el aviso: el juez es un doble léxico; las clases Faithfulness y AnswerRelevancy sí son las de ragas 0.4.3. 2) Abrir puntuaciones.jsonl y enseñar una fila evaluable (valor, evaluador, consumo) y una con motivo rechazo_sin_respuesta. 3) Volver a la raíz y repetir informe: ahora aparecen media y cobertura de las dos métricas. 4) Abrir el CSV de revisión de ejemplo y leer T16. Decir que el modo real exige clave y --execute; se ejecutó el 22/11/2026 con Claude Opus 5.5 (resultados/ejemplo-real).
QUÉ ABRIR: terminal; resultados/mi-val-A/puntuaciones.jsonl; resultados/ejemplo-doble/test-A/revision-manual-EJEMPLO-rellena.csv.
PREGUNTA: ¿por qué los dos rechazos no bajan la cobertura?
Fuentes: salida real de evaluar.py con el juez doble (resultados/ejemplo-doble/validacion-A, 17/11/2026).""")
    return sl


def s19_piramide(deck):
    sl = deck.slide(tag="piramide")
    header(sl, "Testing automatizado", "La pirámide de tests de un sistema de IA",
           "No todo necesita un modelo. La mayor parte de lo que puede romperse es código normal y se prueba con "
           "tests deterministas; las evaluaciones con modelo son pocas, caras y se ejecutan aparte.")
    capas = [(150, "Revisión humana", "muestreo · minutos por caso", CORAL, CORAL_BG),
             (250, "Evaluación con modelo real", "@pytest.mark.llm · de pago · antes de desplegar", AMBER, AMBER_BG),
             (350, "Integración con servicios locales", "@pytest.mark.db · pgvector en Docker · segundos", VIOLET, VIOLET_BG),
             (450, "Tests deterministas con dobles", "131 en la demo · milisegundos · en cada cambio", MINT, GREEN_BG)]
    cx = 268
    for i, (w, t, d, col, fill) in enumerate(capas):
        y = 132 + i * 82
        box(sl, cx - w / 2, y, w, 74, fill=fill, line=col)
        text(sl, cx - w / 2 + 8, y + 16, w - 16, 18, t, size=11.5 if w > 160 else 10.5, color=TITLE, bold=True, align="c")
        text(sl, cx - w / 2 + 8, y + 38, w - 16, 28, d, size=9, color=col, align="c")
    line(sl, 30, 452, 30, 140, color=MUTED)
    # derecha: qué prueba cada nivel
    table(sl, 512, 128, 405, [120, 285], [
        ["Nivel", "Qué comprueba en la demo"],
        ["Dobles", "Ingesta sin duplicados, fragmentación, fórmulas de precision y recall, formato, fuentes inventadas, errores del proveedor, contrato JSONL, informe, regresión"],
        ["Servicios locales", "Que pgvector reconstruye el índice sin duplicar y ordena por coseno"],
        ["Modelo real", "Que el RAG real cita una fuente y rechaza lo que no consta; que el juez puntúa"],
        ["Persona", "Que la nota del juez coincide con una lectura atenta"],
    ], size=9.5, row_h=50, bold_cols=(0,), colors={0: MINT_L})
    box(sl, 512, 388, 405, 78, fill=CARD, line=BORDER)
    img(sl, "pytest-tile.png", 524, 400, w=34, h=34)
    text(sl, 568, 396, 340, 12, "POR QUÉ LA BASE ES ANCHA", size=8.5, color=MINT, bold=True)
    text(sl, 568, 412, 340, 50, "Un test que tarda milisegundos y da siempre lo mismo se ejecuta en cada cambio. "
         "Uno que cuesta dinero y varía se ejecuta poco: no puede ser la única red.", size=9.5, color=TEXT)
    text(sl, 36, 458, 200, 12, "más lento, más caro, menos repetible ↑", size=8, color=MUTED, check=False)
    takeaway(sl, "Cuanto más arriba, más lento, caro y variable. Lo que se pueda comprobar sin modelo, se comprueba sin modelo.",
             label="Idea guía")
    footer(sl, block=4)
    notes(sl, """19:24–19:25. Tercera parte del temario: testing automatizado de agentes y pipelines RAG. Presentar la pirámide de abajo arriba. Base: tests deterministas con dobles, 103 en la demo, sin red, sin Docker y sin claves; se ejecutan en cada cambio. Segundo nivel: integración con servicios locales, aquí PostgreSQL con pgvector en Docker (marcador db). Tercer nivel: evaluaciones con modelo real, marcadas con @pytest.mark.llm y excluidas por defecto porque cuestan dinero y no son deterministas. Cima: revisión humana por muestreo. La tabla dice qué comprueba cada nivel en la demo.
QUÉ ABRIR: carpeta tests/ de la demo.
PREGUNTA: ¿qué pasaría si todos nuestros tests necesitaran llamar al modelo?
Fuentes: enunciado de S19 («Automatiza las comprobaciones»); tests de la demo (131 pasan, 3 excluidos, 22/11/2026).""")
    return sl


def s20_dobles(deck):
    sl = deck.slide(tag="dobles")
    header(sl, "pytest con dobles", "Respuestas simuladas para probar lo que rodea al modelo",
           "Un doble sustituye al modelo por una pieza que devuelve lo que el test decide. Así se prueban el "
           "formato, las fuentes y los errores sin gastar y con un resultado siempre igual.")
    tag(sl, 43, 124, "codigo")
    term(sl, 43, 142, 520, 208, [
        ("def test_sin_evidencia_se_rechaza_sin_llamar_al_generador(sistema):", MINT_L),
        "    almacen, prov, indice_id = sistema",
        ("    generador = GeneradorSimulado(\"no debería ejecutarse\")", AMBER),
        "    r = responder(config(umbral_evidencia=0.99), almacen,",
        "                  Proveedores(prov.embeddings, generador),",
        "                  indice_id, PREGUNTA)",
        "    assert r.rechazo and r.motivo_rechazo == \"evidencia_insuficiente\"",
        ("    assert generador.llamadas == 0      # ni una llamada, ni un céntimo", AMBER),
        "",
        ("@pytest.mark.llm                        # evaluación real: de pago", CORAL),
        ("def test_rag_real_responde_con_fuente_y_rechaza_lo_que_no_consta():", MINT_L),
        "    if os.environ.get(\"S19_EJECUTAR_REAL\") != \"1\":",
        "        pytest.skip(\"exige clave y autorización de gasto\")",
    ], title="tests/test_consulta.py · tests/test_integracion.py", size=8.5)
    term(sl, 43, 358, 520, 108, [
        ("# pyproject.toml", FAINT),
        "addopts = \"-ra -m 'not llm and not db'\"",
        "markers = [\"llm: evaluación real con modelos de pago\",",
        "           \"db: integración con PostgreSQL + pgvector\"]",
        "",
        ("$ uv run pytest", MINT_L),
        ("131 passed, 3 deselected in 1.29s", MINT),
    ], size=8.5)
    img(sl, "pytest-tile.png", 577, 128, w=34, h=34)
    text(sl, 620, 130, 290, 12, "LO QUE PIDE EL ENUNCIADO", size=9, color=MINT, bold=True)
    text(sl, 620, 144, 296, 18, "Cuatro cosas que se prueban sin modelo", size=12.5, font=SERIF, color=TITLE)
    cosas = [("Ingesta sin duplicados", "Reconstruir dos veces deja las mismas filas; un documento copiado con otro nombre no entra dos veces.", MINT),
             ("Formato", "Respuesta, fuentes, documentos, latencia y tokens presentes; el JSONL valida su versión.", BLUE),
             ("Fuentes", "Solo se aceptan citas de documentos que estaban en el contexto; las inventadas se avisan.", AMBER),
             ("Errores", "Si el proveedor falla, el caso queda con su error. No se sustituye por otra respuesta.", CORAL)]
    for i, (t, d, col) in enumerate(cosas):
        side_note(sl, 577, 172 + i * 74, 340, 68, t, d, accent=col, size=9.5)
    takeaway(sl, "Los dobles prueban el código que rodea al modelo. La calidad del modelo se mide aparte, con el marcador llm.",
             label="Idea guía")
    footer(sl, block=4)
    notes(sl, """19:25–19:27. Leer el primer test: se construye un generador simulado, se fuerza un umbral imposible y se comprueba que el sistema rechaza sin haber llamado al generador. No hay red ni coste y el resultado es siempre el mismo. Leer el segundo: la evaluación real va marcada con @pytest.mark.llm y además exige una variable de entorno; pyproject.toml la excluye por defecto con addopts. Recorrer las cuatro cosas que pide el enunciado y que se prueban con respuestas simuladas: ingesta sin duplicados, formato, fuentes y errores. Subrayar la regla de la demo: si el proveedor real falla, no se cae al doble para «completar» el lote.
QUÉ ABRIR: tests/test_consulta.py y pyproject.toml.
PREGUNTA: ¿qué demuestra un test con dobles y qué no puede demostrar nunca?
Fuentes: enunciado de S19; tests de la demo; salida real de `uv run pytest` (17/11/2026).""")
    return sl


def s21_agentes(deck):
    sl = deck.slide(tag="agentes")
    header(sl, "Testing de agentes", "En un agente se prueban las decisiones y los límites, no el texto",
           "Un agente elige qué hacer en cada paso. Lo que hay que comprobar es su trayectoria: qué decidió, en "
           "qué orden y cuántas llamadas gastó. Ejemplo: un agente correctivo (CRAG) en LangGraph sobre nuestro RAG.")
    # diagrama CRAG
    box(sl, 43, 128, 520, 196, fill=CARD)
    text(sl, 55, 136, 400, 12, "AMPLIACIÓN OPCIONAL · ampliacion/crag.py · grafo de LangGraph", size=8.5, color=MUTED, bold=True)
    chip(sl, 60, 176, 96, 34, "Recuperar", fill=PINK_BG, color=TITLE, size=10.5, line=PINK, radius=6)
    s = box(sl, 196, 166, 128, 54, fill=VIOLET_BG, line=VIOLET, shape=MSO_SHAPE.DIAMOND)
    shape_text(s, "¿Evidencia?", size=9.5, color=TITLE)
    chip(sl, 372, 176, 96, 34, "Responder", fill=GREEN_BG, color=TITLE, size=10.5, line=MINT, radius=6)
    chip(sl, 212, 262, 96, 34, "Reformular", fill=AMBER_BG, color=TITLE, size=10.5, line=AMBER, radius=6)
    chip(sl, 372, 262, 96, 34, "Rechazar", fill=CORAL_BG, color=TITLE, size=10.5, line=CORAL, radius=6)
    line(sl, 158, 193, 194, 193, color=MUTED)
    line(sl, 326, 193, 370, 193, color=MINT)
    text(sl, 330, 178, 40, 12, "sí", size=9, color=MINT, bold=True, check=False)
    line(sl, 260, 221, 260, 242, color=MUTED, head="none")
    text(sl, 266, 223, 30, 12, "no", size=9, color=MUTED, bold=True, check=False)
    line(sl, 260, 242, 260, 260, color=AMBER)
    text(sl, 136, 244, 118, 12, "quedan intentos", size=8.5, color=AMBER, bold=True, align="r", check=False)
    poly(sl, [(210, 279), (108, 279), (108, 212)], color=AMBER)
    poly(sl, [(260, 242), (420, 242), (420, 260)], color=CORAL)
    text(sl, 300, 228, 130, 12, "se acabaron los intentos", size=8.5, color=CORAL, bold=True, check=False)
    text(sl, 55, 302, 500, 16, "Dos límites: N intentos en la regla y recursion_limit de LangGraph si la regla falla.",
         size=9.5, color=TEXT)
    # tabla de decisiones
    table(sl, 577, 128, 340, [110, 70, 160], [
        ["Mejor similitud", "Intento", "Decisión esperada"],
        ["0,60", "1 de 2", ("responder", {"color": MINT_L, "bold": True})],
        ["0,28 (umbral)", "1 de 2", ("responder", {"color": MINT_L, "bold": True})],
        ["0,10", "1 de 2", ("reformular", {"color": AMBER, "bold": True})],
        ["0,10", "2 de 2", ("rechazar", {"color": CORAL, "bold": True})],
        ["sin resultados", "2 de 2", ("rechazar", {"color": CORAL, "bold": True})],
    ], size=10, row_h=24.5)
    text(sl, 577, 280, 340, 44, "La regla de enrutado es una función pura. Se prueba con una tabla de casos, "
         "sin modelo: tests/test_enrutado.py.", size=9.5, color=MUTED)
    term(sl, 43, 334, 520, 132, [
        ("def test_sin_evidencia_reformula_y_rechaza_sin_generar(sistema):", MINT_L),
        "    t = crag(config(umbral_evidencia=0.99), almacen, proveedores,",
        "             indice_id, \"¿Cuál es el horario de la cafetería?\",",
        "             max_intentos=3)",
        ("    assert t.decisiones == [\"reformular\", \"reformular\", \"rechazar\"]", AMBER),
        ("    assert t.llamadas_recuperacion == 3   # límite respetado: ni una más", AMBER),
        "    assert generador.llamadas == 0 and t.respuesta is None",
    ], title="tests/test_enrutado.py", size=8.5)
    box(sl, 577, 334, 340, 132, fill=VIOLET_BG)
    text(sl, 589, 342, 320, 12, "QUÉ SE COMPRUEBA EN UN AGENTE", size=8.5, color=VIOLET, bold=True)
    bullets(sl, 589, 360, 320, 104, [
        [("Decisiones: ", {"bold": True, "color": TITLE}), ("la ruta elegida ante cada situación.", {})],
        [("Herramientas: ", {"bold": True, "color": TITLE}), ("cuál llama y con qué argumentos.", {})],
        [("Límites: ", {"bold": True, "color": TITLE}), ("máximo de pasos, de llamadas y de coste.", {})],
        [("Parada: ", {"bold": True, "color": TITLE}), ("termina siempre; nunca un bucle sin fin.", {})],
    ], size=9.5, mark_color=VIOLET, space=3)
    takeaway(sl, "Un agente se prueba por su trayectoria: decisiones, argumentos y número de llamadas. Estos tests no sustituyen a los del RAG.",
             label="Idea guía")
    footer(sl, block=4)
    notes(sl, """19:27–19:29. El temario habla de «testing automatizado de agentes y pipelines RAG». Para un agente, el texto final importa menos que la trayectoria: qué decidió en cada paso, qué herramienta llamó, con qué argumentos y cuántas llamadas gastó. El enunciado lo propone como ampliación opcional: tests de enrutado de un agente o CRAG para comprobar decisiones y límites de llamadas, sin sustituir los tests del RAG. Explicar el diagrama: recuperar; si hay evidencia, responder; si no y quedan intentos, reformular y volver a recuperar; si no quedan, rechazar. La regla de enrutado es una función pura y se prueba con la tabla de la derecha. El test del panel comprueba la trayectoria completa y que el límite se respeta. El agente es un grafo de LangGraph (como el de S5): nodos recuperar, reformular, responder y rechazar, con una arista condicional. Tiene dos límites: el de la regla (N intentos) y recursion_limit del framework, que corta el grafo si una regla mal escrita no deja de reformular; hay un test que lo demuestra. La propia consulta del RAG también es un grafo (rag/grafo.py) y tests/test_grafo.py comprueba su trayectoria: el rechazo previo nunca pasa por generar. Si vamos con retraso, esta diapositiva queda como lectura.
QUÉ ABRIR: ampliacion/crag.py, tests/test_enrutado.py y, si hay tiempo, python s19.py chat (el panel muestra la rama de cada pregunta).
PREGUNTA: ¿qué test detectaría un agente que entra en un bucle de reformulaciones?
Fuentes: enunciado de S19 («Ampliación opcional»); código y tests de la demo (grafo LangGraph desde el 22/11/2026).""")
    return sl


def s22_umbrales(deck):
    sl = deck.slide(tag="umbrales")
    header(sl, "Control de regresión", "Umbrales elegidos con validación, con margen y congelados",
           "Una regresión es un cambio que empeora algo que ya funcionaba. El control compara cada ejecución con "
           "unos mínimos fijados de antemano y devuelve un código de salida.")
    reglas = [("1", "Salen de validación", "Valor medido en validación; nunca del test. El test no se usa para poner el listón.", MINT),
              ("2", "Llevan margen", "Umbral = validación ± 0,10. Absorbe la variación normal del juez y de 8 preguntas.", AMBER),
              ("3", "Se congelan", "Se guardan con fecha, perfil y modelos. No se reajustan después de ver el test.", VIOLET),
              ("4", "Sin dato, falla", "Métrica ausente, NaN, caso que falta o error del sistema: el control no aprueba.", CORAL)]
    for i, (n, t, d, col) in enumerate(reglas):
        y = 128 + i * 84
        box(sl, 43, y, 300, 78, fill=CARD)
        box(sl, 43, y, 3.5, 78, fill=col, radius=0)
        badge(sl, 56, y + 10, n, fill=col, d=18, size=9.5)
        text(sl, 82, y + 10, 250, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, 56, y + 34, 278, 42, d, size=9.5, color=TEXT)
    # gráfico de umbrales
    box(sl, 357, 128, 560, 338, fill=CARD)
    tag(sl, 369, 137, "salida")
    text(sl, 369, 158, 536, 14, "datos/umbrales.doble.json · valor en validación (barra) y umbral (marca blanca)", size=9.5, color=MUTED)
    filas = [("recall@5", 1.00, 0.90, "mín.", MINT), ("precision@5", 0.24, 0.13, "mín.", MINT),
             ("rechazos correctos", 0.67, 0.56, "mín.", VIOLET), ("abstenciones incorrectas", 0.00, 0.10, "máx.", CORAL),
             ("aciertos por criterio", 0.60, 0.50, "mín.", BLUE), ("faithfulness · media", 1.00, 0.90, "mín.", AMBER),
             ("faithfulness · cobertura", 1.00, 0.90, "mín.", AMBER), ("answer_relevancy · media", 0.41, 0.31, "mín.", AMBER),
             ("answer_relevancy · cobertura", 1.00, 0.90, "mín.", AMBER)]
    y = 182
    for nombre, val, umb, sentido, col in filas:
        text(sl, 369, y, 160, 14, nombre, size=9.5, color=TITLE, check=False)
        bar(sl, 536, y + 2, 240, 10, val, color=col, mark=umb, mark_color=TITLE)
        text(sl, 784, y - 1, 44, 14, f"{val:.2f}".replace(".", ","), size=10, color=col, bold=True, font=MONO, check=False)
        text(sl, 830, y - 1, 80, 14, f"{sentido} {umb:.2f}".replace(".", ",", 1) if False else f"{sentido} {umb:.2f}".replace("0.", "0,"), size=9.5, color=TITLE, font=MONO, check=False)
        y += 27.5
    text(sl, 369, 436, 536, 26, "Las reglas de un perfil no valen para otro: los umbrales del doble no se aplican a un modelo real.",
         size=9.5, color=MUTED)
    takeaway(sl, "El umbral se decide antes y con margen. Después solo se pregunta: ¿esta ejecución lo cumple, sí o no?",
             label="Idea guía")
    footer(sl, block=4)
    notes(sl, """19:29–19:31. Definir regresión y el control. Cuatro reglas: los umbrales salen de validación; llevan margen (0,10 en la demo) para absorber la variación normal; se congelan con fecha, perfil y modelos; y un dato que falta no aprueba. El gráfico muestra las nueve reglas reales del perfil doble: la barra es el valor medido en validación y la marca ámbar, el umbral. Ocho son mínimos; «abstenciones incorrectas» es un máximo. Avisar de una limitación que la demo deja a la vista: con solo 8 preguntas de validación, el test A del perfil doble no cumple tres de estas reglas. No se retocan: es la prueba de que una validación pequeña generaliza mal, y la razón por la que el control se pasa sobre validación en cada cambio y el test se reserva.
QUÉ ABRIR: datos/umbrales.doble.json y evaluacion/regresion.py.
PREGUNTA: ¿por qué un «sin dato» tiene que contar como fallo?
Fuentes: enunciado de S19 («Define umbrales con margen usando validación»); datos/umbrales.doble.json (17/11/2026).""")
    return sl


def s23_vivo4(deck):
    sl = deck.slide(tag="vivo4")
    header_s(sl, "En vivo 4 · Tests y regresión", "Un control que nunca has visto fallar no demuestra nada",
             "Pasamos el control a una ejecución buena y a una copia estropeada a propósito.")
    code_panel_s(sl, 48, 153.8, 852.8, 96, [
        "uv run pytest",
        "python s19.py umbrales resultados/mi-val-A",
        "python s19.py regresion resultados/mi-val-A ; echo $?",
        "python s19.py degradar resultados/mi-val-A --modo recuperacion --salida resultados/mal",
        "python s19.py informe resultados/mal ; python s19.py regresion resultados/mal ; echo $?",
    ], size=11.5)
    term(sl, 48, 260, 420, 150, [
        ("CONTROL DE REGRESIÓN: PASA", MINT),
        "validacion-A cumple las reglas de",
        "umbrales.doble.json",
        "",
        ("código de salida: 0", MINT_L),
    ], title="EJECUCIÓN DE REFERENCIA", size=10.5)
    term(sl, 480, 260, 420.8, 150, [
        ("CONTROL DE REGRESIÓN: FALLA", CORAL),
        "  ✗ recuperacion.recall_at_5: 0.10 < mínimo 0.90",
        "  ✗ recuperacion.precision_at_5: 0.04 < mínimo 0.13",
        "  ✗ correccion.tasa_aciertos: 0.00 < mínimo 0.50",
        "",
        ("código de salida: 1", CORAL),
    ], title="COPIA DEGRADADA · el buscador pierde su mejor documento", size=9.5)
    tag(sl, 48, 420, "salida")
    text(sl, 290, 421, 610, 26, "Otros modos: sin-rechazo, juez-caido (cae la cobertura, la media sigue en 1,00) e incompleto "
         "(el informe se niega a resumir un conjunto al que le faltan casos).", size=9.5, color=MUTED)
    band_s(sl, "El código de salida 1 es lo que detiene un despliegue en CI: el control es un comando, no una opinión.")
    footer_s(sl)
    notes(sl, """19:31–19:38. EN VIVO 4, la demostración central. 1) uv run pytest: 131 pasan y 3 quedan excluidos (2 db y 1 llm); enseñar addopts en pyproject.toml. 2) umbrales sobre la validación A: calcula las nueve reglas (validación ± 0,10) y las compara con las fijadas en datos/umbrales.doble.json; no escribe sin --fijar, porque las reglas se congelan antes de mirar el test. 3) regresion sobre esa misma ejecución: PASA; enseñar el código de salida 0. 4) degradar con el modo recuperacion: copia la ejecución quitando el primer documento recuperado de cada pregunta y rotula el resultado como degradado a propósito. 5) informe y regresion sobre la copia: FALLA con tres reglas y código de salida 1. Si hay tiempo, modo juez-caido: la media de fidelidad sigue en 1,00 y lo que cae es la cobertura. Comentar que con la configuración B el control también falla en validación: detecta una regresión real, no fabricada.
QUÉ ABRIR: terminal; evaluacion/degradar.py; evaluacion/regresion.py.
PREGUNTA: ¿qué pasaría si el control tratara un «sin dato» como aprobado?
Fuentes: salida real de los comandos (resultados/ejemplo-doble, perfil doble, 17/11/2026); enunciado de S19 («demuestra, con resultados degradados de prueba, que el control de regresiones falla cuando debe»).""")
    return sl


SLIDES = [s12_faithfulness, s13_relevancy, s14_juez, s15_aislado, s16_no_evaluables, s17_revision, s18_vivo3,
          s19_piramide, s20_dobles, s21_agentes, s22_umbrales, s23_vivo4]
