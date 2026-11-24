"""S19 · Diapositivas 7–14: tres pruebas reales, cada una con su diapositiva de pregunta y de resultado.

Todas las cifras proceden de archivos guardados (ver las notas de cada diapositiva). No se ha
vuelto a llamar a ningún modelo para preparar el deck.
"""
from deck_lib import *  # noqa: F401,F403

ENSAYO3 = "demo-evaluacion/resultados/ensayo-tres-pruebas-20261122/"
REGRE = "demo-evaluacion/resultados/ensayo-regresion-modelo-20261122/"


# ---------------------------------------------------------------- piezas comunes
def _cambio(sl, x, y, w, h, de, a, fijo, accent, titulo="Lo que cambiamos"):
    stage_card(sl, x, y, w, h, accent, lab=titulo)
    chip(sl, x + 12, y + 32, w - 24, 26, de, fill=CARD2, color=TITLE, size=11, line=BORDER, radius=4)
    text(sl, x, y + 60, w, 16, "↓", size=13, color=accent, bold=True, align="c", check=False)
    chip(sl, x + 12, y + 78, w - 24, 26, a, fill=CARD2, color=accent, size=11, line=accent, radius=4)
    label(sl, x + 12, y + 116, w - 24, "Se mantiene igual", color=MUTED, size=8.5)
    bullets(sl, x + 12, y + 132, w - 24, h - 140, fijo, size=10, color=TEXT, mark="=", mark_color=MUTED, space=2)


def _mirar(sl, x, y, w, h, items, accent=ST_OBS, titulo="Qué vamos a mirar"):
    stage_card(sl, x, y, w, h, accent, lab=titulo)
    yy = y + 34
    for i, t in enumerate(items, 1):
        badge(sl, x + 12, yy + 1, i, fill=accent, color=DARK, d=17, size=9)
        text(sl, x + 36, yy, w - 48, 34, t, size=10.5, color=TITLE)
        yy += (h - 44) / len(items)


def _vivo(sl, y, lineas, aviso):
    term(sl, 43, y, 874, 56, lineas, size=9.5, pitch=13)
    chip(sl, 735, y + 6, 172, 15, aviso, fill=AMBER, color=DARK, size=7.5, radius=3)


def _porque(sl, x, y, w, h, body, titulo="Por qué ocurrió", accent=MINT, size=10.5):
    box(sl, x, y, w, h, fill=CARD)
    box(sl, x, y, 3.5, h, fill=accent, radius=0)
    label(sl, x + 12, y + 9, w - 24, titulo, color=accent, size=8.5)
    if isinstance(body, list):
        body = [{"runs": p, "space": 6} for p in body]
    text(sl, x + 12, y + 26, w - 22, h - 32, body, size=size, color=TEXT, space=6)


def _cost_bars(sl, x, y, w, filas, maximo, color_lab=TITLE, alto=14, paso=30, fmt=None, lab_w=120, val_w=112):
    for nombre, valor, col in filas:
        text(sl, x, y - 1, lab_w, 14, nombre, size=10.5, color=color_lab, bold=True)
        bar(sl, x + lab_w + 4, y, w - lab_w - val_w - 12, alto, valor / maximo, color=col)
        text(sl, x + w - val_w, y - 1, val_w, 14, fmt(valor) if fmt else f"{valor:.6f} USD".replace(".", ","),
             size=10.5, color=TITLE, bold=True, align="r", font=MONO)
        y += paso


# ---------------------------------------------------------------- prueba 1 · T01
def s07_t01_prueba(deck):
    sl = deck.slide(tag="t01-prueba")
    header(sl, "Prueba 1 · Cambiar el generador · T01", "¿Qué dato y qué cita debería dar el sistema?")
    quote(sl, 43, 96, 874, 64, "¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?", size=19,
          label_t="Pregunta T01 · datos/test.jsonl", accent=ST_GEN)
    _cambio(sl, 43, 172, 280, 226, "Gemini 4 Hydrogen", "GPT‑6.1 Terra",
            ["Índice A y umbral 0,5223", "Prompt v1", "Los mismos 12 fragmentos, en el mismo orden"], ST_GEN,
            titulo="Lo que cambiamos · el generador")
    _mirar(sl, 335, 172, 280, 226, ["El dato que da cada modelo",
                                    "La cita entre corchetes: ¿qué documento?",
                                    "Los fragmentos que recibió (recuperacion)",
                                    "Tokens y coste de cada llamada (generacion)"])
    prediccion(sl, 627, 172, 290, 226, ["¿Qué dato tiene que aparecer?", "¿Qué documento debe citar?",
                                        "¿Cuál de los dos costará más?"], ["dato:", "cita: ["])
    _vivo(sl, 410, [("$ S19_PROMPT_VERSION=v1 S19_GEN_TEMPERATURE='' uv run python s19.py chat \\", MINT_L),
                    ("      --env .env.hydrogen-sol --config A --execute", MINT_L),
                    "  › 1          › /perfil terra-opus          › 1          (Esc para salir)"],
          "EN VIVO · consume OpenRouter")
    takeaway(sl, "Cambiamos una sola pieza, el modelo que redacta. Si la entrada es la misma, la diferencia es suya.",
             label="Idea guía")
    footer(sl, block=2)
    notes(sl, """18:52–18:56. PRUEBA 1, primera parte. Leer la pregunta T01 y pedir la predicción antes de ejecutar: qué dato debe aparecer, qué documento debe citar y cuál de los dos modelos costará más. Dejar 30 segundos para que lo anoten en el chat de la clase.
Explicar qué cambia y qué no: solo el modelo generador (Gemini 4 Hydrogen → GPT‑6.1 Terra). Se mantienen el índice A, el umbral 0,5223, el prompt v1 y, por tanto, los mismos 12 fragmentos en el mismo orden. Así cualquier diferencia en la respuesta viene del modelo.
EN VIVO: lanzar el chat con el comando de la diapositiva (temperatura sin fijar en ambos porque Terra no la admite), escribir `1`, después `/perfil terra-opus` y `1` otra vez. En el panel del chat, señalar la ruta recuperar → generar → comprobar. Si se prefiere no gastar o va justo de tiempo, proyectar el ensayo guardado (siguiente diapositiva). Coste previsto: décimas de céntimo.
QUÉ ABRIR: datos/test.jsonl (T01: documentos_relevantes y datos_clave); el chat en Terminal con letra grande.
PREGUNTA: ¿qué dato y qué cita exigiríais para dar la respuesta por buena?
Fuentes: guion-directo-modelos.md («Prueba 1 · Cambiar el generador en el chat» y caso `1` · T01); datos/test.jsonl.""")
    return sl


