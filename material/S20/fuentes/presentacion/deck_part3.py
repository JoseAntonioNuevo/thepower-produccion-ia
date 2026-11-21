"""Diapositivas 13–18: bloque 4 (MCP y RAG) y bloque 5 (Deep Research)."""

from comun import EVIDENCIA, TEMARIO
from deck_lib import *  # noqa: F401,F403

MCP_SDK = ("SDK oficial de MCP para Python, versión 2.3.0 fijada en uv.lock: en la serie 2.x FastMCP pasa a llamarse "
           "MCPServer (from mcp.server.mcpserver import MCPServer); importar mcp.server.fastmcp falla con un mensaje "
           "que remite a la guía de migración (py.sdk.modelcontextprotocol.io/v2/migration). Comprobado en el entorno "
           "del proyecto el 16/11/2026.")
LOGO_MCP = "Logotipo de Model Context Protocol (repositorio modelcontextprotocol/modelcontextprotocol, docs/logo)."


def s13_mcp(d):
    sl = d.slide(tag="mcp")
    header(sl, "Integración con MCP", "Un servidor MCP propio para el sistema de tickets",
           "El agente no abre tickets.json: se lo pide a un servidor que habla Model Context Protocol. El servidor "
           "publica qué ofrece y con qué contrato; el agente lo descubre y lo usa.")
    nodo(sl, 43, 140, 220, 64, "langgraph-icon.png", "Agente · cliente MCP", "mcp_cliente.py", icon_s=32)
    line(sl, 265, 164, 455, 164, color=MINT, head="both")
    text(sl, 270, 144, 180, 14, "JSON-RPC por stdio", size=9, color=MINT, bold=True, align="c")
    text(sl, 270, 170, 180, 30, "initialize · tools/list\ntools/call · resources/read", size=8.5, font=MONO,
         color=MINT_L, align="c", bold=True)
    nodo(sl, 457, 140, 240, 64, "mcp-icon.png", "tickets-aethercloud", "servidor_mcp/tickets.py", icon_s=32,
         fill=TAKE_BG, line=MINT)
    line(sl, 699, 172, 727, 172, color=MINT)
    nodo(sl, 729, 140, 188, 64, "g-data-table.png", "tickets.json", "solo lectura · ficticio", icon_s=28)
    tarjetas = [("Herramienta · la invoca el modelo", "consultar_ticket(ticket_id)",
                 "El servidor valida el argumento con el patrón ^T-\\d{3}$ y devuelve una respuesta estructurada "
                 "con ok. Un ticket que no existe devuelve ok: false, no un error.", MINT),
                ("Recurso · lo lee la aplicación", "tickets://abiertos",
                 "Lista de tickets sin resolver (T-100 y T-200). Es contexto que la aplicación puede leer; no es una "
                 "acción que el modelo dispare.", BLUE)]
    for i, (lab, firma, cuerpo, acc) in enumerate(tarjetas):
        x = 43 + i * 444
        y0 = panel(sl, x, 216, 430, 116, lab, accent=acc)
        text(sl, x + 12, y0, 406, 16, firma, size=11, font=MONO, color=MINT_L, bold=True)
        text(sl, x + 12, y0 + 22, 406, 50, cuerpo, size=10, color=TEXT)
    codigo(sl, 43, 342, 874, 84,
           ['servidor = MCPServer("tickets-aethercloud", instructions="Consulta de tickets ficticios. Solo lectura.")',
            '@servidor.tool()',
            'def consultar_ticket(ticket_id: Annotated[str, Field(pattern=r"^T-\\d{3}$")]) -> dict: ...',
            '@servidor.resource("tickets://abiertos")'], None, size=9.5, pitch=16)
    en_vivo(sl, 43, 436, 874, "uv run python -m agente.cli mcp   →   [{\"nombre\": \"consultar_ticket\", … \"pattern\": \"^T-\\\\d{3}$\"}]")
    takeaway(sl, "MCP separa quién ofrece una capacidad de quién la usa: el servidor publica el contrato y el agente lo "
                 "descubre.", "Idea guía")
    footer(sl, block=4)
    nota(sl, "19:12", "19:17",
         "BLOQUE 4 de 7 · MCP y RAG (19:12–19:28). Temario: «integración con mcps». Repasar las dos primitivas de S15 "
         "que usamos: una herramienta (la invoca el modelo, con argumentos validados por el servidor) y un recurso "
         "(contexto que lee la aplicación). El transporte es stdio: el agente arranca el servidor como subproceso y "
         "hablan JSON-RPC por la entrada y salida estándar; por eso el servidor no puede usar print(). Ventaja frente "
         "a leer el JSON directamente: el sistema de tickets tiene su propio contrato y podría ser de otro equipo, "
         "otro lenguaje u otro servicio. Aviso práctico: quien use el SDK 2.x verá MCPServer, no FastMCP.",
         vivo="«uv run python -m agente.cli mcp» y abrir servidor_mcp/tickets.py. Opcional: «uv run python "
              "servidor_mcp/tickets.py» se queda esperando mensajes JSON-RPC (cortar con Ctrl+C).",
         pregunta="«¿Qué cambiaría en el agente si el servidor de tickets pasara a ser remoto?» (Solo el transporte "
                  "del cliente: Streamable HTTP en vez de stdio.)",
         fuentes=MCP_SDK + " " + TEMARIO,
         imagenes=LOGO_MCP + " Logotipo de LangGraph (repositorio langchain-ai/langgraph). Icono de tabla de datos: "
                  "AWS Architecture Icons (genéricos).")
    return sl


