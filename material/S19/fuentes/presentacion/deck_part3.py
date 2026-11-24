"""S19 · Diapositiva 15 (cierre y práctica opcional) y anexo de consulta (16–20)."""
from deck_lib import *  # noqa: F401,F403

ANEXO = "ANEXO · CONSULTA. Fuera del horario de 18:30–20:00: solo si surge la pregunta o para preparar la clase."


def s15_cierre(deck):
    sl = deck.slide(BG_SECTION, tag="cierre")
    img(sl, "thepower-logo.png", 38, 34, h=30)
    text(sl, 43, 80, 300, 14, "CIERRE", size=10, color=MINT, bold=True)
    text(sl, 43, 98, 520, 44, "Antes de aprobar un cambio, pedimos…", size=28, font=SERIF, color=TITLE)
    pide = [("Misma entrada", "Pregunta, fragmentos y respuesta idénticos: lo comprobamos con cmp y con los ids.",
             "T01 · V02 · T09", MINT),
            ("Una variable cambiada", "El generador o el juez, nada más. Si cambian dos, no sabemos cuál explica la diferencia.",
             "Pruebas 1 y 2", AMBER),
            ("Resultado comprobable", "Dato, cita y fragmentos leídos; veredicto por afirmación; código 0 o 1 por caso.",
             "T12 · T09", CORAL),
            ("Coste visible", "Por llamada y desde OpenRouter, con generar y juzgar en trazas distintas.",
             "Langfuse · V02", BLUE)]
    y = 156
    for i, (t, d, donde, col) in enumerate(pide, 1):
        circle(sl, 43, y + 2, 26, col)
        text(sl, 43, y + 6, 26, 18, str(i), size=12, color=DARK, bold=True, align="c", check=False)
        text(sl, 80, y, 300, 18, t, size=14, color=TITLE, bold=True)
        text(sl, 400, y + 2, 160, 14, donde, size=9, color=col, bold=True, align="r", check=False)
        text(sl, 80, y + 20, 480, 34, d, size=11, color=TEXT)
        y += 66
    box(sl, 43, 424, 517, 40, fill="1A463C", radius=6)
    text(sl, 55, 424, 495, 40, [[("Por caso y por lote: ", {"bold": True, "color": MINT_L}),
                                 ("la media del lote no sustituye a comprobar los casos que conocemos.", {})]],
         size=11, color=TITLE, anchor="m")
    # práctica y preguntas
    box(sl, 584, 80, 333, 386, fill="1A463C", radius=8)
    text(sl, 604, 96, 300, 12, "PRÁCTICA OPCIONAL", size=9, color=MINT, bold=True)
    text(sl, 604, 114, 296, 40, "Construir un RAG completo desde cero con evaluación y testing integrados.", size=12,
         font=SERIF, color=TITLE)
    pasos = ["Construir", "Preparar datos", "Medir", "Comprobar", "Comparar", "Automatizar"]
    x, yy = 604, 162
    for p in pasos:
        w = len(p) * 5.8 + 18
        if x + w > 904:
            x, yy = 604, yy + 26
        chip(sl, x, yy, w, 20, p, fill=BG_SECTION, color=MINT_L, size=9, line="2A5246", radius=10)
        x += w + 6
    text(sl, 604, 222, 296, 30, [[("Paso a paso: ", {"bold": True, "color": TITLE}),
                                  ("demo-evaluacion/docs/ejercicio.md", {"font": MONO, "color": MINT_L, "bold": True})]],
         size=10, color=TEXT)
    text(sl, 604, 256, 296, 56, "Gratis con el perfil doble. Con modelos, primero «s19.py estimar»: 566 llamadas como máximo "
         "y el juez es la partida principal. 7–9 h orientativas.", size=10, color=TEXT)
    box(sl, 604, 318, 293, 0.8, fill="2A5246", radius=0)
    text(sl, 604, 328, 296, 40, "¿Preguntas?", size=28, font=SERIF, color=MINT_L)
    text(sl, 604, 374, 296, 12, "PRÓXIMA SESIÓN · S20", size=9, color=MINT, bold=True)
    text(sl, 604, 390, 296, 40, "Proyecto final: agente conversacional. Lo de hoy es su red de seguridad.", size=10.5,
         color=TITLE)
    text(sl, 604, 430, 296, 30, "Anexo: métricas, A/B de fragmentación, histórico Hydrogen–Sol, prompt NO_CONSTA y comandos.",
         size=8.5, color=MUTED)
    notes(sl, """19:50–20:00. Cierre con la pregunta del día: ¿cómo comprobamos qué ha cambiado y si empeoró? Con cuatro evidencias, y cada una salió en una prueba. 1 Misma entrada: cmp sobre respuestas.jsonl y los mismos ids de fragmento (T01, V02, T09). 2 Una variable cambiada: solo el generador o solo el juez. 3 Resultado comprobable: dato y cita frente a lo que el modelo leyó (T12), veredictos por afirmación y un código 0/1 por caso (T09). 4 Coste visible: por llamada, el que devuelve OpenRouter, con el juez en su propia traza de Langfuse (V02). Recordar la diferencia del final: un umbral agregado por lote no sustituye a las comprobaciones por caso.
Práctica OPCIONAL (indicación de la escuela del 04/11/2026): construir desde documentos en bruto, preparar 20 preguntas (14 + 6) y validación aparte con criterios fechados, medir recuperación y generación por separado, revisar a mano, comparar cambiando una variable y automatizar con pytest y un control de regresión. Guía paso a paso en demo-evaluacion/docs/ejercicio.md. Se puede hacer entera con el perfil doble, sin coste. Con modelos, ejecutar antes `python s19.py estimar`: 566 llamadas como máximo; con Hydrogen y juez Opus el README estima 2,91 USD (cota 24,90); con juez Sol, la ejecución local del 22/11/2026 dio 1,56 USD (cota 12,93), 1,34 de ellos del juez.
Turno de preguntas. Anunciar S20: proyecto final.
QUÉ ABRIR: docs/ejercicio.md y la salida de `uv run python s19.py estimar`.
PREGUNTA: ¿qué comprobación por caso añadiríais primero a vuestro proyecto final?
Fuentes: temario de AI Engineer (Gmail, 17/07/2026); enunciado de S19 (ejercicios.docx, 29/09/2026); demo-evaluacion/docs/ejercicio.md; demo-evaluacion/README.md (estimación); salida local de `s19.py estimar` (22/11/2026).""")
    return sl


