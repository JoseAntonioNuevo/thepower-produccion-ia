"""Diapositivas 16–24: bloque 3 (AWS Lambda y API Gateway)."""
from deck_lib import *  # noqa: F401,F403
from deck_part1 import SRC_AWS_ICONS

SRC_TEMPLATE = "Plantilla infra/s17/servicio.json de la referencia (Python 3.12 x86_64, 512 MB, 24 s, reserva 2, alias aula, ruta POST /clasificar con AWS_IAM, payload 2.0, 29.000 ms, throttling 2/2)."
SRC_APIGW_SHOTS = ("Capturas oficiales del tutorial «Create a CRUD API with Lambda and DynamoDB» de la API Gateway Developer Guide "
                   "(ddb-create-routes.png, ddb-attach-integrations.png, ddb-invoke-url.png), recortadas sin alterar su contenido. "
                   "Los nombres y valores son los del tutorial (us-west-1), no los de nuestra API.")


def s16_div3(d):
    sl = divider(d, 3, "Lambda y API Gateway", "La función que ejecuta y la puerta que la expone",
                 "Funciones, código, configuración, permisos y concurrencia; después rutas, integraciones, autorización y stages.",
                 ["¿Qué recibe la función, qué valida y qué devuelve?",
                  "¿Qué configuramos: memoria, timeout, variables y rol?",
                  "¿Cómo llega una ruta HTTP hasta Lambda?",
                  "¿Qué diferencia hay entre recibir una petición y autorizarla?"],
                 [("aws-lambda.png", "AWS Lambda"), ("aws-apigw.png", "Amazon\nAPI Gateway"), ("r-lambda-fn.png", "Versión\ny alias")],
                 "19:00–19:20 · 20 min")
    notes(sl, """
TIEMPO 19:00 (10 s). Bloque 3 de 7: AWS Lambda y API Gateway, de 19:00 a 19:20 (20 min).
QUÉ EXPLICAR: primero la función (qué ejecuta y cómo se configura) y después la puerta HTTP (cómo llega la petición y quién puede entrar).
CONSOLA: abrir Lambda en eu-west-1 en una pestaña y API Gateway en otra.
PREGUNTA: «¿Qué parte del recorrido creéis que comprueba la autorización: API Gateway o Lambda?»
FUENTES: temario AI Engineer y guion de S17 (material/S17/guion-profesor.md), con la distribución de tiempos de esta versión.
IMÁGENES: """ + SRC_AWS_ICONS + " Recurso Lambda Function del mismo paquete.")
    return sl


