"""Diapositivas 9–15: bloque 2 (Amazon Bedrock desde la consola)."""
from deck_lib import *  # noqa: F401,F403
from deck_part1 import SRC_AWS_ICONS

SRC_NOVA = ("Amazon Bedrock User Guide, ficha «Nova 2 Lite» (model-card-amazon-nova-2-lite.html), consultada el 06/11/2026: "
            "ID amazon.nova-2-lite-v1:0; perfiles us., eu., jp. y global.; entrada texto, imagen y vídeo; salida texto; "
            "contexto 1M tokens; salida máxima 64K; APIs Converse e Invoke; niveles Standard, Priority y Flex; "
            "«Structured outputs» no figura como compatible; lanzamiento 02/12/2025.")


def s09_div2(d):
    sl = divider(d, 2, "Bedrock", "Amazon Bedrock desde la consola",
                 "Catálogo, ficha del modelo, perfiles de inferencia, parámetros y playground, sin ejecutar inferencias.",
                 ["¿Qué ofrece Bedrock y qué no hace por nosotros?",
                  "¿Qué diferencia hay entre modelo, proveedor y perfil?",
                  "¿Dónde se procesa una petición con el perfil eu.?",
                  "¿Qué controlan los tokens y los parámetros?"],
                 [("aws-bedrock.png", "Amazon\nBedrock"), ("g-sdk.png", "bedrock-runtime\n(SDK)"),
                  ("grp-region.png", "Regiones\neuropeas")], "18:45–19:00 · 15 min")
    notes(sl, """
TIEMPO 18:45 (10 s). Bloque 2 de 7: Amazon Bedrock desde la consola, de 18:45 a 19:00 (15 min).
QUÉ EXPLICAR: Bedrock es la pieza de IA gestionada. La recorreremos en la consola sin pulsar «Run» en el playground.
CONSOLA: abrir Amazon Bedrock en eu-west-1.
PREGUNTA: «¿Qué esperáis encontrar en la ficha de un modelo antes de usarlo?»
FUENTES: temario AI Engineer y guion de S17 (material/S17/guion-profesor.md), con la distribución de tiempos de esta versión.
IMÁGENES: """ + SRC_AWS_ICONS + " Icono genérico SDK y grupo Region del mismo paquete.")
    return sl


