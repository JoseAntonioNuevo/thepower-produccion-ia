"""Diapositivas 1–18: apertura, bloque 1 (CI/CD y entornos) y bloque 2 (GitHub Actions)."""
from deck_lib import *  # noqa: F401,F403

SRC_AWS = ("Iconos de AWS: AWS Architecture Icons, paquete oficial del 31/07/2026 "
           "(aws.amazon.com/architecture/icons).")
SRC_GH = "Logotipos de GitHub, GitHub Actions, OpenTelemetry y Python: github/explore (repositorio oficial de GitHub)."


def s01_portada(d):
    sl = d.slide(BG_SECTION, "portada")
    img(sl, "thepower-logo.png", 38, 34, h=32)
    text(sl, 43, 104, 420, 14, "S18 · AI ENGINEER", size=10, color=MINT, bold=True)
    text(sl, 43, 124, 450, 92, "CI/CD y monitorización\nen producción", size=36, font=SERIF, color=TITLE)
    text(sl, 43, 226, 425, 78,
         "Llevamos la API de IA de S16 a staging con las garantías de cualquier software: tests en cada "
         "cambio, el mismo artefacto en cada entorno, logs que explican un fallo y vuelta atrás comprobada.",
         size=12.5, color=TEXT)
    text(sl, 43, 322, 420, 16, "José Antonio Nuevo", size=12.5, color=TITLE, bold=True)
    text(sl, 43, 342, 440, 32, "Miércoles 25 de noviembre de 2026 · grupo L/X\n18:30–20:00 · hora de Madrid",
         size=10.5, color=MUTED)
    box(sl, 497, 52, 420, 410, fill=BG, line="2A5246", radius=8)
    img(sl, "github-mark-white.png", 515, 70, h=34)
    img(sl, "aws-logo-dark.png", 559, 70, h=34)
    text(sl, 515, 116, 380, 14, "HERRAMIENTAS QUE CONECTAMOS EN LA DEMO", size=9, color=MINT, bold=True)
    items = [("gh-actions.png", "GitHub Actions"), ("docker-mark-white.png", "Docker"), ("aws-ecr.png", "ECR"),
             ("aws-fargate.png", "ECS · Fargate"), ("aws-cloudwatch.png", "CloudWatch")]
    for i, (ic, lab) in enumerate(items):
        x = 515 + i * 78
        img(sl, ic, x + 15, 140, w=44, h=44)
        text(sl, x - 4, 188, 82, 14, lab, size=9.5, color=TITLE, align="c", bold=True)
    text(sl, 515, 222, 380, 12, "EL RECORRIDO DE UN CAMBIO", size=9, color=MINT, bold=True)
    flow = ["commit", "tests", "imagen", "staging", "logs"]
    ws = [54, 44, 54, 58, 40]
    x = 515
    for i, (f, w) in enumerate(zip(flow, ws)):
        chip(sl, x, 242, w, 22, f, fill=TAKE_BG, color=MINT_L, size=9.5, line="2A5246")
        if i < len(flow) - 1:
            line(sl, x + w + 2, 253, x + w + 12, 253, color=MINT, w=1.25)
        x += w + 14
    chip(sl, x - 2, 242, 64, 22, "rollback", fill=CORAL_BG, color=CORAL, size=9.5, line="5A3A31")
    rows = [("r-iam-sts.png", "OIDC", "credenciales temporales; ninguna clave guardada en GitHub."),
            ("aws-secrets.png", "Secrets Manager", "la clave del modelo, fuera del código.")]
    y = 280
    for ic, t, b in rows:
        img(sl, ic, 515, y, w=22, h=22)
        text(sl, 545, y + 3, 350, 16, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10.5, color=TEXT)
        y += 30
    box(sl, 515, 350, 384, 94, fill=CARD, radius=6)
    text(sl, 527, 358, 360, 12, "Y TAMBIÉN EXPLICAMOS", size=8.5, color=MUTED, bold=True)
    alts = [("gh-opentelemetry.png", "OpenTelemetry · APM"), ("g-alert.png", "Error tracking"),
            ("aws-backup.png", "Backups"), ("aws-rds.png", "Migraciones de BD")]
    for i, (ic, lab) in enumerate(alts):
        x = 527 + i * 92
        img(sl, ic, x + 28, 376, w=30, h=30)
        text(sl, x - 2, 410, 90, 26, lab, size=8.5, color=TEXT, align="c")
    notes(sl, f"""
18:30–18:31. Presentar el objetivo con el título del temario: «Llevar una aplicación de IA a producción con las mismas garantías de calidad que cualquier sistema de software». No es tener un pipeline, sino poder demostrar tres cosas: que un cambio defectuoso no llega a desplegarse, que lo desplegado es exactamente lo que se probó y que se puede volver a una versión conocida.
Usamos la misma API de soporte de S16 (FastAPI, clasificación de incidencias ficticias) y un entorno de staging en ECS/Fargate. El grupo L/X tuvo la S16 con otro profesor: la demo trae su propia API, no hace falta la de José.
En vivo: nada todavía; terminal en demo-cicd preparada.
Pregunta: «¿Qué tendría que pasar para que os fiarais de desplegar un viernes a las 19:00?».
Fuentes: temario de AI Engineer (correo de la escuela, 17/07/2026); enunciado S18 (ejercicios.docx, 29/09/2026). Imágenes: logotipo de thePower (recurso del curso). {SRC_AWS} {SRC_GH} Docker: logotipo oficial (docker.com, reutilizado de S17).""")
    return sl


def s02_encuesta(d):
    sl = d.slide(tag="encuesta")
    header_simple(sl, "Antes de empezar", "Encuesta de S17 y plan de la sesión")
    img(sl, "qr-ai-engineer.jpg", 390, 149.4, w=180, h=180)
    text(sl, 367.5, 349.9, 225, 41.2, "Encuesta de la sesión anterior ·\nS17 (lunes 23/11)", size=13.5,
         color=TITLE, bold=True, align="c")
    # plan de la sesión (izquierda)
    text(sl, 48, 140, 300, 12, "PLAN DE LA SESIÓN · 18:30–20:00", size=9, color=MINT, bold=True)
    plan = [("18:33", "Punto de partida: CI/CD y monitorización", MUTED),
            ("18:39", "1 · Caso, CI/CD y entornos", MINT), ("18:45", "2 · GitHub Actions y alternativas", AMBER),
            ("19:05", "3 · Artefacto, secretos y OIDC", PINK), ("19:17", "4 · Despliegue a staging", VIOLET),
            ("19:34", "5 · Observabilidad y rollback", BLUE), ("19:50", "6 · Datos y recuperación", CORAL),
            ("19:54", "Práctica opcional y cierre", MINT_L)]
    y = 160
    for hora, nombre, col in plan:
        box(sl, 48, y, 300, 30, fill=CARD, radius=4)
        box(sl, 48, y, 3.5, 30, fill=col, radius=0)
        text(sl, 60, y, 44, 30, hora, size=10.5, color=col, bold=True, anchor="m", font=MONO)
        text(sl, 106, y, 236, 30, nombre, size=11, color=TITLE, anchor="m")
        y += 35
    # qué se valora y cómo trabajamos (derecha)
    text(sl, 622, 140, 290, 12, "QUÉ SESIÓN SE VALORA", size=9, color=MINT, bold=True)
    side_note(sl, 622, 160, 290, 56, "Grupo L/X · directo del 25/11", "S17 del lunes 23/11/2026: Bedrock y Lambda.",
              accent=MINT)
    text(sl, 622, 236, 290, 12, "CÓMO TRABAJAMOS HOY", size=9, color=MINT, bold=True)
    bullets(sl, 622, 256, 290, 150, ["Teoría y cinco demos intercaladas: cada bloque acaba con algo en pantalla.",
                                     "La demo funciona en local con Docker; GitHub y AWS solo si el ensayo está hecho.",
                                     "Ninguna clave ni identificador de cuenta en pantalla.",
                                     "La práctica posterior es opcional."], size=10.5, color=TEXT, space=6)
    footer_simple(sl)
    notes(sl, """
18:31–18:33. El QR evalúa la sesión anterior de este grupo: S17, Serverless AI con Bedrock y Lambda, del lunes 23/11. Dejar un minuto para responder; la escuela insiste en que las respuestas son importantes porque llegan pocas.
Plan de hoy (columna izquierda, con la hora de inicio de cada parte): punto de partida (qué es CI/CD y qué es monitorizar) · 1 caso conductor, CI/CD y entornos · 2 GitHub Actions, la PR que se bloquea y alternativas · 3 artefacto inmutable, secretos y OIDC · 4 despliegue a staging, sin corte y progresivo · 5 observabilidad, error y rollback · 6 migraciones y backups · práctica y cierre. La teoría y la demo se alternan; cada bloque termina con algo en pantalla.
La práctica posterior es opcional (aclaración de Laura del 04/11).
En vivo: no mostrar credenciales ni el archivo .env.
Pregunta: ninguna; tiempo para el QR.
Fuentes: Gmail, hilo «Update Directos Desarrollo Agéntico y AI Engineer»: QR al inicio de todas las clases (29/09), nuevos QR (19/10), insistir en la encuesta (06/10), prácticas opcionales (04/11). Imagen: QR vigente de AI Engineer (material/S16/assets, sin modificar).""")
    return sl


def s03_caso(d):
    sl = d.slide(tag="caso")
    header_simple(sl, "Caso conductor", "La misma API de S16, ahora con garantías",
                  "Entra una incidencia ficticia y salen categoría, prioridad y respuesta. Hoy no cambiamos qué "
                  "hace la API, sino cómo llega a staging y cómo sabemos que funciona.")
    box(sl, 48, 153.8, 852.8, 67.5, fill=CARD, line=BORDER, radius=4)
    text(sl, 60.8, 162, 827.2, 52, 'POST /clasificar  {"texto":"No puedo entrar en mi cuenta ficticia"}\n'
         '→ 200  {"version":"<commit>", "request_id":"…", "resultado":{…}}', size=15, font=MONO, color=MINT_L,
         check=False, lsp=Pt(22))
    rows = [["Pregunta de producción", "Cómo lo demostramos hoy", "Evidencia"],
            ["¿Un cambio roto llega a desplegarse?", "La pull request ejecuta tests y queda roja", "Check en rojo, PR bloqueada"],
            ["¿Lo desplegado es lo que se probó?", "Se despliega por digest, sin reconstruir", "El mismo sha256 en ECR y en ECS"],
            ["¿Quién puede desplegar?", "OIDC y environment staging, solo desde main", "sub del token y regla del entorno"],
            ["¿Qué falló y en qué versión?", "Log JSON con request_id y versión", "La línea del error en CloudWatch"],
            ["¿Podemos volver atrás?", "Rollback al digest anterior", "Salud y petición funcional en 200"]]
    table(sl, 48, 238, 852.8, [1.15, 1.25, 1.1], rows, size=11.5, row_h=34)
    band_simple(sl, "El código de la API apenas cambia; lo nuevo son los tests, los workflows, las plantillas y los logs.")
    footer_simple(sl)
    notes(sl, """
18:39–18:40. Leer la petición: es la misma tarea de S16. La respuesta añade dos campos que hoy serán clave: version (el commit con el que se construyó la imagen) y request_id (identificador de cada petición, también en la cabecera x-request-id).
Recorrer la tabla: cada fila es una pregunta que hay que poder contestar con evidencia, no con «creo que sí». Son los criterios con los que se valora el ejercicio: bloqueo de cambios defectuosos, uso del mismo artefacto, secretos protegidos y recuperación comprobable.
En vivo: abrir demo-cicd/app.py un momento: un único archivo con contrato, proveedores, logs y endpoints.
Pregunta: «¿Cuál de estas cinco preguntas no sabríais contestar hoy en vuestro proyecto?».
Fuentes: enunciado S18 (29/09/2026), apartado «Entrega y valoración»; demo-cicd/app.py.""")
    return sl


