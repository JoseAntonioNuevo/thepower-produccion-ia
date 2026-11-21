"""Diapositivas 37–41: bloque 6 (costes y alternativas)."""
from deck_lib import *  # noqa: F401,F403
from deck_part1 import SRC_AWS_ICONS

# Desglose del ejemplo de 1.000 solicitudes (datos/s17/costes-ejemplo.json + tarifas-s17-2026-10-17.json).
# Recalculado con scripts/costes_s17.py: total 0,4249 USD. Mantener sincronizado si cambian tarifas o supuestos.
COST = {
    "bedrock_in": 0.0935, "bedrock_out": 0.3157,
    "lambda_gbs": 0.01262503, "lambda_req": 0.0002,
    "api": 0.00111,
    "logs_ingest": 0.00114, "logs_store": 0.000014,
    "s3_store": 0.00046, "s3_req": 0.0000054, "egress": 0.00018,
}
TOTAL = sum(COST.values())  # 0,4249344 USD
SRC_COST = ("Datos: datos/s17/costes-ejemplo.json (cantidades hipotéticas) y docs/fuentes/tarifas-s17-2026-10-17.json "
            "(11 SKU de la lista pública de precios de AWS para eu-west-1, leídos el 17/10/2026). Las 11 tarifas se "
            "comprobaron sin cambios en la lista pública el 06/11/2026. Cálculo reproducible: uv run python scripts/costes_s17.py "
            "(total_usd 0.4249; ejecuta cero peticiones).")


def fmt(v, dec=4):
    return f"{v:.{dec}f}".replace(".", ",")


def s36_div6(d):
    sl = divider(d, 6, "Costes y alternativas", "Cuánto cuesta y cuándo elegir otra cosa",
                 "Estimación de 1.000 solicitudes con supuestos declarados, alternativas en Azure y Google Cloud y criterios de elección.",
                 ["¿Qué partida domina el coste del ejemplo?",
                  "¿Qué supuestos hay detrás de 0,4249 USD?",
                  "¿Qué servicios cumplen la misma función en otras nubes?",
                  "¿Cuándo conviene un contenedor o un proceso asíncrono?"],
                 [("aws-costexplorer.png", "Coste\nestimado"), ("az-functions.png", "Azure\nFunctions"),
                  ("gc-functions.png", "Cloud Run\nfunctions")], "19:40–19:50 · 10 min")
    notes(sl, """
TIEMPO 19:40 (10 s). Bloque 6 de 7: costes y alternativas, de 19:40 a 19:50 (10 min).
QUÉ EXPLICAR: estimar sin ejecutar y elegir arquitectura con criterios.
CONSOLA: ninguna en el separador.
PREGUNTA: «¿Qué creéis que cuesta más en esta arquitectura: Lambda, API Gateway o los tokens?»
FUENTES: temario AI Engineer y guion de S17 (material/S17/guion-profesor.md), con la distribución de tiempos de esta versión.
IMÁGENES: """ + SRC_AWS_ICONS + " Azure Functions: Azure Public Service Icons V25. Cloud Run functions: iconos oficiales de Google Cloud.")
    return sl


