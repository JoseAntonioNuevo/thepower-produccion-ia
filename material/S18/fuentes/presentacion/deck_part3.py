"""Diapositivas 30–40: bloque 5 (observabilidad, APM, error tracking y rollback), bloque 6 (migraciones y backups) y bloque 7 (práctica y cierre)."""
from deck_lib import *  # noqa: F401,F403

SRC_AWS = ("Iconos de AWS: AWS Architecture Icons, paquete oficial del 31/07/2026 "
           "(aws.amazon.com/architecture/icons).")


def s22_observabilidad(d):
    sl = d.slide(tag="observabilidad")
    header(sl, "Observabilidad", "Logs, métricas, trazas y errores responden preguntas distintas",
           "Monitorizar no es solo mirar logs. Las métricas avisan de que algo va mal, los logs explican una petición, "
           "las trazas muestran dónde se va el tiempo y el error tracking agrupa los fallos.")
    cards = [("r-cw-logs.png", "Logging", BLUE, "¿Qué pasó en esta petición?",
              "Una línea JSON por petición en CloudWatch Logs.", "CloudWatch Logs · Cloud Logging · Loki", True),
             ("g-metrics.png", "Monitoring y métricas", BLUE, "¿Cómo va el servicio: errores, latencia, tráfico?",
              "Métricas extraídas de los logs, panel y una alarma.", "CloudWatch · Prometheus y Grafana · Azure Monitor", True),
             ("gh-opentelemetry.png", "APM y trazas", MUTED, "¿En qué servicio o llamada se va el tiempo?",
              "proveedor_ms frente a duracion_ms. Cascada ilustrativa en la 32; no integramos trazas.",
              "OpenTelemetry · CloudWatch Application Signals · X-Ray · Application Insights", False),
             ("g-alert.png", "Error tracking", MUTED, "¿Qué errores hay, desde cuándo y a cuántos afecta?",
              "Log de excepción y alarma de 5xx. Agrupación al estilo Sentry en la 34; no se integra.",
              "Sentry · Rollbar · Application Insights", False)]
    cw, ch = (874 - 12) / 2, 160
    for i, (ic, t, col, q, demo, tools, done) in enumerate(cards):
        x = 43 + (i % 2) * (cw + 12)
        y = 134 + (i // 2) * (ch + 10)
        box(sl, x, y, cw, ch, fill=CARD, line=BLUE if done else None)
        img(sl, ic, x + 12, y + 12, w=34, h=34)
        text(sl, x + 56, y + 12, cw - 180, 18, t, size=13, font=SERIF, color=TITLE)
        chip_tag(sl, x + cw - 124, y + 13, "EN LA DEMO" if done else "SE EXPLICA", kind="info" if done else "warn", w=112)
        text(sl, x + 56, y + 32, cw - 68, 16, q, size=10.5, color=BLUE if done else AMBER, bold=True)
        text(sl, x + 14, y + 62, cw - 28, 14, "EN LA DEMO", size=8, color=MUTED, bold=True)
        text(sl, x + 14, y + 76, cw - 28, 30, demo, size=9.5, color=TEXT)
        text(sl, x + 14, y + 110, cw - 28, 14, "HERRAMIENTAS", size=8, color=MUTED, bold=True)
        text(sl, x + 14, y + 124, cw - 28, 30, tools, size=9.5, color=TITLE)
    takeaway(sl, "La demo implementa logs y métricas; APM y error tracking se explican, no se presentan como integrados.",
             label="Idea guía", lab_color=BLUE)
    footer(sl, block=5)
    notes(sl, f"""
19:34–19:35. Temario: «Logging, monitoring y APM / Error tracking». Un minuto: es el mapa del bloque; APM tiene su cascada en la 32 y error tracking su incidencia agrupada en la 34. Cuatro preguntas. Logging: el detalle de un evento (una petición). Monitoring: series numéricas agregadas (tasa de errores, latencia p95, tráfico) con paneles y alarmas. APM (Application Performance Monitoring) y trazas distribuidas: una petición que pasa por varios servicios se ve como un árbol de spans con su duración; el estándar abierto es OpenTelemetry; en AWS, CloudWatch Application Signals recoge métricas y trazas de aplicaciones en EC2, ECS y Lambda. Error tracking: agrupa excepciones iguales, cuenta usuarios afectados y avisa (Sentry tiene integración para FastAPI con sentry_sdk.init(dsn=…)).
En la demo: logs + métricas + alarma. Una aproximación de APM: proveedor_ms frente a duracion_ms separa nuestro tiempo del del modelo. No integramos OpenTelemetry ni Sentry: no se presentan como hechos.
Distinguir también de las trazas semánticas de LLM (Langfuse y similares: prompts, tokens, evaluación) que se ven en S19.
En vivo: nada; conceptual.
Pregunta: «La latencia p95 se ha duplicado. ¿Qué herramienta abrís primero?».
Fuentes: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Monitoring-Sections.html · https://docs.sentry.io/platforms/python/integrations/fastapi/ (16/11/2026). {SRC_AWS} OpenTelemetry: logotipo de github/explore.""")
    return sl


def s23_log(d):
    sl = d.slide(tag="log")
    header(sl, "Logging estructurado", "Una línea JSON por petición, pensada para buscar",
           "Cada petición escribe un objeto JSON en la salida estándar y Fargate lo envía a CloudWatch Logs. Con campos "
           "fijos se puede filtrar, agrupar y convertir en métricas sin expresiones regulares.")
    section_label(sl, 43, 134, 300, "La línea que escribió la versión B", color=BLUE)
    tag(sl, 360, 132, "real", w=172)
    box(sl, 43, 151, 520, 196, fill="0B1418", line=BORDER, radius=4)
    js = [('{"ts": "2026-11-17T09:37:10.614+00:00",', TEXT),
          (' "nivel": "ERROR", "evento": "peticion",', TEXT),
          (' "request_id": "aaf20664-36dc-4102-a9d3-b392dda9189c",', MINT_L),
          (' "version": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",', MINT_L),
          (' "metodo": "POST", "ruta": "/clasificar",', MINT_L),
          (' "estado": 500, "duracion_ms": 1.0,', MINT_L),
          (' "modo": "demo", "proveedor_ms": 0.0,', MINT_L),
          (' "categoria": "consulta", "prioridad": "baja"}', TEXT)]
    pitch = 21
    text(sl, 55, 162, 470, pitch * 8 + 6, [[(t, {"color": c})] for t, c in js], size=9, font=MONO, check=False,
         lsp=Pt(pitch))
    for li, n in [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)]:
        line_badge(sl, 538, 169, pitch, li, n, BLUE)
    legend = [("request_id", "Lo genera el servidor y vuelve al cliente en la cabecera x-request-id: une cliente, log y error."),
              ("version", "El commit con el que se construyó la imagen. Aquí, la versión ficticia del ensayo."),
              ("ruta", "La plantilla de la ruta, no la URL recibida: acota lo que se escribe."),
              ("estado y duracion_ms", "La base de las métricas de errores y de latencia."),
              ("proveedor_ms", "El tiempo del modelo aparte del total: distingue nuestra API del proveedor.")]
    y = 151
    for i, (t, b) in enumerate(legend, 1):
        box(sl, 577, y, 340, 36.4, fill=CARD)
        badge(sl, 585, y + 10, i, fill=BLUE, d=16, size=8.5)
        text(sl, 608, y + 3, 302, 32, [[(t + "  ", {"bold": True, "color": TITLE, "font": MONO, "size": 8.5}), (b, {})]],
             size=8.5, color=TEXT)
        y += 40
    side_note(sl, 43, 361, 431, 104, "Lo que nunca se registra",
              "El texto de la incidencia, cabeceras Authorization, claves, el cuerpo que devuelve el proveedor ni datos "
              "personales. Un test comprueba que el texto del usuario no aparece en el log.", accent=CORAL, size=9.5)
    side_note(sl, 486, 361, 431, 104, "Retención y coste",
              "Staging guarda 7 días. La capa gratuita de CloudWatch incluye 5 GB de logs al mes (ingesta, archivo y "
              "datos analizados por consultas); después se paga por GB. Un log por petición, sin cuerpos, cabe de sobra.",
              accent=BLUE, size=9.5)
    takeaway(sl, "Si un log no lleva request_id y versión, sabrás que algo falló, pero no qué petición ni qué código.",
             label="Idea guía", lab_color=BLUE)
    footer(sl, block=5)
    notes(sl, f"""
19:35–19:37. app.py: la función registrar() escribe una línea JSON (json.dumps) en stdout con flush; el middleware observar() genera un uuid4 por petición, lo devuelve en la cabecera x-request-id y escribe al final una línea «peticion» con versión, método, ruta (plantilla de FastAPI), estado, duración y, para /clasificar, proveedor_ms, categoría y prioridad. Las excepciones no previstas escriben además una línea «excepcion» con el tipo y la traza (limitada a 6 marcos); el cliente solo recibe error_interno y el request_id.
El driver awslogs de ECS envía stdout al grupo /thepower/<lab> (modo non-blocking con búfer de 1 MB: si CloudWatch no responde, la app no se bloquea, aunque se podrían perder líneas).
La línea es real (ensayo local del 17/11/2026 con APP_VERSION ficticia bbbb…).
Coste: capa gratuita de CloudWatch, 5 GB de datos de logs al mes (ingesta, almacenamiento de archivo y datos escaneados por Logs Insights), según la página de precios consultada el 16/11/2026.
En vivo: docker logs del contenedor local tras una petición.
Pregunta: «¿Por qué registramos la plantilla de la ruta y no la URL completa?».
Fuentes: demo-cicd/app.py (registrar, observar); tests/test_api.py (test_el_log_identifica_la_peticion_y_no_contiene_el_texto); https://aws.amazon.com/cloudwatch/pricing/ (16/11/2026); .build/s18/ensayo/logs-B.txt.""")
    return sl


