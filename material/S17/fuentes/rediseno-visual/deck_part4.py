"""Diapositivas 26–36: bloque 4 (IAM y CloudWatch) y bloque 5 (latencia y límites)."""
from deck_lib import *  # noqa: F401,F403
from deck_part1 import SRC_AWS_ICONS
from deck_part3 import SRC_TEMPLATE


def s25_div4(d):
    sl = divider(d, 4, "IAM y CloudWatch", "Quién puede invocar cada pieza y cómo seguimos una petición",
                 "Tres permisos distintos, la firma SigV4, los logs, las métricas y el diagnóstico por capas.",
                 ["¿Qué tres permisos intervienen en el recorrido?",
                  "¿Qué aporta la firma y qué no aporta?",
                  "¿Cómo encontramos una petición en CloudWatch?",
                  "¿En qué capa falló un error?"],
                 [("aws-iam.png", "AWS IAM"), ("r-iam-temp.png", "Credenciales\ntemporales"), ("aws-cloudwatch.png", "Amazon\nCloudWatch")],
                 "19:20–19:30 · 10 min")
    notes(sl, """
TIEMPO 19:20 (10 s). Bloque 4 de 7: IAM y CloudWatch, de 19:20 a 19:30 (10 min).
QUÉ EXPLICAR: ya conocemos las piezas; ahora, quién puede invocar cada una y cómo encontramos el rastro de una petición.
CONSOLA: abrir IAM y CloudWatch en pestañas.
PREGUNTA: «¿Cuántos permisos distintos creéis que hacen falta para que la petición llegue al modelo?»
FUENTES: temario AI Engineer y guion de S17 (material/S17/guion-profesor.md), con la distribución de tiempos de esta versión.
IMÁGENES: """ + SRC_AWS_ICONS + " Recurso IAM Temporary Security Credential del mismo paquete.")
    return sl


def s26_permisos(d):
    sl = d.slide(tag="tres-permisos")
    header(sl, "IAM", "Tres permisos distintos en el mismo recorrido",
           "Cada flecha del recorrido es una autorización diferente, en un lugar diferente y con un síntoma diferente "
           "cuando falta. Una no sustituye a las otras.")
    nodes = [(43, "g-user.png", "Cliente", "identidad con credenciales temporales"),
             (283, "aws-apigw.png", "API Gateway", "ruta POST /clasificar"),
             (523, "aws-lambda.png", "Lambda", "alias aula y rol de ejecución"),
             (763, "aws-bedrock.png", "Bedrock", "perfil eu. y modelo base")]
    for x, ic, t, b in nodes:
        box(sl, x, 134, 154, 62, fill=CARD)
        img(sl, ic, x + 10, 149, w=32, h=32)
        text(sl, x + 50, 142, 100, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, x + 50, 160, 100, 34, b, size=8.5, color=TEXT)
    for x in (197, 437, 677):
        line(sl, x + 2, 165, x + 84, 165, color=VIOLET, w=1.5)
    perms = [(1, "¿Puede el cliente invocar la ruta?", "Política de identidad del cliente",
              "execute-api:Invoke", "arn:aws:execute-api:eu-west-1:<cuenta>:<api-id>/$default/POST/clasificar",
              "Si falta: 403 en API Gateway; Lambda no se ejecuta."),
             (2, "¿Puede la API invocar la función?", "Política basada en recursos de Lambda",
              "lambda:InvokeFunction", "alias aula · condición SourceArn de la API y SourceAccount",
              "Si falta: la integración falla y el gateway devuelve un error 5xx sin log de la función."),
             (3, "¿Puede la función invocar el modelo?", "Rol de ejecución de Lambda",
              "bedrock:InvokeModel", "perfil eu.amazon.nova-2-lite-v1:0 y modelo base en origen y destinos",
              "Si falta: AccessDenied; nuestro handler responde 502 bedrock_denegado.")]
    w = (874 - 2 * 12) / 3
    for i, (n, q, where, act, res, fail) in enumerate(perms):
        x = 43 + i * (w + 12)
        box(sl, x, 210, w, 214, fill=VIOLET_BG)
        badge(sl, x + 10, 220, n, fill=VIOLET, d=20, size=10)
        text(sl, x + 38, 220, w - 48, 34, q, size=11, color=TITLE, bold=True)
        text(sl, x + 12, 258, w - 24, 12, where.upper(), size=8, color=VIOLET, bold=True)
        text(sl, x + 12, 274, w - 24, 16, act, size=10.5, font=MONO, color=MINT_L, bold=True)
        text(sl, x + 12, 294, w - 24, 52, res, size=9, font=MONO if n == 1 else SANS, color=TEXT)
        box(sl, x + 10, 350, w - 20, 66, fill=CORAL_BG, radius=4)
        text(sl, x + 18, 356, w - 36, 56, fail, size=9.5, color=TITLE)
    text(sl, 43, 432, 874, 36, [[("Converse ≠ acción IAM.  ", {"bold": True, "color": VIOLET}),
                                  ("Converse es el método del SDK; la acción que se concede es bedrock:InvokeModel "
                                   "(ConverseStream: bedrock:InvokeModelWithResponseStream). La política no usa bedrock:Converse.", {})]],
         size=10, color=TEXT)
    takeaway(sl, "¿Puede el cliente llamar a la ruta? ¿Puede la API invocar la función? ¿Puede la función invocar el modelo? Son tres preguntas.",
             "Idea guía")
    footer(sl, block=4)
    notes(sl, """
""" + timing_note("19:20", "19:23") + """
QUÉ EXPLICAR: tres permisos distintos. 1) El cliente puede invocar la ruta: la identidad que llama necesita execute-api:Invoke sobre el ARN exacto de la ruta y el stage (arn:aws:execute-api:eu-west-1:<cuenta>:<api-id>/$default/POST/clasificar). Lo concede el administrador del laboratorio; el script politica-cliente lo genera pero no modifica identidades. Si falta: 403 en API Gateway. 2) API Gateway puede invocar Lambda: política basada en recursos de la función con lambda:InvokeFunction sobre el alias, limitada por SourceArn y SourceAccount. Si falta: la integración falla con un error del gateway, sin log de la función. 3) El rol de Lambda puede invocar el modelo: bedrock:InvokeModel sobre el perfil y sobre el modelo base en las regiones de origen y destino, con la condición bedrock:InferenceProfileArn. Si falta: AccessDenied que nuestro handler traduce a 502 bedrock_denegado. Converse es el método del SDK; la acción IAM es bedrock:InvokeModel. No convertir este bloque en una lectura de políticas JSON: el detalle está en el anexo.
CONSOLA: IAM › Roles › (rol de la función) › Permissions (Action y Resource, solo lectura). Lambda › (función) › Configuration › Permissions › Resource-based policy statements. IAM › Policy simulator puede mencionarse como herramienta de comprobación, sin usarlo en clase.
PREGUNTA: «La petición está firmada, pero aparece bedrock_denegado. ¿Qué política revisamos?». Respuesta: el rol de Lambda y los recursos del perfil y modelos (y posibles restricciones de la cuenta), no la firma del cliente.
FUENTES: API Gateway Developer Guide, «Control access to HTTP APIs with IAM authorization»; AWS Lambda Developer Guide, «Working with resource-based IAM policies in Lambda» y «Lambda execution role»; Amazon Bedrock User Guide, «Using the Converse API» y «Geographic cross-Region inference», consultadas el 06/11/2026. Enunciado S17 (José, 28/09/2026): «Converse se autoriza mediante bedrock:InvokeModel, no bedrock:Converse».
IMÁGENES: """ + SRC_AWS_ICONS + " Icono genérico User.")
    return sl