def s08_t01_resultado(deck):
    sl = deck.slide(tag="t01-resultado")
    header(sl, "Resultado · T01", "Los dos dan TLS 1.3 y citan la misma fuente; cambia el coste")
    tag(sl, 43, 90, "ensayo")
    text(sl, 200, 90, 700, 14, "Mismo perfil base, índice A y v1; solo cambió S19_GEN_MODEL · 4 llamadas guardadas en "
         "ensayo-tres-pruebas-20261122", size=8.5, color=MUTED, check=False)
    frag(sl, 43, 110, 874, 50, "01-arquitectura-aethercloud#03",
         [("El tráfico entrante atraviesa pasarelas perimetrales Anycast con terminación ", {}),
          hl("TLS 1.3 obligatoria"), (". Ningún servicio de aplicación expone puertos…", {})],
         sub="1.er fragmento del prompt · similitud 0,78", size=11)
    answer(sl, 43, 172, 430, 112, "Gemini 4 Hydrogen",
           [("Las pasarelas perimetrales de AetherCloud exigen la versión ", {}), hl("TLS 1.3"), (" ", {}),
            hl("[01-arquitectura-aethercloud]", ST_GEN), (".", {})],
           "404 → 126 tokens · 2,06 s · 0,001551 USD", estado="✓ dato y cita", size=13)
    answer(sl, 487, 172, 430, 112, "GPT‑6.1 Terra",
           [("Las pasarelas perimetrales exigen ", {}), hl("TLS 1.3"), (". ", {}),
            hl("[01-arquitectura-aethercloud]", ST_GEN)],
           "366 → 30 tokens · 1,31 s · 0,000516 USD", estado="✓ dato y cita", size=13)
    # coste
    box(sl, 43, 296, 430, 168, fill=CARD)
    label(sl, 55, 305, 400, "Coste de generar · dos llamadas medidas", color=ST_GEN, size=8.5)
    _cost_bars(sl, 55, 330, 406, [("Hydrogen", 0.001551, ST_GEN), ("Terra", 0.000516, ST_GEN)], 0.001551, paso=30)
    text(sl, 55, 392, 406, 66, "Terra costó un tercio en esta llamada y escribió una frase más corta (30 tokens de salida). "
         "Es lo que midió OpenRouter para cada respuesta, no una tarifa ni una media.", size=10.5, color=TEXT)
    _porque(sl, 487, 296, 430, 168, [
        [("El dato está en un único fragmento y llega el primero al prompt. ", {"bold": True, "color": TITLE}),
         ("Con una evidencia así de clara, cambiar de modelo cambia la redacción, los tokens y el coste, no el contenido.", {})],
        [("Lo que no cambió: ", {"bold": True, "color": TITLE}),
         ("los 12 fragmentos y su orden, los 4 del prompt y la similitud 0,78. Por eso podemos atribuir la diferencia al modelo.", {})],
    ], size=11.5)
    takeaway(sl, "Misma entrada, una variable cambiada: el resultado es comparable y el coste queda a la vista.",
             label="Idea guía")
    footer(sl, block=2)
    notes(sl, """18:56–19:00. Contrastar con la predicción. Ambos modelos dieron TLS 1.3 y citaron [01-arquitectura-aethercloud], el documento de referencia: el criterio automático (dato clave + cita de un documento relevante) los da por buenos. Arriba, la evidencia: el fragmento 01#03, primero del prompt, con similitud 0,78.
Cifras del ensayo controlado del 22/11/2026 (perfil base .env.terra-opus, índice A, v1; solo cambió S19_GEN_MODEL): Hydrogen 404 → 126 tokens, 2,06 s de generación y 0,001551 USD; Terra 366 → 30 tokens, 1,31 s y 0,000516 USD. Son dos llamadas medidas por OpenRouter, no un promedio: otra ejecución puede variar algo. Los tokens de entrada difieren porque cada modelo usa su propio tokenizador con el mismo prompt.
Si en el directo sale otra redacción, comprobar dato y cita igual; lo importante es el método.
QUÉ ABRIR: resultados/ensayo-tres-pruebas-20261122/gemini-4-hydrogen-T01.txt y gpt-6.1-terra-T01.txt; en Langfuse, la observación generacion de cada turno (modelo, tokens y coste).
PREGUNTA: con este resultado, ¿cambiaríais de generador? ¿Qué os falta saber?
Fuentes: """ + ENSAYO3 + """gemini-4-hydrogen-T01.txt y gpt-6.1-terra-T01.txt; verificacion.md («Ensayo de las tres pruebas del directo · 22/11/2026»); guion-directo-modelos.md (tabla del ensayo controlado).""")
    return sl


