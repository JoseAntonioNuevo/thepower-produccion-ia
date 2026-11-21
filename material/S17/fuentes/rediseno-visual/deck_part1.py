"""Diapositivas 1–8: apertura y bloque 1 (serverless y arquitectura)."""
from deck_lib import *  # noqa: F401,F403

SRC_AWS_ICONS = ("Iconos: AWS Architecture Icons, paquete oficial del 31/07/2026 (aws.amazon.com/architecture/icons). "
                 "Logotipo de AWS: a0.awsstatic.com (aws_logo_smile), igual que en S16.")


def s01_portada(d):
    sl = d.slide(BG_SECTION, "portada")
    img(sl, "thepower-logo.png", 38, 34, h=32)
    text(sl, 43, 104, 420, 14, "S17 · AI ENGINEER", size=10, color=MINT, bold=True)
    text(sl, 43, 124, 450, 92, "Serverless AI:\nAWS Bedrock y Lambda", size=36, font=SERIF, color=TITLE)
    text(sl, 43, 226, 425, 78,
         "Desplegar una API de IA sin gestionar servidores: recorremos en la consola de AWS cómo API Gateway, "
         "Lambda, Bedrock, IAM y CloudWatch atienden una petición, y qué determina su coste, su latencia y sus límites.",
         size=12.5, color=TEXT)
    text(sl, 43, 322, 420, 16, "José Antonio Nuevo", size=12.5, color=TITLE, bold=True)
    text(sl, 43, 342, 440, 48, "Martes 17 de noviembre de 2026 · grupo M/J\nLunes 23 de noviembre de 2026 · grupo L/X\n"
         "18:30–20:00 · hora de Madrid", size=10.5, color=MUTED)
    box(sl, 497, 52, 420, 410, fill=BG, line="2A5246", radius=8)
    img(sl, "aws-logo-dark.png", 515, 70, h=34)
    text(sl, 515, 116, 380, 14, "SERVICIOS QUE RECORREREMOS EN LA CONSOLA", size=9, color=MINT, bold=True)
    items = [("aws-apigw.png", "API Gateway"), ("aws-lambda.png", "Lambda"), ("aws-bedrock.png", "Bedrock"),
             ("aws-iam.png", "IAM"), ("aws-cloudwatch.png", "CloudWatch")]
    for i, (ic, lab) in enumerate(items):
        x = 515 + i * 78
        img(sl, ic, x + 15, 140, w=44, h=44)
        text(sl, x - 4, 188, 82, 14, lab, size=9.5, color=TITLE, align="c", bold=True)
    text(sl, 515, 222, 380, 12, "EL RECORRIDO DE UNA PETICIÓN", size=9, color=MINT, bold=True)
    flow = ["cliente", "API Gateway", "Lambda", "Bedrock", "respuesta"]
    ws = [58, 82, 58, 62, 70]
    x = 515
    for i, (f, w) in enumerate(zip(flow, ws)):
        chip(sl, x, 242, w, 22, f, fill=TAKE_BG, color=MINT_L, size=9.5, line="2A5246")
        if i < len(flow) - 1:
            line(sl, x + w + 2, 253, x + w + 12, 253, color=MINT, w=1.25)
        x += w + 14
    rows = [("aws-iam.png", "IAM", "decide quién puede invocar cada pieza."),
            ("aws-cloudwatch.png", "CloudWatch", "registra el recorrido: logs, duración y errores.")]
    y = 280
    for ic, t, b in rows:
        img(sl, ic, 515, y, w=22, h=22)
        text(sl, 545, y + 3, 350, 16, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10.5, color=TEXT)
        y += 30
    box(sl, 515, 350, 384, 94, fill=CARD, radius=6)
    text(sl, 527, 358, 360, 12, "Y COMO ALTERNATIVAS", size=8.5, color=MUTED, bold=True)
    alts = [("az-functions.png", "Azure Functions"), ("az-foundry.png", "Microsoft Foundry"),
            ("gc-functions.png", "Cloud Run functions"), ("gc-vertex.png", "Vertex AI")]
    for i, (ic, lab) in enumerate(alts):
        x = 527 + i * 92
        img(sl, ic, x + 28, 376, w=30, h=30)
        text(sl, x - 2, 410, 90, 26, lab, size=8.5, color=TEXT, align="c")
    notes(sl, """
TIEMPO 18:30–18:31 (1 min).
QUÉ EXPLICAR: título del temario: «Serverless AI: AWS Bedrock + Lambda». Hoy mantenemos el problema de S16 (una API de soporte que clasifica una incidencia) y cambiamos la arquitectura: API Gateway recibe la petición, Lambda ejecuta nuestro código, Bedrock da acceso al modelo, IAM controla los permisos y CloudWatch registra el recorrido. Entraremos en la consola para ver cada servicio desde dentro: qué es, qué responsabilidad tiene, qué vemos en sus pantallas, qué configuraríamos, cómo se conecta con los demás y qué determina su coste, latencia y límites.
FORMATO: abriremos listados y formularios y cancelaremos antes de guardar. No creamos recursos, no contratamos capacidad, no ejecutamos inferencias de pago y no desplegamos el laboratorio durante la sesión. La práctica es opcional.
CONSOLA: tener abierta la consola en Europa (Irlanda), eu-west-1, en otra pestaña y sin pantallas de credenciales.
PREGUNTA: «¿Qué creéis que significa "sin servidores"? ¿Desaparecen los servidores?».
FUENTES: temario AI Engineer (texto de Laura): «Desplegar modelos y agentes sin gestionar servidores, usando los servicios de IA gestionada de los grandes proveedores. AWS bedrock / AWS Lambda / Alternativas como Azure y Vertex AI / Consideraciones de coste, latencia y límites de las arquitecturas». Misma presentación para el 17/11 (M/J) y el 23/11 (L/X).
IMÁGENES: logotipo de thePower (recurso original del curso). """ + SRC_AWS_ICONS + " Azure Functions y Microsoft Foundry: Azure Public Service Icons V25 (Microsoft). Cloud Run functions y Vertex AI: iconos oficiales de cloud.google.com/icons.")
    return sl