def s10_bedrock(d):
    sl = d.slide(tag="bedrock")
    header(sl, "Amazon Bedrock", "Qué ofrece Bedrock y qué hacemos nosotros con él",
           "Bedrock da acceso gestionado a modelos de Amazon y de otros proveedores con una API común. AWS opera la "
           "inferencia; nosotros elegimos modelo, región y parámetros, y autorizamos el acceso con IAM.")
    # pila de capas
    layers = [("NUESTRA FUNCIÓN", "Lambda prepara el mensaje y llama a Converse con el SDK de AWS (boto3).", "aws-lambda.png", AMBER, AMBER_BG),
              ("API DE INFERENCIA", "bedrock-runtime: Converse, InvokeModel y sus variantes en streaming. Se autoriza con IAM y se factura en AWS.",
               "g-sdk.png", PINK, PINK_BG),
              ("MODELOS DEL CATÁLOGO", "Amazon, Anthropic, Meta, Mistral AI, Cohere y otros proveedores. AWS aloja y escala la infraestructura de inferencia.",
               "aws-bedrock.png", PINK, PINK_BG)]
    y = 134
    for i, (t, b, ic, col, bg) in enumerate(layers):
        box(sl, 43, y, 440, 78, fill=bg)
        img(sl, ic, 55, y + 20, w=36, h=36)
        text(sl, 103, y + 10, 370, 12, t, size=9, color=col, bold=True)
        text(sl, 103, y + 26, 370, 48, b, size=10.5, color=TITLE)
        if i < 2:
            line(sl, 263, y + 79, 263, y + 89, color=col, w=1.5)
        y += 90
    text(sl, 43, 406, 440, 60, "Bedrock no aloja nuestra API ni ejecuta nuestro código: aloja el modelo. Pagamos los tokens de "
                               "entrada y salida de cada invocación (o capacidad reservada, que hoy no usamos).", size=10.5, color=TEXT)
    text(sl, 503, 134, 414, 12, "«DESPLEGAR MODELOS Y AGENTES»: TRES COSAS DISTINTAS", size=9, color=MUTED, bold=True)
    opts = [("aws-bedrock.png", "Consumir un modelo gestionado", "Lo que hace S17",
             "Llamamos a un modelo del catálogo desde Lambda. No gestionamos pesos, GPU ni servidores de inferencia.", MINT),
            ("aws-bedrock.png", "Importar un modelo propio", "Custom Model Import",
             "Pesos abiertos personalizados (por ejemplo, de Llama o Mistral) servidos por Bedrock; se factura por copias activas del modelo.", MUTED),
            ("aws-agentcore.png", "Ejecutar agentes", "Amazon Bedrock AgentCore",
             "Servicio aparte para alojar y operar agentes. Queda fuera del ejemplo y de la práctica de hoy.", MUTED)]
    y = 152
    for ic, t, tag_, b, col in opts:
        box(sl, 503, y, 414, 96, fill=CARD, line=col if col == MINT else None)
        img(sl, ic, 515, y + 12, w=30, h=30)
        text(sl, 555, y + 10, 350, 15, t, size=11.5, color=TITLE, bold=True)
        text(sl, 555, y + 27, 350, 13, tag_, size=9, color=col if col == MINT else PINK, bold=True)
        text(sl, 515, y + 48, 392, 46, b, size=10, color=TEXT)
        y += 104
    takeaway(sl, "El ejemplo preparado consume un modelo gestionado: los pesos del modelo no viven dentro de nuestra función Lambda.",
             "Idea guía")
    footer(sl, block=2)
    notes(sl, """
""" + timing_note("18:45", "18:47") + """
QUÉ EXPLICAR: Amazon Bedrock es acceso gestionado a modelos fundacionales mediante una API común (Converse, InvokeModel y sus variantes en streaming), con autenticación IAM y facturación en AWS. No es el servidor de nuestra API. El texto del temario habla de «desplegar modelos y agentes sin gestionar servidores»: distinguir tres cosas. 1) Consumir un modelo gestionado del catálogo (lo que hace la referencia S17 desde Lambda). 2) Custom Model Import: importar pesos abiertos personalizados (Llama, Mistral, Qwen…) para que Bedrock los sirva; se factura por copias de modelo activas en ventanas de 5 minutos. 3) Amazon Bedrock AgentCore: servicio aparte para alojar y operar agentes. Solo la primera forma parte del ejemplo.
CONSOLA: Amazon Bedrock (eu-west-1) › página de inicio y menú lateral: Model catalog, Playgrounds, Cross-Region inference. Señalar que Custom models / Imported models y AgentCore existen, sin entrar en sus formularios.
PREGUNTA: «¿Dónde están los pesos de Nova 2 Lite en nuestra arquitectura?». Respuesta: en la infraestructura de Bedrock; nuestro ZIP solo contiene código y el SDK.
FUENTES: Amazon Bedrock User Guide: «What is Amazon Bedrock?», «Using the Converse API» (Converse requiere bedrock:InvokeModel), «Import a pre-trained model» y «Calculate the cost of running a custom model» (Custom Model Import), consultadas el 06/11/2026. AgentCore: documentación de Amazon Bedrock AgentCore.
IMÁGENES: """ + SRC_AWS_ICONS + " Iconos Amazon Bedrock y Amazon Bedrock AgentCore; genérico SDK.")
    return sl