def s14_llamada(d):
    sl = d.slide(tag="llamada-mcp")
    header(sl, "Integración con MCP", "Qué ocurre en una llamada: descubrir, comprobar, llamar",
           "Cada llamada recorre el protocolo completo a la vista. Abrir un proceso por llamada es lento pero fácil de "
           "seguir; en producción se mantiene la sesión abierta o se usa un servidor remoto.")
    pasos = [("Arrancar el servidor como subproceso (stdio) e inicializar la sesión.", None),
             ("tools/list: descubrir qué herramientas publica y con qué esquema.", None),
             ("Comprobar nuestra lista blanca.", 'PERMITIDAS = {"consultar_ticket"}'),
             ("tools/call con un tiempo máximo.", "S20_MCP_TIMEOUT_S = 10"),
             ("Cualquier fallo se convierte en ErrorMCP: el grafo lo registra y sigue.", None)]
    y0 = panel(sl, 43, 134, 430, 292, "Cliente MCP del agente · mcp_cliente.py")
    y = y0 + 4
    for i, (t, c) in enumerate(pasos, 1):
        badge(sl, 55, y + 1, i, fill=MINT, d=18, size=9)
        text(sl, 83, y, 378, 32, t, size=11, color=TITLE)
        if c:
            text(sl, 83, y + 20, 378, 14, c, size=9.5, font=MONO, color=MINT_L, bold=True)
        y += 54 if c else 46
    filas = [["Llamada", "Resultado", "Lo decide"],
             ["consultar_ticket T-100", "ok: true y los datos", "servidor"],
             ["consultar_ticket T-999", "ok: false · no_encontrado", "servidor"],
             ["consultar_ticket T-1", "error de validación", "servidor (esquema)"],
             ["borrar_ticket", "no permitida; no sale del agente", "cliente (lista blanca)"],
             ["servidor colgado", "timeout → ErrorMCP", "cliente"]]
    table(sl, 487, 134, 430, [36, 40, 24], filas, size=9, row_h=24, font_cols={0: MONO}, colors={0: MINT_L},
          bold_cols=(0,))
    y1 = panel(sl, 487, 296, 430, 130, "Medido en local · 16/11/2026", accent=VIOLET)
    bullets(sl, 499, y1, 406, 96,
            ["≈ 0,25 s por llamada: casi todo es arrancar el proceso de Python.",
             "Descubrir herramientas: 0,29 s.",
             "6 tests con llamadas MCP reales por stdio (tests/test_mcp.py)."], size=10.5, mark_color=VIOLET, space=5)
    en_vivo(sl, 43, 436, 874, "chat \"¿Cómo está el ticket T-100?\"   ·   chat \"Consulta el ticket T-999\"   →   «…no existe en el sistema»",
            size=9)
    takeaway(sl, "La lista blanca está en el cliente: aunque el servidor publique más, el agente solo usa lo permitido.",
             "Idea guía")
    footer(sl, block=4)
    nota(sl, "19:17", "19:20",
         "recorrer los cinco pasos con el código de agente/mcp_cliente.py. Insistir en dos ideas de seguridad MCP "
         "vistas en S15: no confiar ciegamente en lo que publica un servidor (lista blanca en el cliente) y poner "
         "siempre un tiempo máximo. La tabla distingue quién decide cada resultado: el servidor valida argumentos y "
         "dice si el ticket existe; el cliente decide qué herramientas puede usar el agente. Los tiempos son de la "
         "prueba local (Mac, Python 3.12): orientativos, no un compromiso de rendimiento.",
         vivo="los dos chats de la franja. En el de T-999, señalar que la herramienta devolvió ok: false y que la "
              "respuesta lo dice sin inventar datos.",
         pregunta="«¿Por qué T-1 lo rechaza el servidor y borrar_ticket el cliente?»",
         fuentes="proyecto-final/agente/mcp_cliente.py y servidor_mcp/tickets.py; tests/test_mcp.py. Mediciones: "
                 "ejecución local del 16/11/2026 (descubrir 0,29 s; llamar 0,25 s). " + MCP_SDK,
         imagenes="sin imágenes externas: formas y tablas nativas.")
    return sl