def s02_encuesta(d):
    sl = d.slide(tag="encuesta")
    header(sl, "Antes de empezar", "Encuesta de S16 y plan de la sesión",
           "Un minuto para valorar la sesión anterior de tu grupo. Después, 90 minutos para seguir una petición por los "
           "servicios de AWS desde su consola; la práctica queda como opción para después.")
    box(sl, 43, 140, 250, 326, fill=CARD, line=BORDER)
    box(sl, 70, 156, 196, 196, fill="FFFFFF", radius=6)
    img(sl, "qr-ai-engineer.jpg", 78, 164, w=180, h=180)
    text(sl, 55, 362, 226, 18, "Encuesta de la sesión anterior · S16", size=11.5, color=TITLE, bold=True, align="c")
    text(sl, 55, 382, 226, 14, "Formulario de AI Engineer", size=10, color=MUTED, align="c")
    text(sl, 55, 402, 226, 50, "Valora S16, la sesión anterior de tu grupo (no la de hoy). Escanea el código con la cámara del móvil.",
         size=10, color=TEXT, align="c")
    rows = [("18:30", "Apertura", "QR, caso conductor y continuidad con S16", 5, MUTED),
            ("18:35", "1 · Serverless", "Qué cambia frente al contenedor de S16", 10, MINT),
            ("18:45", "2 · Bedrock", "Catálogo, ficha, perfiles, parámetros y playground", 15, PINK),
            ("19:00", "3 · Lambda y API Gateway", "Función, configuración, rutas e integración", 20, AMBER),
            ("19:20", "4 · IAM y CloudWatch", "Tres permisos, SigV4, logs y diagnóstico", 10, VIOLET),
            ("19:30", "5 · Latencia y límites", "Frío y caliente, relojes, timeouts y concurrencia", 10, BLUE),
            ("19:40", "6 · Costes y alternativas", "1.000 solicitudes, Azure, Google Cloud y elección", 10, CORAL),
            ("19:50", "7 · Práctica y cierre", "Evidencias, práctica opcional y preguntas", 10, MINT_L)]
    text(sl, 312, 140, 60, 12, "HORA", size=8.5, color=MUTED, bold=True)
    text(sl, 385, 140, 180, 12, "BLOQUE", size=8.5, color=MUTED, bold=True)
    text(sl, 580, 140, 280, 12, "QUÉ HAREMOS", size=8.5, color=MUTED, bold=True)
    text(sl, 862, 140, 55, 12, "MIN", size=8.5, color=MUTED, bold=True, align="r")
    y = 156
    for t, b, desc, m, col in rows:
        box(sl, 312, y, 605, 35, fill=CARD)
        box(sl, 312, y, 4, 35, fill=col, radius=0)
        text(sl, 324, y + 10, 56, 16, t, size=11, font=MONO, color=MINT_L, bold=True)
        text(sl, 385, y + 10, 195, 16, b, size=11, color=TITLE, bold=True)
        text(sl, 580, y + 4, 275, 28, desc, size=10, color=TEXT, anchor="m")
        text(sl, 862, y + 10, 45, 16, str(m), size=11.5, color=col, bold=True, align="r")
        y += 39
    takeaway(sl, "Hoy no creamos recursos ni ejecutamos inferencias de pago: abrimos pantallas, explicamos sus campos y cancelamos.",
             "Formato")
    footer(sl)
    notes(sl, """
TIEMPO 18:31–18:33 (2 min).
QUÉ EXPLICAR: dar un minuto para escanear. La encuesta evalúa «S16, la sesión anterior de tu grupo»: en M/J es la S16 del 12/11 y en L/X la S16 del 18/11. Ambas las impartió José, con la misma clase, así que la continuidad es la misma para los dos grupos. Después, presentar la agenda: siete bloques que siguen una petición desde el cliente hasta el modelo y vuelta, y terminan en el coste y las alternativas.
FORMATO: teoría y consola a la vez. En cada servicio: diapositiva para situarlo, consola para verlo, diapositiva para fijar la idea. Preguntas durante los recorridos y al final.
CONSOLA: aún no. Tener la consola en eu-west-1.
PREGUNTA: «En S16 la API vivía en un contenedor. ¿Qué tendría que pasar para no tener que mantener ese contenedor encendido?».
FUENTES: QR de AI Engineer recibido de Laura el 19/10/2026, el mismo que usa S16, sin modificar (SHA-256 29c9041e…8c6). Destino: https://kb.tools.thepower.education/feedback/feedback-form.html?form=ai-engineer . El QR que traía la versión anterior de S17 estaba desactualizado y se ha sustituido. Indicaciones de Laura del 04/11/2026: ejercicios no obligatorios, teoría junto a aplicaciones prácticas, material manejable y pasos comprensibles.
IMÁGENES: QR de AI Engineer (material/S16/assets/qr-ai-engineer.jpg), byte a byte.""")
    return sl


