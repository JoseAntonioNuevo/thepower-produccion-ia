"""Diapositivas 1–13: apertura y bloque 1 (orientación)."""
from deck_lib import *  # noqa: F401,F403

SRC_IMG = ("Iconos: AWS Architecture Icons (paquete oficial 31/07/2026, aws.amazon.com/architecture/icons). "
           "Logotipo de AWS: a0.awsstatic.com (aws_logo_smile).")


def s01_portada(d):
    sl = d.slide(BG_SECTION, "portada")
    img(sl, "thepower-logo.png", 38, 34, h=32)
    text(sl, 43, 112, 420, 14, "S16 · AI ENGINEER", size=10, color=MINT, bold=True)
    text(sl, 43, 132, 440, 92, "Cloud deployment:\nAWS basics", size=38, font=SERIF, color=TITLE)
    text(sl, 43, 236, 420, 74,
         "Entender AWS desde su consola: dónde se aloja una API de IA, cómo se le da acceso, "
         "cómo se protegen sus claves, cómo se observa y cuánto cuesta.", size=13.5, color=TEXT)
    text(sl, 43, 336, 420, 16, "José Antonio Nuevo", size=12.5, color=TITLE, bold=True)
    text(sl, 43, 355, 430, 30, "12 y 18 de noviembre de 2026 · 18:30–20:00 · Madrid\n"
         "Misma sesión para los grupos de martes/jueves y lunes/miércoles", size=10.5, color=MUTED)
    # panel derecho con los servicios que se abrirán
    box(sl, 497, 52, 420, 410, fill=BG, line="2A5246", radius=8)
    img(sl, "aws-logo-dark.png", 515, 70, h=34)
    img(sl, "docker-logo-white.png", 786, 76, h=22)
    text(sl, 515, 116, 380, 14, "SERVICIOS QUE ABRIREMOS EN LA CONSOLA", size=9, color=MINT, bold=True)
    items = [("aws-iam.png", "IAM"), ("aws-ec2.png", "EC2"), ("aws-ebs.png", "EBS"), ("aws-s3.png", "S3"),
             ("aws-vpc.png", "VPC"), ("aws-ecr.png", "ECR"), ("aws-ecs.png", "ECS"), ("aws-fargate.png", "Fargate"),
             ("aws-secrets.png", "Secrets Manager"), ("aws-cloudwatch.png", "CloudWatch"),
             ("aws-budgets.png", "Budgets"), ("aws-bedrock.png", "Bedrock")]
    for i, (ic, lab) in enumerate(items):
        r, c = divmod(i, 4)
        x = 515 + c * 98
        y = 140 + r * 78
        img(sl, ic, x + 22, y, w=40, h=40)
        text(sl, x - 4, y + 44, 92, 24, lab, size=9.5, color=TITLE, align="c", bold=True)
    flow = ["consulta", "API en Fargate", "modelo", "respuesta"]
    ws = [70, 106, 64, 76]
    x = 515
    for i, (f, w) in enumerate(zip(flow, ws)):
        chip(sl, x, 410, w, 22, f, fill=TAKE_BG, color=MINT_L, size=9.5, line="2A5246")
        if i < len(flow) - 1:
            line(sl, x + w + 3, 421, x + w + 17, 421, color=MINT, w=1.25)
        x += w + 20
    notes(sl, """
TIEMPO 18:30–18:31 (1 min).
QUÉ EXPLICAR: título literal del temario («Cloud deployment: AWS basics»). Hoy entramos en la web y la consola de AWS para entender sus servicios desde dentro: qué es cada uno, qué problema resuelve, qué vemos en pantalla, qué configuraríamos para una API de IA, cómo se relaciona con los demás y qué determina su coste.
FORMATO: abriremos listados y formularios y cancelaremos antes del botón final. No lanzamos recursos, no activamos servicios y no ejecutamos inferencias de pago. La práctica de despliegue es opcional.
CONSOLA: tener abierta la página de inicio de la consola (región Europa · Irlanda, eu-west-1) en otra pestaña, sin pantallas de credenciales.
PREGUNTA: «¿Quién ha entrado alguna vez en la consola de AWS? ¿Qué os pareció más confuso?».
FUENTES: temario AI Engineer (Laura, 17/07/2026): «Cloud deployment: AWS basics». Misma versión para el 12/11 (M/J) y el 18/11 (L/X).
IMÁGENES: logotipo de thePower (recurso original del curso). """ + SRC_IMG + " Logotipo de Docker: Docker-Logos-1.zip de docker.com (media resources).")
    return sl


def s02_encuesta(d):
    sl = d.slide(tag="encuesta")
    header(sl, "Antes de empezar", "Encuesta de S15 y plan de la sesión",
           "Un minuto para valorar la sesión anterior de tu grupo. Después, 90 minutos para recorrer AWS "
           "desde su consola; la práctica queda como opción para después.")
    box(sl, 43, 140, 250, 326, fill=CARD, line=BORDER)
    box(sl, 70, 156, 196, 196, fill="FFFFFF", radius=6)
    img(sl, "qr-ai-engineer.jpg", 78, 164, w=180, h=180)
    text(sl, 55, 362, 226, 18, "Encuesta de la sesión anterior · S15", size=11.5, color=TITLE, bold=True, align="c")
    text(sl, 55, 382, 226, 14, "Formulario de AI Engineer", size=10, color=MUTED, align="c")
    text(sl, 55, 402, 226, 50, "Valora S15 de tu grupo (no la sesión de hoy). Escanea el código con la cámara del móvil.",
         size=10, color=TEXT, align="c")
    rows = [("18:30", "Apertura", "QR, caso conductor y mapa de la sesión", 7, MUTED),
            ("18:37", "1 · Orientación", "Consola, región, responsabilidad compartida e IAM, en vivo", 15, MINT),
            ("18:52", "2 · Cómputo y datos", "EC2, EBS y S3; Launch instance y Create bucket en vivo", 12, AMBER),
            ("19:04", "3 · Red", "VPC, rutas, internet gateway y security groups en vivo", 10, VIOLET),
            ("19:14", "4 · Contenedores", "Docker, ECR, ECS y Fargate, roles y Secrets Manager", 18, CORAL),
            ("19:32", "5 · Operar y pagar", "CloudWatch, Billing, costes, calculadora y Budgets", 13, BLUE),
            ("19:45", "6 · IA y otras nubes", "Catálogo de Bedrock en vivo y equivalencias", 7, PINK),
            ("19:52", "Cierre", "Práctica opcional, recapitulación y preguntas", 8, MUTED)]
    text(sl, 312, 140, 60, 12, "HORA", size=8.5, color=MUTED, bold=True)
    text(sl, 385, 140, 160, 12, "BLOQUE", size=8.5, color=MUTED, bold=True)
    text(sl, 552, 140, 300, 12, "QUÉ HAREMOS", size=8.5, color=MUTED, bold=True)
    text(sl, 862, 140, 55, 12, "MIN", size=8.5, color=MUTED, bold=True, align="r")
    y = 156
    for t, b, desc, m, col in rows:
        box(sl, 312, y, 605, 35, fill=CARD)
        box(sl, 312, y, 4, 35, fill=col, radius=0)
        text(sl, 324, y + 10, 56, 16, t, size=11, font=MONO, color=MINT_L, bold=True)
        text(sl, 385, y + 10, 165, 16, b, size=11.5, color=TITLE, bold=True)
        text(sl, 552, y + 4, 300, 28, desc, size=10, color=TEXT, anchor="m")
        text(sl, 862, y + 10, 45, 16, str(m), size=11.5, color=col, bold=True, align="r")
        y += 39
    takeaway(sl, "Hoy no lanzamos recursos: abrimos listados y formularios, explicamos cada campo y cancelamos antes de crear.",
             "Formato")
    footer(sl, 2)
    notes(sl, """
TIEMPO 18:31–18:33 (2 min).
QUÉ EXPLICAR: dar un minuto para escanear. La encuesta evalúa la sesión anterior de cada grupo, S15, sin una fecha fija porque esta versión se usa el 12/11 (M/J) y el 18/11 (L/X). Después, presentar la agenda: seis bloques que siguen una petición desde la cuenta hasta la factura.
FORMATO: teoría y consola a la vez. En cada servicio: diapositiva para situarlo, consola para verlo, diapositiva para fijar la idea. Preguntas durante los recorridos y siete minutos al final.
CONSOLA: aún no. Tener la consola preparada en la región eu-west-1.
PREGUNTA: «Si una API funciona en mi portátil, ¿qué puede fallar al llevarla a AWS?». Anotar respuestas (arquitectura, puertos, permisos, configuración, coste) y volver a ellas en los bloques 3–5.
FUENTES: QR de AI Engineer recibido de Laura el 19/10/2026, usado sin modificar (SHA-256 29c9041e…8c6). Destino: https://kb.tools.thepower.education/feedback/feedback-form.html?form=ai-engineer . Indicaciones de Laura del 04/11/2026: ejercicios no obligatorios, teoría junto a práctica y material manejable.""")
    return sl