def s15_ingesta(d):
    sl = d.slide(tag="ingesta")
    header(sl, "Deep Research + RAG · recuperación propia", "De documento a fragmento con cita",
           "La ingesta convierte cada sección de la documentación en un fragmento con identificador, título y sección: "
           "lo necesario para citarlo. Reingestar borra e inserta en una transacción, así que nunca duplica.")
    pasos = [("g-document.png", "10 documentos", "Markdown ficticios"),
             ("g-source-code.png", "Secciones «##»", "un trozo por sección"),
             ("g-data-table.png", "20 fragmentos", "id, título y sección"),
             ("g-sdk.png", "Embedding", "768 dimensiones"),
             ("postgresql.png", "pgvector", "HNSW · coseno")]
    for i, (ic, t, s) in enumerate(pasos):
        x = 43 + i * 178.5
        nodo(sl, x, 140, 160, 58, ic, t, s, icon_s=28)
        if i < len(pasos) - 1:
            line(sl, x + 162, 169, x + 176, 169, color=MINT)
    filas = ['fragmento_id  03-limites-y-cuotas-api#1',
             'titulo        Límites de tráfico y cuotas de API',
             'seccion       Cuotas por plan de suscripción',
             'contenido     La pasarela aplica control de tasa',
             '              … Plan Estándar: hasta 120',
             '              peticiones por minuto y 10',
             '              concurrentes …',
             'modelo        doble-hash-768',
             'embedding     vector(768)']
    codigo(sl, 43, 212, 430, 214, filas, "Un fragmento · tabla fragmentos", size=9.5, pitch=19)
    y0 = panel(sl, 487, 212, 430, 214, "Reglas de la ingesta")
    bullets(sl, 499, y0, 406, 176,
            ["Mismo modelo al indexar y al consultar: la búsqueda filtra por modelo y otro modelo no encuentra nada.",
             "Se vectoriza título + sección + contenido: el título da contexto al trozo.",
             "Un fragmento por sección: la cita apunta a un sitio que el técnico puede abrir.",
             "Perfil doble: el «embedding» es una bolsa de palabras; solo acierta si comparten palabras."],
            size=11, space=9)
    en_vivo(sl, 43, 436, 874, "uv run python -m agente.cli ingestar   (dos veces)   →   {\"documentos\": 10, \"fragmentos\": 20}")
    takeaway(sl, "Sin título y sección no hay cita; sin cita, el técnico no puede comprobar la respuesta.", "Idea guía")
    footer(sl, block=4)
    nota(sl, "19:20", "19:25",
         "temario: «Deep-research + RAG… combinadas con recuperación de información propia». Esta es la parte de "
         "recuperación propia: el RAG de S10 en pequeño. Seguir la tubería de arriba con el documento 03. Explicar por "
         "qué el fragmento guarda título, sección y modelo: el primero y el segundo hacen posible la cita; el modelo "
         "evita mezclar vectores de modelos distintos (un error silencioso: la búsqueda devolvería basura con buena "
         "puntuación). El corpus son los mismos diez documentos ficticios de AetherCloud de S10. Recordar que en el "
         "perfil doble no hay modelo de embeddings: con S20_PERFIL=real se usa gemini-embedding-2 a 768 dimensiones "
         "(no ejecutado en la preparación).",
         vivo="«uv run python -m agente.cli ingestar» dos veces (sigue en 20) y la consulta SQL de comandos.md para ver "
              "los fragment_id y las secciones.",
         pregunta="«¿Qué pasaría si indexáis con un modelo y consultáis con otro?»",
         fuentes="proyecto-final/agente/rag.py (fragmentar, ingestar) y esquema.sql; tests/test_rag.py. Corpus: "
                 "datos/corpus/PROCEDENCIA.md (copia de 3-rag/lab/corpus/aethercloud-s10). Modelo de embeddings del "
                 "perfil real: documentación de la Gemini API, «Embeddings» (ai.google.dev/gemini-api/docs/embeddings, "
                 "consultada el 16/11/2026).",
         imagenes="Logotipo de PostgreSQL (postgresql.org). Iconos genéricos de AWS Architecture Icons (documento, "
                  "código, tabla y SDK).")
    return sl