def s17_lambda_consola(d):
    sl = d.slide(tag="lambda-consola")
    header(sl, "AWS Lambda", "La página de una función en la consola",
           "Lambda › Event functions lista las funciones de la región. Al abrir una, la consola reúne lo que AWS necesita "
           "para ejecutarla: código, runtime, configuración, permisos, versiones y monitorización.")
    ui_panel(sl, 43, 134, 520, 332, title="s17-clasificar", crumbs="Lambda  ›  Event functions  ›  s17-clasificar")
    tag(sl, 393, 137, "esquema", w=164)
    text(sl, 51, 186, 200, 12, "Function overview", size=9.5, color=UI_TEXT, bold=True, check=False)
    box(sl, 51, 202, 504, 92, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    box(sl, 63, 226, 120, 40, fill="FFFFFF", line="7D8998", lw=0.5, radius=3)
    img(sl, "aws-apigw.png", 69, 232, w=28, h=28)
    text(sl, 101, 232, 80, 28, "API Gateway\n(trigger)", size=8, color=UI_TEXT, bold=True, check=False)
    line(sl, 183, 246, 223, 246, color=UI_MUTED, w=1)
    box(sl, 225, 214, 170, 64, fill="FFFFFF", line=UI_ORANGE, lw=1, radius=3)
    img(sl, "aws-lambda.png", 233, 226, w=30, h=30)
    text(sl, 269, 224, 124, 30, "s17-clasificar\nLayers (0)", size=8.5, color=UI_TEXT, bold=True, check=False)
    line(sl, 395, 246, 425, 246, color=UI_MUTED, w=1, dash=True)
    box(sl, 427, 232, 116, 28, fill="FFFFFF", line="7D8998", lw=0.5, radius=3, dash=True)
    text(sl, 431, 239, 108, 14, "+ Add destination", size=8, color=UI_BLUE, align="c", check=False)
    tabs = ["Code", "Test", "Monitor", "Configuration", "Aliases", "Versions"]
    x = 51
    centers = []
    for i, t in enumerate(tabs):
        w = len(t) * 5.6 + 18
        box(sl, x, 304, w, 20, fill="FFFFFF" if i else UI_CARD, line="7D8998" if i == 0 else "DDE1E5", lw=0.5, radius=0)
        text(sl, x, 308, w, 12, t, size=8.5, color=UI_BLUE if i == 0 else UI_TEXT, bold=i == 0, align="c", check=False)
        centers.append(x + w / 2)
        x += w + 2
    for n, cx in zip([1, 2, 3, 4, 5], centers[:4] + [(centers[4] + centers[5]) / 2]):
        badge(sl, cx - 7, 288, n, fill=AMBER, d=14, size=8)
    box(sl, 51, 330, 504, 128, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    text(sl, 59, 336, 300, 12, "Runtime settings", size=9.5, color=UI_TEXT, bold=True, check=False)
    rs = [("Runtime", "Python 3.12"), ("Handler", "curso_ia.serverless.handler.lambda_handler"), ("Architecture", "x86_64")]
    y = 354
    for k, v in rs:
        text(sl, 59, y, 90, 12, k, size=8.5, color=UI_LABEL, bold=True, check=False)
        text(sl, 150, y, 400, 12, v, size=9, color=UI_TEXT, font=MONO if k == "Handler" else SANS, bold=k == "Handler", check=False)
        y += 18
    text(sl, 59, 412, 488, 40, "Nombre de función de ejemplo. El código llega como ZIP para Linux amd64; no se edita en el navegador.",
         size=8.5, color=UI_MUTED, check=False)
    ann = [("Code", "Editor y Runtime settings: runtime, handler y arquitectura deben coincidir con el ZIP."),
           ("Test", "Invoca la función con un evento de prueba. Ejecuta de verdad: hoy no lo pulsamos."),
           ("Monitor", "Métricas de invocaciones, duración, errores y throttles; enlace a CloudWatch Logs."),
           ("Configuration", "Memoria, timeout, variables, permisos, concurrencia y triggers."),
           ("Aliases y Versions", "Qué versión publicada invoca API Gateway a través del alias aula.")]
    y = 134
    for i, (t, b) in enumerate(ann):
        badge(sl, 577, y + 1, i + 1, fill=AMBER, d=16, size=8.5)
        text(sl, 601, y, 316, 50, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10, color=TEXT)
        y += 52
    box(sl, 577, 398, 340, 68, fill=CARD, line=BORDER)
    text(sl, 589, 405, 318, 58, [[("Nombre en la consola de 2026  ", {"bold": True, "color": AMBER}),
                                   ("Este tipo de función aparece como «Event function». Lambda Web Functions y MicroVMs son "
                                    "otros tipos que no usamos.", {})]], size=9.5, color=TITLE)
    takeaway(sl, "La página de la función reúne lo que AWS necesita para ejecutarla: código, runtime, configuración, permisos y versiones.",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:00", "19:03") + """
QUÉ EXPLICAR: Lambda › Event functions lista las funciones de la región (comprobar el selector de región). La página de una función tiene: Function overview (triggers → función → destinos), pestañas Code (editor y Runtime settings), Test (eventos de prueba), Monitor (métricas y logs), Configuration (general, variables, permisos, concurrencia, triggers…), Aliases y Versions. En la referencia el handler es curso_ia.serverless.handler.lambda_handler, runtime Python 3.12 y arquitectura x86_64; el código llega como ZIP construido para Linux amd64, porque las dependencias nativas del Mac no sirven en Lambda. Desde 2026 la documentación y la consola llaman «Event function» al tipo clásico; Lambda Web Functions (servidores HTTP en Node.js) y Lambda MicroVMs son otros tipos que no usamos.
CONSOLA: Lambda › Event functions. Si existe una función del laboratorio, abrirla y recorrer las pestañas sin pulsar Test ni Deploy. Si no existe, abrir «Create function» › «Author from scratch» para enseñar Function name, Runtime (Python 3.12), Architecture (x86_64) y «Change default execution role», y CANCELAR. No crear la función.
PREGUNTA: «¿Qué pasa si el handler configurado no coincide con el módulo del ZIP?». Respuesta: la invocación falla al importar; no llega a ejecutarse nuestro código.
FUENTES: AWS Lambda Developer Guide: «What is AWS Lambda?» (nota sobre Event Functions, Web Functions y MicroVMs), «Create a Lambda function with the console» y «Testing Lambda functions in the console», consultadas el 06/11/2026. """ + SRC_TEMPLATE + """
IMÁGENES: ESQUEMA propio de la página de la función (no es una captura). """ + SRC_AWS_ICONS)
    return sl


def s18_handler(d):
    sl = d.slide(tag="handler")
    header(sl, "Código y handler", "Qué recibe la función, qué valida, cómo llama al modelo y qué devuelve",
           "El handler es el punto de entrada. Recibe el evento de API Gateway y el contexto de la invocación, valida antes "
           "de gastar, hace una sola llamada a Bedrock y devuelve una respuesta controlada.")
    sw, sh = shot(sl, "shot-lambda-code.png", 43, 152, w=380, kind="oficial", tag_w=210,
                  caption="Pestaña Code con el ejemplo «Hello from Lambda» de la guía oficial: mismo esquema handler(event, context).",
                  cap_w=380)
    box(sl, 43, 348, 380, 118, fill=CARD, line=BORDER)
    text(sl, 55, 355, 360, 12, "EVENTO QUE ENTREGA HTTP API (FORMATO 2.0, RESUMIDO)", size=8.5, color=AMBER, bold=True)
    ev = ['{"version": "2.0", "routeKey": "POST /clasificar",',
          ' "rawPath": "/clasificar", "headers": {…},',
          ' "requestContext": {"requestId": "…",',
          '    "http": {"method": "POST"}, "timeEpoch": …},',
          ' "body": "{\\"texto\\": \\"…\\"}", "isBase64Encoded": false}']
    code_block(sl, 55, 372, 362, ev, size=8.5, pitch=12)
    box(sl, 437, 134, 480, 332, fill=CARD, line=BORDER)
    text(sl, 449, 142, 460, 12, "FRAGMENTO SIMPLIFICADO DE handler.py", size=9, color=AMBER, bold=True)
    code = ["def handle(event, context, cfg, client):",
            "    incoming = parse_event(event)",
            "    remaining = min(",
            "        context.get_remaining_time_in_millis(),",
            "        29000 - ms_desde(requestContext.timeEpoch))",
            "    if remaining < 20000:",
            "        raise FalloBedrock('presupuesto_tiempo_agotado', 504)",
            "    result, usage, latency = classify(incoming.texto, cfg)",
            "    payload = {'resultado': result,",
            "               'metadata': {'request_id': ..., 'consumo': usage}}",
            "    return {'statusCode': 200,",
            "            'headers': {'content-type': 'application/json'},",
            "            'body': json.dumps(payload)}"]
    p = code_block(sl, 471, 160, 440, code, size=8.5, pitch=13)
    for li, n in [(1, 1), (5, 2), (7, 3), (10, 4)]:
        line_badge(sl, 451, 160, p, li, n, AMBER)
    ann = [("Validar la entrada", "versión 2.0, ruta, Content-Type, 8 KiB y esquema; si falla, 400, 413, 415 o 422 sin llamar al modelo."),
           ("Comprobar margen", "con el tiempo restante de Lambda y el transcurrido desde que entró en API Gateway."),
           ("Una llamada", "classify() usa Converse una vez con toolConfig, sin reintentos; la salida se valida con Pydantic."),
           ("Respuesta proxy", "statusCode, headers y body; API Gateway la traduce a HTTP.")]
    y = 334
    for i, (t, b) in enumerate(ann):
        badge(sl, 451, y + 1, i + 1, fill=AMBER, d=13, size=7.5)
        text(sl, 470, y, 440, 30, [[(t + ": ", {"bold": True, "color": TITLE}), (b, {})]], size=9, color=TEXT)
        y += 31 if i < 3 else 26
    takeaway(sl, "El handler valida antes de gastar, hace una sola llamada al modelo y devuelve siempre una respuesta controlada.",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:03", "19:06") + """
QUÉ EXPLICAR: qué recibe la función (event: el JSON del formato 2.0 de HTTP API con version, routeKey, rawPath, headers, requestContext con requestId, http.method y timeEpoch, body e isBase64Encoded; context: request ID de Lambda y tiempo restante), qué valida (parse_event: versión 2.0, método POST y ruta /clasificar, Content-Type application/json, cuerpo de 8 KiB como máximo incluso en base64, JSON y esquema Incidencia de 5 a 2.000 caracteres), cómo llama al SDK (classify: un cliente bedrock-runtime cacheado, Converse con toolConfig, un solo intento) y qué devuelve (respuesta proxy con statusCode, headers con x-request-id y body JSON). Antes de llamar, exige 20 s de margen tanto respecto al tiempo restante de Lambda como a los 29 s de la integración, contando desde que API Gateway recibió la petición: la inicialización fría también consume ese plazo. El fragmento está simplificado: ms_desde() resume el cálculo real con time.time() y requestContext.timeEpoch.
CÓDIGO: abrir src/curso_ia/serverless/handler.py (parse_event, handle y lambda_handler) solo para estas cuatro marcas; no recorrer todo el repositorio.
CONSOLA: Lambda › (función) › Code › Runtime settings: señalar Handler. Opcional: Test › plantilla «API Gateway HTTP API» para ver la forma del evento, sin invocar.
DEMO LOCAL OPCIONAL (sin AWS): uv run python scripts/demo_s17.py. Señalar execution: demo, tokens nulos y el 422 de una entrada vacía. No convertir sus milisegundos en una medición de Bedrock.
PREGUNTA: «¿Por qué validamos antes de llamar a Bedrock?». Respuesta: para no gastar tokens ni tiempo en peticiones que vamos a rechazar.
FUENTES: src/curso_ia/serverless/handler.py y bedrock.py; API Gateway Developer Guide, «Create AWS Lambda proxy integrations for HTTP APIs» (payload format version 2.0), y AWS Lambda Developer Guide, «Create a Lambda function with the console», consultadas el 06/11/2026.
IMÁGENES: captura oficial python_code_editor.png de la AWS Lambda Developer Guide (tutorial de inicio), sin modificar. Código y evento: texto propio a partir del repositorio.""")
    return sl


def s19_config(d):
    sl = d.slide(tag="config")
    header(sl, "Configuration", "Memoria, timeout y variables de entorno",
           "En Configuration › General configuration fijamos la memoria (y con ella la CPU) y el timeout. En Environment "
           "variables, la configuración que cambia el comportamiento sin tocar el código.")
    ui_panel(sl, 43, 134, 470, 332, title="Edit basic settings", crumbs="Lambda  ›  s17-clasificar  ›  Configuration  ›  General configuration")
    tag(sl, 343, 137, "esquema", w=164)
    y = 190
    y = ui_field(sl, 53, y, 200, "Memory", "512 MB", hint="128 MB – 10,240 MB") + 10
    y = ui_field(sl, 53, y, 200, "Ephemeral storage", "512 MB", hint="512 MB – 10,240 MB") + 10
    y = ui_field(sl, 53, y, 200, "Timeout", "0 min  24 sec", hint="Default 3 sec · max 15 min") + 10
    text(sl, 53, y, 200, 12, "Execution role", size=8.5, color=UI_LABEL, bold=True, check=False)
    text(sl, 53, y + 13, 210, 24, "Use an existing role: rol de la función (ver Permissions)", size=8, color=UI_MUTED, check=False)
    badge(sl, 236, 190, 1, fill=AMBER, d=14, size=8)
    badge(sl, 236, 288, 2, fill=AMBER, d=14, size=8)
    box(sl, 271, 186, 234, 228, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    text(sl, 279, 192, 220, 12, "Environment variables (4)", size=9.5, color=UI_TEXT, bold=True, check=False)
    badge(sl, 487, 191, 3, fill=AMBER, d=14, size=8)
    env = [("BEDROCK_MODEL_ID", "eu.amazon.nova-2-lite-v1:0"), ("S17_MODE", "real"),
           ("APP_VERSION", "s17-…"), ("S17_MAX_OUTPUT_TOKENS", "300")]
    y2 = 214
    for k, v in env:
        box(sl, 279, y2, 218, 40, fill="FFFFFF", line="7D8998", lw=0.5, radius=2)
        text(sl, 285, y2 + 4, 206, 12, k, size=8.5, font=MONO, color=UI_TEXT, bold=True, check=False)
        text(sl, 285, y2 + 20, 206, 12, v, size=8.5, font=MONO, color=UI_BLUE, check=False)
        y2 += 46
    ui_button(sl, 359, 432, 60, "Cancel")
    ui_button(sl, 425, 432, 80, "Save", primary=True)
    chip(sl, 53, 432, 170, 16, "en clase: Cancel, no Save", fill=CORAL, color=DARK, size=7.5, radius=3)
    cards = [("Memoria = memoria y CPU", "Lambda asigna CPU en proporción a la memoria: con 1.769 MB, el equivalente a una vCPU. "
              "Más memoria puede acortar la duración, pero cada milisegundo cuesta más GB-s.", AMBER),
             ("Timeout", "Por defecto 3 s; máximo 900 s. La referencia fija 24 s para terminar antes de que la integración "
              "HTTP corte a los 29 s y poder devolver un error controlado.", BLUE),
             ("Variables, no secretos", "Modelo, modo y límite de tokens. No hay clave de API: Bedrock se autoriza con el rol de "
              "la función. Las variables suman como máximo 4 KB.", MINT)]
    y = 134
    for t, b, col in cards:
        side_note(sl, 527, y, 390, 106, t, b, accent=col, size=10)
        y += 113
    takeaway(sl, "Memoria y timeout son decisiones de coste y de latencia; las variables cambian el comportamiento sin redesplegar código.",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:06", "19:08") + """
QUÉ EXPLICAR: General configuration: Memory (128–10.240 MB; la CPU crece en proporción y a 1.769 MB equivale a una vCPU), Ephemeral storage (/tmp, 512–10.240 MB) y Timeout (por defecto 3 s; máximo 900 s). La referencia usa 512 MB y 24 s: el enunciado pide no dejar los 3 s por defecto y terminar antes del corte de la integración (29 s, máximo documentado de HTTP API 30 s). Environment variables: BEDROCK_MODEL_ID, S17_MODE, APP_VERSION y S17_MAX_OUTPUT_TOKENS (máximo 4 KB en total). No contienen secretos: el acceso a Bedrock lo da el rol de ejecución, no una clave copiada de S16. Más memoria puede reducir la duración sin garantizar menor coste: medir antes de cambiar.
CONSOLA: Lambda › (función) › Configuration › General configuration › Edit: señalar Memory, Ephemeral storage y Timeout y pulsar CANCEL. Configuration › Environment variables: leer los nombres (si la función existe). No guardar cambios.
PREGUNTA: «Si subo el timeout de Lambda a 60 s, ¿podrá la API esperar 60 s?». Respuesta: no; la integración de HTTP API corta antes (máximo 30 s).
FUENTES: AWS Lambda Developer Guide: «Configure Lambda function memory» (1.769 MB = 1 vCPU), «Configure Lambda function timeout» y «Lambda quotas» (memoria, /tmp, 900 s, 4 KB de variables), consultadas el 06/11/2026. """ + SRC_TEMPLATE + """ src/curso_ia/serverless/config.py (variables).
IMÁGENES: ESQUEMA propio del formulario (no es una captura).""")
    return sl


def s20_permisos(d):
    sl = d.slide(tag="permisos-lambda")
    header(sl, "Permissions", "Quién puede invocar la función y qué puede hacer ella",
           "Configuration › Permissions muestra dos políticas distintas. Una dice quién puede llamar a la función; "
           "la otra, a qué puede acceder la función cuando se ejecuta.")
    # diagrama central
    box(sl, 377, 178, 206, 150, fill=AMBER_BG, line=AMBER)
    img(sl, "aws-lambda.png", 452, 192, w=56, h=56)
    text(sl, 387, 256, 186, 16, "Función Lambda", size=12, color=TITLE, bold=True, align="c")
    text(sl, 387, 276, 186, 44, "alias aula → versión publicada", size=9.5, color=TEXT, align="c")
    # entrada
    box(sl, 43, 162, 300, 182, fill=CARD, line=BORDER)
    box(sl, 43, 162, 300, 4, fill=AMBER, radius=0)
    img(sl, "aws-apigw.png", 55, 176, w=30, h=30)
    text(sl, 93, 176, 240, 14, "ENTRADA · quién puede invocarla", size=9, color=AMBER, bold=True)
    text(sl, 93, 192, 240, 14, "Resource-based policy statements", size=9.5, color=TITLE, bold=True)
    text(sl, 55, 216, 280, 124, [{"runs": [("Principal  ", {"bold": True, "color": TITLE}), ("apigateway.amazonaws.com", {"font": MONO})], "space": 3},
                                 {"runs": [("Acción  ", {"bold": True, "color": TITLE}), ("lambda:InvokeFunction", {"font": MONO})], "space": 3},
                                 {"runs": [("Recurso  ", {"bold": True, "color": TITLE}), ("alias aula de la función", {})], "space": 3},
                                 {"runs": [("Condición  ", {"bold": True, "color": TITLE}), ("SourceArn de nuestra API y ruta; SourceAccount", {})], "space": 3}],
         size=9.5, color=TEXT, space=3)
    line(sl, 343, 253, 375, 253, color=AMBER, w=1.5)
    # salida
    box(sl, 617, 162, 300, 182, fill=CARD, line=BORDER)
    box(sl, 617, 162, 300, 4, fill=VIOLET, radius=0)
    img(sl, "r-iam-role.png", 629, 176, w=30, h=30)
    text(sl, 667, 176, 240, 14, "SALIDA · qué puede hacer", size=9, color=VIOLET, bold=True)
    text(sl, 667, 192, 240, 14, "Execution role", size=9.5, color=TITLE, bold=True)
    text(sl, 629, 216, 280, 124, [{"runs": [("Logs  ", {"bold": True, "color": TITLE}), ("logs:CreateLogStream y logs:PutLogEvents en su log group", {})], "space": 3},
                                  {"runs": [("Modelo  ", {"bold": True, "color": TITLE}), ("bedrock:InvokeModel sobre el perfil eu. y el modelo base en origen y destinos", {})], "space": 3},
                                  {"runs": [("Sin comodines  ", {"bold": True, "color": TITLE}), ("ni Resource: * para todos los modelos", {})], "space": 3}],
         size=9.5, color=TEXT, space=3)
    line(sl, 585, 253, 615, 253, color=VIOLET, w=1.5)
    img(sl, "aws-bedrock.png", 870, 300, w=34, h=34)
    img(sl, "r-cw-logs.png", 830, 300, w=34, h=34)
    console_path(sl, 43, 356, 874, "Lambda › (función) › Configuration › Permissions › Execution role (enlace a IAM) · Resource-based policy statements",
                 h=42)
    box(sl, 43, 406, 874, 60, fill=VIOLET_BG)
    text(sl, 55, 413, 852, 48, [[("Converse frente a la acción IAM  ", {"bold": True, "color": VIOLET}),
                                  ("Converse es el método del SDK; la acción que lo autoriza es ", {}),
                                  ("bedrock:InvokeModel", {"font": MONO, "bold": True, "color": MINT_L}),
                                  (". Para ConverseStream sería ", {}),
                                  ("bedrock:InvokeModelWithResponseStream", {"font": MONO, "bold": True, "color": MINT_L}),
                                  (". La política no usa bedrock:Converse.", {})]], size=10, color=TITLE)
    takeaway(sl, "La política de recursos responde «quién puede llamar a esta función»; el rol, «qué puede hacer la función al ejecutarse».",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:08", "19:10") + """
QUÉ EXPLICAR: dos políticas con direcciones opuestas. Entrada: la política basada en recursos de la función (Resource-based policy statements) permite a apigateway.amazonaws.com ejecutar lambda:InvokeFunction sobre el alias aula, limitado por SourceArn (nuestra API y ruta) y SourceAccount. Salida: el rol de ejecución (Execution role) es la identidad que asume la función; le damos permisos de CloudWatch Logs y bedrock:InvokeModel sobre el ARN del perfil eu.amazon.nova-2-lite-v1:0 y sobre el modelo base en las regiones de origen y destino, con la condición bedrock:InferenceProfileArn. Nada de Resource: * para todos los modelos. Converse se autoriza con bedrock:InvokeModel; ConverseStream, con bedrock:InvokeModelWithResponseStream. La política detallada está en el anexo de consulta.
CONSOLA: Lambda › (función) › Configuration › Permissions: señalar Execution role (nombre y enlace a IAM) y Resource-based policy statements (statement de API Gateway). Desde el enlace, IAM › Roles › (rol) › Permissions: abrir la política en vista JSON solo para señalar Action y Resource; no editar.
PREGUNTA: «Si el rol no tiene bedrock:InvokeModel, ¿qué ve el cliente?». Respuesta: un 502 bedrock_denegado de nuestra función, no un 403 de API Gateway.
FUENTES: AWS Lambda Developer Guide, «Lambda execution role» y «Working with resource-based IAM policies in Lambda»; Amazon Bedrock User Guide, «Using the Converse API» (Converse requiere bedrock:InvokeModel; ConverseStream, bedrock:InvokeModelWithResponseStream) y «Geographic cross-Region inference» (política de dos statements), consultadas el 06/11/2026. """ + SRC_TEMPLATE + """
IMÁGENES: """ + SRC_AWS_ICONS + " Recursos IAM Role y CloudWatch Logs del mismo paquete.")
    return sl


def s21_operar(d):
    sl = d.slide(tag="concurrencia-versiones")
    header(sl, "Concurrency, Monitor, Versions y Aliases", "Cuántas ejecuciones a la vez y qué versión exacta responde",
           "La concurrencia acota cuántas ejecuciones simultáneas puede tener la función. Las versiones congelan código y "
           "configuración; el alias es el nombre estable que invoca API Gateway.")
    # concurrencia
    box(sl, 43, 132, 280, 334, fill=CARD)
    box(sl, 43, 132, 280, 4, fill=BLUE, radius=0)
    text(sl, 55, 142, 260, 14, "Concurrencia reservada", size=12, color=TITLE, bold=True)
    text(sl, 55, 160, 260, 26, "Configuration › Concurrency and recursion detection", size=8.5, font=MONO, color=MINT_L, bold=True)
    text(sl, 55, 196, 260, 12, "CUOTA DE LA REGIÓN (POR DEFECTO): 1.000", size=8, color=MUTED, bold=True)
    box(sl, 55, 212, 256, 20, fill=CARD2, radius=2)
    box(sl, 55, 212, 3, 20, fill=BLUE, radius=0)
    box(sl, 55 + 256 * 0.9, 212, 256 * 0.1, 20, fill="2B4B57", radius=0)
    text(sl, 61, 236, 250, 30, [[("2 ", {"bold": True, "color": BLUE}), ("reservadas para esta función  ·  ", {}),
                                  ("100 ", {"bold": True, "color": TITLE}), ("siempre sin reservar", {})]], size=9, color=TEXT)
    text(sl, 55, 268, 256, 110, "Reservar 2 garantiza esa capacidad y es también el máximo: una tercera ejecución simultánea "
                               "se rechaza (throttle). No precalienta entornos ni tiene coste adicional.", size=10, color=TEXT)
    tag(sl, 55, 440, "referencia", w=230)
    # monitor
    box(sl, 335, 132, 280, 334, fill=CARD)
    box(sl, 335, 132, 280, 4, fill=VIOLET, radius=0)
    text(sl, 347, 142, 260, 14, "Monitor", size=12, color=TITLE, bold=True)
    text(sl, 347, 160, 260, 26, "Monitor › Metrics · View CloudWatch logs", size=8.5, font=MONO, color=MINT_L, bold=True)
    mets = [("Invocations", "cuántas veces se ejecutó"), ("Duration", "cuánto tardó el handler"),
            ("Errors", "excepciones o fallos de la función"), ("Throttles", "rechazos por concurrencia"),
            ("ConcurrentExecutions", "ejecuciones simultáneas")]
    y = 194
    for k, v in mets:
        img(sl, "g-metrics.png", 347, y + 2, w=18, h=18)
        text(sl, 373, y, 236, 13, k, size=9.5, font=MONO, color=TITLE, bold=True)
        text(sl, 373, y + 14, 236, 13, v, size=9, color=TEXT)
        y += 36
    text(sl, 347, 384, 256, 76, "Las métricas dicen cuánto y cuándo; el log de una invocación dice qué pasó en esa petición.",
         size=10, color=TEXT)
    # versiones y alias
    box(sl, 627, 132, 290, 334, fill=CARD)
    box(sl, 627, 132, 290, 4, fill=AMBER, radius=0)
    text(sl, 639, 142, 270, 14, "Versiones y alias", size=12, color=TITLE, bold=True)
    text(sl, 639, 160, 270, 26, "Aliases › aula · Versions", size=8.5, font=MONO, color=MINT_L, bold=True)
    chip(sl, 645, 196, 110, 26, "$LATEST (editable)", fill=CARD2, color=TITLE, size=9, line=BORDER, radius=4)
    line(sl, 700, 223, 700, 244, color=AMBER, w=1.25)
    text(sl, 706, 226, 120, 14, "publicar", size=8.5, color=AMBER)
    chip(sl, 645, 246, 110, 26, "Versión N (inmutable)", fill=AMBER_BG, color=TITLE, size=9, line=AMBER, radius=4)
    chip(sl, 790, 246, 110, 26, "alias aula", fill=TAKE_BG, color=MINT_L, size=9.5, line=MINT, radius=4)
    line(sl, 788, 259, 757, 259, color=MINT, w=1.25)
    img(sl, "aws-apigw.png", 832, 196, w=26, h=26)
    line(sl, 845, 223, 845, 244, color=MINT, w=1.25)
    text(sl, 639, 284, 270, 120, "Una versión congela código y configuración. API Gateway invoca el alias aula; para cambiar de versión se "
                                "mueve el alias sin tocar la integración. Cambiar la configuración con el mismo ZIP también crea otra versión.",
         size=10, color=TEXT)
    takeaway(sl, "La concurrencia acota cuántas ejecuciones hay a la vez; el alias fija qué versión exacta responde a la API.",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:10", "19:12") + """
QUÉ EXPLICAR: Concurrency: la cuenta tiene por defecto 1.000 ejecuciones simultáneas por región; se pueden reservar hasta 900 porque Lambda mantiene siempre 100 sin reservar. La referencia reserva 2: es mínimo garantizado y máximo para la función; una tercera ejecución simultánea recibe throttle. Reservar no precalienta entornos y no tiene coste adicional (eso sería concurrencia provisionada, bloque 5). Monitor: Invocations, Duration, Errors, Throttles y ConcurrentExecutions; desde aquí, View CloudWatch logs. Versions y Aliases: $LATEST es editable; publicar crea una versión inmutable (código + configuración); el alias aula apunta a una versión y API Gateway invoca el alias. El script estado de la referencia comprueba el CodeSha256 de la versión a la que apunta el alias. Empaquetado y publicación del ZIP, en el anexo.
CONSOLA: Lambda › (función) › Configuration › Concurrency and recursion detection (señalar Reserved concurrency, sin editar); Monitor (gráficos de Invocations, Duration, Errors, Throttles); Aliases › aula (versión a la que apunta) y Versions.
PREGUNTA: «¿Reservar 2 significa tener 2 entornos calientes esperando?». Respuesta: no; limita y reserva capacidad, pero los entornos se crean bajo demanda.
FUENTES: AWS Lambda Developer Guide: «Lambda concurrency» (1.000 por defecto, 100 sin reservar, comparativa reservada/provisionada), «Configuring reserved concurrency», «Lambda function versions», «Create an alias for a Lambda function» y «Types of metrics for Lambda functions», consultadas el 06/11/2026. """ + SRC_TEMPLATE + """
IMÁGENES: """ + SRC_AWS_ICONS + " Icono genérico Metrics. Diagrama de versiones propio.")
    return sl


def s22_apigw(d):
    sl = d.slide(tag="apigw")
    header(sl, "Amazon API Gateway", "La puerta HTTP: recibir, enrutar, autorizar, limitar e integrar",
           "Un endpoint HTTP es una dirección pública que acepta peticiones. API Gateway lo publica y decide qué hacer con "
           "cada petición antes de que llegue a nuestro código.")
    steps = [("g-padlock.png", "Recibe HTTPS", "https://{api-id}.execute-api.eu-west-1.amazonaws.com"),
             ("g-magnifier.png", "Busca la ruta", "método + ruta: POST /clasificar"),
             ("r-iam-sts.png", "Autoriza", "AWS_IAM: firma SigV4 y permiso execute-api:Invoke"),
             ("g-metrics.png", "Limita", "throttling de la ruta: 2 solicitudes/s, ráfaga 2"),
             ("aws-lambda.png", "Integra", "Lambda (alias aula), payload 2.0, espera 29 s")]
    y = 134
    for i, (ic, t, b) in enumerate(steps):
        box(sl, 43, y, 420, 50, fill=CARD)
        badge(sl, 51, y + 17, i + 1, fill=AMBER, d=16, size=8.5)
        img(sl, ic, 75, y + 11, w=28, h=28)
        text(sl, 113, y + 8, 340, 14, t, size=11, color=TITLE, bold=True)
        text(sl, 113, y + 26, 345, 20, b, size=9, color=TEXT, font=MONO if i in (0, 1) else SANS)
        y += 56
    sw, sh = shot(sl, "shot-apigw-api.png", 483, 152, w=434, kind="oficial", tag_w=210)
    text(sl, 483, 152 + sh + 4, 434, 24, "API details de una HTTP API: protocolo HTTP y endpoint por defecto (tutorial oficial, us-west-1).",
         size=8.5, color=MUTED)
    rows = [["", "HTTP API (la que usamos)", "REST API"],
            ["Para qué", "API sencilla y de menor coste", "Más funciones de gestión"],
            ["Extras", "IAM, JWT y Lambda authorizers", "API keys, planes de uso, validación, WAF, privada"],
            ["Precio eu-west-1", "1,11 USD por millón", "3,50 USD por millón"]]
    table(sl, 483, 330, 434, [92, 171, 171], rows, size=8.5, row_h=22, bold_cols=(0,), colors={0: TITLE})
    text(sl, 483, 427, 434, 40, "Sus límites no son los mismos: aquí aplican los de HTTP API (30 s de integración, 10 MB de payload).",
         size=9.5, color=AMBER)
    takeaway(sl, "API Gateway no ejecuta nuestra lógica: recibe, enruta, autoriza, limita e integra. La lógica está en Lambda.",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:12", "19:14") + """
QUÉ EXPLICAR: qué hace un endpoint HTTP y qué hace API Gateway con cada petición: 1) recibe HTTPS en el endpoint por defecto https://{api-id}.execute-api.eu-west-1.amazonaws.com; 2) busca la ruta por método y ruta (POST /clasificar); 3) aplica la autorización de la ruta (AWS_IAM: firma SigV4 y permiso execute-api:Invoke); 4) aplica los límites (throttling de la ruta en la referencia: 2 solicitudes por segundo y ráfaga 2); 5) integra con Lambda (alias aula, formato 2.0, 29.000 ms). HTTP API frente a REST API: REST tiene más funciones (API keys, planes de uso, validación de peticiones, WAF, endpoints privados); HTTP API es más simple y barata. La práctica usa HTTP API con IAM: no mezclar sus límites (30 s, 10 MB) con los de REST API. Precios de la lista pública de AWS para eu-west-1 (06/11/2026): HTTP API 1,11 USD por millón (primeros 300 millones); REST API 3,50 USD por millón (primeros 333 millones).
CONSOLA: API Gateway › APIs: señalar la columna Protocol (HTTP/REST). Abrir «Create API» para ver las tarjetas HTTP API / WebSocket / REST API y CANCELAR. Si existe la API del laboratorio, abrirla y señalar API details (Protocol, Default endpoint).
PREGUNTA: «¿Necesitamos REST API para usar autorización IAM?». Respuesta: no; HTTP API admite IAM.
FUENTES: API Gateway Developer Guide: «Choose between REST APIs and HTTP APIs», «Quotas for configuring and running an HTTP API» (30 s, 10 MB) y «Throttle requests to your HTTP APIs», consultadas el 06/11/2026; lista pública de precios de Amazon API Gateway para eu-west-1 (publicación del 13/10/2026). """ + SRC_TEMPLATE + """
IMÁGENES: """ + SRC_APIGW_SHOTS + " " + SRC_AWS_ICONS + " Genéricos SSL padlock, Magnifying glass y Metrics; recurso AWS STS.")
    return sl


def s23_rutas(d):
    sl = d.slide(tag="rutas")
    header(sl, "Routes y Authorization", "La ruta: qué peticiones atiende y quién puede usarla",
           "Una ruta une un método y una ruta con una autorización y una integración. En la consola, cada ruta muestra su "
           "ARN, si tiene autorizador y a qué backend llama.")
    k = 432 / 1302
    sw, sh = shot(sl, "shot-apigw-routes.png", 62, 152, w=440, kind="oficial", tag_w=210)
    for n, yy in [(1, 116), (2, 326), (3, 590)]:
        badge(sl, 43, 156 + yy * k - 7, n, fill=AMBER, d=15, size=8)
    text(sl, 62, 152 + sh + 5, 440, 24, "Routes › Route details del tutorial oficial (ruta PUT /items, región us-west-1).",
         size=8.5, color=MUTED)
    ann = [("Ruta", "En la referencia, POST /clasificar. Una petición a otra ruta no llega a la función: API Gateway responde 404."),
           ("Authorization", "En la referencia, IAM (AuthorizationType AWS_IAM). En la captura, «No authorizer attached»: esa ruta "
                             "estaría abierta a cualquiera."),
           ("Integration", "En la referencia, la función Lambda a través del alias aula. Se configura en Integrations.")]
    y = 140
    for i, (t, b) in enumerate(ann):
        badge(sl, 527, y + 1, i + 1, fill=AMBER, d=16, size=8.5)
        text(sl, 551, y, 366, 60, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10.5, color=TEXT)
        y += 70
    box(sl, 527, 356, 390, 110, fill=VIOLET_BG)
    text(sl, 539, 364, 368, 12, "TIPOS DE AUTORIZACIÓN EN HTTP API", size=8.5, color=VIOLET, bold=True)
    bullets(sl, 539, 382, 368, 80, [[("IAM  ", {"bold": True, "color": TITLE}), ("firma SigV4 + execute-api:Invoke (la referencia).", {})],
                                    [("JWT  ", {"bold": True, "color": TITLE}), ("tokens de un proveedor OIDC/OAuth 2.0.", {})],
                                    [("Lambda authorizer  ", {"bold": True, "color": TITLE}), ("una función decide.", {})]],
            size=9.5, mark_color=VIOLET, space=3)
    takeaway(sl, "La ruta define qué se atiende; la autorización, quién puede; la integración, a quién se pasa la petición.",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:14", "19:16") + """
QUÉ EXPLICAR: Routes: cada ruta es método + ruta (POST /clasificar) con su ARN, su autorización y su integración. Una petición que no coincide con ninguna ruta no llega a la función (404 de API Gateway). Authorization: en la referencia, IAM (AWS_IAM). La captura del tutorial muestra «No authorizer attached»: una ruta sin autorización queda abierta, justo lo que no queremos. HTTP API admite autorización IAM, JWT y Lambda authorizers. Integration: la función Lambda (alias aula), que veremos en la diapositiva siguiente.
CONSOLA: API Gateway › APIs › (API del laboratorio, si existe) › Develop › Routes: seleccionar la ruta y señalar ARN, Authorization e Integration. Develop › Authorization: ver el tipo asociado a cada ruta. Sin crear rutas ni adjuntar autorizadores.
PREGUNTA: «¿Qué pasaría si dejáramos la ruta sin autorización?». Respuesta: cualquiera con la URL podría invocar la función y gastar tokens.
FUENTES: API Gateway Developer Guide: «Create a CRUD API with Lambda and DynamoDB» (tutorial y capturas), «Routes for HTTP APIs», «Control access to HTTP APIs with IAM authorization», «JWT authorizers» y «Lambda authorizers», consultadas el 06/11/2026. """ + SRC_TEMPLATE + """
IMÁGENES: """ + SRC_APIGW_SHOTS + " Las insignias numeradas son anotaciones propias.")
    return sl


def s23b_integracion(d):
    sl = d.slide(tag="integracion")
    header(sl, "Integrations y Stages", "La integración: a quién llama y cuánto espera",
           "La integración conecta la ruta con el backend: qué función invoca, con qué formato de evento, con qué permiso y "
           "cuánto espera la respuesta. El stage publica la API en una URL.")
    k = 392 / 1376
    sw, sh = shot(sl, "shot-apigw-integ.png", 62, 152, w=400, kind="oficial", tag_w=210)
    for n, yy in [(1, 182), (2, 422), (3, 606), (4, 806)]:
        badge(sl, 43, 156 + yy * k - 7, n, fill=AMBER, d=15, size=8)
    text(sl, 62, 152 + sh + 5, 400, 24, "Integrations del tutorial oficial (función de us-west-1).", size=8.5, color=MUTED)
    k2 = 419 / 1160
    sw2, sh2 = shot(sl, "shot-apigw-stage.png", 490, 152, w=427, kind="oficial", tag_w=210)
    badge(sl, 900, 156 + 228 * k2 - 7, 5, fill=AMBER, d=15, size=8)
    ann = [("Lambda function", "en la referencia, el alias aula, no $LATEST."),
           ("Payload format version", "2.0: la forma del evento que recibe el handler."),
           ("Invoke permissions", "la política de recursos de la función que permite a API Gateway invocarla."),
           ("Timeout", "30000 ms en el tutorial (el máximo); 29000 ms en la referencia."),
           ("Stage", "$default con auto-deploy publica la URL; la ruta completa termina en /clasificar.")]
    y = 152 + sh2 + 12
    for i, (t, b) in enumerate(ann):
        badge(sl, 490, y + 1, i + 1, fill=AMBER, d=15, size=8)
        text(sl, 512, y, 405, 32, [[(t + ": ", {"bold": True, "color": TITLE}), (b, {})]], size=10, color=TEXT)
        y += 36
    takeaway(sl, "El timeout de la integración es distinto del de Lambda: el de la integración decide cuánto espera el cliente.",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:16", "19:18") + """
QUÉ EXPLICAR: Integrations: la integración Lambda indica la función (en la referencia, el alias aula, para que la API invoque una versión publicada concreta), el Payload format version (2.0, el evento de la diapositiva del handler), los Invoke permissions (la política de recursos de la función, que vimos en Permissions) y el Timeout en milisegundos (máximo documentado de 30.000 para HTTP API; la referencia usa 29.000). Stages: $default con auto-deploy publica la API en https://{api-id}.execute-api.eu-west-1.amazonaws.com y la ruta se añade al final. Protect › Throttling fija los límites por ruta del stage (referencia: 2 solicitudes/s, ráfaga 2).
CONSOLA: API Gateway › (API) › Develop › Integrations: seleccionar la ruta y señalar Lambda function, Payload format version, Invoke permissions y Timeout. Deploy › Stages: $default e Invoke URL. Protect › Throttling. Sin editar ni pulsar Deploy.
PREGUNTA: «¿Dónde se configura cuánto espera API Gateway a Lambda: en Lambda o en la integración?». Respuesta: en la integración; el timeout de Lambda es otro límite.
FUENTES: API Gateway Developer Guide: «Create a CRUD API with Lambda and DynamoDB» (capturas), «Create AWS Lambda proxy integrations for HTTP APIs» (payload 2.0), «Quotas for configuring and running an HTTP API» (30 s) y «Throttle requests to your HTTP APIs», consultadas el 06/11/2026. """ + SRC_TEMPLATE + """
IMÁGENES: """ + SRC_APIGW_SHOTS + " Las insignias numeradas son anotaciones propias.")
    return sl


def s24_autorizar(d):
    sl = d.slide(tag="autorizar")
    header(sl, "Recibir no es autorizar", "Qué ocurre antes de que la petición llegue a Lambda",
           "Cualquiera en Internet puede enviar una petición al endpoint. API Gateway decide si esa petición está autorizada "
           "y si cabe en los límites; solo entonces invoca la función.")
    nodes = [("g-internet.png", "Llega al endpoint", "HTTPS a /clasificar; aún no sabemos quién es.", MUTED),
             ("r-iam-sts.png", "¿Firma y permiso?", "SigV4 válida y execute-api:Invoke sobre la ruta.", VIOLET),
             ("g-metrics.png", "¿Dentro del límite?", "Throttling de la ruta y de la cuenta en la región.", BLUE),
             ("aws-lambda.png", "Invoca Lambda", "El handler valida y llama a Bedrock.", AMBER)]
    w = 196
    for i, (ic, t, b, col) in enumerate(nodes):
        x = 43 + i * (w + 30)
        box(sl, x, 134, w, 96, fill=CARD, line=col)
        img(sl, ic, x + 10, 146, w=30, h=30)
        text(sl, x + 48, 150, w - 54, 16, t, size=11, color=TITLE, bold=True)
        text(sl, x + 10, 184, w - 20, 44, b, size=9.5, color=TEXT)
        if i < 3:
            line(sl, x + w + 3, 182, x + w + 27, 182, color=MINT, w=1.5)
    rej = [(1, "403 Forbidden", "Sin firma, firma inválida o sin permiso. Lo devuelve API Gateway: la función no se ejecuta y no deja log de Lambda.", VIOLET),
           (2, "429 Too Many Requests", "Se superó el ritmo o la ráfaga. Tampoco llega a Lambda.", BLUE)]
    for k, (i, code, b, col) in enumerate(rej):
        x = 43 + i * (w + 30)
        line(sl, x + w / 2, 231, x + w / 2, 254, color=col, w=1.25)
        box(sl, x, 256, w, 84, fill=VIOLET_BG if col == VIOLET else BLUE_BG)
        text(sl, x + 10, 262, w - 20, 16, code, size=11, font=MONO, color=col, bold=True)
        text(sl, x + 10, 281, w - 20, 58, b, size=9, color=TITLE)
    x = 43 + 3 * (w + 30)
    line(sl, x + w / 2, 231, x + w / 2, 254, color=AMBER, w=1.25)
    box(sl, x, 256, w, 84, fill=AMBER_BG)
    text(sl, x + 10, 262, w - 20, 16, "4xx / 5xx del handler", size=11, color=AMBER, bold=True)
    text(sl, x + 10, 281, w - 20, 58, "Errores de validación o del modelo. Sí dejan log de la función.", size=9, color=TITLE)
    box(sl, 43, 256, w, 84, fill=CARD)
    text(sl, 53, 262, w - 20, 16, "Sin filtro todavía", size=11, color=MUTED, bold=True)
    text(sl, 53, 281, w - 20, 58, "El endpoint es público: recibir la petición no dice nada de quién la envía.", size=9, color=TEXT)
    text(sl, 43, 350, 874, 12, "LÍMITES DE SOLICITUDES DE HTTP API", size=9, color=BLUE, bold=True)
    cards = [("Cuenta y región", "10.000 solicitudes por segundo con ráfaga de 5.000, compartidas por todas las APIs (HTTP, REST, WebSocket) "
              "de la cuenta en la región. Se puede pedir aumento.", "documentado"),
             ("Ruta del laboratorio", "2 solicitudes por segundo y ráfaga de 2. Son objetivos de mejor esfuerzo, no techos garantizados: "
              "protegen la cuota de Bedrock y el presupuesto.", "referencia")]
    for i, (t, b, k) in enumerate(cards):
        x = 43 + i * 443
        box(sl, x, 368, 431, 98, fill=CARD)
        text(sl, x + 12, 376, 250, 14, t, size=11, color=TITLE, bold=True)
        tag(sl, x + 431 - 12 - (226 if k == "documentado" else 206), 376, k, w=226 if k == "documentado" else 206)
        text(sl, x + 12, 396, 407, 66, b, size=10, color=TEXT)
    takeaway(sl, "Una petición puede llegar al endpoint y no estar autorizada: el 403 de IAM se produce en API Gateway, antes de Lambda.",
             "Idea guía")
    footer(sl, block=3)
    notes(sl, """
""" + timing_note("19:18", "19:20") + """
QUÉ EXPLICAR: la diferencia entre recibir una petición y estar autorizado a ejecutarla. El endpoint es público: cualquiera puede enviarle bytes. Con AWS_IAM, API Gateway comprueba la firma SigV4 y que la identidad tenga execute-api:Invoke sobre esa ruta y stage; si no, responde 403 sin invocar Lambda (no hay log de la función ni coste de Lambda). Después aplica el throttling (429 si se supera). Solo entonces invoca la función, que puede devolver sus propios 4xx (validación) o 5xx (modelo, tiempo). Límites de solicitudes: por defecto 10.000 rps con ráfaga de 5.000 por cuenta y región, compartidos por todas las APIs; la referencia fija 2 rps y ráfaga 2 en la ruta. AWS indica que los throttles son objetivos de mejor esfuerzo.
CONSOLA: API Gateway › (API) › Develop › Authorization: ver qué rutas tienen IAM. Protect › Throttling: límites del stage y de la ruta. Sin editar.
PREGUNTA: «Un alumno recibe 403. ¿Miramos primero los logs de Lambda?». Respuesta: no; no habrá log de la función. Revisar firma, credenciales temporales, región, servicio execute-api y permiso sobre la ruta.
FUENTES: API Gateway Developer Guide: «Control access to HTTP APIs with IAM authorization», «Throttle requests to your HTTP APIs» (token bucket, 429, mejor esfuerzo) y «Amazon API Gateway quotas» (10.000 rps y ráfaga 5.000 por cuenta y región; 2.500/1.250 en algunas regiones), consultadas el 06/11/2026. """ + SRC_TEMPLATE + """
IMÁGENES: """ + SRC_AWS_ICONS + " Genéricos Internet y Metrics; recurso AWS STS.")
    return sl


PART3 = [s16_div3, s17_lambda_consola, s18_handler, s19_config, s20_permisos, s21_operar, s22_apigw, s23_rutas,
         s23b_integracion, s24_autorizar]