# ---------------------------------------------------------------- prueba 1 · T12
def s09_t12_prueba(deck):
    sl = deck.slide(tag="t12-prueba")
    header(sl, "Prueba 1 · Cambiar el generador · T12", "Una pregunta que necesita dos fuentes")
    quote(sl, 43, 96, 874, 70, "Una organización del plan Empresa sufre un SEV-1: ¿qué soporte incluye su plan y cuál es "
          "el tiempo máximo de primera respuesta?", size=15.5, label_t="Pregunta T12 · datos/test.jsonl", accent=ST_GEN)
    # la referencia exige dos datos
    stage_card(sl, 43, 178, 340, 220, ST_DATOS, lab="La referencia exige dos datos")
    for i, (dato, que) in enumerate([("24x7", "soporte del plan Empresa para SEV-1"),
                                     ("15 minutos", "primera respuesta máxima de un SEV-1")]):
        y = 206 + i * 62
        chip(sl, 55, y, 104, 40, dato, fill=GREEN_BG, color=MINT_L, size=14, line=ST_DATOS, radius=4)
        text(sl, 168, y + 2, 120, 36, que, size=9.5, color=TEXT)
        chip(sl, 296, y + 8, 76, 24, "¿fuente?", fill=BG, color=MINT_L, size=9.5, line=MINT_L, radius=12)
    label(sl, 55, 334, 320, "documentos_relevantes", color=MUTED, size=8.5)
    for i, d in enumerate(["07-facturacion-y-planes", "06-respuesta-a-incidentes"]):
        chip(sl, 55 + i * 162, 352, 156, 22, d, fill=CARD2, color=TITLE, size=8.5, font=MONO, radius=3)
    text(sl, 55, 378, 320, 16, "¿Cuál acredita cada dato?", size=9.5, color=MUTED, check=False)
    _mirar(sl, 395, 178, 240, 220, ["Los 5 documentos recuperados: ¿están los dos?",
                                    "Los 4 fragmentos que entran al prompt",
                                    "Respuesta, cita o abstención de cada modelo"])
    prediccion(sl, 647, 178, 270, 220, ["¿Qué fuente acredita cada parte?", "¿Llegarán las dos al prompt?",
                                        "¿Responderá o se abstendrá cada modelo?"], ["Hydrogen:", "Terra:"])
    _vivo(sl, 410, [("  misma sesión (quedó en Terra tras T01):", MUTED),
                    "  › /perfil hydrogen-sol     › 3     › /perfil terra-opus     › 3",
                    ("  chat nuevo: comando completo de la diapositiva 7 (temperatura sin fijar en ambos)", MUTED)],
          "EN VIVO · consume OpenRouter")
    takeaway(sl, "Mismo cambio de generador, pero ahora la respuesta necesita combinar dos documentos.", label="Idea guía")
    footer(sl, block=2)
    notes(sl, """19:00–19:06. PRUEBA 1, segunda pregunta. Leer T12 y la referencia: «El plan Empresa incluye soporte 24x7 para SEV-1 y la primera respuesta llega en 15 minutos como máximo», con dos documentos relevantes (07-facturacion-y-planes y 06-respuesta-a-incidentes). Pedir la predicción: qué fuente debería acreditar cada parte, si llegarán las dos al prompt y si cada modelo responderá o se abstendrá. No adelantar el resultado.
Mismo cambio que en T01: solo el generador. Los fragmentos son los mismos para los dos modelos.
EN VIVO: al terminar T01 el chat quedó en Terra. En la misma sesión, empezar con `/perfil hydrogen-sol` y comprobar en la cabecera google/gemini-4-hydrogen; después `3`, `/perfil terra-opus` y `3`. Si se abre otro chat, copiar el comando completo de la diapositiva 7, que deja la temperatura sin fijar en ambos modelos. Después abrir la sesión chat-… en Langfuse: en recuperacion mirar los 5 documentos; en generacion, el prompt con los 4 fragmentos. Un modelo puede decidir distinto en cada llamada: si sale algo diferente al ensayo, mostrar ambas ejecuciones y revisar cada respuesta frente a los fragmentos que recibió.
QUÉ ABRIR: datos/test.jsonl (T12); corpus/07-facturacion-y-planes.md y corpus/06-respuesta-a-incidentes.md.
PREGUNTA: ¿qué fuente debería acreditar «24x7» y cuál «15 minutos»?
Fuentes: datos/test.jsonl (T12); guion-directo-modelos.md (caso `3` · T12 y tabla del ensayo controlado).""")
    return sl