def s27_sigv4(d):
    sl = d.slide(tag="sigv4")
    header(sl, "SigV4", "Firmar una petición no es tener permiso",
           "Con autorización IAM, el cliente firma cada petición con credenciales temporales. La firma demuestra quién envía "
           "y que los bytes no han cambiado; el permiso lo decide IAM y el cifrado lo pone HTTPS.")
    steps = [("r-iam-temp.png", "Credenciales temporales", "Access key ID, clave secreta y session token, con caducidad. "
              "Nunca en el repositorio ni en la pantalla."),
             ("g-document.png", "Petición canónica", "Método, ruta, headers firmados y hash de los bytes exactos del cuerpo."),
             ("r-iam-sts.png", "Firma", "Clave derivada para la fecha, la región eu-west-1 y el servicio execute-api. Viaja en Authorization."),
             ("aws-apigw.png", "Verificación", "API Gateway recalcula la firma (autenticación) y evalúa la política IAM (autorización).")]
    y = 134
    for i, (ic, t, b) in enumerate(steps):
        box(sl, 43, y, 440, 62, fill=CARD)
        badge(sl, 51, y + 23, i + 1, fill=VIOLET, d=16, size=8.5)
        img(sl, ic, 75, y + 15, w=30, h=30)
        text(sl, 115, y + 8, 360, 15, t, size=11, color=TITLE, bold=True)
        text(sl, 115, y + 25, 362, 36, b, size=9.5, color=TEXT)
        if i < 3:
            line(sl, 59, y + 62, 59, y + 68, color=VIOLET, w=1.25)
        y += 68
    pieces = [("Firma SigV4", "Autenticidad e integridad: quién envía y que la petición no se alteró.", VIOLET, VIOLET_BG),
              ("Política IAM", "Autorización: si esa identidad puede invocar esa ruta.", MINT, TAKE_BG),
              ("HTTPS / TLS", "Cifrado del transporte. La firma no cifra nada.", BLUE, BLUE_BG)]
    y = 134
    for t, b, col, bg in pieces:
        box(sl, 497, y, 420, 46, fill=bg)
        text(sl, 509, y + 6, 130, 34, t, size=11, color=col, bold=True, anchor="m")
        text(sl, 640, y + 6, 270, 34, b, size=9.5, color=TITLE, anchor="m")
        y += 52
    box(sl, 497, 298, 420, 168, fill=CARD, line=BORDER)
    text(sl, 509, 306, 400, 12, "PRUEBA CON curl (DEL ENUNCIADO) · las variables contienen credenciales", size=8.5, color=VIOLET, bold=True)
    code = ['curl --aws-sigv4 "aws:amz:${AWS_REGION}:execute-api" \\',
            '  --user "${AWS_ACCESS_KEY_ID}:${AWS_SECRET_ACCESS_KEY}" \\',
            '  -H "x-amz-security-token: ${AWS_SESSION_TOKEN}" \\',
            '  -H "content-type: application/json" \\',
            '  --data-binary @peticion.json "${API_URL}"']
    code_block(sl, 509, 324, 400, code, size=8.5, pitch=13)
    text(sl, 509, 398, 400, 64, "La referencia firma desde Python con SigV4Auth del SDK y envía exactamente los bytes firmados. "
                               "Si los bytes cambian después de firmar, la firma deja de valer. No se imprimen ni se guardan los headers.",
         size=9.5, color=TEXT)
    takeaway(sl, "Una firma válida identifica a quien llama; no le concede permisos. Sin execute-api:Invoke, la respuesta sigue siendo 403.",
             "Idea guía")
    footer(sl, block=4)
    notes(sl, """
""" + timing_note("19:23", "19:25") + """
QUÉ EXPLICAR: SigV4 de forma comprensible. 1) El cliente obtiene credenciales temporales (access key ID, secreto y session token, con caducidad), por ejemplo con aws sso login; no se guardan en el repositorio ni se muestran. 2) Construye la petición canónica: método, ruta, headers firmados y el hash de los bytes del cuerpo. 3) Firma con una clave derivada para la fecha, la región y el servicio execute-api; la firma viaja en Authorization junto a x-amz-date y x-amz-security-token. 4) API Gateway recalcula la firma (autenticación) y evalúa si esa identidad tiene execute-api:Invoke (autorización). Tres piezas distintas: la firma aporta autenticidad e integridad, IAM autoriza y HTTPS cifra el transporte.
CÓDIGO: src/curso_ia/serverless/firma.py: validar_url (solo la ruta HTTPS /clasificar de la HTTP API de la región) y signed_headers (exige session token; SigV4Auth con servicio execute-api). No mostrar valores de credenciales.
CONSOLA: ninguna. No ejecutar el curl en clase (consumiría una inferencia real si estuviera desplegado).
PREGUNTA: «Si firmo bien pero mi identidad no tiene execute-api:Invoke, ¿qué recibo?». Respuesta: 403; la firma no concede permisos.
FUENTES: API Gateway Developer Guide, «Control access to HTTP APIs with IAM authorization»; AWS IAM User Guide, «AWS Signature Version 4 for API requests», consultadas el 06/11/2026; ejercicio S17 (docs/fuentes/S17-ejercicio-original.txt, comando curl --aws-sigv4); src/curso_ia/serverless/firma.py.
IMÁGENES: """ + SRC_AWS_ICONS + " Recursos IAM Temporary Security Credential y AWS STS; genérico Document.")
    return sl