def s03_caso(d):
    sl = d.slide(tag="caso")
    header(sl, "Caso conductor", "Una API de soporte que consulta un modelo",
           "La misma API nos acompaña toda la sesión. Recibe una incidencia de soporte, llama a un modelo y "
           "devuelve una clasificación y una respuesta. La usaremos para dar sentido a cada servicio.")
    box(sl, 43, 138, 420, 66, fill=CARD, line=BORDER)
    text(sl, 55, 146, 300, 12, "PETICIÓN · POST /clasificar", size=9, color=MINT, bold=True)
    text(sl, 55, 162, 400, 36, '{"texto": "Me han cobrado dos veces la factura de este mes. Es una incidencia ficticia."}',
         size=10, font=MONO, color=MINT_L, bold=True)
    line(sl, 140, 205, 140, 222, color=MINT)
    box(sl, 43, 224, 220, 74, fill=GREEN_BG, line="2A5246")
    img(sl, "docker-mark-white.png", 55, 234, h=20)
    text(sl, 88, 233, 170, 18, "Nuestra API", size=14, font=SERIF, color=TITLE)
    text(sl, 55, 258, 202, 36, "FastAPI dentro de un contenedor Docker · GET /health · POST /clasificar", size=9.5, color=TEXT)
    line(sl, 264, 261, 296, 261, color=BLUE, head="both")
    box(sl, 298, 224, 165, 74, fill=BLUE_BG, line="2C4A66")
    text(sl, 308, 233, 150, 18, "Modelo", size=14, font=SERIF, color=TITLE)
    text(sl, 308, 255, 150, 40, "Proveedor externo por HTTPS (Anthropic en la referencia de S16)", size=9.5, color=TEXT)
    line(sl, 140, 299, 140, 316, color=MINT)
    box(sl, 43, 318, 420, 148, fill=CARD, line=BORDER)
    text(sl, 55, 326, 400, 12, "RESPUESTA · forma del JSON (valores ilustrativos)", size=9, color=MINT, bold=True)
    code = ('{"resultado": {"categoria": "facturacion",\n'
            '               "prioridad": "alta | media | baja",\n'
            '               "respuesta": "…"},\n'
            ' "metadata":  {"request_id": "…", "execution": "real",\n'
            '               "version": "…", "duration_ms": …,\n'
            '               "consumo": {"input_tokens": …}}}')
    text(sl, 55, 344, 400, 100, code, size=9.5, font=MONO, color=TEXT, bold=True)
    text(sl, 55, 446, 400, 14, "La metadata la añade el servidor: el modelo no puede inventarla.", size=9, color=MUTED)
    text(sl, 487, 138, 430, 12, "QUÉ NECESITAMOS EN AWS PARA…", size=9, color=MUTED, bold=True)
    rows = [("Alojarla", "ECS + Fargate (o EC2)", "Un lugar donde corra el contenedor; con Fargate no administramos servidores.",
             ["aws-ecs.png", "aws-fargate.png"]),
            ("Darle acceso", "VPC + security group", "Una red con ruta a Internet y una regla que solo deja entrar a quien autorizamos.",
             ["aws-vpc.png"]),
            ("Proteger sus claves", "Secrets Manager + IAM", "La clave del proveedor vive fuera de la imagen; solo un rol concreto puede leerla.",
             ["aws-secrets.png", "aws-iam.png"]),
            ("Observarla", "CloudWatch", "Una línea de log por petición con request_id, estado y duración; métricas y alarmas.",
             ["aws-cloudwatch.png"]),
            ("Controlar el gasto", "Billing, Budgets y calculadora", "Estimar antes de crear, vigilar mientras existe y retirar al terminar.",
             ["aws-costexplorer.png", "aws-budgets.png"])]
    y = 154
    for verb, svc, desc, ics in rows:
        box(sl, 487, y, 430, 58, fill=CARD)
        for k, ic in enumerate(ics):
            img(sl, ic, 497 + k * 30, y + 15, w=27, h=27)
        tx = 563
        text(sl, tx, y + 7, 160, 16, verb, size=12, color=TITLE, bold=True)
        text(sl, tx + 160, y + 8, 186, 14, svc, size=9.5, color=MINT, bold=True, align="r")
        text(sl, tx, y + 25, 346, 30, desc, size=10, color=TEXT)
        y += 63
    takeaway(sl, "El problema de IA ya lo conocemos de S7/S8. Hoy cambia dónde se ejecuta, quién puede usarlo y cuánto cuesta mantenerlo.",
             "Idea guía")
    footer(sl, 3)
    notes(sl, """
TIEMPO 18:33–18:35 (2 min).
QUÉ EXPLICAR: caso conductor de toda la sesión: «Tenemos una pequeña API de IA que recibe una consulta de soporte, llama a un modelo y devuelve una clasificación y una respuesta. Queremos entender qué piezas de AWS necesitaríamos para alojarla, permitir el acceso, proteger sus claves, observar su funcionamiento y controlar el gasto». Es la API ya preparada de S16 (S16-inicio.zip): GET /health comprueba el proceso sin llamar al modelo; POST /clasificar valida la entrada, llama al proveedor y valida la salida. No desarrollamos código hoy.
CÓDIGO (opcional, 30 s): enseñar datos/peticion.json y src/curso_ia/contratos.py: categorías acceso, facturacion, tecnico, consulta; prioridades alta, media, baja.
CONSOLA: ninguna todavía.
PREGUNTA: «¿Dónde está el modelo en este dibujo? ¿Dentro de nuestro contenedor?». Respuesta: no; el contenedor solo tiene la aplicación que lo llama por HTTPS.
FUENTES: material/S16 (README, guion, guía del alumno) y src/curso_ia del repositorio 4-produccion-ia. La forma del JSON procede de api.py y contratos.py; los valores son ilustrativos, no una ejecución real.
IMÁGENES: iconos oficiales de AWS Architecture Icons (31/07/2026); Docker logo oficial (docker.com).""")
    return sl


