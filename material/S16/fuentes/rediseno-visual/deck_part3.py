"""Diapositivas 25–33: bloque 4 (contenedores)."""
from deck_lib import *  # noqa: F401,F403


def code_block(sl, x, y, w, lines, size=10, pitch=None, color=TEXT, gutter=0):
    """Código con interlineado exacto para alinear los marcadores con cada línea."""
    pitch = pitch or round(size * 1.3, 1)
    text(sl, x + gutter, y, w - gutter, pitch * len(lines) + 6, "\n".join(lines), size=size, font=MONO, color=color,
         bold=True, check=False, lsp=Pt(pitch))
    return pitch


def line_badge(sl, x, y0, pitch, li, n, fill, d=12):
    badge(sl, x, y0 + li * pitch + (pitch - d) / 2, n, fill=fill, d=d, size=7)


def s25_div4(d):
    sl = divider(d, 4, "Contenedores", "De la imagen Docker a una tarea en Fargate",
                 "Docker, ECR, ECS, Fargate, los roles de la tarea y Secrets Manager.",
                 ["¿Qué diferencia hay entre imagen y contenedor?",
                  "¿Qué hace cada línea de nuestro Dockerfile?",
                  "¿Qué guardan ECR, la etiqueta y el digest?",
                  "¿Qué organiza ECS y qué aporta Fargate?",
                  "¿Quién lee el secreto y con qué rol?"],
                 [("docker-mark.png", "Docker"), ("aws-ecr.png", "Amazon ECR"), ("aws-ecs.png", "Amazon ECS"),
                  ("aws-fargate.png", "AWS Fargate"), ("aws-secrets.png", "Secrets\nManager")], "19:12–19:29")
    notes(sl, """
TIEMPO 19:12 (10 s). Bloque 4 de 6: Contenedores, de 19:12 a 19:29 (17 min). Es el bloque central del caso.
QUÉ EXPLICAR: construir (Docker) → almacenar (ECR) → describir y mantener la ejecución (ECS) → poner el cómputo (Fargate) → inyectar la clave (Secrets Manager) con el rol adecuado.
IMÁGENES: logotipo de Docker (docker.com, Docker-Logos-1.zip); AWS Architecture Icons: ECR, ECS, Fargate, Secrets Manager.""")
    return sl


def s26_docker(d):
    sl = d.slide(tag="docker")
    header(sl, "Docker", "Imagen y contenedor: el artefacto y su ejecución",
           "Un Dockerfile describe cómo construir una imagen. La imagen es un artefacto inmutable formado por capas; "
           "un contenedor es un proceso que se ejecuta a partir de ella con su propia configuración.")
    img(sl, "docker-logo-white.png", 793, 34, h=22)
    box(sl, 43, 146, 128, 150, fill=CARD)
    img(sl, "g-source-code.png", 89, 160, w=36, h=36)
    text(sl, 51, 204, 112, 18, "Dockerfile", size=13, font=SERIF, color=TITLE, align="c")
    text(sl, 51, 226, 112, 66, "La receta: base, dependencias, código y cómo arrancar.", size=9.5, color=TEXT, align="c")
    line(sl, 173, 221, 207, 221, color=MINT, w=1.5)
    text(sl, 170, 200, 40, 14, "build", size=9, font=MONO, color=MINT, bold=True, align="c", check=False)
    box(sl, 209, 146, 248, 150, fill=CARD)
    text(sl, 221, 152, 220, 14, "IMAGEN · capas de solo lectura", size=9, color=MINT, bold=True)
    layers = [("metadatos: USER 10001 · EXPOSE 8000 · CMD", BLUE_BG, BLUE),
              ("código de la API: src/", CORAL_BG, CORAL),
              ("dependencias de requirements.lock", AMBER_BG, AMBER),
              ("python:3.12-slim · base fijada por digest", TAKE_BG, MINT)]
    yy = 172
    for t, bg, col in layers:
        box(sl, 221, yy, 224, 24, fill=bg, line=col, lw=0.5, radius=3)
        text(sl, 229, yy + 5, 210, 14, t, size=9.5, color=TITLE, bold=True)
        yy += 29
    line(sl, 459, 221, 499, 221, color=MINT, w=1.5)
    text(sl, 456, 200, 46, 14, "run", size=9, font=MONO, color=MINT, bold=True, align="c", check=False)
    ctrs = [("Contenedor en el portátil", "API_MODE=demo · 127.0.0.1:8016 → 8000"),
            ("Tarea en Fargate", "API_MODE=real · clave inyectada · :8000")]
    for i, (t, b) in enumerate(ctrs):
        y = 146 + i * 80
        box(sl, 501, y, 416, 70, fill=GREEN_BG, line="2A5246")
        img(sl, "docker-mark-white.png", 513, y + 14, h=20)
        text(sl, 551, y + 10, 350, 18, t, size=12, color=TITLE, bold=True)
        text(sl, 551, y + 32, 360, 30, b, size=10, font=MONO, color=MINT_L, bold=True)
    text(sl, 501, 300, 416, 14, "Misma imagen, distinta configuración y distinto lugar de ejecución.", size=9.5, color=MUTED)
    cards = [("Dependencias", "Fijadas con versiones y hashes en requirements.lock. Reconstruir produce el mismo entorno.",
              "pip install --require-hashes \\\n  -r requirements.lock", AMBER),
             ("Arquitectura", "Un Mac con Apple Silicon construye arm64 por defecto. La tarea es X86_64.",
              "docker build --platform linux/amd64 \\\n  --provenance=false …", CORAL),
             ("Configuración", "Modo, modelo y versión llegan como variables al arrancar. La clave se inyecta; nunca se copia a una capa.",
              "docker compose up --build -d\n# local: 127.0.0.1:8016 → 8000", BLUE)]
    for i, (t, b, cmd, col) in enumerate(cards):
        x = 43 + i * 296
        box(sl, x, 324, 284, 142, fill=CARD)
        box(sl, x, 324, 4, 142, fill=col, radius=0)
        text(sl, x + 16, 334, 260, 18, t, size=14, font=SERIF, color=TITLE)
        text(sl, x + 16, 356, 258, 48, b, size=10.5, color=TEXT)
        box(sl, x + 14, 412, 258, 46, fill=BG, radius=3)
        text(sl, x + 22, 418, 246, 36, cmd, size=8.5, font=MONO, color=MINT_L, bold=True, check=False)
    takeaway(sl, "Cambiar el código no cambia una imagen ya construida: hay que reconstruir, publicar y reemplazar la ejecución.", "Idea guía")
    footer(sl, 26, 4)
    notes(sl, """
TIEMPO 19:12–19:14 (2 min).
QUÉ ES: Docker empaqueta una aplicación con su runtime y dependencias. Dockerfile = receta; imagen = artefacto inmutable en capas; contenedor = proceso en ejecución creado desde una imagen, con su configuración (variables, puertos, usuario). Un contenedor comparte el kernel del host; no es una máquina virtual completa.
QUÉ RESUELVE: «en mi máquina funciona». La misma imagen se ejecuta en el portátil (modo demo, puerto 127.0.0.1:8016 → 8000 con Compose) y en Fargate (modo real, con la clave inyectada).
ARQUITECTURA: en Apple Silicon el build por defecto es arm64; nuestra tarea declara X86_64, así que se construye con --platform linux/amd64 (también sería válido ARM64 si la tarea se configura así y se prueba).
CÓDIGO (opcional): abrir Dockerfile, .dockerignore y compose.yaml del proyecto. No es necesario construir en directo.
PREGUNTA: «Edito api.py y recargo la página. ¿Cambia lo que responde el contenedor?». Respuesta: no hasta reconstruir la imagen y reemplazar el contenedor.
FUENTES: Docker Docs, «Python language guide» (docs.docker.com/guides/python/) y «Multi-platform builds»; Dockerfile, compose.yaml y requirements.lock del repositorio 4-produccion-ia.
IMÁGENES: logotipo y marca de Docker (docker.com, media resources); icono genérico Source Code de AWS Architecture Icons.""")
    return sl