def s28_cloudwatch(d):
    sl = d.slide(tag="cloudwatch")
    header(sl, "Amazon CloudWatch", "Seguir una petición por su identificador",
           "Cada entorno de ejecución escribe en un log stream dentro del log group de la función. El identificador que "
           "devuelve la respuesta lleva a sus líneas de log y a su REPORT.")
    sw, sh = shot(sl, "shot-cw-streams.png", 43, 152, w=400, kind="oficial", tag_w=210)
    text(sl, 43, 152 + sh + 4, 400, 24, "Log streams de un log group: uno por entorno de ejecución (captura oficial de la guía de Lambda).",
         size=8.5, color=MUTED)
    hier = [("r-cw-logs.png", "Log group", "/aws/lambda/<función>, retención de 7 días en la referencia."),
            ("g-logs.png", "Log stream", "Uno por entorno: si Lambda escala, hay varios."),
            ("g-document.png", "Eventos", "START, nuestra línea JSON, END y REPORT de cada invocación.")]
    y = 336
    for ic, t, b in hier:
        img(sl, ic, 43, y + 2, w=24, h=24)
        text(sl, 75, y, 368, 30, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=9.5, color=TEXT)
        y += 34
    box(sl, 457, 134, 460, 196, fill=CARD, line=BORDER)
    tag(sl, 467, 142, "ilustrativo", w=210, t="FORMA DE LAS LÍNEAS · sin valores medidos")
    lines_ = ['START RequestId: 3f1c… Version: 3',
              '{"request_id": "3f1c…", "status": 200,',
              ' "duration_ms": …, "model_duration_ms": …,',
              ' "first_in_environment": true, "error": null}',
              'END RequestId: 3f1c…',
              'REPORT RequestId: 3f1c… Duration: … ms',
              '  Billed Duration: … ms  Memory Size: 512 MB',
              '  Max Memory Used: … MB  Init Duration: … ms']
    code_block(sl, 467, 164, 444, lines_, size=8.5, pitch=12.5)
    text(sl, 467, 268, 444, 58, "La respuesta HTTP trae x-request-id = RequestId de Lambda. Con él filtramos el log group y unimos "
                               "nuestra línea JSON con el REPORT. Init Duration solo aparece si el entorno era nuevo.", size=9.5, color=TEXT)
    box(sl, 457, 340, 225, 126, fill=VIOLET_BG)
    text(sl, 467, 348, 205, 12, "MÉTRICAS", size=8.5, color=VIOLET, bold=True)
    text(sl, 467, 364, 205, 100, "Duration, Errors, Throttles y ConcurrentExecutions de la función; Count, 4xx, 5xx y Latency "
                                "de la API. Resumen en el tiempo, no el detalle de una petición.", size=9.5, color=TITLE)
    box(sl, 692, 340, 225, 126, fill=AMBER_BG)
    img(sl, "r-cw-alarm.png", 702, 348, w=20, h=20)
    text(sl, 728, 351, 180, 12, "ALARMAS (CONCEPTO)", size=8.5, color=AMBER, bold=True)
    text(sl, 702, 374, 205, 90, "Una regla sobre una métrica, por ejemplo Errors > 0 durante 5 minutos, pasa a ALARM y notifica. "
                               "Hoy no creamos ninguna.", size=9.5, color=TITLE)
    takeaway(sl, "El identificador de la respuesta lleva al log de la función y a su REPORT: duración, facturación, memoria e Init Duration.",
             "Idea guía")
    footer(sl, block=4)
    notes(sl, """
""" + timing_note("19:25", "19:28") + """
QUÉ EXPLICAR: Log groups y log streams: la función escribe en /aws/lambda/<función> (retención de 7 días en la plantilla); cada entorno de ejecución tiene su log stream. Registros de ejecución: START, nuestra línea JSON (request_id, versión, execution, status, duration_ms, model_duration_ms, first_in_environment, error; sin texto de la incidencia ni headers), END y REPORT (Duration, Billed Duration, Memory Size, Max Memory Used e Init Duration si el entorno era nuevo). Seguir una petición: la respuesta trae x-request-id (RequestId de Lambda); con él se busca en el log group o en Logs Insights. Métricas: Duration, Errors, Throttles y ConcurrentExecutions de Lambda; Count, 4xx, 5xx y Latency de la API. Alarmas como concepto: umbral sobre una métrica que cambia a ALARM y notifica; no creamos ninguna hoy. Las líneas de la diapositiva muestran la forma, no valores medidos.
CONSOLA: CloudWatch › Logs › Log groups › /aws/lambda/(función, si existe) › Log streams; Search log group con un RequestId. CloudWatch › Metrics › All metrics › Lambda › By Function Name. CloudWatch › Alarms: ver la lista sin crear. Si no hay función del laboratorio, abrir cualquier log group existente y explicar con la captura oficial.
PREGUNTA: «Hay un 403 en el cliente. ¿Encontraremos su RequestId en el log group de Lambda?». Respuesta: no; la petición no llegó a la función.
FUENTES: AWS Lambda Developer Guide, «Viewing CloudWatch logs for Lambda functions» (RequestId, Duration, Billed Duration, Memory Size, Max Memory Used, Init Duration) y «Types of metrics for Lambda functions»; API Gateway Developer Guide, «Monitor HTTP APIs with CloudWatch metrics»; Amazon CloudWatch User Guide, «Using Amazon CloudWatch alarms», consultadas el 06/11/2026. src/curso_ia/serverless/handler.py (línea JSON y x-request-id); """ + SRC_TEMPLATE + """
IMÁGENES: captura oficial log-stream.png de la AWS Lambda Developer Guide, sin modificar. """ + SRC_AWS_ICONS + " Recursos CloudWatch Logs y Alarm; genéricos Logs y Document.")
    return sl