def s04_mapa(d):
    sl = d.slide(tag="mapa")
    header(sl, "El mapa de la sesión", "Las piezas de AWS alrededor de nuestra API",
           "Cada bloque explica una parte de este diagrama. Al final podremos seguir una petición de izquierda a derecha "
           "y nombrar el servicio que interviene en cada paso.")
    # actores externos
    img(sl, "g-user.png", 64, 196, w=40, h=40)
    text(sl, 43, 240, 90, 30, "Profesor\n203.0.113.10/32", size=9, color=TEXT, align="c")
    box(sl, 43, 352, 92, 92, fill=BLUE_BG, line="2C4A66")
    img(sl, "g-generic-application.png", 76, 360, w=26, h=26)
    text(sl, 47, 390, 84, 50, "Proveedor del modelo\n(Anthropic hoy; Bedrock en S17)", size=8.5, color=TEXT, align="c")
    badge(sl, 125, 344, 6, fill=PINK)
    # nube
    box(sl, 140, 132, 604, 334, fill=None, line="AAB7BD", lw=0.75, radius=0)
    img(sl, "grp-cloud.png", 140, 132, w=20, h=20)
    text(sl, 165, 136, 300, 12, "AWS Cloud · cuenta del laboratorio", size=9, color=TITLE, bold=True)
    img(sl, "aws-iam.png", 168, 180, w=32, h=32)
    text(sl, 148, 215, 72, 30, "IAM · roles\n(global)", size=8.5, color=TEXT, align="c")
    badge(sl, 204, 172, 1, fill=MINT)
    img(sl, "aws-budgets.png", 168, 330, w=32, h=32)
    text(sl, 148, 365, 72, 30, "Billing y\nBudgets (global)", size=8.5, color=TEXT, align="c")
    badge(sl, 204, 322, 5, fill=BLUE)
    # región
    box(sl, 232, 156, 500, 300, fill=None, line="00A4A6", lw=1, radius=0, dash=True)
    img(sl, "grp-region.png", 232, 156, w=18, h=18)
    text(sl, 255, 159, 300, 12, "Región eu-west-1 · Europa (Irlanda)", size=9, color="5FD0D2", bold=True)
    # VPC
    box(sl, 262, 182, 290, 264, fill=None, line="8C4FFF", lw=1, radius=0)
    img(sl, "grp-vpc.png", 262, 182, w=18, h=18)
    text(sl, 285, 185, 200, 12, "VPC 10.216.0.0/24", size=9, color=VIOLET, bold=True)
    badge(sl, 530, 186, 3, fill=VIOLET)
    # subred pública
    box(sl, 290, 208, 250, 228, fill="132620", line="7AA116", lw=1, radius=0)
    img(sl, "grp-public.png", 290, 208, w=16, h=16)
    text(sl, 311, 210, 220, 12, "Subred pública 10.216.0.0/25", size=8.5, color="A6D05A", bold=True)
    # IGW
    img(sl, "r-igw.png", 246, 286, w=32, h=32)
    text(sl, 232, 320, 60, 22, "Internet\ngateway", size=8, color=TEXT, align="c")
    # security group
    box(sl, 308, 236, 216, 186, fill=None, line="DD344C", lw=1, radius=0, dash=True)
    text(sl, 316, 240, 204, 24, "Security group · entra TCP 8000 desde /32 · sale TCP 443", size=8.5, color=CORAL, bold=True)
    box(sl, 322, 274, 188, 132, fill=CARD, line=BORDER)
    img(sl, "aws-fargate.png", 334, 286, w=36, h=36)
    img(sl, "docker-mark-white.png", 378, 294, h=18)
    text(sl, 334, 328, 170, 16, "Tarea ECS en Fargate", size=11, color=TITLE, bold=True)
    text(sl, 334, 346, 170, 52, "Contenedor «api» escuchando en :8000. Su interfaz de red (ENI) tiene IP privada y pública.",
         size=9, color=TEXT)
    badge(sl, 490, 280, 4, fill=CORAL)
    # servicios regionales a la derecha
    sv = [("aws-ecr.png", "ECR", "imagen @sha256", 196, CORAL, 4),
          ("aws-secrets.png", "Secrets Manager", "clave del proveedor", 282, CORAL, 4),
          ("aws-cloudwatch.png", "CloudWatch", "logs y métricas", 368, BLUE, 5)]
    for ic, nm, sub, y, col, n in sv:
        img(sl, ic, 572, y, w=34, h=34)
        text(sl, 612, y + 2, 116, 14, nm, size=10, color=TITLE, bold=True)
        text(sl, 612, y + 17, 116, 14, sub, size=9, color=MUTED)
        badge(sl, 708, y - 6, n, fill=col)
    # flechas
    line(sl, 106, 222, 246, 296, color=MINT, w=1.5)
    text(sl, 116, 266, 110, 22, "petición :8000", size=8.5, color=MINT, bold=True, check=False)
    line(sl, 278, 302, 322, 322, color=MINT, w=1.5)
    line(sl, 322, 372, 278, 316, color=BLUE, w=1.25, dash=True)
    line(sl, 252, 318, 135, 380, color=BLUE, w=1.25, dash=True)
    text(sl, 150, 412, 90, 24, "HTTPS 443\nal modelo", size=8.5, color=BLUE, bold=True, check=False)
    line(sl, 572, 214, 511, 292, color=CORAL, w=1.1, dash=True)
    line(sl, 572, 300, 511, 330, color=CORAL, w=1.1, dash=True)
    line(sl, 511, 380, 572, 386, color=BLUE, w=1.1, dash=True)
    # leyenda
    lx = 756
    text(sl, lx, 134, 161, 12, "DÓNDE LO EXPLICAMOS", size=9, color=MUTED, bold=True)
    leg = [(1, MINT, "Cuenta, región, ARN e IAM"), (2, AMBER, "EC2 + EBS como alternativa; S3 si guardáramos adjuntos"),
           (3, VIOLET, "VPC, subred, ruta, gateway y security group"), (4, CORAL, "Docker, ECR, ECS, Fargate y secretos"),
           (5, BLUE, "CloudWatch, Billing y Budgets"), (6, PINK, "Bedrock frente a un proveedor externo")]
    y = 152
    for n, col, t in leg:
        badge(sl, lx, y, n, fill=col)
        text(sl, lx + 22, y, 140, 40, t, size=9.5, color=TEXT)
        y += 50
    takeaway(sl, "Alojar, conectar, proteger, observar y pagar: cada servicio de hoy responde a una de esas cinco necesidades.",
             "Idea guía")
    footer(sl, 4)
    notes(sl, """
TIEMPO 18:35–18:36 (1 min).
QUÉ EXPLICAR: mapa completo antes de entrar en detalle. Recorrer las flechas: ① la petición entra por el internet gateway, pasa el security group y llega a la tarea; la tarea descarga su imagen de ECR y recibe el secreto al arrancar (líneas coral discontinuas); escribe logs en CloudWatch; y sale por HTTPS hacia el proveedor del modelo. IAM y Billing son globales: no dependen de la región. Los números indican el bloque donde explicamos cada pieza.
ADVERTENCIA: el diagrama es una arquitectura de laboratorio (una tarea, una subred, IP pública temporal y acceso restringido a una /32). No es una arquitectura de producción ni tiene alta disponibilidad. EC2 y S3 no aparecen dentro porque nuestra API no los necesita: los veremos como alternativa (EC2+EBS) y como almacenamiento si existieran adjuntos (S3).
CONSOLA: ninguna. Volveremos a esta diapositiva al final del bloque 4.
PREGUNTA: «¿Qué flecha falla si el contenedor arranca pero nadie puede entrar desde el portátil?».
FUENTES: plantillas infra/s16/registro.json y servicio.json (VPC 10.216.0.0/24, subred /25, entrada TCP 8000 desde /32, salida TCP 443, logs /thepower/<lab>, Fargate X86_64). 203.0.113.10 pertenece al rango de documentación TEST-NET-3: es un ejemplo.
IMÁGENES: iconos de grupo, servicio y recurso de AWS Architecture Icons (31/07/2026); icono de Docker de docker.com.""")
    return sl