def s10_t12_resultado(deck):
    sl = deck.slide(tag="t12-resultado")
    header(sl, "Resultado · T12", "El documento del plan se recuperó, pero no llegó al prompt")
    tag(sl, 43, 90, "ensayo")
    # tira de candidatos
    frs = ["06#02", "06#03", "06#04", "06#05", "06#01", "07#02", "01#05", "10#03", "10#02", "05#02", "05#04", "10#01"]
    items = []
    for f in frs:
        if f == "07#02":
            items.append((f, ST_FALLO_BG, ST_FALLO, TITLE))
        elif f[:2] in ("06", "07"):
            items.append((f, GREEN_BG, ST_DATOS, MINT_L))
        else:
            items.append((f, CARD2, BORDER, MUTED))
    text(sl, 43, 110, 400, 13, "12 candidatos, en orden de similitud", size=9.5, color=TITLE, bold=True)
    chip_row(sl, 43, 126, items, w=40, gap=3, size=8)
    box(sl, 43, 150, 4 * 43 - 3, 2.5, fill=ST_GEN, radius=0)
    text(sl, 43, 154, 169, 12, "al prompt (k_contexto = 4)", size=8.5, color=ST_GEN, bold=True, check=False)
    text(sl, 43 + 5 * 43 - 6, 154, 80, 12, "↑ puesto 6", size=8.5, color=ST_FALLO, bold=True, check=False)
    box(sl, 572, 106, 345, 60, fill=ST_RECUP_BG)
    text(sl, 584, 110, 325, 52, [{"runs": [("5 documentos: ", {"bold": True, "color": TITLE}), ("06 · 07 · 01 · 10 · 05", {"font": MONO})],
                                  "space": 3},
                                 {"runs": [("recall@5 = 2/2 = 1,00", {"bold": True, "color": MINT_L, "size": 13})]}],
         size=11, color=TEXT, space=3, anchor="m")
    # lo que leyó y lo que no
    label(sl, 43, 176, 420, "Lo que leyó el generador · los 4 fragmentos del prompt, resumidos", color=ST_GEN, size=8.5)
    leidos = [("06#02", [("SEV-1: primera respuesta en ", {}), hl("15 minutos"), (", actualizaciones cada 30 min ", {}),
                         hl("(24x7)", AMBER)]),
              ("06#03", [("SEV-2: primera respuesta en 60 minutos, actualizaciones cada 2 h", {})]),
              ("06#04", [("SEV-3: primera respuesta en 8 horas hábiles", {})]),
              ("06#05", [("Postmortem preliminar en 48 h; RCA en 5 días hábiles", {})])]
    y = 192
    for fid, runs in leidos:
        box(sl, 43, y, 440, 34, fill=CARD, line=ST_GEN, lw=0.75)
        text(sl, 51, y, 52, 34, fid, size=10, font=MONO, color=ST_GEN, bold=True, anchor="m")
        text(sl, 104, y, 372, 34, [runs], size=10.5, color=TITLE, anchor="m")
        y += 38
    box(sl, 497, 176, 420, 166, fill=ST_FALLO_BG, line=ST_FALLO, lw=1.5)
    label(sl, 509, 184, 400, "Puesto 6 · recuperado, pero no leído", color=ST_FALLO, size=9)
    text(sl, 509, 202, 400, 14, "07-facturacion-y-planes#02", size=10, font=MONO, color=ST_FALLO, bold=True)
    text(sl, 509, 222, 398, 116, [[("Plan Empresa: cuota base de 850 EUR/mes, incluye 15 millones de peticiones API, "
                                    "1 TiB de almacenamiento cifrado, ", {}), hl("soporte 24x7 para SEV-1", TITLE),
                                   (" y réplica activa en eu-fra-1.", {})]], size=14, color=TEXT)
    # resultados
    box(sl, 43, 350, 874, 1, fill=BORDER, radius=0)
    label(sl, 43, 356, 300, "Ensayo controlado · mismos fragmentos", color=ST_GEN, size=8.5)
    box(sl, 43, 372, 280, 92, fill=CARD, line=ST_GEN)
    text(sl, 55, 378, 258, 82, [{"runs": [("Hydrogen y Terra: ", {"bold": True, "color": TITLE}),
                                          ("«No consta en la documentación de AetherCloud».", {})], "space": 4},
                                {"runs": [("0,003327 y 0,001093 USD", {"font": MONO, "bold": True, "color": MUTED, "size": 9.5})]}],
         size=11, color=TEXT, space=4)
    tag(sl, 335, 356, "chat", w=200)
    box(sl, 335, 372, 280, 92, fill=CARD, line=ST_OBS)
    text(sl, 347, 378, 258, 82, [{"runs": [("Terra, otro turno: ", {"bold": True, "color": TITLE}), hl("24x7"), (" y ", {}),
                                           hl("15 minutos"), (", citando ", {}), hl("[06-respuesta-a-incidentes]", ST_GEN)],
                                  "space": 4},
                                 {"runs": [("La cita no acredita el plan.", {"bold": True, "color": ST_FALLO})]}],
         size=11, color=TEXT, space=4)
    box(sl, 627, 356, 290, 108, fill=CARD)
    box(sl, 627, 356, 3.5, 108, fill=MINT, radius=0)
    label(sl, 639, 364, 270, "Por qué", color=MINT, size=8.5)
    text(sl, 639, 381, 270, 80, "recall@5 cuenta documentos entre los 5 primeros; el modelo lee 4 fragmentos. "
         "El «24x7» de 06 son las actualizaciones, no el soporte del plan.", size=10.5, color=TEXT)
    takeaway(sl, "recall@5 = 1,00 no garantiza que el dato llegue al modelo: hay que mirar qué fragmentos entraron al prompt.",
             label="Idea guía")
    footer(sl, block=2)
    notes(sl, """19:06–19:16. El momento para explicar recall@5. Recall@5 = documentos relevantes entre los 5 primeros documentos distintos ÷ documentos relevantes de la pregunta: aquí 2/2 = 1,00 (06 y 07 están entre 06, 07, 01, 10 y 05). precision@5 = 2/5 = 0,40. Ambas cuentan documentos, no fragmentos. Pero el generador no lee 5 documentos: lee los 4 primeros FRAGMENTOS (S19_K_CONTEXTO=4), y aquí los cuatro son del documento 06. El fragmento del plan, 07#02, con «soporte 24x7 para SEV-1», quedó en el puesto 6: cuenta para recall@5 y no llega al prompt. Señalar en grande ese fragmento y los cuatro que sí entraron.
Resultados, presentados como ejecuciones distintas. Ensayo controlado del 22/11/2026 (mismos fragmentos para los dos): Hydrogen y Terra se abstuvieron después de generar («No consta», motivo generador_sin_respuesta); costes de generación 0,003327 y 0,001093 USD. Es coherente con lo que leyeron, aunque el criterio lo cuente como abstención incorrecta. En otro turno real, el chat del 22/11/2026 (sesión chat-20261122-155649, coste 0,001338 USD), Terra respondió «24x7» y «15 minutos» y citó 06-respuesta-a-incidentes. Revisarlo frente a la fuente: en 06#02 «(24x7)» describe la cadencia de actualizaciones de un SEV-1, no el soporte incluido en el plan Empresa. La cita acredita los 15 minutos, no la parte del plan.
Contraste con el histórico (anexo): en la comparación por lotes Hydrogen–Sol, T12 también fue el caso inestable.
Mejoras posibles, que se validarían con validación y no con este test: subir k_contexto, limitar fragmentos por documento o reordenar.
QUÉ ABRIR: Langfuse → sesión del chat → recuperacion (documentos) y generacion (prompt con los 4 fragmentos); evaluacion/metricas.py (documentos distintos).
PREGUNTA: ¿cómo afecta a la respuesta que un documento recuperado quede fuera del prompt?
Fuentes: """ + ENSAYO3 + """gemini-4-hydrogen-T12.txt y gpt-6.1-terra-T12.txt; verificacion.md («Chat T12 con Hydrogen y Terra» y «Ensayo de las tres pruebas»); guion-directo-modelos.md (caso `3`); textos de 06#02–06#05 y 07#02 obtenidos con rag/corpus.py sobre corpus/.""")
    return sl


