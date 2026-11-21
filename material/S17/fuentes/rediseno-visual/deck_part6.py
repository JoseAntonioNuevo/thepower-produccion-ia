"""Diapositivas 42–49: bloque 7 (evidencias, práctica opcional y cierre) y anexos de consulta."""
from deck_lib import *  # noqa: F401,F403
from deck_part1 import SRC_AWS_ICONS
from deck_part3 import SRC_TEMPLATE


def s41_div7(d):
    sl = divider(d, 7, "Práctica y cierre", "Qué demuestra cada evidencia y cómo seguir por tu cuenta",
                 "Preparación local, configuración, simulación y ejecución real; la práctica opcional y lo que nos llevamos.",
                 ["¿Qué prueba una demo local y qué no prueba?",
                  "¿Qué incluye la práctica opcional?",
                  "¿Qué nos llevamos de la sesión?"],
                 [("g-document.png", "Evidencias"), ("r-lambda-fn.png", "Práctica\nopcional"), ("g-user.png", "Preguntas")],
                 "19:50–20:00 · 10 min")
    notes(sl, """
TIEMPO 19:50 (10 s). Bloque 7 de 7: práctica y cierre, de 19:50 a 20:00 (10 min).
QUÉ EXPLICAR: cerramos distinguiendo evidencias, presentando la práctica opcional y respondiendo preguntas.
CONSOLA: ninguna en el separador.
PREGUNTA: «¿Qué evidencia necesitaríais para afirmar que la API funciona en AWS?»
FUENTES: temario AI Engineer y guion de S17 (material/S17/guion-profesor.md), con la distribución de tiempos de esta versión.
IMÁGENES: """ + SRC_AWS_ICONS + " Genéricos Document y User; recurso Lambda Function.")
    return sl