SIMILITUDES = [("Límite del plan Estándar", 0.404), ("Rollback en un canary", 0.357),
               ("Rotación de certificados", 0.302), ("Precio del plan Empresa", 0.232),
               ("Política de vacaciones", 0.192), ("Teletrabajo de empleados", 0.156),
               ("Soporte telefónico en Japón", 0.154), ("Tiempo en Madrid", 0.127)]
UMBRAL = 0.20


def s16_umbral(d):
    sl = d.slide(tag="umbral")
    header(sl, "Responder o rechazar", "Si el mejor fragmento no supera el umbral, no consta",
           "La recuperación siempre devuelve «el más parecido», aunque no tenga nada que ver. El umbral de evidencia "
           "convierte esa similitud en una decisión: responder con cita o decir que no consta.")
    y0 = panel(sl, 43, 134, 560, 292, "Similitud del mejor fragmento · valores medidos, perfil doble", accent=VIOLET)
    x0, ancho, escala = 225, 300, 300 / 0.45
    for i, (q, v) in enumerate(SIMILITUDES):
        y = y0 + 8 + i * 30
        responde = v >= UMBRAL
        text(sl, 55, y + 2, 166, 16, q, size=9.5, color=TITLE if responde else MUTED, align="r")
        box(sl, x0, y, ancho, 20, fill="14222A", radius=3)
        box(sl, x0, y, v * escala, 20, fill=MINT if responde else CORAL, radius=3)
        text(sl, max(x0 + v * escala, x0 + UMBRAL * escala + 2) + 6, y + 3, 60, 14, f"{v:.3f}".replace(".", ","),
             size=9, font=MONO,
             color=MINT_L if responde else CORAL, bold=True, check=False)
    xu = x0 + UMBRAL * escala
    line(sl, xu, y0 + 2, xu, y0 + 246, color=AMBER, w=1.5, head="none", dash=True)
    chip(sl, xu - 44, y0 + 248, 88, 16, "umbral 0,20", fill=AMBER, color=DARK, size=8, radius=3)
    text(sl, 55, y0 + 248, 150, 14, "responde", size=8.5, color=MINT, bold=True, check=False)
    text(sl, 120, y0 + 248, 80, 14, "rechaza", size=8.5, color=CORAL, bold=True, check=False)
    y1 = panel(sl, 617, 134, 300, 104, "Con evidencia · cita", fill=GREEN_BG, borde="2A5246")
    text(sl, 629, y1, 276, 70, "«Plan Estándar: hasta 120 peticiones por minuto…» "
                               "[03-limites-y-cuotas-api § Cuotas por plan de suscripción]", size=10.5, color=TITLE)
    y2 = panel(sl, 617, 246, 300, 82, "Sin evidencia · rechazo", accent=CORAL, fill=CORAL_BG, borde="5A3A32")
    text(sl, 629, y2, 276, 48, "«No consta en la documentación de AetherCloud: no puedo responder a eso con fuentes.»",
         size=10.5, color=TITLE)
    side_note(sl, 617, 336, 300, 90, "Margen estrecho",
              "0,232 frente a 0,192. Con un modelo real el umbral se vuelve a medir con preguntas reservadas (S19).",
              accent=AMBER, size=10.5)
    en_vivo(sl, 43, 436, 874, "chat \"¿Cuál es la política de teletrabajo de los empleados?\"   →   «No consta en la documentación…»")
    takeaway(sl, "«No consta» es una respuesta correcta; inventar con el fragmento más parecido no lo es.", "Idea guía")
    footer(sl, block=4)
    nota(sl, "19:25", "19:28",
         "la gráfica es real: similitud coseno del mejor fragmento para ocho preguntas, medida el 16/11/2026 con el "
         "perfil doble. Las cuatro primeras tienen respuesta en el corpus; las cuatro últimas no. Con el umbral 0,20 "
         "todas aciertan, pero el margen es pequeño (0,232 frente a 0,192): el doble es una bolsa de palabras y "
         "«política» o «plan» aparecen en sitios que no responden. Ese umbral se eligió mirando estas preguntas, así "
         "que no es una medición de calidad. Enlazar con S19: con un modelo real hay que elegir el umbral con un "
         "conjunto de validación y comprobarlo con preguntas que no se usaron para elegirlo.",
         vivo="la pregunta de teletrabajo («No consta») y, a continuación, la del plan Estándar (cita).",
         pregunta="«¿Qué es peor para un técnico de soporte: un “no consta” de más o una política inventada?»",
         fuentes="proyecto-final/agente/rag.py (recuperar) y config.py (S20_UMBRAL_EVIDENCIA = 0,20 en el perfil "
                 "doble). Valores: ejecución local del 16/11/2026. Material de S19 (material/S19) sobre umbrales con "
                 "validación. " + EVIDENCIA,
         imagenes="sin imágenes externas: gráfica de barras dibujada con formas nativas a partir de los valores medidos.")
    return sl