def s27_dockerfile(d):
    sl = d.slide(tag="dockerfile")
    header(sl, "Nuestro Dockerfile", "El Dockerfile de la API, línea a línea",
           "Es el archivo real del proyecto S16, abreviado solo en el digest y en dos argumentos. Cada instrucción responde "
           "a una decisión de reproducibilidad, seguridad o ejecución.")
    box(sl, 43, 136, 520, 330, fill="0B151B", line=BORDER)
    text(sl, 55, 144, 300, 12, "Dockerfile", size=9, color=MINT, bold=True, font=MONO)
    lines = ['FROM python:3.12-slim-bookworm@sha256:34386ef0…',
             'ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \\',
             '    PYTHONPATH=/app/src',
             'WORKDIR /app',
             'COPY requirements.lock ./',
             'RUN pip install --no-cache-dir --require-hashes \\',
             '    -r requirements.lock && useradd --uid 10001 …',
             'COPY --chown=10001:10001 src/ ./src/',
             'ARG APP_VERSION=desarrollo-local',
             'ENV APP_VERSION=${APP_VERSION} API_MODE=demo',
             'USER 10001:10001',
             'EXPOSE 8000',
             'HEALTHCHECK … urlopen("http://127.0.0.1:8000/health")',
             'CMD ["uvicorn", "curso_ia.api:create_app", "--factory",',
             '     "--host", "0.0.0.0", "--port", "8000", …]']
    y0 = 164
    pitch = code_block(sl, 43, y0, 515, lines, size=9.5, gutter=36)
    marks = {0: 1, 1: 2, 5: 3, 7: 4, 8: 5, 10: 6, 11: 7, 12: 8, 13: 9}
    for li, n in marks.items():
        line_badge(sl, 55, y0, pitch, li, n, AMBER)
    box(sl, 55, 362, 496, 96, fill=CARD)
    text(sl, 67, 370, 200, 12, ".dockerignore", size=9, color=MINT, bold=True, font=MONO)
    text(sl, 67, 386, 120, 66, "*\n!requirements.lock\n!src/\n!src/**", size=9.5, font=MONO, color=TEXT, bold=True)
    text(sl, 205, 386, 336, 66, "Lista de inclusión: se ignora todo salvo el lock y el código. .env, tests, evidencias "
                                "y materiales nunca entran en el contexto de build.", size=10.5, color=TEXT)
    ann = [("Base fijada", "FROM con digest: siempre la misma base."),
           ("Logs inmediatos", "Sin búfer: cada línea llega enseguida a CloudWatch."),
           ("Dependencias con hashes", "Si un paquete cambia, la instalación falla."),
           ("Solo el código", "COPY src/ con propietario 10001."),
           ("Versión", "Argumento de build visible en /health y en los logs."),
           ("Sin root", "El proceso corre como usuario 10001."),
           ("EXPOSE", "Documenta el puerto; no abre la red."),
           ("HEALTHCHECK", "Comprueba /health sin llamar al modelo."),
           ("Arranque", "uvicorn escucha en 0.0.0.0:8000 dentro del contenedor.")]
    y = 136
    for i, (t, b) in enumerate(ann):
        badge(sl, 578, y + 1, i + 1, fill=AMBER, d=15, size=8.5)
        text(sl, 600, y, 317, 34, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10.5, color=TEXT)
        y += 37
    takeaway(sl, "La imagen no contiene la clave del proveedor ni datos: solo runtime, dependencias fijadas y código.", "Idea guía")
    footer(sl, 27, 4)
    notes(sl, """
TIEMPO 19:14–19:16 (2 min).
QUÉ EXPLICAR: leer el Dockerfile del proyecto en orden. (1) FROM con digest: base exacta y reproducible. (2) Variables para no escribir bytecode y para que los logs salgan sin búfer (aparecen enseguida en CloudWatch). (3) pip install --require-hashes: dependencias del lock con sus hashes. (4) COPY solo de src/ con propietario 10001; .dockerignore funciona como lista de inclusión. (5) APP_VERSION como argumento de build: se ve en /health y en los logs. (6) USER 10001: no root. (7) EXPOSE documenta, no publica. (8) HEALTHCHECK local contra /health, sin llamar al proveedor. (9) CMD: uvicorn en 0.0.0.0:8000.
CÓDIGO: abrir el Dockerfile real y señalar el digest completo. No construir la imagen en directo si no es necesario.
PREGUNTA: «Si escribo la clave en un ENV del Dockerfile y la borro en una línea posterior, ¿desaparece de la imagen?». Respuesta: no; queda en el historial de capas.
FUENTES: Dockerfile y .dockerignore del repositorio 4-produccion-ia (verificados el 17/10/2026: build linux/amd64, usuario 10001:10001, healthcheck healthy); Docker Docs, «Dockerfile reference».
IMÁGENES: diapositiva de texto y código; sin imágenes externas.""")
    return sl