def s37_coste(d):
    sl = d.slide(tag="coste")
    header(sl, "Coste estimado", "1.000 solicitudes: 0,4249 USD en el ejemplo",
           "Estimación sin ejecutar ninguna petición, con tarifas públicas de eu-west-1 y cantidades supuestas. No es una "
           "factura ni una medición del laboratorio.")
    tag(sl, 43, 134, "hipotetico", w=230)
    text(sl, 43, 156, 300, 50, "0,4249 USD", size=36, font=SERIF, color=TITLE)
    text(sl, 290, 166, 300, 36, "1.000 solicitudes · eu-west-1 · modelo eu.amazon.nova-2-lite-v1:0 (Standard) · sin impuestos, "
                                "créditos ni capa gratuita", size=9.5, color=MUTED)
    groups = [("Bedrock · tokens", COST["bedrock_in"] + COST["bedrock_out"], PINK),
              ("Lambda", COST["lambda_gbs"] + COST["lambda_req"], AMBER),
              ("CloudWatch Logs", COST["logs_ingest"] + COST["logs_store"], VIOLET),
              ("API Gateway", COST["api"], BLUE),
              ("Otros: S3 y tráfico", COST["s3_store"] + COST["s3_req"] + COST["egress"], MUTED)]
    X0, W = 43, 600
    x = X0
    for t, v, col in groups:
        w = max(W * v / TOTAL, 2.5)
        box(sl, x, 214, w, 30, fill=col, radius=0)
        x += w
    text(sl, X0 + 8, 221, 300, 16, "96,3 % tokens de Bedrock", size=10.5, color=DARK, bold=True, check=False)
    text(sl, X0 + W + 6, 214, 50, 30, "3,7 %\nresto", size=8.5, color=MUTED, check=False)
    y = 258
    details = {
        "Bedrock · tokens": "entrada 0,0935 + salida 0,3157",
        "Lambda": "GB-s 0,0126 + solicitudes 0,0002",
        "CloudWatch Logs": "ingesta 0,0011 + almacenamiento 0,00001",
        "API Gateway": "1.000 solicitudes HTTP API",
        "Otros: S3 y tráfico": "artefacto 0,00046 + PUT/GET + salida 0,00018",
    }
    for t, v, col in groups:
        box(sl, 43, y, 640, 38, fill=CARD)
        box(sl, 43, y, 4, 38, fill=col, radius=0)
        text(sl, 57, y + 4, 180, 14, t, size=10.5, color=TITLE, bold=True)
        text(sl, 57, y + 20, 330, 14, details[t], size=8.5, color=TEXT)
        text(sl, 400, y + 10, 140, 16, fmt(100 * v / TOTAL, 2) + " %", size=10.5, color=col, bold=True, align="r")
        text(sl, 560, y + 10, 112, 16, fmt(v, 4 if v >= 0.001 else 5) + " USD", size=10.5, font=MONO, color=TITLE, bold=True, align="r")
        y += 42
    box(sl, 697, 134, 220, 332, fill=CORAL_BG)
    text(sl, 709, 142, 200, 12, "SUPUESTOS DEL EJEMPLO", size=9, color=CORAL, bold=True)
    sup = ["512 MiB de memoria.", "1.500 ms facturados en caliente y 1.800 ms en frío.", "Frecuencia fría supuesta: 5 %.",
           "250 tokens de entrada y 100 de salida por solicitud.", "Logs: 0,002 GB ingeridos y 7 días de retención.",
           "ZIP de 0,02 GB un mes en S3, 1 PUT y 1 GET.", "0,002 GB de salida facturable."]
    bullets(sl, 709, 162, 200, 236, sup, size=10, mark_color=CORAL, space=6)
    text(sl, 709, 400, 200, 62, "Tarifas leídas el 17/10/2026 y sin cambios el 06/11/2026 en la lista pública de precios. "
                               "Revisar antes de cada uso.", size=9, color=TITLE)
    takeaway(sl, "En este ejemplo los tokens son el 96 % del coste. Con otro modelo, otra entrada u otra salida, el reparto cambia.",
             "Idea guía")
    footer(sl, block=6)
    notes(sl, """
""" + timing_note("19:40", "19:43") + """
QUÉ EXPLICAR: estimación de 1.000 solicitudes sin ejecutarlas, con cantidades hipotéticas (no proceden de la demo ni de un lote real) y tarifas estándar de eu-west-1. Desglose: Bedrock 0,4092 USD (entrada 0,0935 + salida 0,3157; 96,30 %), Lambda 0,0128 (757,5 GB-s × 0,0000166667 = 0,0126 + 1.000 solicitudes × 0,0000002 = 0,0002; 3,02 %), CloudWatch Logs 0,0012 (0,27 %), API Gateway 0,0011 (0,26 %) y otros recursos usados 0,0006 (S3 del artefacto, PUT/GET y tráfico de salida; 0,15 %). Total 0,4249344 → 0,4249 USD, sin impuestos, descuentos, créditos ni capa gratuita. Los tokens dominan este ejemplo, pero eso no demuestra que ocurra en toda aplicación. Con un lote real y REPORT completos, la calculadora puede usar duración y tokens observados; la frecuencia fría y el volumen futuro siguen siendo supuestos.
CONSOLA: opcional, la calculadora pública calculator.aws (sin sesión) para enseñar dónde se introducen solicitudes, duración y memoria de Lambda. No es necesario abrir Billing.
CÓDIGO: uv run python scripts/costes_s17.py (no hace peticiones; imprime filas y total_usd 0.4249).
PREGUNTA: «Si duplicamos la memoria y la duración baja a la mitad, ¿cambia mucho el total?». Respuesta: casi nada en este ejemplo; manda la salida del modelo.
FUENTES: """ + SRC_COST + """
IMÁGENES: diapositiva sin imágenes externas; gráfico propio a partir de esos datos.""")
    return sl