def s17_research(d):
    sl = d.slide(tag="research")
    header(sl, "Deep Research + RAG", "Investigar de forma autónoma, pero con límites",
           "La investigación planifica, busca, lee y extrae evidencia de fuentes públicas; la política interna sigue "
           "saliendo del RAG. El informe mantiene separados los dos orígenes y dice qué falta.")
    pasos = [("planificar", "divide el tema en consultas"), ("buscar", "solo en la lista blanca"),
             ("leer", "copia de aula o red"), ("extraer", "párrafos que responden"),
             ("verificar", "¿falta evidencia?"), ("informe", "completo o parcial")]
    w = (874 - 5 * 14) / 6
    for i, (t, s) in enumerate(pasos):
        x = 43 + i * (w + 14)
        box(sl, x, 134, w, 52, fill=CARD, line=BLOCK_COLORS[4] if i in (0, 5) else BORDER)
        text(sl, x + 10, 140, w - 20, 16, f"{i + 1} · {t}", size=10.5, color=TITLE, bold=True)
        text(sl, x + 10, 160, w - 20, 22, s, size=9, color=TEXT)
        if i < len(pasos) - 1:
            line(sl, x + w + 1, 160, x + w + 13, 160, color=BLOCK_COLORS[4])
    filas = [["Límite", "Valor"], ["Consultas por investigación", "3"], ["Fuentes leídas", "3"],
             ["Bytes por fuente", "1,5 MB"], ["Tiempo total", "30 s"], ["Llamadas al modelo", "0 doble · 1 real"]]
    table(sl, 43, 198, 300, [64, 36], filas, size=9.5, row_h=24, bold_cols=(0,))
    side_note(sl, 43, 354, 300, 72, "Por qué una lista blanca",
              "Reproducible y acotada. La búsqueda web abierta es una extensión.", accent=BLOCK_COLORS[4], size=10)
    y0 = panel(sl, 357, 198, 560, 228, "Informe real · tema «HTTP 429 Too Many Requests y cabecera Retry-After»",
               accent=BLUE)
    text(sl, 369, y0, 260, 12, "POLÍTICA INTERNA · RAG", size=8.5, color=MINT, bold=True)
    text(sl, 369, y0 + 15, 260, 96,
         "[03-limites-y-cuotas-api § Respuesta ante exceso de cuota] HTTP 429 con error_code RATE_LIMIT_EXCEEDED y "
         "cabecera Retry-After en segundos enteros.", size=10.5, color=TITLE)
    text(sl, 643, y0, 262, 12, "INFORMACIÓN PÚBLICA · LISTA BLANCA", size=8.5, color=BLUE, bold=True)
    text(sl, 643, y0 + 15, 262, 130,
         [{"runs": [("[rfc6585-429] ", {"bold": True, "color": BLUE}),
                    ("«The 429 status code indicates that the user has sent too many requests in a given amount of "
                     "time.»", {})], "space": 6},
          {"runs": [("[rfc9110-retry-after] ", {"bold": True, "color": BLUE}),
                    ('«Servers send the "Retry-After" header field to indicate how long the user agent ought to '
                     'wait…»', {})]}], size=10.5, color=TITLE, space=8)
    line(sl, 633, y0 + 2, 633, y0 + 150, color=BORDER, w=1, head="none")
    box(sl, 369, y0 + 158, 536, 32, fill="14222A", radius=4)
    text(sl, 379, y0 + 158, 520, 32, "estado: completo · faltan: [] · 2 fuentes · 520.105 bytes · 0,62 s · "
                                     "0 llamadas al modelo", size=9, font=MONO, color=MINT_L, bold=True, anchor="m")
    en_vivo(sl, 43, 436, 874, "S20_FUENTES=red uv run python -m agente.cli investigar   →   lee rfc-editor.org (solo la lista blanca)")
    takeaway(sl, "Un informe parcial que dice qué falta es mejor que uno completo inventado.", "Idea guía")
    footer(sl, block=5)
    nota(sl, "19:28", "19:33",
         "BLOQUE 5 de 7 · Deep Research (19:28–19:38). Temario: «Extensión del agente con capacidades de investigación "
         "autónoma combinadas con recuperación de información propia». Es el recorrido de S12 reducido a lo esencial y "
         "portado a Python: planificar consultas, buscar en una lista blanca, leer con límite de bytes, extraer los "
         "párrafos que responden, verificar si falta algo y redactar. En el perfil doble el informe usa una plantilla "
         "(0 llamadas); en el real, el modelo redacta una vez con las evidencias ya reunidas, sin navegar. El informe "
         "de la derecha es real: fuentes descargadas de rfc-editor.org el 17/11/2026 (S20_FUENTES=red); los extractos "
         "públicos se citan en su idioma original. Si una consulta no encuentra fuente, va a «faltan» y el informe "
         "sale parcial (hay un test).",
         vivo="solo si hay internet: «S20_FUENTES=red» con un trabajo pendiente (o «recorridos» con esa variable). "
              "Sin red, el mismo recorrido usa las copias de aula de datos/fuentes_publicas y da el mismo informe.",
         pregunta="«¿Qué haríais si la investigación encuentra una fuente pública que contradice la política "
                  "interna?» (Gana la política interna; la discrepancia se señala.)",
         fuentes=TEMARIO + " proyecto-final/agente/investigacion.py; datos/fuentes_publicas/catalogo.json. RFC 6585, "
                 "sección 4 (rfc-editor.org/rfc/rfc6585.txt) y RFC 9110, sección 10.2.3 (rfc-editor.org/rfc/rfc9110.txt). "
                 "Núcleo de investigación de S12: 3-rag/packages/research/src. Ejecución: evidencias/"
                 "recorridos-doble-postgres-red.json.",
         imagenes="sin imágenes externas: formas y tablas nativas.")
    return sl


