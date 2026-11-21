"""Diapositivas 1–6: apertura y bloque 1 (el proyecto: piezas, planificación y arquitectura)."""

from comun import AWS, DOBLE, EVIDENCIA, LAURA, LOGOS, PROYECTO, TEMARIO
from deck_lib import *  # noqa: F401,F403


def s01_portada(d):
    sl = d.slide(BG_SECTION, "portada")
    img(sl, "thepower-logo.png", 38, 34, h=32)
    text(sl, 43, 104, 420, 14, "S20 · AI ENGINEER", size=10, color=MINT, bold=True)
    text(sl, 43, 124, 450, 92, "Proyecto final:\nagente conversacional", size=36, font=SERIF, color=TITLE)
    text(sl, 43, 226, 425, 78,
         "Integramos en un solo proyecto lo aprendido en el curso: un agente LangGraph que consulta tickets por MCP, "
         "responde con fuentes gracias al RAG, investiga con límites, recuerda en PostgreSQL, se observa con Langfuse "
         "y se expone con FastAPI, listo para AWS.", size=12.5, color=TEXT)
    text(sl, 43, 322, 420, 16, "José Antonio Nuevo", size=12.5, color=TITLE, bold=True)
    text(sl, 43, 342, 440, 34, "Miércoles 2 de diciembre de 2026 · grupo L/X\n18:30–20:00 · hora de Madrid",
         size=10.5, color=MUTED)
    box(sl, 497, 52, 420, 410, fill=BG, line="2A5246", radius=8)
    text(sl, 515, 70, 380, 14, "TECNOLOGÍAS QUE INTEGRAMOS", size=9, color=MINT, bold=True)
    items = [("langgraph-icon.png", "LangGraph"), ("mcp-icon.png", "MCP"), ("postgresql.png", "PostgreSQL"),
             ("fastapi-icon.png", "FastAPI"), ("langfuse-icon.png", "Langfuse"), ("aws-fargate.png", "AWS")]
    for i, (ic, lab) in enumerate(items):
        x = 515 + i * 64
        encajar(sl, ic, x + 12, 92, 40, 40)
        text(sl, x - 4, 138, 72, 14, lab, size=9, color=TITLE, align="c", bold=True)
    text(sl, 515, 172, 380, 12, "EL RECORRIDO DE UN TURNO", size=9, color=MINT, bold=True)
    flujo = ["cliente", "FastAPI", "grafo", "herramientas", "respuesta"]
    anchos = [56, 62, 50, 92, 74]
    x = 515
    for i, (f, w) in enumerate(zip(flujo, anchos)):
        chip(sl, x, 192, w, 22, f, fill=TAKE_BG, color=MINT_L, size=9.5, line="2A5246")
        if i < len(flujo) - 1:
            line(sl, x + w + 2, 203, x + w + 12, 203, color=MINT, w=1.25)
        x += w + 14
    filas = [("mcp-icon.png", "MCP", "trae los datos del ticket desde su propio servidor."),
             ("g-document.png", "RAG", "cita la política interna o dice que no consta."),
             ("g-globe.png", "Deep Research", "añade fuentes públicas, con límites.")]
    y = 228
    for ic, t, b in filas:
        encajar(sl, ic, 515, y, 22, 22)
        text(sl, 545, y + 3, 360, 16, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10.5, color=TEXT)
        y += 30
    box(sl, 515, 330, 384, 114, fill=CARD, radius=6)
    text(sl, 527, 340, 360, 12, "CADA PIEZA VIENE DE UNA SESIÓN DEL CURSO", size=8.5, color=MUTED, bold=True)
    sesiones = ["S5 · LangGraph", "S6 · Langfuse", "S9 · PostgreSQL", "S10–S12 · RAG", "S15 · MCP",
                "S16–S17 · AWS"]
    for i, s in enumerate(sesiones):
        chip(sl, 527 + (i % 3) * 122, 362 + (i // 3) * 34, 116, 24, s, fill=CARD2, color=MINT_L, size=8.5,
             line="2A5246")
    nota(sl, "18:30", "18:31",
         "título del temario: «Proyecto final: Agente conversacional». Es la última sesión del programa para el grupo "
         "L/X. No presentamos tecnología nueva: juntamos en un proyecto pequeño lo que vimos por separado (LangGraph en "
         "S5, Langfuse en S6, PostgreSQL en S9, RAG y Deep Research en S10–S12, MCP en S15, AWS en S16–S17) y "
         "comprobamos que funciona junto. " + DOBLE,
         pregunta="«Si tuvierais que enseñar a alguien que vuestro agente funciona, ¿qué le enseñaríais?»",
         fuentes=TEMARIO + " Calendario: GUIA-DE-CLASES-2026.md (S20, 02/12, L/X). " + PROYECTO,
         imagenes=LOGOS)
    return sl


def s02_encuesta(d):
    sl = d.slide(tag="encuesta")
    header(sl, "Antes de empezar", "Encuesta de S19 y plan de la sesión",
           "Un minuto para valorar la sesión anterior de tu grupo. Después, 90 minutos para recorrer el proyecto final "
           "pieza a pieza: cada bloque explica un concepto y lo enseña funcionando.")
    box(sl, 43, 140, 250, 326, fill=CARD, line=BORDER)
    box(sl, 70, 156, 196, 196, fill="FFFFFF", radius=6)
    img(sl, "qr-ai-engineer.jpg", 78, 164, w=180, h=180)
    text(sl, 55, 362, 226, 18, "Encuesta de la sesión anterior · S19", size=11.5, color=TITLE, bold=True, align="c")
    text(sl, 55, 382, 226, 14, "Formulario de AI Engineer", size=10, color=MUTED, align="c")
    text(sl, 55, 402, 226, 50, "Valora S19, la sesión del lunes 30/11 (no la de hoy). Escanea el código con la "
                               "cámara del móvil.", size=10, color=TEXT, align="c")
    filas = [("18:30", "Apertura", "QR, caso y las tres fuentes de verdad", 6, MUTED),
             ("18:36", "1 · Proyecto", "Piezas, planificación y arquitectura", 9, BLOCK_COLORS[0]),
             ("18:45", "2 · Agente", "Prompt, configuración, grafo y herramientas", 13, BLOCK_COLORS[1]),
             ("18:58", "3 · Memoria y API", "PostgreSQL, dueño del hilo y FastAPI", 14, BLOCK_COLORS[2]),
             ("19:12", "4 · MCP y RAG", "Servidor MCP propio, citas y rechazo", 16, BLOCK_COLORS[3]),
             ("19:28", "5 · Deep Research", "Investigación acotada como trabajo", 10, BLOCK_COLORS[4]),
             ("19:38", "6 · Observar y desplegar", "Traza, AWS y límites en el código", 10, BLOCK_COLORS[5]),
             ("19:48", "7 · Entrega y cierre", "Aceptación, entrega y preguntas", 12, BLOCK_COLORS[6])]
    text(sl, 312, 140, 60, 12, "HORA", size=8.5, color=MUTED, bold=True)
    text(sl, 385, 140, 180, 12, "BLOQUE", size=8.5, color=MUTED, bold=True)
    text(sl, 580, 140, 280, 12, "QUÉ HAREMOS", size=8.5, color=MUTED, bold=True)
    text(sl, 862, 140, 55, 12, "MIN", size=8.5, color=MUTED, bold=True, align="r")
    y = 156
    for t, b, desc, m, col in filas:
        box(sl, 312, y, 605, 35, fill=CARD)
        box(sl, 312, y, 4, 35, fill=col, radius=0)
        text(sl, 324, y + 10, 56, 16, t, size=11, font=MONO, color=MINT_L, bold=True)
        text(sl, 385, y + 10, 195, 16, b, size=11, color=TITLE, bold=True)
        text(sl, 580, y + 4, 275, 28, desc, size=10, color=TEXT, anchor="m")
        text(sl, 862, y + 10, 45, 16, str(m), size=11.5, color=col, bold=True, align="r")
        y += 39
    takeaway(sl, "Hoy todo corre en el perfil doble: sin modelo, sin claves y sin coste. Lo real es la integración.",
             "Formato")
    footer(sl)
    nota(sl, "18:31", "18:33",
         "dar un minuto para escanear. La encuesta evalúa S19, la sesión anterior del grupo L/X (lunes 30/11, "
         "evaluación y testing, impartida por José). Después, presentar la agenda: siete bloques que siguen un turno "
         "del agente desde la petición HTTP hasta la respuesta con fuentes, y terminan en cómo se entrega el proyecto. "
         "Formato pedido por la escuela: teoría y práctica a la vez. Cada bloque tiene una franja «EN VIVO» con el "
         "comando que se ejecuta. " + DOBLE,
         vivo="aún no. Tener abiertas dos terminales en proyecto-final/ y el contenedor de PostgreSQL arrancado.",
         pregunta="«¿Qué pieza del curso os costó más conectar con las demás?»",
         fuentes="QR de AI Engineer recibido de Laura el 19/10/2026 (Gmail 1a1533d7800144ad), el mismo que S16–S19, "
                 "sin modificar (SHA-256 29c9041e…). Laura pidió el QR «al inicio o al final de todas las» clases "
                 "(29/09/2026). " + LAURA,
         imagenes="QR de AI Engineer (material/S20/assets/qr-ai-engineer.jpg, copia byte a byte de material/S16/assets).")
    return sl


def _fuente(sl, x, y, w, h, icono, titulo, cuerpo, accent):
    box(sl, x, y, w, h, fill=CARD)
    box(sl, x, y, 3.5, h, fill=accent, radius=0)
    encajar(sl, icono, x + 14, y + (h - 30) / 2, 30, 30)
    text(sl, x + 56, y + 9, w - 66, 15, titulo, size=11, color=TITLE, bold=True)
    text(sl, x + 56, y + 27, w - 66, h - 32, cuerpo, size=9.5, color=TEXT)


def s03_caso(d):
    sl = d.slide(tag="caso")
    header(sl, "Caso conductor", "Un técnico, un ticket y tres fuentes de verdad",
           "Un técnico de soporte de AetherCloud (plataforma ficticia) pide ayuda con un ticket. Para contestar bien, el "
           "agente necesita tres fuentes distintas y no puede mezclarlas.")
    panel(sl, 43, 134, 420, 96, "La petición del técnico")
    text(sl, 55, 162, 396, 62,
         "«El ticket T-100 sigue abierto. Resume el problema, consulta la política aplicable y prepara una "
         "recomendación con fuentes. Si falta información pública, investígala.»",
         size=11.5, color=TITLE, font=SERIF, italic=True)
    _fuente(sl, 43, 242, 420, 66, "mcp-icon.png", "1 · Sistema de tickets → MCP",
            "Solo a través de un servidor MCP propio. T-100: abierto, plan Estándar, respuestas 429 en la carga "
            "nocturna.", BLOCK_COLORS[3])
    _fuente(sl, 43, 316, 420, 66, "g-document.png", "2 · Documentación interna → RAG",
            "Diez documentos ficticios de AetherCloud. La política de cuotas y del error 429 sale de aquí, con cita.",
            MINT)
    _fuente(sl, 43, 390, 420, 66, "g-globe.png", "3 · Información pública → Deep Research",
            "Lista blanca de fuentes: RFC 6585 (429) y RFC 9110 (Retry-After). Complementa; no sustituye.",
            BLOCK_COLORS[4])
    lineas = ['"herramientas": [',
              '    "consultar_ticket",',
              '    "buscar_documentacion",',
              '    "investigar"],',
              '"fuentes": [',
              '    "ticket:T-100",',
              '    "doc:03-limites-y-cuotas-api',
              '         § Respuesta ante exceso de cuota",',
              '    "web:rfc6585-429",',
              '    "web:rfc9110-retry-after"]']
    codigo(sl, 480, 134, 437, 198, lineas, "Lo que devuelve el agente · salida real", size=10.5)
    side_note(sl, 480, 344, 437, 112, "La regla",
              "Dato del ticket → solo del sistema de tickets. Política → solo de la documentación. Lo público "
              "complementa, pero nunca rellena una política que falte. Si falta una fuente, la respuesta lo dice: "
              "«no consta» o «informe parcial».", size=10.5)
    takeaway(sl, "Tres fuentes con su propio contrato: cada dato de la respuesta sabe de dónde viene.", "Idea guía")
    footer(sl)
    nota(sl, "18:33", "18:36",
         "leer la petición del técnico: es el caso que recorreremos toda la clase. Señalar las tres fuentes y por qué "
         "no se mezclan: el ticket es un dato de negocio con su propio sistema (no lo leemos de un archivo, lo pedimos "
         "por MCP); la política es interna y solo vale la documentación propia (RAG); lo público ayuda a explicar la "
         "tecnología (qué es un 429, cómo se usa Retry-After) pero nunca sustituye una política que no exista. A la "
         "derecha, la salida real del proyecto para este caso (perfil doble), después de que el ejecutor haya terminado "
         "la investigación: tres herramientas y cuatro fuentes identificadas. Los tickets son ficticios.",
         pregunta="«Si la documentación no dijera nada sobre el 429, ¿podría el agente usar la RFC como política?» "
                  "(No: diría que no consta en la documentación.)",
         fuentes="Caso definido en PLAN-S16-S20 (sección 7, «Caso y alcance»). Datos: proyecto-final/datos/tickets.json "
                 "y datos/corpus (copiado de 3-rag/lab/corpus/aethercloud-s10). " + EVIDENCIA,
         imagenes="Logotipo de MCP (repositorio modelcontextprotocol/modelcontextprotocol). Iconos genéricos de AWS "
                  "Architecture Icons (documento y globo).")
    return sl


def s04_piezas(d):
    sl = d.slide(tag="piezas")
    header(sl, "Proyecto final · qué pide el temario", "Cada pieza viene de una sesión que ya dimos",
           "Temario: «Integrar todo lo aprendido en un único proyecto». No hay tecnología nueva; lo nuevo es que todas "
           "las piezas tienen que funcionar juntas y poder comprobarse.")
    piezas = [
        ("g-source-code.png", "S2–S3", "Prompts y configuración", "prompts.py · config.py",
         "Prompt con versión; modelo y límites por variables."),
        ("langgraph-icon.png", "S5", "Construcción del grafo", "grafo.py",
         "Estado, nodos y el bucle agente ⇄ herramientas."),
        ("g-gear.png", "S4–S5", "Módulos y herramientas", "herramientas.py",
         "Tres herramientas con argumentos validados."),
        ("postgresql.png", "S9", "Integración con PostgreSQL", "almacen.py · esquema.sql",
         "Memoria, dueño del hilo, vectores y trabajos."),
        ("langfuse-icon.png", "S6", "Integración con Langfuse", "observabilidad.py",
         "Traza por turno y log JSON con request_id."),
        ("fastapi-icon.png", "S16", "Exposición vía FastAPI", "api.py",
         "Cuatro rutas, token de laboratorio y validación."),
        ("mcp-icon.png", "S15", "Integración con MCP", "servidor_mcp/tickets.py",
         "Servidor propio: una herramienta y un recurso."),
        ("g-magnifier.png", "S10–S12", "Deep Research + RAG", "investigacion.py · rag.py",
         "Investigación acotada y recuperación con cita."),
        ("aws-fargate.png", "S16–S17", "Despliegue en AWS", "Dockerfile · infra/",
         "ECS Fargate y RDS; imagen por digest."),
        ("g-json-script.png", "S18–S19", "Integración y entrega", "tests/ · cli.py",
         "Recorridos de aceptación y 43 tests."),
    ]
    w = (874 - 4 * 10) / 5
    for i, (ic, ses, tit, arch, desc) in enumerate(piezas):
        x = 43 + (i % 5) * (w + 10)
        y = 134 + (i // 5) * 166
        box(sl, x, y, w, 158, fill=CARD)
        encajar(sl, ic, x + 12, y + 12, 34, 34)
        chip(sl, x + w - 66, y + 14, 54, 18, ses, fill=TAKE_BG, color=MINT_L, size=8.5, line="2A5246")
        text(sl, x + 12, y + 54, w - 24, 30, tit, size=11, color=TITLE, bold=True)
        text(sl, x + 12, y + 86, w - 24, 26, arch, size=8.5, font=MONO, color=MINT_L, bold=True)
        text(sl, x + 12, y + 112, w - 24, 40, desc, size=9.5, color=TEXT)
    takeaway(sl, "El temario nombra diez piezas; el proyecto tiene un archivo corto y comentado para cada una.",
             "Idea guía")
    footer(sl, block=1)
    nota(sl, "18:36", "18:39",
         "BLOQUE 1 de 7 · Proyecto (18:36–18:45). Recorrer las diez piezas en el orden en que las nombra el temario y "
         "decir en voz alta de qué sesión viene cada una. Insistir en que el proyecto es deliberadamente pequeño (doce "
         "archivos de Python cortos) por la petición de la escuela de un repositorio menos denso: cada archivo empieza "
         "con un comentario que dice qué paso es. «Integración y entrega» (S18–S19) no es una tecnología: son las "
         "pruebas que demuestran que todo funciona junto.",
         pregunta="«¿Qué pieza creéis que es más difícil de integrar con las demás?»",
         fuentes=TEMARIO + " Correspondencia sesión–tema: GUIA-DE-CLASES-2026.md. " + LAURA,
         imagenes=LOGOS)
    return sl


def s05_planificar(d):
    sl = d.slide(tag="planificar")
    header(sl, "Introducción y planificación", "Antes de programar: requisitos, alcance y orden",
           "Planificar es decidir qué debe hacer el agente, qué no hará y cómo sabremos que funciona. Cada requisito "
           "funcional del proyecto tiene una comprobación automática con nombre propio.")
    y0 = panel(sl, 43, 134, 440, 330, "Requisitos funcionales · y su comprobación")
    reqs = [("Responder sin herramientas si no hacen falta", "directo_sin_herramientas"),
            ("Consultar un ticket a través de MCP", "ticket_por_mcp"),
            ("Decir que un ticket no existe", "inexistente_explicito"),
            ("Responder con cita de la documentación", "rag_con_cita"),
            ("Rechazar cuando no hay evidencia", "rechazo_sin_fuentes"),
            ("Investigar fuentes públicas sin duplicar", "investigacion_no_se_duplica"),
            ("Recordar la conversación tras reiniciar", "memoria_recuerda_ticket"),
            ("No enseñar un hilo a otro usuario", "aislamiento_entre_usuarios")]
    y = y0 + 2
    for i, (r, c) in enumerate(reqs, 1):
        badge(sl, 55, y + 4, i, fill=MINT, d=16, size=8.5)
        text(sl, 80, y + 1, 380, 15, r, size=10.5, color=TITLE)
        text(sl, 80, y + 18, 380, 12, c, size=8.5, font=MONO, color=MINT_L, bold=True)
        y += 37
    y1 = panel(sl, 495, 134, 422, 162, "Requisitos no funcionales", accent=BLUE)
    bullets(sl, 507, y1, 400, 126,
            ["Límites de herramientas, fuentes y tiempo escritos en el código.",
             "Trazabilidad: request_id, ruta y fuentes en cada respuesta.",
             "Reproducible: versiones fijadas en uv.lock y datos ficticios.",
             "Sin secretos en Git ni dentro de la imagen.",
             "Coste cero para practicar (perfil doble)."], size=10.5, mark_color=BLUE, space=6)
    y2 = panel(sl, 495, 306, 422, 158, "Fuera de alcance · extensiones posibles", accent=CORAL)
    bullets(sl, 507, y2, 400, 120,
            ["Interfaz web, voz y multimodal.", "Respuesta en streaming.", "Búsqueda web abierta.",
             "Autenticación real y multiusuario.", "Varios agentes coordinados."], size=10.5, mark_color=CORAL, space=6)
    takeaway(sl, "Si un requisito no tiene una prueba que lo compruebe, todavía no está terminado.", "Idea guía")
    footer(sl, block=1)
    nota(sl, "18:39", "18:42",
         "el temario empieza por «introducción al proyecto y planificación». Leer los ocho requisitos funcionales y "
         "señalar que cada uno tiene una comprobación con nombre (columna en verde): son exactamente las diez "
         "comprobaciones que imprime «agente.cli recorridos» (ocho requisitos, de los que el caso completo aporta "
         "tres comprobaciones). Los no funcionales son los que separan una demo de un sistema: límites, trazabilidad, "
         "reproducibilidad y secretos. Lo que queda fuera no es «menos importante»: es una extensión que no necesita "
         "el temario y que haría el proyecto inabarcable en el tiempo disponible.",
         pregunta="«¿Cuál de estos requisitos se suele olvidar en una demo?» (Normalmente el rechazo y el aislamiento.)",
         fuentes="Requisitos tomados de los criterios de cierre de S20 en PLAN-S16-S20 (sección 7) y de "
                 "proyecto-final/agente/cli.py (función recorridos). " + TEMARIO)
    return sl


def s06_arquitectura(d):
    sl = d.slide(tag="arquitectura")
    header(sl, "Arquitectura", "Un turno atraviesa cinco piezas y deja rastro en dos",
           "La API autentica y autoriza; el grafo decide; cada herramienta habla con su propia fuente; PostgreSQL guarda "
           "lo que debe sobrevivir a un reinicio y Langfuse, lo que ocurrió.")
    nodo(sl, 43, 180, 120, 52, "g-client.png", "Cliente", "curl o CLI")
    line(sl, 165, 206, 181, 206, color=MINT)
    nodo(sl, 183, 180, 134, 52, "fastapi-icon.png", "FastAPI", "token → usuario")
    line(sl, 319, 206, 333, 206, color=MINT)
    box(sl, 335, 160, 162, 92, fill=TAKE_BG, line="2A5246")
    encajar(sl, "langgraph-icon.png", 345, 170, 30, 30)
    text(sl, 383, 174, 110, 16, "Grafo LangGraph", size=10.5, color=TITLE, bold=True)
    text(sl, 345, 206, 146, 40, "inicio → agente ⇄ herramientas\ncerebro: modelo o doble", size=8.5, color=TEXT)
    herramientas = ["consultar_ticket", "buscar_documentacion", "investigar"]
    destinos = [("mcp-icon.png", "Servidor MCP", "tickets.json · stdio"),
                ("postgresql.png", "RAG · pgvector", "20 fragmentos con cita"),
                ("g-globe.png", "Ejecutor de trabajos", "lista blanca de fuentes")]
    for i, (h, (ic, t, s)) in enumerate(zip(herramientas, destinos)):
        y = 136 + i * 50
        line(sl, 499, 206, 523, y + 22, color=MINT, w=1.25)
        chip(sl, 525, y, 168, 44, h, fill=CARD2, color=MINT_L, size=9.5, font=MONO, radius=5, line=BORDER)
        line(sl, 695, y + 22, 713, y + 22, color=MINT, w=1.25)
        nodo(sl, 715, y, 202, 44, ic, t, s, icon_s=24)
    box(sl, 43, 300, 274, 62, fill=CARD, line=BORDER, dash=True)
    encajar(sl, "langfuse-icon.png", 53, 315, 32, 32)
    text(sl, 95, 310, 214, 16, "Langfuse · opcional", size=10.5, color=TITLE, bold=True)
    text(sl, 95, 328, 214, 30, "una traza por turno; log JSON siempre", size=9, color=TEXT)
    line(sl, 360, 254, 290, 298, color=MUTED, w=1, dash=True)
    line(sl, 430, 254, 430, 298, color=MINT, head="both")
    box(sl, 335, 300, 582, 62, fill=CARD, line=BORDER)
    encajar(sl, "postgresql.png", 345, 314, 32, 32)
    text(sl, 387, 308, 520, 14, "PostgreSQL · lo que debe sobrevivir a un reinicio", size=10, color=TITLE, bold=True)
    tablas = [("checkpoints", "memoria"), ("conversaciones", "dueño"), ("fragmentos", "vector 768"),
              ("trabajos", "investigaciones")]
    for i, (t, s) in enumerate(tablas):
        chip(sl, 387 + i * 130, 330, 124, 22, f"{t} · {s}", fill=CARD2, color=MINT_L, size=8.5, line=BORDER)
    box(sl, 43, 374, 874, 42, fill=CARD)
    for i, ic in enumerate(["aws-fargate.png", "aws-rds.png", "aws-secrets.png", "aws-cloudwatch.png"]):
        encajar(sl, ic, 53 + i * 32, 383, 24, 24)
    text(sl, 189, 374, 718, 42,
         [[("En AWS  ", {"bold": True, "color": TITLE}),
           ("la misma imagen en ECS Fargate (API y ejecutor), PostgreSQL en RDS privado, secretos en Secrets "
            "Manager y logs en CloudWatch.", {})]], size=10, color=TEXT, anchor="m")
    en_vivo(sl, 43, 426, 874, "uv run python -m agente.cli recorridos      →   \"todo_ok\": true · 10 de 10")
    takeaway(sl, "Cada flecha es un contrato: si falla una pieza, la respuesta lo dice en vez de inventar.",
             "Idea guía")
    footer(sl, block=1)
    nota(sl, "18:42", "18:45",
         "seguir el dibujo de izquierda a derecha con el caso de T-100: el cliente llama a FastAPI con un token; la API "
         "traduce el token a un usuario y comprueba que el hilo es suyo; el grafo decide qué herramientas usar; cada "
         "herramienta habla con su fuente (MCP para tickets, pgvector para la documentación, un trabajo en PostgreSQL "
         "para la investigación). Abajo, lo que persiste (cuatro familias de tablas) y la observabilidad. La franja de "
         "AWS adelanta el bloque 6: la arquitectura no cambia, cambia dónde se ejecuta.",
         vivo="uv sync; después «uv run python -m agente.cli recorridos». Señalar las diez comprobaciones en verde. "
              "Dura unos segundos y no necesita Docker (perfil doble, almacén en memoria).",
         pregunta="«¿Qué pieza tendríais que tocar para cambiar de proveedor de modelos?» (Solo la configuración.)",
         fuentes="proyecto-final/docs/arquitectura.md. PLAN-S16-S20, sección 7 («Arquitectura propuesta»). " + EVIDENCIA,
         imagenes=LOGOS + " " + AWS)
    return sl


PART1 = [s01_portada, s02_encuesta, s03_caso, s04_piezas, s05_planificar, s06_arquitectura]