def s23a_apm(d):
    sl = d.slide(tag="apm")
    header(sl, "APM · trazas distribuidas", "Una traza dibuja dónde se va el tiempo de una petición",
           "Cada operación es un span con inicio y duración; todos los spans de una petición comparten el mismo trace_id. "
           "La cascada separa lo que tarda nuestra API de lo que tarda el proveedor del modelo.")
    section_label(sl, 43, 134, 380, "Una petición a /clasificar, en cascada", color=BLUE)
    tag(sl, 433, 132, "ilustrativo", w=200, t="ESQUEMA · VALORES ILUSTRATIVOS")
    box(sl, 43, 151, 590, 228, fill=CARD, line=BORDER)
    text(sl, 55, 160, 566, 13, [[("trace_id  ", {"color": MUTED, "bold": True, "font": SANS, "size": 8}),
                                 ("4bf92f3577b34da6a3ce929d0e0e4736", {"color": MINT_L}),
                                 ("   5 spans · 2.400 ms", {"color": MUTED, "font": SANS})]],
         size=9, font=MONO, bold=True, check=False)
    # eje de tiempo: 0–2.400 ms en la franja x0..x1; columna de duraciones a la derecha
    X0, X1, Y0 = 262, 548, 182
    k = (X1 - X0) / 2400
    for ms in (0, 600, 1200, 1800, 2400):
        x = X0 + ms * k
        line(sl, x, Y0 + 14, x, 336, color=BORDER, w=0.5, head="none", dash=True)
        text(sl, x - 30, Y0, 60, 11, f"{ms:,} ms".replace(",", "."), size=7.5, color=FAINT, align="c", check=False)
    text(sl, 558, Y0, 66, 11, "DURACIÓN", size=7.5, color=FAINT, bold=True, align="r", check=False)
    spans = [("POST /clasificar", "servidor · FastAPI", 0, 2400, BLUE, BLUE_BG, 0),
             ("validar entrada", "Pydantic", 3, 6, MUTED, CARD2, 1),
             ("POST openrouter.ai/…/responses", "cliente · httpx · openai/gpt-6-luna", 8, 2378, CORAL, CORAL_BG, 1),
             ("validar salida", "Clasificacion", 2380, 2384, MUTED, CARD2, 1),
             ("escribir log y responder", "registrar()", 2386, 2392, MUTED, CARD2, 1)]
    y = Y0 + 17
    for name, sub, a, b, col, fill, lvl in spans:
        nx = 55 + lvl * 12
        if lvl:
            line(sl, 59, y - 6, 59, y + 10, color=BORDER, w=0.75, head="none")
            line(sl, 59, y + 10, nx - 2, y + 10, color=BORDER, w=0.75, head="none")
        text(sl, nx, y + 1, X0 - nx - 8, 12, name, size=8.5, color=CORAL if col == CORAL else TITLE, bold=True,
             font=MONO, check=False)
        text(sl, nx, y + 14, X0 - nx - 8, 11, sub, size=7.5, color=MUTED, check=False)
        bx = X0 + a * k
        bw = max(3, (b - a) * k)
        box(sl, bx, y + 4, bw, 18, fill=fill, line=col, radius=2)
        dur = b - a
        text(sl, 558, y + 7, 66, 12, f"{dur:,} ms".replace(",", "."), size=9, color=CORAL if col == CORAL else TITLE,
             bold=True, align="r", check=False)
        y += 28
    # el cuello de botella, rotulado sobre su barra
    text(sl, X0 + 30, Y0 + 17 + 2 * 28 + 7, 230, 12, "99 % del tiempo · cuello de botella", size=8.5, color=CORAL,
         bold=True, check=False)
    text(sl, 55, 344, 566, 26, [[("Enlace con el log (31): ", {"bold": True, "color": TITLE}),
                                 ("duracion_ms = span raíz (2.400) · proveedor_ms = span del proveedor (2.370). La traza "
                                  "añade los tramos intermedios y el orden.", {})]], size=8.5, color=TEXT)
    side_note(sl, 43, 389, 590, 76, "Qué haríamos con este cuello de botella",
              "Optimizar nuestra API ahorraría como mucho 30 ms. Para reducir la latencia: un modelo o ruta más rápidos, "
              "menos tokens de salida o caché. Un timeout acota la espera si el proveedor se atasca.",
              accent=CORAL, size=9.5)
    section_label(sl, 649, 134, 268, "trace_id frente a request_id", color=BLUE)
    ids = [("request_id", "EN LA DEMO", "info",
            "Lo crea nuestra API (uuid4) y vuelve al cliente en x-request-id. Une el error del cliente con las líneas "
            "de log de una petición, en un servicio."),
           ("trace_id", "SE EXPLICA", "warn",
            "32 hex (16 bytes). Lo crea el primer servicio y viaja a los siguientes en la cabecera traceparent (W3C). "
            "Agrupa los spans de todos los servicios.")]
    y = 151
    for t, lab, kind, b in ids:
        box(sl, 649, y, 268, 96, fill=CARD, line=BLUE if kind == "info" else None)
        text(sl, 661, y + 10, 150, 16, t, size=12, font=MONO, color=TITLE, bold=True)
        chip_tag(sl, 819, y + 10, lab, kind=kind, w=86)
        text(sl, 661, y + 34, 246, 58, b, size=9.5, color=TEXT)
        y += 104
    box(sl, 649, 359, 268, 106, fill=CARD)
    img(sl, "gh-opentelemetry.png", 659, 369, w=26, h=26)
    text(sl, 693, 369, 214, 14, "Cómo se integraría", size=10, color=TITLE, bold=True)
    text(sl, 693, 386, 216, 74, "OpenTelemetry instrumenta FastAPI y httpx y exporta los spans a X-Ray, Application "
         "Signals, Jaeger o Sentry. Con trace_id en cada log se salta del log a la traza.", size=9, color=TEXT)
    takeaway(sl, "El log dice cuánto tardó la petición; la traza dice en qué tramo. Si el 99 % es el proveedor, no toques la API.",
             label="Idea guía", lab_color=BLUE)
    footer(sl, block=5)
    notes(sl, f"""
19:37–19:40. Temario: «Logging, monitoring y APM». APM (Application Performance Monitoring) con trazas distribuidas: una traza es el recorrido de una petición; cada operación es un span con nombre, inicio, duración, atributos y el span padre. Según la especificación de OpenTelemetry, el TraceId identifica la traza (16 bytes, 32 hexadecimales) y el SpanId cada span (8 bytes); el primero viaja entre servicios en la cabecera traceparent del estándar W3C Trace Context.
Leer la cascada de arriba abajo: el span raíz (servidor, FastAPI) dura 2.400 ms; dentro, validar la entrada (3 ms), la llamada a OpenRouter Responses con el modelo del caso conductor (openai/gpt-6-luna por la ruta openai/fast: 2.370 ms), validar la salida (4 ms) y registrar y responder (6 ms). El proveedor es el 99 %: ese es el cuello de botella. El lado del proveedor es una caja negra: solo vemos nuestro span cliente.
Los valores son ilustrativos (no medidos): la demo no integra OpenTelemetry ni trazas. El trace_id es el ejemplo de la especificación W3C. Lo que sí es real es la aproximación del log: duracion_ms y proveedor_ms (diapositiva 31) separan ya esos dos tiempos.
trace_id frente a request_id: request_id lo crea nuestra API y une log, error y cliente dentro de un servicio; trace_id une spans de varios servicios. Lo habitual es registrar los dos en cada línea de log.
Integración (no hecha): paquetes de instrumentación de OpenTelemetry para FastAPI y httpx, exportador OTLP hacia X-Ray/CloudWatch Application Signals, Jaeger o Sentry (sentry_sdk con traces_sample_rate).
En vivo: nada; conceptual.
Pregunta: «Si la traza dijera que el 70 % es validar la salida, ¿qué cambiaríais?».
Fuentes: https://opentelemetry.io/docs/concepts/signals/traces/ · https://opentelemetry.io/docs/specs/otel/overview/ · https://www.w3.org/TR/trace-context/ · https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Monitoring-Sections.html (consultadas con Context7 el 17/11/2026; copias en .build/s18/investigacion/ctx7-otel-*.txt); demo-cicd/app.py (ProveedorOpenRouter, proveedor_ms). OpenTelemetry: logotipo de github/explore.""")
    return sl