def s18_trabajo(d):
    sl = d.slide(tag="trabajo")
    header(sl, "Deep Research + RAG", "La investigación es un trabajo con estado",
           "Investigar puede tardar más que una petición HTTP. El agente solo registra el trabajo; un ejecutor aparte lo "
           "termina y guarda el informe; volver a preguntar lee ese mismo trabajo.")
    chip(sl, 43, 156, 112, 30, "pendiente", fill=CARD2, color=TITLE, size=10, font=MONO, radius=5, line=BORDER)
    line(sl, 157, 171, 189, 171, color=BLOCK_COLORS[4])
    chip(sl, 191, 156, 112, 30, "en_curso", fill=CARD2, color=TITLE, size=10, font=MONO, radius=5, line=BORDER)
    for i, (e, f, c) in enumerate([("completo", GREEN_BG, MINT_L), ("parcial", AMBER_BG, AMBER),
                                   ("error", CORAL_BG, CORAL)]):
        y = 134 + i * 26
        line(sl, 305, 171, 339, y + 11, color=BLOCK_COLORS[4], w=1.25)
        chip(sl, 341, y, 100, 22, e, fill=f, color=c, size=9.5, font=MONO, radius=4)
    text(sl, 43, 192, 140, 24, "lo registra el agente", size=8.5, color=MUTED)
    text(sl, 191, 192, 140, 24, "lo toma el ejecutor\n(SKIP LOCKED)", size=8.5, color=MUTED)
    y0 = panel(sl, 467, 134, 450, 86, "Idempotencia", accent=BLOCK_COLORS[4])
    text(sl, 479, y0, 426, 14, "clave = sha256(thread_id | tema normalizado)", size=9.5, font=MONO, color=MINT_L,
         bold=True)
    text(sl, 479, y0 + 18, 426, 32, "Misma conversación y mismo tema = mismo trabajo. UNIQUE(clave) en PostgreSQL.",
         size=9.5, color=TEXT)
    filas = [["Paso", "Comando", "Salida real"],
             ["1 · Turno del agente", 'chat "$CASO" --thread caso', "«He registrado la investigación INV-b6055bd5 "
                                                                    "(estado: pendiente).»"],
             ["2 · Ejecutor", "agente.cli investigar", '{"procesados": ["INV-b6055bd5"]}'],
             ["3 · Misma pregunta", 'chat "$CASO" --thread caso', "«Investigación INV-b6055bd5 (completo): … "
                                                                  "[rfc6585-429] … [rfc9110-retry-after]»"],
             ["4 · Ejecutor otra vez", "agente.cli investigar", '{"procesados": []} · no se duplica']]
    table(sl, 43, 232, 874, [17, 27, 56], filas, size=9.5, row_h=36, bold_cols=(0, 1), font_cols={1: MONO},
          colors={1: MINT_L})
    en_vivo(sl, 43, 436, 874, "CASO=\"El ticket T-100 sigue abierto…\"  ·  chat  ·  investigar  ·  chat  ·  investigar --ver INV-…",
            size=9)
    takeaway(sl, "Consultar el estado solo lee: repetir la petición nunca paga dos veces el mismo trabajo.", "Idea guía")
    footer(sl, block=5)
    nota(sl, "19:33", "19:38",
         "por qué un trabajo y no una llamada dentro de la petición: una investigación real puede durar más que el "
         "plazo de una API (recordar los 30 s de HTTP API en S17) y, si el proceso se reinicia, una tarea en memoria "
         "se pierde. Aquí el estado vive en la tabla trabajos. El ejecutor toma pendientes con FOR UPDATE SKIP LOCKED: "
         "dos ejecutores no toman el mismo (test test_dos_ejecutores_no_toman_el_mismo_trabajo). La clave idempotente "
         "evita pagar dos veces la misma investigación. Las salidas de la tabla son de la ejecución local del 16/11 "
         "(el identificador INV-… cambia en cada ejecución). En AWS el ejecutor es el segundo contenedor de la tarea.",
         vivo="los cuatro pasos de comandos.md (diapositiva 18) con S20_ALMACEN=postgres. Terminar con "
              "«investigar --ver INV-…» para enseñar el informe completo con consumo y límites.",
         pregunta="«¿Qué pasa si el ejecutor se cae a mitad de un trabajo?» (Queda en_curso: hace falta un plazo y un "
                  "reintento; es una mejora pendiente, no está implementada.)",
         fuentes="proyecto-final/agente/almacen.py (crear_trabajo, tomar_pendiente), investigacion.py "
                 "(procesar_pendientes) y esquema.sql; tests/test_investigacion.py y test_postgres.py. Decisión de "
                 "diseño: PLAN-S16-S20, sección 7, punto 7. " + EVIDENCIA,
         imagenes="sin imágenes externas: formas y tablas nativas.")
    return sl


PART3 = [s13_mcp, s14_llamada, s15_ingesta, s16_umbral, s17_research, s18_trabajo]