def s42_evidencias(d):
    sl = d.slide(tag="evidencias")
    header(sl, "Evidencias", "Preparación, configuración, simulación y ejecución real",
           "Cada evidencia demuestra algo distinto. Hoy hemos visto configuración y código; ningún despliegue ni inferencia "
           "se presenta como ejecutado.")
    levels = [("1", "Preparación local", "Verificada el 17/10/2026",
               "45 pruebas correctas, plantillas validadas con cfn-lint y ZIP Linux amd64 construido.",
               "Código y configuración coherentes.", "Despliegue, permisos efectivos e inferencia.", MINT),
              ("2", "Configuración visible", "Hoy, en la consola",
               "Pantallas y formularios abiertos y cancelados; capturas oficiales y esquemas rotulados.",
               "Qué se configuraría y dónde.", "Que exista un recurso o que funcione.", BLUE),
              ("3", "Simulación", "demo_s17 y RIE",
               "execution: demo y tokens nulos; RIE ejecuta el contrato del runtime Lambda en local.",
               "Contrato, validación y errores.", "Firma aceptada, IAM, latencia y coste reales.", AMBER),
              ("4", "Ejecución real en AWS", "Pendiente del ensayo",
               "Petición firmada aceptada, inferencia, REPORT unido por request ID y retirada con inventario.",
               "Que el sistema funciona en AWS.", "Sin ella no hablamos de resultados reales.", CORAL)]
    y = 132
    for n, t, when, what, yes, no, col in levels:
        box(sl, 43, y, 874, 78, fill=CARD)
        box(sl, 43, y, 4, 78, fill=col, radius=0)
        circle(sl, 57, y + 10, 26, col)
        text(sl, 57, y + 15, 26, 16, n, size=12, color=DARK, bold=True, align="c", check=False)
        text(sl, 93, y + 9, 230, 16, t, size=12, color=TITLE, bold=True)
        text(sl, 93, y + 27, 230, 13, when, size=9, color=col, bold=True)
        text(sl, 93, y + 43, 300, 34, what, size=9, color=TEXT)
        text(sl, 405, y + 9, 250, 12, "DEMUESTRA", size=8, color=MINT, bold=True)
        text(sl, 405, y + 24, 250, 50, yes, size=10, color=TITLE)
        text(sl, 665, y + 9, 245, 12, "NO DEMUESTRA", size=8, color=CORAL, bold=True)
        text(sl, 665, y + 24, 245, 50, no, size=10, color=TITLE)
        y += 84
    takeaway(sl, "Una simulación local no demuestra autorización IAM ni inferencia real. Las mediciones solo se presentan con su evidencia.",
             "Idea guía")
    footer(sl, block=7)
    notes(sl, """
""" + timing_note("19:50", "19:52") + """
QUÉ EXPLICAR: cuatro niveles de evidencia. 1) Preparación local (17/10/2026): 45 pruebas del repositorio, cuatro plantillas validadas con cfn-lint, petición Converse validada contra el SDK con Stubber y ZIP Linux amd64 construido con la imagen oficial; no acredita despliegue ni inferencia. 2) Configuración visible: lo que hemos visto hoy en la consola, sin guardar, y los esquemas rotulados. 3) Simulación: scripts/demo_s17.py (execution: demo, tokens nulos) y el emulador RIE (contrato del runtime en local); la firma generada en local tampoco prueba que IAM la acepte. 4) Ejecución real: petición firmada aceptada, inferencia real, REPORT unido por request ID, coste interpretado y retirada; queda pendiente del ensayo en la cuenta del laboratorio, con permiso y presupuesto. No presentar recibos anteriores como ejecución del día.
CONSOLA: ninguna.
PREGUNTA: «La demo local devuelve 200. ¿Podemos decir que la API funciona en AWS?». Respuesta: no; demuestra el contrato, no IAM, Bedrock real ni el despliegue.
FUENTES: material/S17/verificacion.md (preparación del 17/10/2026: 45 pruebas, cfn-lint, Stubber, ZIP y RIE; pendientes cloud), README.md y guia-alumno.md (tres evidencias distintas).
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


def s43_practica(d):
    sl = d.slide(tag="practica")
    header(sl, "Práctica opcional", "Práctica opcional: una API de IA serverless con Bedrock",
           "Los ejercicios de estas sesiones no son obligatorios, según confirmó Laura el 4 de noviembre. Si decides hacerla, "
           "este es el recorrido y lo que debería contener la entrega.")
    chip(sl, 829, 40, 88, 22, "OPCIONAL", fill=AMBER, color=DARK, size=11)
    box(sl, 43, 130, 430, 92, fill=CARD, line=BORDER)
    text(sl, 55, 137, 410, 12, "ENCARGO DE EJERCICIOS DE LAURA · 10 DE AGOSTO", size=8.5, color=MINT, bold=True)
    text(sl, 55, 153, 410, 20, "«Sesión 17 Serverless AI: AWS Bedrock.»", size=12.5, font=SERIF, color=TITLE, italic=True)
    text(sl, 55, 178, 410, 42, "HTTP API con IAM, firma SigV4, JSON validado y mediciones son concreciones del enunciado "
                               "que redactó José (28/09/2026), no del encargo.", size=9.5, color=MUTED)
    box(sl, 485, 130, 432, 92, fill=CARD, line=BORDER)
    info = [("Dedicación", "4–6 horas con cuenta, permisos y accesos preparados."),
            ("Punto de partida", "S17-inicio.zip; S17-referencia.zip como consulta."),
            ("Ayuda", "Guía del alumno: pasos, comandos y errores esperados.")]
    yy = 138
    for t, b in info:
        text(sl, 497, yy, 410, 26, [[(t + "  ", {"bold": True, "color": MINT_L}), (b, {})]], size=10, color=TEXT)
        yy += 27
    steps = [("HTTP API con IAM", "Ruta POST con AWS_IAM."),
             ("Lambda", "Valida e invoca Bedrock."),
             ("Petición firmada", "SigV4 con credenciales temporales."),
             ("JSON validado", "Estructura pedida y comprobada."),
             ("Errores controlados", "Sin reintentos ocultos."),
             ("Medidas", "≥ 5 calientes y frío acreditado o «no capturado»."),
             ("1.000 solicitudes", "Estimación sin ejecutarlas."),
             ("Limpieza", "Retirada documentada.")]
    w = (874 - 7 * 6) / 8
    for i, (t, b) in enumerate(steps):
        x = 43 + i * (w + 6)
        box(sl, x, 232, w, 112, fill=CARD)
        badge(sl, x + 8, 240, i + 1, fill=AMBER if i < 5 else BLUE, d=20, size=10)
        text(sl, x + 8, 266, w - 14, 30, t, size=10, color=TITLE, bold=True)
        text(sl, x + 8, 298, w - 14, 44, b, size=8.5, color=TEXT)
    box(sl, 43, 354, 520, 112, fill=CARD)
    text(sl, 55, 362, 400, 12, "SI LA HACES, LA ENTREGA INCLUYE", size=9, color=MINT, bold=True)
    ent = ["Código y configuración reproducibles, sin credenciales.",
           "Una petición válida y los errores controlados.",
           "Medidas con su evidencia (REPORT y request ID) y su análisis.",
           "Coste de 1.000 solicitudes con región, fecha, tarifas y supuestos; limpieza."]
    bullets(sl, 55, 380, 500, 84, ent, size=10, space=3)
    box(sl, 575, 354, 342, 112, fill=CORAL_BG)
    text(sl, 587, 362, 320, 12, "ANTES DE EMPEZAR", size=9, color=CORAL, bold=True)
    text(sl, 587, 380, 322, 84, "Crea recursos facturables y consume inferencias. Usa la cuenta del laboratorio, un presupuesto, "
                                "credenciales temporales y la retirada al terminar. La demo local no sustituye la evidencia real.",
         size=10, color=TITLE)
    takeaway(sl, "Si la haces, la prueba es una petición firmada aceptada, su REPORT y el inventario de lo retirado; no una demo local.",
             "Idea guía")
    footer(sl, block=7)
    notes(sl, """
""" + timing_note("19:52", "19:54") + """
QUÉ EXPLICAR: la práctica es OPCIONAL (Laura, 04/11/2026: los ejercicios de estas sesiones no son obligatorios; conviene explicar la teoría con aplicaciones prácticas y que los alumnos entiendan los pasos). Distinguir el encargo general de Laura del 10/08 («Sesión 17 Serverless AI: AWS Bedrock.») de las decisiones concretas que José incorporó al enunciado del 28/09: API Gateway HTTP API, autorización IAM, SigV4, salida JSON validada y mediciones. Para quien la haga: HTTP API con IAM; Lambda que valida e invoca Bedrock; petición firmada; JSON validado; errores controlados; medidas y análisis (al menos cinco peticiones calientes y un cold start acreditado, o declarar que no se capturó); estimación de 1.000 solicitudes sin ejecutarlas; limpieza documentada. Dedicación orientativa de 4–6 horas con accesos preparados, fuera del directo. Streaming es una ampliación opcional y la referencia no lo implementa.
CONSOLA: ninguna.
AVISO: hoy no hemos desplegado nada. La práctica crea recursos y consume inferencias: solo con la cuenta, permisos y presupuesto del laboratorio. No presentar ensayos anteriores como ejecución de hoy.
PREGUNTA: «¿Qué falta si solo tengo la demo local en verde?». Respuesta: la petición firmada aceptada, la inferencia real, el REPORT y la limpieza.
FUENTES: material/S17/enunciado.md y guia-alumno.md; docs/fuentes/S17-ejercicio-original.txt (enunciado de José, enviado el 28/09/2026, página 6 de AI_Engineer_enunciados.docx); correos de Laura del 10/08/2026 (encargo de ejercicios) y del 04/11/2026 (ejercicios no obligatorios). El enunciado.md antiguo dice «Trabajo obligatorio»: esta presentación lo corrige a práctica opcional.
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


def s44_cierre(d):
    sl = d.slide(BG_SECTION, tag="cierre")
    img(sl, "thepower-logo.png", 38, 34, h=30)
    text(sl, 43, 84, 300, 14, "CIERRE", size=10, color=MINT, bold=True)
    text(sl, 43, 102, 520, 44, "Lo que nos llevamos", size=32, font=SERIF, color=TITLE)
    pts = ["Serverless traslada los servidores a AWS; código, permisos, límites y coste siguen siendo nuestros.",
           "API Gateway recibe, autoriza e integra; Lambda ejecuta y valida; Bedrock da acceso al modelo.",
           "Tres permisos: cliente → ruta, API → función, función → modelo. Firmar no es estar autorizado.",
           "El perfil eu. acota la geografía: hay que leer y autorizar sus regiones de destino.",
           "Un cold start se acredita con Init Duration; los relojes se superponen; cada capa tiene su timeout.",
           "En el ejemplo, los tokens dominan el coste; los supuestos se declaran y las medidas se identifican."]
    y = 158
    for i, p in enumerate(pts):
        circle(sl, 43, y, 22, MINT_L)
        text(sl, 43, y + 3, 22, 16, str(i + 1), size=10.5, color=DARK, bold=True, align="c", check=False)
        text(sl, 76, y + 1, 470, 44, p, size=12, color=TITLE)
        y += 50
    box(sl, 584, 130, 333, 336, fill="1A463C", radius=8)
    text(sl, 604, 146, 300, 40, "¿Preguntas?", size=30, font=SERIF, color=MINT_L)
    text(sl, 604, 198, 300, 12, "PARA COMPROBAR", size=9, color=MINT, bold=True)
    qs = ["¿Qué acción IAM necesita Converse?", "¿Qué demuestra que una llamada fue fría?",
          "¿Por qué 24 s de Lambda no permiten una tarea de minutos detrás de esta HTTP API?"]
    bullets(sl, 604, 216, 300, 96, qs, size=10.5, color=TITLE, mark_color=MINT, space=4)
    text(sl, 604, 322, 300, 12, "PRÓXIMA SESIÓN · S18", size=9, color=MINT, bold=True)
    text(sl, 604, 338, 300, 40, "CI/CD y monitorización en producción: una API que devuelve JSON aún necesita pruebas y entrega verificable.",
         size=10.5, color=TITLE)
    text(sl, 604, 388, 300, 12, "MATERIALES DE S17", size=9, color=MINT, bold=True)
    text(sl, 604, 404, 300, 56, "Presentación, guía del alumno, enunciado de la práctica opcional y paquetes S17-inicio y "
                                "S17-referencia.", size=10.5, color=TITLE)
    notes(sl, """
""" + timing_note("19:54", "20:00", ": dos de recapitulación y cuatro de preguntas") + """
QUÉ EXPLICAR: leer los seis puntos y pedir a un alumno que recorra en voz alta el mapa «El recorrido de una petición en S17» nombrando cada servicio, cada permiso y dónde queda el rastro.
RECUPERACIÓN ACTIVA (respuestas): «¿Qué acción IAM necesita Converse?» → bedrock:InvokeModel. «¿Qué demuestra que una llamada fue fría?» → Init Duration en el REPORT de ese RequestId, no su posición en la tabla. «¿Por qué 24 s de Lambda no permiten una tarea de minutos detrás de esta HTTP API?» → la integración tiene un máximo de 30 s; hay que cambiar a un patrón asíncrono.
SI NADIE PREGUNTA: «La llamada firmada devuelve 403» (credenciales temporales, región, servicio execute-api, permiso de la ruta) y «La función responde 502 bedrock_denegado» (rol de Lambda, perfil y destinos).
CONSOLA: cerrar las pestañas de la consola sin guardar cambios.
CONEXIÓN CON S18: CI/CD y monitorización en producción (temario): pruebas automáticas, entornos, variables y secretos, observabilidad.
CERRAR a las 20:00. No hay recursos que retirar: hoy no se ha creado nada en AWS.
FUENTES: guion de S17; temario AI Engineer (S18: CI/CD + Monitorización en producción).
IMÁGENES: logotipo de thePower (recurso original del curso).""")
    return sl


def consulta_header(sl, title, sub):
    header(sl, "Consulta", title, sub)


def s45_ruta(d):
    sl = d.slide(tag="consulta-ruta")
    consulta_header(sl, "Consulta · recorrido por la consola",
                    "Ruta, campos que conviene señalar y qué determina el coste de cada servicio de la sesión. Útil para repasar o "
                    "repetir el recorrido sin crear recursos.")
    rows = [["Servicio", "Ruta en la consola", "Qué señalar", "Qué determina el coste"],
            ["Bedrock", "Bedrock › Model catalog · Cross-Region inference · Playgrounds › Chat / Text",
             "Model ID, modalidades, contexto, perfiles y destinos, parámetros", "Tokens de entrada y salida según modelo, región y nivel"],
            ["Lambda", "Lambda › Event functions › (función) › Code · Configuration · Monitor · Aliases",
             "Handler, memoria, timeout, variables, rol, concurrencia, alias", "Solicitudes y GB-s (incluida la fase INIT)"],
            ["API Gateway", "API Gateway › APIs › (HTTP API) › Routes · Authorization · Integrations · Stages",
             "POST /clasificar, IAM, payload 2.0, 29.000 ms, $default, throttling", "Solicitudes de HTTP API"],
            ["IAM", "IAM › Roles › (rol de la función) › Permissions",
             "bedrock:InvokeModel sobre perfil y modelos; logs; política execute-api del cliente", "Sin cargo"],
            ["CloudWatch", "CloudWatch › Logs › Log groups · Metrics · Alarms",
             "RequestId, REPORT, Init Duration, Errors, Throttles", "GB ingeridos y almacenados; métricas y alarmas"],
            ["S3", "S3 › (bucket del artefacto) › Objects › Versions", "ZIP, checksum y versiones del objeto", "GB-mes y solicitudes"],
            ["CloudFormation", "CloudFormation › Stacks › (stack) › Resources", "Inventario creado y retirado",
             "Sin cargo propio; los recursos sí"]]
    table(sl, 43, 134, 874, [100, 300, 260, 214], rows, size=8.5, row_h=40, bold_cols=(0, 1), colors={0: TITLE, 1: MINT_L},
          font_cols={1: MONO})
    footer(sl)
    notes(sl, """
CONSULTA (no se proyecta en el directo salvo que se pida).
QUÉ CONTIENE: la ruta de consola de cada servicio de la sesión, los campos que conviene señalar y qué determina su coste. Sirve para repasar o repetir el recorrido sin crear recursos.
FUENTES: las mismas de las diapositivas de cada bloque (Amazon Bedrock User Guide, AWS Lambda Developer Guide, API Gateway Developer Guide, Amazon CloudWatch User Guide, consultadas el 06/11/2026) y la plantilla infra/s17/servicio.json.
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


def s46_politica(d):
    sl = d.slide(tag="consulta-politica")
    consulta_header(sl, "Consulta · política del rol de Lambda para el perfil europeo",
                    "Dos statements: el perfil de inferencia y el modelo base en la región de origen y en todos los destinos, "
                    "condicionado al perfil. La política del cliente es independiente.")
    box(sl, 43, 132, 560, 334, fill=CARD, line=BORDER)
    text(sl, 55, 140, 540, 12, "ROL DE EJECUCIÓN · extracto (cuenta y ARN abreviados)", size=8.5, color=VIOLET, bold=True)
    code = ['{"Statement": [',
            ' {"Effect": "Allow", "Action": "bedrock:InvokeModel",',
            '  "Resource": "arn:aws:bedrock:eu-west-1:<cuenta>:',
            '     inference-profile/eu.amazon.nova-2-lite-v1:0"},',
            ' {"Effect": "Allow", "Action": "bedrock:InvokeModel",',
            '  "Resource": [',
            '   "arn:aws:bedrock:eu-central-1::foundation-model/',
            '      amazon.nova-2-lite-v1:0", … (una por región:',
            '    eu-north-1, eu-south-1, eu-south-2,',
            '    eu-west-1, eu-west-3)],',
            '  "Condition": {"StringEquals": {',
            '   "bedrock:InferenceProfileArn": "<ARN del perfil>"}}}]}']
    p = code_block(sl, 75, 158, 520, code, size=9, pitch=13.5)
    for li, n in [(1, 1), (4, 2), (10, 3)]:
        line_badge(sl, 55, 158, p, li, n, VIOLET)
    text(sl, 55, 330, 536, 132, [{"runs": [("1 ", {"bold": True, "color": VIOLET}), ("El perfil concreto, en la región de origen.", {})], "space": 3},
                                 {"runs": [("2 ", {"bold": True, "color": VIOLET}), ("El modelo base en origen y destinos, leídos con GetInferenceProfile; nunca Resource: * para todos los modelos.", {})], "space": 3},
                                 {"runs": [("3 ", {"bold": True, "color": VIOLET}), ("La condición limita ese permiso a las llamadas que pasan por el perfil.", {})], "space": 3},
                                 {"runs": [("Además: logs:CreateLogStream y logs:PutLogEvents en su log group. Las denegaciones de la cuenta (SCP) prevalecen sobre un Allow.", {})], "space": 3}],
         size=9.5, color=TEXT, space=3)
    box(sl, 617, 132, 300, 160, fill=CARD, line=BORDER)
    text(sl, 629, 140, 280, 12, "IDENTIDAD DEL CLIENTE · extracto", size=8.5, color=AMBER, bold=True)
    code2 = ['{"Effect": "Allow",', ' "Action": "execute-api:Invoke",', ' "Resource": "arn:aws:execute-api:',
             '   eu-west-1:<cuenta>:<api-id>/',
             '   $default/POST/clasificar"}']
    code_block(sl, 629, 158, 280, code2, size=9, pitch=13.5)
    text(sl, 629, 232, 280, 56, "La genera scripts.aws_s17 politica-cliente; la asigna el administrador del laboratorio.",
         size=9.5, color=TEXT)
    box(sl, 617, 302, 300, 164, fill=VIOLET_BG)
    text(sl, 629, 310, 280, 150, [{"runs": [("No usar  ", {"bold": True, "color": CORAL}), ("bedrock:Converse: la acción que autoriza Converse es bedrock:InvokeModel.", {})], "space": 5},
                                  {"runs": [("Streaming  ", {"bold": True, "color": VIOLET}), ("ConverseStream requeriría bedrock:InvokeModelWithResponseStream; la referencia no lo usa.", {})], "space": 5},
                                  {"runs": [("Perfil global  ", {"bold": True, "color": VIOLET}), ("tendría otros recursos y destinos: no se sustituye sin justificarlo.", {})], "space": 5}],
         size=9.5, color=TITLE, space=5)
    footer(sl)
    notes(sl, """
CONSULTA. Extracto de las políticas de la referencia. El primer statement autoriza el perfil concreto en la región de origen. El segundo autoriza el modelo base en origen y destinos (eu-central-1, eu-north-1, eu-south-1, eu-south-2, eu-west-1 y eu-west-3 según la ficha consultada el 06/11/2026; la referencia los lee con GetInferenceProfile en el preflight), con la condición bedrock:InferenceProfileArn. No usar bedrock:Converse ni Resource: * para modelos. Las denegaciones de la cuenta u organización pueden prevalecer sobre un Allow específico. La política execute-api del cliente es independiente y la asigna el administrador del laboratorio.
FUENTES: Amazon Bedrock User Guide, «Geographic cross-Region inference» (IAM policy requirements y ejemplo de dos statements) y «Using the Converse API», consultadas el 06/11/2026; infra/s17/servicio.json y scripts/aws_s17.py (preflight y politica-cliente).
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


def s47_empaquetado(d):
    sl = d.slide(tag="consulta-empaquetado")
    consulta_header(sl, "Consulta · empaquetado, versiones y comandos del laboratorio",
                    "Cómo llega el código a Lambda en la referencia y qué comandos solo leen o cambian recursos. Todo esto se "
                    "hace fuera del directo.")
    flow = [("g-source-code.png", "Construir", "Imagen oficial Lambda Python 3.12, linux/amd64, dependencias con hashes."),
            ("r-lambda-fn.png", "ZIP", "19.368.078 bytes, 2.373 archivos; SHA-256 0195a544…f073."),
            ("r-s3-bucket.png", "Publicar", "Bucket S3 privado, cifrado y versionado; checksum leído de vuelta."),
            ("aws-lambda.png", "Desplegar", "CloudFormation: función, versión publicada, alias aula, HTTP API, integración y ruta IAM."),
            ("g-magnifier.png", "Comprobar", "estado: CodeSha256 de la versión del alias, configuración y ruta.")]
    w = (874 - 4 * 14) / 5
    for i, (ic, t, b) in enumerate(flow):
        x = 43 + i * (w + 14)
        box(sl, x, 132, w, 120, fill=CARD)
        img(sl, ic, x + 10, 142, w=28, h=28)
        text(sl, x + 46, 148, w - 52, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, x + 10, 178, w - 20, 72, b, size=9, color=TEXT)
        if i < 4:
            line(sl, x + w + 1, 192, x + w + 13, 192, color=MINT, w=1.5)
    rows = [["Comando (uv run python -m scripts.aws_s17 …)", "Qué hace", "¿Cambia recursos o gasta?"],
            ["plan · preflight · estado · logs · politica-cliente", "Leen configuración, cuotas, perfil, estado y logs", "No"],
            ["bootstrap · subir · desplegar", "Crean bucket, publican el ZIP y despliegan el stack", "Sí: recursos facturables"],
            ["medir", "Hasta 6 clasificaciones reales, secuenciales, sin reintentos", "Sí: hasta 6 inferencias"],
            ["verificar", "403 sin firma, 422 firmada inválida, 200 válida", "Sí: 1 inferencia"],
            ["limpiar", "Retira API, función, rol, logs y el bucket propio con sus versiones", "Sí: elimina recursos"]]
    table(sl, 43, 266, 874, [300, 374, 200], rows, size=9, row_h=28, font_cols={0: MONO}, colors={0: MINT_L}, bold_cols=(0,))
    text(sl, 43, 440, 874, 26, [[("Las operaciones que cambian recursos o hacen inferencias exigen ", {}),
                                  ("--execute", {"font": MONO, "bold": True, "color": MINT_L}),
                                  (", perfil, región, cuenta esperada y nombre del laboratorio. Es una barrera del script, no una autorización.", {})]],
         size=9.5, color=AMBER)
    footer(sl)
    notes(sl, """
CONSULTA. Empaquetado: scripts/build_lambda_s17.py usa la imagen oficial de Lambda Python 3.12 fijada por digest, objetivo linux/amd64 y dependencias con hashes; el ZIP verificado el 17/10/2026 mide 19.368.078 bytes comprimidos (30.393.926 descomprimidos, 2.373 archivos) con SHA-256 0195a544766e680610584298d12feb716473e8b7c9d932867e2ad6070f96f073. Publicación en un bucket S3 privado, cifrado y versionado con checksum. Despliegue con CloudFormation: logs, rol, función, versión publicada, alias aula, HTTP API, integración y ruta IAM. Cambiar la configuración con el mismo ZIP también cambia la versión de despliegue. Comandos: los de lectura no cambian recursos; bootstrap, subir y desplegar crean recursos; medir hace hasta seis inferencias; verificar, una; limpiar retira API, Lambda (alias y versiones), rol, logs y el bucket propio con todas sus versiones y delete markers, y conserva identidades compartidas.
FUENTES: material/S17/verificacion.md, guia-alumno.md (secciones 4–8 y 11), paquetes/lambda-manifiesto.json, scripts/aws_s17.py y build_lambda_s17.py.
IMÁGENES: """ + SRC_AWS_ICONS + " Recurso S3 Bucket y Lambda Function; genéricos Source Code y Magnifying Glass.")
    return sl


def s48_fuentes(d):
    sl = d.slide(tag="consulta-fuentes")
    consulta_header(sl, "Consulta · fuentes y procedencia de las imágenes",
                    "Documentación oficial consultada el 06/11/2026, materiales del curso y recursos gráficos. Las pantallas "
                    "rotuladas como ESQUEMA son dibujos propios, no capturas.")
    left = [("Temario y encargos", "Temario AI Engineer (texto de Laura sobre S17); encargo de ejercicios del 10/08/2026; correo de Laura del 04/11/2026."),
            ("Enunciado", "Ejercicio S17 redactado por José (28/09/2026): docs/fuentes/S17-ejercicio-original.txt."),
            ("Amazon Bedrock", "User Guide: ficha «Nova 2 Lite», «Supported Regions and models for inference profiles», «Geographic cross-Region inference», «Using the Converse API», «Custom Model Import»."),
            ("AWS Lambda", "Developer Guide: «What is AWS Lambda?», «Lambda execution environment», «Lambda concurrency», «Lambda quotas», configuración, versiones y alias; Compute Blog sobre la facturación de INIT."),
            ("API Gateway", "Developer Guide: «Choose between REST APIs and HTTP APIs», cuotas de HTTP API y de cuenta, IAM, throttling, integración Lambda 2.0."),
            ("Precios", "Lista pública de precios de AWS para eu-west-1 (tarifas del 17/10/2026, sin cambios el 06/11/2026)."),
            ("Otras nubes", "Microsoft Learn (Bedrock ↔ Foundry); Google Cloud (comparativa de servicios; Gemini Enterprise Agent Platform).")]
    y = 134
    for t, b in left:
        text(sl, 43, y, 520, 44, [[(t + "  ", {"bold": True, "color": MINT_L}), (b, {})]], size=10, color=TEXT)
        y += 47
    box(sl, 577, 134, 340, 332, fill=CARD)
    text(sl, 589, 142, 320, 12, "IMÁGENES", size=9, color=BLUE, bold=True)
    imgs = ["Iconos AWS Architecture Icons, paquete del 31/07/2026 (aws.amazon.com/architecture/icons).",
            "Azure Public Service Icons V25 y Microsoft Entra architecture icons.",
            "Google Cloud: core products y legacy icons (cloud.google.com/icons); logotipo de gstatic.com.",
            "Diagramas y capturas oficiales de la AWS Lambda Developer Guide y de la API Gateway Developer Guide, recortados sin alterar.",
            "QR de AI Engineer de S16 (19/10/2026), byte a byte; logotipo de thePower del curso.",
            "Pantallas rotuladas como ESQUEMA: dibujos propios."]
    bullets(sl, 589, 162, 318, 300, imgs, size=10, mark_color=BLUE, space=6)
    footer(sl)
    notes(sl, """
CONSULTA. Fuentes técnicas y gráficas. La documentación oficial informa el diseño, pero no acredita el acceso, la cuota ni los permisos de la cuenta del curso. Tarifas y modelos deben comprobarse de nuevo antes de cada uso; la disponibilidad de un modelo en la documentación no demuestra acceso real.
FUENTES DETALLADAS: material/S17/fuentes.md y fuentes/rediseno-visual/README.md (procedencia de cada imagen y comandos de regeneración).
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


PART6 = [s41_div7, s42_evidencias, s43_practica, s44_cierre, s45_ruta, s46_politica, s47_empaquetado, s48_fuentes]