def s16_metricas(deck):
    sl = deck.slide(tag="anexo-metricas")
    header(sl, "Anexo · consulta", "Las métricas de hoy en una tabla",
           "Qué mide cada una, cómo se calcula y dónde apareció en las pruebas. Ninguna se mezcla en una media con otra.")
    table(sl, 43, 122, 874, [150, 220, 290, 214], [
        ["Métrica", "Qué mide", "Cálculo", "Dónde salió hoy"],
        ["recall@5", "Lo que hacía falta y llegó", "relevantes entre 5 documentos ÷ relevantes de la pregunta", "T12: 2/2 = 1,00"],
        ["precision@5", "Ruido entre lo recuperado", "relevantes entre 5 documentos ÷ 5", "T12: 2/5 = 0,40 · V02: 0,20"],
        ["Rechazos correctos", "Se abstiene cuando no consta", "rechazos ÷ preguntas sin respuesta", "test A real: 6/6"],
        ["Abstenciones incorrectas", "Se abstiene pudiendo responder", "abstenciones ÷ preguntas respondibles", "test A real: 1/14 (T12)"],
        ["Acierto por criterio", "Datos clave + cita relevante", "aciertos ÷ respondibles (fijado antes del test)", "test A real: 13/14"],
        ["Faithfulness", "Afirmaciones respaldadas", "afirmaciones con veredicto 1 ÷ afirmaciones", "T09: 1/1 con Sol · 0/2 con Opus"],
        ["Answer Relevancy", "Contesta a lo preguntado", "similitud entre la pregunta y las que el juez deduce", "V02: 0,9566 · 0,9585"],
        ["Cobertura", "Casos que el juez pudo puntuar", "evaluables ÷ esperados (lo demás, con motivo)", "V02: 1/1 en los dos jueces"],
        ["Coste", "Lo que cuesta cada llamada", "el que devuelve OpenRouter; generar y juzgar aparte", "V02: 0,0015 frente a 0,0106 USD"],
    ], size=10, row_h=32, bold_cols=(0,), colors={0: MINT_L, 3: TITLE})
    takeaway(sl, "Unidad de recuperación: el documento. Unidad de Faithfulness: la afirmación. Unidad de coste: la llamada.",
             label="Para recordar")
    footer(sl, block=6)
    notes(sl, ANEXO + """ Tabla de consulta con las métricas usadas en las tres pruebas. Las de recuperación cuentan documentos distintos entre los cinco primeros (dos fragmentos del mismo documento son un acierto); las preguntas sin respuesta no tienen recall: se miden con rechazos correctos. Abstenciones incorrectas y rechazos correctos van aparte porque tienen denominadores distintos. Faithfulness y Answer Relevancy las calcula Ragas con un juez; si no puede puntuar, la fila queda como no evaluable con su motivo y baja la cobertura, nunca se convierte en 0 ni en 1. El coste es el de cada llamada según OpenRouter.
Hora de referencia si se usa: 19:50–20:00, durante las preguntas.
QUÉ ABRIR: evaluacion/metricas.py; resultados/ejemplo-real/test-A/informe.md.
PREGUNTA: ¿por qué precision@5 no puede pasar de 0,20 cuando solo hay un documento relevante?
Fuentes: evaluacion/metricas.py; resultados/ejemplo-real/test-A/informe.json (6/6, 1/14, 13/14); pruebas 1–3 de este deck.""")
    return sl