# ---------------------------------------------------------------- prueba 2 · V02
def s11_v02_prueba(deck):
    sl = deck.slide(tag="v02-prueba")
    header(sl, "Prueba 2 · Cambiar el juez · V02", "Misma respuesta, otro juez: ¿qué nota esperáis?")
    quote(sl, 43, 96, 874, 56, "¿Qué tamaño máximo de cuerpo admite una petición POST?", size=19,
          label_t="Pregunta V02 · datos/validacion.jsonl", accent=ST_JUEZ)
    # respuesta congelada y evidencia
    answer(sl, 43, 164, 340, 104, "Respuesta congelada · no se regenera",
           [("El tamaño máximo de cuerpo permitido en cualquier petición POST es de ", {}), hl("4 MiB"), (" ", {}),
            hl("[03-limites-y-cuotas-api]", ST_GEN), (".", {})],
           "Hydrogen · 390→127 tk · 0,0015375 USD", accent=ST_GEN, size=10.5)
    frag(sl, 43, 278, 340, 62, "03-limites-y-cuotas-api#04",
         [("El tamaño máximo de cuerpo permitido en cualquier petición POST es de ", {}), hl("4 MiB"), (".", {})],
         sub="1.er fragmento del contexto", size=10.5)
    box(sl, 43, 350, 340, 48, fill=CARD)
    text(sl, 55, 354, 96, 40, "Cada juez recibe exactamente:", size=9.5, color=MUTED, anchor="m")
    x = 152
    for t in ("pregunta", "respuesta", "4 fragmentos"):
        chip(sl, x, 364, len(t) * 5.0 + 14, 20, t, fill=CARD2, color=TITLE, size=9, line=ST_JUEZ, radius=4)
        x += len(t) * 5.0 + 19
    # cambio y métricas
    stage_card(sl, 395, 164, 250, 234, ST_JUEZ, lab="Lo que cambiamos · el juez")
    chip(sl, 407, 190, 226, 24, "GPT‑6.2 Sol", fill=CARD2, color=TITLE, size=11, line=BORDER, radius=4)
    text(sl, 395, 214, 250, 14, "↓", size=12, color=ST_JUEZ, bold=True, align="c", check=False)
    chip(sl, 407, 230, 226, 24, "Claude Opus 5.5", fill=CARD2, color=ST_JUEZ, size=11, line=ST_JUEZ, radius=4)
    text(sl, 407, 262, 226, 40, "= misma fila (cmp sin diferencias), Ragas 0.4.3, embeddings y máx. 1024 tokens",
         size=9, color=MUTED)
    text(sl, 407, 302, 226, 94, [
        {"runs": [("Faithfulness: ", {"bold": True, "color": TITLE}),
                  ("afirmaciones de la respuesta respaldadas por el contexto ÷ afirmaciones.", {})], "space": 5},
        {"runs": [("Answer Relevancy: ", {"bold": True, "color": TITLE}),
                  ("¿contesta a lo preguntado? El juez deduce preguntas desde la respuesta y las compara con la original.", {})]},
    ], size=9.5, color=TEXT, space=5)
    prediccion(sl, 657, 164, 260, 234, ["¿La cita respalda «4 MiB»?", "¿Qué fidelidad dará cada juez?",
                                        "¿Cuánto más costará juzgar que generar?"], ["Sol:", "Opus:"])
    _vivo(sl, 410, [("$ s19_ensayo=resultados/ensayo-tres-pruebas-20261122", MINT_L),
                    ('$ cmp "$s19_ensayo/juez-sol/respuestas.jsonl" "$s19_ensayo/juez-opus/respuestas.jsonl"', MINT_L),
                    ('$ cat "$s19_ensayo/juez-sol/puntuaciones.jsonl" "$s19_ensayo/juez-opus/puntuaciones.jsonl"', MINT_L)],
          "SIN COSTE · archivos guardados")
    takeaway(sl, "Congelamos la respuesta para que lo único que cambie sea quién la puntúa.", label="Idea guía")
    footer(sl, block=3)
    notes(sl, """19:16–19:22. PRUEBA 2. Ahora no se toca el sistema: se congela una respuesta y se cambia el juez. Leer V02 (pregunta de validación) y la respuesta guardada: «El tamaño máximo de cuerpo permitido en cualquier petición POST es de 4 MiB [03-limites-y-cuotas-api]». Pedir al grupo que compruebe en la evidencia que la frase del documento 03 lo dice literalmente.
Explicar en una frase cada métrica. Faithfulness: el juez divide la respuesta en afirmaciones y comprueba cada una contra el contexto; la nota es respaldadas ÷ total. Answer Relevancy: el juez genera preguntas a partir de la respuesta y mide, con embeddings, cuánto se parecen a la pregunta original.
Qué cambia: el modelo juez, de GPT‑6.2 Sol a Claude Opus 5.5. Qué no: la fila completa (pregunta, respuesta y fragmentos: `cmp` no encuentra diferencias), Ragas 0.4.3, los embeddings y el máximo de 1024 tokens.
El coste de generar la respuesta (Hydrogen, 0,0015375 USD) se pagó una vez y no forma parte de la prueba: se muestra aparte.
EN VIVO, sin coste: `cmp` y `cat` sobre los archivos del ensayo. Para repetir el ensayo con gasto real, comandos en el anexo y en el guion del directo.
QUÉ ABRIR: resultados/ensayo-tres-pruebas-20261122/juez-sol/ y juez-opus/ (respuestas.jsonl y puntuaciones.jsonl); evaluador/evaluar.py (dónde lee la respuesta y el modelo juez).
PREGUNTA: si los dos jueces leen exactamente lo mismo, ¿qué esperáis que cambie?
Fuentes: """ + ENSAYO3 + """juez-sol y juez-opus (respuestas.jsonl idénticos; puntuaciones.jsonl); resultados/ejemplo-real/validacion-A/respuestas.jsonl (V02, coste de generación); guion-directo-modelos.md («Prueba 2»).""")
    return sl