def s03_caso(d):
    sl = d.slide(tag="caso")
    header(sl, "Caso conductor", "La misma incidencia, otra arquitectura",
           "Conservamos el contrato de S16: una incidencia ficticia entra y sale una clasificación. Lo que cambia es quién "
           "ejecuta el código, cómo se autoriza la llamada y dónde está el modelo.")
    box(sl, 43, 134, 430, 66, fill=CARD, line=BORDER)
    text(sl, 55, 142, 300, 12, "PETICIÓN · POST /clasificar", size=9, color=MINT, bold=True)
    text(sl, 55, 158, 410, 36, '{"texto": "Me han cobrado dos veces la factura de este mes. Es una incidencia ficticia."}',
         size=9.5, font=MONO, color=MINT_L, bold=True)
    line(sl, 150, 201, 150, 214, color=MINT)
    box(sl, 43, 216, 430, 250, fill=CARD, line=BORDER)
    text(sl, 55, 224, 400, 12, "RESPUESTA · forma del JSON (valores ilustrativos)", size=9, color=MINT, bold=True)
    code = ['{"resultado": {',
            '   "categoria": "facturacion",',
            '   "prioridad": "alta | media | baja",',
            '   "respuesta": "…"},',
            ' "metadata": {',
            '   "request_id": "…",  "lambda_version": "…",',
            '   "duration_ms": …,  "model_duration_ms": …,',
            '   "consumo": {"inputTokens": …, "outputTokens": …}}}']
    p = code_block(sl, 55, 240, 380, code, size=9.5, pitch=13.2)
    box(sl, 440, 242, 4, 4 * p, fill=PINK, radius=0)
    box(sl, 440, 242 + 4 * p, 4, 4 * p, fill=MINT, radius=0)
    text(sl, 55, 362, 408, 30, [[("Lo propone el modelo y lo valida Lambda:  ", {"bold": True, "color": PINK}),
                                  ("categoría, prioridad y una respuesta breve.", {})]], size=10, color=TEXT)
    text(sl, 55, 390, 408, 44, [[("Lo añade nuestro programa:  ", {"bold": True, "color": MINT}),
                                  ("identificador, versión, tiempos y consumo de tokens cuando Bedrock lo informa. "
                                   "Si no lo informa, queda vacío: nunca se inventa.", {})]], size=10, color=TEXT)
    text(sl, 55, 436, 408, 24, "Categorías y prioridades proceden de S7/S8 y de contratos.py.", size=9, color=MUTED)
    text(sl, 487, 134, 430, 12, "QUÉ SE CONSERVA Y QUÉ CAMBIA RESPECTO A S16", size=9, color=MUTED, bold=True)
    rows = [("Contrato", "Igual en S16 y S17", "texto → categoría, prioridad y respuesta.", "g-json-script.png", None),
            ("Código", "Contenedor → función", "De una tarea de Fargate encendida a una función Lambda por invocación.",
             "aws-fargate.png", "aws-lambda.png"),
            ("Entrada HTTP", "IP de la tarea → API Gateway", "Un endpoint gestionado con ruta, autorización IAM y límites.",
             "g-internet.png", "aws-apigw.png"),
            ("Acceso al modelo", "Clave → rol de IAM", "En S16, clave de Anthropic en Secrets Manager; aquí, permiso bedrock:InvokeModel.",
             "r-iam-role.png", None),
            ("Modelo", "Anthropic → Nova 2 Lite", "Nova 2 Lite en Bedrock con el perfil europeo de la referencia.",
             "aws-bedrock.png", None)]
    y = 150
    for t, svc, desc, ic1, ic2 in rows:
        box(sl, 487, y, 430, 60, fill=CARD)
        img(sl, ic1, 497, y + 15, w=27, h=27)
        if ic2:
            img(sl, ic2, 527, y + 15, w=27, h=27)
        text(sl, 563, y + 7, 150, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, 700, y + 8, 208, 14, svc, size=9.5, color=MINT, bold=True, align="r")
        text(sl, 563, y + 25, 346, 32, desc, size=10, color=TEXT)
        y += 63
    takeaway(sl, "El problema de IA ya lo conocemos. Hoy estudiamos dónde se ejecuta, quién puede invocarlo, cuánto tarda y cuánto cuesta.",
             "Idea guía")
    footer(sl)
    notes(sl, """
TIEMPO 18:33–18:35 (2 min).
QUÉ EXPLICAR: el caso conductor es el mismo de S16: una incidencia ficticia entra por POST /clasificar y sale una categoría (acceso, facturacion, tecnico, consulta), una prioridad (alta, media, baja) y una respuesta breve. Separar dos orígenes en la respuesta: el resultado lo propone el modelo y nuestro código lo valida; la metadata la añade el programa (request_id, versión de Lambda, duration_ms, model_duration_ms y consumo de tokens cuando Bedrock lo informa). Si Bedrock no informa un dato, queda null; nunca se convierte en cero.
CONTINUIDAD: en S16 la API corría en una tarea de ECS sobre Fargate y llamaba a Anthropic con una clave guardada en Secrets Manager. En S17 la función Lambda llama a Nova 2 Lite en Bedrock con el permiso de su rol de IAM. Ambos grupos vieron la misma S16 con José, así que basta recordar el dibujo de S16.
CÓDIGO (opcional, 30 s): datos/peticion.json y src/curso_ia/contratos.py.
CONSOLA: ninguna todavía.
PREGUNTA: «¿Quién decide el request_id: el modelo o nuestro programa?». Respuesta: el programa (es el identificador de la invocación de Lambda).
FUENTES: material/S17 (README, guion, guía del alumno) y src/curso_ia/serverless/handler.py y bedrock.py del repositorio 4-produccion-ia. Los valores del JSON son ilustrativos, no una ejecución real.
IMÁGENES: """ + SRC_AWS_ICONS + " Icono genérico JSON Script e Internet del mismo paquete.")
    return sl