def s17_fragmentos(deck):
    sl = deck.slide(tag="anexo-ab")
    header(sl, "Anexo · comparación controlada", "Tamaño de fragmento 320 → 900: una sola variable",
           "Ejemplo de comparación A/B con modelos reales: mismo test de 20, mismos modelos (Hydrogen genera, Opus juzga), "
           "mismo prompt y mismo evaluador. Solo cambia chunk_size.")
    tag(sl, 43, 128, "real")
    table(sl, 43, 148, 560, [230, 100, 100, 130], [
        ["Métrica · test de 20", "A · 320", "B · 900", "B − A"],
        ["Fragmentos del índice", ("41", {"align": "r"}), ("13", {"align": "r"}), ("", {})],
        ["recall@5", ("1,00", {"align": "r"}), ("0,96", {"align": "r"}), ("−0,04", {"align": "r", "color": CORAL})],
        ["Rechazos correctos", ("6/6", {"align": "r"}), ("6/6", {"align": "r"}), ("=", {"align": "r"})],
        ["Abstenciones incorrectas", ("1/14", {"align": "r"}), ("3/14", {"align": "r"}), ("+2  empeora", {"align": "r", "color": CORAL, "bold": True})],
        ["Aciertos por criterio", ("13/14", {"align": "r"}), ("11/14", {"align": "r"}), ("−2  empeora", {"align": "r", "color": CORAL, "bold": True})],
        ["faithfulness (media)", ("0,92", {"align": "r"}), ("0,98", {"align": "r"}), ("+0,05", {"align": "r"})],
        ["Latencia p95", ("3,77 s", {"align": "r"}), ("2,76 s", {"align": "r"}), ("−1,01 s", {"align": "r", "color": MINT_L})],
        ["Coste por consulta", ("0,002045", {"align": "r"}), ("0,002268", {"align": "r"}), ("+0,0002 USD", {"align": "r"})],
        ["Coste del evaluador", ("0,46 USD", {"align": "r"}), ("0,43 USD", {"align": "r"}), ("", {})],
    ], size=10, row_h=28, bold_cols=(0,), colors={0: MINT_L})
    box(sl, 617, 128, 300, 160, fill=ST_FALLO_BG)
    label(sl, 629, 137, 280, "Casos que cambian", color=ST_FALLO, size=8.5)
    text(sl, 629, 155, 278, 128, [
        {"runs": [("T08 ", {"bold": True, "color": TITLE}),
                  ("(plazo del crédito): con fragmentos de 900 la similitud baja de 0,62 a 0,46, no llega al umbral y se "
                   "rechaza sin llamar al modelo.", {})], "space": 6},
        {"runs": [("T14 ", {"bold": True, "color": TITLE}), ("pasa de acierto a fallo por criterio.", {})]},
    ], size=10.5, color=TEXT, space=6)
    box(sl, 617, 298, 300, 166, fill=CARD)
    label(sl, 629, 307, 280, "Cómo se lee", color=MINT, size=8.5)
    text(sl, 629, 325, 278, 136, "B pierde aciertos porque el umbral se calibró con el índice A: con fragmentos más largos "
         "las similitudes bajan. La fidelidad media sube y no lo detecta. Con 20 preguntas, 2 casos pueden ser ruido.",
         size=10.5, color=TEXT)
    takeaway(sl, "El comando comparar se niega si cambian dos variables o el evaluador: la comparación vale si solo cambia una.",
             label="Para recordar")
    footer(sl, block=6)
    notes(sl, ANEXO + """ Ejemplo de comparación controlada con el cambio de tamaño de fragmento, que antes abría la clase. Ejecutado con modelos reales el 22/11/2026: A (chunk_size 320, 41 fragmentos) frente a B (900, 13 fragmentos), mismo test de 20, Hydrogen como generador y Opus como juez. Recall@5 1,00 → 0,96; abstenciones incorrectas 1/14 → 3/14; aciertos 13/14 → 11/14; faithfulness media 0,92 → 0,98; p95 3,77 s → 2,76 s; coste por consulta 0,002045 → 0,002268 USD. Cambian T08 y T14. La causa principal: el umbral de evidencia (0,5223) se calibró con el índice A; con fragmentos de 900 las similitudes bajan y T08 cae en rechazo previo (0,62 → 0,46, según el guion del directo, caso 7).
Hora de referencia si se usa: 19:50–20:00, durante las preguntas.
QUÉ ABRIR: resultados/ejemplo-real/comparacion/comparacion.md; datos/configuraciones.json.
PREGUNTA: ¿qué habría que recalibrar antes de dar por mala la variante B?
Fuentes: resultados/ejemplo-real/comparacion/comparacion.md y test-A/test-B/informe.json (perfil real, 22/11/2026); guion-directo-modelos.md (caso `7` · T08 con fragmentos de 900).""")
    return sl