def s28_ecr(d):
    sl = d.slide(tag="ecr")
    header(sl, "Amazon ECR", "ECR: el registro donde guardamos las imágenes",
           "ECR almacena imágenes de contenedor en repositorios privados de nuestra cuenta y región. Guardar una imagen no "
           "ejecuta nada: es el almacén desde el que ECS la descargará.")
    ui_panel(sl, 43, 132, 500, 196, title="s16-lab · Images (2)", crumbs="Amazon ECR  ›  Private registry  ›  Repositories  ›  s16-lab")
    esquema_label(sl, 388, 135, w=150, t="ESQUEMA · valores de ejemplo")
    cols = [("Image tags", 90), ("Digest", 150), ("Pushed at", 130), ("Size (MB)", 70)]
    box(sl, 51, 190, 484, 18, fill="E9EBED", radius=0)
    x = 55
    for c, w in cols:
        text(sl, x, 193, w, 12, c, size=8.5, color=UI_LABEL, bold=True, check=False)
        x += w + 10
    rows = [["2026-11-12.1", "sha256:4b7e…e19a", "12 nov 2026, 17:40", "61,3"],
            ["2026-11-05.2", "sha256:c03d…7f21", "5 nov 2026, 10:12", "61,1"]]
    y = 208
    for r in rows:
        box(sl, 51, y, 484, 22, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=0)
        x = 55
        for (c, w), v in zip(cols, r):
            text(sl, x, y + 5, w, 12, v, size=9, color=UI_BLUE if c == "Image tags" else UI_TEXT,
                 font=MONO if c == "Digest" else SANS, bold=c == "Digest", check=False)
            x += w + 10
        y += 22
    badge(sl, 182, 169, 1, fill=AMBER, d=13, size=7.5)
    badge(sl, 120, 192, 2, fill=AMBER, d=13, size=7.5)
    badge(sl, 210, 192, 3, fill=AMBER, d=13, size=7.5)
    text(sl, 55, 262, 476, 60, "Tag immutability: Immutable  ·  Encryption: AES-256  ·  Scan on push: activado\n"
                               "(configuración de nuestra plantilla infra/s16/registro.json)", size=9, color=UI_LABEL, check=False)
    box(sl, 43, 338, 500, 128, fill=CARD, line=BORDER)
    text(sl, 55, 346, 400, 12, "URI DE LA IMAGEN QUE REFERENCIA LA TAREA", size=9, color=MINT, bold=True)
    segs = [("111122223333.dkr.ecr.eu-west-1.amazonaws.com", "registro privado: cuenta y región", BLUE),
            ("/s16-lab", "repositorio", CORAL), ("@sha256:4b7e…e19a", "digest: huella del contenido", MINT)]
    x = 55
    for s_, lab, col in segs:
        w = len(s_) * 5.75 + 10
        chip(sl, x, 366, w, 24, s_, fill=CARD2, color=col, size=9.5, font=MONO, radius=3, line=col)
        text(sl, x, 394, max(w, 100), 28, lab, size=9, color=col, bold=True)
        x += w + 4
    text(sl, 55, 426, 480, 36, "Con una etiqueta legible publicamos; con el digest desplegamos y comprobamos qué contenido corre.",
         size=10, color=TEXT)
    concepts = [("Repositorio", "Colección de imágenes con nombre dentro del registro privado de la cuenta y la región."),
                ("Etiqueta (tag)", "Nombre legible de una versión. Con «Immutable» no puede reasignarse a otro contenido."),
                ("Digest", "sha256 del manifiesto: identifica exactamente el contenido publicado.")]
    y = 132
    for i, (t, b) in enumerate(concepts):
        box(sl, 557, y, 360, 58, fill=CARD)
        badge(sl, 567, y + 9, i + 1, fill=AMBER, d=14, size=8)
        text(sl, 587, y + 8, 300, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, 569, y + 27, 340, 30, b, size=10, color=TEXT)
        y += 63
    box(sl, 557, 323, 360, 82, fill=CARD)
    text(sl, 569, 331, 330, 12, "CREATE REPOSITORY · QUÉ SE ELIGE", size=9, color=MINT, bold=True)
    text(sl, 569, 347, 340, 56, "Repository name · Image tag mutability (Mutable / Immutable) · Encryption configuration "
                                "(AES-256 / AWS KMS) · Image scanning (mejor a nivel de registro).", size=10, color=TEXT)
    cost_chip(sl, 557, 412, 360, "0,10 USD por GB-mes en eu-west-1 + transferencia fuera de la región. Una lifecycle policy borra versiones antiguas.",
              h=54, size=9.5)
    takeaway(sl, "La task definition referencia la imagen por digest: sabemos qué contenido exacto corre aunque alguien publique otra etiqueta.",
             "Idea guía")
    footer(sl, 28, 4)
    notes(sl, """
TIEMPO 19:16–19:18 (2 min). Recorrido en consola.
QUÉ ES: Amazon Elastic Container Registry, registro privado de imágenes OCI/Docker por cuenta y región. QUÉ RESUELVE: un almacén seguro, cercano a ECS, controlado con IAM. RELACIÓN: ECS (con el execution role) descarga desde aquí; la task definition guarda la URI. COSTE: GB-mes almacenados (0,10 USD/GB-mes en eu-west-1 según las tarifas leídas el 17/10/2026) y transferencia fuera de la región; una lifecycle policy evita acumular versiones.
CONSOLA: Amazon ECR › Private registry › Repositories (vacío en una cuenta nueva) → Create repository: Repository name, Image tag mutability (Mutable / Immutable, con exclusiones), Encryption configuration (AES-256 / AWS KMS) → Cancel. Mencionar Private registry › Settings › Scanning (configuración recomendada a nivel de registro).
SI HAY UN REPOSITORIO: Images → columnas Image tags, Digest, Pushed at, Size. Copiar el digest y compararlo con la task definition.
PREGUNTA: «¿Una imagen en ECR ya responde a HTTP?». Respuesta: no; es un artefacto almacenado.
FUENTES: Amazon ECR User Guide, «Creating an Amazon ECR private repository» (docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html) y «Image tag mutability»; plantilla infra/s16/registro.json (IMMUTABLE, ScanOnPush, AES256); datos/costes-ejemplo.json.
IMÁGENES: ESQUEMA propio del listado Images con etiquetas, digests, fechas y tamaños de ejemplo (no es una captura).""")
    return sl