def s04_div1(d):
    sl = divider(d, 1, "Serverless", "Del contenedor encendido a la función por invocación",
                 "Qué gestiona AWS, qué seguimos configurando y qué ocurre cada vez que llega un evento.",
                 ["¿Qué gestiona AWS y qué configuramos nosotros?",
                  "¿En qué se diferencia un contenedor continuo de una función?",
                  "¿Qué estado sobrevive entre invocaciones?",
                  "¿Por qué serverless no es gratis ni ilimitado?"],
                 [("aws-fargate.png", "AWS Fargate\n(S16)"), ("aws-lambda.png", "AWS Lambda\n(S17)"),
                  ("aws-apigw.png", "Amazon\nAPI Gateway")], "18:35–18:45 · 10 min")
    notes(sl, """
TIEMPO 18:35 (10 s). Bloque 1 de 7: serverless y arquitectura, de 18:35 a 18:45 (10 min).
QUÉ EXPLICAR: leer las cuatro preguntas; las responderemos con la comparación con S16.
CONSOLA: ninguna en el separador.
PREGUNTA: «¿Qué creéis que sigue siendo responsabilidad nuestra si AWS gestiona los servidores?»
FUENTES: temario AI Engineer y guion de S17 (material/S17/guion-profesor.md), con la distribución de tiempos de esta versión.
IMÁGENES: """ + SRC_AWS_ICONS)
    return sl


def s05_comparacion(d):
    sl = d.slide(tag="comparacion")
    header(sl, "Serverless frente a S16", "Un contenedor que espera frente a código que se invoca",
           "En S16 un proceso servidor estaba siempre en marcha esperando peticiones. En S17 no hay proceso esperando: "
           "cada petición se convierte en un evento y Lambda ejecuta nuestra función para atenderlo.")
    panels = [(43, "S16 · CONTENEDOR EN FARGATE", CORAL, CORAL_BG,
               [("g-client.png", "Cliente"), ("aws-fargate.png", "Tarea en Fargate"), ("g-generic-application.png", "Anthropic")],
               "Un proceso (uvicorn) escucha el puerto 8000 las 24 horas. Pagamos vCPU y memoria por cada segundo encendido, "
               "lleguen o no peticiones."),
              (485, "S17 · FUNCIÓN EN LAMBDA", MINT, TAKE_BG,
               [("g-client.png", "Cliente"), ("aws-apigw.png", "API Gateway"), ("aws-lambda.png", "Lambda"),
                ("aws-bedrock.png", "Bedrock")],
               "Cada petición llega como evento. Lambda prepara un entorno, ejecuta el handler y factura invocaciones y "
               "duración (GB-s).")]
    for x, lab, col, bg, nodes, body in panels:
        box(sl, x, 132, 432, 178, fill=bg)
        text(sl, x + 12, 140, 300, 12, lab, size=9, color=col, bold=True)
        n = len(nodes)
        step = 410 / n
        for k, (ic, t) in enumerate(nodes):
            cx = x + 12 + k * step + step / 2
            img(sl, ic, cx - 15, 158, w=30, h=30)
            text(sl, cx - step / 2, 191, step, 13, t, size=9, color=TITLE, bold=True, align="c")
            if k < n - 1:
                line(sl, cx + 19, 173, cx + step - 19, 173, color=col, w=1.25)
        # línea de tiempo
        text(sl, x + 12, 212, 200, 11, "24 horas de un día con pocas peticiones", size=8.5, color=MUTED)
        box(sl, x + 12, 226, 408, 2, fill=BORDER, radius=0)
        reqs = [0.08, 0.31, 0.36, 0.62, 0.88]
        if col == CORAL:
            box(sl, x + 12, 232, 408, 14, fill=CORAL, radius=2)
            text(sl, x + 16, 233, 300, 12, "tarea en marcha · facturada todo el tiempo", size=8, color=DARK, bold=True, check=False)
        for r in reqs:
            rx = x + 12 + r * 408
            box(sl, rx, 222, 2, 10, fill=TITLE, radius=0)
            if col == MINT:
                box(sl, rx - 1, 232, 16 if r != reqs[0] else 26, 14, fill=MINT, radius=2)
        if col == MINT:
            text(sl, x + 220, 212, 200, 11, "bloques = ejecuciones facturadas", size=8.5, color=MINT_L, align="r", check=False)
        text(sl, x + 12, 254, 408, 52, body, size=10, color=TEXT)
    rows = [["", "S16 · Fargate", "S17 · Lambda"],
            ["Qué arranca", "Un proceso servidor que escucha un puerto", "Una función handler que Lambda invoca con un evento"],
            ["Cuándo cuesta cómputo", "Mientras la tarea está encendida (vCPU-h y GB-h)", "Por invocación y por GB-s de ejecución"],
            ["Escalado", "Número de tareas que configuramos", "Entornos que Lambda crea según la concurrencia"],
            ["Estado en memoria", "Dura mientras la tarea siga viva", "Efímero: puede reutilizarse, sin garantía"],
            ["Duración de una petición", "Sin plazo propio de Fargate por petición", "Hasta 15 min en Lambda; 30 s detrás de HTTP API"]]
    table(sl, 43, 320, 874, [170, 352, 352], rows, size=9.5, row_h=24, bold_cols=(0,), colors={0: TITLE})
    takeaway(sl, "En S16 pagábamos por tener el servidor encendido; en S17 pagamos por ejecutar código cuando llega un evento. Los tokens, en ambos.",
             "Idea guía")
    footer(sl, block=1)
    notes(sl, """
""" + timing_note("18:35", "18:38") + """
QUÉ EXPLICAR: contraste con S16. Fargate ejecuta un contenedor continuo: el proceso servidor (uvicorn) está en marcha y espera peticiones; pagamos por el tiempo encendido. Lambda ejecuta código por invocación: API Gateway transforma la petición en un evento, Lambda ejecuta el handler en un entorno de ejecución y devuelve una respuesta. Leer la tabla: qué arranca, cuándo cuesta cómputo, cómo escala, qué pasa con el estado y qué duración admite una petición. Matizar la última fila: Lambda admite hasta 900 s por invocación, pero detrás de una HTTP API la integración tiene un máximo documentado de 30 s.
CONSOLA: opcional, abrir Lambda › Event functions para enseñar que una función no tiene «instancias encendidas» que administrar (la consola de 2026 etiqueta este tipo como «Event function»). No crear nada.
PREGUNTA: «Si nadie llama a la API durante una noche, ¿qué factura cada arquitectura?». Respuesta: Fargate, el tiempo encendido; Lambda, nada por cómputo (sí lo que siga almacenado: logs, artefacto).
FUENTES: AWS Lambda Developer Guide, «What is AWS Lambda?» y «Lambda quotas» (900 s por invocación); API Gateway Developer Guide, «Quotas for configuring and running an HTTP API» (30 s de integración), consultadas el 06/11/2026. Material de S16 (tarea en Fargate, uvicorn en el puerto 8000).
IMÁGENES: """ + SRC_AWS_ICONS + " Iconos genéricos Client y Generic Application del mismo paquete. La línea de tiempo es un esquema propio.")
    return sl


