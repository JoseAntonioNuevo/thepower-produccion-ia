"""Diapositivas 42–51: bloque 6 (IA gestionada y otras nubes), cierre y consulta."""
from deck_lib import *  # noqa: F401,F403


def s42_div6(d):
    sl = divider(d, 6, "IA y otras nubes", "IA gestionada y otras nubes",
                 "Amazon Bedrock, Microsoft Foundry, Vertex AI y las equivalencias entre AWS, Azure y Google Cloud.",
                 ["¿Qué diferencia hay entre alojar nuestra API y consumir un modelo?",
                  "¿Qué muestra el catálogo de Amazon Bedrock?",
                  "¿Qué ofrecen Microsoft Foundry y Vertex AI?",
                  "¿Cómo se llaman las mismas piezas en Azure y Google Cloud?"],
                 [("aws-bedrock.png", "Amazon\nBedrock"), ("az-foundry.png", "Microsoft\nFoundry"), ("gc-vertex.png", "Vertex AI")],
                 "19:42–19:49")
    notes(sl, """
TIEMPO 19:42 (10 s). Bloque 6 de 6: IA gestionada y otras nubes, de 19:42 a 19:49 (7 min). Es un primer vistazo: Bedrock y Lambda se trabajan en S17.
IMÁGENES: Amazon Bedrock (AWS Architecture Icons); Microsoft Foundry (Azure Public Service Icons V25, «AI Foundry»); Vertex AI (Google Cloud core product icons).""")
    return sl


def s43_alojar(d):
    sl = d.slide(tag="alojar")
    header(sl, "IA gestionada", "Alojar nuestra API no es lo mismo que consumir un modelo",
           "Fargate ejecuta nuestro código. El modelo vive en un servicio del proveedor y lo llamamos por API. Hoy nuestra API "
           "llama a Anthropic; en S17 la conectaremos con Amazon Bedrock.")
    flows = [("HOY · S16", MINT, TAKE_BG,
              [("g-client.png", "Cliente", "POST /clasificar"), ("aws-fargate.png", "Nuestra API", "ECS en Fargate"),
               ("g-generic-application.png", "API del proveedor", "Anthropic · modelo"), ("g-json-script.png", "Respuesta", "clasificación")],
              "HTTPS + clave de Secrets Manager"),
             ("S17 · CON AMAZON BEDROCK", PINK, PINK_BG,
              [("g-client.png", "Cliente", "a través de API Gateway"), ("aws-lambda.png", "Nuestra función", "AWS Lambda"),
               ("aws-bedrock.png", "Amazon Bedrock", "bedrock-runtime"), ("g-json-script.png", "Respuesta", "clasificación")],
              "rol de IAM: bedrock:InvokeModel")]
    y = 134
    for lab, col, bg, nodes, link in flows:
        box(sl, 43, y, 874, 112, fill=bg)
        text(sl, 55, y + 8, 300, 12, lab, size=9, color=col, bold=True)
        x = 55
        ws = [150, 190, 200, 150]
        for k, ((ic, t, sub), w) in enumerate(zip(nodes, ws)):
            box(sl, x, y + 28, w, 72, fill=CARD)
            img(sl, ic, x + 10, y + 46, w=32, h=32)
            text(sl, x + 50, y + 42, w - 56, 16, t, size=11, color=TITLE, bold=True)
            text(sl, x + 50, y + 60, w - 56, 30, sub, size=9.5, color=TEXT)
            if k < 3:
                gapw = 52 if k == 1 else 22
                line(sl, x + w + 2, y + 64, x + w + gapw - 2, y + 64, color=col, w=1.5)
            x += w + (52 if k == 1 else 22)
        chip(sl, 470, y + 8, 220, 16, link, fill=CARD2, color=col, size=8.5, line=col)
        y += 120
    cards = [("Qué alojamos", "Código, contenedor o función, red, logs y permisos. Pagamos cómputo y recursos.", MINT),
             ("Qué consumimos", "Capacidad de inferencia del proveedor por API. Pagamos tokens o capacidad reservada.", BLUE),
             ("Qué cambia con Bedrock", "Autenticación con IAM en lugar de una clave externa, factura en AWS y disponibilidad por región.", PINK)]
    for i, (t, b, col) in enumerate(cards):
        x = 43 + i * 296
        box(sl, x, 376, 284, 90, fill=CARD)
        box(sl, x, 376, 4, 90, fill=col, radius=0)
        text(sl, x + 16, 384, 260, 18, t, size=13.5, font=SERIF, color=TITLE)
        text(sl, x + 16, 406, 258, 56, b, size=10.5, color=TEXT)
    takeaway(sl, "Ningún modelo se descarga en nuestra imagen: el contenedor solo contiene la aplicación que lo llama.", "Idea guía")
    footer(sl, 43, 6)
    notes(sl, """
TIEMPO 19:42–19:44 (2 min).
QUÉ EXPLICAR: dos decisiones distintas. Alojar la aplicación (Fargate, Lambda, EC2…) y consumir un modelo gestionado (Anthropic directamente, Amazon Bedrock, Microsoft Foundry, Vertex AI). Hoy la API corre en Fargate y llama por HTTPS a la API de Anthropic con una clave guardada en Secrets Manager. En S17 mantendremos el contrato y cambiaremos el recorrido: API Gateway → Lambda → Bedrock, autenticando con un rol de IAM (bedrock:InvokeModel) en lugar de una clave externa. No anticipar la práctica de S17.
CONSOLA: ninguna en esta diapositiva (la siguiente abre Bedrock).
PREGUNTA: «¿Fargate es el modelo?». Respuesta: no; es el cómputo que ejecuta nuestra API.
FUENTES: guion de S16 y repositorio 4-produccion-ia (adaptador de Anthropic; S17 con Lambda, HTTP API e IAM para Bedrock); Amazon Bedrock User Guide, «What is Amazon Bedrock?».
IMÁGENES: AWS Architecture Icons: Fargate, Lambda, Bedrock; genéricos Client, Generic Application y JSON Script.""")
    return sl