def s29_ecs(d):
    sl = d.slide(tag="ecs")
    header(sl, "Amazon ECS y AWS Fargate", "ECS organiza la ejecución; Fargate pone el cómputo",
           "ECS es el orquestador: guarda definiciones, lanza tareas y mantiene servicios. Fargate es la capacidad donde "
           "corren esas tareas sin que veamos ni administremos servidores.")
    box(sl, 43, 136, 518, 236, fill=None, line=CORAL, lw=1, radius=0)
    img(sl, "aws-ecs.png", 43, 136, w=20, h=20)
    text(sl, 68, 140, 300, 12, "Cluster s16-lab", size=9.5, color=CORAL, bold=True)
    box(sl, 55, 164, 300, 196, fill=CARD, line=BORDER)
    img(sl, "r-ecs-service.png", 65, 172, w=26, h=26)
    text(sl, 97, 172, 250, 16, "Service s16-lab", size=11.5, color=TITLE, bold=True)
    text(sl, 97, 188, 250, 28, "desired count 1 · reemplaza tareas que fallan y despliega revisiones", size=9, color=TEXT)
    box(sl, 67, 226, 276, 122, fill=GREEN_BG, line="2A5246")
    img(sl, "r-ecs-container.png", 77, 236, w=30, h=30)
    img(sl, "docker-mark-white.png", 112, 242, h=16)
    text(sl, 150, 236, 186, 16, "Tarea · RUNNING", size=11.5, color=TITLE, bold=True)
    text(sl, 77, 272, 258, 72, "Una ejecución concreta de la revisión :3. Tiene su propia interfaz de red (ENI) con IP 10.216.0.x.",
         size=10, color=TEXT)
    box(sl, 377, 164, 172, 132, fill=CARD, line=BORDER)
    img(sl, "r-ecs-task.png", 389, 174, w=28, h=28)
    text(sl, 423, 174, 120, 30, "Task definition\ns16-lab:3", size=10.5, color=TITLE, bold=True)
    text(sl, 389, 210, 152, 80, "Plantilla versionada: imagen, CPU, memoria, puertos, variables, secretos y logs.", size=9.5, color=TEXT)
    line(sl, 376, 262, 345, 280, color=MINT, w=1.5)
    text(sl, 380, 302, 170, 40, "describe la tarea", size=9, color=MINT, bold=True)
    line(sl, 205, 349, 205, 384, color=MINT, w=1.5)
    text(sl, 212, 360, 120, 14, "se ejecuta en", size=9, color=MINT, bold=True, check=False)
    box(sl, 43, 386, 300, 80, fill=TAKE_BG, line=MINT, lw=1)
    img(sl, "aws-fargate.png", 55, 400, w=34, h=34)
    text(sl, 99, 396, 236, 16, "AWS Fargate", size=12, color=TITLE, bold=True)
    text(sl, 99, 414, 236, 48, "AWS pone el cómputo para cada tarea. No vemos ni parcheamos instancias.", size=10, color=TEXT)
    box(sl, 353, 386, 208, 80, fill=CARD, line=BORDER, dash=True)
    img(sl, "aws-ec2.png", 363, 400, w=28, h=28)
    text(sl, 399, 396, 156, 16, "EC2 (alternativa)", size=11, color=MUTED, bold=True)
    text(sl, 399, 414, 156, 48, "Instancias que administramos y registramos en el cluster.", size=9.5, color=MUTED)
    gl = [("Cluster", "Agrupación lógica donde viven servicios y tareas."),
          ("Task definition", "Receta versionada en revisiones (:1, :2, :3…). No se edita: se crea una revisión nueva."),
          ("Task", "Ejecución concreta. Estados: PROVISIONING → PENDING → RUNNING → STOPPED."),
          ("Service", "Mantiene N tareas, sustituye las que se paran y gestiona despliegues.")]
    y = 136
    for t, b in gl:
        box(sl, 575, y, 342, 60, fill=CARD)
        text(sl, 587, y + 8, 320, 16, t, size=11.5, color=CORAL, bold=True)
        text(sl, 587, y + 26, 322, 32, b, size=10, color=TEXT)
        y += 65
    cost_chip(sl, 575, 398, 342, "Fargate cobra vCPU-h y GB-h por segundo (mínimo 1 min) mientras la tarea existe. ECS no añade cargo propio.",
              h=68)
    takeaway(sl, "Fargate no es el modelo ni la API: es el cómputo que ejecuta el contenedor que ECS le pide.", "Idea guía")
    footer(sl, 29, 4)
    notes(sl, """
TIEMPO 19:18–19:20 (2 min).
QUÉ ES: Amazon ECS orquesta contenedores: guarda task definitions (recetas versionadas), lanza tareas (ejecuciones) y mantiene servicios (número deseado de tareas, sustitución y despliegues). AWS Fargate es una opción de capacidad: ejecuta cada tarea sin que administremos instancias; la alternativa es registrar instancias EC2 en el cluster. QUÉ RESUELVE: ejecutar la imagen de forma continua y recuperable. RELACIÓN: imagen en ECR, red en la VPC (modo awsvpc: una ENI por tarea), roles de IAM, secretos y logs. COSTE: Fargate factura vCPU-h y GB-h por segundo con mínimo de un minuto mientras la tarea existe; ECS no tiene cargo adicional.
CONSOLA: Amazon ECS › Clusters (vacío) → Create cluster: nombre e Infrastructure (AWS Fargate, Amazon EC2 instances) → Cancel. ECS › Task definitions (vacío). Si existe un cluster, Services › Deployments / Events y Tasks › Last status.
PREGUNTA: «Si una tarea se para por un error, ¿quién arranca otra?». Respuesta: el servicio, porque mantiene el desired count.
FUENTES: Amazon ECS Developer Guide, «What is Amazon ECS?» (capas de aprovisionamiento, controlador y capacidad), «Amazon ECS task lifecycle» y AWS Fargate Pricing (aws.amazon.com/fargate/pricing/); plantilla infra/s16/servicio.json (DesiredCount 1, LaunchType FARGATE).
IMÁGENES: AWS Architecture Icons: ECS, ECS Service, ECS Task, ECS Container, Fargate, EC2; marca de Docker.""")
    return sl