def s18_historico(deck):
    sl = deck.slide(tag="anexo-historico")
    header(sl, "Anexo · comparación histórica", "Hydrogen frente a Sol como generadores, por lotes",
           "Evaluación de modelos con método: solo cambia gen_modelo; mismo índice, prompt v1, test de 20 y el mismo juez "
           "(Claude Opus 5.5, que no es ninguno de los candidatos). Cifras guardadas, sin cambios.")
    tag(sl, 43, 136, "real")
    table(sl, 43, 156, 520, [220, 150, 150], [
        ["Métrica · test de 20", "Hydrogen (MH)", "Sol (MS)"],
        ["Aciertos por criterio", "13/14 (falla T12)", "12/14 (T12, T14)"],
        ["Abstenciones incorrectas", "1/14", "0/14"],
        ["faithfulness · answer_relevancy", "0,92 · 0,86", "1,00 · 0,88"],
        ["Latencia p50 / p95", "2,54 s / 3,65 s", "1,61 s / 1,88 s"],
        ["Coste por 1.000 consultas", "2,13 USD", "1,00 USD"],
    ], size=10.5, row_h=32, bold_cols=(0,), colors={0: MINT_L, 1: TITLE, 2: TITLE})
    term(sl, 43, 362, 520, 100, [
        ("$ for m in MH MS; do", MINT_L),
        ("    uv run python s19.py lote --env .env.sol-opus --conjunto test \\", MINT_L),
        ("        --config $m --salida resultados/real-test-$m --execute", MINT_L),
        ("    (cd evaluador && uv run python evaluar.py … --modo real --execute)", MINT_L),
        ("  done; uv run python s19.py comparar resultados/real-test-MH resultados/real-test-MS", MINT_L),
    ], title="COMANDOS (docs/comandos.md · «Evaluación de modelos»)", size=8.5, pitch=12)
    box(sl, 577, 136, 340, 326, fill=CARD)
    label(sl, 589, 146, 316, "Cómo se lee", color=MINT, size=8.5)
    text(sl, 589, 164, 318, 290, [
        {"runs": [("Ninguno gana en todo. ", {"bold": True, "color": TITLE}),
                  ("Hydrogen acierta uno más por criterio; Sol es más rápido y cuesta la mitad por consulta.", {})], "space": 7},
        {"runs": [("T14 es un falso fallo del criterio: ", {"bold": True, "color": TITLE}),
                  ("Sol escribió «800 ms» y el criterio literal pedía «800 milisegundos». Se anota; no se cambia la regla "
                   "después de ver el test.", {})], "space": 7},
        {"runs": [("T12 varía entre pasadas, ", {"bold": True, "color": TITLE}),
                  ("como vimos en la prueba 1.", {})], "space": 7},
        {"runs": [("20 preguntas son evidencia de laboratorio, ", {"bold": True, "color": TITLE}),
                  ("no una prueba estadística. La decisión depende de qué se priorice.", {})]},
    ], size=10.5, color=TEXT, space=7)
    takeaway(sl, "Archivos en resultados/ejemplo-real/modelos/: es la referencia histórica y no se modifica.",
             label="Para recordar")
    footer(sl, block=6)
    notes(sl, ANEXO + """ Comparación histórica por lotes entre Gemini 4 Hydrogen y GPT‑6.2 Sol como generadores, ejecutada el 22/11/2026 con .env.sol-opus: mismo índice A, prompt v1, sin temperatura, razonamiento bajo y el mismo juez (Claude Opus 5.5), así que `comparar` la acepta porque solo cambia gen_modelo. Hydrogen 13/14 aciertos (falla T12) y Sol 12/14 (T12 y T14); abstenciones incorrectas 1/14 y 0/14; faithfulness 0,92 y 1,00; answer_relevancy 0,86 y 0,88; p50/p95 2,54/3,65 s frente a 1,61/1,88 s; 2,13 frente a 1,00 USD por 1.000 consultas. Estas cifras, los comandos y los archivos guardados se conservan intactos; Terra es el segundo generador del chat actual, no forma parte de esta comparación.
Hora de referencia si se usa: 19:50–20:00, durante las preguntas.
QUÉ ABRIR: resultados/ejemplo-real/modelos/comparacion/comparacion.md; respuestas de test-MH y test-MS.
PREGUNTA: con estas cifras, ¿qué generador elegiríais para un servicio con mucho tráfico?
Fuentes: resultados/ejemplo-real/modelos/comparacion/comparacion.md; guion-directo-modelos.md («Parte 3 · Evaluación de modelos»); docs/comandos.md («Evaluación de modelos»).""")
    return sl