def s24_error(d):
    sl = d.slide(tag="demo-error")
    header(sl, "Demo 4 · el fallo que los tests no cubrían", "Del request_id que ve el cliente a la causa en el log",
           "En staging, B responde 500 a una consulta de prioridad baja: a SLA_HORAS le falta esa clave. El cliente solo "
           "recibe un identificador; con él encontramos la causa sin exponer detalles internos.")
    tag(sl, 745, 132, "real", w=172)
    cols = [("1", "El cliente", "g-client.png", [
                "$ curl -X POST …/clasificar \\",
                "  -d '{\"texto\":\"Tengo una duda",
                "       sobre los horarios\"}'",
                "",
                '{"error": "error_interno",',
                ' "request_id": "aaf20664-36dc-…"}'],
             "Ni traza ni detalles: solo el código y el identificador."),
            ("2", "La búsqueda", "r-cw-logs.png", [
                "$ aws logs filter-log-events \\",
                '  --log-group-name /thepower/$LAB \\',
                "  --filter-pattern \\",
                "  '{ $.request_id =",
                '     "aaf20664-36dc-…" }\''],
             "Local: docker logs api | grep aaf20664"),
            ("3", "La causa", "g-magnifier.png", [
                '"evento": "excepcion",',
                '"version": "bbbbbbbb…",',
                '"error_tipo": "KeyError",',
                '"traza": "… KeyError: \'baja\'"',
                "",
                '"evento": "peticion",',
                '"estado": 500, "prioridad": "baja"'],
             "Dos líneas con el mismo request_id: qué falló y en qué versión (ficticia en el ensayo local).")]
    cw = (874 - 2 * 14) / 3
    for i, (n, t, ic, code, b) in enumerate(cols):
        x = 43 + i * (cw + 14)
        box(sl, x, 151, cw, 210, fill=CARD)
        badge(sl, x + 9, 159, n, fill=BLUE, d=16, size=8.5)
        img(sl, ic, x + 31, 156, w=22, h=22)
        text(sl, x + 60, 159, cw - 70, 16, t, size=11, color=TITLE, bold=True)
        code_panel(sl, x + 9, 186, cw - 18, 126, code, size=8.3, color=MINT_L if i else TEXT, fill="0B1418")
        text(sl, x + 10, 320, cw - 20, 38, b, size=9, color=TEXT)
        if i < 2:
            line(sl, x + cw + 2, 256, x + cw + 12, 256, color=BLUE, w=1.5)
    side_note(sl, 43, 373, 431, 92, "Por qué pasó",
              "El test de B solo comprobaba la prioridad media, y el smoke usa una incidencia de acceso (media). Nadie "
              "probó «baja»: los tests solo detectan lo que describen.", accent=CORAL, size=9.5)
    side_note(sl, 486, 373, 431, 92, "Qué hacemos ahora",
              "1 Volver a A con su digest: minutos y sin tocar código. 2 Escribir el test que faltaba. "
              "3 Corregir, pasar por la PR y publicar una versión C.", accent=MINT, size=9.5)
    takeaway(sl, "El cliente recibe un request_id y nada interno; nosotros, con ese id, llegamos a la línea exacta y a la versión.",
             label="Idea guía", lab_color=BLUE)
    footer(sl, block=5)
    notes(sl, """
19:40–19:43. Cuarto momento de demo. El enunciado: «Localiza un error de prueba». Reproducir: curl a /clasificar con «Tengo una duda sobre los horarios» → las reglas del modo demo dan categoría consulta y prioridad baja → SLA_HORAS["baja"] lanza KeyError → el middleware registra «excepcion» con la traza y responde 500 con error_interno y request_id.
Buscar en CloudWatch con un filtro JSON por request_id (sintaxis de filtros de CloudWatch: { $.campo = "valor" }), o en Logs Insights: filter request_id = "…". Local: docker logs api | grep <id>.
Valores reales del ensayo local del 17/11/2026 (request_id aaf20664-…, versión ficticia bbbb…, KeyError: 'baja'); en staging los identificadores serán otros.
En vivo · GitHub/AWS: comandos.md, diapositiva 33. Local: contenedor s18:B en 127.0.0.1:8000.
Pregunta: «¿Qué habría pasado si el error devolviera la traza al cliente?» (expondríamos código y rutas internas; por eso solo request_id).
Fuentes: demo-cicd/app.py (middleware observar); https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntaxForMetricFilters.html (16/11/2026); .build/s18/ensayo/logs-B.txt. Iconos: AWS Architecture Icons (Logs, Client, Magnifying Glass).""")
    return sl