def s06_responsabilidades(d):
    sl = d.slide(tag="responsabilidades")
    header(sl, "Responsabilidades", "Qué gestiona AWS y qué seguimos decidiendo nosotros",
           "Serverless significa que no administramos servidores, no que desaparezcan. AWS opera la infraestructura; "
           "nosotros seguimos siendo responsables del código, los permisos, los límites y el coste.")
    box(sl, 43, 132, 300, 230, fill=BLUE_BG)
    img(sl, "aws-logo-dark.png", 55, 142, h=20)
    text(sl, 100, 144, 230, 14, "LO GESTIONA AWS", size=9.5, color=BLUE, bold=True)
    aws_items = ["Servidores, sistema operativo y parches del runtime gestionado.",
                 "Crear, reutilizar y retirar entornos de ejecución según la demanda.",
                 "El endpoint HTTPS y su certificado en API Gateway.",
                 "La infraestructura de inferencia del modelo en Bedrock.",
                 "Disponibilidad dentro de la región."]
    bullets(sl, 55, 174, 280, 184, aws_items, size=11, mark_color=BLUE, space=7)
    box(sl, 355, 132, 562, 230, fill=TAKE_BG)
    text(sl, 367, 144, 300, 14, "LO DECIDIMOS NOSOTROS", size=9.5, color=MINT, bold=True)
    ours = [("Código y dependencias", "Paquete para Linux con el SDK y el contrato.", "r-lambda-fn.png"),
            ("Memoria, timeout y concurrencia", "Fijan CPU, plazo y ejecuciones simultáneas.", "g-gear.png"),
            ("Permisos de cada pieza", "Quién invoca la ruta, la función y el modelo.", "r-iam-role.png"),
            ("Validación", "Entrada antes del modelo; salida antes de responder.", "g-json-script.png"),
            ("Modelo, región y parámetros", "Perfil eu., maxTokens y datos que enviamos.", "aws-bedrock.png"),
            ("Observación y retirada", "Logs, retención, alarmas y limpieza.", "r-cw-logs.png")]
    for i, (t, b, ic) in enumerate(ours):
        c, r = divmod(i, 3)
        x = 367 + c * 275
        y = 168 + r * 62
        img(sl, ic, x, y + 3, w=26, h=26)
        text(sl, x + 34, y, 230, 15, t, size=10.5, color=TITLE, bold=True)
        text(sl, x + 34, y + 17, 232, 40, b, size=9.5, color=TEXT)
    text(sl, 43, 372, 600, 12, "SERVERLESS NO SIGNIFICA GRATIS NI ILIMITADO", size=9, color=AMBER, bold=True)
    chips = [("Pago por uso", "Invocaciones, GB-s, solicitudes HTTP y tokens: cada petición cuesta algo."),
             ("Cuotas", "1.000 ejecuciones simultáneas de Lambda por región y cuenta, por defecto."),
             ("Plazos", "Hasta 15\u00a0min por invocación de Lambda; 30\u00a0s de integración en HTTP API."),
             ("Lo almacenado", "Logs y artefacto en S3 siguen costando aunque no haya tráfico.")]
    w = (874 - 3 * 10) / 4
    for i, (t, b) in enumerate(chips):
        x = 43 + i * (w + 10)
        box(sl, x, 388, w, 78, fill=AMBER_BG)
        text(sl, x + 10, 395, w - 20, 14, t, size=10.5, color=AMBER, bold=True)
        text(sl, x + 10, 413, w - 20, 50, b, size=9.5, color=TITLE)
    takeaway(sl, "Serverless quita servidores de nuestra lista de tareas, no decisiones: código, permisos, límites y coste siguen siendo nuestros.",
             "Idea guía")
    footer(sl, block=1)
    notes(sl, """
""" + timing_note("18:38", "18:40") + """
QUÉ EXPLICAR: el proveedor aprovisiona y opera los servidores; nosotros configuramos función, dependencias, memoria, tiempo, concurrencia, identidades, modelo y parámetros, validación y observación. Cobro por uso no significa coste cero ni capacidad infinita: cada invocación, cada GB-s, cada solicitud HTTP y cada token se facturan; hay cuotas por cuenta y región; hay plazos por invocación y por integración; lo que queda almacenado (logs, artefacto) cuesta aunque no haya tráfico.
CONSOLA: Service Quotas › AWS services › AWS Lambda › «Concurrent executions» (solo mirar el valor aplicado; no solicitar aumentos). Alternativa: Lambda › Account settings / Dashboard si la consola lo muestra.
PREGUNTA: «¿Quién tiene que validar que la prioridad devuelta existe: AWS o nosotros?». Respuesta: nosotros, en el handler.
FUENTES: AWS Lambda Developer Guide, «What is AWS Lambda?», «Lambda quotas» y «Lambda concurrency» (1.000 por cuenta y región por defecto; 900 s por invocación), consultadas el 06/11/2026. API Gateway, «Quotas for configuring and running an HTTP API» (30 s).
IMÁGENES: logotipo de AWS (versión para fondo oscuro, como en S16). """ + SRC_AWS_ICONS)
    return sl