def s12_v02_resultado(deck):
    sl = deck.slide(tag="v02-resultado")
    header(sl, "Resultado · V02", "Los dos jueces la aprueban; Opus cuesta 2,7 veces más")
    tag(sl, 43, 90, "ensayo")
    # tabla visual
    X = 43
    box(sl, X, 110, 580, 250, fill=CARD)
    text(sl, X + 220, 118, 170, 14, "GPT‑6.2 Sol", size=11, color=TITLE, bold=True, align="c")
    text(sl, X + 400, 118, 170, 14, "Claude Opus 5.5", size=11, color=ST_JUEZ, bold=True, align="c")
    filas = [("Faithfulness", "afirmaciones respaldadas", 1.0, 1.0, "1,0000", "1,0000", 1.0),
             ("Answer Relevancy", "contesta a lo preguntado", 0.9566, 0.9585, "0,9566", "0,9585", 1.0),
             ("Coste de juzgar", "las dos métricas", 0.01064334, 0.02860928, "0,01064334 USD", "0,02860928 USD", 0.02860928),
             ("Tokens del juez", "entrada → salida", 3745, 5537, "3.745 → 253", "5.537 → 323", 5537)]
    y = 144
    for nombre, sub, a, b, ta, tb, mx in filas:
        box(sl, X + 10, y - 6, 560, 0.8, fill=BORDER, radius=0)
        text(sl, X + 12, y, 200, 15, nombre, size=12, color=TITLE, bold=True)
        text(sl, X + 12, y + 17, 200, 13, sub, size=9, color=MUTED)
        for i, (v, t) in enumerate(((a, ta), (b, tb))):
            xx = X + 220 + i * 180
            text(sl, xx, y, 170, 15, t, size=12, color=TITLE if i == 0 else ST_JUEZ, bold=True, align="c", font=MONO)
            bar(sl, xx + 10, y + 22, 150, 8, v / mx, color=MINT if nombre in ("Faithfulness", "Answer Relevancy") else ST_JUEZ)
        y += 52
    # coste de generar aparte
    box(sl, 635, 110, 282, 250, fill=ST_GEN_BG)
    label(sl, 647, 118, 260, "Generar no es juzgar", color=ST_GEN, size=8.5)
    text(sl, 647, 136, 260, 30, "La respuesta se generó una vez con Hydrogen.", size=10, color=TEXT)
    _cost_bars(sl, 647, 176, 258, [("Generar", 0.0015375, ST_GEN), ("Juez Sol", 0.01064334, ST_JUEZ),
                                   ("Juez Opus", 0.02860928, ST_JUEZ)], 0.02860928, paso=32,
               fmt=lambda v: f"{v:.4f}".replace(".", ","), lab_w=74, val_w=52)
    text(sl, 647, 280, 260, 74, [[("Juzgar costó ×6,9 (Sol) y ×18,6 (Opus) lo que costó generar. ", {"bold": True, "color": TITLE}),
                                  ("En Langfuse van en trazas distintas.", {})]], size=10, color=TEXT)
    _porque(sl, 43, 372, 580, 92, [
        [("Una sola afirmación que el contexto dice literalmente: ", {"bold": True, "color": TITLE}),
         ("no hay nada que dividir ni interpretar, y los dos la verifican. La relevancia sale de preguntas que el juez "
          "reconstruye y de embeddings: varía 0,0019 entre jueces.", {})]], size=11.5)
    box(sl, 635, 372, 282, 92, fill=ST_OBS_BG)
    label(sl, 647, 380, 260, "Dónde se ve", color=ST_OBS, size=8.5)
    text(sl, 647, 397, 262, 62, "Scores de consulta-rag (V02) y consumo-juez en evaluador-ragas. En la sesión de "
         "Langfuse están los de Sol; los de Opus, en puntuaciones.jsonl.", size=9.5, color=TEXT)
    takeaway(sl, "Con notas iguales en un caso fácil, el juez se elige por coste… salvo que un caso difícil diga otra cosa.",
             label="Idea guía")
    footer(sl, block=3)
    notes(sl, """19:22–19:32. Contrastar con la predicción. Sobre la misma fila de V02, los dos jueces dieron Faithfulness 1,0000 y puntuaron las dos métricas (cobertura 1/1). Answer Relevancy: 0,9566 con Sol y 0,9585 con Opus, una diferencia de 0,0019. Coste de juzgar (las dos métricas): 0,01064334 USD con Sol (3.745 → 253 tokens) y 0,02860928 USD con Opus (5.537 → 323 tokens), unas 2,7 veces más. Estas cifras son del juez.
Aparte, el coste de generar la respuesta: 0,0015375 USD con Hydrogen, una sola vez. Juzgarla costó unas 6,9 veces más con Sol y 18,6 con Opus: en una evaluación por lotes, el juez suele ser la partida principal. Por eso la demo publica su consumo en otra traza (evaluador-ragas → consumo-juez) y no lo suma al coste por consulta.
Por qué coinciden: la respuesta tiene una sola afirmación y el contexto la dice literalmente. La relevancia depende de las preguntas que el juez reconstruye y de los embeddings, así que varía un poco. Advertir: un caso fácil no basta para elegir juez; la prueba 3 lo demuestra.
En Langfuse (sesión langfuse-prueba-hydrogen) están los scores y el consumo de Sol para V02; los de Opus de este ensayo están solo en local.
QUÉ ABRIR: puntuaciones.jsonl de juez-sol y juez-opus (campos valor, consumo.tokens_* y consumo.coste_usd); Langfuse → V02 → Scores y evaluador-ragas → consumo-juez.
PREGUNTA: el juez falla en 3 de 14 respuestas y la media sale 0,95. ¿Qué número falta? (La cobertura.)
Fuentes: """ + ENSAYO3 + """juez-sol/puntuaciones.jsonl y juez-opus/puntuaciones.jsonl; verificacion.md («Ensayo de las tres pruebas» y «Corrección del consumo del juez»); resultados/ejemplo-real/validacion-A/respuestas.jsonl (V02).""")
    return sl


# ---------------------------------------------------------------- prueba 3 · T09
def _cond(sl, x, y, t, col=MINT_L, fill=GREEN_BG, line_c=ST_DATOS, w=None, size=10, rota=False):
    if rota:
        col, fill, line_c = TITLE, ST_FALLO_BG, ST_FALLO
    w = w or (len(t) * size * 0.52 + 20)
    chip(sl, x, y, w, 22, t, fill=fill, color=col, size=size, line=line_c, radius=4)
    return x + w