def s04_cicd(d):
    sl = d.slide(tag="cicd")
    header(sl, "CI/CD · en la demo", "Del commit a staging: qué automatiza la demo y qué no",
           "La 3 definió CI y CD; aquí se reparten entre nuestros workflows. Integrar y publicar son automáticos; "
           "desplegar en staging es, a propósito, una decisión de una persona.")
    section_label(sl, 43, 134, 874, "El camino de un cambio", color=MINT)
    nodes = [("g-source-code.png", "Código", "una rama"), ("g-git.png", "Pull request", "propuesta a main"),
             ("gh-actions.png", "Comprobaciones", "lock, ruff, pytest"), ("docker-mark-white.png", "Imagen", "docker build"),
             ("aws-ecr.png", "Registro", "ECR · digest"), ("aws-fargate.png", "Staging", "ensayo real"),
             ("g-users.png", "Producción", "usuarios reales")]
    w, gap = 112, (874 - 7 * 112) / 6
    for i, (ic, t, s) in enumerate(nodes):
        x = 43 + i * (w + gap)
        box(sl, x, 151, w, 66, fill=CARD)
        img(sl, ic, x + (w - 26) / 2, 157, w=26, h=26)
        text(sl, x + 2, 186, w - 4, 13, t, size=10, color=TITLE, bold=True, align="c")
        text(sl, x + 2, 200, w - 4, 12, s, size=8.5, color=MUTED, align="c")
        if i < 6:
            line(sl, x + w + 1, 184, x + w + gap - 1, 184, color=MINT, w=1.25)
    def span(n_end, y, color, t, fill):
        x2 = 43 + n_end * (w + gap) - gap
        box(sl, 43, y, x2 - 43, 15, fill=fill, line=color, radius=3)
        text(sl, 50, y + 1.5, x2 - 57, 12, t, size=8.5, color=color, bold=True, check=False)
    span(3, 225, MINT, "CI · integración continua", TAKE_BG)
    span(5, 245, BLUE, "Entrega continua · siempre hay una imagen validada; desplegar es una decisión", BLUE_BG)
    span(7, 265, VIOLET, "Despliegue continuo · cada cambio validado llega solo hasta producción", VIOLET_BG)
    cw = (874 - 2 * 11) / 3
    cards = [("CI · automática en cada PR", MINT,
              "ci-pr.yml llama a comprobaciones.yml: lock, análisis, tests, imagen y smoke del contenedor. "
              "Si algo falla, la pull request no se puede integrar.", "Disparador: pull_request hacia main"),
             ("Entrega · automática al integrar", BLUE,
              "publicar-main.yml repite las comprobaciones sobre el commit integrado, sube la imagen a ECR "
              "y anota su digest. Siempre hay una versión lista.", "Disparador: push a main"),
             ("Despliegue · una decisión", VIOLET,
              "desplegar-staging.yml se lanza a mano con un digest ya publicado. Nada llega solo a producción: "
              "no hacemos despliegue continuo.", "Disparador: workflow_dispatch desde main")]
    for i, (t, col, b, demo) in enumerate(cards):
        x = 43 + i * (cw + 11)
        box(sl, x, 292, cw, 172, fill=CARD)
        box(sl, x, 292, 3.5, 172, fill=col, radius=0)
        text(sl, x + 14, 302, cw - 24, 18, t, size=13, font=SERIF, color=TITLE)
        text(sl, x + 14, 328, cw - 24, 96, b, size=11.2, color=TEXT)
        text(sl, x + 14, 434, cw - 24, 24, demo, size=10, color=col, bold=True)
    takeaway(sl, "CI evita que entre código roto; CD evita que llegar a un entorno sea artesanal. La demo hace CI y entrega continua.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, f"""
18:40–18:41. Un minuto: las definiciones ya se dieron en la 3; aquí solo se sitúan en la demo. Recorrer las barras: CI cubre hasta las comprobaciones; la entrega continua llega hasta tener la imagen en el registro; el despliegue continuo llegaría solo hasta producción, y la demo no lo hace.
Las tres tarjetas dicen qué workflow hace cada tramo y qué lo dispara: pull_request (CI), push a main (entrega: imagen y digest) y workflow_dispatch (despliegue, decidido por una persona). Muchas empresas hacen CI + entrega continua; el despliegue continuo exige mucha confianza en las pruebas y en la monitorización.
En vivo: nada; diapositiva conceptual.
Pregunta: «¿Vuestro equipo hace entrega continua o despliegue continuo? ¿Quién pulsa el botón?».
Fuentes: enunciado S18 (despliegue a staging con workflow_dispatch); demo-cicd/.github/workflows. {SRC_AWS} {SRC_GH} Docker: logotipo oficial.""")
    return sl


def s05_entornos(d):
    sl = d.slide(tag="entornos")
    header(sl, "Entornos", "Una imagen, varios entornos: cambia la configuración",
           "Cada entorno responde a una pregunta distinta. Staging se parece a producción para descubrir problemas "
           "sin afectar a usuarios reales. Los datos y las claves de cada entorno no se mezclan.")
    envs = [("g-client.png", "Local", MINT, "Programar y probar rápido.", "API_MODE=demo, sin coste ni red.", "Datos ficticios."),
            ("gh-actions.png", "CI", AMBER, "Comprobar cada cambio en una máquina limpia.", "Sin claves; el modelo es un doble.", "Datos de test."),
            ("aws-fargate.png", "Staging", BLUE, "Ensayar el despliegue real: imagen, red, permisos y logs.", "La misma imagen que irá a producción.", "Datos ficticios."),
            ("g-users.png", "Producción", CORAL, "Atender a usuarios reales.", "Solo imágenes que pasaron staging.", "Datos reales, con copias. Fuera de la práctica.")]
    cw = (874 - 3 * 10) / 4
    for i, (ic, t, col, a, b, c) in enumerate(envs):
        x = 43 + i * (cw + 10)
        box(sl, x, 134, cw, 116, fill=CARD, line=col)
        img(sl, ic, x + 10, 142, w=26, h=26)
        text(sl, x + 44, 146, cw - 52, 18, t, size=13, font=SERIF, color=TITLE)
        bullets(sl, x + 10, 176, cw - 18, 72, [a, b, c], size=9, mark_color=col, space=2)
    section_label(sl, 43, 262, 874, "La configuración de cada entorno, fuera del código", color=MINT)
    rows = [["Variable", "Local", "Staging (demo)", "Producción (referencia)"],
            ["API_MODE", "demo, por defecto", "parámetro ApiMode del stack", "real"],
            ["OPENROUTER_MODEL", ".env", "parámetro ModelId del stack", "parámetro de su propio stack"],
            ["OPENROUTER_API_KEY", ".env, nunca en Git", "Secrets Manager → ECS al arrancar", "otro secreto, otro rol"],
            ["APP_VERSION", "desarrollo-local", "el commit, dentro de la imagen", "el mismo commit que en staging"]]
    table(sl, 43, 279, 874, [1.0, 1.0, 1.35, 1.35], rows, size=9.5, row_h=21, font_cols={0: MONO},
          colors={0: MINT_L})
    side_note(sl, 43, 395, 874, 70, "Si API_MODE=real y falta la clave",
              "La API no arranca (RuntimeError al crear la app): ECS no da la tarea por sana y el circuit breaker "
              "mantiene la versión anterior. Es preferible un despliegue que falla a una API que responde sin poder trabajar.",
              accent=AMBER)
    takeaway(sl, "La imagen probada en staging es la que llegaría a producción; solo cambian las variables y los secretos que inyecta la plataforma.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, f"""
18:41–18:43. Entornos y para qué sirve cada uno. Local: rapidez. CI: máquina limpia que no tiene nada de nuestro portátil (si funciona solo en local, es que dependemos de algo no declarado). Staging: el sitio donde se ensaya el despliegue real (permisos, red, logs, arranque del contenedor) sin usuarios. Producción: usuarios reales.
Principio de «una imagen, muchos entornos» (twelve-factor: la configuración vive en el entorno). Variables de la tabla reales de la demo: .env.example para local; parámetros ApiMode y ModelId de infra/02-staging.yaml; la clave llega de Secrets Manager por la sección Secrets de la definición de tarea; APP_VERSION la fija el workflow con --build-arg al construir.
El enunciado pide «una configuración local y otra de staging» y «modelos y secretos fuera del código»: es esta tabla.
En vivo: enseñar .env.example y el bloque Environment/Secrets de infra/02-staging.yaml.
Pregunta: «¿Por qué APP_VERSION va dentro de la imagen y no en la plantilla?» (porque identifica el contenido; si lo pusiera la plantilla podría mentir).
Fuentes: demo-cicd/app.py (crear_app), .env.example, infra/02-staging.yaml; ECS, datos sensibles: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html. {SRC_AWS} {SRC_GH}""")
    return sl


def s06_cadena(d):
    sl = d.slide(tag="cadena")
    header(sl, "Diseño del sistema · la demo", "La cadena que une un commit con cada petición",
           "Cada eslabón guarda el identificador del anterior. Así contestamos la pregunta clave de producción: "
           "¿qué código exacto atendió esta petición?")
    # carril GitHub
    box(sl, 43, 134, 874, 106, fill=None, line=BORDER, radius=6)
    img(sl, "github-mark-white.png", 53, 140, w=14, h=14)
    text(sl, 72, 141, 300, 12, "GITHUB", size=8.5, color=MUTED, bold=True)
    box(sl, 43, 256, 874, 110, fill=None, line=BORDER, radius=6)
    img(sl, "aws-logo-dark.png", 53, 262, h=12)
    text(sl, 80, 262, 300, 12, "AWS · eu-north-1", size=8.5, color=MUTED, bold=True)
    tag(sl, 200, 260, "ilustrativo", w=172)
    nw, gap = 196, (874 - 24 - 4 * 196) / 3
    xs = [55 + i * (nw + gap) for i in range(4)]
    top = [("g-git.png", "Pull request", "rama → main"), ("gh-actions.png", "Comprobaciones", "ci-pr · obligatorio"),
           ("g-source-code.png", "main", "commit integrado"), ("gh-actions.png", "Publicar · main", "construye una vez")]
    ids_top = ["PR #2 · plazo-de-atencion", "check en verde", "commit a8b0d4c…", "etiqueta = commit"]
    for i, ((ic, t, s), idt) in enumerate(zip(top, ids_top)):
        node(sl, xs[i], 160, nw, 52, ic, t, s, icon_s=26, tsize=10.5, ssize=8.5)
        text(sl, xs[i], 218, nw, 12, idt, size=8.5, font=MONO, color=MINT_L, align="c", check=False)
        if i < 3:
            line(sl, xs[i] + nw + 2, 186, xs[i + 1] - 2, 186, color=MINT, w=1.25)
    # carril AWS, de derecha a izquierda
    bot = [("aws-cloudwatch.png", "CloudWatch Logs", "una línea por petición"), ("aws-fargate.png", "Servicio Fargate", "tarea en marcha"),
           ("r-ecs-task.png", "Definición de tarea", "revisión nueva"), ("aws-ecr.png", "ECR", "imagen publicada")]
    ids_bot = ["request_id + version", "version = a8b0d4c…", "s18-lab:5 → @sha256:c41b…", "sha256:c41b…"]
    for i, ((ic, t, s), idt) in enumerate(zip(bot, ids_bot)):
        node(sl, xs[i], 284, nw, 52, ic, t, s, icon_s=26, tsize=10.5, ssize=8.5)
        text(sl, xs[i], 342, nw, 12, idt, size=8.5, font=MONO, color=MINT_L, align="c", check=False)
        if i < 3:
            line(sl, xs[i + 1] - 2, 310, xs[i] + nw + 2, 310, color=BLUE, w=1.25)
    line(sl, xs[3] + nw / 2, 232, xs[3] + nw / 2, 282, color=MINT, w=1.5)
    text(sl, xs[3] + nw / 2 - 156, 244, 150, 12, "docker push · rol publicar", size=8, color=MUTED, align="r", check=False)
    text(sl, xs[2] + 6, 290 - 34, nw - 12, 12, "desplegar-staging · por digest", size=8, color=BLUE, bold=True,
         align="r", check=False)
    side_note(sl, 43, 378, 431, 87, "Dos roles, dos permisos",
              "Publicar solo sube imágenes a este repositorio de ECR y solo desde main. Desplegar solo actualiza este "
              "servicio y solo desde el environment staging.", accent=MINT, size=9.5)
    side_note(sl, 486, 378, 431, 87, "Lo que no hay",
              "Ninguna clave de AWS guardada en GitHub. Ningún secreto dentro de la imagen. Ninguna reconstrucción "
              "al desplegar: staging recibe un digest que ya existe.", accent=CORAL, size=9.5)
    takeaway(sl, "commit → digest → definición de tarea → tarea → request_id: si un eslabón no guarda el anterior, se pierde la pista.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, f"""
18:43–18:45. Es el mapa de toda la clase. Arriba, GitHub: la PR pasa las comprobaciones; al integrarse, publicar-main construye una sola vez y etiqueta la imagen con el commit (40 caracteres). Abajo, AWS (se lee de derecha a izquierda): ECR guarda la imagen y calcula su digest; desplegar-staging registra una definición de tarea nueva que apunta a repositorio@sha256:…; el servicio Fargate ejecuta esa tarea; cada petición escribe en CloudWatch una línea con request_id y version (= commit).
Los identificadores son ilustrativos (todavía no hay ensayo real en GitHub y AWS).
En vivo: recorrer el repositorio: app.py, tests/, .github/workflows/ (5 archivos), infra/ (2 plantillas), scripts/smoke.sh, cambios/ (3 parches para la demo).
Pregunta: «Si mañana falla una petición, ¿qué dato necesitáis para saber qué versión la atendió?» (la version del log; con ella, el commit y el digest).
Fuentes: demo-cicd/.github/workflows/publicar-main.yml y desplegar-staging.yml; infra/01-registro-y-publicacion.yaml y 02-staging.yaml. {SRC_AWS} {SRC_GH}""")
    return sl


def s07_actions(d):
    sl = d.slide(tag="actions")
    header(sl, "GitHub Actions · qué es", "Un workflow es un YAML que GitHub ejecuta ante un evento",
           "GitHub Actions ejecuta automatizaciones en máquinas temporales (runners). Cada archivo de "
           ".github/workflows/ declara cuándo se ejecuta, con qué permisos y qué pasos sigue.")
    section_label(sl, 43, 134, 430, "Un workflow mínimo", color=AMBER)
    tag(sl, 300, 132, "simplificado", w=173)
    lines = ["name: CI · pull request",
             "on:",
             "  pull_request:",
             "    branches: [main]",
             "permissions:",
             "  contents: read",
             "jobs:",
             "  comprobar:",
             "    runs-on: ubuntu-24.04",
             "    steps:",
             "      - uses: actions/checkout@3d3c42e5…",
             "        with:",
             "          persist-credentials: false",
             "      - run: uv sync --locked",
             "      - run: uv run pytest"]
    y0 = 158
    box(sl, 43, 151, 430, 314, fill=CARD, line=BORDER, radius=4)
    pitch = code_block(sl, 55, y0, 400, lines, size=10, pitch=19.3)
    for li, n, col in [(1, 1, VIOLET), (4, 2, BLUE), (8, 3, AMBER), (13, 4, MINT), (10, 5, CORAL)]:
        line_badge(sl, 448, y0 + 3, pitch, li, n, col)
    parts = [(VIOLET, "Evento · on:", "Qué lo dispara: una pull request, un push a main, un botón manual (workflow_dispatch) o una hora."),
             (BLUE, "Permisos · permissions:", "Lo que puede hacer el token del job. Aquí solo leer el código; pedir credenciales a AWS exige id-token: write."),
             (AMBER, "Job y runner · runs-on:", "Pasos que se ejecutan en una máquina limpia de GitHub que se destruye al terminar."),
             (MINT, "Step · run:", "Un comando de shell. Si termina con error, el job falla y la pull request queda en rojo."),
             (CORAL, "Action · uses:", "Código de otra persona que se descarga y se ejecuta con nuestros permisos: se fija a un commit.")]
    y = 151
    for i, (col, t, b) in enumerate(parts, 1):
        box(sl, 487, y, 430, 58.4, fill=CARD)
        badge(sl, 497, y + 9, i, fill=col, d=16, size=8.5)
        text(sl, 521, y + 8, 386, 15, t, size=11, color=TITLE, bold=True)
        text(sl, 521, y + 26, 386, 30, b, size=9, color=TEXT)
        y += 64
    takeaway(sl, "Evento, permisos, jobs y pasos viven en el repositorio: se revisan en una pull request como el resto del código.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, f"""
18:45–18:47. Vocabulario mínimo de GitHub Actions con un workflow reducido a lo esencial (el real de la demo reparte esto entre ci-pr.yml y comprobaciones.yml). Workflow: un archivo YAML en .github/workflows/. Evento (on): pull_request, push, workflow_dispatch, schedule… Permisos: el GITHUB_TOKEN del job solo tiene lo que se declara; contents: read basta para descargar el código. Job: conjunto de pasos en un runner (máquina virtual efímera de GitHub, aquí ubuntu-24.04). Step: run (shell) o uses (una action). Action: código de terceros; por eso se fija a un SHA (diapositiva 16).
persist-credentials: false evita que el token quede guardado en .git del runner para pasos posteriores.
Coste: los runners estándar son gratuitos en repositorios públicos.
En vivo: abrir .github/workflows/comprobaciones.yml y señalar on: workflow_call, permissions y los pasos.
Pregunta: «¿Qué pasa si un step devuelve un código de salida distinto de 0?».
Fuentes: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows · https://docs.github.com/en/actions/reference/security/secure-use · https://docs.github.com/en/billing/concepts/product-billing/github-actions (consultadas 16/11/2026).""")
    return sl


def s08_workflows(d):
    sl = d.slide(tag="workflows")
    header(sl, "GitHub Actions · la demo", "Cinco workflows cortos, cada uno con un solo trabajo",
           "Separar comprobar, publicar y desplegar permite dar a cada paso solo los permisos que necesita. "
           "La pull request nunca puede pedir credenciales de AWS.")
    flow = [("pull request", CARD2, TITLE), ("ci-pr", TAKE_BG, MINT_L), ("merge", CARD2, TITLE),
            ("publicar-main", TAKE_BG, MINT_L), ("digest", AMBER_BG, AMBER), ("desplegar-staging", TAKE_BG, MINT_L),
            ("staging", BLUE_BG, BLUE)]
    ws = [96, 70, 64, 116, 70, 138, 76]
    x = 43 + (874 - (sum(ws) + 6 * 26)) / 2
    for i, ((t, f, c), w) in enumerate(zip(flow, ws)):
        chip(sl, x, 136, w, 24, t, fill=f, color=c, size=10, line=BORDER)
        if i < len(flow) - 1:
            line(sl, x + w + 4, 148, x + w + 22, 148, color=MINT, w=1.25)
        x += w + 26
    rows = [["Workflow", "Se ejecuta con", "Qué hace", "Credenciales de AWS"],
            ["comprobaciones.yml", "workflow_call (lo llaman los dos siguientes)", "Lock, ruff, cfn-lint, pytest, build y smoke del contenedor", ("Ninguna", {"color": MINT_L, "bold": True})],
            ["ci-pr.yml", "pull_request hacia main", "Llama a comprobaciones; cancela la ejecución anterior de la misma PR", ("Ninguna, y no puede pedirlas", {"color": MINT_L, "bold": True})],
            ["publicar-main.yml", "push a main", "Repite comprobaciones; construye una imagen, la prueba, la sube y anota el digest", ("Rol publicar: solo ECR", {"color": AMBER, "bold": True})],
            ["desplegar-staging.yml", "workflow_dispatch desde main", "Despliega un digest publicado, comprueba qué quedó en marcha y hace el smoke", ("Rol desplegar: solo este servicio", {"color": AMBER, "bold": True})],
            ["diagnostico-oidc.yml", "workflow_dispatch", "Muestra el sub y el aud del token; no asume ningún rol", ("Ninguna", {"color": MINT_L, "bold": True})]]
    table(sl, 43, 176, 874, [1.1, 1.25, 2.1, 1.2], rows, size=9.5, row_h=33, font_cols={0: MONO}, colors={0: MINT_L})
    side_note(sl, 43, 390, 431, 75, "Reutilizar, no copiar",
              "comprobaciones.yml se declara con on: workflow_call. La PR y main ejecutan exactamente los mismos pasos: "
              "una sola definición de «validado».", accent=AMBER, size=9.5)
    side_note(sl, 486, 390, 431, 75, "Uno detrás de otro",
              "concurrency: si llega otro commit a la PR, se cancela la ejecución anterior; en staging, un despliegue "
              "espera a que termine el anterior y nunca se cancela a medias.", accent=AMBER, size=9.5)
    takeaway(sl, "El que comprueba no publica y el que publica no despliega: cada workflow tiene el mínimo poder necesario.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, """
18:49–18:51. Mapa de los cinco archivos de demo-cicd/.github/workflows/. Leer la columna de credenciales de arriba abajo: dos workflows no tocan AWS; publicar y desplegar usan roles distintos (dos stacks distintos). diagnostico-oidc sirve para leer el sub real antes de escribir la confianza del rol.
comprobaciones.yml es un workflow reutilizable: lo llaman ci-pr y publicar-main con uses: ./.github/workflows/comprobaciones.yml. Así «validado» significa lo mismo en la PR y en main (el enunciado pide repetir análisis, tests y construcción sobre el commit integrado).
concurrency: ci-pr-<número de PR> con cancel-in-progress: true; publicar-main y staging con cancel-in-progress: false (no se interrumpe una publicación ni un despliegue).
En vivo: abrir publicar-main.yml y señalar needs: comprobaciones y permissions: id-token: write solo en el job publicar.
Pregunta: «¿Por qué no hacemos todo en un único workflow?».
Fuentes: demo-cicd/.github/workflows/*.yml (validados con actionlint 1.7.12 el 17/11/2026); https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows.""")
    return sl


def s09_comprobaciones(d):
    sl = d.slide(tag="comprobaciones")
    header(sl, "Integración continua · cada PR", "Lo que debe pasar antes de integrar un cambio",
           "comprobaciones.yml define «validado» una sola vez. Cada paso responde a una pregunta y cualquiera de ellos "
           "puede dejar la pull request en rojo.")
    steps = [("Dependencias bloqueadas", ["uv sync --locked", "uv export … | diff requirements.lock -"],
              "Falla si uv.lock no coincide con pyproject.toml; Docker instala ese mismo lock con hashes."),
             ("Análisis de código", ["ruff check . && ruff format --check .", "cfn-lint infra/*.yaml"],
              "Errores, imports y formato; plantillas de AWS válidas antes de desplegarlas."),
             ("Tests", ["pytest"],
              "23 pruebas sin red ni claves: el proveedor de IA es un doble."),
             ("Imagen", ["docker build --provenance=false \\", '  --build-arg "APP_VERSION=$GITHUB_SHA" .'],
              "Si la imagen no se construye aquí, nunca llegaría a ECR."),
             ("Contenedor en marcha", ["docker run --read-only --cap-drop ALL …", "bash scripts/smoke.sh …"],
              "Arranca la imagen como en staging y prueba salud, versión, clasificación y 422."),
             ("Check obligatorio", ["comprobaciones / Lock, análisis,", "tests e imagen"],
              "Una regla de main exige este check en verde para poder integrar.")]
    cw, ch = (874 - 2 * 10.8) / 3, 113.8
    for i, (t, code, b) in enumerate(steps):
        x = 43 + (i % 3) * (cw + 10.8)
        y = 134 + (i // 3) * (ch + 8.6)
        box(sl, x, y, cw, ch, fill=CARD)
        badge(sl, x + 8.6, y + 7.9, i + 1, fill=AMBER, d=16, size=8.5)
        text(sl, x + 30.2, y + 7.2, cw - 40, 17.3, t, size=10.5, color=TITLE, bold=True)
        code_panel(sl, x + 8.6, y + 31.7, cw - 17.2, 43.2, code, size=8.5)
        text(sl, x + 10.1, y + 80.6, cw - 20, 30, b, size=9, color=TEXT)
    box(sl, 43, 382, 874, 83, fill=CARD)
    text(sl, 54.5, 389, 600, 12.2, "RESULTADO EN LOCAL · 17/11/2026 · MISMOS COMANDOS", size=8.5, color=BLUE, bold=True)
    tag(sl, 735, 387, "pendiente", w=172)
    text(sl, 54.5, 406, 851, 56, [
        [("Validado: ", {"bold": True, "color": TITLE}),
         ("uv sync --locked ✓ · lock igual que requirements.lock ✓ · ruff ✓ · cfn-lint ✓ · pytest 23 passed ✓ · "
          "docker build ✓ · smoke del contenedor de solo lectura ✓ · actionlint ✓.", {})],
        [("Pendiente: ", {"bold": True, "color": AMBER}),
         ("la ejecución en GitHub Actions; se hará en el ensayo con el repositorio publicado.", {})]],
        size=9.5, color=TEXT, space=4)
    takeaway(sl, "Una PR solo entra si los mismos comandos que usaríamos en local pasan en una máquina limpia.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, """
18:51–18:53. Recorrer los seis pasos de comprobaciones.yml en orden. 1 uv sync --locked falla si alguien cambia pyproject.toml sin regenerar uv.lock («nadie instala lo último»); además se compara requirements.lock (lo que usa Docker con pip --require-hashes) con uv export. 2 ruff (lint y formato) y cfn-lint de las plantillas. 3 pytest: 23 pruebas sin red. 4 docker build con APP_VERSION=$GITHUB_SHA: la versión de la imagen es el commit. 5 arrancar el contenedor de solo lectura y sin capacidades, y lanzar scripts/smoke.sh (el mismo script que usa staging). 6 el check aparece en la PR con el nombre «comprobaciones / Lock, análisis, tests e imagen»; una regla de rama lo hace obligatorio.
Dependencias bloqueadas = el enunciado; análisis de código = ruff; tests = pytest; imagen Docker = build.
En vivo: uv run ruff check . && uv run pytest -q (23 passed) en la terminal.
Pregunta: «¿Qué detecta el paso 5 que no detecta el paso 4?» (que la imagen arranca, escucha en el puerto y responde, por ejemplo con un sistema de archivos de solo lectura).
Fuentes: demo-cicd/.github/workflows/comprobaciones.yml; verificación local en .build/s18/logs (17/11/2026).""")
    return sl


def s10_tests(d):
    sl = d.slide(tag="tests")
    header(sl, "Tests automáticos", "Probar una API de IA sin llamar al modelo",
           "Un test que llama a un modelo de pago es lento, cuesta dinero y no siempre responde igual. Sustituimos el "
           "proveedor por un doble que hace lo que queremos y comprobamos nuestro código.")
    section_label(sl, 43, 134, 440, "tests/test_api.py · caso 3, fallo del proveedor", color=AMBER)
    code_panel(sl, 43, 151, 440, 314, [
        "class DobleCaido:",
        '    """Simula que el proveedor no responde."""',
        '    modelo = "doble-de-test"',
        "",
        "    async def clasificar(self, texto):",
        '        raise ErrorProveedor("proveedor_timeout", 504)',
        "",
        "",
        "def test_fallo_del_proveedor_devuelve_error_",
        "        y_no_inventa_una_respuesta():",
        "    with TestClient(crear_app(DobleCaido())) as c:",
        '        r = c.post("/clasificar",',
        '                   json={"texto": "Caso ficticio"})',
        "    assert r.status_code == 504",
        '    assert r.json()["error"] == "proveedor_timeout"',
        '    assert "resultado" not in r.json()'], size=9, fill=CARD, line=BORDER, pad=12)
    section_label(sl, 499, 134, 418, "Los tres casos que pide el enunciado", color=AMBER)
    cases = [(MINT, "Respuesta válida → 200", "El doble devuelve una clasificación. Comprobamos campos, modelo y que request_id coincide con la cabecera."),
             (AMBER, "Entrada inválida → 422", "Vacía, de más de 1.000 caracteres, sin campo o de otro tipo. El doble registra 0 llamadas: no se paga por basura."),
             (CORAL, "Fallo del proveedor → 504", "Timeout simulado: error controlado con su código, sin respuesta inventada.")]
    y = 151
    for col, t, b in cases:
        box(sl, 499, y, 418, 62, fill=CARD)
        box(sl, 499, y, 3.5, 62, fill=col, radius=0)
        text(sl, 512, y + 8, 396, 15, t, size=11, color=TITLE, bold=True)
        text(sl, 512, y + 26, 396, 34, b, size=9, color=TEXT)
        y += 68
    box(sl, 499, 357, 418, 108, fill=CARD, line=AMBER)
    text(sl, 511, 364, 396, 12, "Y ADEMÁS SE PRUEBA", size=8.5, color=AMBER, bold=True)
    bullets(sl, 511, 380, 398, 84, [
        "Un error no previsto devuelve 500 sin detalles internos.",
        "El log lleva request_id y versión, y no contiene el texto del usuario.",
        "El adaptador real con httpx.MockTransport: 429, 5xx, timeout y JSON inválido.",
        "API_MODE=real sin clave no arranca."], size=9, mark_color=AMBER, space=2)
    takeaway(sl, "Los tests comprueban nuestro contrato y nuestros errores; la calidad del modelo se evalúa aparte, en S19.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, """
18:53–18:55. El enunciado pide probar entrada inválida, respuesta válida y fallo del proveedor «con respuestas simuladas para no consumir APIs de pago». crear_app(proveedor) acepta cualquier objeto con un atributo modelo y un método clasificar: en producción es ProveedorOpenRouter; en los tests, un doble. Tres dobles en tests/test_api.py: DobleCorrecto (cuenta llamadas), DobleCaido (ErrorProveedor 504) y DobleRoto (excepción inesperada).
Además, el adaptador HTTP real se prueba sin red con httpx.MockTransport: se comprueba la petición que enviaría (modelo, esquema JSON, sin fallbacks) y cómo convierte cada fallo en un error controlado. Total: 23 pruebas en 0,2 s.
Distinguir: estos tests prueban nuestro código, no si el modelo clasifica bien. Medir la calidad del modelo es evaluación (S19).
En vivo: abrir tests/test_api.py y buscar los comentarios «caso 1», «caso 2», «caso 3».
Pregunta: «¿Qué ventaja tiene contar las llamadas al doble en el caso de entrada inválida?».
Fuentes: demo-cicd/tests/test_api.py; demo-cicd/app.py (Proveedor, ErrorProveedor).""")
    return sl


def s11_demo_pr(d):
    sl = d.slide(tag="demo-pr")
    header(sl, "Demo 1 · PR con un fallo", "Un cambio razonable que los tests bloquean",
           "cambios/01 «mejora» la API: si el proveedor falla, devuelve una respuesta por defecto. Parece amable con el "
           "usuario, pero oculta el fallo y entrega una clasificación inventada.")
    section_label(sl, 43, 134, 430, "El cambio · app.py", color=AMBER)
    box(sl, 43, 151, 430, 178, fill=CARD, line=BORDER, radius=4)
    diff = [("     try:", TEXT), ("         resultado = await proveedor.clasificar(", TEXT),
            ("             incidencia.texto)", TEXT), ("+    except ErrorProveedor:", MINT),
            ("+        # «Mejora»: respondemos algo por defecto", MINT), ("+        resultado = Clasificacion(", MINT),
            ('+            categoria="consulta",', MINT), ('+            prioridad="media",', MINT),
            ('+            respuesta="Hemos recibido tu', MINT), ('+                incidencia…")', MINT),
            ("     finally:", TEXT)]
    paras = [[(t, {"color": c})] for t, c in diff]
    text(sl, 55, 160, 410, 165, paras, size=9, font=MONO, check=False, lsp=Pt(14.4))
    section_label(sl, 487, 134, 260, "Lo que dice pytest", color=AMBER)
    tag(sl, 745, 132, "real", w=172)
    box(sl, 487, 151, 430, 178, fill="0B1418", line=BORDER, radius=4)
    term = [("$ uv run pytest -q", MUTED), ("", TEXT),
            ("FAILED tests/test_api.py::", CORAL), ("  test_fallo_del_proveedor_devuelve_error_", CORAL),
            ("  y_no_inventa_una_respuesta", CORAL), ("FAILED tests/test_api.py::", CORAL),
            ("  test_el_log_de_un_fallo_guarda_el_", CORAL), ("  codigo_y_el_estado", CORAL), ("", TEXT),
            ("2 failed, 21 passed", AMBER)]
    text(sl, 499, 160, 410, 165, [[(t, {"color": c})] for t, c in term], size=9, font=MONO, check=False, lsp=Pt(15.4))
    states = [("PR abierta", CARD2, TITLE), ("comprobaciones ✗", CORAL_BG, CORAL), ("merge bloqueado", CORAL_BG, CORAL),
              ("sin credenciales de AWS", TAKE_BG, MINT_L)]
    x = 43
    ws = [120, 160, 150, 200]
    for i, ((t, f, c), w) in enumerate(zip(states, ws)):
        chip(sl, x, 343, w, 24, t, fill=f, color=c, size=10, line=BORDER)
        if i < 3:
            line(sl, x + w + 4, 355, x + w + 26, 355, color=MUTED, w=1.25)
        x += w + 30
    side_note(sl, 43, 380, 431, 85, "Por qué no recibe credenciales",
              "ci-pr.yml no declara id-token: write. Aunque alguien lo añadiera en su rama, el sub del token terminaría en "
              ":pull_request y ningún rol de AWS confía en ese valor.", accent=CORAL, size=9.5)
    side_note(sl, 486, 380, 431, 85, "Por qué lo detecta un test y no el build",
              "El código compila y la imagen arranca. Solo un test que conoce el contrato («si el proveedor falla, "
              "error y sin resultado») ve que inventamos una respuesta.", accent=AMBER, size=9.5)
    takeaway(sl, "Un fallo de comportamiento solo lo bloquea un test que describe el comportamiento esperado.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, """
18:55–18:59. Primer momento de demo (el enunciado pide «introduce un fallo deliberado y demuestra que el workflow lo detecta»). El parche cambios/01-pr-con-fallo.patch añade un except que devuelve una clasificación por defecto. Dos tests fallan: el de fallo del proveedor (esperaba 504 y sin resultado) y el que comprueba que el log de un fallo guarda el código del error.
La salida de pytest es real (ensayo local del 17/11/2026, .build/s18/logs/gen_cambios.json).
En vivo · GitHub (si hay ensayo): git switch -c respuesta-por-defecto; git apply cambios/01-pr-con-fallo.patch; commit, push, gh pr create --fill; gh pr checks --watch → rojo; el botón de merge aparece bloqueado por la regla. Cerrar la PR.
En vivo · local: los mismos dos primeros comandos y uv run pytest -q → 2 failed, 21 passed. Comandos exactos en docs/comandos.md, diapositiva 15.
Pregunta: «¿Hay algún caso en el que sí tendría sentido una respuesta por defecto?» (sí, si el contrato lo dice y se marca como tal; aquí el contrato dice lo contrario).
Fuentes: demo-cicd/cambios/01-pr-con-fallo.patch; tests/test_api.py.""")
    return sl


def s12_proteger(d):
    sl = d.slide(tag="proteger")
    header(sl, "GitHub · reglas y cadena de suministro", "Proteger main y lo que ejecutan nuestros workflows",
           "Un check en rojo solo bloquea si una regla lo exige. Y cada acción externa es código de otra persona que corre "
           "con nuestros permisos: hay que fijar exactamente qué versión.")
    section_label(sl, 43, 134, 400, "Ruleset de la rama main", color=AMBER)
    box(sl, 43, 151, 400, 205, fill=CARD)
    img(sl, "g-shield.png", 55, 162, w=28, h=28)
    text(sl, 92, 164, 340, 30, "Settings → Rules → Rulesets → New branch ruleset · objetivo: main", size=9.5,
         color=MUTED)
    rules = [("Require a pull request before merging", "nadie integra sin PR"),
             ("Require status checks to pass", "comprobaciones / Lock, análisis, tests e imagen"),
             ("Block force pushes", "la historia de main no se reescribe")]
    y = 202
    for t, s in rules:
        box(sl, 55, y, 9, 9, fill=AMBER, radius=1)
        text(sl, 72, y - 3, 360, 14, t, size=10, color=TITLE, bold=True)
        text(sl, 72, y + 12, 360, 14, s, size=9, color=TEXT)
        y += 42
    text(sl, 55, 330, 380, 22, "Rulesets y environments: disponibles en repositorios públicos con GitHub Free.",
         size=8.5, color=MUTED)
    section_label(sl, 459, 134, 458, "Acciones fijadas al commit, no a una etiqueta", color=AMBER)
    box(sl, 459, 151, 458, 64, fill=CARD)
    text(sl, 471, 159, 436, 50, [
        [("✗  ", {"color": CORAL, "bold": True}), ("uses: actions/checkout@v7", {"font": MONO, "color": TITLE}),
         ("   la etiqueta puede moverse", {"color": MUTED, "size": 8.5})],
        [("✓  ", {"color": MINT, "bold": True}), ("uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1", {"font": MONO, "color": MINT_L, "size": 7.6}),
         ("  # v7.0.1", {"font": MONO, "color": MUTED, "size": 7.6})]], size=9.5, color=TEXT, space=8)
    rows = [["Acción", "Versión", "SHA completo (40 caracteres)"],
            ["actions/checkout", "v7.0.1", "3d3c42e5aac5ba805825da76410c181273ba90b1"],
            ["astral-sh/setup-uv", "v10.3.3", "68559e99cc807c1eb7e9238fd43a15bba460eec2"],
            ["aws-actions/configure-aws-credentials", "v6.3.0", "e1253824e5c10ff9df46874f81ed3ec929e19cfd"],
            ["actions/github-script", "v9.0.0", "3a2844b7e9c422d3c10d287c895573f7108da1b3"]]
    table(sl, 459, 223, 458, [1.55, 0.52, 2.1], rows, size=8, row_h=20, font_cols={2: MONO}, colors={2: MINT_L})
    text(sl, 459, 330, 458, 24, "Comprobado el 17/11/2026 con gh api repos/<acción>/git/ref/tags/<versión> "
         "(si la etiqueta es anotada, se sigue hasta su commit).", size=8.5, color=MUTED)
    side_note(sl, 43, 368, 874, 97, "Por qué importa",
              "Quien controla una etiqueta puede apuntarla a otro código y ese código se ejecutaría con nuestros "
              "permisos, incluido el token OIDC que obtiene credenciales de AWS. Un SHA identifica un commit concreto "
              "que no se puede cambiar. El comentario # v7.0.1 dice a las personas qué versión es; para actualizar, "
              "se revisa la nueva versión y se cambia el SHA en una PR.", accent=AMBER, size=11)
    takeaway(sl, "La regla convierte el rojo en un bloqueo; el SHA convierte «la versión 7» en un código que nadie puede cambiar.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, """
18:59–19:01. Dos protecciones distintas. Ruleset: hace obligatorio el check (sin él, una PR roja se podría integrar igualmente). Se configura en la interfaz de GitHub; el nombre del check aparece en la lista después de la primera PR. Rulesets y environments están disponibles en repositorios públicos con GitHub Free (en privados requieren Pro, Team o Enterprise).
Acciones por SHA: GitHub recomienda fijar las acciones a un SHA completo de commit como la única forma de usarlas de forma inmutable. Los cuatro SHA de la tabla son los de la demo, comprobados con gh api: para etiquetas anotadas (github-script v9.0.0) hay que seguir el objeto tag hasta el commit.
Se puede añadir Dependabot para proponer actualizaciones de los SHA mediante PR (no incluido en la demo).
En vivo: grep -rn "uses:" .github/workflows mostrando que ninguna acción externa usa una etiqueta.
Pregunta: «Si una acción la publica GitHub, ¿hace falta fijarla?» (sí: la recomendación es para todas; el riesgo es la etiqueta, no el autor).
Fuentes: https://docs.github.com/en/actions/reference/security/secure-use · https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets · .build/s18/logs/acciones-sha.txt (17/11/2026). Icono: AWS Architecture Icons (Shield, general).""")
    return sl


# ---------------------------------------------------------------- ampliación 17/11/2026 (petición de José)
SRC_ALT = ("Logotipos de GitLab y Cloudflare: github/explore (repositorio oficial de GitHub). "
           "Hetzner: logotipo de hetzner.com. AWS CodeBuild: AWS Architecture Icons 31/07/2026.")


def s07b_action(d):
    sl = d.slide(tag="action")
    header(sl, "GitHub Actions · qué es una action", "Una action es un paso empaquetado y reutilizable",
           "El workflow decide cuándo y en qué orden; cada action resuelve una tarea concreta: descargar el código, "
           "instalar uv o pedir credenciales a AWS. Vive en su propio repositorio y la describe un archivo action.yml.")
    # --- columna izquierda: del workflow al repositorio de la action
    section_label(sl, 43, 134, 420, "Del workflow al código de la action", color=AMBER)
    box(sl, 43, 151, 420, 86, fill=CARD, line=BORDER)
    img(sl, "gh-actions.png", 53, 159, w=18, h=18)
    text(sl, 78, 160, 375, 13, "NUESTRO PASO · desplegar-staging.yml", size=8.5, color=AMBER, bold=True)
    code_panel(sl, 51, 181, 404, 50, [
        "- uses: aws-actions/configure-aws-credentials@e1253824… # v6.3.0",
        "  with:",
        "    role-to-assume: ${{ vars.AWS_ROLE_DESPLEGAR }}",
        "    aws-region: ${{ vars.AWS_REGION }}"], size=7.8, pad=6)
    line(sl, 253, 239, 253, 257, color=AMBER, w=1.5)
    text(sl, 262, 239, 200, 16, "GitHub descarga ese commit exacto", size=8.5, color=MUTED, anchor="m")
    box(sl, 43, 259, 420, 206, fill=CARD, line=BORDER)
    img(sl, "github-mark-white.png", 53, 267, w=20, h=20)
    text(sl, 80, 266, 375, 13, "aws-actions/configure-aws-credentials", size=10, font=MONO, color=TITLE, bold=True)
    text(sl, 80, 280, 375, 12, "action.yml · extracto real del commit e1253824 (v6.3.0)", size=8, color=MUTED)
    lines = ["name: \"Configure AWS Credentials\" Action…",
             "inputs:",
             "  aws-region:",
             "    required: true",
             "  audience:",
             "    default: sts.amazonaws.com",
             "outputs:",
             "  aws-account-id:",
             "runs:",
             "  using: node24",
             "  main: dist/index.js",
             "  post: dist/cleanup/index.js"]
    pitch = code_panel(sl, 51, 298, 404, 160, lines, size=8.5, pad=8, bold=True)
    for li, n, col in [(1, 1, BLUE), (6, 2, VIOLET), (8, 3, MINT)]:
        line_badge(sl, 432, 298 + 7, pitch, li, n, col)
    # --- columna derecha: qué declara, tipos y dónde corre
    section_label(sl, 477, 134, 440, "Qué declara action.yml", color=AMBER)
    parts = [(BLUE, "inputs · lo que recibe en with:", "aws-region es obligatorio; audience ya trae sts.amazonaws.com, la audiencia de OIDC."),
             (VIOLET, "outputs · lo que devuelve", "Valores para los pasos siguientes: ${{ steps.<id>.outputs.aws-account-id }}."),
             (MINT, "runs · cómo se ejecuta", "Node 24 ejecuta dist/index.js; el paso post borra las credenciales al terminar el job.")]
    y = 151
    for i, (col, t, b) in enumerate(parts, 1):
        box(sl, 477, y, 440, 43, fill=CARD)
        badge(sl, 486, y + 7, i, fill=col, d=15, size=8)
        text(sl, 508, y + 5.5, 400, 14, t, size=10, color=TITLE, bold=True)
        text(sl, 508, y + 21, 402, 20, b, size=8.6, color=TEXT)
        y += 47
    section_label(sl, 477, 297, 440, "Tres formas de escribir una action", color=AMBER)
    kinds = [("g-source-code.png", "JavaScript", "using: node24", "Corre directamente en el runner. Arranca rápido; Linux, macOS y Windows."),
             ("docker-mark-white.png", "Contenedor", "using: docker", "Trae su propio sistema y herramientas. Solo runners Linux; arranca más lento."),
             ("g-gear.png", "Compuesta", "using: composite", "Agrupa varios pasos run y uses en uno solo, reutilizable entre workflows.")]
    x = 477
    for icon, t, code, b in kinds:
        box(sl, x, 313, 142.7, 84, fill=CARD)
        img(sl, icon, x + 8, 320, w=20, h=20)
        text(sl, x + 34, 320, 104, 13, t, size=10.5, color=TITLE, bold=True)
        text(sl, x + 34, 333.5, 104, 10, code, size=7.5, font=MONO, color=MINT_L, bold=True)
        text(sl, x + 8, 348, 128, 46, b, size=8.3, color=TEXT)
        x += 148.65
    section_label(sl, 477, 405, 440, "¿En qué máquina se ejecuta?", color=AMBER)
    box(sl, 477, 421, 216, 44, fill=TAKE_BG)
    text(sl, 486, 425, 200, 38, [[("Runner de GitHub  ", {"bold": True, "color": MINT_L}),
                                  ("runs-on: ubuntu-24.04 · máquina limpia en cada job, se paga por minuto.", {})]],
         size=8.5, color=TEXT)
    box(sl, 701, 421, 216, 44, fill=AMBER_BG)
    text(sl, 710, 425, 200, 38, [[("Runner propio  ", {"bold": True, "color": AMBER}),
                                  ("runs-on: self-hosted · tu servidor; lo comparamos en las alternativas.", {})]],
         size=8.5, color=TEXT)
    takeaway(sl, "Una action es código de otra persona que corre con los permisos de nuestro job: se elige, se fija a un commit y se revisa al actualizar.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, """
18:47–18:49. Profundizar en la pieza uses: de la diapositiva anterior. Un workflow orquesta (eventos, jobs, orden); una action es un paso reutilizable que vive en su propio repositorio con un archivo action.yml (o action.yaml) en la raíz. Al escribir uses: dueño/repo@ref, GitHub descarga ese repositorio en esa referencia y lo ejecuta dentro de nuestro job, con nuestros permisos y nuestro token.
action.yml declara tres cosas: inputs (lo que pasamos en with:, con obligatorios y valores por defecto), outputs (valores que leen los pasos siguientes con steps.<id>.outputs.<nombre>) y runs (cómo se ejecuta). El extracto es real: configure-aws-credentials v6.3.0, commit e1253824…, el mismo SHA que usan publicar-main.yml y desplegar-staging.yml. Su runs usa Node 24 con un paso post que limpia las credenciales al acabar el job.
Tipos: JavaScript (rápida, cualquier sistema operativo), contenedor Docker (entorno propio, solo Linux, arranque más lento) y compuesta (varios pasos en uno; nuestra comprobaciones.yml no es una action sino un workflow reutilizable con workflow_call: misma idea, otro nivel).
Las actions públicas se descubren en GitHub Marketplace (github.com/marketplace?type=actions). Que esté en el Marketplace no significa que esté revisada: por eso la diapositiva 16 fija cada una a un SHA.
Runner: la máquina donde se ejecuta el job. Los de GitHub son efímeros y se pagan por minuto en repositorios privados; los self-hosted son máquinas propias (diapositivas 17 y 18).
En vivo: abrir https://github.com/aws-actions/configure-aws-credentials/blob/e1253824e5c10ff9df46874f81ed3ec929e19cfd/action.yml y señalar inputs, outputs y runs.
Pregunta: «¿Qué diferencia hay entre un step con run: y uno con uses:?» (run ejecuta un comando nuestro; uses ejecuta el código de una action).
Fuentes: https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions · https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax · gh api repos/aws-actions/configure-aws-credentials/contents/action.yml?ref=e1253824e5c10ff9df46874f81ed3ec929e19cfd (consultadas 17/11/2026). Iconos: logotipo de GitHub Actions y marca de GitHub (github/explore, octicons); Docker (docker.com); iconos genéricos de AWS Architecture Icons.""")
    return sl


ALT = [  # icono, nombre, subtítulo, acento, cómo, despliega, ideal
    ("gh-actions.png", "GitHub Actions", "runners de GitHub", AMBER,
     "YAML en el repo; cada job en una máquina limpia de GitHub.",
     "A cualquier sitio, con actions o comandos.",
     "el código está en GitHub y quieres PR, rulesets y OIDC juntos."),
    ("gh-cloudflare.png", "Cloudflare", "Workers Builds", CORAL,
     "Conectas el repo y cada push construye y despliega. Sin YAML.",
     "Solo a Cloudflare, con vista previa por rama.",
     "la aplicación vive en Cloudflare."),
    ("gh-gitlab.png", "GitLab CI/CD", "gitlab.com o autoalojado", VIOLET,
     ".gitlab-ci.yml; runners de GitLab o propios.",
     "A cualquier sitio; repo, CI y registro en una herramienta.",
     "el equipo ya trabaja en GitLab."),
    ("aws-codebuild.png", "AWS CodeBuild", "+ CodePipeline", BLUE,
     "buildspec.yml; CodePipeline encadena build y despliegue.",
     "A AWS, con roles de IAM y acceso a la VPC.",
     "todo está en AWS y no quieres un CI externo."),
    ("g-servers.png", "VPS propio", "runner, Jenkins o Coolify", MINT,
     "Runner self-hosted, Jenkins o un PaaS como Coolify en tu servidor.",
     "Donde quieras: máquina y red son tuyas.",
     "muchos minutos o red privada, y alguien que lo mantenga."),
]


EXTRA_ALT = {"GitHub Actions": ("≈ 2.000 min privados", 1), "Cloudflare": ("3.000 min/mes", 1),
             "GitLab CI/CD": ("400 min/mes", 2), "AWS CodeBuild": ("100 min/mes", 3),
             "VPS propio": ("0 · VPS 5,49 €/mes", 5)}


def s12b_alternativas(d):
    sl = d.slide(tag="alternativas")
    header(sl, "Alternativas · dónde ejecutar el CI/CD", "GitHub Actions no es la única forma de llegar a producción",
           "Todas reaccionan a un commit, comprueban, construyen y despliegan. Cambia dónde corre la máquina, quién la "
           "mantiene, hasta dónde puede desplegar y cómo se paga.")
    # eje gestionado ↔ control
    text(sl, 43, 128, 300, 12, "MÁS GESTIONADO · menos que mantener", size=8, color=MUTED, bold=True)
    text(sl, 617, 128, 300, 12, "MÁS CONTROL · más que mantener", size=8, color=MUTED, bold=True, align="r")
    line(sl, 43, 145, 917, 145, color=BORDER, w=1.5, head="both")
    w = (874 - 4 * 9) / 5
    x = 43
    for icon, name, sub, acc, como, dest, ideal in ALT:
        y = 153
        box(sl, x, y, w, 232, fill=CARD)
        box(sl, x, y, w, 3.5, fill=acc, radius=0)
        if icon == "g-servers.png":
            img(sl, icon, x + 10, y + 13, w=34, h=34)
            img(sl, "hetzner-logo.png", x + 52, y + 26, w=104)
        else:
            iw, ih = img_size(icon, h=38)
            img(sl, icon, x + (w - iw) / 2, y + 11, w=iw, h=ih)
        text(sl, x + 10, y + 55, w - 20, 16, name, size=12, color=TITLE, font=SERIF, align="c")
        text(sl, x + 10, y + 72, w - 20, 12, sub, size=8.3, color=acc, bold=True, align="c")
        text(sl, x + 10, y + 91, w - 20, 138, [
            {"runs": [("Cómo  ", {"bold": True, "color": acc}), (como, {})], "space": 5},
            {"runs": [("Despliega  ", {"bold": True, "color": acc}), (dest, {})], "space": 5},
            {"runs": [("Elígela si  ", {"bold": True, "color": acc}), (ideal, {})]}], size=9.2, color=TEXT, space=5)
        inc, lvl = EXTRA_ALT[name]
        box(sl, x + 10, 341, w - 20, 0.8, fill=BORDER, line=BORDER, radius=0)
        text(sl, x + 10, 346, w - 20, 13, [[("INCLUIDO  ", {"bold": True, "color": acc, "size": 7.5}),
                                            (inc, {"bold": True, "color": TITLE})]], size=9)
        text(sl, x + 10, 365, 90, 11, "LO QUE MANTIENES", size=7.5, color=MUTED, bold=True)
        for k in range(5):
            circle(sl, x + w - 58 + k * 10, 366.5, 7, acc if k < lvl else BORDER)
        x += w + 9
    chip(sl, 43 + w - 92, 138, 84, 13, "LA DE LA DEMO", fill=AMBER, color=DARK, size=7, radius=3)
    # notas inferiores
    box(sl, 43, 393, 431, 74, fill=CARD)
    box(sl, 43, 393, 3.5, 74, fill=MINT, radius=0)
    text(sl, 55, 400, 410, 12, "MISMO WORKFLOW, OTRA MÁQUINA", size=8.5, color=MINT, bold=True)
    code_panel(sl, 55, 415, 160, 20, ["runs-on: [self-hosted, linux]"], size=8, pad=5)
    text(sl, 222, 414, 245, 50, "Con un runner propio solo cambia esta línea: el YAML, los rulesets y OIDC siguen igual.",
         size=9.6, color=TEXT)
    text(sl, 55, 442, 410, 24, "Con Cloudflare o CodeBuild se reescribe la canalización en su formato.",
         size=9.6, color=MUTED)
    side_note(sl, 486, 393, 431, 74, "Ojo con el runner propio",
              "No es una máquina limpia en cada job y GitHub desaconseja usarlo en repositorios públicos: "
              "una PR ajena podría ejecutar código en tu servidor.", accent=CORAL, size=9.8)
    takeaway(sl, "Elegir CI/CD es elegir quién mantiene la máquina y hasta dónde despliega; las garantías de la clase no cambian.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, f"""
19:01–19:03. Ampliar la mirada antes de pasar al artefacto. Todas las opciones hacen el mismo trabajo (evento → comprobar → construir → desplegar); se diferencian en tres ejes: quién mantiene la máquina, hasta dónde pueden desplegar y cómo se paga. El eje de arriba va de lo más gestionado (GitHub, Cloudflare) a lo que mantienes tú (VPS).
GitHub Actions: la de la demo. Runners efímeros de GitHub; despliega a cualquier destino porque los pasos son comandos y actions.
Cloudflare Workers Builds: integración Git de Cloudflare; conectas un repositorio de GitHub o GitLab a un Worker y cada push construye y despliega, con vistas previas por rama y rollback a versiones anteriores desde el panel. No hay YAML que mantener, pero solo despliega en Cloudflare: nuestra imagen no iría a ECS desde ahí.
GitLab CI/CD: equivalente directo de Actions con .gitlab-ci.yml; útil si el repositorio está en GitLab.
AWS CodeBuild + CodePipeline: CI/CD dentro de la cuenta de AWS; los permisos son roles de IAM nativos y puede ejecutarse dentro de la VPC.
VPS propio: tres variantes. (1) Runner self-hosted de GitHub: el YAML no cambia, solo runs-on. (2) Jenkins u otro servidor de CI. (3) PaaS autoalojado tipo Coolify o Dokploy, que hace git pull, construye la imagen y la arranca en el propio servidor. Hetzner aparece como ejemplo de proveedor europeo de VPS (precio en la diapositiva siguiente).
Seguridad: la documentación de GitHub dice que los runners self-hosted casi nunca deben usarse en repositorios públicos, porque cualquiera que abra una PR podría ejecutar código en esa máquina, y que no garantizan una máquina limpia por job.
Pregunta: «Si mañana movemos la API a Cloudflare, ¿qué partes de la clase siguen valiendo?» (tests en cada cambio, artefacto inmutable, staging, logs y rollback: todo; cambia la herramienta).
Fuentes: https://developers.cloudflare.com/workers/ci-cd/builds/ · https://docs.github.com/en/actions/concepts/runners/self-hosted-runners · https://docs.github.com/en/actions/reference/security/secure-use · https://about.gitlab.com/pricing/ · https://aws.amazon.com/codebuild/pricing/ (consultadas 17/11/2026). {SRC_ALT}""")
    return sl


PRECIOS = [  # icono, opción, incluido, después, a favor, en contra
    ("gh-actions.png", "GitHub Actions\n(runners de GitHub)",
     "Públicos: gratis. Privados: 12 USD (≈ 2.000 min) en Free; 18 USD (≈ 3.000) en Pro y Team.",
     "0,006 USD/min Linux; 0,062 USD/min macOS.",
     "Integrado con PR, rulesets, environments y OIDC.",
     "Un YAML más; actions de terceros; macOS caro."),
    ("g-servers.png", "Runner propio\nen un VPS",
     "GitHub no cobra los minutos self-hosted.",
     "El servidor: desde 5,49 €/mes sin IVA (Hetzner).",
     "Tarifa plana, hardware a medida, caché y red privada.",
     "Lo mantienes tú; sin máquina limpia; nunca en repos públicos."),
    ("gh-cloudflare.png", "Cloudflare\nWorkers Builds",
     "Free: 3.000 min, 1 build. Workers Paid (5 USD/mes): 6.000 min, 6 a la vez.",
     "0,005 USD/min por encima de 6.000.",
     "Sin YAML; vista previa por rama; rollback de versiones.",
     "Solo Cloudflare; 20 min por build; no despliega en ECS."),
    ("gh-gitlab.png", "GitLab CI/CD",
     "Free: 400 min. Premium (29 USD/usuario/mes): 10.000 min.",
     "10 USD por cada 1.000 min más.",
     "Repo, CI, registro y entornos juntos.",
     "Hay que estar en GitLab; Free se queda corto."),
    ("aws-codebuild.png", "AWS CodeBuild\n(+ CodePipeline)",
     "Capa gratuita: 100 min/mes (general1.small).",
     "Ejemplo oficial: 0,005 USD/min; varía por región.",
     "IAM nativo, VPC y sin credenciales externas.",
     "Más piezas; CodePipeline se cobra aparte."),
]


def s12c_precios(d):
    sl = d.slide(tag="precios")
    header(sl, "Alternativas · precios y compromisos", "Cuánto cuesta cada opción y qué ganas o pierdes",
           "Precios oficiales consultados el 17/11/2026, en USD salvo el VPS (EUR sin IVA). Cambian a menudo: "
           "hay que comprobarlos antes de decidir.")
    wtag = len(TAGS["documentado"][0]) * 7.5 * 0.56 + 14
    tag(sl, 917 - wtag, 113, "documentado")
    rows = [["Opción", "Incluido al mes", "Después", "A favor", "En contra"]]
    for _, op, inc, des, fav, con in PRECIOS:
        rows.append([(op.replace("\n", " "), {"bold": True, "color": TITLE}), inc, des,
                     (fav, {"color": MINT_L}), (con, {"color": "F3B5A3"})])
    x0, rh = 79, 41
    gf = table(sl, x0, 132, 917 - x0, [1.05, 1.6, 1.15, 1.45, 1.6], rows, size=9, row_h=rh)
    gf.table.rows[0].height = P(22)
    for i, (icon, *_r) in enumerate(PRECIOS):
        y = 132 + 22 + rh * i
        box(sl, 43, y + 3, 30, rh - 6, fill=CARD2, radius=4)
        iw, ih = img_size(icon, h=22)
        img(sl, icon, 43 + (30 - iw) / 2, y + (rh - ih) / 2, w=iw, h=ih)
    # ejemplo de coste
    y0 = 375
    text(sl, 43, y0, 300, 12, "EJEMPLO · 5.000 MIN LINUX AL MES, REPO PRIVADO", size=8.5, color=AMBER, bold=True)
    tag(sl, 345, y0 - 1, "ilustrativo")
    bars = [("GitHub Actions (Free)", 18, "18 USD", AMBER, "30 − 12 incluidos"),
            ("Runner en VPS", 5.49, "5,49 €", MINT, "fijo, si un servidor basta"),
            ("Cloudflare (Paid)", 5, "5 USD", CORAL, "dentro de los 6.000 min"),
            ("GitLab (Free)", 50, "50 USD", VIOLET, "400 + 5 packs de 1.000"),
            ("AWS CodeBuild", 24.5, "24,5 USD", BLUE, "4.900 min × 0,005")]
    by, bmax = y0 + 19, 190
    for lab, v, vt, col, why in bars:
        text(sl, 43, by - 1.5, 118, 12, lab, size=8.6, color=TEXT, align="r", check=False)
        bw = max(3, bmax * v / 50)
        box(sl, 167, by, bw, 9.5, fill=col, radius=2)
        text(sl, 167 + bw + 5, by - 2, 220, 12, [[(vt + "  ", {"bold": True, "color": TITLE}), (why, {"color": MUTED})]],
             size=8.6, check=False)
        by += 14.5
    # cómo decidir
    box(sl, 560, y0, 357, 90, fill=CARD)
    box(sl, 560, y0, 3.5, 90, fill=AMBER, radius=0)
    text(sl, 572, y0 + 7, 340, 12, "CÓMO DECIDIR", size=8.5, color=AMBER, bold=True)
    bullets(sl, 572, y0 + 22, 338, 58, [
        [("Pocos minutos y código en GitHub", {"bold": True, "color": TITLE}), (" → runners de GitHub.", {})],
        [("App que vive en Cloudflare", {"bold": True, "color": TITLE}), (" → Workers Builds.", {})],
        [("Muchos minutos, hardware o red propios", {"bold": True, "color": TITLE}), (" → runner en un VPS, con alguien que lo mantenga.", {})]],
        size=9.4, mark_color=AMBER, space=3)
    takeaway(sl, "El precio por minuto pesa menos que las horas de quien mantiene la máquina: en equipos pequeños, lo gestionado suele salir más barato.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=2)
    notes(sl, f"""
19:03–19:05. Leer la tabla por filas y luego el ejemplo. Todas las cifras son de las páginas oficiales consultadas el 17/11/2026; el ejemplo de abajo es un cálculo ilustrativo, no una factura.
GitHub Actions: en repositorios públicos los runners estándar son gratis. En privados, cada plan incluye un importe mensual de uso: 12 USD en Free (≈ 2.000 min de Linux 2 núcleos a 0,006 USD/min), 18 USD en Pro y Team (≈ 3.000 min), 300 USD en Enterprise Cloud. macOS cuesta 0,062 USD/min. Los runners self-hosted no consumen ese importe.
Runner propio: GitHub no cobra sus minutos; pagas el servidor. Ejemplo: Hetzner Cloud anuncia planes Regular Performance desde 5,49 €/mes sin IVA (con el 21 % de IVA, unos 6,64 €). Coste oculto: actualizaciones, aislamiento entre jobs, discos llenos, monitorización.
Cloudflare Workers Builds: plan Free 3.000 min/mes, 1 build simultáneo, 2 vCPU; planes de pago 6.000 min/mes, 6 simultáneos, 4 vCPU y 0,005 USD/min extra. Límite de 20 min por build. Workers Paid tiene un cargo mínimo de 5 USD/mes por cuenta.
GitLab: Free 400 min de cómputo/mes; Premium 29 USD por usuario/mes (facturación anual) con 10.000 min; paquetes de 1.000 min por 10 USD.
AWS CodeBuild: capa gratuita de 100 min/mes en general1.small o arm1.small; la página oficial usa 0,005 USD/min en general1.small en su ejemplo (el precio depende de la región). CodePipeline se factura aparte.
Ejemplo (5.000 min Linux/mes en un repositorio privado, plan más barato que lo cubre): GitHub Free 5.000 × 0,006 = 30 USD − 12 incluidos = 18 USD; VPS 5,49 €/mes fijos si un servidor da abasto; Cloudflare Workers Paid 5 USD (5.000 < 6.000 incluidos; el plan Free no llega); GitLab Free 400 incluidos + 4.600 → 5 paquetes = 50 USD; CodeBuild (5.000 − 100) × 0,005 = 24,5 USD. No incluye impuestos, almacenamiento ni el tiempo de mantenimiento.
Pregunta: «¿Por qué el VPS, que parece el más barato, no es siempre la mejor opción?» (el coste real incluye horas de mantenimiento y riesgo de seguridad).
Fuentes: https://docs.github.com/en/billing/concepts/product-billing/github-actions · https://docs.github.com/en/billing/reference/actions-runner-pricing · https://developers.cloudflare.com/workers/ci-cd/builds/limits-and-pricing/ · https://developers.cloudflare.com/workers/platform/pricing/ · https://about.gitlab.com/pricing/ · https://aws.amazon.com/codebuild/pricing/ · https://www.hetzner.com/cloud/ (consultadas 17/11/2026; copias en .build/s18/investigacion/). {SRC_ALT}""")
    return sl


# ================================================================ introducción 20/11/2026 (petición de José)
def _stage(sl, cx, cy, icon, label, col, w=92):
    box(sl, cx - w / 2, cy - 12, w, 24, fill=CARD2, line=col, lw=1.25, radius=12)
    img(sl, icon, cx - w / 2 + 7, cy - 8, w=16, h=16)
    text(sl, cx - w / 2 + 27, cy - 12, w - 31, 24, label, size=9, color=TITLE, bold=True, anchor="m", check=False)


def s02a_que_es_cicd(d):
    sl = d.slide(tag="que-es-cicd")
    header(sl, "Punto de partida · qué es CI/CD", "CI/CD: del commit al usuario por un camino automático",
           "CI comprueba cada cambio en cuanto se propone. CD lo deja listo para publicar, o lo publica, sin pasos a mano. "
           "La monitorización cierra el círculo: dice si lo publicado funciona y de ahí sale el siguiente cambio.")
    # --- infografía: bucle infinito
    box(sl, 92, 160, 206, 186, fill=None, line=MINT, lw=9, radius=0, shape=MSO_SHAPE.OVAL)
    box(sl, 292, 160, 206, 186, fill=None, line=BLUE, lw=9, radius=0, shape=MSO_SHAPE.OVAL)
    text(sl, 145, 222, 100, 34, "CI", size=34, font=SERIF, color=MINT, align="c", check=False)
    text(sl, 130, 260, 130, 12, "integración continua", size=8.5, color=MINT_L, bold=True, align="c", check=False)
    text(sl, 345, 222, 100, 34, "CD", size=34, font=SERIF, color=BLUE, align="c", check=False)
    text(sl, 320, 260, 150, 12, "entrega y despliegue", size=8.5, color=BLUE, bold=True, align="c", check=False)
    _stage(sl, 195, 160, "g-source-code.png", "Código", MINT)
    _stage(sl, 92, 253, "docker-mark-white.png", "Construir", MINT)
    _stage(sl, 195, 346, "g-magnifier.png", "Probar", MINT)
    _stage(sl, 395, 160, "r-ecr-image.png", "Publicar", BLUE)
    _stage(sl, 498, 253, "r-ecs-service.png", "Desplegar", BLUE, w=96)
    _stage(sl, 395, 346, "g-metrics.png", "Monitorizar", AMBER, w=104)
    chip(sl, 250, 246, 90, 16, "cada cambio", fill=BG, color=MUTED, size=7.5, bold=True, line=BORDER)
    # --- leyenda
    leg = [(MINT, "CI · integración continua", "Cada cambio se integra a menudo y una máquina limpia lo construye y lo prueba. Si falla, no entra."),
           (BLUE, "CD · entrega o despliegue", "Lo que pasa CI queda como artefacto listo. Entrega: desplegar es un botón. Despliegue: es automático."),
           (AMBER, "Monitorización", "Mide lo que está en marcha y avisa si falla. Lo que descubre se convierte en el siguiente cambio.")]
    x = 43
    for col, t, b in leg:
        box(sl, x, 376, 168, 90, fill=CARD)
        box(sl, x, 376, 168, 3.5, fill=col, radius=0)
        text(sl, x + 10, 385, 150, 13, t, size=9.2, color=col, bold=True)
        text(sl, x + 10, 402, 150, 62, b, size=9.3, color=TEXT)
        x += 175
    # --- antes y después
    def lista(y, h, fill, col, lab, items, mark, res):
        box(sl, 571, y, 346, h, fill=fill)
        text(sl, 583, y + 9, 320, 13, lab, size=9, color=col, bold=True)
        text(sl, 583, y + 28, 324, h - 70, [{"runs": [(mark + "  ", {"color": col, "bold": True}), (it, {})], "space": 6}
                                           for it in items], size=10.2, color=TEXT, space=6)
        box(sl, 583, y + h - 34, 322, 0.8, fill=col, line=col, radius=0)
        text(sl, 583, y + h - 28, 322, 22, res, size=10.5, color=col, bold=True, anchor="m")
    lista(132, 160, CORAL_BG, CORAL, "SIN CI/CD", [
        "Se compila en un portátil y se copia al servidor a mano.",
        "Los tests se pasan cuando alguien se acuerda.",
        "Nadie sabe con certeza qué versión está en marcha.",
        "Volver atrás es repetirlo todo, deprisa y con miedo."], "✗",
        "Resultado: despliegues raros, grandes y con miedo.")
    lista(300, 166, TAKE_BG, MINT, "CON CI/CD Y MONITORIZACIÓN", [
        "Cada PR se construye y se prueba en una máquina limpia.",
        "Se publica un artefacto con huella (digest) que no cambia.",
        "Desplegar o volver atrás es un botón, y queda registrado.",
        "Los fallos aparecen en un panel antes que en el correo de un cliente."], "✓",
        "Resultado: despliegues frecuentes, pequeños y reversibles.")
    takeaway(sl, "CI responde «¿este cambio rompe algo?»; CD, «¿lo puedo publicar ya?»; la monitorización, «¿funciona ahora mismo?».",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """
18:33–18:35. Antes de cualquier herramienta, la idea completa en una imagen. El bucle infinito es la forma habitual de dibujar DevOps: a la izquierda el trabajo del equipo de desarrollo (código, construir, probar), a la derecha la operación (publicar, desplegar, monitorizar), y el bucle no termina: lo que se observa en producción genera el siguiente cambio.
CI (integración continua): integrar en main a menudo, en cambios pequeños, y que una máquina construya y pruebe cada uno. Su pregunta: ¿este cambio rompe algo?
CD tiene dos lecturas. Entrega continua: siempre hay un artefacto validado listo y desplegar es una decisión (un botón). Despliegue continuo: lo que pasa todas las comprobaciones se despliega solo. La demo hace entrega continua: a staging se despliega a mano desde main.
Monitorización: medir lo que está en marcha y avisar cuando se sale de lo normal; cierra el bucle.
Leer las dos columnas de la derecha como una historia: el mismo equipo antes y después. Cada línea de «con» corresponde a una parte de la clase: PR con tests (bloque 2), digest (bloque 3), despliegue y rollback (bloques 4 y 5), panel y alarma (bloque 5).
En vivo: nada; diapositiva conceptual. Iconos de las etapas: AWS Architecture Icons (ECR, ECS, métricas), Docker y pytest.
Pregunta: «¿Cómo se publica hoy el código en vuestro trabajo o en vuestros proyectos? ¿A cuál de las dos columnas se parece?».
Fuentes: https://dora.dev/guides/dora-metrics/ (cambios pequeños y frecuentes) · https://docs.github.com/en/actions/get-started/continuous-integration · https://aws.amazon.com/devops/continuous-delivery/ (consultadas 20/11/2026).""")
    return sl


def s02b_que_es_monitorizar(d):
    sl = d.slide(tag="que-es-monitorizar")
    header(sl, "Punto de partida · qué es monitorizar", "Monitorizar: enterarte del fallo antes que tus usuarios",
           "Monitorizar es medir de forma continua cómo se comporta el sistema en producción y avisar cuando algo se sale de lo "
           "normal. Un test comprueba lo que imaginamos; la monitorización descubre lo que nadie previó.")
    section_label(sl, 43, 134, 300, "Un panel mínimo: las cuatro señales doradas", color=AMBER)
    tag(sl, 340, 132, "ilustrativo")
    tiles = [("Latencia · p95", "820 ms", "cuánto tarda en responder", BLUE,
              [4, 5, 4, 6, 5, 5, 6, 7, 6, 8, 9, 8]),
             ("Tráfico", "42 req/min", "cuánta demanda recibe", MINT,
              [3, 4, 5, 5, 6, 6, 7, 6, 7, 8, 7, 8]),
             ("Errores · 5xx", "3,1 %", "cuántas peticiones fallan", CORAL,
              [1, 1, 1, 1, 1, 2, 1, 1, 1, 9, 10, 8]),
             ("Saturación · CPU", "71 %", "lo cerca que está del límite", VIOLET,
              [4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7])]
    tw, th = 222, 104
    for i, (lab, val, q, col, bars) in enumerate(tiles):
        x = 43 + (i % 2) * (tw + 10)
        y = 151 + (i // 2) * (th + 8)
        box(sl, x, y, tw, th, fill=CARD, line=CORAL if col == CORAL else None, lw=1.25)
        text(sl, x + 12, y + 9, 140, 12, lab.upper(), size=8, color=col, bold=True)
        text(sl, x + 12, y + 24, 140, 26, val, size=21, font=SERIF, color=TITLE)
        text(sl, x + 12, y + 52, 120, 24, q, size=8.3, color=MUTED)
        bx, bw, base = x + 132, 6.2, y + 92
        for k, v in enumerate(bars):
            hh = v * 5.6
            box(sl, bx + k * 7.3, base - hh, bw, hh, fill=col if (col != CORAL or v > 5) else BORDER, radius=0)
        if col == CORAL:
            img(sl, "r-cw-alarm.png", x + 190, y + 7, w=22, h=22)
    text(sl, 43, 370, 454, 12, "Latencia, tráfico, errores y saturación: las cuatro señales que propone el libro de SRE de Google.",
         size=8, color=MUTED)
    section_label(sl, 43, 388, 454, "En una aplicación de IA, además", color=AMBER)
    ai = [("g-document.png", "Tokens por consulta"), ("g-credentials.png", "Coste por día"),
          ("g-globe.png", "Latencia del modelo"), ("g-magnifier.png", "Calidad (S19)")]
    x = 43
    for ic, t in ai:
        box(sl, x, 405, 108, 60, fill=CARD)
        img(sl, ic, x + 41, 412, w=26, h=26)
        text(sl, x + 4, 442, 100, 20, t, size=8.4, color=TITLE, bold=True, align="c")
        x += 115.3
    # --- ciclo de un incidente
    section_label(sl, 513, 134, 404, "Qué hace la monitorización cuando algo falla", color=AMBER)
    steps = [("g-metrics.png", "Detectar", CORAL, "Una métrica cruza un umbral: por ejemplo, demasiadas respuestas 5xx en pocos minutos."),
             ("r-cw-alarm.png", "Avisar", AMBER, "La alarma notifica a una persona; nadie tiene que mirar el panel todo el día."),
             ("g-logs.png", "Diagnosticar", BLUE, "Con el request_id y la versión, los logs dicen qué petición falló y por qué."),
             ("r-ecs-service.png", "Recuperar", VIOLET, "Volver al artefacto anterior, que ya estaba probado: eso lo da CD."),
             ("g-source-code.png", "Aprender", MINT, "Se añade el test que faltaba: la próxima vez, CI lo para antes de publicar.")]
    y = 151
    line(sl, 535, 170, 535, 430, color=BORDER, w=2, head="none")
    for ic, t, col, b in steps:
        circle(sl, 520, y + 4, 30, CARD2, line=col, lw=1.5)
        img(sl, ic, 527, y + 11, w=16, h=16)
        box(sl, 560, y, 357, 54, fill=CARD)
        box(sl, 560, y, 3.5, 54, fill=col, radius=0)
        text(sl, 571, y + 6, 330, 14, t, size=10.5, color=col, bold=True)
        text(sl, 571, y + 22, 338, 30, b, size=8.8, color=TEXT)
        y += 63
    takeaway(sl, "CI/CD evita que lleguen los fallos que sabemos probar; la monitorización encuentra los que nadie previó.",
             label="Idea guía", lab_color=AMBER)
    footer(sl, block=1)
    notes(sl, """
18:35–18:37. Segunda mitad del título de la clase. Monitorizar es medir de forma continua el sistema en producción y avisar cuando se sale de lo normal. Los tests de CI solo comprueban lo que alguien imaginó; la monitorización detecta lo que nadie previó (en la demo, la prioridad «baja» que rompe la versión B).
Panel de la izquierda (valores ilustrativos, no medidos): las cuatro señales doradas del libro de SRE de Google. Latencia (cuánto tarda; mejor un percentil como p95 que la media), tráfico (cuánta demanda), errores (proporción de peticiones que fallan) y saturación (lo cerca que está del límite: CPU, memoria, cuota). El pico rojo es lo que dispara una alarma.
En una aplicación de IA hay señales propias: tokens por consulta, coste por día, latencia del proveedor del modelo y calidad de las respuestas (esta última se evalúa en S19).
Ciclo de un incidente, de arriba abajo: detectar, avisar, diagnosticar, recuperar y aprender. Es exactamente lo que se hará en vivo en el bloque 5: error de B, request_id, log, rollback y cambios/03 con el test que faltaba.
Las herramientas concretas (logs, métricas, trazas y error tracking) se ven en las diapositivas 30 a 35.
En vivo: nada; diapositiva conceptual.
Pregunta: «¿Qué preferís: una alarma que salta de más o una que no salta nunca?» (conectar con umbrales y fatiga de alertas).
Fuentes: https://sre.google/sre-book/monitoring-distributed-systems/ (las cuatro señales doradas) · https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html (consultadas 20/11/2026). Iconos: AWS Architecture Icons (CloudWatch, ECS e iconos generales) y pytest.""")
    return sl


CASOS = [
    ("g-source-code.png", "Un cambio rompe la API", ["CI"], MINT,
     "Lo descubre un cliente cuando ya está publicado.",
     "Un test falla en la pull request y el cambio no se integra."),
    ("gh-python.png", "Cambiar de modelo o de prompt", ["CI"], MINT,
     "«Parece que responde bien», y se publica.",
     "La canalización ejecuta tests y evaluaciones (S19); si empeora, no sale."),
    ("r-cw-alarm.png", "Un error a las tres de la mañana", ["MONITORIZACIÓN"], AMBER,
     "Nadie se entera hasta el lunes.",
     "La alarma de 5xx avisa y el log con request_id dice qué versión falló."),
    ("r-ecs-service.png", "Volver atrás en minutos", ["CD"], BLUE,
     "Recompilar la versión anterior a mano, con prisa.",
     "Se redespliega el digest anterior: la misma imagen que ya pasó las pruebas."),
    ("g-credentials.png", "La factura de tokens se dispara", ["MONITORIZACIÓN"], AMBER,
     "Se ve a final de mes, en la factura.",
     "Una métrica de tokens y coste por día con alarma de presupuesto."),
    ("g-users.png", "Publicar varias veces al día", ["CI", "CD"], VIOLET,
     "Se acumulan cambios y cada despliegue da miedo.",
     "Cambios pequeños y comprobados: publicar deja de ser un evento."),
]


def s02c_casos_de_uso(d):
    sl = d.slide(tag="casos-de-uso")
    header(sl, "Punto de partida · casos de uso", "Para qué sirve en la vida real: seis situaciones",
           "Situaciones típicas de un equipo que publica una aplicación con IA. En cada una, CI/CD evita que el problema "
           "llegue o acorta el arreglo, y la monitorización lo detecta.")
    cw, ch = (874 - 20) / 3, 117
    for i, (ic, t, tags, acc, sin, con) in enumerate(CASOS):
        x = 43 + (i % 3) * (cw + 10)
        y = 132 + (i // 3) * (ch + 8)
        box(sl, x, y, cw, ch, fill=CARD)
        box(sl, x, y, cw, 3.5, fill=acc, radius=0)
        circle(sl, x + 10, y + 12, 32, CARD2, line=acc, lw=1.25)
        img(sl, ic, x + 17, y + 19, w=18, h=18)
        text(sl, x + 50, y + 12, cw - 60, 15, t, size=11, color=TITLE, bold=True)
        tx = x + 50
        for tg in tags:
            tx += chip_tag(sl, tx, y + 29, tg, kind={"CI": "ok", "CD": "info", "MONITORIZACIÓN": "warn"}[tg]) + 5
        text(sl, x + 12, y + 52, cw - 24, 26, [[("Sin  ", {"bold": True, "color": CORAL}), (sin, {})]], size=8.8, color=TEXT)
        text(sl, x + 12, y + 80, cw - 24, 34, [[("Con  ", {"bold": True, "color": MINT}), (con, {})]], size=8.8, color=TITLE)
    # --- métricas DORA
    y0 = 382
    box(sl, 43, y0, 874, 86, fill=CARD, line=BORDER)
    text(sl, 55, y0 + 8, 520, 12, "CÓMO SE MIDE SI FUNCIONA · LAS CINCO MÉTRICAS DE DORA", size=8.5, color=AMBER, bold=True)
    tag(sl, 917 - 200, y0 + 6, "documentado", w=190, t="DOCUMENTACIÓN OFICIAL · dora.dev")
    mets = [("Tiempo de entrega del cambio", "del commit a producción", MINT),
            ("Frecuencia de despliegue", "cuántas veces se despliega", MINT),
            ("Recuperación de un fallo", "de un despliegue fallido a estar bien", MINT),
            ("Tasa de fallos del cambio", "despliegues que exigen intervención", CORAL),
            ("Tasa de retrabajo", "despliegues no planificados por incidentes", CORAL)]
    mw = (850 - 4 * 8) / 5
    x = 55
    for t, b, col in mets:
        box(sl, x, y0 + 27, mw, 50, fill=CARD2)
        box(sl, x, y0 + 27, 3, 50, fill=col, radius=0)
        text(sl, x + 9, y0 + 32, mw - 14, 14, t, size=8.8, color=TITLE, bold=True)
        text(sl, x + 9, y0 + 49, mw - 14, 26, b, size=8, color=TEXT)
        x += mw + 8
    takeaway(sl, "Rapidez (verde) y estabilidad (rojo) no compiten: cambios pequeños, comprobados y fáciles de deshacer mejoran las dos.",
             label="Idea guía")
    footer(sl, block=1)
    notes(sl, """
18:37–18:39. Bajar la teoría a situaciones reconocibles. Las seis tarjetas son casos típicos, no empresas concretas. Leer dos o tres en voz alta y preguntar cuál les ha pasado.
1 Un cambio rompe la API → CI (en la demo: cambios/01, dos tests en rojo). 2 Cambiar de modelo o de prompt → CI con evaluaciones (enlace con S19: precisión, fidelidad, regresión). 3 Error de madrugada → monitorización (alarma de 5xx y request_id; bloque 5). 4 Volver atrás → CD (rollback por digest). 5 Factura de tokens → monitorización de coste (alarma de presupuesto o métrica de tokens). 6 Publicar a menudo → CI y CD juntos.
Abajo, cómo mide la industria si esto funciona: las métricas de entrega de software de DORA (programa de investigación de Google Cloud). Hoy son cinco. Rapidez o throughput: tiempo de entrega del cambio (del commit a producción), frecuencia de despliegue y tiempo de recuperación de un despliegue fallido. Estabilidad o instability: tasa de fallos del cambio (despliegues que exigen intervención inmediata, como un rollback o un hotfix) y tasa de retrabajo (despliegues no planificados que se hacen por un incidente). DORA sustituyó el antiguo MTTR por el tiempo de recuperación de un despliegue fallido.
Mensaje: hacer cambios pequeños y comprobados mejora a la vez la rapidez y la estabilidad.
En vivo: nada; diapositiva conceptual.
Pregunta: «¿Cuál de estas seis situaciones os ha pasado ya?».
Fuentes: https://dora.dev/guides/dora-metrics/ · https://dora.dev/insights/dora-metrics-history (consultadas 20/11/2026). Iconos: AWS Architecture Icons (generales, CloudWatch, ECS) y logotipo de Python (github/explore).""")
    return sl