def s11_ids(d):
    sl = d.slide(tag="ids")
    header(sl, "Modelo, proveedor y perfil", "Qué significa eu.amazon.nova-2-lite-v1:0",
           "El identificador que configuramos en Lambda no nombra solo un modelo: también dice quién lo creó y por qué "
           "conjunto de regiones puede viajar la petición.")
    box(sl, 43, 134, 874, 112, fill=CARD, line=BORDER)
    text(sl, 43, 140, 874, 18, "eu.amazon.nova-2-lite-v1:0", size=13, font=MONO, color=MUTED, bold=True, align="c", check=False)
    parts = [("eu.", PINK, "Perfil geográfico", "Europa: la petición puede\nprocesarse en regiones de la UE."),
             ("amazon.", BLUE, "Proveedor", "Quién creó el modelo y\nsus condiciones de uso."),
             ("nova-2-lite", MINT, "Modelo", "Nova 2 Lite: multimodal\nde bajo coste de Amazon."),
             ("-v1:0", AMBER, "Versión", "Versión concreta del modelo\nque se invoca.")]
    for i, (t, col, lab, b) in enumerate(parts):
        xx = 43 + 10 + i * 214
        text(sl, xx, 160, 210, 24, t, size=18, font=MONO, color=col, bold=True, align="c", check=False)
        box(sl, xx + 55, 186, 100, 3, fill=col, radius=0)
        text(sl, xx, 193, 210, 14, lab, size=10.5, color=col, bold=True, align="c")
        text(sl, xx, 209, 210, 34, b, size=9.5, color=TEXT, align="c")
    rows = [("Modelo base", "amazon.nova-2-lite-v1:0", "Invocación en una sola región (In-Region). La ficha indica que eu-west-1 no la ofrece para este modelo.", BLUE),
            ("Perfil geográfico EU", "eu.amazon.nova-2-lite-v1:0", "Referencia del material S17. Enruta dentro de un conjunto fijo de regiones europeas.", PINK),
            ("Perfil global", "global.amazon.nova-2-lite-v1:0", "Puede procesar en cualquier región comercial. No lo usamos sin justificar dónde se procesan los datos.", CORAL)]
    y = 258
    for t, code, b, col in rows:
        box(sl, 43, y, 874, 44, fill=CARD)
        box(sl, 43, y, 4, 44, fill=col, radius=0)
        text(sl, 57, y + 7, 160, 30, t, size=10.5, color=TITLE, bold=True, anchor="m")
        text(sl, 205, y + 7, 270, 30, code, size=10, font=MONO, color=col, bold=True, anchor="m")
        text(sl, 480, y + 5, 428, 36, b, size=9.5, color=TEXT, anchor="m")
        y += 50
    box(sl, 43, 412, 874, 54, fill=AMBER_BG)
    text(sl, 55, 418, 852, 44, [[("En el código  ", {"bold": True, "color": AMBER}),
                                  ("BEDROCK_MODEL_ID = eu.amazon.nova-2-lite-v1:0", {"font": MONO, "bold": True, "color": MINT_L}),
                                  ("  es una variable de entorno de Lambda; config.py rechaza perfiles no europeos. Es la referencia "
                                   "del material preparado, no un modelo exigido por el temario ni con disponibilidad garantizada en cualquier cuenta.", {})]],
         size=10, color=TITLE)
    takeaway(sl, "El modelo es lo que responde; el proveedor, quién lo creó; el perfil, por qué regiones puede viajar la petición.",
             "Idea guía")
    footer(sl, block=2)
    notes(sl, """
""" + timing_note("18:47", "18:49") + """
QUÉ EXPLICAR: descomponer el identificador. «eu.» es el prefijo de un perfil de inferencia geográfico (Europa); «amazon.» es el proveedor; «nova-2-lite» es el modelo; «-v1:0», la versión. Tres formas de invocar el mismo modelo: el modelo base (In-Region, una sola región; según la ficha, no disponible en eu-west-1 para Nova 2 Lite), el perfil geográfico eu. (referencia del ejercicio) y el perfil global. (cualquier región comercial). La referencia es una elección del material existente redactado por José, no un modelo impuesto por Laura; su disponibilidad, permisos y cuota dependen de cada cuenta y deben comprobarse antes del ensayo real.
CONSOLA: Bedrock › Model catalog › buscar «Nova 2 Lite» › abrir la ficha y señalar el Model ID. Después Bedrock › Cross-Region inference › localizar «EU Nova 2 Lite» y su Inference profile ID.
PREGUNTA: «Si mañana cambio eu. por global., ¿qué cambia aunque el modelo sea el mismo?». Respuesta: las regiones donde puede procesarse la petición, los permisos necesarios y posiblemente la tarifa.
FUENTES: """ + SRC_NOVA + " src/curso_ia/serverless/config.py (REFERENCE_MODEL y validación del prefijo eu.). Enunciado S17 (José, 28/09/2026): «No cambies a un perfil global sin justificar dónde se procesan las peticiones».\nIMÁGENES: diapositiva sin imágenes externas.")
    return sl