def s19_prompt(deck):
    sl = deck.slide(tag="anexo-prompt")
    header(sl, "Anexo · respaldo de laboratorio", "Un prompt que responde siempre NO_CONSTA",
           "Regresión provocada a propósito para ver fallar el control por umbrales del lote. Misma validación A; solo cambia "
           "prompt_version. Ragas no hace ninguna llamada: no hay respuestas que juzgar.")
    tag(sl, 43, 136, "real")
    table(sl, 43, 156, 470, [200, 135, 135], [
        ["Validación A · 5 respondibles", "v1 (referencia)", "regresion-rechazo"],
        ["recall@5", "1,00", "1,00"],
        ["Abstenciones incorrectas", "0/5", ("5/5", {"color": CORAL, "bold": True})],
        ["Aciertos por criterio", "4/5", ("0/5", {"color": CORAL, "bold": True})],
        ["Llamadas al juez", "sí, a las respondidas", "0 (nada que juzgar)"],
        ["Control de regresión", ("PASA (0)", {"color": MINT_L, "bold": True}), ("FALLA (1)", {"color": CORAL, "bold": True})],
    ], size=10.5, row_h=32, bold_cols=(0,), colors={0: MINT_L, 1: TITLE, 2: TITLE})
    term(sl, 527, 136, 390, 200, [
        ("$ uv run python s19.py regresion resultados/ejemplo-real/validacion-A", MINT_L),
        ("CONTROL DE REGRESIÓN: PASA · validacion-A-real-…", MINT_L),
        "",
        ("$ uv run python s19.py regresion \\", MINT_L),
        ("    resultados/ensayo-tres-pruebas-20261122/regresion-rechazo", MINT_L),
        ("CONTROL DE REGRESIÓN: FALLA · ensayo-s19-regresion-rechazo", CORAL),
        ("  ✗ rechazo.tasa_abstenciones_incorrectas: 1.00 > máximo 0.10", CORAL),
        ("  ✗ correccion.tasa_aciertos: 0.00 < mínimo 0.70", CORAL),
        ("  ✗ generacion.faithfulness.media: sin dato …", CORAL),
        ("  (y 3 reglas más de Ragas: sin dato)", MUTED),
    ], title="SALIDA REAL · ejecutada en local, sin coste", size=8.5, pitch=12.5)
    box(sl, 43, 362, 874, 100, fill=CARD)
    label(sl, 55, 371, 850, "Por qué es solo un respaldo", color=MINT, size=8.5)
    text(sl, 55, 389, 850, 70, [
        {"runs": [("Es un fallo evidente y agregado: ", {"bold": True, "color": TITLE}),
                  ("cualquier umbral del lote lo detecta. La regresión de T09 es más sutil: la media pasa y solo una "
                   "comprobación por caso la ve.", {})], "space": 5},
        {"runs": [("Los umbrales salen de validación con margen (umbrales.real.json, 22/11/2026) ", {"bold": True, "color": TITLE}),
                  ("y nunca se ajustan mirando el test. «Sin dato» no se da por bueno.", {})]},
    ], size=10.5, color=TEXT, space=5)
    takeaway(sl, "Un control que nunca habéis visto fallar no demuestra nada: provocad el fallo una vez.", label="Para recordar")
    footer(sl, block=6)
    notes(sl, ANEXO + """ El prompt `regresion-rechazo` ordena responder siempre NO_CONSTA. Queda como respaldo de laboratorio: la regresión principal del directo es la de T09 al sustituir el juez. Ensayo del 22/11/2026 sobre la misma validación A, con la configuración idéntica salvo prompt_version: recall@5 1,00 en v1, v2 y regresion-rechazo; abstenciones incorrectas 0/5 → 5/5; aciertos 4/5 → 0/5; Ragas hizo cero llamadas. El control `s19.py regresion` con datos/umbrales.real.json devuelve PASA (0) para la referencia y FALLA (1) para el prompt defectuoso; la salida de la diapositiva se volvió a ejecutar en local, sin coste, el 22/11/2026. Las reglas de Ragas sin dato también fallan: lo que no se ha medido no se da por bueno.
Contraste con la prueba 3: aquí el fallo es masivo y lo ve la media; en T09 el lote pasa (0,92 ≥ 0,90) y solo una comprobación por caso lo detecta.
Hora de referencia si se usa: 19:50–20:00, durante las preguntas.
QUÉ ABRIR: datos/umbrales.real.json; resultados/ensayo-tres-pruebas-20261122/regresion-rechazo/informe.md.
PREGUNTA: ¿qué regla del control habría saltado si el prompt solo fallara en una de cinco preguntas?
Fuentes: verificacion.md («Ensayo de las tres pruebas del directo · 22/11/2026»); resultados/ensayo-tres-pruebas-20261122/regresion-rechazo y resultados/ejemplo-real/validacion-A (informe.json); salida local de `s19.py regresion` (22/11/2026).""")
    return sl