def s44_bedrock(d):
    sl = d.slide(tag="bedrock")
    header(sl, "Amazon Bedrock", "El catálogo de Bedrock: proveedores, modalidades y región",
           "En la consola, Bedrock › Model catalog lista los modelos disponibles. Filtramos por proveedor y modalidad, "
           "y comprobamos en qué regiones se ofrece cada uno antes de elegir.")
    ui_panel(sl, 43, 132, 500, 336, title="Model catalog", crumbs="Amazon Bedrock  ›  Model catalog")
    esquema_label(sl, 388, 135, w=150, t="ESQUEMA · no es una captura")
    box(sl, 51, 188, 118, 272, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    text(sl, 57, 194, 100, 12, "Filters", size=9.5, color=UI_TEXT, bold=True, check=False)
    ui_field(sl, 57, 212, 108, "Providers", [("Amazon", False), ("Anthropic", True), ("Cohere", False), ("Meta", False),
                                             ("Mistral AI", False), ("…", False)], kind="check")
    ui_field(sl, 57, 310, 108, "Modality", [("Texto", True), ("Imagen", False), ("Embeddings", False), ("Vídeo", False), ("Audio", False)], kind="check")
    badge(sl, 150, 210, 1, fill=AMBER, d=14, size=8)
    badge(sl, 150, 308, 2, fill=AMBER, d=14, size=8)
    models = [("Anthropic", "Claude Sonnet 4.6", "texto, imagen → texto"),
              ("Amazon", "Nova 2 Lite", "texto, imagen, vídeo → texto"),
              ("Meta", "Llama 3.3 70B Instruct", "texto → texto"),
              ("Cohere", "Embed v4", "texto, imagen → embeddings"),
              ("Stability AI", "Stable Image Core 1.0", "texto → imagen"),
              ("Amazon", "Titan Text Embeddings V2", "texto → embeddings")]
    for i, (p, m, mod) in enumerate(models):
        r, c = divmod(i, 2)
        x = 177 + c * 180
        y = 188 + r * 92
        box(sl, x, y, 172, 84, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
        text(sl, x + 8, y + 8, 150, 12, p, size=8.5, color=UI_MUTED, check=False)
        text(sl, x + 8, y + 22, 158, 28, m, size=10, color=UI_BLUE, bold=True, check=False)
        text(sl, x + 8, y + 52, 158, 26, mod, size=8.5, color=UI_TEXT, check=False)
    badge(sl, 527, 236, 3, fill=AMBER, d=14, size=8)
    text(sl, 557, 132, 360, 12, "PROVEEDORES EN EL CATÁLOGO · docs de AWS, 06/11/2026", size=9, color=PINK, bold=True)
    provs = ["AI21 Labs", "Amazon", "Anthropic", "Cohere", "DeepSeek", "Google", "Luma AI", "Meta", "MiniMax", "Mistral AI",
             "Moonshot AI", "NVIDIA", "OpenAI", "Qwen", "Stability AI", "TwelveLabs", "Writer", "xAI", "Z.AI"]
    x, y = 557, 150
    for p in provs:
        w = len(p) * 5.4 + 16
        if x + w > 917:
            x = 557
            y += 22
        chip(sl, x, y, w, 18, p, fill=CARD2, color=TITLE, size=8.5, bold=False, line=BORDER)
        x += w + 5
    y += 30
    ann = [("Proveedor", "Quién ha creado el modelo y sus condiciones."),
           ("Modalidad", "Qué entra y qué sale: texto, imagen, vídeo, audio o embeddings."),
           ("Ficha del modelo", "ID, regiones, contexto, precios y si admite Converse.")]
    for i, (t, b) in enumerate(ann):
        badge(sl, 557, y + 1, i + 1, fill=AMBER, d=14, size=8)
        text(sl, 577, y, 340, 30, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10, color=TEXT)
        y += 30
    box(sl, 557, y + 2, 360, 70, fill=PINK_BG)
    text(sl, 567, y + 8, 342, 60, "Acceso: muchos modelos vienen habilitados si la cuenta tiene los permisos de AWS Marketplace; "
                                  "Anthropic exige además un formulario de primer uso. Ver la ficha no cuesta; invocar sí.",
         size=9.5, color=TITLE)
    cost_chip(sl, 557, y + 80, 360, "Tokens de entrada y salida (o imágenes, segundos…), según modelo, región y modo de inferencia.",
              h=468 - (y + 80) if 468 - (y + 80) > 30 else None, size=9.5)
    takeaway(sl, "Elegir modelo es también elegir región, permisos, cuotas y precio. En S17 haremos la llamada desde Lambda.", "Idea guía")
    footer(sl, 44, 6)
    notes(sl, """
TIEMPO 19:44–19:46 (2 min). Recorrido en consola, sin invocar modelos.
QUÉ ES: Amazon Bedrock ofrece modelos fundacionales de varios proveedores mediante una API común (InvokeModel y Converse), con autenticación IAM y facturación en AWS. QUÉ VEMOS: Bedrock › Model catalog con filtros por proveedor y modalidad; cada ficha indica ID del modelo, regiones, modalidades de entrada y salida y enlaces de precio. RELACIÓN: IAM (bedrock:InvokeModel), región, cuotas, CloudWatch y, en S17, Lambda.
ACCESO (docs de AWS consultados el 06/11/2026): muchos modelos están habilitados por defecto si la identidad tiene permisos de AWS Marketplace; la primera invocación de un modelo de terceros inicia la suscripción; los modelos de Anthropic exigen un formulario de primer uso (First Time Use).
CONSOLA: comprobar región (Europa · Irlanda) → Amazon Bedrock › Model catalog → filtrar por proveedor (Anthropic, Amazon, Meta…) y modalidad → abrir una ficha y señalar Model ID, regiones y precios. NO abrir el playground para invocar, NO enviar el formulario de casos de uso y NO activar suscripciones.
COMPARACIÓN: Microsoft Foundry (Azure) y Vertex AI (Google Cloud) cumplen una función parecida: catálogo de modelos, identidad de la nube, cuotas y facturación propias. Varían catálogo, regiones, permisos y precios.
PREGUNTA: «Un modelo aparece en us-east-1 pero no en eu-west-1. ¿Qué opciones tenemos?». Respuesta: elegir otro modelo o región y revisar requisitos de datos y latencia (o perfiles de inferencia entre regiones, que se verán más adelante).
FUENTES: Amazon Bedrock User Guide, «Models at a glance» (docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html, lista de proveedores consultada el 06/11/2026) y «Request access to models» (model-access.html). Los modelos del esquema figuran en esa lista; sus modalidades se resumen de las fichas oficiales.
IMÁGENES: ESQUEMA propio del catálogo (no es una captura); los nombres de proveedores se muestran como texto, sin logotipos.""")
    return sl


def s45_nubes(d):
    sl = d.slide(tag="nubes")
    header(sl, "Otras nubes", "Las mismas funciones en AWS, Azure y Google Cloud",
           "Correspondencias por función para orientarse. No implican las mismas APIs, límites, precios ni prestaciones.")
    cx = [223, 455, 687]
    cw = 226
    hdrs = [("aws-logo-light.png", 22, None), ("az-logo.png", 22, "Microsoft Azure"), ("gc-logo.png", 17, None)]
    for x, (lg, h, lab) in zip(cx, hdrs):
        box(sl, x, 120, cw, 32, fill="FFFFFF", radius=5)
        if lab:
            img(sl, lg, x + 50, 125, h=h)
            text(sl, x + 78, 128, 140, 16, lab, size=11, color=UI_TEXT, bold=True)
        else:
            w, _ = img_size(lg, h=h)
            img(sl, lg, x + (cw - w) / 2, 120 + (32 - h) / 2, h=h)
    rows = [("Máquina virtual", ("aws-ec2.png", "Amazon EC2"), ("az-vm.png", "Azure Virtual Machines"), ("gc-compute.png", "Compute Engine")),
            ("Contenedores gestionados", ("aws-fargate.png", "Amazon ECS + Fargate"), ("az-containerapps.png", "Azure Container Apps"), ("gc-run.png", "Cloud Run")),
            ("Funciones", ("aws-lambda.png", "AWS Lambda"), ("az-functions.png", "Azure Functions"), ("gc-functions.png", "Cloud Run functions")),
            ("Almacenamiento de objetos", ("aws-s3.png", "Amazon S3"), ("az-storage.png", "Azure Blob Storage"), ("gc-storage.png", "Cloud Storage")),
            ("Red privada", ("aws-vpc.png", "Amazon VPC"), ("az-vnet.png", "Azure Virtual Network"), ("gc-vpc.png", "VPC")),
            ("Identidad y permisos", ("aws-iam.png", "AWS IAM"), ("az-entra.png", "Microsoft Entra ID + Azure RBAC"), ("gc-iam.png", "Cloud IAM")),
            ("Base de datos relacional", ("aws-rds.png", "Amazon RDS"), ("az-sql.png", "Azure SQL Database"), ("gc-sql.png", "Cloud SQL")),
            ("IA gestionada", ("aws-bedrock.png", "Amazon Bedrock"), ("az-foundry.png", "Microsoft Foundry"), ("gc-vertex.png", "Vertex AI"))]
    y = 158
    for i, (fn, *cells) in enumerate(rows):
        hl = fn == "IA gestionada"
        box(sl, 43, y, 174, 36, fill=PINK_BG if hl else CARD, radius=3)
        text(sl, 53, y + 4, 160, 28, fn, size=10.5, color=PINK if hl else TITLE, bold=True, anchor="m")
        for x, (ic, nm) in zip(cx, cells):
            box(sl, x, y, cw, 36, fill=PINK_BG if hl else CARD, radius=3)
            img(sl, ic, x + 8, y + 6, w=24, h=24)
            text(sl, x + 40, y + 4, cw - 46, 28, nm, size=10.5, color=TITLE, bold=hl, anchor="m")
        y += 39
    takeaway(sl, "Elegimos nube por datos, identidad, región, modelos, operación y coste de la arquitectura completa, no por el número de servicios.",
             "Idea guía", y=476)
    footer(sl, 45, 6)
    notes(sl, """
TIEMPO 19:46–19:49 (3 min).
QUÉ EXPLICAR: comparación por funciones, no por logotipos. Máquina virtual: EC2 / Azure Virtual Machines / Compute Engine. Contenedores gestionados: ECS con Fargate / Azure Container Apps / Cloud Run (para Kubernetes: EKS / AKS / GKE). Funciones: Lambda / Azure Functions / Cloud Run functions (antes Cloud Functions). Objetos: S3 / Blob Storage / Cloud Storage. Red: VPC / Virtual Network / VPC. Identidad: IAM / Microsoft Entra ID con Azure RBAC / Cloud IAM (modelos de autorización distintos). Base de datos relacional: RDS / Azure SQL Database (o Azure Database for PostgreSQL) / Cloud SQL. IA gestionada: Amazon Bedrock / Microsoft Foundry / Vertex AI.
IA GESTIONADA: los tres permiten consumir modelos gestionados con la identidad, las cuotas y la facturación de su nube. Varían catálogo, regiones, permisos, privacidad y precios. Elegir una nube para la IA no obliga a alojar allí la aplicación, pero mover datos tiene coste y latencia.
CONSOLA: ninguna (no abrimos Azure ni Google Cloud).
PREGUNTA: «La empresa ya tiene identidad y datos en Azure. ¿Es obligatorio irse a AWS para usar IA gestionada?». Respuesta: no; comparar requisitos, datos, identidad, región, modelos y coste total.
FUENTES: Microsoft Learn, «Azure for AWS professionals» y comparativas de servicios (learn.microsoft.com/azure/architecture/aws-professional/); Google Cloud, «Compare AWS and Azure services to Google Cloud» (docs.cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison). Son correspondencias funcionales, no equivalencias exactas.
IMÁGENES: logotipo de AWS (a0.awsstatic.com, versión monocroma Squid Ink); iconos de AWS Architecture Icons (31/07/2026); iconos de Azure Public Service Icons V25 y Microsoft Entra architecture icons (Microsoft, uso permitido en materiales de formación); logotipo de Google Cloud (gstatic.com) e iconos oficiales de Google Cloud (core products y legacy: Cloud Functions, VPC, IAM).""")
    return sl


def s46_practica(d):
    sl = d.slide(tag="practica")
    header(sl, "Práctica opcional", "Práctica opcional: desplegar la API con Docker",
           "Los ejercicios de estas sesiones no son obligatorios, según confirmó Laura el 4 de noviembre. Si decides hacerla, "
           "este es el recorrido y lo que debe contener la entrega.")
    chip(sl, 829, 40, 88, 22, "OPCIONAL", fill=AMBER, color=DARK, size=11)
    box(sl, 43, 132, 430, 92, fill=CARD, line=BORDER)
    text(sl, 55, 140, 400, 12, "ENUNCIADO DE S16 · ENCARGO DE EJERCICIOS DEL 10 DE AGOSTO", size=8.5, color=MINT, bold=True)
    text(sl, 55, 156, 410, 22, "«Sesión 16 Cloud deployment: Desplegar una aplicación con Docker.»", size=12, font=SERIF, color=TITLE, italic=True)
    text(sl, 55, 182, 410, 38, "La concreción con ECR, ECS/Fargate y Secrets Manager procede del enunciado enviado por José el 28/09.",
         size=9.5, color=MUTED)
    box(sl, 485, 132, 432, 92, fill=CARD, line=BORDER)
    info = [("Dedicación", "4–6 horas con cuenta, permisos y entorno preparados."),
            ("Punto de partida", "S16-inicio.zip, con la API ya preparada."),
            ("Ayuda", "Guía del alumno con comandos y proyecto de referencia.")]
    yy = 140
    for t, b in info:
        text(sl, 497, yy, 410, 26, [[(t + "  ", {"bold": True, "color": MINT_L}), (b, {})]], size=10.5, color=TEXT)
        yy += 26
    steps = [("Docker local", "/health, /clasificar en demo y usuario 10001."),
             ("ECR", "Imagen publicada con etiqueta y digest."),
             ("Task definition", "Imagen por digest, X86_64 y secreto por ARN."),
             ("Red", "Entrada /32 al 8000; salida 443."),
             ("Salud y función reales", "request_id localizado en CloudWatch."),
             ("Coste y retirada", "730 h, demo e inventario final.")]
    w = (874 - 5 * 8) / 6
    for i, (t, b) in enumerate(steps):
        x = 43 + i * (w + 8)
        box(sl, x, 234, w, 108, fill=CARD)
        badge(sl, x + 10, 244, i + 1, fill=CORAL if i < 4 else BLUE, d=20, size=10)
        text(sl, x + 36, 244, w - 42, 32, t, size=10.5, color=TITLE, bold=True)
        text(sl, x + 10, 282, w - 18, 56, b, size=9.5, color=TEXT)
    box(sl, 43, 352, 520, 114, fill=CARD)
    text(sl, 55, 360, 400, 12, "SI LA HACES, LA ENTREGA INCLUYE", size=9, color=MINT, bold=True)
    ent = ["Código, lock, Dockerfile y .dockerignore; procedimiento reproducible.",
           "Evidencia real: imagen identificada, tarea, salud y una petición funcional.",
           "Coste con región, fecha, tarifas, supuestos e inferencia aparte.",
           "Retirada e inventario: qué se eliminó, qué se conserva y por qué."]
    text(sl, 55, 378, 500, 86, [{"runs": [("•  ", {"color": MINT, "bold": True}), (t, {})], "space": 3} for t in ent], size=10.5, color=TEXT, space=3)
    box(sl, 575, 352, 342, 114, fill=CORAL_BG)
    text(sl, 587, 360, 320, 12, "ANTES DE EMPEZAR", size=9, color=CORAL, bold=True)
    text(sl, 587, 378, 322, 84, "Crea recursos con coste: usa una cuenta de laboratorio, un presupuesto y la retirada al terminar. "
                                "El modo demo sirve para practicar sin gasto, pero no sustituye la evidencia real.", size=10.5, color=TITLE)
    takeaway(sl, "Si la haces, la prueba no es una pantalla verde: es la imagen identificada, una petición real y el inventario de lo retirado.",
             "Idea guía")
    footer(sl, 46)
    notes(sl, """
TIEMPO 19:49–19:51 (2 min).
QUÉ EXPLICAR: la práctica es OPCIONAL (Laura, 04/11/2026: los ejercicios de estas sesiones no son obligatorios). El encargo de ejercicios de Laura del 10/08 dice literalmente: «Sesión 16 Cloud deployment: Desplegar una aplicación con Docker». La concreción técnica (ECR, ECS/Fargate, Secrets Manager, coste de 730 h y limpieza) es la del enunciado que redactó José y envió el 28/09; no atribuirla a Laura.
RECORRIDO: seis pasos con su evidencia. Empezar por S16-inicio.zip y la guía del alumno; la referencia completa queda como consulta. Dedicación orientativa 4–6 horas con cuenta, permisos y entorno preparados.
AVISO: hoy no hemos desplegado nada. Los materiales dejan pendientes el ensayo en AWS, la inferencia real y la retirada remota; no presentar recibos anteriores como ejecución de hoy.
PREGUNTA: «¿Qué evidencia falta si solo tengo health 200?». Respuesta: una petición funcional real y su correspondencia con la versión desplegada.
FUENTES: material/S16/enunciado.md y guia-alumno.md; correos de Laura del 10/08/2026 (encargo de ejercicios) y del 04/11/2026 (ejercicios no obligatorios, teoría junto a práctica); enunciado de José del 28/09/2026 (AI_Engineer_enunciados.docx, pág. 5).
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


def s47_cierre(d):
    sl = d.slide(BG_SECTION, tag="cierre")
    img(sl, "thepower-logo.png", 38, 34, h=30)
    text(sl, 43, 92, 300, 14, "CIERRE", size=10, color=MINT, bold=True)
    text(sl, 43, 110, 520, 44, "Lo que nos llevamos", size=32, font=SERIF, color=TITLE)
    pts = ["La región y la cuenta determinan qué vemos y dónde viven los recursos.",
           "IAM decide qué acción se permite sobre qué recurso; la red decide qué conexión llega.",
           "EC2 con EBS es una máquina que administramos; S3 guarda objetos; Fargate ejecuta contenedores.",
           "ECR guarda la imagen; ECS la describe y la mantiene; el secreto se inyecta al arrancar.",
           "CloudWatch une cada petición con su log; factura, estimación, presupuesto y alerta son cosas distintas.",
           "Consumir un modelo gestionado no es lo mismo que alojar nuestra API."]
    y = 170
    for i, p in enumerate(pts):
        circle(sl, 43, y, 22, MINT_L)
        text(sl, 43, y + 3, 22, 16, str(i + 1), size=10.5, color=DARK, bold=True, align="c", check=False)
        text(sl, 76, y + 1, 460, 40, p, size=12.5, color=TITLE)
        y += 48
    box(sl, 584, 150, 333, 312, fill="1A463C", radius=8)
    text(sl, 604, 168, 300, 40, "¿Preguntas?", size=30, font=SERIF, color=MINT_L)
    text(sl, 604, 222, 300, 12, "PRÓXIMA SESIÓN · S17", size=9, color=MINT, bold=True)
    text(sl, 604, 238, 300, 56, "API Gateway, AWS Lambda y Amazon Bedrock con el mismo caso de soporte.", size=12, color=TITLE)
    imgs = ["aws-lambda.png", "aws-bedrock.png"]
    for k, ic in enumerate(imgs):
        img(sl, ic, 604 + k * 44, 298, w=34, h=34)
    text(sl, 604, 346, 300, 12, "MATERIALES DE S16", size=9, color=MINT, bold=True)
    text(sl, 604, 362, 300, 90, "Presentación, guía del alumno, enunciado de la práctica opcional y paquetes S16-inicio y "
                                "S16-referencia.", size=11, color=TITLE)
    notes(sl, """
TIEMPO 19:51–20:00 (9 min): dos minutos de recapitulación y siete de preguntas.
QUÉ EXPLICAR: leer los seis puntos y pedir a un alumno que recorra en voz alta el mapa de la diapositiva 4 nombrando cada servicio.
RECUPERACIÓN ACTIVA: «¿Qué diferencia hay entre imagen, ECR y Fargate?» (artefacto, registro, cómputo). «¿Quién lee el secreto inyectado al arrancar?» (execution role). «¿Qué falta si solo vemos health 200?» (una petición funcional real). «¿Qué permanece si paramos la tarea?» (ECR, secreto, logs y lo que no se haya retirado).
SI NADIE PREGUNTA: dos casos: «Docker local funciona, pero AWS no descarga la imagen» (execution role, URI/región, salida de red) y «La API funciona, pero el secreto se ha rotado» (reemplazar las tareas).
CONEXIÓN CON S17: mismo caso; cambiamos el alojamiento a Lambda con API Gateway y el modelo a Bedrock con IAM.
CERRAR a las 20:00. No hay recursos que retirar: hoy no se ha creado nada en AWS.
FUENTES: guion de S16; materiales de material/S16.
IMÁGENES: logotipo de thePower (recurso original del curso); iconos de Lambda y Bedrock de AWS Architecture Icons.""")
    return sl


def consulta_header(sl, title, sub):
    header(sl, "Consulta", title, sub)


def s48_ruta(d):
    sl = d.slide(tag="ruta")
    consulta_header(sl, "Consulta · recorrido por la consola",
                    "Ruta, campos que conviene señalar y qué determina el coste de cada servicio de la sesión. Útil para repasar o repetir el recorrido.")
    rows = [["Servicio", "Ruta en la consola", "Qué señalar", "Qué determina el coste"],
            ["IAM", "IAM › Roles › (rol)", "Permissions, Trust relationships; «Global»", "Sin cargo"],
            ["EC2", "EC2 › Instances › Launch instances", "AMI, Instance type, Network settings, Storage", "Segundos en marcha, EBS, IPv4"],
            ["EBS", "EC2 › Elastic Block Store › Volumes", "Type, Size, IOPS, zona, Encryption", "GB-mes aprovisionados"],
            ["S3", "S3 › General purpose buckets › Create bucket", "Region, Block Public Access, Versioning, Encryption", "GB-mes, peticiones y salida"],
            ["VPC", "VPC › Your VPCs › Resource map", "Subredes, tablas de rutas, internet gateway", "NAT, IPv4 y tráfico"],
            ["Security groups", "VPC › Security groups › Inbound rules", "Type, Port range, Source /32", "Sin cargo"],
            ["ECR", "ECR › Private registry › Repositories", "Tag mutability, digest, encryption", "GB-mes almacenados"],
            ["ECS y Fargate", "ECS › Clusters · Task definitions", "Revisión, CPU y memoria, roles, secrets, logs", "vCPU-h y GB-h de Fargate"],
            ["Secrets Manager", "Secrets Manager › Secrets", "Name, ARN, Rotation (sin Retrieve)", "Secreto-mes y llamadas"],
            ["CloudWatch", "CloudWatch › Logs › Log groups · Alarms", "Retención, streams, request_id", "GB ingeridos y almacenados"],
            ["Billing", "Billing and Cost Management › Bills · Cost Explorer · Budgets", "Factura, previsión, umbrales", "Consultar en la consola: sin cargo"],
            ["Bedrock", "Bedrock › Model catalog", "Proveedor, modalidad, regiones, acceso", "Tokens al invocar"]]
    table(sl, 43, 130, 874, [110, 300, 280, 184], rows, size=9.5, row_h=26, font_cols={1: MONO},
          bold_cols=(0, 1), colors={0: TITLE, 1: MINT_L})
    footer(sl, 48)
    notes(sl, """
DIAPOSITIVA DE CONSULTA (no se proyecta en el tiempo de clase salvo para responder dudas).
USO: resumen del recorrido por la consola de AWS con la ruta de cada servicio, lo que conviene señalar y el motor de su coste. En todos los casos: comprobar la región, abrir listados y formularios, cancelar antes de crear y no mostrar valores de secretos.
NOTA SOBRE BILLING: consultar Bills, Cost Explorer o Budgets en la consola no tiene cargo; algunas funciones avanzadas (por ejemplo, llamadas a la API de Cost Explorer o presupuestos con acciones por encima de los incluidos) tienen tarifa propia.
FUENTES: las citadas en las diapositivas de cada servicio (AWS documentation, consultada entre el 22/10 y el 06/11/2026).""")
    return sl


def s49_costes(d):
    sl = d.slide(tag="tabla-costes")
    consulta_header(sl, "Consulta · cálculo completo de costes",
                    "Nueve partidas, dos escenarios y la misma fuente de tarifas. Región eu-west-1 (Irlanda), tarifas leídas el 17/10/2026, USD sin impuestos.")
    R = {"align": "r", "font": MONO, "bold": True}
    rows = [["Concepto", "Unidad", "Tarifa USD", "Cantidad 730 h", "USD 730 h", "Cantidad demo", "USD demo"],
            ["CPU", "vCPU-h", ("0,04048", R), ("182,5", R), ("7,3876", R), ("0,375", R), ("0,0152", R)],
            ["Memoria", "GB-h", ("0,004445", R), ("365", R), ("1,6224", R), ("0,75", R), ("0,0033", R)],
            ["IPv4 pública", "IP-h", ("0,005", R), ("730", R), ("3,6500", R), ("1,5", R), ("0,0075", R)],
            ["ECR", "GB-mes", ("0,10", R), ("0,25", R), ("0,0250", R), ("0,25", R), ("0,0250", R)],
            ["Logs ingeridos", "GB", ("0,57", R), ("1", R), ("0,5700", R), ("0,01", R), ("0,0057", R)],
            ["Logs almacenados", "GB-mes", ("0,03", R), ("1", R), ("0,0300", R), ("0,01", R), ("0,0003", R)],
            ["Secreto conservado", "secreto-mes", ("0,40", R), ("1", R), ("0,4000", R), ("1", R), ("0,4000", R)],
            ["Lecturas del secreto", "petición", ("0,000005", R), ("2", R), ("0,00001", R), ("1", R), ("0,000005", R)],
            ["Salida a Internet", "GB facturable", ("0,09", R), ("1", R), ("0,0900", R), ("0,001", R), ("0,00009", R)],
            [("Total", {"bold": True, "color": MINT_L}), "", "", "", ("13,7750 → 13,78", {"align": "r", "font": MONO, "bold": True, "color": MINT_L}),
             "", ("0,4571 → 0,46", {"align": "r", "font": MONO, "bold": True, "color": MINT_L})]]
    table(sl, 43, 128, 874, [150, 110, 100, 120, 140, 120, 134], rows, size=10, row_h=24, bold_cols=(0,), colors={0: TITLE})
    text(sl, 43, 402, 874, 66,
         [{"runs": [("Demo: ", {"bold": True, "color": TITLE}),
                    ("cómputo e IPv4 0,0260 · retención de 30 días 0,4253 · uso 0,0058 USD. Total sin redondear 0,45710875 USD.", {})], "space": 3},
          {"runs": [("Fuentes: ", {"bold": True, "color": TITLE}),
                    ("catálogo público AWS Price List (eu-west-1), docs/fuentes/tarifas-aws-2026-10-17.json y datos/costes-ejemplo.json. "
                     "Cantidades supuestas; sin NAT, balanceador, base de datos ni KMS propia; inferencia aparte. No es una factura.", {})]}],
         size=10, color=TEXT, space=3)
    footer(sl, 49)
    notes(sl, """
DIAPOSITIVA DE CONSULTA.
CÁLCULO: 730 h → CPU 182,5 × 0,04048 = 7,3876; memoria 365 × 0,004445 = 1,622425; IPv4 730 × 0,005 = 3,65; ECR 0,25 × 0,10 = 0,025; logs ingeridos 0,57; logs almacenados 0,03; secreto 0,40; lecturas 2 × 0,000005 = 0,00001; salida 0,09. Total 13,775035 → 13,78 USD.
Demo → CPU 0,375 × 0,04048 = 0,01518; memoria 0,75 × 0,004445 = 0,00333375; IPv4 1,5 × 0,005 = 0,0075; ECR 0,025; logs ingeridos 0,0057; logs almacenados 0,0003; secreto 0,40; lectura 0,000005; salida 0,00009. Total 0,45710875 → 0,46 USD.
Las URLs de cada tarifa (offers/v1.0/aws/<servicio>/current/eu-west-1/index.json) están en datos/costes-ejemplo.json. Si se actualizan las tarifas, recalcular todas las cifras con scripts/costes.py y revisar las diapositivas de coste mensual, coste de la demo y esta tabla.""")
    return sl


def s50_comandos(d):
    sl = d.slide(tag="comandos")
    consulta_header(sl, "Consulta · comandos de la práctica opcional",
                    "Resumen de la guía del alumno. En clase no se ejecutan: los que llevan --execute crean, modifican o gastan recursos.")
    box(sl, 43, 130, 430, 200, fill="0B151B", line=BORDER)
    box(sl, 43, 340, 430, 126, fill=CARD, line=BORDER)
    text(sl, 55, 348, 400, 12, "DÓNDE ENCONTRARLO", size=9, color=MINT, bold=True)
    text(sl, 55, 366, 408, 96, [{"runs": [("•  ", {"color": MINT, "bold": True}), (t, {})], "space": 3} for t in [
        "Guía del alumno, secciones 2 a 11: comandos completos y resultados esperados.",
        "S16-inicio.zip: punto de partida con la API preparada.",
        "S16-referencia.zip: solución completa para consultar cada configuración."]], size=10, color=TEXT, space=3)
    text(sl, 55, 138, 400, 12, "SIN AWS · offline o lectura", size=9, color=MINT, bold=True)
    off = ["uv sync --frozen --all-extras",
           "uv run python scripts/preflight.py",
           "uv run pytest",
           "docker compose up --build -d",
           "uv run python scripts/ensayo_local.py",
           "docker build --platform linux/amd64 \\",
           "  --provenance=false -t thepower-s16:ensayo .",
           "uv run python scripts/costes.py \\",
           "  datos/costes-ejemplo.json",
           'uv run python scripts/aws_lab.py plan "${S16_ARGS[@]}"',
           'uv run python scripts/aws_lab.py estado "${S16_ARGS[@]}"']
    text(sl, 55, 156, 412, 166, "\n".join(off), size=9.5, font=MONO, color=MINT_L, bold=True, lsp=Pt(14), check=False)
    box(sl, 487, 130, 430, 200, fill="0B151B", line=CORAL)
    text(sl, 499, 138, 400, 12, "CREAN, MODIFICAN O GASTAN · requieren --execute", size=9, color=CORAL, bold=True)
    ex = ["aws_lab.py bootstrap      registro ECR",
          "aws_lab.py publicar       build, push y digest",
          "aws_lab.py crear-secreto  secreto (entrada oculta)",
          "aws_lab.py desplegar      red, roles, logs y servicio",
          "aws_lab.py verificar      salud + 1 inferencia real",
          "aws_lab.py limpiar        retira servicio y ECR propios",
          "aws_lab.py retirar-secreto  borrado programado (7 días)"]
    text(sl, 499, 156, 412, 120, "\n".join(ex), size=9.5, font=MONO, color=TITLE, bold=True, lsp=Pt(16), check=False)
    text(sl, 499, 274, 410, 54, 'Todos usan "${S16_ARGS[@]}": perfil, región, cuenta esperada y laboratorio propio (s16-…). '
                                "Comprueban la cuenta con STS y se detienen si no coincide.", size=10, color=TEXT)
    box(sl, 487, 340, 430, 126, fill=CORAL_BG)
    text(sl, 499, 350, 400, 12, "ANTES DE EJECUTAR", size=9, color=CORAL, bold=True)
    text(sl, 499, 368, 410, 92, "No pegues claves en la terminal, en argumentos, en capturas ni en consultas a una IA de ayuda. "
                                "Ejecuta solo con cuenta, presupuesto y destino autorizados.", size=10.5, color=TITLE)
    footer(sl, 50)
    notes(sl, """
DIAPOSITIVA DE CONSULTA. Material de apoyo para la práctica opcional; no se ejecuta en clase.
OFFLINE: instalación con lock, preflight (modo demo, sin comprobaciones remotas), tests, Compose, ensayo local en loopback, build linux/amd64 y calculadora de costes. LECTURA: aws_lab.py plan (offline) y estado (lee AWS).
CON --execute: bootstrap (ECR), publicar (build amd64, login por stdin, push y digest), crear-secreto (entrada oculta), desplegar (CloudFormation: VPC, subred, ruta, security group, logs, roles, cluster, task definition y servicio), verificar (GET /health y una clasificación real: consume una inferencia), limpiar (servicio, red, roles, logs y ECR propios) y retirar-secreto (borrado programado con siete días de recuperación). Las guardas comprueban cuenta (STS), región y propiedad del laboratorio.
FUENTES: material/S16/guia-alumno.md (secciones 2 a 11); scripts/aws_lab.py; AGENTS.md del repositorio (los comandos de modificación requieren --execute y autorización expresa).""")
    return sl


def s51_fuentes(d):
    sl = d.slide(tag="fuentes")
    consulta_header(sl, "Consulta · fuentes de contenido e imágenes",
                    "Documentación técnica consultada, procedencia de logotipos, iconos y capturas, y materiales del curso.")
    cols = [("DOCUMENTACIÓN TÉCNICA", MINT,
             ["AWS Management Console Getting Started Guide.",
              "IAM User Guide: políticas, evaluación, buenas prácticas, ARN.",
              "Amazon EC2 y EBS User Guides; S3 User Guide (create bucket, namespaces).",
              "Amazon VPC User Guide (how it works, internet gateways, security groups).",
              "Amazon ECR y ECS Developer Guides (task definition, execution role, Fargate networking).",
              "Secrets Manager, CloudWatch Logs, Cost Management (Cost Explorer, Budgets).",
              "Amazon Bedrock User Guide: Models at a glance y Request access to models (06/11/2026).",
              "Microsoft Learn: Azure for AWS professionals. Google Cloud: service comparison."]),
            ("IMÁGENES Y LOGOTIPOS", AMBER,
             ["AWS Architecture Icons, paquete del 31/07/2026 (aws.amazon.com/architecture/icons).",
              "Logotipo de AWS: a0.awsstatic.com; versión clara en su color Squid Ink.",
              "Azure Public Service Icons V25 y Microsoft Entra icons (uso permitido en formación).",
              "Google Cloud: logotipo de gstatic.com e iconos oficiales (core y legacy).",
              "Docker: Docker-Logos-1.zip de docker.com (media resources).",
              "Capturas oficiales: modelo de responsabilidad compartida (aws.amazon.com) y Resource map de la VPC User Guide.",
              "Captura real de calculator.aws del 06/11/2026.",
              "Pantallas rotuladas «ESQUEMA»: dibujos propios, no capturas."]),
            ("MATERIALES DEL CURSO", BLUE,
             ["Temario AI Engineer (Laura, 17/07/2026): «Cloud deployment: AWS basics».",
              "Encargo de ejercicios (Laura, 10/08/2026) e indicaciones del 04/11/2026.",
              "Enunciado de S16 (José, 28/09/2026); guía del alumno y guion del profesor.",
              "Repositorio 4-produccion-ia: API, Dockerfile, plantillas infra/s16 y costes.",
              "PowerPoint original S16-cloud-docker.pptx (24 diapositivas), conservado como fuente.",
              "QR de AI Engineer recibido el 19/10/2026, sin modificar.",
              "Logotipo de thePower: recurso original del curso."])]
    for i, (t, col, items) in enumerate(cols):
        x = 43 + i * 296
        box(sl, x, 128, 284, 340, fill=CARD)
        box(sl, x, 128, 284, 4, fill=col, radius=0)
        text(sl, x + 12, 140, 260, 12, t, size=9, color=col, bold=True)
        text(sl, x + 12, 160, 262, 304, [{"runs": [("•  ", {"color": col, "bold": True}), (it, {})], "space": 4} for it in items],
             size=9.5, color=TEXT, space=4)
    footer(sl, 51)
    notes(sl, """
DIAPOSITIVA DE CONSULTA.
Cada diapositiva incluye en sus notas las fuentes técnicas y de imágenes concretas. Iconos y logotipos se usan sin alterar proporciones ni colores; el logotipo de AWS sobre fondo claro es su versión monocroma oficial en Squid Ink (#232F3E). Los iconos de Microsoft se usan conforme a sus condiciones (diagramas, materiales de formación y documentación). Las pantallas de consola dibujadas están rotuladas como ESQUEMA y no reproducen una interfaz real; las capturas reales se identifican en su pie.""")
    return sl


PART5 = [s42_div6, s43_alojar, s44_bedrock, s45_nubes, s46_practica, s47_cierre, s48_ruta, s49_costes, s50_comandos, s51_fuentes]