def s24a_error_tracking(d):
    sl = d.slide(tag="error-tracking")
    header(sl, "Error tracking", "Los eventos iguales se agrupan en una sola incidencia",
           "Un error tracker como Sentry recibe cada excepción como un evento, le calcula una huella (fingerprint) con el "
           "tipo y la traza, y junta los de la misma huella en una incidencia con su frecuencia, usuarios y release.")
    section_label(sl, 43, 134, 330, "Eventos  →  huella  →  incidencia", color=BLUE)
    esquema_label(sl, 627, 132, w=290, t="ESQUEMA · no es una captura de Sentry · valores ilustrativos")
    evs = [("19:36:12", "aaf20664…"), ("19:35:40", "3e91c0d2…"), ("19:31:05", "0b7d55e1…")]
    y = 151
    for hora, rid in evs:
        box(sl, 43, y, 196, 50, fill=CARD, line=BORDER)
        text(sl, 51, y + 6, 182, 12, [[("evento  ", {"color": MUTED, "bold": True, "size": 7.5}), (hora, {})]],
             size=8.5, color=TITLE, check=False)
        text(sl, 51, y + 20, 182, 12, f"request_id {rid}", size=8.6, font=MONO, color=MINT_L, bold=True, check=False)
        text(sl, 51, y + 34, 182, 12, "KeyError: 'baja' · release B", size=8.6, font=MONO, color=CORAL, bold=True, check=False)
        line(sl, 240, y + 25, 262, 248, color=BLUE, w=1.25)
        y += 57
    text(sl, 43, 323, 196, 14, "… y 211 eventos más", size=9, color=MUTED, bold=True, align="c")
    box(sl, 264, 196, 112, 104, fill=BLUE_BG, line=BLUE)
    text(sl, 272, 204, 96, 12, "HUELLA", size=8.5, color=BLUE, bold=True, align="c")
    text(sl, 272, 220, 96, 46, "tipo KeyError\n+ marcos de la traza\n(app.py · clasificar)", size=8.5, color=TITLE,
         align="c")
    text(sl, 272, 270, 96, 24, "misma huella =\nmisma incidencia", size=8.6, color=MUTED, align="c")
    line(sl, 377, 248, 395, 248, color=BLUE, w=1.5)
    side_note(sl, 43, 345, 333, 70, "Qué añade a nuestros logs",
              "Los logs guardan 214 excepciones; el tracker muestra una incidencia: desde cuándo, a cuántos usuarios y "
              "qué release la trajo. Si vuelve tras resolverla en C, es una regresión.", accent=BLUE, size=9)
    code_panel(sl, 43, 421, 333, 44, ["# solo configuración · ejemplo de Sentry",
                                      "sentry_sdk.init(dsn=SENTRY_DSN,",
                                      '  release=APP_VERSION, environment="staging")'],
               size=8.5, fill="0B1418", line=BORDER, pad=7)
    # panel claro: la incidencia
    px, py, pw, ph = 397, 151, 520, 314
    box(sl, px, py, pw, ph, fill=UI_BG, line="AEB5BD", radius=4)
    box(sl, px, py, pw, 18, fill=UI_NAV, radius=0)
    text(sl, px + 8, py + 3, pw - 16, 12, "Error tracking (p. ej. Sentry) › Incidencias › s18-api · staging", size=8.5,
         color="FFFFFF", bold=True, check=False)
    text(sl, px + 12, py + 26, 300, 18, "KeyError: 'baja'", size=14, color=UI_TEXT, bold=True, font=MONO, check=False)
    chip(sl, px + 210, py + 28, 50, 15, "NUEVA", fill="D62728", color="FFFFFF", size=7.5, radius=3)
    chip(sl, px + 266, py + 28, 76, 15, "sin resolver", fill="FFFFFF", color=UI_TEXT, size=7.5, radius=3, line=UI_LINE)
    text(sl, px + 12, py + 47, pw - 24, 12, "app.py:281 en clasificar   SLA_HORAS[resultado.prioridad]", size=8.5,
         font=MONO, color=UI_LABEL, check=False)
    stats = [("EVENTOS", "214"), ("USUARIOS", "37"), ("PRIMERA VEZ", "19:31 · release B"), ("ÚLTIMA VEZ", "19:36")]
    sw = (pw - 24 - 3 * 8) / 4
    for i, (lab, val) in enumerate(stats):
        sx = px + 12 + i * (sw + 8)
        box(sl, sx, py + 66, sw, 40, fill=UI_CARD, line=UI_LINE, radius=2)
        text(sl, sx + 7, py + 71, sw - 12, 10, lab, size=7.6, color=UI_MUTED, bold=True, check=False)
        text(sl, sx + 7, py + 84, sw - 12, 18, val, size=12 if i < 2 else 9.5, color=UI_TEXT, bold=True, check=False)
    # frecuencia: eventos por cada 5 minutos
    gx, gy, gw, gh = px + 12, py + 114, 300, 120
    box(sl, gx, gy, gw, gh, fill=UI_CARD, line=UI_LINE, radius=2)
    text(sl, gx + 7, gy + 5, gw - 14, 11, "Eventos por cada 5 min", size=8.6, color=UI_TEXT, bold=True, check=False)
    vals = [0, 0, 0, 0, 0, 0, 38, 92, 84, 0, 0, 0]
    bw = (gw - 20) / len(vals)
    base = gy + gh - 22
    for i, v in enumerate(vals):
        h = v * 0.75
        if h:
            box(sl, gx + 10 + i * bw + 2, base - h, bw - 4, h, fill="D62728", radius=0)
    line(sl, gx + 10, base, gx + gw - 10, base, color=UI_LINE, w=0.75, head="none")
    for i, lab in [(6, "B desplegada"), (9, "rollback a A")]:
        xx = gx + 10 + i * bw
        line(sl, xx, gy + 18, xx, base, color=UI_MUTED, w=0.75, head="none", dash=True)
        text(sl, xx - 40, base + 4, 80, 10, lab, size=7.6, color=UI_MUTED, align="c", check=False)
    # etiquetas y release
    tx = px + 322
    box(sl, tx, gy, pw - 334, gh, fill=UI_CARD, line=UI_LINE, radius=2)
    text(sl, tx + 7, gy + 5, 170, 11, "Etiquetas de los eventos", size=8.6, color=UI_TEXT, bold=True, check=False)
    tags_ = [("release", "B (a8b0d4c)", 1.0), ("prioridad", "baja", 1.0), ("ruta", "/clasificar", 1.0),
             ("environment", "staging", 1.0)]
    yy = gy + 22
    for k_, v_, f in tags_:
        text(sl, tx + 7, yy, 170, 10, [[(k_ + "  ", {"color": UI_MUTED}), (v_ + "  100 %", {"bold": True})]],
             size=8.2, color=UI_TEXT, check=False)
        box(sl, tx + 7, yy + 11, (pw - 348) * f, 4, fill=UI_BLUE, radius=0)
        yy += 23
    # pie del panel: acciones
    text(sl, px + 12, py + 244, pw - 24, 26, "La release se envía con cada evento (release = APP_VERSION, el mismo commit "
         "que el log): así se sabe qué versión trajo la incidencia.", size=8.5, color=UI_LABEL)
    ui_button(sl, px + 12, py + 284, 170, "Resolver en la siguiente release", primary=True, size=8.5)
    ui_button(sl, px + 190, py + 284, 110, "Ver los 214 eventos", size=8.5)
    ui_button(sl, px + 308, py + 284, 110, "Avisar si se repite", size=8.5)
    takeaway(sl, "Un log cuenta un error; el error tracking agrupa los iguales y dice cuántos, a quién y desde qué release.",
             label="Idea guía", lab_color=BLUE)
    footer(sl, block=5)
    notes(sl, """
19:43–19:45. Temario: «Error tracking». Continúa la demo 4: el mismo KeyError: 'baja' de la versión B, visto como lo vería un error tracker. Sentry (y Rollbar, Application Insights…) recibe cada excepción como un evento. Según la documentación de Sentry, todo evento tiene una huella (fingerprint) y los eventos con la misma huella se agrupan en una incidencia (issue); la huella por defecto sale de la traza, la excepción y el mensaje, y se puede ajustar con reglas o desde el SDK.
Leer el esquema: tres eventos con request_id distintos (uno es el real del ensayo, aaf20664…; los otros son ilustrativos) → una huella → una incidencia NUEVA con 214 eventos y 37 usuarios (valores ilustrativos), primera vez en la release B, pico entre el despliegue de B y el rollback a A, y etiquetas: 100 % release B, 100 % prioridad baja. Con eso se ve en segundos lo que con logs exige una consulta: qué release lo trajo y qué entradas lo provocan.
Release: con release configurada, cada error queda asociado a la versión; «resolver en la siguiente release» hace que nuevos eventos en una versión posterior marquen la incidencia como regresión. En la demo sería release = APP_VERSION (el commit). Alertas típicas: incidencia nueva tras un despliegue, o más de N eventos/usuarios en M minutos.
La demo NO integra Sentry: el error se localiza con el log de excepción y la alarma de 5xx (diapositivas 33 y 35). Configuración posible: sentry_sdk.init(dsn=…, release=…, environment="staging"). Como nuestro middleware captura el KeyError y devuelve un 500, llamar a sentry_sdk.capture_exception(error) dentro de ese except con un filtro de datos y sin adjuntar el texto de la incidencia.
En vivo: nada; conceptual.
Pregunta: «¿Por qué agrupar por huella y no por mensaje de error?».
Fuentes: https://docs.sentry.io/concepts/data-management/event-grouping/ · https://docs.sentry.io/product/releases/ · https://docs.sentry.io/product/issues/states-triage/ · https://docs.sentry.io/platforms/python/integrations/fastapi/ (consultadas con Context7 el 17/11/2026; copias en .build/s18/investigacion/ctx7-sentry-*.txt); demo-cicd/cambios/02 (SLA_HORAS, línea 281 de app.py en B); .build/s18/ensayo/logs-B.txt.""")
    return sl