def s29_diagnostico(d):
    sl = d.slide(tag="diagnostico")
    header(sl, "Diagnóstico", "¿En qué capa falló? Cuatro tipos de error",
           "El mismo «no funciona» puede nacer en cuatro capas. El código HTTP y la presencia o ausencia de un log de "
           "Lambda indican dónde mirar primero.")
    cols = [("1 · Autorización", "Antes de Lambda", VIOLET, VIOLET_BG,
             [("403", "sin firma, firma inválida o sin execute-api:Invoke"), ("429", "throttling de la ruta o de la cuenta")],
             "No hay log de Lambda. Revisar credenciales, región, servicio de firma y permiso de la ruta."),
            ("2 · Validación", "Dentro del handler", AMBER, AMBER_BG,
             [("400", "JSON o base64 mal formado"), ("413", "cuerpo mayor de 8 KiB"), ("415", "Content-Type distinto de JSON"),
              ("422", "esquema inválido")],
             "Hay log con error y sin llamada al modelo: no hay tokens."),
            ("3 · Invocar Bedrock", "Llamada al modelo", PINK, PINK_BG,
             [("502", "bedrock_denegado: rol, perfil o regiones"), ("502", "modelo no disponible o salida inválida"),
              ("503", "bedrock_limitado: cuota del modelo")],
             "Un intento, sin reintento oculto. Puede haber consumo aunque falle."),
            ("4 · Límite o timeout", "Plazos y concurrencia", BLUE, BLUE_BG,
             [("504", "presupuesto_tiempo_agotado antes de llamar"), ("504", "bedrock_timeout tras 15 s de lectura"),
              ("—", "Throttles de Lambda si hay más de 2 ejecuciones")],
             "Cruzar request ID, tiempo total y REPORT. El corte de la integración llega a los 29 s.")]
    w = (874 - 3 * 10) / 4
    for i, (t, sub, col, bg, codes, tip) in enumerate(cols):
        x = 43 + i * (w + 10)
        box(sl, x, 132, w, 334, fill=bg)
        box(sl, x, 132, w, 4, fill=col, radius=0)
        text(sl, x + 10, 142, w - 20, 16, t, size=12, color=TITLE, bold=True)
        text(sl, x + 10, 160, w - 20, 13, sub, size=9, color=col, bold=True)
        y = 182
        for c, b in codes:
            box(sl, x + 10, y, 38, 20, fill=col, radius=3)
            text(sl, x + 10, y + 3, 38, 14, c, size=10, font=MONO, color=DARK, bold=True, align="c", check=False)
            text(sl, x + 54, y - 1, w - 62, 44, b, size=9.5, color=TITLE)
            y += 48
        box(sl, x + 8, 380, w - 16, 78, fill=CARD, radius=4)
        text(sl, x + 16, 386, w - 32, 70, tip, size=9.5, color=TEXT)
    takeaway(sl, "Siempre: request ID, capa y código. No repetir llamadas de pago para diagnosticar lo que puede leerse en los logs.",
             "Idea guía")
    footer(sl, block=4)
    notes(sl, """
""" + timing_note("19:28", "19:30") + """
QUÉ EXPLICAR: cuatro capas de error. 1) Autorización antes de Lambda: 403 (sin firma o sin permiso) o 429 (throttling); no hay log de la función. 2) Validación dentro del handler: 400, 413, 415 o 422 antes de llamar al modelo; hay log, no hay tokens. 3) Error al invocar Bedrock: 502 bedrock_denegado (rol, perfil o regiones), 502 por modelo no disponible o salida inválida, 503 bedrock_limitado; un solo intento sin reintento oculto; puede haber consumo aunque falle. 4) Límite o timeout: 504 presupuesto_tiempo_agotado (no se llama al modelo si quedan menos de 20 s), 504 bedrock_timeout (15 s de lectura), throttles de Lambda por la reserva de 2 y el corte de la integración a los 29 s. Los mensajes remotos no se devuelven al alumno: el handler devuelve códigos saneados.
CÓDIGO: la tabla de la guía del alumno (sección 3) y las pruebas tests/test_s17.py prueban estos caminos con dobles, sin AWS. Opcional: uv run pytest tests/test_s17.py -q. Los dobles prueban la lógica, no la disponibilidad real de AWS.
CONSOLA: CloudWatch › Logs › Log groups › (función) › Search log group: buscar "error" en las líneas JSON. Lambda › Monitor: Errors y Throttles.
PREGUNTA: «Un 504 con model_duration_ms nulo, ¿se llegó a llamar al modelo?». Respuesta: no; es el presupuesto de tiempo agotado antes de invocar.
FUENTES: src/curso_ia/serverless/handler.py y bedrock.py (mapa de errores); material/S17/guia-alumno.md (tabla de situaciones); API Gateway Developer Guide, «Throttle requests to your HTTP APIs» (429), consultada el 06/11/2026.
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


def s30_div5(d):
    sl = divider(d, 5, "Latencia y límites", "Dónde se va el tiempo y qué corta cada capa",
                 "Arranque en frío, relojes que se superponen, timeouts encadenados, concurrencia y tamaño de las peticiones.",
                 ["¿Qué demuestra un cold start y qué no?",
                  "¿Qué mide cada reloj y por qué no se suman?",
                  "¿Qué timeout debe saltar primero?",
                  "¿Reservar concurrencia precalienta entornos?"],
                 [("aws-lambda.png", "Inicialización\ny ejecución"), ("aws-apigw.png", "Plazo de la\nintegración"),
                  ("aws-cloudwatch.png", "REPORT e\nInit Duration")], "19:30–19:40 · 10 min")
    notes(sl, """
TIEMPO 19:30 (10 s). Bloque 5 de 7: latencia y límites, de 19:30 a 19:40 (10 min).
QUÉ EXPLICAR: cuatro ideas con infografías: frío y caliente, relojes superpuestos, timeouts encadenados y límites del laboratorio.
CONSOLA: ninguna en el separador.
PREGUNTA: «Si la primera petición tarda más, ¿es siempre un cold start?»
FUENTES: temario AI Engineer y guion de S17 (material/S17/guion-profesor.md), con la distribución de tiempos de esta versión.
IMÁGENES: """ + SRC_AWS_ICONS)
    return sl


def s31_frio(d):
    sl = d.slide(tag="frio")
    header(sl, "Cold start", "Arranque en frío frente a entorno reutilizado",
           "Si no hay un entorno disponible, Lambda crea uno: descarga el código, arranca el runtime y ejecuta la "
           "inicialización antes del handler. Si reutiliza uno, solo ejecuta el handler.")
    sw, sh = shot(sl, "shot-coldstart.png", 43, 152, w=430, kind="diagrama", tag_w=230)
    text(sl, 43, 152 + sh + 4, 430, 24, "Fases de una invocación en frío (azul) y de la ejecución (naranja). Fuente: AWS Lambda Developer Guide.",
         size=8.5, color=MUTED)
    tag(sl, 43, 274, "ilustrativo", w=180, t="ESQUEMA · duraciones no medidas")
    rows = [("Frío", [("Init", 0.32, BLUE), ("Handler: validar + Bedrock + responder", 0.68, AMBER)]),
            ("Caliente", [("Handler: validar + Bedrock + responder", 0.68, AMBER)])]
    y = 296
    for lab, segs in rows:
        text(sl, 43, y + 4, 70, 14, lab, size=10.5, color=TITLE, bold=True)
        x = 113
        for t, frac, col in segs:
            wseg = 360 * frac
            box(sl, x, y, wseg, 24, fill=col, radius=3)
            text(sl, x + 6, y + 5, wseg - 10, 14, t, size=8.5, color=DARK, bold=True, check=False)
            x += wseg + 2
        y += 34
    text(sl, 43, 370, 430, 96, "El código fuera del handler (importar el SDK, crear el cliente) se ejecuta en Init. Un paquete "
                               "más pequeño y una inicialización ligera acortan el frío. La concurrencia provisionada lo evita "
                               "pagando entornos preparados.", size=10, color=TEXT)
    cards = [("Cómo se acredita", "Con Init Duration en el REPORT del mismo RequestId. first_in_environment es una pista del "
              "proceso, no la prueba.", MINT),
             ("La primera no basta", "La primera petición que enviamos puede llegar a un entorno que ya estaba caliente. "
              "No se etiqueta como fría por su posición en la tabla.", AMBER),
             ("Facturación", "Desde el 01/08/2025, Billed Duration incluye la fase INIT en funciones ZIP con runtime "
              "gestionado. No hay que sumarla otra vez.", BLUE),
             ("Lo que pide la práctica", "Al menos cinco peticiones calientes y un frío acreditado, o declarar que no se capturó.", VIOLET)]
    y = 134
    for t, b, col in cards:
        side_note(sl, 489, y, 428, 76, t, b, accent=col, size=9.5)
        y += 83
    takeaway(sl, "Un cold start se demuestra con Init Duration en el REPORT, no por ser la primera fila de la tabla.", "Idea guía")
    footer(sl, block=5)
    notes(sl, """
""" + timing_note("19:30", "19:33") + """
QUÉ EXPLICAR: inicialización fría frente a entorno reutilizado. En frío, Lambda descarga el código, arranca el entorno y ejecuta el código de inicialización (fuera del handler) antes de ejecutar el handler; en caliente solo ejecuta el handler. Evidencia: el REPORT del mismo RequestId incluye Init Duration solo cuando hubo inicialización; first_in_environment es una pista del proceso. La primera petición observada no demuestra por sí sola un cold start: puede llegar a un entorno ya caliente. Facturación: desde el 1 de agosto de 2025 la fase INIT se incluye en Billed Duration también para funciones ZIP con runtime gestionado; usar Billed Duration para costes sin sumar Init otra vez. La práctica exige al menos cinco peticiones calientes y un cold acreditado, o declarar «no capturado». No inventar una duración fría ni inferir una frecuencia de fríos de una muestra de seis.
CONSOLA: CloudWatch › Logs › (log group) › un REPORT con Init Duration si existe; si no, la captura de log streams de la diapositiva anterior. No generar invocaciones para conseguir un frío.
PREGUNTA: «La primera fila de mi tabla tardó más. ¿Es un cold start?». Respuesta: solo si su REPORT trae Init Duration.
FUENTES: AWS Lambda Developer Guide, «Lambda execution environment» (cold starts y cobro de INIT) y «Understanding Lambda function scaling»; AWS Compute Blog, «AWS Lambda standardizes billing for INIT Phase» (efectivo el 01/08/2025), consultados el 06/11/2026. Ejercicio S17 (cinco peticiones calientes; no suponer que la primera fue fría).
IMÁGENES: diagrama oficial perf-optimize-figure-1.png de la AWS Lambda Developer Guide, sin modificar. Barras: esquema propio con proporciones no medidas.""")
    return sl


def s32_relojes(d):
    sl = d.slide(tag="relojes")
    header(sl, "Tiempos", "Tres relojes que se superponen",
           "El cliente, el handler y el modelo miden tramos anidados. Restarlos explica dónde se fue el tiempo; sumarlos "
           "lo cuenta dos veces.")
    tag(sl, 43, 134, "ilustrativo", w=220, t="ESQUEMA · proporciones no medidas")
    bars = [("Cliente", "http_duration_ms", 0, 1.0, MUTED, "red + API Gateway + (init si hubo) + handler + vuelta"),
            ("REPORT", "Billed Duration", 0.14, 0.80, BLUE, "lo que factura Lambda: handler e init si hubo"),
            ("Handler", "duration_ms (metadata)", 0.24, 0.66, AMBER, "trabajo dentro del handler; excluye init"),
            ("Modelo", "model_duration_ms", 0.30, 0.56, PINK, "paso del SDK: Converse completo"),
            ("Bedrock", "provider_latency_ms", 0.32, 0.50, VIOLET, "latencia que informa Bedrock, si existe")]
    X0, W = 195, 520
    y = 160
    for lab, field, start, end, col, desc in bars:
        text(sl, 43, y + 2, 72, 14, lab, size=10.5, color=TITLE, bold=True)
        text(sl, 43, y + 17, 150, 12, field, size=8, font=MONO, color=col, bold=True)
        box(sl, X0, y + 4, W, 22, fill=CARD2, radius=3)
        box(sl, X0 + W * start, y + 4, W * (end - start), 22, fill=col, radius=3)
        text(sl, X0 + W + 12, y, 198, 32, desc, size=9, color=TEXT)
        y += 40
    for f in (0.14, 0.24):
        line(sl, X0 + W * f, 158, X0 + W * f, 360, color=FAINT, w=0.75, dash=True, head="none")
    text(sl, X0 + W * 0.0, 360, 200, 12, "red y API Gateway", size=8, color=MUTED, check=False)
    text(sl, X0 + W * 0.15, 360, 100, 12, "init", size=8, color=BLUE, check=False)
    cards = [("No sumar", "model_duration_ms ya está dentro de duration_ms, que está dentro del tiempo del cliente.", AMBER),
             ("Restar", "Cliente − handler = red, API Gateway e init si hubo. Handler − modelo = nuestra validación y respuesta.", MINT),
             ("Comparar con cuidado", "S16 usaba Anthropic directo; S17, Nova en Bedrock. Esa comparación no aísla el efecto de la arquitectura.", CORAL)]
    w = (874 - 2 * 10) / 3
    for i, (t, b, col) in enumerate(cards):
        side_note(sl, 43 + i * (w + 10), 380, w, 86, t, b, accent=col, size=9.5)
    takeaway(sl, "Cada reloj contiene al siguiente. Para comparar arquitecturas, mismas entradas, mismo modelo y mismos parámetros.",
             "Idea guía")
    footer(sl, block=5)
    notes(sl, """
""" + timing_note("19:33", "19:35") + """
QUÉ EXPLICAR: tiempo total del cliente (http_duration_ms: red, API Gateway, inicialización si hubo, handler y vuelta), REPORT de Lambda (Duration y Billed Duration; esta incluye init cuando lo hubo), tiempo del handler (duration_ms de la metadata, excluye init), tiempo del modelo (model_duration_ms, el paso del SDK) y provider_latency_ms (metrics.latencyMs que informa Bedrock, si existe). Se superponen: no se suman. Restarlos sí aporta información. Comparaciones: S16 invocaba Anthropic directamente y la referencia S17 usa Nova en Bedrock; una diferencia de latencia o coste no puede atribuirse solo a Fargate frente a Lambda. Para aislar la arquitectura hay que mantener modelo, entrada y parámetros. Las barras son un esquema: no son mediciones.
CONSOLA: ninguna nueva.
PREGUNTA: «Si el cliente mide 2.000 ms y el modelo 1.500 ms, ¿el total es 3.500?». Respuesta: no; el modelo está dentro del total.
FUENTES: src/curso_ia/serverless/handler.py (duration_ms, model_duration_ms, provider_latency_ms) y evidencia.py; material/S17/guia-alumno.md (sección 9); AWS Lambda Developer Guide, «Viewing CloudWatch logs» (Duration excluye INIT), consultada el 06/11/2026.
IMÁGENES: diapositiva sin imágenes externas; esquema propio.""")
    return sl


def s33_timeouts(d):
    sl = d.slide(tag="timeouts")
    header(sl, "Timeouts", "Un timeout en cada capa: debe saltar primero el de dentro",
           "Cada capa espera un máximo. Para devolver un error controlado, la capa interior tiene que rendirse antes de "
           "que la exterior corte la conexión.")
    tag(sl, 43, 134, "referencia", w=220)
    X0, S = 195, 14.6  # puntos por segundo
    for s_ in range(0, 37, 5):
        x = X0 + s_ * S
        line(sl, x, 156, x, 340, color=BORDER, w=0.5, head="none")
        text(sl, x - 10, 342, 20, 12, f"{s_} s", size=8, color=MUTED, align="c", check=False)
    bars = [("Cliente", 0, 35, MUTED, "35 s"), ("Integración HTTP API", 0, 29, AMBER, "29 s"),
            ("Lambda", 0, 24, BLUE, "24 s"), ("SDK · conexión", 0, 2, PINK, "2 s"), ("SDK · lectura", 2, 17, PINK, "15 s")]
    y = 160
    for lab, a, b, col, v in bars:
        text(sl, 43, y + 4, 150, 14, lab, size=10, color=TITLE, bold=True)
        box(sl, X0 + a * S, y, (b - a) * S, 24, fill=col, radius=3)
        text(sl, X0 + a * S + 6, y + 5, 60, 14, v, size=9.5, color=DARK, bold=True, check=False)
        y += 34
    line(sl, X0 + 30 * S, 152, X0 + 30 * S, 340, color=CORAL, w=1.5, dash=True, head="none")
    text(sl, X0 + 30 * S - 70, 362, 140, 24, "30 s: máximo documentado de la integración HTTP API", size=8, color=CORAL, align="c")
    box(sl, 43, 394, 400, 72, fill=AMBER_BG)
    text(sl, 53, 400, 380, 62, [[("Margen antes de llamar  ", {"bold": True, "color": AMBER}),
                                  ("si quedan menos de 20 s (de Lambda o de los 29 s desde que entró en API Gateway), el handler "
                                   "no llama al modelo y responde 504.", {})]], size=9.5, color=TITLE)
    notes_ = [("Lambda no amplía el gateway", "Subir el timeout de Lambda no cambia los 30 s de la integración HTTP API."),
              ("Timeout no es cancelación", "Una llamada cortada puede haber consumido inferencia: no presupone gasto cero ni que el trabajo remoto se detuviera."),
              ("Trabajos largos", "Patrón asíncrono: aceptar, guardar estado y consultar el resultado después.")]
    y = 394
    for i, (t, b) in enumerate(notes_):
        x = 455 + i * 156
        box(sl, x, y, 150, 72, fill=CARD)
        text(sl, x + 8, y + 6, 136, 26, t, size=9, color=TITLE, bold=True)
        text(sl, x + 8, y + 32, 136, 40, b, size=8, color=TEXT)
    takeaway(sl, "35 > 29 > 24 > 2 + 15 s: cada capa interior termina antes para que el cliente reciba un error controlado, no un corte.",
             "Idea guía")
    footer(sl, block=5)
    notes(sl, """
""" + timing_note("19:35", "19:37") + """
QUÉ EXPLICAR: timeouts encadenados de la referencia: cliente 35 s, integración HTTP 29 s (máximo documentado de HTTP API: 30 s), Lambda 24 s, SDK 2 s de conexión y 15 s de lectura, un intento. Antes de llamar al modelo, el handler exige 20 s de margen respecto al tiempo restante de Lambda y a los 29 s contados desde que API Gateway recibió la petición (la inicialización fría también consume ese plazo). Ideas: subir Lambda no amplía el gateway; un timeout no garantiza cancelación remota ni gasto cero; para investigaciones largas, patrón asíncrono (inicio, estado y resultado). Estos valores son decisiones del ejemplo, no recomendaciones generales de AWS.
CONSOLA: API Gateway › (API) › Integrations › Timeout; Lambda › Configuration › General configuration › Timeout. Solo señalar.
PREGUNTA: «¿Por qué 24 s de Lambda no autorizan una investigación de varios minutos detrás de esta HTTP API?». Respuesta: la integración corta a los 30 s como máximo; hay que cambiar el patrón de trabajo.
FUENTES: API Gateway Developer Guide, «Quotas for configuring and running an HTTP API» (Maximum integration timeout: 30 seconds), consultada el 06/11/2026; """ + SRC_TEMPLATE + """ src/curso_ia/serverless/bedrock.py (connect_timeout=2, read_timeout=15, total_max_attempts=1) y handler.py (margen de 20 s). Cliente de 35 s: scripts/aws_s17.py (httpx.Client(timeout=35)).
IMÁGENES: diapositiva sin imágenes externas; esquema propio a escala de segundos.""")
    return sl


def s34_concurrencia(d):
    sl = d.slide(tag="concurrencia")
    header(sl, "Concurrencia", "Concurrencia reservada frente a provisionada",
           "Reservar concurrencia limita y garantiza capacidad para una función. Provisionarla mantiene entornos ya "
           "inicializados. Son decisiones distintas, con costes distintos.")
    sw, sh = shot(sl, "shot-conc.png", 43, 152, w=490, kind="diagrama", tag_w=230)
    text(sl, 43, 152 + sh + 3, 520, 24, "Reservada: tras inactividad, la petición paga Init. Provisionada: entornos ya "
                                        "inicializados (t1). Fuente: AWS Lambda Developer Guide.",
         size=8.5, color=MUTED)
    rows = [["", "Reservada", "Provisionada"],
            ["Qué es", "Máximo y reserva de ejecuciones simultáneas", "Entornos preinicializados"],
            ["Cold start", "Posible: los entornos se crean bajo demanda", "Se evita en los entornos preparados"],
            ["Coste", "Sin cargo adicional", "Cargo adicional por tenerlos preparados"],
            ["En la referencia", "2 (y la cuenta conserva 100 sin reservar)", "No se usa"]]
    table(sl, 43, 372, 520, [100, 210, 210], rows, size=9, row_h=18.5, bold_cols=(0,), colors={0: TITLE})
    cards = [("Cuota de la cuenta", "1.000 ejecuciones simultáneas por región por defecto, compartidas por todas las funciones.", BLUE),
             ("Al superar la reserva", "Con 2 reservadas, la tercera ejecución simultánea recibe throttle; no se encola en una "
              "llamada síncrona desde API Gateway.", AMBER),
             ("Antes de desplegar", "El preflight comprueba que la cuota permita reservar 2 y dejar 100 sin reservar. Si no, se "
              "pide una cuenta adecuada; no se quita el límite en silencio.", VIOLET)]
    y = 134
    for t, b, col in cards:
        side_note(sl, 577, y, 340, 106, t, b, accent=col, size=10)
        y += 113
    takeaway(sl, "Reservar 2 limita y garantiza capacidad; no deja dos entornos calientes esperando. Eso es la concurrencia provisionada.",
             "Idea guía")
    footer(sl, block=5)
    notes(sl, """
""" + timing_note("19:37", "19:39") + """
QUÉ EXPLICAR: reservada frente a provisionada con el diagrama oficial. Reservada: define el máximo y reserva esa parte de la cuota para la función; los entornos se crean bajo demanda, así que hay cold starts; no tiene coste adicional. Provisionada: Lambda preinicializa entornos antes de recibir peticiones; evita el cold start en esos entornos y tiene cargo adicional. La referencia reserva 2 (protege el presupuesto y la cuota de Bedrock) y no usa provisionada. Cuota: 1.000 por región y cuenta por defecto; siempre quedan 100 sin reservar. Con una invocación síncrona desde API Gateway, superar la reserva produce throttle (no hay cola).
CONSOLA: Lambda › (función) › Configuration › Concurrency and recursion detection: Reserved concurrency y, debajo, Provisioned concurrency configurations (vacío). No editar.
PREGUNTA: «¿Reservar concurrencia evita los cold starts?». Respuesta: no; para eso está la provisionada, con coste.
FUENTES: AWS Lambda Developer Guide, «Lambda concurrency» (tabla comparativa y diagrama) y «Configuring reserved concurrency», consultadas el 06/11/2026. """ + SRC_TEMPLATE + """ Preflight de la referencia (scripts/aws_s17 preflight).
IMÁGENES: diagrama oficial concurrency-7-reserved-vs-provisioned.png de la AWS Lambda Developer Guide, sin modificar.""")
    return sl


def s35_limites(d):
    sl = d.slide(tag="limites")
    header(sl, "Límites antes de gastar", "Entrada, tokens, reintentos y concurrencia",
           "La referencia fija límites más estrechos que los de AWS para que el comportamiento y el coste sean explicables. "
           "Son decisiones del ejemplo, no límites universales.")
    rows = [["Qué limitamos", "Referencia S17", "Límite documentado (06/11/2026)", "Para qué"],
            ["Cuerpo de la petición", "8 KiB", "HTTP API: 10 MB de payload · Lambda síncrona: 6 MB", "Rechazar con 413 antes del modelo"],
            ["Texto de la incidencia", "5–2.000 caracteres", "Lo decide nuestro contrato", "Acotar tokens de entrada"],
            ["Tokens de salida", "maxTokens = 300", "Nova 2 Lite: hasta 64K", "Acotar coste y duración"],
            ["Reintentos del SDK", "1 intento total", "Sin configurar, botocore aplica sus reintentos", "Evitar gasto repetido oculto"],
            ["Concurrencia", "2 reservadas", "1.000 por región y cuenta (por defecto)", "Proteger presupuesto y cuota"],
            ["Ritmo de la ruta", "2 solicitudes/s, ráfaga 2", "10.000/s y ráfaga 5.000 por cuenta y región", "Frenar ráfagas antes de Lambda"],
            ["Duración", "Lambda 24 s · integración 29 s", "Lambda 900 s · integración HTTP API 30 s", "Error controlado antes del corte"]]
    table(sl, 43, 134, 874, [150, 170, 300, 254], rows, size=9.5, row_h=32, bold_cols=(0,), colors={0: TITLE, 1: MINT_L})
    tag(sl, 193, 400, "referencia", w=170)
    tag(sl, 363 + 8, 400, "documentado", w=226)
    text(sl, 43, 422, 874, 44, "Antes de presentarlos como recomendación general hay que comprobar la documentación vigente: las cuotas "
                               "cambian, varían por región y algunas pueden ampliarse. Tamaño de entrada, tokens y reintentos son los "
                               "tres mandos que más mueven la latencia y el coste de cada petición.", size=9.5, color=TEXT)
    takeaway(sl, "Los límites del laboratorio no son límites de AWS: son decisiones para que una petición tenga un coste y un tiempo acotados.",
             "Idea guía")
    footer(sl, block=5)
    notes(sl, """
""" + timing_note("19:39", "19:40") + """
QUÉ EXPLICAR: leer la tabla por filas: el valor de la referencia frente al límite documentado por AWS. Cuerpo 8 KiB (HTTP API admite 10 MB y Lambda síncrona 6 MB), texto de 5 a 2.000 caracteres (contrato), salida de 300 tokens (Nova 2 Lite admite hasta 64K), un intento total del SDK (total_max_attempts=1, cero reintentos adicionales; sin esa configuración, botocore reintenta según su modo), 2 de concurrencia reservada (cuota por defecto 1.000), throttling de la ruta 2/s y ráfaga 2 (cuenta: 10.000/s y ráfaga 5.000), duración 24/29 s frente a 900/30 s. Tamaño de entrada, tokens y reintentos determinan la latencia y el coste de cada petición. Comprobar la documentación vigente antes de recomendarlos en general.
CONSOLA: ninguna nueva.
PREGUNTA: «¿Qué límite protege más el coste: los 8 KiB o los 300 tokens?». Respuesta: en este ejemplo, los 300 tokens de salida, que es la partida más cara por token.
FUENTES: API Gateway Developer Guide, «Quotas for configuring and running an HTTP API» (10 MB, 30 s) y «Amazon API Gateway quotas» (10.000 rps, ráfaga 5.000); AWS Lambda Developer Guide, «Lambda quotas» (6 MB síncrona, 900 s) y «Lambda concurrency» (1.000); ficha «Nova 2 Lite» (64K), consultadas el 06/11/2026. src/curso_ia/serverless/handler.py (MAX_BODY_BYTES=8192), contratos.py (2.000 caracteres), bedrock.py (maxTokens y total_max_attempts) y """ + SRC_TEMPLATE + """
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


PART4 = [s25_div4, s26_permisos, s27_sigv4, s28_cloudwatch, s29_diagnostico,
         s30_div5, s31_frio, s32_relojes, s33_timeouts, s34_concurrencia, s35_limites]