def s07_ciclo(d):
    sl = d.slide(tag="ciclo")
    header(sl, "Evento, función, ejecución y respuesta", "Qué ocurre cada vez que Lambda atiende una petición",
           "API Gateway entrega un evento; Lambda ejecuta el handler en un entorno aislado y devuelve una respuesta. "
           "El entorno puede ser nuevo o reutilizado, y eso cambia el tiempo de la petición.")
    steps = [("g-json-script.png", "1 · Evento", "API Gateway convierte la petición HTTP en un JSON (formato 2.0)."),
             ("r-lambda-fn.png", "2 · Función", "lambda_handler(event, context) es nuestro punto de entrada."),
             ("g-servers.png", "3 · Ejecución", "Lambda la ejecuta en un entorno aislado, nuevo o reutilizado."),
             ("g-document.png", "4 · Respuesta", "statusCode, headers y body; API Gateway la devuelve como HTTP.")]
    w = (874 - 3 * 18) / 4
    for i, (ic, t, b) in enumerate(steps):
        x = 43 + i * (w + 18)
        box(sl, x, 132, w, 82, fill=CARD)
        img(sl, ic, x + 10, 142, w=28, h=28)
        text(sl, x + 46, 147, w - 52, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, x + 10, 176, w - 20, 36, b, size=9.5, color=TEXT)
        if i < 3:
            line(sl, x + w + 2, 173, x + w + 16, 173, color=MINT, w=1.5)
    sw, sh = shot(sl, "shot-lifecycle.png", 43, 240, w=520, kind="diagrama", tag_w=230,
                  caption="Fases INIT, INVOKE y SHUTDOWN de un entorno. Fuente: AWS Lambda Developer Guide.", cap_w=520)
    cards = [("Entorno nuevo", "Descarga el código, arranca el runtime y ejecuta lo que está fuera del handler antes de atender la petición.", BLUE),
             ("Entorno reutilizado", "Solo se ejecuta el handler: las variables globales y el cliente del SDK ya existen.", MINT)]
    y = 368
    for t, b, col in cards:
        box(sl, 43, y, 254, 47, fill=CARD)
        box(sl, 43, y, 3.5, 47, fill=col, radius=0)
        text(sl, 55, y + 5, 236, 14, t, size=10.5, color=col, bold=True)
        text(sl, 55, y + 20, 236, 27, b, size=9, color=TEXT)
        y += 51
    box(sl, 309, 368, 254, 98, fill=CARD)
    box(sl, 309, 368, 3.5, 98, fill=AMBER, radius=0)
    text(sl, 321, 374, 236, 14, "En nuestro código", size=10.5, color=AMBER, bold=True)
    text(sl, 321, 391, 236, 74, "client_for() se cachea: el cliente de bedrock-runtime y su conexión se reutilizan en caliente. "
                                "FIRST_IN_ENVIRONMENT marca la primera ejecución del proceso: es una pista, no una medición.",
         size=9.5, color=TEXT)
    side_note(sl, 578, 240, 339, 230, "Estado efímero",
              "Lo que el código crea fuera del handler puede seguir en memoria si Lambda reutiliza el entorno. "
              "No hay garantía de que ocurra ni de cuánto dura.\n\n"
              "Sirve para reutilizar clientes y conexiones. No sirve para guardar datos de negocio: lo que haya que "
              "conservar va a un almacén persistente.\n\n"
              "Tampoco el directorio /tmp es persistente entre entornos.", accent=VIOLET, size=10.5)
    takeaway(sl, "Una función no es un servidor que espera: es código que Lambda invoca con un evento, en un entorno que a veces reutiliza.",
             "Idea guía")
    footer(sl, block=1)
    notes(sl, """
""" + timing_note("18:40", "18:43") + """
QUÉ EXPLICAR: el ciclo evento → función → ejecución → respuesta. La integración de HTTP API con formato 2.0 transforma la petición en un evento JSON (versión, ruta, headers, requestContext, body). Lambda ejecuta lambda_handler(event, context) y nuestro código devuelve statusCode, headers y body, que API Gateway traduce a una respuesta HTTP. Lambda no es FastAPI: no arrancamos uvicorn. El diagrama oficial muestra la vida de un entorno: INIT (extensiones, runtime y código fuera del handler), varias INVOKE en el mismo entorno y SHUTDOWN cuando Lambda lo retira. Estado efímero: lo creado fuera del handler puede reutilizarse (cliente del SDK, conexiones), pero no es persistencia.
CONSOLA: Lambda › (función de ejemplo, si existe) › pestaña Test: enseñar el formulario de evento de prueba sin pulsar Test (invocar ejecutaría la función y podría llamar a Bedrock). Si no hay función, describir con el diagrama.
PREGUNTA: «Si guardo un contador en una variable global, ¿cuenta todas las peticiones?». Respuesta: no; cada entorno tiene el suyo y puede desaparecer.
FUENTES: AWS Lambda Developer Guide, «Lambda execution environment» (lambda-runtime-environment.html) y «Define Lambda function handler in Python», consultadas el 06/11/2026; src/curso_ia/serverless/handler.py y bedrock.py (client_for con lru_cache).
IMÁGENES: diagrama oficial Overview-Successful-Invokes.png de la AWS Lambda Developer Guide (docs.aws.amazon.com), sin modificar. """ + SRC_AWS_ICONS)
    return sl