def s30_taskdef(d):
    sl = d.slide(tag="taskdef")
    header(sl, "Task definition", "La definición de tarea: la receta completa",
           "Es el documento que ECS usa para arrancar cada tarea. En la consola se lee en ECS › Task definitions › "
           "s16-lab › revisión › JSON. Estos son los valores de nuestra plantilla, abreviados.")
    box(sl, 43, 134, 492, 332, fill="0B151B", line=BORDER)
    lines = ['{',
             '  "family": "s16-lab",',
             '  "requiresCompatibilities": ["FARGATE"],',
             '  "runtimePlatform": {"cpuArchitecture": "X86_64",',
             '                      "operatingSystemFamily": "LINUX"},',
             '  "cpu": "256",  "memory": "512",',
             '  "networkMode": "awsvpc",',
             '  "executionRoleArn": "arn:aws:iam::…:role/…Execution…",',
             '  "taskRoleArn": "arn:aws:iam::…:role/…TaskRole…",',
             '  "containerDefinitions": [{',
             '    "name": "api",',
             '    "image": "…/s16-lab@sha256:4b7e…",',
             '    "user": "10001:10001", "readonlyRootFilesystem": true,',
             '    "portMappings": [{"containerPort": 8000}],',
             '    "environment": [{"name": "API_MODE", "value": "real"},',
             '                    {"name": "MODEL_ID", "value": "…"}],',
             '    "secrets": [{"name": "ANTHROPIC_API_KEY",',
             '                 "valueFrom": "arn:aws:secretsmanager:…"}],',
             '    "logConfiguration": {"logDriver": "awslogs",',
             '      "options": {"awslogs-group": "/thepower/s16-lab"}}',
             '  }]',
             '}']
    y0 = 142
    pitch = code_block(sl, 43, y0, 490, lines, size=9.5, pitch=14.2, gutter=30)
    groups = [(3, 1, AMBER), (6, 2, VIOLET), (7, 3, PINK), (11, 4, CORAL), (14, 5, BLUE), (16, 6, "F07B72"), (18, 7, MINT)]
    for li, n, col in groups:
        line_badge(sl, 51, y0, pitch, li, n, col)
    ann = [("Cómputo", "cpu 256 = 0,25 vCPU y 512 MiB. Linux X86_64 debe coincidir con la imagen.", AMBER),
           ("Red", "awsvpc: cada tarea tiene su ENI e IP. El puerto 8000 se declara en portMappings.", VIOLET),
           ("Identidad", "executionRoleArn lo usa ECS; taskRoleArn lo usa nuestro código.", PINK),
           ("Imagen", "Referencia por digest: el contenido exacto publicado en ECR.", CORAL),
           ("Configuración", "Variables visibles en la consola: modo, modelo y versión.", BLUE),
           ("Secretos", "Solo el ARN. ECS inyecta el valor al arrancar la tarea.", "F07B72"),
           ("Logs", "Driver awslogs hacia el grupo de CloudWatch del laboratorio.", MINT)]
    y = 134
    for i, (t, b, col) in enumerate(ann):
        box(sl, 549, y, 368, 43, fill=CARD)
        badge(sl, 558, y + 13, i + 1, fill=col, d=16)
        text(sl, 582, y + 5, 330, 36, [[(t + "  ", {"bold": True, "color": col}), (b, {})]], size=10, color=TEXT, anchor="m")
        y += 47.5
    takeaway(sl, "Las variables de entorno se ven en la consola; los secretos solo aparecen como una referencia ARN.", "Idea guía")
    footer(sl, 30, 4)
    notes(sl, """
TIEMPO 19:20–19:23 (3 min). Recorrido en consola.
QUÉ EXPLICAR: la task definition reúne todo lo necesario para arrancar: compatibilidad FARGATE, plataforma LINUX/X86_64, tamaño (cpu 256 = 0,25 vCPU; memory 512 MiB), modo de red awsvpc, los dos roles, y la definición del contenedor: imagen por digest, usuario 10001, raíz de solo lectura, puerto 8000, variables (API_MODE, MODEL_ID, APP_VERSION), secretos (ANTHROPIC_API_KEY desde un ARN de Secrets Manager), healthcheck y logs awslogs al grupo /thepower/<lab> con prefijo api.
CONSOLA: ECS › Task definitions › Create new task definition → recorrer Task definition family, Launch type (AWS Fargate), Operating system/Architecture, Task size (CPU, Memory), Task role, Task execution role, Container (Image URI, Port mappings, Environment variables con tipo Value o ValueFrom), Log collection → Cancel. Si existe una definición, abrir una revisión y la pestaña JSON.
SEÑALAR: que un secreto aparece como valueFrom con un ARN, nunca como valor.
PREGUNTA: «Cambio la memoria a 1024. ¿Se modifica la revisión 3?». Respuesta: no; se crea la revisión 4 y el servicio se actualiza para usarla.
FUENTES: plantilla infra/s16/servicio.json del proyecto; AWS CloudFormation, AWS::ECS::TaskDefinition; Amazon ECS Developer Guide, «Task definition parameters» y «Pass sensitive data to an Amazon ECS container».
IMÁGENES: diapositiva de código; JSON abreviado a partir de la plantilla real (los «…» sustituyen identificadores de cuenta y valores).""")
    return sl