def s05_metodo(d):
    sl = d.slide(tag="metodo")
    header(sl, "Método", "Seis preguntas para leer cualquier servicio",
           "Usaremos la misma lente en cada pantalla de AWS. Así la consola no se convierte en un catálogo de botones: "
           "cada servicio queda conectado con nuestra API.")
    qs = [("¿Qué es?", "El servicio en una frase y el tipo de recurso que crea dentro de la cuenta."),
          ("¿Qué problema resuelve?", "Qué necesidad de nuestra API cubre y qué ocurriría si no existiera."),
          ("¿Qué vemos en pantalla?", "Listados, pestañas y campos del formulario que vamos a señalar."),
          ("¿Qué configuraríamos?", "Los valores concretos que usaría nuestra API de soporte."),
          ("¿Con qué se relaciona?", "Servicios de los que depende y servicios que dependen de él."),
          ("¿Qué determina su coste?", "Tiempo encendido, capacidad, almacenamiento, tráfico o número de peticiones.")]
    cols = [MINT, BLUE, VIOLET, AMBER, PINK, CORAL]
    for i, (q, a) in enumerate(qs):
        r, c = divmod(i, 3)
        x = 43 + c * 196
        y = 140 + r * 166
        box(sl, x, y, 186, 156, fill=CARD)
        badge(sl, x + 12, y + 12, i + 1, fill=cols[i], d=22, size=11)
        text(sl, x + 12, y + 44, 162, 40, q, size=14, font=SERIF, color=TITLE)
        text(sl, x + 12, y + 88, 162, 62, a, size=10.5, color=TEXT)
    box(sl, 637, 140, 280, 322, fill=CARD, line=BORDER)
    text(sl, 651, 152, 250, 12, "REGLAS DEL RECORRIDO EN DIRECTO", size=9, color=MINT, bold=True)
    rules = [("✓", MINT, "Comprobar región y cuenta antes de interpretar un listado."),
             ("✓", MINT, "Abrir formularios y cancelar antes del botón final (Launch, Create)."),
             ("✕", CORAL, "No lanzar recursos, activar servicios ni ejecutar inferencias de pago."),
             ("✕", CORAL, "No mostrar el valor de un secreto ni pantallas de credenciales."),
             ("✓", MINT, "Si la cuenta está vacía, el listado vacío también enseña: columnas, filtros y el botón que crearía el recurso.")]
    y = 174
    for sym, col, t in rules:
        circle(sl, 651, y + 1, 18, TAKE_BG if col == MINT else CORAL_BG)
        text(sl, 651, y + 2, 18, 16, sym, size=10, color=col, bold=True, align="c", check=False)
        text(sl, 677, y, 228, 52, t, size=10.5, color=TEXT)
        y += 56
    takeaway(sl, "Una pantalla vacía no es un fallo de la demo: enseña qué recurso crearíamos y qué datos nos pediría AWS.",
             "Idea guía")
    footer(sl, 5)
    notes(sl, """
TIEMPO 18:36–18:37 (1 min).
QUÉ EXPLICAR: la lente de seis preguntas que repetiremos en cada servicio (qué es, qué problema resuelve, qué vemos, qué configuraríamos, con qué se relaciona, qué determina su coste). Pedir a los alumnos que la usen para tomar notas.
REGLAS: comprobar región y cuenta; abrir formularios y cancelar; no crear recursos, no activar servicios y no invocar modelos de pago; no mostrar valores de secretos.
SI LA CUENTA ESTÁ VACÍA: es lo esperado en una cuenta de laboratorio. Enseñar el listado vacío (columnas, filtros, botón «Create…»), abrir el formulario y explicar sus campos. Existen recursos por defecto que sirven de ejemplo sin crear nada: la VPC por defecto de cada región y, normalmente, roles vinculados a servicios en IAM.
CONSOLA: ninguna.
PREGUNTA: «¿Cuál de las seis preguntas os parece más difícil de responder mirando solo la consola?» (suele ser el coste: lo resolveremos en el bloque 5).
FUENTES: indicaciones docentes del encargo para S16 (recorrido por la consola sin crear recursos).""")
    return sl


def s06_div1(d):
    sl = divider(d, 1, "Orientación", "Orientarse en AWS: cuenta, región e identidad",
                 "Dónde estamos, qué estamos viendo y quién puede hacer cada cosa.",
                 ["¿Qué contratamos al usar un proveedor cloud?",
                  "¿Cómo se lee la consola: buscador, región y cuenta?",
                  "¿Qué diferencia hay entre un servicio y un recurso?",
                  "¿Qué es regional, qué es global y qué nos toca proteger?",
                  "¿Cómo decide IAM si una acción está permitida?"],
                 [("aws-console.png", "Consola de\nAWS"), ("grp-region.png", "Regiones y\nzonas"),
                  ("aws-iam.png", "IAM"), ("grp-account.png", "Cuenta")], "18:37–18:50")
    notes(sl, """
TIEMPO 18:37 (10 s). Bloque 1 de 6: Orientación, de 18:37 a 18:50 (13 min).
QUÉ EXPLICAR: antes de abrir servicios necesitamos tres coordenadas: cuenta, región e identidad. Leer las cinco preguntas del bloque.
CONSOLA: tener abierta la página de inicio de la consola.
IMÁGENES: AWS Architecture Icons (31/07/2026): AWS Management Console, IAM, iconos de grupo Region y AWS Account.""")
    return sl


def s07_proveedores(d):
    sl = d.slide(tag="proveedores")
    header(sl, "Proveedores cloud", "Qué contratamos cuando usamos una nube",
           "Un proveedor cloud nos deja crear capacidad mediante una consola o una API: cómputo, almacenamiento, red, "
           "identidad y servicios gestionados. Pagamos por uso y elegimos dónde se ejecuta cada recurso.")
    provs = [("aws-logo-light.png", 34, "Amazon Web Services",
              "Organización › Unidad organizativa › Cuenta › Recursos",
              "La cuenta separa permisos, recursos y factura. Es la frontera del laboratorio."),
             ("az-logo.png", 36, "Microsoft Azure",
              "Tenant de Entra ID › Grupo de administración › Suscripción › Grupo de recursos",
              "El grupo de recursos reúne lo que se crea y se borra junto."),
             ("gc-logo.png", 26, "Google Cloud",
              "Organización › Carpeta › Proyecto › Recursos",
              "El proyecto agrupa recursos, APIs activadas, permisos y facturación.")]
    for i, (lg, lh, nm, hier, note) in enumerate(provs):
        x = 43 + i * 296
        box(sl, x, 140, 284, 178, fill=CARD)
        box(sl, x + 10, 150, 264, 50, fill="FFFFFF", radius=6)
        w, h = img_size(lg, h=lh)
        img(sl, lg, x + 10 + (264 - w) / 2, 150 + (50 - h) / 2, h=lh)
        text(sl, x + 12, 210, 260, 18, nm, size=14, font=SERIF, color=TITLE)
        text(sl, x + 12, 232, 260, 12, "ORGANIZACIÓN Y FACTURACIÓN", size=8, color=MINT, bold=True)
        text(sl, x + 12, 246, 260, 30, hier, size=10, color=MINT_L, bold=True)
        text(sl, x + 12, 280, 260, 34, note, size=10, color=TEXT)
    text(sl, 43, 330, 600, 12, "LO QUE CONTRATAMOS EN CUALQUIERA DE ELLAS", size=9, color=MUTED, bold=True)
    tiles = [("g-server.png", "Cómputo", "Máquinas virtuales, contenedores y funciones.", AMBER),
             ("g-disk.png", "Almacenamiento", "Discos, objetos, bases de datos y copias.", BLUE),
             ("g-internet.png", "Red", "Redes privadas, IP, rutas, DNS y cortafuegos.", VIOLET),
             ("g-credentials.png", "Identidad", "Usuarios, roles y políticas de acceso.", CORAL),
             ("g-gear.png", "Servicios gestionados", "Bases de datos, colas, IA… que opera el proveedor.", PINK)]
    for i, (ic, t, b, col) in enumerate(tiles):
        x = 43 + i * 177
        box(sl, x, 348, 167, 116, fill=CARD)
        box(sl, x, 348, 167, 4, fill=col, radius=0)
        img(sl, ic, x + 12, 362, w=26, h=26)
        text(sl, x + 46, 367, 115, 30, t, size=11.5, color=TITLE, bold=True)
        text(sl, x + 12, 398, 145, 60, b, size=10.5, color=TEXT)
    takeaway(sl, "Una nube no elimina la administración: seguimos eligiendo capacidad, ubicación, permisos y retirada, y todo tiene coste.",
             "Idea guía")
    footer(sl, 7, 1)
    notes(sl, """
TIEMPO 18:37–18:39 (2 min).
QUÉ EXPLICAR: «cloud» significa consumir recursos administrados por un proveedor bajo demanda. Las tres grandes nubes ofrecen las mismas familias (cómputo, almacenamiento, red, identidad y servicios gestionados), pero organizan cuentas y facturación de forma distinta: AWS con cuentas agrupadas en AWS Organizations; Azure con un tenant de Microsoft Entra ID, grupos de administración, suscripciones y grupos de recursos; Google Cloud con organización, carpetas y proyectos. Hoy trabajamos con AWS; en el bloque 6 veremos los nombres equivalentes.
CONSOLA: página de inicio de la consola de AWS. Señalar que todo lo que veamos pertenece a una cuenta concreta.
PREGUNTA: «Si mi empresa ya tiene su identidad y sus datos en Azure, ¿tiene sentido desplegar esta API en AWS?». Respuesta: depende de datos, identidad, región, modelos, operación y coste total; no del número de servicios.
FUENTES: Microsoft Learn, «Azure for AWS professionals» (learn.microsoft.com/azure/architecture/aws-professional/); Google Cloud, «Compare AWS and Azure services to Google Cloud» (docs.cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison).
IMÁGENES: logotipo de AWS (a0.awsstatic.com, versión monocroma Squid Ink sobre fondo claro); icono «Azure A» de Azure Public Service Icons V25 (Microsoft, uso permitido en materiales de formación); logotipo de Google Cloud (www.gstatic.com/cgc/google-cloud-logo-fullcolor.svg); iconos genéricos de AWS Architecture Icons.""")
    return sl