def s25_metricas(d):
    sl = d.slide(tag="metricas")
    header(sl, "Monitoring · métricas desde los logs", "Errores y latencia en un panel, y una alarma que avisa",
           "Tres filtros de métricas convierten las líneas JSON en series numéricas sin instalar agentes. Un panel "
           "muestra errores 5xx y la latencia p50/p95 de /clasificar; una alarma salta con un solo 5xx en un minuto.")
    section_label(sl, 43, 134, 420, "Filtros de métricas · infra/02-staging.yaml", color=BLUE)
    flt = [("Peticiones", '{ $.evento = "peticion" && $.ruta = "/clasificar" }', "1 por línea"),
           ("Errores5xx", '{ $.evento = "peticion" && $.estado >= 500 }', "1 por línea"),
           ("DuracionMs", '{ … && $.ruta = "/clasificar" }', "valor $.duracion_ms")]
    y = 151
    for m, p, v in flt:
        box(sl, 43, y, 420, 46, fill=CARD)
        text(sl, 53, y + 5, 400, 14, [[(m, {"bold": True, "color": TITLE}), ("   " + v, {"color": MUTED, "size": 8.5})]],
             size=10, color=TEXT)
        text(sl, 53, y + 24, 404, 14, p, size=9, font=MONO, color=MINT_L, check=False)
        y += 51
    section_label(sl, 43, 310, 420, "Logs Insights · comparar versiones", color=BLUE)
    code_panel(sl, 43, 327, 420, 64, [
        'filter evento = "peticion" and ruta = "/clasificar"',
        "| stats count() as peticiones,",
        "        pct(duracion_ms, 95) as p95_ms",
        "  by version, estado"], size=9.2, fill=CARD, line=BORDER)
    node(sl, 43, 401, 420, 64, "r-cw-alarm.png", "Alarma  s18-…-errores-5xx",
         "Suma de Errores5xx ≥ 1 en 1 minuto; sin datos = sin error. Ampliación opcional del enunciado.",
         icon_s=32, tsize=10.5, ssize=9)
    section_label(sl, 479, 134, 260, "Panel de staging", color=BLUE)
    esquema_label(sl, 767, 132, w=150, t="ESQUEMA · datos ilustrativos")
    box(sl, 479, 151, 438, 314, fill=UI_BG, line="AEB5BD", radius=4)
    box(sl, 479, 151, 438, 18, fill=UI_NAV, radius=0)
    text(sl, 487, 154, 300, 12, "CloudWatch › Dashboards › s18-tu-nombre", size=8.5, color="FFFFFF", bold=True, check=False)
    # gráfico 1: peticiones y errores
    gx, gy, gw, gh = 489, 177, 205, 128
    box(sl, gx, gy, gw, gh, fill=UI_CARD, line=UI_LINE, radius=2)
    text(sl, gx + 6, gy + 4, gw - 12, 12, "Peticiones y errores 5xx / min", size=8.6, color=UI_TEXT, bold=True, check=False)
    vals = [6, 7, 5, 8, 6, 7, 9, 8, 6, 7]
    errs = [0, 0, 0, 0, 0, 3, 4, 0, 0, 0]
    bw = (gw - 20) / len(vals)
    for i, (v, e) in enumerate(zip(vals, errs)):
        bx = gx + 10 + i * bw
        h = v * 9
        box(sl, bx + 2, gy + gh - 12 - h, bw - 4, h, fill="7EB5E8", radius=0)
        if e:
            box(sl, bx + 2, gy + gh - 12 - e * 9, bw - 4, e * 9, fill="D62728", radius=0)
    text(sl, gx + 6, gy + gh - 11, gw - 12, 10, "B desplegada       rollback a A", size=7.6, color=UI_MUTED, check=False)
    # gráfico 2: latencia
    lx, ly = 702, 177
    box(sl, lx, ly, 205, 128, fill=UI_CARD, line=UI_LINE, radius=2)
    text(sl, lx + 6, ly + 4, 193, 12, "Duración de /clasificar (ms)", size=8.6, color=UI_TEXT, bold=True, check=False)
    p50 = [40, 42, 41, 43, 40, 44, 42, 41, 40, 42]
    p95 = [70, 75, 72, 90, 74, 78, 76, 73, 71, 74]
    for serie, col in [(p50, "2CA02C"), (p95, "FF7F0E")]:
        pts = [(lx + 12 + i * 18.5, ly + 118 - v * 0.95) for i, v in enumerate(serie)]
        for a, b in zip(pts, pts[1:]):
            line(sl, a[0], a[1], b[0], b[1], color=col, w=1.5, head="none")
    text(sl, lx + 120, ly + 18, 80, 10, "— p95", size=7.6, color="FF7F0E", bold=True, check=False)
    text(sl, lx + 120, ly + 30, 80, 10, "— p50", size=7.6, color="2CA02C", bold=True, check=False)
    # tabla de errores
    box(sl, 489, 313, 418, 142, fill=UI_CARD, line=UI_LINE, radius=2)
    text(sl, 495, 317, 400, 12, "Últimos errores: request_id, versión y causa", size=8.6, color=UI_TEXT, bold=True, check=False)
    rows = [["@timestamp", "evento", "version", "estado", "error_tipo"],
            ["19:36:12", "excepcion", "a8b0d4c…", "", "KeyError"],
            ["19:36:12", "peticion", "a8b0d4c…", "500", ""],
            ["19:35:40", "excepcion", "a8b0d4c…", "", "KeyError"],
            ["19:35:40", "peticion", "a8b0d4c…", "500", ""]]
    table(sl, 495, 333, 406, [1, 1, 1.1, 0.7, 1], rows, size=8.5, row_h=19, header_fill="E9EBED",
          header_color=UI_TEXT, fills=("FFFFFF", "F6F7F7"), colors={0: UI_TEXT, 1: UI_TEXT, 2: UI_TEXT, 3: UI_TEXT, 4: "D62728"})
    takeaway(sl, "Las métricas dicen que algo va mal y desde cuándo; los logs de ese minuto dicen por qué.",
             label="Idea guía", lab_color=BLUE)
    footer(sl, block=5)
    notes(sl, """
19:45–19:47. El enunciado: «revisa errores y latencia en un panel básico». La plantilla de staging crea tres AWS::Logs::MetricFilter sobre el grupo de logs: Peticiones (cuenta líneas «peticion» de /clasificar), Errores5xx (estado ≥ 500) y DuracionMs (valor = duracion_ms). Con ellas, un AWS::CloudWatch::Dashboard con dos gráficos (peticiones y 5xx por minuto; p50 y p95) y una tabla de Logs Insights con los últimos errores, y una AWS::CloudWatch::Alarm de 5xx (ampliación opcional del enunciado: «Añade una alerta automática»). Sin destinatario: para recibir un aviso se añade un tema de SNS en AlarmActions.
El panel de la diapositiva es un esquema con datos ilustrativos, no una captura (no hay ensayo en AWS).
Coste: la capa gratuita de CloudWatch incluye 3 paneles personalizados y 10 métricas de alarma al mes (página de precios, 16/11/2026); las métricas personalizadas de los filtros pueden tener coste fuera de la capa gratuita.
En vivo: abrir la salida Panel del stack y Logs Insights con la consulta (comandos.md) si hay staging.
Pregunta: «¿Por qué la alarma trata la ausencia de datos como "no hay error"?».
Fuentes: infra/02-staging.yaml (MetricaPeticiones, MetricaErrores, MetricaDuracion, Panel, AlarmaErrores); https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntaxForMetricFilters.html · https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Dashboard-Body-Structure.html · https://aws.amazon.com/cloudwatch/pricing/ (16/11/2026). Icono: AWS Architecture Icons (CloudWatch Alarm).""")
    return sl