def s13_t09_prueba(deck):
    sl = deck.slide(tag="t09-prueba")
    header(sl, "Prueba 3 · Detectar una regresión · T09", "¿Está respaldada esta respuesta?")
    quote(sl, 43, 96, 874, 64, "¿Cuánto mantenimiento programado al mes queda fuera del cálculo de disponibilidad y con "
          "qué antelación se avisa?", size=15.5, label_t="Pregunta T09 · datos/test.jsonl", accent=ST_FALLO)
    frag(sl, 43, 172, 560, 62, "05-sla-y-creditos-servicio#02  ·  lo que lee el juez",
         [("El cálculo excluye las ventanas de mantenimiento programado ", {}),
          hl("notificadas con al menos 7 días naturales de antelación"), (" ", {}), hl("y", AMBER), (" ", {}),
          hl("cuya duración no supere los 45 minutos al mes"), (".", {})], size=10.5)
    answer(sl, 43, 242, 560, 104, "Respuesta guardada · Hydrogen · test A",
           [("Quedan fuera del cálculo de disponibilidad las ventanas de mantenimiento programado ", {}),
            hl("cuya duración no supere los 45 minutos al mes"), (" [05-…], ", {}), hl("siempre que", AMBER), (" ", {}),
            hl("hayan sido notificadas con al menos 7 días naturales de antelación"), (" [05-…].", {})],
           "misma fila para los dos jueces · cmp sin diferencias", size=10.5, accent=ST_GEN)
    # condiciones juntas
    box(sl, 43, 354, 560, 44, fill=CARD)
    text(sl, 55, 356, 110, 40, "Las dos condiciones van juntas:", size=9.5, color=MUTED, anchor="m")
    x = _cond(sl, 170, 365, "≤ 45 min al mes")
    text(sl, x + 4, 365, 26, 22, "Y", size=13, color=AMBER, bold=True, align="c", anchor="m", check=False)
    x = _cond(sl, x + 34, 365, "aviso ≥ 7 días naturales")
    text(sl, x + 6, 365, 120, 22, "→ fuera del cálculo", size=10, color=TITLE, anchor="m", check=False)
    # derecha
    stage_card(sl, 615, 172, 302, 64, ST_JUEZ, lab="Lo que cambiamos · el juez")
    chip(sl, 627, 198, 120, 26, "GPT‑6.2 Sol", fill=CARD2, color=TITLE, size=10.5, line=BORDER, radius=4)
    text(sl, 747, 200, 36, 22, "→", size=13, color=ST_JUEZ, bold=True, align="c", check=False)
    chip(sl, 783, 198, 122, 26, "Claude Opus 5.5", fill=CARD2, color=ST_JUEZ, size=10.5, line=ST_JUEZ, radius=4)
    prediccion(sl, 615, 244, 302, 154, ["¿Está respaldada: sí o no?", "¿Qué fidelidad dará cada juez?"],
               ["Sol:", "Opus:"])
    _vivo(sl, 410, [("$ s19_ensayo=resultados/ensayo-regresion-modelo-20261122", MINT_L),
                    ('$ cmp "$s19_ensayo/juez-sol-T09/respuestas.jsonl" "$s19_ensayo/juez-opus-T09/respuestas.jsonl"', MINT_L),
                    ("  después: afirmaciones y veredictos en detalle-faithfulness.json de cada juez", MUTED)],
          "SIN COSTE · archivos guardados")
    takeaway(sl, "Decidid antes de ver las notas: si el contexto respalda todas las afirmaciones, esperamos fidelidad 1,00.",
             label="Idea guía")
    footer(sl, block=4)
    notes(sl, """19:32–19:38. PRUEBA 3. Proyectar T09 y leer el fragmento 05#02, que es lo que recibe el juez como contexto: el mantenimiento queda fuera del cálculo si se notifica con al menos 7 días naturales de antelación Y dura como máximo 45 minutos al mes. Las dos condiciones van juntas.
Leer la respuesta guardada (generada por Hydrogen en el test A del 22/11/2026): une las dos condiciones con «siempre que» y cita 05-sla-y-creditos-servicio. Es correcta y está completa: el criterio automático la dio por acierto.
Pedir al grupo que decida si está respaldada ANTES de enseñar las notas, y qué fidelidad esperan de cada juez. Cambia lo mismo que en la prueba 2: el juez de Sol a Opus. La fila es idéntica para los dos (`cmp` sin diferencias).
EN VIVO, sin coste: el `cmp` de la diapositiva. Opcional: `uv run pytest` y enseñar en tests/test_grafo.py y tests/test_enrutado.py las comprobaciones de trayectoria, para enlazar con «testing de agentes y pipelines».
QUÉ ABRIR: resultados/ensayo-regresion-modelo-20261122/juez-sol-T09/ y juez-opus-T09/ (respuestas.jsonl y detalle-faithfulness.json).
PREGUNTA: si el contexto respalda todas las afirmaciones, ¿qué fidelidad esperáis? (Fidelidad mide respaldo en el contexto, no corrección: no mezclar las dos ideas.)
Fuentes: """ + REGRE + """juez-sol-T09 y juez-opus-T09 (respuestas.jsonl idénticos); datos/test.jsonl (T09); verificacion.md («Regresión al sustituir el juez en T09 · 22/11/2026»).""")
    return sl