def s08_consola(d):
    sl = d.slide(tag="consola")
    header(sl, "La consola de AWS", "Dónde estamos: servicio, región y cuenta",
           "La barra superior se mantiene en todos los servicios. Antes de interpretar una pantalla comprobamos tres datos: "
           "en qué servicio estamos, qué región está seleccionada y con qué identidad hemos entrado.")
    esquema_label(sl, 767, 128)
    box(sl, 43, 146, 874, 40, fill=UI_NAV, radius=4)
    img(sl, "aws-logo-dark.png", 54, 153, h=24)
    text(sl, 104, 154, 20, 22, "▦", size=15, color="FFFFFF", check=False)
    box(sl, 132, 155, 360, 22, fill="FFFFFF", radius=4)
    text(sl, 142, 159, 340, 14, "Search   [buscar servicios, funciones, recursos y documentación]", size=9.5, color=UI_MUTED, check=False)
    img(sl, "aws-cloudshell.png", 566, 156, w=20, h=20)
    img(sl, "g-gear.png", 604, 157, w=18, h=18)
    text(sl, 672, 159, 110, 14, "Europe (Ireland)  ▾", size=10, color="FFFFFF", bold=True, check=False)
    text(sl, 790, 159, 122, 14, "rol-profesor  ▾", size=10, color="FFFFFF", bold=True, check=False)
    marks = [(1, 106), (2, 300), (3, 568), (4, 715), (5, 832)]
    for n, x in marks:
        line(sl, x + 8, 187, x + 8, 200, color=AMBER, w=1, head="none")
        badge(sl, x, 200, n, fill=AMBER)
    cards = [("Menú de servicios", "Catálogo por categorías, favoritos y servicios visitados recientemente."),
             ("Buscador", "Escribir «ECS», «bucket» o «budgets» lleva al servicio, a sus funciones y a la documentación."),
             ("CloudShell", "Terminal en el navegador con las credenciales de la sesión. Hoy no lo usamos."),
             ("Región", "Cambia lo que vemos en los servicios regionales. En IAM o Billing indica «Global»."),
             ("Cuenta e identidad", "Usuario o rol con el que hemos entrado, ID de la cuenta y acceso a Billing.")]
    for i, (t, b) in enumerate(cards):
        x = 43 + i * 177
        box(sl, x, 224, 167, 118, fill=CARD)
        badge(sl, x + 10, 234, i + 1, fill=AMBER)
        text(sl, x + 32, 234, 130, 16, t, size=12, color=TITLE, bold=True)
        text(sl, x + 10, 258, 148, 80, b, size=10.5, color=TEXT)
    text(sl, 43, 354, 500, 12, "RECORRIDO QUE HAREMOS EN CADA SERVICIO", size=9, color=MUTED, bold=True)
    steps = ["Buscar el servicio", "Comprobar región", "Abrir el listado", "Abrir un recurso o formulario", "Cancel"]
    ws = [142, 142, 130, 210, 84]
    x = 43
    for i, (s, w) in enumerate(zip(steps, ws)):
        chip(sl, x, 372, w, 26, s, fill=TAKE_BG if i < 4 else CORAL_BG, color=MINT_L if i < 4 else CORAL, size=10.5, line="2A5246" if i < 4 else None)
        if i < len(steps) - 1:
            line(sl, x + w + 3, 385, x + w + 21, 385, color=MINT, w=1.25)
        x += w + 26
    text(sl, 43, 410, 874, 54,
         [[("Cuenta vacía: ", {"bold": True, "color": AMBER}),
           ("los listados muestran que no hay recursos y ofrecen el botón «Create…». Basta para explicar columnas, filtros y "
            "las opciones del formulario. Los servicios regionales muestran solo lo que existe en la región seleccionada.", {})]],
         size=10.5, color=TEXT)
    takeaway(sl, "Si un recurso «ha desaparecido», mira primero la región y la cuenta: la mayoría de los listados son regionales.",
             "Idea guía")
    footer(sl, 8, 1)
    notes(sl, """
TIEMPO 18:39–18:41 (2 min). Primer paso en la consola.
QUÉ EXPLICAR: la barra superior es común a todos los servicios. (1) Menú de servicios por categorías y recientes; (2) buscador unificado para servicios, funciones, recursos y documentación; (3) CloudShell, una terminal con las credenciales de la sesión (no la abrimos); (4) selector de región; (5) menú de cuenta con la identidad, el ID de cuenta y el acceso a Billing and Cost Management.
CONSOLA: página de inicio → escribir «ECS» en el buscador → abrir Amazon ECS → cambiar la región a otra y volver a Europa (Irlanda) para ver cómo cambia el listado → abrir IAM y mostrar que el selector indica «Global».
SEÑALAR: nombre de la región (eu-west-1), menú de la cuenta (sin mostrar correos ni credenciales), widgets de la página de inicio.
SI LA CUENTA ESTÁ VACÍA: mostrar el mensaje de listado vacío y el botón de creación; abrirlo y cancelar.
PREGUNTA: «He creado algo y no lo veo. ¿Qué dos cosas compruebo primero?». Respuesta: región y cuenta/identidad.
AVISO: la barra es un ESQUEMA para orientar (no es una captura). La consola real cambia de diseño con el tiempo; los elementos descritos se mantienen.
FUENTES: AWS Management Console Getting Started Guide (docs.aws.amazon.com/awsconsolehelpdocs/).
IMÁGENES: esquema propio; logotipo de AWS (a0.awsstatic.com); iconos de CloudShell y genéricos de AWS Architecture Icons.""")
    return sl