def s26_rollback(d):
    sl = d.slide(tag="rollback")
    header(sl, "Demo 5 · rollback", "Volver a A es desplegar su digest otra vez",
           "No revertimos commits ni reconstruimos: lanzamos el mismo workflow con el digest de A, que ya pasó todas las "
           "comprobaciones. Después arreglamos hacia delante con el test que faltaba.")
    steps = [("A", "sha256:7d1e…", "en marcha · 200", BLUE, BLUE_BG),
             ("B", "sha256:c41b…", "desplegada · 500 con «baja»", CORAL, CORAL_BG),
             ("A", "sha256:7d1e…", "rollback · 200 otra vez", BLUE, BLUE_BG),
             ("C", "B + test + arreglo", "nueva PR · 27 passed", MINT, TAKE_BG)]
    w = (874 - 3 * 34) / 4
    for i, (v, dg, st, col, f) in enumerate(steps):
        x = 43 + i * (w + 34)
        box(sl, x, 136, w, 70, fill=f, line=col)
        circle(sl, x + 10, 148, 30, col)
        text(sl, x + 10, 152, 30, 22, v, size=16, font=SERIF, color=DARK, align="c", check=False)
        text(sl, x + 50, 146, w - 58, 14, dg, size=9.5, font=MONO, color=TITLE, bold=True, check=False)
        text(sl, x + 50, 166, w - 58, 30, st, size=9.5, color=TEXT)
        if i < 3:
            line(sl, x + w + 4, 171, x + w + 30, 171, color=MUTED, w=1.5)
    tag(sl, 43, 212, "ilustrativo", w=172, t="DIGEST ILUSTRATIVOS · no medidos")
    section_label(sl, 43, 236, 470, "El rollback", color=BLUE)
    code_panel(sl, 43, 253, 470, 86, [
        "gh workflow run desplegar-staging.yml --ref main \\",
        '  -f "digest=$DIGEST_A" -f motivo=rollback',
        "",
        "curl -s -o /dev/null -w '%{http_code}' -X POST \\",
        "  http://$IP:8000/clasificar -d '{\"texto\":\"…duda…\"}'  # 200"], size=8.5, fill=CARD, line=BORDER)
    side_note(sl, 43, 351, 470, 114, "Lo que un rollback no deshace",
              "Datos que B escribió, mensajes o correos enviados, cobros, migraciones de esquema. Volver a la imagen A "
              "solo cambia el código en marcha; los datos se protegen con cambios compatibles y copias (bloque 6).",
              accent=CORAL, size=9.5)
    box(sl, 529, 236, 388, 229, fill=CARD)
    text(sl, 541, 244, 260, 12.2, "ENSAYO LOCAL DEL 17/11/2026", size=8.5, color=BLUE, bold=True)
    tag(sl, 735, 241, "real", w=172)
    res = [("A", "smoke correcto; consulta de prioridad baja → 200"),
           ("B", "smoke correcto; consulta de prioridad baja → 500 (KeyError en el log)"),
           ("A", "la misma imagen, sin reconstruir: smoke correcto; → 200"),
           ("C", "test nuevo con B: 1 failed; con el arreglo: 27 passed")]
    y = 266
    for v, t in res:
        circle(sl, 541, y + 1, 18, {"A": BLUE, "B": CORAL, "C": MINT}[v])
        text(sl, 541, y + 3, 18, 14, v, size=9, color=DARK, bold=True, align="c", check=False)
        text(sl, 567, y, 340, 34, t, size=9.5, color=TEXT)
        y += 40
    text(sl, 541, 428, 366, 32, "En GitHub y AWS, el mismo recorrido está pendiente del ensayo autorizado.",
         size=8.5, color=AMBER)
    takeaway(sl, "El rollback compra tiempo; el arreglo es otra PR que recorre el mismo camino.", label="Idea guía",
             lab_color=BLUE)
    footer(sl, block=5)
    notes(sl, """
19:47–19:50. Quinto momento de demo. El enunciado: «Despliega una segunda versión y demuestra un rollback a la anterior reutilizando el digest de la imagen previamente validada; comprueba después el endpoint».
Rollback = desplegar-staging.yml con DIGEST_A y motivo rollback (queda en el título de la ejecución). El workflow vuelve a comprobar que el digest existe, registra una revisión nueva con la imagen A y hace el smoke. Después repetir la petición de prioridad baja: 200. Abrir el panel: los 5xx paran y la alarma vuelve a OK.
Arreglar hacia delante: cambios/03-test-que-faltaba.patch añade un test parametrizado con las tres prioridades (en rojo con B: 1 failed) y la corrección SLA_HORAS con «baja»: 72 (27 passed). Ese cambio es la versión C, que recorre PR → main → publicar → desplegar.
Resultados reales del ensayo local (17/11/2026, .build/s18/logs/ensayo-local.txt y ensayo-comandos.txt). Digest de la fila superior ilustrativos.
En vivo: comandos.md, diapositiva 36 (GitHub/AWS o local).
Pregunta: «¿El rollback arregla el código?» (no: devuelve el servicio a un estado conocido mientras se corrige).
Fuentes: demo-cicd/.github/workflows/desplegar-staging.yml; cambios/03-test-que-faltaba.patch; README de la demo, apartado 8.4–8.5.""")
    return sl