def s08_mapa(d):
    sl = d.slide(tag="mapa")
    header(sl, "El mapa de la sesión", "El recorrido de una petición en S17",
           "Cada bloque explica una parte de este diagrama. Al final podremos seguir una petición de izquierda a derecha y "
           "decir qué servicio interviene, qué permiso necesita y dónde queda registrada.")
    # cliente
    img(sl, "g-user.png", 58, 222, w=40, h=40)
    text(sl, 43, 264, 72, 40, "Cliente con\ncredenciales\ntemporales", size=8.5, color=TEXT, align="c")
    chip(sl, 47, 312, 64, 16, "firma SigV4", fill=VIOLET_BG, color=VIOLET, size=8, line=VIOLET)
    # nube
    box(sl, 128, 132, 600, 334, fill=None, line="AAB7BD", lw=0.75, radius=0)
    img(sl, "grp-cloud.png", 128, 132, w=20, h=20)
    text(sl, 153, 136, 300, 12, "AWS Cloud · cuenta del laboratorio", size=9, color=TITLE, bold=True)
    img(sl, "aws-iam.png", 153, 158, w=28, h=28)
    text(sl, 188, 160, 260, 26, [[("IAM (global)  ", {"bold": True, "color": TITLE}),
                                   ("permisos de las tres flechas", {})]], size=9, color=TEXT)
    badge(sl, 372, 164, 4, fill=VIOLET)
    box(sl, 146, 196, 568, 260, fill=None, line="00A4A6", lw=1, radius=0, dash=True)
    img(sl, "grp-region.png", 146, 196, w=18, h=18)
    text(sl, 169, 199, 300, 12, "Región de origen eu-west-1 · Europa (Irlanda)", size=9, color="5FD0D2", bold=True)
    nodes = [(158, "aws-apigw.png", "API Gateway", "HTTP API\nPOST /clasificar\nauth: AWS_IAM", AMBER, 3),
             (338, "aws-lambda.png", "Lambda", "alias aula\nPython 3.12 · 512 MB\ntimeout 24 s", AMBER, 3),
             (518, "aws-bedrock.png", "Bedrock", "eu.amazon.nova-2-\nlite-v1:0\nmaxTokens 300", PINK, 2)]
    for x, ic, t, sub, col, b in nodes:
        box(sl, x, 230, 156, 92, fill=CARD, line=col)
        img(sl, ic, x + 9, 242, w=32, h=32)
        text(sl, x + 48, 240, 104, 15, t, size=11.5, color=TITLE, bold=True)
        text(sl, x + 48, 258, 106, 60, sub, size=8.5, color=TEXT)
        badge(sl, x + 140, 222, b, fill=col)
    line(sl, 112, 252, 156, 252, color=MINT, w=1.5)
    line(sl, 315, 266, 336, 266, color=MINT, w=1.5)
    line(sl, 495, 266, 516, 266, color=MINT, w=1.5)
    line(sl, 156, 300, 112, 300, color=MINT_L, w=1.25, dash=True)
    text(sl, 113, 303, 44, 11, "respuesta", size=7.5, color=MINT_L, align="c", check=False)
    perms = [(127, 234, "1"), (319, 276, "2"), (499, 276, "3")]
    for x, y, n in perms:
        circle(sl, x, y, 14, VIOLET)
        text(sl, x, y + 1.5, 14, 12, n, size=8, color=DARK, bold=True, align="c", check=False)
    # CloudWatch
    box(sl, 338, 362, 156, 76, fill=CARD, line=VIOLET)
    img(sl, "aws-cloudwatch.png", 347, 374, w=32, h=32)
    text(sl, 386, 372, 104, 15, "CloudWatch", size=11.5, color=TITLE, bold=True)
    text(sl, 386, 390, 106, 44, "log group, REPORT\nmétricas y alarmas", size=8.5, color=TEXT)
    badge(sl, 478, 354, 4, fill=VIOLET)
    line(sl, 416, 323, 416, 360, color=VIOLET, w=1.25, dash=True)
    # leyenda permisos
    text(sl, 162, 360, 170, 90, [{"runs": [("PERMISOS (bloque 4)", {"bold": True, "color": VIOLET, "size": 8.5})], "space": 3},
                                 {"runs": [("1 ", {"bold": True, "color": VIOLET}), ("execute-api:Invoke", {})], "space": 2},
                                 {"runs": [("2 ", {"bold": True, "color": VIOLET}), ("lambda:InvokeFunction", {})], "space": 2},
                                 {"runs": [("3 ", {"bold": True, "color": VIOLET}), ("bedrock:InvokeModel", {})], "space": 2}],
         size=9, font=MONO, color=TEXT)
    # destinos
    box(sl, 746, 196, 171, 270, fill=PINK_BG, line="6B3A5A")
    text(sl, 756, 204, 155, 26, "REGIONES DE DESTINO\nDEL PERFIL EU · bloque 2", size=8.5, color=PINK, bold=True)
    regs = [("eu-central-1", "Fráncfort"), ("eu-north-1", "Estocolmo"), ("eu-south-1", "Milán"),
            ("eu-south-2", "España"), ("eu-west-1", "Irlanda"), ("eu-west-3", "París")]
    y = 238
    for code, name in regs:
        img(sl, "grp-region.png", 756, y + 1, w=14, h=14)
        text(sl, 776, y, 140, 13, [[(code + "  ", {"font": MONO, "bold": True, "color": TITLE}), (name, {})]], size=8.5, color=TEXT)
        y += 22
    text(sl, 756, 378, 155, 80, "Bedrock puede procesar la petición en cualquiera de ellas. La respuesta no indica en cuál.",
         size=8.5, color=TITLE)
    line(sl, 675, 276, 744, 276, color=PINK, w=1.25, dash=True)
    takeaway(sl, "Cliente → API Gateway → Lambda → Bedrock → respuesta. IAM decide quién invoca cada pieza; CloudWatch deja el rastro.",
             "Idea guía")
    footer(sl, block=1)
    notes(sl, """
""" + timing_note("18:43", "18:45") + """
QUÉ EXPLICAR: el mapa completo. 1) El cliente firma la petición con credenciales temporales (SigV4) y la envía por HTTPS. 2) API Gateway (HTTP API) recibe POST /clasificar, comprueba la autorización IAM y la integra con el alias aula de Lambda. 3) Lambda valida la entrada y hace una sola llamada Converse a Bedrock con el perfil eu.amazon.nova-2-lite-v1:0. 4) Bedrock procesa en una de las seis regiones de destino del perfil europeo. 5) La respuesta vuelve por el mismo camino. IAM interviene en tres flechas distintas (execute-api:Invoke, lambda:InvokeFunction y bedrock:InvokeModel) y CloudWatch recibe los logs y el REPORT de cada invocación. Las insignias numeradas indican el bloque donde se explica cada pieza.
VALORES: son los de la referencia S17 (plantilla infra/s17/servicio.json): Python 3.12, 512 MB, 24 s, alias aula, ruta con AWS_IAM. Son decisiones del ejemplo.
CONSOLA: ninguna en esta diapositiva; a partir del bloque 2 abrimos cada servicio.
PREGUNTA: «¿Qué pieza devuelve un 403 si el cliente no firma la petición?». Respuesta: API Gateway, antes de Lambda.
FUENTES: infra/s17/servicio.json y src/curso_ia/serverless/*.py; ficha «Nova 2 Lite» de la Amazon Bedrock User Guide (destinos del perfil EU desde eu-west-1: eu-central-1, eu-north-1, eu-south-1, eu-south-2, eu-west-1 y eu-west-3), consultada el 06/11/2026.
IMÁGENES: """ + SRC_AWS_ICONS + " Grupos AWS Cloud y Region del mismo paquete. Diagrama propio.")
    return sl


PART1 = [s01_portada, s02_encuesta, s03_caso, s04_div1, s05_comparacion, s06_responsabilidades, s07_ciclo, s08_mapa]