def s31_roles(d):
    sl = d.slide(tag="roles")
    header(sl, "Identidades en ECS", "Execution role y task role: quién usa cada permiso",
           "Una tarea tiene dos roles. ECS usa el execution role para prepararla y arrancarla; nuestro código usa el task role "
           "cuando llama a servicios de AWS mientras se ejecuta.")
    box(sl, 43, 136, 478, 262, fill=VIOLET_BG)
    text(sl, 55, 146, 440, 12, "EXECUTION ROLE · lo usa el agente de ECS", size=9, color=VIOLET, bold=True)
    box(sl, 55, 166, 130, 220, fill=CARD)
    img(sl, "r-iam-role.png", 100, 186, w=40, h=40)
    text(sl, 61, 234, 118, 60, "Rol de ejecución de la tarea", size=11, color=TITLE, bold=True, align="c")
    text(sl, 61, 290, 118, 90, "Confía en ecs-tasks.amazonaws.com. Actúa antes y durante el arranque.", size=9.5, color=TEXT, align="c")
    tgt = [("aws-ecr.png", "ECR", "ecr:GetAuthorizationToken, BatchGetImage… · descargar la imagen"),
           ("aws-secrets.png", "Secrets Manager", "secretsmanager:GetSecretValue · leer el secreto al arrancar"),
           ("aws-cloudwatch.png", "CloudWatch Logs", "logs:CreateLogStream, PutLogEvents · enviar los logs"),
           ("aws-kms.png", "KMS (solo con clave propia)", "kms:Decrypt · descifrar el secreto")]
    y = 166
    for ic, t, b in tgt:
        line(sl, 186, 276, 214, y + 25, color=VIOLET, w=1.1)
        box(sl, 216, y, 293, 50, fill=CARD)
        img(sl, ic, 224, y + 10, w=28, h=28)
        text(sl, 260, y + 6, 240, 14, t, size=10.5, color=TITLE, bold=True)
        text(sl, 260, y + 22, 244, 26, b, size=8.5, color=TEXT)
        y += 56
    box(sl, 533, 136, 384, 262, fill=BLUE_BG)
    text(sl, 545, 146, 360, 12, "TASK ROLE · lo usa nuestro código", size=9, color=BLUE, bold=True)
    box(sl, 545, 166, 360, 92, fill=CARD)
    img(sl, "docker-mark-white.png", 557, 178, h=18)
    text(sl, 593, 176, 300, 16, "Nuestra API S16", size=12, color=TITLE, bold=True)
    text(sl, 557, 202, 340, 52, "No llama a ningún servicio de AWS: su task role no tiene permisos. La clave del modelo "
                                "le llega como variable inyectada.", size=10.5, color=TEXT)
    box(sl, 545, 266, 360, 120, fill=CARD)
    text(sl, 557, 274, 330, 12, "EJEMPLOS EN LOS QUE SÍ HARÍA FALTA", size=8.5, color=MUTED, bold=True)
    exs = [("aws-s3.png", "Leer un adjunto: s3:GetObject sobre un bucket concreto."),
           ("aws-bedrock.png", "Invocar un modelo en Bedrock (S17): bedrock:InvokeModel.")]
    yy = 294
    for ic, t in exs:
        img(sl, ic, 557, yy, w=26, h=26)
        text(sl, 591, yy + 2, 304, 40, t, size=10, color=TEXT)
        yy += 44
    box(sl, 43, 406, 300, 60, fill=AMBER_BG)
    text(sl, 55, 412, 280, 50, [[("OPERADOR  ", {"bold": True, "color": AMBER, "size": 9}),
                                 ("tu usuario o rol en la consola: crea, cambia y retira los recursos.", {})]], size=10.5, color=TITLE, anchor="m")
    box(sl, 351, 406, 566, 60, fill=CORAL_BG)
    text(sl, 363, 412, 546, 50, [[("ResourceInitializationError: unable to pull secrets or registry auth", {"font": MONO, "bold": True, "color": CORAL, "size": 9.5}),
                                  ("  →  revisar execution role, ARN, región, salida de red o KMS; no el task role.", {})]],
         size=10.5, color=TITLE, anchor="m")
    takeaway(sl, "Dar el permiso al rol equivocado no arregla nada: primero identificamos quién hace la llamada que falla.", "Idea guía")
    footer(sl, 31, 4)
    notes(sl, """
TIEMPO 19:23–19:25 (2 min).
QUÉ EXPLICAR: tres identidades. El operador crea los recursos. El execution role lo asume el agente de ECS/Fargate para descargar la imagen de ECR, crear el log stream y enviar logs a CloudWatch y leer secretos de Secrets Manager o Parameter Store al arrancar (más kms:Decrypt con una clave propia). El task role lo asume el código de la aplicación para llamar a APIs de AWS; nuestra API no las usa, así que no tiene permisos. Dar al task role acceso al secreto no arregla un fallo de arranque del execution role.
CONSOLA: IAM › Roles → buscar «ecsTaskExecutionRole» (puede no existir en una cuenta nueva) → Trust relationships (ecs-tasks.amazonaws.com) y la política gestionada AmazonECSTaskExecutionRolePolicy. En una task definition existente, los campos Task role y Task execution role.
ERROR REAL: «ResourceInitializationError: unable to pull secrets or registry auth» aparece en la razón de parada de la tarea cuando falla el execution role, el ARN, la región, la salida de red o KMS.
PREGUNTA: «¿Quién lee el secreto inyectado al arrancar?». Respuesta: el execution role (ECS), no nuestro código.
FUENTES: Amazon ECS Developer Guide, «Amazon ECS task execution IAM role» (docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html) y «Amazon ECS task IAM role»; plantilla infra/s16/servicio.json.
IMÁGENES: AWS Architecture Icons: IAM Role, ECR, Secrets Manager, CloudWatch, KMS, S3, Bedrock; marca de Docker.""")
    return sl