def s38_calculo(d):
    sl = d.slide(tag="calculo")
    header(sl, "Cálculo", "Cómo se obtiene cada partida",
           "Cantidad × tarifa, partida a partida. La duración media facturable mezcla peticiones calientes y frías según la "
           "frecuencia supuesta.")
    tag(sl, 43, 132, "hipotetico", w=230)
    text(sl, 290, 133, 627, 14, "Duración media = 0,95 × 1.500 ms + 0,05 × 1.800 ms = 1.515 ms  ·  GB-s = 1.000 × 1,515 s × 0,5 GB = 757,5",
         size=9.5, font=MONO, color=MINT_L, bold=True)
    rows = [["Partida", "Cantidad", "Tarifa (USD)", "Coste (USD)"],
            ["Lambda · duración", "757,5 GB-s", "0,0000166667 / GB-s", "0,012625"],
            ["Lambda · solicitudes", "1.000", "0,0000002 / solicitud", "0,000200"],
            ["API Gateway · HTTP API", "1.000", "0,00000111 / solicitud", "0,001110"],
            ["Bedrock · entrada", "250.000 tokens", "0,000374 / 1.000 tokens", "0,093500"],
            ["Bedrock · salida", "100.000 tokens", "0,003157 / 1.000 tokens", "0,315700"],
            ["CloudWatch Logs · ingesta", "0,002 GB", "0,57 / GB", "0,001140"],
            ["CloudWatch Logs · almacenamiento", "0,000467 GB-mes", "0,03 / GB-mes", "0,000014"],
            ["S3 · artefacto ZIP", "0,02 GB-mes", "0,023 / GB-mes", "0,000460"],
            ["S3 · PUT y GET", "1 + 1", "0,000005 y 0,0000004", "0,000005"],
            ["Transferencia de salida", "0,002 GB", "0,09 / GB", "0,000180"],
            [("Total", {"bold": True, "color": TITLE}), "", "", ("0,4249", {"bold": True, "color": MINT_L, "font": MONO, "align": "r"})]]
    for r in rows[1:-1]:
        r[3] = (r[3], {"font": MONO, "align": "r", "color": TITLE})
    table(sl, 43, 154, 600, [190, 120, 170, 120], rows, size=9.5, row_h=24, bold_cols=(0,), colors={0: TITLE})
    text(sl, 657, 154, 260, 12, "PALANCAS PARA OPTIMIZAR", size=9, color=CORAL, bold=True)
    lev = [("Tokens de salida", "Son la partida mayor: acotar maxTokens y pedir respuestas breves."),
           ("Memoria medida", "Más memoria puede acortar la duración sin abaratar: medir antes de cambiar."),
           ("Sin reintentos ocultos", "Cada reintento repite tokens; una llamada fallida también puede costar."),
           ("Logs y retención", "Registrar lo necesario y fijar la retención."),
           ("Retirar", "Lo que queda desplegado o almacenado sigue facturando.")]
    y = 172
    for t, b in lev:
        box(sl, 657, y, 260, 54, fill=CARD)
        box(sl, 657, y, 3.5, 54, fill=CORAL, radius=0)
        text(sl, 667, y + 5, 244, 14, t, size=10, color=TITLE, bold=True)
        text(sl, 667, y + 21, 244, 32, b, size=9, color=TEXT)
        y += 59
    takeaway(sl, "Con un lote real se sustituyen duración y tokens por los observados; la frecuencia fría y el volumen siguen siendo supuestos.",
             "Idea guía")
    footer(sl, block=6)
    notes(sl, """
""" + timing_note("19:43", "19:45") + """
QUÉ EXPLICAR: cada partida es cantidad × tarifa. Duración media facturable: 0,95 × 1.500 + 0,05 × 1.800 = 1.515 ms; Lambda: 1.000 × 1,515 s × 0,5 GB = 757,5 GB-s × 0,0000166667 = 0,012625 USD; solicitudes Lambda 0,0002; HTTP API 1.000 × 0,00000111 = 0,00111; Bedrock: 250.000 tokens × 0,000374/1.000 = 0,0935 y 100.000 × 0,003157/1.000 = 0,3157; logs: 0,002 GB × 0,57 = 0,00114 e ingesta almacenada 0,000467 GB-mes (7 días de 0,002 GB) × 0,03 = 0,000014; S3: 0,02 GB-mes × 0,023 = 0,00046 más PUT 0,000005 y GET 0,0000004; salida 0,002 GB × 0,09 = 0,00018. Suma 0,4249344 USD. Palancas: tokens de salida, memoria medida, sin reintentos ocultos, logs con retención y retirada.
CONSOLA: ninguna.
PREGUNTA: «¿Qué dato de esta tabla podríamos sustituir por uno medido tras un lote real?». Respuesta: duración facturada (REPORT) y tokens (usage); la frecuencia fría y el volumen siguen siendo supuestos.
FUENTES: """ + SRC_COST + """
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


def s39_alternativas(d):
    sl = d.slide(tag="alternativas")
    header(sl, "Otras nubes", "Las mismas funciones en AWS, Azure y Google Cloud",
           "Correspondencias por función para orientarse. No implican las mismas APIs, límites, regiones, modelos ni precios: "
           "cada plan se comprueba por separado.")
    cx = [223, 455, 687]
    cw = 226
    hdrs = [("aws-logo-light.png", 22, None), ("az-logo.png", 22, "Microsoft Azure"), ("gc-logo.png", 17, None)]
    for x, (lg, h, lab) in zip(cx, hdrs):
        box(sl, x, 126, cw, 30, fill="FFFFFF", radius=5)
        if lab:
            img(sl, lg, x + 50, 130, h=h)
            text(sl, x + 78, 133, 140, 16, lab, size=11, color=UI_TEXT, bold=True)
        else:
            w, _ = img_size(lg, h=h)
            img(sl, lg, x + (cw - w) / 2, 126 + (30 - h) / 2, h=h)
    rows = [("Código por invocación", ("aws-lambda.png", "AWS Lambda"), ("az-functions.png", "Azure Functions"),
             ("gc-functions.png", "Cloud Run functions")),
            ("Modelos gestionados", ("aws-bedrock.png", "Amazon Bedrock"), ("az-foundry.png", "Microsoft Foundry"),
             ("gc-vertex.png", "Vertex AI · hoy en Gemini Enterprise Agent Platform")),
            ("Entrada HTTP gestionada", ("aws-apigw.png", "Amazon API Gateway"), ("az-apim.png", "Azure API Management"),
             ("gc-apigw.png", "API Gateway")),
            ("Identidad y permisos", ("aws-iam.png", "AWS IAM"), ("az-entra.png", "Microsoft Entra ID + Azure RBAC"),
             ("gc-iam.png", "Cloud IAM")),
            ("Logs y métricas", ("aws-cloudwatch.png", "Amazon CloudWatch"), ("az-monitor.png", "Azure Monitor + Application Insights"),
             ("gc-logging.png", "Cloud Logging + Cloud Monitoring"))]
    y = 162
    for i, (fn, *cells) in enumerate(rows):
        hl = i < 2
        box(sl, 43, y, 174, 44, fill=PINK_BG if hl else CARD, radius=3)
        text(sl, 53, y + 4, 160, 36, fn, size=10.5, color=PINK if hl else TITLE, bold=True, anchor="m")
        for x, (ic, nm) in zip(cx, cells):
            box(sl, x, y, cw, 44, fill=PINK_BG if hl else CARD, radius=3)
            img(sl, ic, x + 8, y + 9, w=26, h=26)
            text(sl, x + 42, y + 4, cw - 48, 36, nm, size=10, color=TITLE, bold=hl, anchor="m")
        y += 48
    text(sl, 43, 406, 874, 60, [{"runs": [("Notas.  ", {"bold": True, "color": PINK}),
                                          ("Azure Functions y Cloud Run functions también pueden exponer HTTP sin gateway; el gateway es una opción. "
                                           "Google presenta Vertex AI como parte de Gemini Enterprise Agent Platform. Microsoft sitúa Foundry frente a "
                                           "Bedrock y Google, Cloud Run functions frente a Lambda.", {})]}],
         size=9.5, color=TEXT)
    takeaway(sl, "Se compara por función: cómputo por invocación, modelos, entrada HTTP, identidad y observabilidad; no por logotipos.",
             "Idea guía")
    footer(sl, block=6)
    notes(sl, """
""" + timing_note("19:45", "19:47") + """
QUÉ EXPLICAR: comparación por funciones. Código por invocación: AWS Lambda / Azure Functions / Cloud Run functions (antes Cloud Functions). Modelos gestionados: Amazon Bedrock / Microsoft Foundry / Vertex AI, que Google presenta hoy como parte de Gemini Enterprise Agent Platform («evolución de Vertex AI», según su documentación). Entrada HTTP gestionada: Amazon API Gateway / Azure API Management / API Gateway de Google Cloud (las funciones también pueden exponer HTTP directamente). Identidad: AWS IAM / Microsoft Entra ID con Azure RBAC / Cloud IAM, con modelos de autorización distintos. Observabilidad: CloudWatch / Azure Monitor con Application Insights / Cloud Logging y Cloud Monitoring. Son correspondencias funcionales: los límites (plazos HTTP, concurrencia), los modelos disponibles por región, la identidad y los precios dependen de cada servicio y plan. El temario cita «Alternativas como Azure y Vertex AI».
CONSOLA: ninguna (no abrimos Azure ni Google Cloud).
PREGUNTA: «La empresa ya tiene identidad y datos en Azure. ¿Necesita AWS para usar IA gestionada?». Respuesta: no; comparar datos, identidad, regiones, modelos, límites y coste total.
FUENTES: Microsoft Learn, «AI and machine learning services comparison for AWS professionals» (Amazon Bedrock ↔ Microsoft Foundry); Google Cloud, «Compare AWS and Azure services to Google Cloud» (Cloud Run functions ↔ AWS Lambda; API Gateway); Google Cloud, «Gemini Enterprise Agent Platform overview» (evolución de Vertex AI), consultadas el 06/11/2026.
IMÁGENES: logotipo de AWS (a0.awsstatic.com, versión Squid Ink) y logotipo de Google Cloud (gstatic.com), igual que en S16. """ + SRC_AWS_ICONS + " Azure Public Service Icons V25 (Functions, Foundry, API Management, Monitor; Application Insights no se muestra) y Microsoft Entra architecture icons. Google Cloud: core products icons y legacy icons de cloud.google.com/icons (Cloud Run functions, Vertex AI, IAM, API Gateway, Cloud Logging).")
    return sl


def s40_elegir(d):
    sl = d.slide(tag="elegir")
    header(sl, "Elegir arquitectura", "¿Cuándo conviene otra arquitectura?",
           "Lambda + Bedrock encaja con peticiones cortas, tráfico variable y una respuesta JSON validada. Estas señales "
           "indican que puede convenir otro patrón.")
    rows = [("Duración", "El trabajo no cabe en 30 s de integración HTTP.",
             "Proceso asíncrono: aceptar, encolar (SQS) u orquestar (Step Functions) y consultar estado y resultado.",
             ["aws-sqs.png", "aws-stepfunctions.png"]),
            ("Streaming", "El usuario debe ver la respuesta mientras se genera.",
             "ConverseStream con un transporte compatible (respuesta en streaming de Lambda, WebSocket o contenedor) y permiso propio.",
             ["aws-bedrock.png"]),
            ("Latencia", "Los arranques en frío afectan a la experiencia.",
             "Concurrencia provisionada (coste fijo) o un contenedor siempre encendido, como en S16.", ["aws-lambda.png"]),
            ("Carga sostenida", "Tráfico alto y constante durante todo el día.",
             "Comparar con ECS en Fargate: pagar por tiempo encendido puede salir más barato que por invocación.", ["aws-fargate.png"]),
            ("Dependencias", "Librerías nativas o paquetes grandes.",
             "Imagen de contenedor para Lambda (hasta 10 GB) o un contenedor en ECS; el ZIP admite 250 MB descomprimido.",
             ["aws-ecs.png"]),
            ("Coste", "Los tokens dominan la factura.",
             "Revisar modelo, prompt y maxTokens antes que la infraestructura; el nivel Flex, si el caso admite esperar.",
             ["aws-costexplorer.png"])]
    text(sl, 43, 132, 120, 12, "CRITERIO", size=8.5, color=MUTED, bold=True)
    text(sl, 175, 132, 220, 12, "SEÑAL", size=8.5, color=MUTED, bold=True)
    text(sl, 420, 132, 400, 12, "OPCIÓN A CONSIDERAR", size=8.5, color=MUTED, bold=True)
    y = 148
    for t, sig, opt, ics in rows:
        box(sl, 43, y, 874, 50, fill=CARD)
        box(sl, 43, y, 4, 50, fill=CORAL, radius=0)
        text(sl, 57, y + 4, 115, 42, t, size=11.5, color=TITLE, bold=True, anchor="m")
        text(sl, 175, y + 4, 235, 42, sig, size=9.5, color=TEXT, anchor="m")
        text(sl, 420, y + 4, 420, 42, opt, size=9.5, color=TITLE, anchor="m")
        for k, ic in enumerate(ics):
            img(sl, ic, 878 - k * 32, y + 11, w=28, h=28)
        y += 53
    takeaway(sl, "No hay arquitectura ganadora: duración, streaming, latencia, carga, dependencias y coste deciden el patrón.",
             "Idea guía")
    footer(sl, block=6)
    notes(sl, """
""" + timing_note("19:47", "19:50") + """
QUÉ EXPLICAR: cuándo considerar un contenedor, un proceso asíncrono u otra arquitectura. Duración: si el trabajo no cabe en el plazo HTTP (30 s de integración en HTTP API), separar inicio, estado y resultado con una cola (SQS) o un orquestador (Step Functions); la documentación de Lambda menciona también Lambda Durable Functions para flujos de varios pasos. Streaming: ConverseStream necesita bedrock:InvokeModelWithResponseStream y un transporte compatible; la ruta entregada es no streaming y no promete ese extra. Latencia: concurrencia provisionada (con coste) o un contenedor encendido. Carga sostenida: comparar con Fargate (S16). Dependencias: imagen de contenedor para Lambda hasta 10 GB o contenedor en ECS (el ZIP admite 50 MB comprimido por API y 250 MB descomprimido). Coste: si mandan los tokens, revisar modelo, prompt y salida; Nova 2 Lite admite el nivel Flex para cargas que toleran esperar.
CONSOLA: ninguna.
PREGUNTA: «Un informe de investigación tarda cuatro minutos. ¿Qué cambiamos?». Respuesta: el patrón: trabajo asíncrono con estado y consulta del resultado, no el timeout de Lambda.
FUENTES: AWS Lambda Developer Guide, «What is AWS Lambda?» (Durable Functions, Managed Instances) y «Lambda quotas» (10 GB de imagen, 250 MB descomprimido); Amazon Bedrock User Guide, «Using the Converse API» (ConverseStream) y ficha «Nova 2 Lite» (niveles Standard, Priority y Flex); API Gateway, «Quotas for configuring and running an HTTP API», consultadas el 06/11/2026. Enunciado S17 (alternativas y criterios por timeouts, streaming, latencia o tráfico sostenido).
IMÁGENES: """ + SRC_AWS_ICONS + " Iconos de Amazon SQS, AWS Step Functions, Fargate, ECS y Cost Explorer.")
    return sl


PART5 = [s36_div6, s37_coste, s38_calculo, s39_alternativas, s40_elegir]