def s12_ficha(d):
    sl = d.slide(tag="ficha")
    header(sl, "Model catalog", "La ficha del modelo antes de escribir código",
           "En Bedrock › Model catalog filtramos por proveedor y modalidad y abrimos la ficha. Responde qué entra y qué sale, "
           "cuánto cabe, con qué API se llama y desde qué regiones.")
    ui_panel(sl, 43, 134, 470, 332, title="Nova 2 Lite", crumbs="Amazon Bedrock  ›  Model catalog  ›  Nova 2 Lite")
    tag(sl, 343, 137, "esquema", w=164)
    text(sl, 51, 188, 300, 12, "Amazon  ·  Model lifecycle: Active  ·  Launched Dec 02, 2025", size=8.5, color=UI_MUTED, check=False)
    fields = [(1, "Model ID", "amazon.nova-2-lite-v1:0"),
              (2, "Input modalities", "Text, Image, Video"),
              (2, "Output modalities", "Text"),
              (3, "Context window", "1M tokens"),
              (3, "Max output tokens", "64K"),
              (4, "APIs supported", "Converse, Invoke"),
              (4, "Response streaming", "Supported"),
              (5, "Geo inference ID", "eu.amazon.nova-2-lite-v1:0"),
              (5, "In-Region (eu-west-1)", "Not supported"),
              (6, "Service tiers", "Standard, Priority, Flex")]
    y = 206
    for i, (n, k, v) in enumerate(fields):
        col = i % 2
        row = i // 2
        x = 51 + col * 228
        yy = y + row * 50
        box(sl, x, yy, 220, 44, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
        text(sl, x + 8, yy + 6, 180, 12, k, size=8.5, color=UI_LABEL, bold=True, check=False)
        text(sl, x + 8, yy + 22, 200, 16, v, size=10, color=UI_BLUE if n in (1, 5) else UI_TEXT, bold=True,
             font=MONO if n in (1,) or "inference ID" in k else SANS, check=False)
        badge(sl, x + 200, yy + 6, n, fill=AMBER, d=14, size=8)
    ann = [("Identificador", "Lo que se configura en BEDROCK_MODEL_ID (o su perfil)."),
           ("Modalidades", "Qué podemos enviar y qué devuelve: aquí, texto de salida."),
           ("Tamaños", "Contexto de 1M tokens y hasta 64K de salida; nosotros limitamos a 300."),
           ("APIs", "Converse e Invoke; admite streaming y herramientas definidas por el cliente."),
           ("Regiones", "Perfiles us., eu., jp. y global.; en eu-west-1 se usa un perfil."),
           ("Niveles", "Standard, Priority y Flex cambian precio y prioridad; la referencia usa Standard.")]
    y = 134
    for i, (t, b) in enumerate(ann):
        badge(sl, 527, y + 1, i + 1, fill=AMBER, d=16, size=8.5)
        text(sl, 551, y, 366, 36, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10, color=TEXT)
        y += 40
    box(sl, 527, 378, 390, 88, fill=PINK_BG)
    text(sl, 539, 386, 368, 76, [[("Ojo con la salida estructurada  ", {"bold": True, "color": PINK}),
                                   ("La función «Structured outputs» de Bedrock no figura como compatible en esta ficha. Por eso la referencia "
                                    "pide la estructura con una herramienta (toolConfig) y la valida en Lambda.", {})]], size=10, color=TITLE)
    takeaway(sl, "Ver la ficha no cuesta; invocar el modelo, sí. La ficha decide qué podemos pedir antes de escribir una línea.",
             "Idea guía")
    footer(sl, block=2)
    notes(sl, """
""" + timing_note("18:49", "18:52") + """
QUÉ EXPLICAR: qué es una ficha de modelo y qué campos leer antes de programar. 1) Identificador (Model ID y perfiles). 2) Modalidades de entrada y salida. 3) Ventana de contexto y salida máxima (1M y 64K); la referencia limita la salida a 300 tokens. 4) APIs compatibles (Converse, Invoke), streaming y uso de herramientas. 5) Disponibilidad regional: en eu-west-1 no hay In-Region para este modelo; se invoca con el perfil eu. o global. 6) Niveles de servicio (Standard, Priority, Flex). Detalle importante: «Structured outputs» no figura como compatible, así que la salida estructurada se pide con toolConfig y se vuelve a validar.
CONSOLA: Bedrock › Model catalog › filtros Provider: Amazon y Modality: Text › abrir «Nova 2 Lite». Señalar, en este orden, Model ID, modalidades, contexto y salida máxima, APIs, disponibilidad por región y enlace de precios. NO pulsar «Open in playground» para ejecutar, no solicitar acceso ni aceptar términos.
PREGUNTA: «¿Podemos enviar un audio a Nova 2 Lite?». Respuesta: no, según la ficha; entra texto, imagen y vídeo.
FUENTES: """ + SRC_NOVA + """
IMÁGENES: ESQUEMA propio que reproduce los campos de la ficha oficial (no es una captura de la consola; el orden y el diseño de la consola real pueden variar).""")
    return sl


def s13_regiones(d):
    sl = d.slide(tag="regiones")
    header(sl, "Perfiles de inferencia", "Región de entrada y regiones de procesamiento",
           "La llamada sale de Lambda en eu-west-1, que es la región de origen. Con el perfil eu., Bedrock puede procesarla en "
           "cualquiera de las regiones de destino del perfil, y la respuesta no indica en cuál.")
    box(sl, 43, 134, 470, 332, fill=CARD, line=BORDER)
    tag(sl, 53, 142, "esquema", w=200, t="ESQUEMA · posiciones aproximadas")
    # origen
    box(sl, 58, 186, 128, 66, fill=AMBER_BG, line=AMBER)
    img(sl, "aws-lambda.png", 66, 196, w=26, h=26)
    text(sl, 98, 194, 86, 30, "Lambda\neu-west-1", size=9.5, color=TITLE, bold=True)
    text(sl, 66, 228, 116, 20, "región de origen", size=8.5, color=AMBER, bold=True)
    line(sl, 186, 219, 222, 219, color=PINK, w=1.5)
    box(sl, 224, 192, 92, 54, fill=PINK_BG, line=PINK)
    text(sl, 228, 197, 84, 46, "Perfil\neu.amazon.\nnova-2-lite", size=8.5, color=TITLE, bold=True, align="c")
    # mapa esquemático: destinos dentro de un recuadro
    box(sl, 325, 160, 180, 250, fill=PINK_BG, line=PINK, lw=0.75, radius=6, dash=True)
    text(sl, 333, 166, 168, 12, "DESTINOS DEL PERFIL EU", size=8, color=PINK, bold=True)
    line(sl, 316, 219, 323, 219, color=PINK, w=1.5)
    regs = [("eu-north-1", "Estocolmo", 400, 186), ("eu-west-1", "Irlanda", 335, 226), ("eu-west-3", "París", 352, 296),
            ("eu-central-1", "Fráncfort", 412, 256), ("eu-south-1", "Milán", 412, 346), ("eu-south-2", "España", 340, 376)]
    for code, name, x, y in regs:
        if code == "eu-west-1":
            circle(sl, x - 3, y - 3, 18, None, line=AMBER, lw=1.5)
        circle(sl, x, y, 12, PINK)
        text(sl, x + 16, y - 3, 80, 12, code, size=8.5, font=MONO, color=TITLE, bold=True, check=False)
        text(sl, x + 16, y + 9, 80, 12, name + (" · origen" if code == "eu-west-1" else ""), size=8.5,
             color=AMBER if code == "eu-west-1" else TEXT, check=False)
    text(sl, 58, 300, 250, 120, "Desde eu-west-1, el perfil EU de Nova 2 Lite enumera seis regiones de destino. "
                               "El perfil global añade cualquier región comercial del mundo.", size=10, color=TEXT)
    cards = [("Origen no es procesamiento", "El precio se calcula según la región desde la que llamamos, pero el cómputo "
              "puede ocurrir en otra región del perfil. Las cuotas entre regiones son propias.", PINK),
             ("El prefijo no basta", "AWS indica que, si hay requisitos de residencia de datos, hay que consultar los destinos "
              "con GetInferenceProfile desde cada región de origen; el prefijo eu. por sí solo no los garantiza.", AMBER),
             ("Consecuencias en IAM", "El rol debe permitir el perfil y el modelo en el origen y en todos los destinos. "
              "Si una política de la organización bloquea un destino, la petición falla.", VIOLET)]
    y = 134
    for t, b, col in cards:
        side_note(sl, 527, y, 390, 84, t, b, accent=col, size=9.5)
        y += 90
    console_path(sl, 527, 404, 390, "Bedrock › Cross-Region inference › EU Nova 2 Lite › Models", h=62)
    takeaway(sl, "Elegir el perfil eu. acota la geografía, no fija una región: hay que leer sus destinos y autorizarlos todos.",
             "Idea guía")
    footer(sl, block=2)
    notes(sl, """
""" + timing_note("18:52", "18:55") + """
QUÉ EXPLICAR: diferencia entre región de entrada (origen: donde se hace la llamada, eu-west-1) y regiones de procesamiento (destinos del perfil). Según la ficha de Nova 2 Lite, desde eu-west-1 el perfil eu.amazon.nova-2-lite-v1:0 puede enrutar a eu-central-1 (Fráncfort), eu-north-1 (Estocolmo), eu-south-1 (Milán), eu-south-2 (España), eu-west-1 (Irlanda) y eu-west-3 (París). La respuesta de Converse no informa la región que procesó la petición: no atribuirle una. AWS recomienda, si hay requisitos de residencia de datos, llamar a GetInferenceProfile desde cada región de origen y no fiarse solo del prefijo. Los perfiles geográficos mantienen fija su lista de destinos; el global puede cambiar al añadirse regiones. Para IAM: permiso sobre el perfil y sobre el modelo base en origen y destinos (bloque 4). Las SCP que bloqueen un destino hacen fallar la petición.
CONSOLA: Bedrock › Cross-Region inference › elegir «EU Nova 2 Lite» › Inference profile details (ID, ARN) y sección Models (una fila por región de destino). Solo lectura.
PREGUNTA: «La petición sale de Irlanda. ¿Podemos afirmar que se procesó en Irlanda?». Respuesta: no; solo que se procesó en alguna de las regiones del perfil.
FUENTES: Amazon Bedrock User Guide: «Supported Regions and models for inference profiles» (definiciones de Source/Destination Region y nota de residencia de datos), «Geographic cross-Region inference» y ficha «Nova 2 Lite», consultadas el 06/11/2026. El preflight de la referencia (scripts/aws_s17 preflight) lee GetInferenceProfile y rechaza destinos no europeos.
IMÁGENES: ESQUEMA propio de posiciones aproximadas (no es un mapa a escala). Icono de Lambda: AWS Architecture Icons (31/07/2026).""")
    return sl


def s14_playground(d):
    sl = d.slide(tag="playground")
    header(sl, "Playground, parámetros y tokens", "Probar sin código no es probar gratis",
           "El playground permite elegir modelo y perfil, escribir un mensaje y ajustar parámetros. Cada «Run» es una "
           "inferencia facturable, igual que una llamada desde Lambda.")
    ui_panel(sl, 43, 134, 470, 332, title="Chat / Text playground", crumbs="Amazon Bedrock  ›  Playgrounds  ›  Chat / Text")
    tag(sl, 343, 137, "esquema", w=164)
    box(sl, 51, 190, 300, 26, fill=UI_CARD, line="7D8998", lw=0.5, radius=3)
    text(sl, 57, 196, 290, 14, "Amazon · Nova 2 Lite  ·  Inference profile: EU Nova 2 Lite", size=8.5, color=UI_TEXT, check=False)
    badge(sl, 333, 196, 1, fill=AMBER, d=14, size=8)
    box(sl, 51, 222, 300, 156, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    text(sl, 59, 230, 284, 12, "System prompt", size=8.5, color=UI_LABEL, bold=True, check=False)
    text(sl, 59, 244, 284, 36, "Clasifica la incidencia ficticia usando emitir_clasificacion…", size=8.5, color=UI_TEXT, check=False)
    text(sl, 59, 284, 284, 12, "Message", size=8.5, color=UI_LABEL, bold=True, check=False)
    text(sl, 59, 298, 284, 50, "Me han cobrado dos veces la factura de este mes. Es una incidencia ficticia.", size=8.5,
         color=UI_TEXT, check=False)
    badge(sl, 333, 230, 2, fill=AMBER, d=14, size=8)
    ui_button(sl, 51, 386, 70, "Run", primary=True)
    chip(sl, 128, 386, 223, 16, "no pulsar en clase: ejecuta una inferencia", fill=CORAL, color=DARK, size=7.5, radius=3)
    box(sl, 361, 190, 144, 268, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    text(sl, 369, 196, 130, 12, "Configurations", size=9, color=UI_TEXT, bold=True, check=False)
    yy = 214
    for lab, val in [("Temperature", "0.7"), ("Top P", "0.9"), ("Maximum length", "300"), ("Stop sequences", "—")]:
        yy = ui_field(sl, 369, yy, 128, lab, val) + 8
    badge(sl, 487, 214, 3, fill=AMBER, d=14, size=8)
    text(sl, 369, yy + 2, 130, 40, "Valores del esquema: ilustrativos, salvo el límite de 300.", size=7.5, color=UI_MUTED, check=False)
    ann = [("Modelo y perfil", "Igual que BEDROCK_MODEL_ID: el mismo modelo puede invocarse con distintos perfiles."),
           ("Mensajes", "System y usuario cuentan como tokens de entrada, igual que la definición de la herramienta."),
           ("Parámetros", "maxTokens corta la salida; temperature y topP cambian la variabilidad; stopSequences detienen la generación.")]
    y = 134
    for i, (t, b) in enumerate(ann):
        badge(sl, 527, y + 1, i + 1, fill=AMBER, d=16, size=8.5)
        text(sl, 551, y, 366, 44, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10, color=TEXT)
        y += 46
    box(sl, 527, 276, 390, 190, fill=CARD, line=BORDER)
    tag(sl, 537, 284, "hipotetico", w=226)
    text(sl, 537, 304, 370, 12, "COSTE DE UNA PETICIÓN DEL EJEMPLO · eu-west-1, nivel Standard", size=8.5, color=CORAL, bold=True)
    rows = [("Entrada", "250 tokens × 0,000374 USD / 1.000", "0,0000935"),
            ("Salida", "100 tokens × 0,003157 USD / 1.000", "0,0003157"),
            ("Total", "por solicitud, solo modelo", "0,0004092")]
    y = 322
    for t, f, v in rows:
        bold = t == "Total"
        text(sl, 537, y, 60, 14, t, size=10, color=TITLE, bold=True)
        text(sl, 597, y, 220, 14, f, size=9.5, color=TEXT)
        text(sl, 817, y, 90, 14, v, size=10, font=MONO, color=MINT_L if bold else TITLE, bold=True, align="r")
        y += 20
    text(sl, 537, 386, 370, 76, "El token de salida cuesta unas 8,4 veces más que el de entrada. La respuesta de Converse "
                               "informa inputTokens, outputTokens y totalTokens en usage. Tarifas leídas el 17/10/2026 y "
                               "sin cambios en la lista pública de precios el 06/11/2026.", size=9.5, color=TEXT)
    takeaway(sl, "El playground y el SDK consumen lo mismo: tokens de entrada y salida. Hoy mostramos la pantalla sin pulsar «Run».",
             "Idea guía")
    footer(sl, block=2)
    notes(sl, """
""" + timing_note("18:55", "18:58") + """
QUÉ EXPLICAR: el playground es una interfaz para experimentar sin código: seleccionar modelo y perfil de inferencia, escribir system prompt y mensaje, ajustar parámetros y ejecutar. Ejecutar consume inferencia facturable igual que la API. Tokens: entrada = system + mensajes + definición de la herramienta; salida = lo que genera el modelo (en la referencia, la llamada a emitir_clasificacion). Parámetros: maxTokens (300 en la referencia), temperature, topP y stopSequences. Nova 2 Lite admite razonamiento, desactivado por defecto (reasoningConfig); la referencia no lo activa. Leer el cálculo de una petición del ejemplo: 250 tokens de entrada y 100 de salida (cantidades hipotéticas) a las tarifas estándar de eu-west-1.
CONSOLA: Bedrock › Playgrounds › Chat / Text › Select model › Amazon › Nova 2 Lite › Inference: Inference profiles › EU Nova 2 Lite (Apply). Señalar el panel de configuración (temperatura, Top P, longitud máxima). NO pulsar Run. Si la cuenta no tiene acceso al modelo, mostrar el selector y explicar con este esquema.
PREGUNTA: «¿Qué parámetro protege mejor el coste de una respuesta demasiado larga?». Respuesta: maxTokens.
FUENTES: Amazon Bedrock User Guide: «Use an inference profile in model invocation» (Chat / Text playground y selección de perfiles), «Get started in the Amazon Bedrock console» e «Inference request parameters»; ficha «Nova 2 Lite» (reasoningConfig desactivado por defecto), consultadas el 06/11/2026. Tarifas: docs/fuentes/tarifas-s17-2026-10-17.json (SKU EU-Nova2.0Lite-input-tokens 0,000374 USD/1K y output 0,003157 USD/1K), comprobadas sin cambios en la lista pública de precios de AWS para eu-west-1 el 06/11/2026.
IMÁGENES: ESQUEMA propio del playground (no es una captura; la consola real puede ordenar los controles de otra forma).""")
    return sl


def s15_estructura(d):
    sl = d.slide(tag="estructura")
    header(sl, "Salida estructurada", "Pedir JSON no basta: solicitar estructura y validarla",
           "La referencia pide al modelo que responda llamando a una herramienta con un esquema. Después Lambda vuelve a "
           "comprobarlo todo: un JSON bien formado puede seguir siendo inválido para nuestro contrato.")
    steps = [("1 · Solicitar", "toolConfig define emitir_clasificacion con el esquema del contrato; toolChoice obliga a usarla.", PINK),
             ("2 · Recibir", "Esperamos stopReason = tool_use y un único bloque toolUse con su input.", PINK),
             ("3 · Validar", "Nombre y número de herramientas; Pydantic comprueba categoría, prioridad y respuesta.", AMBER),
             ("4 · Responder", "200 con resultado y metadata, o 502 salida_invalida sin reparar ni reintentar.", MINT)]
    w = (874 - 3 * 16) / 4
    for i, (t, b, col) in enumerate(steps):
        x = 43 + i * (w + 16)
        box(sl, x, 132, w, 84, fill=CARD)
        box(sl, x, 132, w, 4, fill=col, radius=0)
        text(sl, x + 10, 142, w - 20, 16, t, size=12, color=TITLE, bold=True)
        text(sl, x + 10, 162, w - 20, 52, b, size=9.5, color=TEXT)
        if i < 3:
            line(sl, x + w + 2, 174, x + w + 14, 174, color=col, w=1.5)
    box(sl, 43, 228, 470, 238, fill=CARD, line=BORDER)
    text(sl, 55, 236, 440, 12, "FRAGMENTO DE bedrock.py · request_for()", size=9, color=PINK, bold=True)
    code = ['"inferenceConfig": {"maxTokens": 300},',
            '"toolConfig": {',
            '  "tools": [{"toolSpec": {',
            '    "name": "emitir_clasificacion",',
            '    "inputSchema": {"json": <esquema',
            '                    Clasificacion>}}}],',
            '  "toolChoice": {"tool":',
            '    {"name": "emitir_clasificacion"}}}']
    p = code_block(sl, 75, 256, 430, code, size=10, pitch=15)
    for li, n in [(0, 1), (3, 2), (4, 3), (6, 4)]:
        line_badge(sl, 55, 256, p, li, n, PINK)
    text(sl, 55, 384, 446, 78, [{"runs": [("1 ", {"bold": True, "color": PINK}), ("Tope de salida.  ", {"bold": True, "color": TITLE}),
                                          ("2 ", {"bold": True, "color": PINK}), ("Una herramienta con nombre fijo.  ", {"bold": True, "color": TITLE}),
                                          ("3 ", {"bold": True, "color": PINK}), ("El esquema sale del contrato Pydantic.  ", {"bold": True, "color": TITLE}),
                                          ("4 ", {"bold": True, "color": PINK}), ("Se fuerza esa herramienta.", {"bold": True, "color": TITLE})]},
                                {"runs": [("La herramienta es un esquema de salida: no ejecuta acciones ni provoca una segunda llamada al modelo.", {})]}],
         size=9.5, color=TEXT, space=4)
    text(sl, 527, 228, 390, 12, "LO QUE COMPRUEBA LAMBDA ANTES DE RESPONDER", size=9, color=AMBER, bold=True)
    checks = [("stopReason", "tool_use; si no, error salida_sin_estructura."),
              ("Herramientas", "Exactamente una, llamada emitir_clasificacion."),
              ("categoria", "acceso, facturacion, tecnico o consulta."),
              ("prioridad", "alta, media o baja."),
              ("respuesta", "Texto de 1 a 1.000 caracteres.")]
    y = 246
    for k, v in checks:
        box(sl, 527, y, 390, 28, fill=CARD)
        text(sl, 537, y + 7, 110, 14, k, size=10, font=MONO, color=MINT_L, bold=True)
        text(sl, 650, y + 7, 260, 14, v, size=9.5, color=TEXT)
        y += 31
    box(sl, 527, 406, 390, 60, fill=VIOLET_BG)
    text(sl, 537, 412, 372, 50, [[("Diferencia con S8  ", {"bold": True, "color": VIOLET}),
                                   ("Allí medíamos al modelo sin ayudas de formato. Aquí construimos un servicio: pedir "
                                    "estructura y validarla es un requisito.", {})]], size=9.5, color=TITLE)
    takeaway(sl, "La estructura se pide al modelo y se comprueba en nuestro código. Si no cumple el contrato, error controlado.",
             "Idea guía")
    footer(sl, block=2)
    notes(sl, """
""" + timing_note("18:58", "19:00") + """
QUÉ EXPLICAR: pedir JSON no elimina la necesidad de validar. La referencia usa toolConfig con una sola herramienta, emitir_clasificacion, cuyo inputSchema es el esquema Pydantic del contrato (Clasificacion), y toolChoice para forzarla (Nova 2 documenta toolChoice.tool). La herramienta es un esquema de salida: no ejecuta una acción de negocio ni requiere una segunda llamada. Lambda comprueba stopReason (tool_use), que haya exactamente una herramienta con ese nombre y valida el input con Pydantic. Si algo falla: 502 salida_invalida (o salida_sin_estructura), sin reparar, sin reintentar y sin cambiar a la demo. Diferencia con S8: allí se medía la capacidad del modelo de devolver JSON sin ayudas; aquí la robustez del servicio es el objetivo, y no se mezclan esos resultados.
CÓDIGO: abrir src/curso_ia/serverless/bedrock.py (request_for y classify) y src/curso_ia/contratos.py (Clasificacion).
CONSOLA: ninguna nueva; volver a la ficha si alguien pregunta por compatibilidad de herramientas.
PREGUNTA: «¿Qué hacemos si el modelo devuelve prioridad "urgente"?». Respuesta: error de salida controlado; no se corrige ni se reintenta de forma oculta.
FUENTES: Amazon Nova 2 User Guide, «Using tools» (selección de una herramienta concreta); Amazon Bedrock User Guide, «Tool use» y ficha «Nova 2 Lite» («Structured outputs» no figura como compatible), consultadas el 06/11/2026; src/curso_ia/serverless/bedrock.py y contratos.py.
IMÁGENES: diapositiva sin imágenes externas; código copiado de bedrock.py con el esquema abreviado.""")
    return sl


PART2 = [s09_div2, s10_bedrock, s11_ids, s12_ficha, s13_regiones, s14_playground, s15_estructura]