def s32_secrets(d):
    sl = d.slide(tag="secrets")
    header(sl, "AWS Secrets Manager", "Secrets Manager: la clave fuera de la imagen",
           "Guarda valores sensibles cifrados con KMS y controla con IAM quién puede leerlos. En clase mostramos metadatos "
           "y referencias; nunca pulsamos «Retrieve secret value».")
    ui_panel(sl, 43, 132, 470, 334, title="s16-lab/anthropic",
             crumbs="Secrets Manager  ›  Secrets  ›  s16-lab/anthropic")
    esquema_label(sl, 358, 135, w=150, t="ESQUEMA · nombres ficticios")
    box(sl, 51, 188, 454, 160, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    text(sl, 59, 194, 300, 14, "Secret details", size=10, color=UI_TEXT, bold=True)
    det = [("Encryption key", "aws/secretsmanager", 2), ("Secret name", "s16-lab/anthropic", 1),
           ("Secret description", "Clave del proveedor para el laboratorio S16 (ejemplo)", None),
           ("Last retrieved (UTC)", "—", None)]
    y = 214
    for lab, v, n in det:
        text(sl, 59, y, 150, 12, lab, size=8.5, color=UI_LABEL, bold=True, check=False)
        text(sl, 59, y + 12, 300, 12, v, size=9, color=UI_TEXT, check=False)
        if n:
            badge(sl, 59 + len(lab) * 4.9 + 6, y - 1, n, fill=AMBER, d=12, size=7)
        y += 30
    text(sl, 290, 214, 200, 12, "Secret ARN", size=8.5, color=UI_LABEL, bold=True, check=False)
    badge(sl, 344, 213, 1, fill=AMBER, d=12, size=7)
    text(sl, 290, 226, 186, 60, "arn:aws:secretsmanager:eu-west-1:\n111122223333:secret:\ns16-lab/anthropic-AbCdEf",
         size=8, font=MONO, color=UI_TEXT, bold=True, check=False)
    tabs = ["Overview", "Rotation", "Versions", "Replication", "Tags"]
    x = 51
    for i, t in enumerate(tabs):
        w = len(t) * 5.6 + 18
        box(sl, x, 354, w, 18, fill=UI_CARD if i == 0 else UI_BG, line="DDE1E5", lw=0.5, radius=0)
        text(sl, x + 8, 358, w - 8, 12, t, size=8.5, color=UI_BLUE if i == 0 else UI_TEXT, bold=i == 0, check=False)
        if t == "Rotation":
            badge(sl, x + w - 14, 357, 3, fill=AMBER, d=11, size=6.5)
        x += w + 2
    box(sl, 51, 380, 454, 76, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    text(sl, 59, 388, 300, 14, "Secret value", size=10, color=UI_TEXT, bold=True)
    text(sl, 59, 406, 260, 40, "El valor no se muestra hasta pulsar el botón; leerlo exige secretsmanager:GetSecretValue.",
         size=8.5, color=UI_MUTED, check=False)
    ui_button(sl, 340, 404, 130, "Retrieve secret value")
    chip(sl, 340, 424, 130, 12, "no pulsar en directo", fill=CORAL, color=DARK, size=7, radius=2)
    badge(sl, 478, 404, 4, fill=AMBER, d=14, size=8)
    box(sl, 527, 132, 390, 104, fill=CARD)
    text(sl, 539, 140, 360, 12, "CÓMO LLEGA EL VALOR A LA API", size=9, color=MINT, bold=True)
    nodes = [("aws-secrets.png", "Secreto\ncifrado"), ("aws-ecs.png", "ECS lo inyecta\nal arrancar"), ("docker-mark-white.png", "La API llama\nal modelo")]
    x = 539
    for i, (ic, t) in enumerate(nodes):
        if ic.startswith("docker"):
            img(sl, ic, x + 4, 164, h=18)
        else:
            img(sl, ic, x + 4, 158, w=28, h=28)
        text(sl, x + 40, 158, 82, 40, t, size=9, color=TITLE, bold=True)
        if i < 2:
            line(sl, x + 112, 172, x + 128, 172, color=MINT, w=1.25)
        x += 128
    text(sl, 539, 200, 370, 32, [[("Lo lee el execution role (GetSecretValue) y llega al contenedor como ", {}),
                                  ("ANTHROPIC_API_KEY", {"font": MONO, "bold": True, "color": MINT_L}), (".", {})]], size=9.5, color=TEXT)
    ann = [("Nombre y ARN", "La task definition guarda el ARN, que termina en 6 caracteres aleatorios."),
           ("Cifrado", "Clave aws/secretsmanager de KMS; una clave propia exige kms:Decrypt."),
           ("Rotación", "Cambiar el valor periódicamente. Las tareas en marcha conservan el anterior: hay que desplegar de nuevo."),
           ("Valor", "Leerlo exige permiso explícito. En clase no se muestra.")]
    y = 244
    for i, (t, b) in enumerate(ann):
        badge(sl, 529, y + 1, i + 1, fill=AMBER, d=15, size=8.5)
        text(sl, 551, y, 366, 40, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10, color=TEXT)
        y += 42
    cost_chip(sl, 527, 414, 390, "0,40 USD por secreto y mes + 0,05 USD por 10.000 llamadas (eu-west-1, tarifas del 17/10/2026).", h=52)
    takeaway(sl, "Una variable de entorno no es un secreto por sí misma: importa de dónde viene, quién la lee y que no quede en imagen, Git ni capturas.",
             "Idea guía")
    footer(sl, 32, 4)
    notes(sl, """
TIEMPO 19:25–19:27 (2 min). Recorrido en consola.
QUÉ ES: un almacén de secretos cifrados con KMS, con control de acceso por IAM, versiones y rotación. QUÉ RESUELVE: que la clave del proveedor no viva en el código, la imagen, Git ni las capturas. RELACIÓN: la task definition guarda el ARN en «secrets.valueFrom»; el execution role lo lee al arrancar; ECS lo entrega al contenedor como variable de entorno. Alternativa permitida por el ejercicio: Parameter Store (SecureString).
ROTACIÓN: Secrets Manager puede rotar automáticamente con una función Lambda o rotación gestionada para algunos servicios; una clave de un proveedor externo se rota generando una nueva en ese proveedor y actualizando el secreto. Las tareas que ya corren conservan el valor leído al arrancar: hay que forzar un nuevo despliegue.
CONSOLA: Secrets Manager › Secrets (vacío en una cuenta nueva) → Store a new secret: Secret type (Other type of secret), Key/value, Encryption key (aws/secretsmanager), Secret name y description, Configure rotation (opcional) → Cancel. Si existe un secreto de laboratorio, abrirlo y mostrar solo Secret details, Rotation y Versions. NO pulsar Retrieve secret value. Usar nombres ficticios.
BORRADO: el borrado se programa con una ventana de recuperación de 7 a 30 días.
PREGUNTA: «Hemos rotado la clave y la API sigue usando la antigua. ¿Por qué?». Respuesta: el valor se inyectó al arrancar; hay que reemplazar las tareas.
FUENTES: AWS Secrets Manager User Guide (create_secret, rotating secrets, delete secret); Amazon ECS Developer Guide, «Pass Secrets Manager secrets through Amazon ECS environment variables»; datos/costes-ejemplo.json (0,40 USD/secreto-mes; 0,000005 USD por llamada = 0,05 USD por 10.000).
IMÁGENES: ESQUEMA propio de la página de detalle con nombre, ARN y descripción ficticios (no es una captura); iconos de AWS Architecture Icons; marca de Docker.""")
    return sl


def s33_cadena(d):
    sl = d.slide(tag="cadena")
    header(sl, "De la imagen a la respuesta", "ECR → definición → servicio → tarea → red",
           "Así se relacionan las piezas del bloque. Cada flecha es una dependencia que podemos comprobar en la consola "
           "cuando algo no funciona.")
    nodes = [("aws-ecr.png", "Imagen", "s16-lab@sha256:4b7e…", "ECR › Repositories › s16-lab › Images"),
             ("r-ecs-task.png", "Task definition", "s16-lab:3", "ECS › Task definitions › s16-lab › JSON"),
             ("r-ecs-service.png", "Service", "desired count 1", "ECS › Clusters › s16-lab › Services › Events"),
             ("aws-fargate.png", "Tarea en Fargate", "RUNNING · ENI 10.216.0.x", "ECS › Tasks › (tarea) › Networking | Logs"),
             ("g-firewall.png", "Red", "SG :8000 /32 · ruta → igw", "VPC › Security groups · Route tables"),
             ("g-json-script.png", "Respuesta", "/health · /clasificar", "Navegador o curl (práctica opcional)")]
    w = 132
    gap = (874 - 6 * w) / 5
    for i, (ic, t, sub, path) in enumerate(nodes):
        x = 43 + i * (w + gap)
        hl = i == 3
        box(sl, x, 138, w, 168, fill=GREEN_BG if hl else CARD, line="2A5246" if hl else None)
        img(sl, ic, x + (w - 36) / 2, 150, w=36, h=36)
        text(sl, x + 6, 192, w - 12, 16, t, size=11, color=TITLE, bold=True, align="c")
        text(sl, x + 6, 210, w - 12, 28, sub, size=8.5, font=MONO, color=MINT_L, bold=True, align="c")
        box(sl, x + 6, 242, w - 12, 56, fill=BG, radius=3)
        text(sl, x + 10, 246, w - 20, 50, path, size=8.5, color=MUTED, align="c")
        if i < 5:
            line(sl, x + w + 1, 220, x + w + gap - 1, 220, color=MINT, w=1.5)
    tx = 43 + 3 * (w + gap) + w / 2
    box(sl, 286, 330, 170, 64, fill=CARD)
    img(sl, "aws-secrets.png", 296, 342, w=28, h=28)
    text(sl, 332, 338, 120, 54, "Secrets Manager\nal arrancar", size=10, color=TITLE, bold=True)
    poly(sl, [(456, 362), (tx - 12, 362), (tx - 12, 308)], color=CORAL, w=1.25, dash=True)
    chip(sl, 470, 368, 118, 18, "execution role", fill=VIOLET_BG, color=VIOLET, size=8.5)
    box(sl, 664, 330, 170, 64, fill=CARD)
    img(sl, "aws-cloudwatch.png", 674, 342, w=28, h=28)
    text(sl, 710, 338, 120, 54, "CloudWatch Logs\nuna línea por petición", size=10, color=TITLE, bold=True)
    poly(sl, [(tx + 12, 308), (tx + 12, 362), (664, 362)], color=BLUE, w=1.25, dash=True)
    box(sl, 43, 404, 874, 62, fill=AMBER_BG)
    text(sl, 55, 410, 850, 50,
         [[("PRÁCTICA OPCIONAL  ", {"bold": True, "color": AMBER, "size": 9}),
           ("Los scripts del proyecto crean estas piezas con CloudFormation y comprueban digest, tarea, salud y función. "
            "Hoy las leemos en la consola sin ejecutarlos; quien haga la práctica aportará su propia evidencia real.", {})]],
         size=10.5, color=TITLE, anchor="m")
    takeaway(sl, "Una imagen en ECR no responde a HTTP: hacen falta una revisión, un servicio, una tarea en marcha y una ruta permitida.",
             "Idea guía")
    footer(sl, 33, 4)
    notes(sl, """
TIEMPO 19:27–19:29 (2 min).
QUÉ EXPLICAR: síntesis del bloque. La imagen (ECR, identificada por digest) → la task definition la referencia → el service mantiene una tarea → la tarea corre en Fargate con su ENI → la red (security group, ruta, gateway) permite llegar → la API responde. Al arrancar, el execution role lee el secreto; durante la ejecución, cada petición deja una línea en CloudWatch Logs.
CONSOLA: si no hay recursos, recorrer las rutas indicadas bajo cada pieza mostrando los listados vacíos y señalar dónde aparecería cada dato (digest, revisión, Events del servicio, pestaña Networking de la tarea). Volver a la diapositiva 4 (mapa) para cerrar.
NO PRESENTAR COMO EJECUTADO: los materiales dejan pendiente el ensayo en AWS (push a ECR, despliegue, inferencia real y retirada). No mostrar recibos anteriores como si fueran un despliegue de hoy.
PREGUNTA: «La tarea está RUNNING pero /health no responde desde el portátil. ¿Qué pieza revisamos?». Respuesta: la red (IP pública, ruta, regla) y el puerto del contenedor.
FUENTES: plantillas infra/s16/registro.json y servicio.json; scripts/aws_lab.py (bootstrap, publicar, desplegar, estado, verificar, limpiar; requieren --execute); material/S16/verificacion.md (ensayo AWS pendiente).
IMÁGENES: AWS Architecture Icons: ECR, ECS Task, ECS Service, Fargate, Secrets Manager, CloudWatch; genéricos Firewall y JSON Script.""")
    return sl


PART3 = [s25_div4, s26_docker, s27_dockerfile, s28_ecr, s29_ecs, s30_taskdef, s31_roles, s32_secrets, s33_cadena]