def s14_t09_resultado(deck):
    sl = deck.slide(tag="t09-resultado")
    header(sl, "Resultado · T09", "Opus separa dos condiciones que debían ir juntas")
    tw = tag(sl, 43, 90, "ensayo")
    tag(sl, 43 + tw + 8, 90, "local")
    # respuesta de partida
    box(sl, 260, 108, 440, 40, fill=CARD, line=ST_GEN)
    text(sl, 272, 108, 110, 40, "MISMA RESPUESTA", size=8.5, color=ST_GEN, bold=True, anchor="m")
    x = _cond(sl, 372, 117, "≤ 45 min", size=9.5)
    text(sl, x + 2, 117, 22, 22, "Y", size=12, color=AMBER, bold=True, align="c", anchor="m", check=False)
    x = _cond(sl, x + 26, 117, "aviso ≥ 7 días", size=9.5)
    text(sl, x + 6, 117, 100, 22, "→ fuera", size=9.5, color=TITLE, anchor="m", check=False)
    poly(sl, [(400, 150), (400, 160), (256, 160), (256, 170)], color=MINT, w=1.75)
    poly(sl, [(560, 150), (560, 160), (704, 160), (704, 170)], color=ST_FALLO, w=1.75)
    # rama Sol
    L, R, W = 43, 487, 430
    for xx, col, fill in ((L, MINT, GREEN_BG), (R, ST_FALLO, ST_FALLO_BG)):
        box(sl, xx, 172, W, 220, fill=CARD, line=col, lw=1.25)
    box(sl, L, 172, W, 24, fill=MINT, radius=0)
    text(sl, L + 10, 176, W - 20, 16, "GPT‑6.2 Sol · extrae 1 afirmación", size=10.5, color=DARK, bold=True)
    box(sl, L + 10, 204, W - 20, 104, fill=GREEN_BG, line=ST_DATOS, radius=4)
    x = _cond(sl, L + 20, 212, "≤ 45 min al mes", size=9.5)
    text(sl, x + 2, 212, 22, 22, "Y", size=12, color=AMBER, bold=True, align="c", anchor="m", check=False)
    x = _cond(sl, x + 26, 212, "aviso ≥ 7 días naturales", size=9.5)
    text(sl, L + 20, 240, W - 110, 60, "«…quedan fuera del cálculo de disponibilidad si suman como máximo 45 minutos al mes "
         "y cuentan con un aviso previo de al menos 7 días naturales.»", size=10.5, color=TITLE)
    chip(sl, L + W - 80, 252, 60, 40, "✓ 1", fill=MINT, color=DARK, size=15, radius=6)
    text(sl, L + 12, 314, W - 24, 30, [[("Motivo del juez: ", {"bold": True, "color": MINT}),
                                        ("el contexto excluye las ventanas notificadas con 7 días y de 45 min como máximo.", {})]],
         size=9, color=TEXT)
    text(sl, L + 12, 350, 200, 34, "fidelidad 1/1 = 1,00", size=15, font=SERIF, color=TITLE, anchor="m")
    chip(sl, L + W - 126, 354, 114, 28, "PASA (0)", fill=MINT, color=DARK, size=12, radius=4)
    # rama Opus
    box(sl, R, 172, W, 24, fill=ST_FALLO, radius=0)
    text(sl, R + 10, 176, W - 20, 16, "Claude Opus 5.5 · extrae 2 afirmaciones", size=10.5, color=DARK, bold=True)
    for i, (cond, falta, motivo) in enumerate([("≤ 45 min al mes", "aviso ≥ 7 días", "omite el aviso"),
                                               ("aviso ≥ 7 días naturales", "≤ 45 min", "presenta el aviso como suficiente")]):
        y = 204 + i * 54
        box(sl, R + 10, y, W - 20, 48, fill=ST_FALLO_BG, line=ST_FALLO, radius=4)
        x = _cond(sl, R + 20, y + 6, cond, size=9.5, rota=True)
        text(sl, x + 4, y + 6, 110, 22, "→ basta", size=10, color=TITLE, bold=True, anchor="m", check=False)
        text(sl, R + 20, y + 30, 300, 14, f"falta «{falta}»: {motivo}", size=9, color=ST_FALLO, bold=True, check=False)
        chip(sl, R + W - 80, y + 8, 60, 32, "✗ 0", fill=ST_FALLO, color=DARK, size=14, radius=6)
    text(sl, R + 12, 314, W - 24, 30, [[("Motivo del juez (traducido): ", {"bold": True, "color": ST_FALLO}),
                                        ("el contexto exige las dos condiciones a la vez.", {})]], size=9, color=TEXT)
    text(sl, R + 12, 350, 200, 34, "fidelidad 0/2 = 0,00", size=15, font=SERIF, color=TITLE, anchor="m")
    chip(sl, R + W - 126, 354, 114, 28, "FALLA (1)", fill=ST_FALLO, color=DARK, size=12, radius=4)
    # abajo: salida real y control por caso frente a lote
    term(sl, 43, 400, 430, 66, [("openai/gpt-6.2-sol · T09 · fidelidad 1.00 · PASA", MINT_L),
                                ("Código de salida: 0", MINT_L),
                                ("anthropic/claude-opus-5.5 · T09 · fidelidad 0.00 · FALLA", CORAL),
                                ("Código de salida: 1", CORAL)], size=9, pitch=12.5)
    box(sl, 487, 400, 430, 66, fill=CARD)
    text(sl, 499, 406, 410, 58, [
        {"runs": [("Por caso: ", {"bold": True, "color": MINT_L}),
                  ("«T09 debe dar 1,00» → con Opus falla y lo detecta.", {})], "space": 3},
        {"runs": [("Por lote: ", {"bold": True, "color": AMBER}),
                  ("test A con juez Opus: fidelidad media 0,92 ≥ 0,90 → el control PASA (0) con este 0 dentro.", {})]},
    ], size=9.5, color=TEXT, space=3)
    takeaway(sl, "La respuesta no cambió: cambió cómo se juzga. Un control por caso lo detecta; la media del lote lo esconde.",
             label="Idea guía")
    footer(sl, block=4)
    notes(sl, """19:38–19:50. La infografía central de la clase. Partimos de la MISMA respuesta y el MISMO contexto. Ragas calcula Faithfulness en dos pasos: primero el juez extrae afirmaciones de la respuesta; después verifica cada una contra el contexto.
Rama Sol (verde): extrajo UNA afirmación que conserva las dos condiciones juntas («si suman como máximo 45 minutos al mes y cuentan con un aviso previo de al menos 7 días naturales») y la verificó: veredicto 1. Fidelidad 1/1 = 1,00 → la comprobación de T09 PASA (código 0).
Rama Opus (coral): extrajo DOS afirmaciones, una por condición, y cada una presenta su condición como suficiente por sí sola. El verificador rechazó ambas por la condición omitida (motivos reales, en inglés en detalle-faithfulness.json: «leaves out the notice requirement» y «presents 7 days' notice as sufficient on its own»). Fidelidad 0/2 = 0,00 → FALLA (código 1). Answer Relevancy 0,7491 (Sol) frente a 0,6911 (Opus); coste de juzgar 0,01283984 frente a 0,05257002 USD.
Se repitió Faithfulness guardando afirmaciones y veredictos: volvió a dar 1,00 y 0,00. La regresión está en la evaluación de una respuesta correcta, no en el sistema.
Abajo a la izquierda, la salida real de la comprobación por caso (script del guion, ejecutado sin coste sobre los archivos guardados). A la derecha, la diferencia con el control por umbrales: el test A completo, juzgado por Opus, tiene fidelidad media 0,9231 sobre 13 respuestas evaluables, por encima del mínimo 0,90 de umbrales.real.json; `python s19.py regresion resultados/ejemplo-real/test-A` devuelve PASA (0) aunque T09 vale 0. El umbral agregado vigila el lote; el control por caso vigila respuestas conocidas. Los dos se pueden automatizar en pytest o en CI.
Estos veredictos son resultados LOCALES: no se publicaron en Langfuse.
QUÉ ABRIR: detalle-faithfulness.json de juez-sol-T09 y juez-opus-T09; ejecutar el bucle de comprobación del guion del directo (Prueba 3); datos/umbrales.real.json.
PREGUNTA: ¿qué parte del evaluador falló si dos modelos recibieron la misma respuesta?
Fuentes: """ + REGRE + """juez-sol-T09 y juez-opus-T09 (detalle-faithfulness.json, puntuaciones.jsonl); salida de la comprobación de T09 y de `s19.py regresion resultados/ejemplo-real/test-A`, ejecutadas en local el 22/11/2026; resultados/ejemplo-real/test-A/informe.json; datos/umbrales.real.json; verificacion.md («Regresión al sustituir el juez en T09»).""")
    return sl


SLIDES = [s07_t01_prueba, s08_t01_resultado, s09_t12_prueba, s10_t12_resultado, s11_v02_prueba, s12_v02_resultado,
          s13_t09_prueba, s14_t09_resultado]