def s09_arn(d):
    sl = d.slide(tag="arn")
    header(sl, "Servicio y recurso", "Un servicio crea recursos; un ARN los identifica",
           "EC2, S3 o ECS son servicios. Una instancia, un bucket o una definición de tarea son recursos concretos de nuestra "
           "cuenta, con nombre, región, permisos y coste propios.")
    pairs = [("aws-ec2.png", "Amazon EC2", "r-ec2-instance.png", "i-0a1b2c3d4e5f67890", "una instancia concreta"),
             ("aws-s3.png", "Amazon S3", "r-s3-bucket.png", "thepower-s16-soporte-ejemplo", "un bucket con sus objetos"),
             ("aws-ecs.png", "Amazon ECS", "r-ecs-task.png", "task-definition/s16-lab:3", "una definición de tarea, revisión 3"),
             ("aws-secrets.png", "Secrets Manager", "g-credentials.png", "s16-lab/anthropic", "un secreto (solo su nombre)")]
    for i, (si, sn, ri, rn, cap) in enumerate(pairs):
        r, c = divmod(i, 2)
        x = 43 + c * 443
        y = 138 + r * 92
        box(sl, x, y, 431, 84, fill=CARD)
        img(sl, si, x + 12, y + 14, w=36, h=36)
        text(sl, x + 12, y + 56, 110, 20, sn, size=10, color=TITLE, bold=True)
        text(sl, x + 128, y + 6, 70, 12, "SERVICIO", size=8, color=FAINT, bold=True, check=False)
        line(sl, x + 128, y + 34, x + 176, y + 34, color=MINT, w=1.5)
        img(sl, ri, x + 186, y + 16, w=32, h=32)
        text(sl, x + 228, y + 6, 70, 12, "RECURSO", size=8, color=FAINT, bold=True, check=False)
        text(sl, x + 228, y + 22, 196, 30, rn, size=10, font=MONO, color=MINT_L, bold=True)
        text(sl, x + 228, y + 56, 196, 20, cap, size=10, color=TEXT)
    box(sl, 43, 326, 874, 140, fill=CARD, line=BORDER)
    text(sl, 57, 336, 400, 12, "ANATOMÍA DE UN ARN (AMAZON RESOURCE NAME)", size=9, color=MINT, bold=True)
    segs = [("arn", "prefijo", MUTED), ("aws", "partición", BLUE), ("ecs", "servicio", CORAL), ("eu-west-1", "región", MINT),
            ("111122223333", "cuenta (ejemplo de la documentación)", AMBER), ("task-definition/s16-lab:3", "recurso: tipo / nombre : revisión", VIOLET)]
    x = 57
    for i, (s, lab, col) in enumerate(segs):
        w = len(s) * 7.6 + 16
        chip(sl, x, 358, w, 26, s, fill=CARD2, color=col, size=12.5, font=MONO, radius=4, line=col)
        text(sl, x, 388, max(w, 70) + (30 if i == 4 else 0), 30, lab, size=9, color=col, bold=True)
        x += w
        if i < len(segs) - 1:
            text(sl, x + 1, 360, 10, 20, ":", size=13, font=MONO, color=TITLE, check=False)
            x += 12
    text(sl, 640, 340, 265, 120,
         [[("Excepción útil: ", {"bold": True, "color": AMBER}),
           ("el ARN de un bucket es ", {}), ("arn:aws:s3:::thepower-s16-soporte-ejemplo", {"font": MONO, "color": MINT_L}),
           (". No lleva región ni cuenta porque el nombre ya identifica el bucket.", {})]], size=10.5, color=TEXT)
    text(sl, 57, 428, 560, 30, "Los ARN aparecen en las políticas de IAM, en la referencia de un secreto desde ECS y en el detalle de la factura.",
         size=10.5, color=TEXT)
    takeaway(sl, "Leer un ARN evita confundir cuentas, regiones o entornos: dice qué servicio, dónde y de quién es el recurso.",
             "Idea guía")
    footer(sl, 9, 1)
    notes(sl, """
TIEMPO 18:41–18:43 (2 min).
QUÉ EXPLICAR: un servicio (EC2, S3, ECS, Secrets Manager) es la capacidad que ofrece AWS; un recurso es lo que creamos con él dentro de nuestra cuenta (una instancia, un bucket, una definición de tarea, un secreto). Cada recurso tiene identificador, región (si es regional), permisos y coste. El ARN lo identifica de forma única: arn:partición:servicio:región:cuenta:recurso. Excepción: el bucket de S3 no incluye región ni cuenta en su ARN.
CONSOLA: abrir cualquier recurso existente o, en una cuenta vacía, IAM › Roles › un rol vinculado a servicio y copiar su ARN (los ARN de IAM no llevan región). Comparar con el ARN de ejemplo de la diapositiva.
SEÑALAR: el campo «ARN» en la página de detalle de un recurso.
PREGUNTA: «¿Por qué el ARN de IAM no lleva región?». Respuesta: IAM es un servicio global.
FUENTES: AWS IAM User Guide, «IAM identifiers» y «Amazon Resource Names (ARNs)» (docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html). 111122223333 es el ID de cuenta de ejemplo que usa la documentación de AWS. Los nombres de recursos son ficticios.
IMÁGENES: AWS Architecture Icons (31/07/2026): iconos de servicio y de recurso (EC2 Instance, S3 Bucket with objects, ECS Task) y genérico Credentials.""")
    return sl