def s28_migraciones(d):
    sl = d.slide(tag="migraciones")
    header(sl, "Migraciones de base de datos", "Cambios de esquema que aceptan la versión anterior",
           "Durante un despliegue, y después de un rollback, conviven dos versiones del código sobre la misma base de "
           "datos. Cada cambio de esquema debe valer para las dos: se expande, se migra y al final se contrae.")
    phases = [("1", "Expand", "Añadir sin quitar", MINT,
               ["ALTER TABLE incidencias", "  ADD COLUMN sla_horas INTEGER;", "-- admite NULL: A no se entera"],
               "A sigue leyendo y escribiendo; B ya puede usar la columna."),
              ("2", "Migrar", "Código nuevo y datos antiguos", AMBER,
               ["-- desplegar B (escribe sla_horas)", "UPDATE incidencias SET sla_horas = 72", " WHERE sla_horas IS NULL", "   AND prioridad = 'baja';"],
               "Relleno por lotes, sin parar el servicio. A y B conviven."),
              ("3", "Contract", "Retirar lo viejo, más tarde", CORAL,
               ["-- otra entrega, cuando ninguna", "-- versión desplegable lo use:", "ALTER TABLE … DROP COLUMN …;"],
               "Solo cuando ya no se va a volver a una versión que lo necesite.")]
    cw = (874 - 2 * 24) / 3
    for i, (n, t, s, col, code, b) in enumerate(phases):
        x = 43 + i * (cw + 24)
        box(sl, x, 134, cw, 186, fill=CARD, line=col)
        badge(sl, x + 10, 143, n, fill=col, d=18, size=9)
        text(sl, x + 36, 140, cw - 48, 20, t, size=14, font=SERIF, color=TITLE)
        text(sl, x + 36, 161, cw - 48, 12, s, size=9, color=col, bold=True)
        code_panel(sl, x + 10, 182, cw - 20, 74, code, size=8.3)
        text(sl, x + 10, 264, cw - 20, 52, b, size=9.5, color=TEXT)
        if i < 2:
            line(sl, x + cw + 3, 227, x + cw + 21, 227, color=MUTED, w=1.5)
    side_note(sl, 43, 334, 431, 131, "Incompatible: renombrar en un paso",
              "ALTER TABLE … RENAME COLUMN prioridad TO urgencia rompe a la versión A al instante. En el ensayo con "
              "SQLite, A falla con «no such column: prioridad». Se hace en tres pasos: añadir urgencia, escribir en las "
              "dos y leer de la nueva, retirar prioridad.", accent=CORAL, size=9.5)
    side_note(sl, 486, 334, 431, 131, "Un rollback no revierte datos",
              "Volver a la imagen A no borra la columna ni las filas que escribió B: en el ensayo quedan 6 filas, no 3. "
              "Si hay que deshacer datos, es otra migración hacia delante o una restauración. Por eso la migración se "
              "prueba antes, con una copia recién hecha.", accent=AMBER, size=9.5)
    takeaway(sl, "Primero el esquema compatible, luego el código, al final la limpieza: así el código siempre puede volver atrás.",
             label="Idea guía", lab_color=CORAL)
    footer(sl, block=6)
    notes(sl, """
19:50–19:52. Temario: «Migraciones de base de datos en producción y despliegues sin downtime». El enunciado pide «cambios de base de datos compatibles con la versión anterior» y advierte: «Volver a una imagen antigua no revierte por sí solo una migración de datos». La demo no tiene base de datos (el enunciado no la exige); el patrón expand/contract (cambio en paralelo) se demuestra en extras/migracion_y_restauracion.py con SQLite y datos ficticios, ejecutado el 17/11/2026: la columna nueva admite NULL y A sigue funcionando; el rollback del código deja 6 filas y la columna; renombrar en un paso rompe a A («no such column: prioridad»).
Reglas prácticas: migraciones versionadas y en el pipeline (Alembic en Python, Flyway, Liquibase); ejecutarlas antes de desplegar el código que las necesita; por lotes las que tocan muchas filas; nunca DROP o RENAME en la misma entrega que el código que deja de usarlo.
En vivo: nada aquí; el script se ejecuta en la diapositiva siguiente.
Pregunta: «Si B escribió datos en una columna nueva y volvemos a A, ¿qué pasa con ellos?».
Fuentes: demo-cicd/extras/migracion_y_restauracion.py y su salida (.build/s18/logs/extras-migracion.txt); README de la demo, «Cambios de base de datos compatibles».""")
    return sl


def s29_backups(d):
    sl = d.slide(tag="backups")
    header(sl, "Disaster recovery y backups", "Una copia solo vale si se ha restaurado",
           "Disaster recovery es volver a dar servicio tras perder datos o infraestructura. Se diseña con dos números: "
           "cuántos datos podemos perder (RPO) y cuánto tardamos en volver (RTO).")
    section_label(sl, 43, 134, 520, "RPO y RTO en una línea de tiempo", color=CORAL)
    box(sl, 43, 151, 520, 128, fill=CARD)
    y = 214
    line(sl, 60, y, 548, y, color=MUTED, w=1.5, head="end")
    pts = [(110, "última copia", MINT), (300, "incidente", CORAL), (490, "servicio de vuelta", BLUE)]
    for x, t, col in pts:
        circle(sl, x - 7, y - 7, 14, col)
        text(sl, x - 60, y + 12, 120, 12, t, size=9, color=TITLE, bold=True, align="c")
    box(sl, 110, 168, 190, 22, fill=CORAL_BG, line=CORAL, radius=3)
    text(sl, 114, 171, 182, 16, "RPO · datos que se pierden", size=9, color=CORAL, bold=True, align="c")
    box(sl, 300, 168, 190, 22, fill=BLUE_BG, line=BLUE, radius=3)
    text(sl, 304, 171, 182, 16, "RTO · tiempo sin servicio", size=9, color=BLUE, bold=True, align="c")
    text(sl, 55, 246, 500, 30, "Copias más frecuentes reducen el RPO; restauraciones ensayadas y automatizadas reducen el RTO.",
         size=9, color=TEXT)
    section_label(sl, 43, 291, 520, "Prueba de restauración · extras/ con SQLite y datos ficticios", color=CORAL)
    tag(sl, 391, 289, "real", w=172)
    code_panel(sl, 43, 308, 520, 92, [
        "2. Copia de seguridad ANTES de migrar, con su huella",
        "   copia-antes-de-migrar.sqlite3: 3 filas, huella d54600f9567acb20",
        "7. PRUEBA DE RESTAURACIÓN en una base nueva, sin tocar la original",
        "   integridad ok, 3 filas, huella d54600f9567acb20: coincide",
        "   lo escrito después de la copia no está: 3 filas (eso mide el RPO)"], size=8.3, fill="0B1418", line=BORDER)
    text(sl, 43, 408, 520, 56, "Restaurar en una base nueva, comprobar integridad, número de filas y una consulta "
         "funcional, y anotar fecha, duración y resultado. Nunca sobre producción real.", size=9.5, color=TEXT)
    items = [("aws-rds.png", "Copias automáticas (RDS)", "Retención de 0 a 35 días; 0 las desactiva. Una copia manual antes de cada migración."),
             ("aws-backup.png", "Restaurar a un punto", "Crea una instancia nueva sin tocar la original; los registros de transacciones se suben cada 5 minutos."),
             ("aws-cloudformation.png", "Lo que se recrea desde Git", "Plantillas, workflows y código. Las imágenes siguen en ECR por su digest."),
             ("aws-secrets.png", "Lo que también hay que copiar", "Secretos y configuración: sin ellos, los datos restaurados no arrancan.")]
    y = 134
    for ic, t, b in items:
        piece_row(sl, 579, y, 338, 77, ic, t, b, tsize=10.5, bsize=9, icon_s=30)
        y += 83
    takeaway(sl, "El código y la infraestructura se recrean desde Git; los datos, solo desde una copia que ya sabemos restaurar.",
             label="Idea guía", lab_color=CORAL)
    footer(sl, block=6)
    notes(sl, f"""
19:52–19:54. Temario: «Disaster recovery y backups». El enunciado pide en el README «copias de seguridad con prueba de restauración». RPO (Recovery Point Objective): cuántos datos podemos perder, medido en tiempo desde la última copia. RTO (Recovery Time Objective): cuánto tiempo podemos estar sin servicio. Se acuerdan con negocio y determinan frecuencia de copias y automatización.
En AWS RDS: copias automáticas con retención configurable de 0 a 35 días (0 desactiva); restauración a un punto en el tiempo, que crea una instancia nueva y no modifica la original; RDS sube los registros de transacciones a S3 cada cinco minutos (LatestRestorableTime). AWS Backup centraliza planes de copia de varios servicios. Este proyecto del aula tiene región única (eu-north-1): no se plantean copias entre regiones.
Salida real de extras/migracion_y_restauracion.py (17/11/2026): copia coherente con la API de backup de SQLite, huella SHA-256 del contenido, restauración en una base nueva con integrity_check = ok y huella igual; las filas posteriores a la copia no están (eso es el RPO).
En vivo: uv run python extras/migracion_y_restauracion.py (2 segundos).
Pregunta: «¿Cuándo fue la última vez que alguien restauró una copia de vuestra base de datos?».
Fuentes: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html · https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html · https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html (16/11/2026). {SRC_AWS}""")
    return sl