def s20_comandos(deck):
    sl = deck.slide(tag="anexo-comandos")
    header(sl, "Anexo · comandos", "Las tres pruebas, paso a paso",
           "Desde demo-evaluacion/ con Docker arrancado. Los comandos con --execute consumen OpenRouter; el resto lee archivos guardados.")
    bloques = [
        ("Prueba 1 · Generador (T01, T12)", ST_GEN, [
            ("$ S19_PROMPT_VERSION=v1 S19_GEN_TEMPERATURE='' \\", MINT_L),
            ("    uv run python s19.py chat --env .env.hydrogen-sol --config A --execute", MINT_L),
            "  T01: › 1  › /perfil terra-opus  › 1    T12: › /perfil hydrogen-sol  › 3  › /perfil terra-opus  › 3",
            ("  Langfuse → Sessions → chat-… → recuperacion / generacion", MUTED)]),
        ("Prueba 2 · Juez (V02 congelada)", ST_JUEZ, [
            ("$ s19_ensayo=resultados/ensayo-tres-pruebas-20261122", MINT_L),
            ('$ cmp "$s19_ensayo/juez-sol/respuestas.jsonl" "$s19_ensayo/juez-opus/respuestas.jsonl"', MINT_L),
            ('$ cat "$s19_ensayo"/juez-{sol,opus}/puntuaciones.jsonl', MINT_L),
            ("  repetir con gasto: S19_EVAL_LLM_MODEL=<juez> evaluar.py … --modo real --execute", MUTED)]),
        ("Prueba 3 · Regresión (T09)", ST_FALLO, [
            ("$ s19_ensayo=resultados/ensayo-regresion-modelo-20261122", MINT_L),
            ('$ cmp "$s19_ensayo/juez-sol-T09/respuestas.jsonl" "$s19_ensayo/juez-opus-T09/respuestas.jsonl"', MINT_L),
            ("$ for s19_juez in sol opus; do python3 - …/detalle-faithfulness.json <<'PY' … PY; done", MINT_L),
            ("  T09 con Sol → PASA (0) · con Opus → FALLA (1)", MUTED)]),
    ]
    y = 124
    for t, col, lineas in bloques:
        box(sl, 43, y, 6, 104, fill=col, radius=0)
        text(sl, 58, y, 400, 14, t, size=10.5, color=col, bold=True)
        term(sl, 58, y + 18, 859, 84, lineas, size=10, pitch=14.5)
        y += 114
    takeaway(sl, "Guion completo, checklist de ensayo y script de T09 en guion-directo-modelos.md (material del profesor).",
             label="Para recordar")
    footer(sl, block=6)
    notes(sl, ANEXO + """ Resumen de comandos para seguir las pruebas paso a paso. Prueba 1: el chat con el perfil hydrogen-sol, `1` (T01), `/perfil terra-opus` y `1`; para T12 en la misma sesión, volver antes con `/perfil hydrogen-sol` y repetir con `3`; consume OpenRouter (los dos turnos del ensayo costaron 0,00312 USD). Prueba 2: `cmp` y `cat` sobre las dos copias de V02, sin coste; para repetir el ensayo con gasto, extraer V02 de resultados/ejemplo-real/validacion-A/respuestas.jsonl y ejecutar evaluar.py con S19_EVAL_LLM_MODEL=openai/gpt-6.2-sol y luego anthropic/claude-opus-5.5 (comandos completos en el guion). Prueba 3: `cmp` y el bucle que lee detalle-faithfulness.json de cada juez y sale con 0 si la fidelidad es 1,00 y con 1 si no. Mantener los archivos .env fuera de la pantalla compartida.
Hora de referencia si se usa: 18:15 (preparación) o 19:50–20:00, durante las preguntas.
QUÉ ABRIR: guion-directo-modelos.md (checklist de ensayo y las tres pruebas); docs/comandos.md.
PREGUNTA: ¿qué comando ejecutaríais en CI para impedir que se repita lo de T09?
Fuentes: guion-directo-modelos.md (Pruebas 1–3); demo-evaluacion/docs/comandos.md; verificacion.md (gasto del chat T12).""")
    return sl


SLIDES = [s15_cierre, s16_metricas, s17_fragmentos, s18_historico, s19_prompt, s20_comandos]