def s10_regiones(d):
    sl = d.slide(tag="regiones")
    header(sl, "Regiones y zonas", "Región, zona de disponibilidad y alcance global",
           "Una región es una ubicación geográfica con varias zonas de disponibilidad aisladas entre sí. La región condiciona "
           "la latencia, los servicios y modelos disponibles, las tarifas y dónde quedan los datos.")
    box(sl, 43, 140, 470, 326, fill=None, line="00A4A6", lw=1, radius=0, dash=True)
    img(sl, "grp-region.png", 43, 140, w=20, h=20)
    text(sl, 70, 144, 400, 14, "Región eu-west-1 · Europa (Irlanda)", size=10.5, color="5FD0D2", bold=True)
    for i, z in enumerate(["a", "b", "c"]):
        x = 60 + i * 150
        box(sl, x, 172, 136, 172, fill=CARD, line=BORDER)
        text(sl, x + 10, 180, 116, 12, "ZONA DE DISPONIBILIDAD", size=7.5, color=MUTED, bold=True)
        text(sl, x + 10, 194, 116, 16, f"eu-west-1{z}", size=12, font=MONO, color=TITLE, bold=True)
        img(sl, "g-server.png", x + 22, 222, w=34, h=34)
        img(sl, "g-server.png", x + 74, 222, w=34, h=34)
        text(sl, x + 10, 266, 116, 70, "Uno o más centros de datos con energía, refrigeración y red independientes.", size=9.5, color=TEXT)
    line(sl, 196, 300, 210, 300, color=MUTED, w=1, head="both")
    line(sl, 346, 300, 360, 300, color=MUTED, w=1, head="both")
    chip(sl, 60, 352, 286, 24, "Nuestro laboratorio: una subred en una sola zona", fill=TAKE_BG, color=MINT_L, size=10, line="2A5246")
    text(sl, 60, 384, 440, 76,
         "Repartir réplicas entre zonas da disponibilidad; una tarea única no. Las letras a, b y c se asignan por cuenta: "
         "el ID de zona (por ejemplo euw1-az1) identifica la zona física.", size=10, color=TEXT)
    groups = [("REGIONALES · cambian con el selector", MINT, TAKE_BG,
               [("aws-ec2.png", "EC2 y EBS"), ("aws-vpc.png", "VPC"), ("aws-ecs.png", "ECS y Fargate"), ("aws-ecr.png", "ECR"),
                ("aws-secrets.png", "Secrets Manager"), ("aws-cloudwatch.png", "CloudWatch"), ("aws-bedrock.png", "Bedrock")]),
              ("GLOBALES · la consola indica «Global»", AMBER, AMBER_BG,
               [("aws-iam.png", "IAM"), ("aws-costexplorer.png", "Billing and Cost Management")])]
    y = 140
    for title, col, bg, items in groups:
        hgt = 36 + ((len(items) + 1) // 2) * 30
        box(sl, 530, y, 387, hgt, fill=CARD)
        text(sl, 542, y + 10, 360, 12, title, size=9, color=col, bold=True)
        for k, (ic, lab) in enumerate(items):
            r, c = divmod(k, 2)
            xx = 542 + c * 186
            yy = y + 30 + r * 30
            img(sl, ic, xx, yy, w=22, h=22)
            text(sl, xx + 28, yy + 4, 158, 16, lab, size=10, color=TITLE, bold=True)
        y += hgt + 8
    box(sl, 530, y, 387, 466 - y, fill=BLUE_BG)
    img(sl, "aws-s3.png", 542, y + 10, w=22, h=22)
    text(sl, 572, y + 10, 330, 14, "CASO ESPECIAL · S3", size=9, color=BLUE, bold=True)
    text(sl, 542, y + 36, 364, 466 - y - 40,
         "La consola lista todos los buckets de la cuenta, pero cada bucket vive en la región elegida al crearlo y sus objetos "
         "no salen de ella salvo que los copiemos.", size=10, color=TEXT)
    takeaway(sl, "Elegimos región por usuarios, datos, servicios, modelos y precio. Cambiarla después implica recrear recursos.",
             "Idea guía")
    footer(sl, 10, 1)
    notes(sl, """
TIEMPO 18:43–18:45 (2 min).
QUÉ EXPLICAR: una región agrupa varias zonas de disponibilidad (AZ), cada una con uno o más centros de datos aislados (energía, refrigeración, red) y conectados entre sí con baja latencia. AWS indica que cada región tiene como mínimo tres AZ. Repartir una aplicación entre zonas mejora la disponibilidad; nuestro laboratorio usa una sola subred y una sola tarea, así que no la tiene. Los nombres eu-west-1a/b/c se asignan por cuenta; el ID de zona (euw1-az1…) identifica la zona física.
REGIONAL frente a GLOBAL: EC2, EBS, VPC, ECS/Fargate, ECR, Secrets Manager, CloudWatch y Bedrock son regionales; IAM y Billing and Cost Management son globales. S3 es un caso especial: listado global, buckets regionales.
CONSOLA: selector de región → desplegar la lista. EC2 › Dashboard muestra las zonas de la región (Service health / Zones). Abrir IAM para ver «Global».
PREGUNTA: «¿Por qué no aparece en Irlanda un modelo de Bedrock que he visto en un tutorial?». Respuesta: la disponibilidad de modelos es por región.
FUENTES: AWS, «Regiones y zonas de disponibilidad» (aws.amazon.com/es/about-aws/global-infrastructure/regions_az/); AWS Whitepaper «AWS Fault Isolation Boundaries»; EC2 User Guide, «Availability Zones» (IDs de zona).
IMÁGENES: esquema propio con iconos de AWS Architecture Icons (grupo Region, genérico Server e iconos de servicio).""")
    return sl


def s11_responsabilidad(d):
    sl = d.slide(tag="srm")
    header(sl, "Responsabilidad compartida", "Qué protege AWS y qué seguimos protegiendo nosotros",
           "AWS responde de la seguridad «de» la nube; el cliente responde de la seguridad «en» la nube. "
           "El reparto cambia según el servicio que elegimos.")
    box(sl, 43, 138, 444, 270, fill="FFFFFF", radius=4)
    img(sl, "shot-srm.png", 49, 144, w=432)
    text(sl, 43, 414, 444, 50,
         "Imagen oficial de AWS (en inglés). CUSTOMER: cliente, seguridad «en» la nube. AWS: seguridad «de» la nube, "
         "desde el hardware hasta las regiones, zonas y ubicaciones de borde.", size=9.5, color=MUTED)
    cx = 503
    colw = 136
    heads = [("aws-ec2.png", "EC2"), ("aws-fargate.png", "ECS en Fargate"), ("aws-bedrock.png", "Bedrock")]
    for i, (ic, t) in enumerate(heads):
        x = cx + 4 + i * (colw + 4) - 4
        img(sl, ic, x + 4, 140, w=24, h=24)
        text(sl, x + 34, 145, colw - 34, 16, t, size=10.5, color=TITLE, bold=True)
    rows = [("AWS GESTIONA", "D9822B", AMBER_BG,
             ["Hardware, red física y virtualización.",
              "Además, el host, su sistema operativo y el agente de contenedores.",
              "La infraestructura y la ejecución del modelo."]),
            ("GESTIONAMOS NOSOTROS", BLUE, BLUE_BG,
             ["Sistema operativo y parches, Docker, aplicación, security groups, IAM, datos y claves.",
              "Imagen y dependencias, definición de tarea, roles, red y security groups, secretos y datos.",
              "Permisos IAM, datos que enviamos, prompts, cuotas, coste y validación de respuestas."])]
    y = 172
    for lab, col, bg, cells in rows:
        h = 92 if lab.startswith("AWS") else 132
        text(sl, cx, y, 300, 12, lab, size=9, color=col if col != "D9822B" else AMBER, bold=True)
        for i, c in enumerate(cells):
            x = cx + i * (colw + 4)
            box(sl, x, y + 16, colw, h - 20, fill=bg)
            text(sl, x + 8, y + 24, colw - 16, h - 34, c, size=10, color=TITLE)
        y += h + 4
    box(sl, cx, 402, 3 * colw + 8, 64, fill=TAKE_BG)
    text(sl, cx + 10, 408, 3 * colw - 12, 54,
         [[("En S16 elegimos Fargate: ", {"bold": True, "color": MINT_L}),
           ("AWS mantiene el host; nosotros reconstruimos y volvemos a publicar la imagen cuando cambian sus dependencias.", {})]],
         size=10.5, color=TITLE, anchor="m")
    takeaway(sl, "Fargate nos quita los servidores, no las decisiones: imagen, permisos, red, secretos y datos siguen siendo nuestros.",
             "Idea guía")
    footer(sl, 11, 1)
    notes(sl, """
TIEMPO 18:45–18:46 (1 min).
QUÉ EXPLICAR: modelo de responsabilidad compartida. AWS protege la infraestructura que ejecuta los servicios (hardware, red, instalaciones, regiones, zonas). Nosotros protegemos lo que configuramos dentro: datos, identidades y permisos, sistema operativo cuando lo administramos, configuración de red y cortafuegos, cifrado. El reparto se desplaza según el servicio: con EC2 parcheamos el sistema operativo; con Fargate AWS gestiona el host, pero la imagen y sus dependencias siguen siendo nuestras; con Bedrock AWS ejecuta el modelo, pero decidimos qué datos enviamos y cómo validamos la respuesta.
CONSOLA: ninguna (diapositiva conceptual).
PREGUNTA: «Si una dependencia de nuestra imagen tiene una vulnerabilidad y la desplegamos en Fargate, ¿de quién es la responsabilidad?». Respuesta: nuestra; AWS no actualiza la imagen.
FUENTES: AWS, Shared Responsibility Model (aws.amazon.com/compliance/shared-responsibility-model/).
IMÁGENES: diagrama oficial del modelo de responsabilidad compartida descargado de d1.awsstatic.com desde esa página (en inglés, sin modificar salvo recorte del margen); iconos de AWS Architecture Icons.""")
    return sl


def s12_iam(d):
    sl = d.slide(tag="iam")
    header(sl, "AWS IAM", "IAM: quién puede hacer qué sobre qué recurso",
           "Cada llamada a la API de AWS la hace una identidad. IAM evalúa las políticas que le aplican y decide si esa acción "
           "está permitida sobre ese recurso. Si nada lo permite, se deniega.")
    steps = [("r-iam-role.png", "Identidad", "Usuario, grupo o rol. ECS usa roles con credenciales temporales.", CORAL),
             ("r-iam-perm.png", "Política", "Documento JSON con efecto, acciones, recursos y condiciones.", AMBER),
             ("g-gear.png", "Acción", "servicio:operación, por ejemplo secretsmanager:GetSecretValue.", BLUE),
             ("g-credentials.png", "Recurso", "El ARN concreto sobre el que se actúa: un secreto, un bucket…", MINT)]
    for i, (ic, t, b, col) in enumerate(steps):
        x = 43 + i * 222
        box(sl, x, 140, 204, 100, fill=CARD)
        box(sl, x, 140, 4, 100, fill=col, radius=0)
        img(sl, ic, x + 14, 150, w=28, h=28)
        text(sl, x + 50, 154, 150, 18, t, size=14, font=SERIF, color=TITLE)
        text(sl, x + 14, 186, 180, 50, b, size=10.5, color=TEXT)
        if i < 3:
            line(sl, x + 206, 190, x + 220, 190, color=MINT, w=1.5)
    box(sl, 43, 252, 520, 214, fill="0B151B", line=BORDER)
    text(sl, 55, 260, 400, 12, "POLÍTICA DE EJEMPLO · lectura de un único secreto", size=9, color=MINT, bold=True)
    code = ['{',
            '  "Version": "2012-10-17",',
            '  "Statement": [{',
            '    "Effect": "Allow",',
            '    "Action": "secretsmanager:GetSecretValue",',
            '    "Resource": "arn:aws:secretsmanager:eu-west-1:',
            '      111122223333:secret:s16-lab/anthropic-AbCdEf"',
            '  }]',
            '}']
    text(sl, 76, 280, 480, 140, "\n".join(code), size=10, font=MONO, color=TEXT, bold=True, lsp=Pt(13))
    for n, i, col in [(1, 3, AMBER), (2, 4, BLUE), (3, 5, MINT)]:
        badge(sl, 55, 280 + i * 13 + 6.5 - 6.5, n, fill=col, d=13, size=7.5)
    text(sl, 55, 418, 498, 44,
         [[("1 · Effect ", {"bold": True, "color": AMBER}), ("Allow o Deny.  ", {}),
           ("2 · Action ", {"bold": True, "color": BLUE}), ("servicio:operación.  ", {}),
           ("3 · Resource ", {"bold": True, "color": MINT}), ("un ARN concreto, no «*». ", {}),
           ("Un Deny explícito gana siempre.", {"bold": True})]], size=10, color=TEXT)
    console_panel(sl, 577, 252, 340, 214, "IAM › Roles › (rol) › Permissions | Trust relationships",
                  ["Permissions: políticas adjuntas y su JSON.",
                   "Trust relationships: quién puede asumir el rol, p. ej. ecs-tasks.amazonaws.com.",
                   "Cuenta nueva: suele haber roles vinculados a servicios que sirven para enseñar las pestañas.",
                   "IAM es global: el selector de región indica «Global»."])
    takeaway(sl, "Una política responde a tres preguntas: qué acción, sobre qué recurso y con qué efecto.", "Idea guía")
    footer(sl, 12, 1)
    notes(sl, """
TIEMPO 18:46–18:48 (2 min).
QUÉ EXPLICAR: identidades (usuarios para personas o aplicaciones con credenciales de larga duración, grupos, y roles que se asumen con credenciales temporales; las personas deberían entrar con IAM Identity Center o federación). Políticas: documentos JSON con Effect, Action, Resource y Condition opcional. Evaluación: por defecto todo está denegado; un Allow aplicable permite; un Deny explícito gana siempre. «Permitir una acción sobre un recurso» = Allow + servicio:operación + ARN.
CONSOLA: IAM › Roles → abrir un rol (en una cuenta nueva, un rol vinculado a servicio como AWSServiceRoleForSupport). Pestaña Permissions: política adjunta y su JSON. Pestaña Trust relationships: el Principal que puede asumir el rol. Mostrar IAM › Policies › una política gestionada por AWS y su vista JSON. No crear usuarios ni claves de acceso.
SEÑALAR: Effect, Action, Resource; Principal en la relación de confianza; que IAM es global.
PREGUNTA: «Si una política permite GetSecretValue sobre "*", ¿qué secretos puede leer?». Respuesta: todos los de la cuenta a los que no se aplique un Deny ni otra restricción (p. ej. la política de clave KMS).
FUENTES: IAM User Guide, «Policies and permissions» y «Policy evaluation logic» (docs.aws.amazon.com/IAM/latest/UserGuide/). El JSON es un ejemplo ficticio con la cuenta de ejemplo 111122223333; el sufijo -AbCdEf imita los seis caracteres aleatorios que Secrets Manager añade al ARN.
IMÁGENES: AWS Architecture Icons: IAM Role, IAM Permissions, genéricos Gear y Credentials; icono AWS Management Console.""")
    return sl


def s13_privilegio(d):
    sl = d.slide(tag="privilegio")
    header(sl, "Mínimo privilegio", "Permisos de AWS y acceso de red: dos puertas distintas",
           "IAM decide si una identidad puede llamar a una API de AWS. La red decide si un paquete puede llegar a una IP y un puerto. "
           "Un fallo en una no se arregla abriendo la otra.")
    lanes = [("PUERTA 1 · PERMISOS DE AWS (IAM)", VIOLET, VIOLET_BG,
              [("aws-ecs.png", "ECS · execution role"), ("r-iam-perm.png", "secretsmanager:\nGetSecretValue"), ("aws-secrets.png", "Secreto del proveedor")],
              "Si falta: AccessDenied. La tarea no arranca (ResourceInitializationError)."),
             ("PUERTA 2 · ACCESO DE RED", BLUE, BLUE_BG,
              [("g-client.png", "Portátil\n203.0.113.10"), ("g-firewall.png", "Security group\nTCP 8000 desde /32"), ("r-ecs-task.png", "Tarea\n10.216.0.x:8000")],
              "Si falta: timeout. AWS no devuelve ningún mensaje de error.")]
    y = 138
    for title, col, bg, nodes, fail in lanes:
        box(sl, 43, y, 874, 92, fill=bg)
        text(sl, 55, y + 8, 400, 12, title, size=9, color=col, bold=True)
        x = 55
        for k, (ic, lab) in enumerate(nodes):
            box(sl, x, y + 26, 158, 56, fill=CARD)
            img(sl, ic, x + 8, y + 38, w=30, h=30)
            text(sl, x + 44, y + 32, 110, 44, lab, size=10, color=TITLE, bold=True, anchor="m")
            if k < 2:
                line(sl, x + 160, y + 54, x + 178, y + 54, color=col, w=1.5)
            x += 180
        text(sl, 600, y + 30, 305, 50, fail, size=10.5, color=TITLE, anchor="m")
        y += 100
    cards = [("✕  Demasiado amplio", CORAL, CORAL_BG, "Action: secretsmanager:*\nResource: *",
              "Permite leer, cambiar y borrar cualquier secreto de la cuenta."),
             ("✓  Mínimo privilegio", MINT, TAKE_BG, "Action: secretsmanager:GetSecretValue\nResource: …:secret:s16-lab/anthropic-…",
              "Solo leer el secreto que la tarea necesita.")]
    for i, (t, col, bg, code, b) in enumerate(cards):
        x = 43 + i * 292
        box(sl, x, 340, 282, 126, fill=bg)
        text(sl, x + 12, 350, 260, 16, t, size=11.5, color=col, bold=True)
        text(sl, x + 12, 372, 262, 34, code, size=9.5, font=MONO, color=TITLE, bold=True)
        text(sl, x + 12, 412, 258, 48, b, size=10.5, color=TEXT)
    box(sl, 627, 340, 290, 126, fill=CARD, line=BORDER)
    text(sl, 639, 350, 266, 12, "NUESTRA PLANTILLA S16", size=9, color=MINT, bold=True)
    text(sl, 639, 368, 268, 94,
         "El execution role solo descarga la imagen de su repositorio, escribe en su grupo de logs y lee un secreto concreto. "
         "El task role no tiene permisos porque la API no llama a servicios de AWS.", size=10.5, color=TEXT)
    takeaway(sl, "Abrir 0.0.0.0/0 no arregla un AccessDenied, y dar AdministratorAccess no arregla una regla de red.", "Idea guía")
    footer(sl, 13, 1)
    notes(sl, """
TIEMPO 18:48–18:50 (2 min).
QUÉ EXPLICAR: hay dos controles independientes. IAM autoriza llamadas a la API de AWS (por ejemplo, que ECS lea un secreto o descargue una imagen). La red (security groups, rutas, NACL) controla qué conexiones llegan a una IP y puerto. Mínimo privilegio: conceder solo las acciones y recursos necesarios; preferir un ARN concreto a «*». Nuestra plantilla lo aplica: el execution role tiene ecr:GetAuthorizationToken, lectura de capas solo en su repositorio, logs:CreateLogStream/PutLogEvents en su grupo y secretsmanager:GetSecretValue sobre un ARN (más kms:Decrypt si se usa una clave propia). El task role no tiene políticas.
CONSOLA: IAM › Roles → buscar «ecs» para ver si existe ecsTaskExecutionRole u otro rol de ejemplo; si no existe, explicarlo sobre la plantilla infra/s16/servicio.json. IAM › Access Analyzer se puede mencionar como herramienta para revisar permisos sin abrirla.
PREGUNTA: «La tarea no arranca y el evento dice "unable to pull secrets". ¿Abro el puerto 8000 a todo Internet?». Respuesta: no; es un problema de permisos (execution role, ARN, KMS) o de salida de red hacia el servicio, no de entrada.
FUENTES: IAM User Guide, «Security best practices in IAM» (grant least privilege); ECS Developer Guide, «Amazon ECS task execution IAM role»; plantilla infra/s16/servicio.json.
IMÁGENES: AWS Architecture Icons (ECS, IAM Permissions, Secrets Manager, ECS Task; genéricos Client y Firewall).""")
    return sl


PART1 = [s01_portada, s02_encuesta, s03_caso, s04_mapa, s05_metodo, s06_div1, s07_proveedores, s08_consola,
         s09_arn, s10_regiones, s11_responsabilidad, s12_iam, s13_privilegio]