def s30_practica(d):
    sl = d.slide(tag="practica")
    header_simple(sl, "Práctica", "Montar un pipeline de CI/CD con tests automáticos",
                  "Práctica opcional (aclaración de la escuela del 04/11). Solución completa en demo-cicd; el "
                  "enunciado pide un repositorio de GitHub y un servicio pequeño en ECS/Fargate.")
    rows_simple(sl, [("Probar", "Dobles del proveedor: entrada inválida, respuesta válida y fallo. Una PR defectuosa en rojo."),
                     ("Publicar", "Desde main: las mismas comprobaciones, una imagen en ECR y su digest."),
                     ("Desplegar", "workflow_dispatch desde main, por digest, con OIDC y environment staging."),
                     ("Observar", "Logs con request_id y versión, un error localizado y un panel de errores y latencia."),
                     ("Recuperar", "Segunda versión, rollback al digest anterior y plan de datos en el README.")],
                y0=156.8, rh=45, gap=6.5, lsize=14.5)
    band_simple(sl, "Entrega: código, workflows, tests, evidencias y limpieza · 6–8 horas con el laboratorio preparado.")
    footer_simple(sl)
    notes(sl, """
19:54–19:56. Práctica OPCIONAL según la aclaración de Laura del 04/11. Enseñar demo-cicd/docs/ejercicio.md y el README de la demo (pasos 1–9). Los alumnos pueden partir de esta solución o de su API de S16. Puntos que valora el enunciado: bloqueo de cambios defectuosos, uso del mismo artefacto, secretos protegidos y recuperación comprobable. Entrega: aplicación, workflows, tests, evidencias de bloqueo, despliegue y rollback, y pasos para eliminar los recursos propios.
Ampliación opcional: alarma automática (incluida en la plantilla) o migración compatible y restauración con datos ficticios (extras/). Nunca sobre producción real.
Recordar costes: repositorio público para Actions y environments gratuitos; una tarea Fargate pequeña y logs con retención de 7 días; borrar los stacks al terminar (README, paso 9).
Pregunta: «¿Qué evidencia guardaríais para demostrar que la PR estaba bloqueada?».
Fuentes: enunciado S18 (ejercicios.docx, 29/09/2026); demo-cicd/docs/ejercicio.md; Gmail, Laura 04/11 (prácticas opcionales).""")
    return sl


def s31_cierre(d):
    sl = d.slide(BG_SECTION, "cierre")
    img(sl, "thepower-logo.png", 38, 34, h=30)
    text(sl, 43, 84, 300, 14, "CIERRE", size=10, color=MINT, bold=True)
    text(sl, 43, 102, 520, 44, "Lo que nos llevamos", size=32, font=SERIF, color=TITLE)
    pts = ["CI comprueba cada cambio; la entrega continua deja siempre una imagen validada lista para desplegar.",
           "Una PR solo bloquea si un test describe el comportamiento y una regla exige el check.",
           "Se prueba, se publica y se despliega el mismo digest; nunca se reconstruye al desplegar.",
           "OIDC da credenciales de una hora a un sub exacto: ni claves guardadas ni ramas ajenas.",
           "Un panel y una alarma avisan antes que el usuario; request_id y versión llevan a la causa y al commit.",
           "El rollback vuelve el código atrás, no los datos: esquema compatible y copias restauradas."]
    y = 158
    for i, p in enumerate(pts, 1):
        circle(sl, 43, y, 22, MINT_L)
        text(sl, 43, y + 3, 22, 16, str(i), size=10.5, color=DARK, bold=True, align="c")
        text(sl, 76, y + 1, 470, 44, p, size=12, color=TITLE)
        y += 50
    box(sl, 584, 130, 333, 336, fill="1A463C", radius=8)
    text(sl, 604, 146, 300, 40, "¿Preguntas?", size=30, font=SERIF, color=MINT_L)
    text(sl, 604, 198, 300, 12, "PARA COMPROBAR", size=9, color=MINT, bold=True)
    bullets(sl, 604, 216, 300, 96, ["¿Qué prueba un build y qué no prueba?", "¿Qué identifica un digest que no identifica una etiqueta?",
                                    "¿Por qué environment: staging cambia el sub?", "¿Qué pasa con los datos al volver a A?"],
            size=10.5, color=TITLE, mark_color=MINT, space=2)
    text(sl, 604, 322, 300, 12, "PRÓXIMA SESIÓN · S19", size=9, color=MINT, bold=True)
    text(sl, 604, 338, 300, 40, "Evaluación y testing de sistemas de IA: medir si funcionan bien antes y después de cada cambio.",
         size=10.5, color=TITLE)
    text(sl, 604, 388, 300, 12, "MATERIALES DE S18", size=9, color=MINT, bold=True)
    text(sl, 604, 404, 300, 56, "demo-cicd: README paso a paso, workflows, plantillas, guion, comandos y práctica opcional.",
         size=10.5, color=TITLE)
    notes(sl, """
19:56–20:00. Recapitular con los seis puntos y abrir preguntas. Las cuatro preguntas de comprobación son las del plan de la clase: qué prueba un build (que la imagen se construye y arranca, no que el comportamiento sea correcto), qué identifica un digest (el contenido exacto), por qué environment cambia el sub (GitHub nombra el entorno en el token y solo lo emite si sus reglas lo permiten) y qué ocurre con los datos al volver a A (nada: siguen ahí).
Pregunta final: «¿Qué evidencia de esta clase os faltaría hoy en vuestro proyecto?».
Recordar el QR de la diapositiva 2 (evalúa S17 del 23/11) para quien no lo haya rellenado.
Estado real de la preparación (17/11/2026): tests, análisis, plantillas, workflows (actionlint) y el recorrido A → B → A con Docker comprobados en local; la ejecución en GitHub Actions, ECR y ECS está pendiente del ensayo que autorice José. No presentar como hecho lo que no se haya ejecutado.
Próxima sesión: S19, evaluación y testing de sistemas de IA (temario del 17/07/2026).
Fuentes: plan S16–S20 (sección S18, preguntas y criterio de cierre); material/S18/verificacion.md.""")
    return sl
