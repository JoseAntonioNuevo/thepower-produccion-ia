"""Diapositivas 14–24: bloque 2 (cómputo y datos) y bloque 3 (red)."""
from deck_lib import *  # noqa: F401,F403


def s14_div2(d):
    sl = divider(d, 2, "Cómputo y datos", "Máquinas, discos y objetos",
                 "EC2 y EBS para alojar una máquina; S3 para guardar archivos; y cuándo hace falta una base de datos.",
                 ["¿Qué alquilamos con una instancia EC2?",
                  "¿Qué campos del formulario fijan CPU, memoria, disco y red?",
                  "¿Qué es un volumen EBS y cuánto dura?",
                  "¿Cómo se organizan bucket, objeto y clave en S3?",
                  "Disco, objeto o base de datos: ¿qué usar para cada dato?"],
                 [("aws-ec2.png", "Amazon EC2"), ("aws-ebs.png", "Amazon EBS"), ("aws-s3.png", "Amazon S3"),
                  ("aws-rds.png", "Amazon RDS\n(en el mapa)")], "18:50–19:02")
    notes(sl, """
TIEMPO 18:50 (10 s). Bloque 2 de 6: Cómputo y datos, de 18:50 a 19:02 (12 min).
QUÉ EXPLICAR: nuestra API no necesita EC2 ni S3 en la arquitectura de laboratorio, pero son los servicios base de AWS y la forma más directa de entender qué hace Fargate por nosotros. RDS solo se sitúa en el mapa.
IMÁGENES: AWS Architecture Icons (31/07/2026): EC2, EBS, S3, RDS.""")
    return sl


def s15_ec2(d):
    sl = d.slide(tag="ec2")
    header(sl, "Amazon EC2", "EC2: una máquina virtual que administramos",
           "Una instancia EC2 es un servidor virtual. AWS opera el hardware; nosotros elegimos imagen, tamaño y red, "
           "y administramos el sistema operativo y todo lo que instalamos encima.")
    comps = [("r-ami.png", "AMI (imagen de la máquina)", "Plantilla con sistema operativo y software inicial. Fija la arquitectura: x86_64 o arm64 (Graviton).", AMBER),
             ("r-ec2-instance.png", "Tipo de instancia", "Familia y tamaño: vCPU y memoria. t3.small = 2 vCPU y 2 GiB; t4g.small es su equivalente arm64.", AMBER),
             ("r-ebs-vol.png", "Volumen EBS raíz", "El disco del sistema. Persiste aunque detengamos la instancia, y se sigue cobrando.", MINT),
             ("aws-vpc.png", "Red", "VPC, subred, security group e IP pública opcional: deciden quién puede conectar.", VIOLET)]
    y = 140
    for ic, t, b, col in comps:
        box(sl, 43, y, 270, 76, fill=CARD)
        box(sl, 43, y, 4, 76, fill=col, radius=0)
        img(sl, ic, 55, y + 10, w=28, h=28)
        text(sl, 91, y + 14, 216, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, 55, y + 42, 250, 32, b, size=9.5, color=TEXT)
        line(sl, 315, y + 38, 338, y + 38 if y < 250 else y + 38, color=col, w=1.25)
        y += 82
    box(sl, 340, 140, 186, 322, fill=GREEN_BG, line="2A5246")
    img(sl, "r-ec2-instance.png", 401, 154, w=64, h=64)
    text(sl, 352, 224, 162, 18, "Instancia EC2", size=15, font=SERIF, color=TITLE, align="c")
    specs = [("AMI", "Amazon Linux 2023 · x86_64"), ("Tipo", "t3.small · 2 vCPU · 2 GiB"),
             ("Disco", "EBS gp3 · 8 GiB"), ("Red", "subred · SG · IP pública"), ("Rol", "instance profile (opcional)")]
    yy = 252
    for k, v in specs:
        text(sl, 352, yy, 162, 12, k.upper(), size=8, color=MINT, bold=True)
        text(sl, 352, yy + 12, 162, 14, v, size=10, color=TITLE)
        yy += 41
    box(sl, 541, 140, 376, 176, fill=CARD)
    text(sl, 555, 150, 340, 12, "LO QUE NOS CORRESPONDE", size=9, color=CORAL, bold=True)
    items = ["Parches del sistema operativo y del runtime.",
             "Instalar Docker y arrancar la API, también tras un reinicio.",
             "Escalado, alta disponibilidad y copias de seguridad.",
             "Acceso seguro: claves SSH o Session Manager con un rol."]
    text(sl, 555, 170, 350, 140, [{"runs": [("•  ", {"color": CORAL, "bold": True}), (t, {})], "space": 5} for t in items],
         size=10.5, color=TEXT, space=5)
    box(sl, 541, 324, 376, 76, fill=CARD)
    text(sl, 555, 334, 340, 12, "CUÁNDO TIENE SENTIDO", size=9, color=MINT, bold=True)
    text(sl, 555, 350, 350, 46, "Control total del sistema, GPU, software que no cabe en un contenedor gestionado o cargas siempre encendidas.",
         size=10.5, color=TEXT)
    cost_chip(sl, 541, 408, 376, "Segundos en marcha (Linux, mínimo 60 s) + GB de EBS aprovisionados aunque esté detenida + IPv4 pública por hora.",
              h=54)
    takeaway(sl, "Con EC2 alquilamos una máquina; con Fargate, la ejecución de un contenedor. Cambia lo que administramos.", "Idea guía")
    footer(sl, 15, 2)
    notes(sl, """
TIEMPO 18:50–18:52 (2 min).
QUÉ ES: Amazon EC2 ofrece máquinas virtuales (instancias). QUÉ RESUELVE: disponer de un servidor sin comprar hardware. QUÉ ADMINISTRAMOS: sistema operativo, parches, Docker, el proceso de la API, reinicios, escalado y copias. RELACIÓN: usa una AMI (plantilla con SO y arquitectura), un tipo de instancia (vCPU y memoria), volúmenes EBS, una subred de una VPC, security groups y, opcionalmente, un rol (instance profile). COSTE: tiempo en marcha (facturación por segundo con mínimo de 60 s en Linux), EBS por GB aprovisionado aunque la instancia esté detenida, IPv4 pública por hora y tráfico de salida.
CONSOLA: EC2 › Dashboard (recursos de la región) → Instances (listado; en una cuenta vacía, «No instances»). Señalar columnas: Instance state, Instance type, Availability Zone, Public IPv4.
PREGUNTA: «Si detengo una instancia, ¿deja de costar todo?». Respuesta: deja de cobrarse el cómputo; el volumen EBS y una IP elástica asociada siguen generando coste.
FUENTES: Amazon EC2 User Guide (Instances, AMIs, Instance types); página de precios de EC2 On-Demand (facturación por segundo). t3.small y t4g.small: 2 vCPU y 2 GiB (EC2 Instance Types). El ejemplo de AMI y tamaños es ilustrativo.
IMÁGENES: AWS Architecture Icons: recursos EC2 AMI, EC2 Instance, EBS Volume e icono de servicio VPC.""")
    return sl


def s16_launch(d):
    sl = d.slide(tag="launch")
    header(sl, "EC2 en la consola", "Launch instance: cada sección es una decisión",
           "Abrimos EC2 › Instances › Launch instances y recorremos el formulario sin pulsar el botón final. "
           "Los nombres de las secciones son los de la consola en inglés.")
    ui_panel(sl, 43, 132, 480, 336, title="Launch an instance", crumbs="EC2  ›  Instances  ›  Launch an instance")
    esquema_label(sl, 368, 135)
    secs = [("Name and tags", "s16-api-ejemplo", "input"),
            ("Application and OS Images (Amazon Machine Image)", "Amazon Linux 2023 AMI · 64-bit (x86)", "select"),
            ("Instance type", "t3.small · 2 vCPU · 2 GiB Memory", "select"),
            ("Key pair (login)", "Select (o continuar sin par de claves)", "select"),
            ("Network settings", "VPC · Subnet · Auto-assign public IP · Firewall (security groups)", "input"),
            ("Configure storage", "1x  8  GiB  gp3   Root volume", "input"),
            ("Advanced details", "IAM instance profile · User data …", "input")]
    y = 186
    for i, (lab, val, kind) in enumerate(secs):
        box(sl, 51, y, 350, 37, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
        ui_field(sl, 58, y + 3, 330, lab, val, kind=kind)
        badge(sl, 405, y + 11, i + 1, fill=AMBER, d=15, size=8.5)
        y += 40
    box(sl, 427, 186, 88, 120, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
    text(sl, 433, 192, 80, 12, "Summary", size=9.5, color=UI_TEXT, bold=True)
    text(sl, 433, 208, 80, 40, "Number of instances\n1", size=8, color=UI_LABEL, check=False)
    ui_button(sl, 433, 250, 76, "Cancel")
    ui_button(sl, 433, 272, 76, "Launch instance", primary=True, size=7.5)
    chip(sl, 433, 292, 76, 11, "no pulsar", fill=CORAL, color=DARK, size=7, radius=2)
    ann = [("Name and tags", "Etiquetas para encontrar el recurso y repartir costes por proyecto."),
           ("AMI", "Sistema operativo y arquitectura. La imagen Docker que ejecutemos debe ser compatible."),
           ("Instance type", "Fija vCPU y memoria y, con ello, el precio por segundo."),
           ("Key pair", "Acceso SSH. Alternativa sin claves: Session Manager con un rol en la instancia."),
           ("Network settings", "Subred, IP pública y security group: aquí se decide si es alcanzable."),
           ("Configure storage", "Volumen EBS raíz: tamaño, tipo y si se borra al terminar la instancia."),
           ("Advanced details", "Rol de la instancia (instance profile) y script de arranque (user data).")]
    y = 136
    for i, (t, b) in enumerate(ann):
        badge(sl, 540, y + 2, i + 1, fill=AMBER, d=16)
        text(sl, 564, y, 353, 46, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10.5, color=TEXT)
        y += 47
    takeaway(sl, "Este formulario reúne cómputo, disco, red e identidad: las mismas piezas que luego configuraremos en ECS.", "Idea guía")
    footer(sl, 16, 2)
    notes(sl, """
TIEMPO 18:52–18:55 (3 min). Recorrido en consola.
CONSOLA: EC2 › Instances › Launch instances. Comprobar antes la región (Europa · Irlanda). Recorrer de arriba abajo:
1 Name and tags: nombre y etiquetas (Project, Lab) para buscar y repartir costes.
2 Application and OS Images: Quick Start, Amazon Linux 2023; señalar «64-bit (x86)» frente a «64-bit (Arm)».
3 Instance type: desplegar y señalar vCPU y memoria; «Compare instance types» muestra precios por región.
4 Key pair (login): no crear claves en directo.
5 Network settings: pulsar «Edit» para ver VPC, Subnet, Auto-assign public IP y Firewall (security groups). Relacionar con el bloque 3.
6 Configure storage: tamaño y tipo del volumen raíz (gp3). En «Advanced» aparece Delete on termination y el cifrado.
7 Advanced details: IAM instance profile y User data.
Panel Summary: número de instancias y botón Launch instance. NO PULSAR. Salir con Cancel.
SI LA CUENTA ESTÁ VACÍA: el formulario funciona igual; no hace falta ningún recurso previo (la VPC por defecto aparece en Network settings).
PREGUNTA: «¿Qué sección decide si podremos conectarnos desde el navegador?». Respuesta: Network settings (IP pública y security group), además de la ruta de la subred.
FUENTES: Amazon EC2 User Guide, «Launch an EC2 instance using the launch instance wizard in the console» (docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-instance-wizard.html). Los valores del esquema son ilustrativos.
IMÁGENES: ESQUEMA propio de la pantalla (no es una captura); los nombres de sección proceden de la documentación oficial.""")
    return sl


def s17_ebs(d):
    sl = d.slide(tag="ebs")
    header(sl, "Amazon EBS", "EBS: el disco persistente de una instancia",
           "Un volumen EBS es almacenamiento de bloques: la instancia lo ve como un disco con sistema de archivos. "
           "Vive en una zona de disponibilidad y se conecta a instancias de esa misma zona.")
    box(sl, 43, 140, 450, 168, fill=None, line="00A4A6", lw=1, radius=0, dash=True)
    text(sl, 53, 146, 300, 12, "Zona de disponibilidad eu-west-1a", size=9, color="5FD0D2", bold=True)
    box(sl, 60, 168, 150, 126, fill=CARD)
    img(sl, "r-ec2-instance.png", 111, 180, w=48, h=48)
    text(sl, 66, 234, 138, 56, "Instancia EC2\nla ve como /dev/xvda", size=10, color=TITLE, align="c", bold=True)
    line(sl, 212, 231, 300, 231, color=MINT, w=1.5, head="both")
    text(sl, 216, 210, 84, 14, "conectado", size=9, color=MINT, align="c", bold=True)
    box(sl, 302, 168, 176, 126, fill=CARD)
    img(sl, "r-ebs-vol.png", 366, 180, w=48, h=48)
    text(sl, 308, 234, 164, 56, "Volumen gp3 · 20 GiB\ncifrado · persiste al detener", size=10, color=TITLE, align="c", bold=True)
    line(sl, 390, 296, 390, 330, color=BLUE, w=1.25)
    box(sl, 302, 330, 191, 64, fill=BLUE_BG)
    img(sl, "r-ebs-snap.png", 312, 342, w=34, h=34)
    text(sl, 352, 336, 136, 56, "Snapshot: copia incremental guardada por AWS en la región", size=9.5, color=TITLE)
    line(sl, 300, 362, 222, 362, color=BLUE, w=1.25)
    box(sl, 43, 330, 176, 64, fill=CARD)
    text(sl, 53, 336, 160, 56, "Con un snapshot creamos un volumen nuevo en otra zona.", size=9.5, color=TEXT)
    console_panel(sl, 43, 402, 450, 64, "EC2 › Elastic Block Store › Volumes | Snapshots", [], size=10)
    box(sl, 508, 140, 409, 128, fill=CARD)
    text(sl, 520, 150, 380, 12, "TIPOS HABITUALES", size=9, color=MINT, bold=True)
    types = [("gp3", "SSD de uso general; incluye 3.000 IOPS y 125 MiB/s, ampliables pagando aparte."),
             ("io2", "SSD con IOPS altas y garantizadas para bases de datos exigentes."),
             ("st1 · sc1", "HDD para lectura secuencial o datos fríos.")]
    yy = 168
    for t, b in types:
        text(sl, 520, yy, 70, 14, t, size=10.5, font=MONO, color=MINT_L, bold=True)
        text(sl, 592, yy, 316, 30, b, size=10, color=TEXT)
        yy += 32
    box(sl, 508, 276, 409, 86, fill=CARD)
    text(sl, 520, 286, 380, 12, "QUÉ DECIDIMOS AL CREARLO", size=9, color=AMBER, bold=True)
    text(sl, 520, 304, 386, 54, "Tamaño, tipo y rendimiento, cifrado con KMS y si se borra al terminar la instancia (Delete on termination).",
         size=10.5, color=TEXT)
    box(sl, 508, 370, 409, 44, fill=TAKE_BG)
    text(sl, 520, 374, 390, 36, [[("En nuestra API: ", {"bold": True, "color": MINT_L}),
                                  ("Fargate da 20 GiB de almacenamiento efímero por tarea y la API no guarda estado: no usamos EBS.", {})]],
         size=10, color=TITLE, anchor="m")
    cost_chip(sl, 508, 420, 409, "GB-mes aprovisionados (no usados) + IOPS y rendimiento extra en gp3 + snapshots.", h=44)
    takeaway(sl, "Un volumen EBS se paga por lo que reservamos, esté la instancia encendida o no.", "Idea guía")
    footer(sl, 17, 2)
    notes(sl, """
TIEMPO 18:55–18:57 (2 min).
QUÉ ES: almacenamiento de bloques para instancias EC2. QUÉ RESUELVE: un disco persistente que sobrevive a la detención de la instancia. RELACIÓN: un volumen está en una zona de disponibilidad y se conecta a instancias de esa zona (Multi-Attach es un caso especial de io1/io2). Los snapshots son copias incrementales que AWS guarda en la región y permiten crear volúmenes en otra zona. El almacén de instancia (instance store) de algunos tipos es local y efímero. COSTE: GB-mes aprovisionados, rendimiento extra en gp3 (por encima de 3.000 IOPS y 125 MiB/s) y snapshots almacenados.
CONSOLA: EC2 › Elastic Block Store › Volumes (vacío en una cuenta nueva) → Create volume: señalar Volume type, Size, IOPS, Throughput, Availability Zone y Encryption. Cancel. Mostrar también Snapshots.
NUESTRA API: Fargate (plataforma 1.4.0) da 20 GiB de almacenamiento efímero por tarea; nuestra API no escribe datos persistentes y usa raíz de solo lectura.
PREGUNTA: «¿Puedo conectar un volumen de eu-west-1a a una instancia de eu-west-1b?». Respuesta: no directamente; snapshot y nuevo volumen en la otra zona.
FUENTES: Amazon EBS User Guide (volume types, snapshots); Amazon ECS Developer Guide, «Fargate task ephemeral storage».
IMÁGENES: AWS Architecture Icons: EC2 Instance, EBS Volume, EBS Snapshot.""")
    return sl


def s18_s3(d):
    sl = d.slide(tag="s3")
    header(sl, "Amazon S3", "S3: objetos dentro de buckets",
           "S3 guarda objetos: un archivo con sus metadatos, identificado por una clave dentro de un bucket. "
           "Se lee y se escribe por HTTPS con la API; no se monta como el disco de una instancia.")
    box(sl, 43, 140, 524, 326, fill=CARD)
    img(sl, "r-s3-bucket.png", 57, 152, w=40, h=40)
    text(sl, 105, 152, 200, 12, "BUCKET", size=8.5, color=MINT, bold=True)
    text(sl, 105, 166, 330, 18, "thepower-s16-soporte-ejemplo", size=13, font=MONO, color=TITLE, bold=True)
    chip(sl, 470, 158, 84, 20, "eu-west-1", fill=TAKE_BG, color=MINT_L, size=9.5, font=MONO)
    text(sl, 57, 204, 300, 12, "CLAVE (KEY) DEL OBJETO", size=8.5, color=MUTED, bold=True)
    text(sl, 424, 204, 80, 12, "TIPO", size=8.5, color=MUTED, bold=True)
    text(sl, 494, 204, 60, 12, "TAMAÑO", size=8.5, color=MUTED, bold=True, align="r")
    objs = [("g-camera.png", "adjuntos/2026/11/inc-0142/", "captura.png", "Imagen", "412 KB"),
            ("g-multimedia.png", "adjuntos/2026/11/inc-0142/", "nota-voz.m4a", "Audio", "1,8 MB"),
            ("g-document.png", "documentos/", "politica-reembolsos-v3.pdf", "Documento", "236 KB"),
            ("g-data-table.png", "datasets/clasificacion/", "train-2026-10.jsonl", "Dataset", "48 MB")]
    y = 220
    for ic, pre, nm, tp, sz in objs:
        box(sl, 55, y, 500, 30, fill=CARD2)
        img(sl, ic, 63, y + 6, w=18, h=18)
        text(sl, 89, y + 8, 330, 14, [[(pre, {"color": AMBER}), (nm, {"color": TITLE})]], size=10, font=MONO, bold=True)
        text(sl, 424, y + 8, 70, 14, tp, size=10, color=TEXT)
        text(sl, 494, y + 8, 54, 14, sz, size=10, color=TEXT, align="r")
        y += 34
    text(sl, 57, 362, 496, 100,
         [{"runs": [("Prefijo ", {"bold": True, "color": AMBER}),
                    ("(en ámbar): parece una carpeta, pero forma parte de la clave.", {})], "space": 4},
          {"runs": [("Objeto ", {"bold": True, "color": TITLE}),
                    ("= datos + metadatos: tipo de contenido, tamaño, cifrado y versión.", {})], "space": 4},
          {"runs": [("Acceso ", {"bold": True, "color": TITLE}),
                    ("con la API por HTTPS: PUT, GET, LIST… nunca montando el bucket como un disco.", {})]}],
         size=10.5, color=TEXT, space=4)
    props = [("Región", "El bucket vive en una región elegida al crearlo."),
             ("Nombre", "Único en la partición (por defecto) o en el espacio regional de la cuenta."),
             ("Acceso público", "Bloqueado por defecto con Block Public Access."),
             ("Cifrado", "Los objetos nuevos se cifran como mínimo con SSE-S3."),
             ("Versionado", "Opcional: conserva versiones anteriores de cada objeto.")]
    y = 140
    for t, b in props:
        box(sl, 579, y, 338, 50, fill=CARD)
        text(sl, 591, y + 7, 100, 14, t, size=10.5, color=MINT, bold=True)
        text(sl, 591, y + 23, 318, 26, b, size=10, color=TEXT)
        y += 55
    cost_chip(sl, 579, 418, 338, "GB-mes según la clase de almacenamiento + peticiones + salida a Internet.", h=48)
    takeaway(sl, "S3 no es el disco de una instancia (EBS) ni una base de datos (RDS). En nuestra API guardaría los adjuntos.", "Idea guía")
    footer(sl, 18, 2)
    notes(sl, """
TIEMPO 18:57–18:59 (2 min).
QUÉ ES: almacenamiento de objetos. Bucket = contenedor con nombre en una región; objeto = datos + metadatos; clave = nombre completo del objeto dentro del bucket. Los prefijos (adjuntos/2026/11/…) se muestran como carpetas, pero son parte de la clave. QUÉ RESUELVE: guardar documentos, imágenes, audios, datasets o copias, a cualquier escala, por HTTPS. RELACIÓN: IAM y políticas de bucket controlan el acceso; KMS si se usa SSE-KMS; CloudFront o aplicaciones lo leen. COSTE: GB-mes según clase (Standard, Intelligent-Tiering, Glacier…), peticiones y transferencia de salida.
CONSOLA: S3 › General purpose buckets. En una cuenta vacía, el listado vacío y el botón «Create bucket». Si existe algún bucket, abrir Objects y Properties (Bucket Versioning, Default encryption) y Permissions (Block public access, Bucket policy). No subir archivos.
PREGUNTA: «¿Guardaríamos aquí la clave de Anthropic?». Respuesta: no; las claves van a Secrets Manager con permisos específicos.
FUENTES: Amazon S3 User Guide, «Buckets overview», «Creating a general purpose bucket» y «Namespaces for general purpose buckets» (docs.aws.amazon.com/AmazonS3/latest/userguide/). Nombres de bucket, claves y tamaños ficticios.
IMÁGENES: AWS Architecture Icons: S3 Bucket with objects y genéricos Camera, Multimedia, Document y Data Table.""")
    return sl


def s19_bucket(d):
    sl = d.slide(tag="bucket")
    header(sl, "S3 en la consola", "Create bucket: región, permisos, versionado y cifrado",
           "S3 › General purpose buckets › Create bucket. Recorremos las opciones y cancelamos. Las opciones por "
           "defecto ya bloquean el acceso público y cifran los objetos nuevos.")
    ui_panel(sl, 43, 132, 480, 336, title="Create bucket", crumbs="Amazon S3  ›  General purpose buckets  ›  Create bucket")
    esquema_label(sl, 368, 135)
    secs = [("AWS Region", "Europe (Ireland) eu-west-1", "input", None),
            ("Bucket name", "thepower-s16-soporte-ejemplo", "input", None),
            ("Object Ownership", [("ACLs disabled (recommended)", True), ("ACLs enabled", False)], "radio", None),
            ("Block Public Access settings for this bucket", [("Block all public access (incluye las 4 opciones)", True)], "check", None),
            ("Bucket Versioning", [("Disable", True), ("Enable", False)], "radio", None),
            ("Default encryption", [("SSE-S3", True), ("SSE-KMS", False), ("DSSE-KMS", False)], "radio", None)]
    y = 186
    for i, (lab, val, kind, hint) in enumerate(secs):
        box(sl, 51, y, 400, 37, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=3)
        ui_field(sl, 58, y + 3, 380, lab, val, kind=kind, lw=260)
        badge(sl, 457, y + 11, i + 1, fill=AMBER, d=15, size=8.5)
        y += 40
    ui_button(sl, 300, 434, 66, "Cancel")
    ui_button(sl, 372, 434, 84, "Create bucket", primary=True)
    chip(sl, 462, 437, 54, 11, "no pulsar", fill=CORAL, color=DARK, size=7, radius=2)
    ann = [("Región", "Se fija al crear el bucket. Los objetos no salen de ella salvo copia explícita."),
           ("Nombre", "3–63 caracteres en minúsculas; aparece en las URL. No se puede cambiar."),
           ("Propiedad de objetos", "Con las ACL desactivadas, el acceso se concede solo con políticas."),
           ("Bloqueo de acceso público", "Activado por defecto. Desactivarlo exige un motivo y un permiso específico."),
           ("Versionado", "Permite recuperar borrados o sobrescrituras; cada versión ocupa y se cobra."),
           ("Cifrado", "SSE-S3 por defecto; SSE-KMS usa una clave de KMS con permisos y coste propios.")]
    y = 136
    for i, (t, b) in enumerate(ann):
        badge(sl, 540, y + 2, i + 1, fill=AMBER, d=16)
        text(sl, 564, y, 353, 48, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10.5, color=TEXT)
        y += 55
    takeaway(sl, "Bloqueo de acceso público y cifrado vienen activados: cambiarlos debe ser una decisión justificada.", "Idea guía")
    footer(sl, 19, 2)
    notes(sl, """
TIEMPO 18:59–19:01 (2 min). Recorrido en consola.
CONSOLA: comprobar región (Europa · Irlanda) → S3 › General purpose buckets › Create bucket. Recorrer: Bucket name (y, si aparece, la elección de espacio de nombres global o regional de la cuenta), Copy settings from existing bucket, Object Ownership (ACLs disabled, recomendado), Block Public Access settings (las cuatro casillas activadas por defecto), Bucket Versioning (Disable por defecto), Tags, Default encryption (SSE-S3 por defecto; SSE-KMS; DSSE-KMS; Bucket Key) y Advanced settings (Object Lock). NO pulsar Create bucket: Cancel.
DIFERENCIAS: S3 no es el disco de una instancia (eso es EBS) ni una base de datos (no consulta por campos ni ofrece transacciones).
SI LA CUENTA ESTÁ VACÍA: el formulario no necesita recursos previos.
PREGUNTA: «¿Qué opción protege contra un borrado accidental de un adjunto?». Respuesta: el versionado (y, para requisitos normativos, Object Lock).
FUENTES: Amazon S3 User Guide, «Creating a general purpose bucket» (docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html), consultada el 06/11/2026: ACLs disabled por defecto, las cuatro opciones de Block Public Access activadas, versionado desactivado y SSE-S3 como cifrado base.
IMÁGENES: ESQUEMA propio de la pantalla (no es una captura).""")
    return sl


def s20_almacen(d):
    sl = d.slide(tag="almacen")
    header(sl, "Almacenamiento", "Disco, objeto o base de datos: según el dato",
           "Cada almacenamiento responde a una forma de acceso distinta. Elegimos por cómo leemos y escribimos el dato, "
           "no por la lista de servicios disponibles.")
    cols = [("aws-ebs.png", "Bloques · EBS", "Un disco para una instancia",
             "Sistema de archivos con latencia baja. Ejemplo: el sistema y los datos de una base de datos instalada por nosotros en EC2.", MINT),
            ("aws-s3.png", "Objetos · S3", "Archivos completos por HTTPS",
             "Escala sin aprovisionar tamaño. Ejemplo: capturas, audios, PDF, datasets y copias de seguridad.", AMBER),
            ("aws-rds.png", "Registros · RDS", "Base de datos relacional gestionada",
             "PostgreSQL, MySQL y otros motores con consultas, índices y transacciones. Ejemplo: incidencias y su estado.", BLUE)]
    for i, (ic, t, sub, b, col) in enumerate(cols):
        x = 43 + i * 296
        box(sl, x, 138, 284, 128, fill=CARD)
        box(sl, x, 138, 284, 4, fill=col, radius=0)
        img(sl, ic, x + 12, 152, w=36, h=36)
        text(sl, x + 56, 152, 220, 18, t, size=15, font=SERIF, color=TITLE)
        text(sl, x + 56, 172, 220, 14, sub, size=10, color=col, bold=True)
        text(sl, x + 12, 198, 260, 64, b, size=10.5, color=TEXT)
    text(sl, 43, 280, 600, 12, "¿DÓNDE GUARDARÍA NUESTRA API…?", size=9, color=MUTED, bold=True)
    pairs = [("La imagen Docker", "aws-ecr.png", "ECR"),
             ("Los logs de cada petición", "aws-cloudwatch.png", "CloudWatch Logs"),
             ("La clave del proveedor", "aws-secrets.png", "Secrets Manager"),
             ("Un adjunto de la incidencia", "aws-s3.png", "S3"),
             ("El historial de incidencias", "aws-rds.png", "Base de datos (RDS u otra)"),
             ("Ficheros temporales", "aws-fargate.png", "Disco efímero de la tarea")]
    for i, (q, ic, a) in enumerate(pairs):
        r, c = divmod(i, 2)
        x = 43 + c * 443
        y = 298 + r * 58
        box(sl, x, y, 431, 50, fill=CARD)
        text(sl, x + 12, y + 16, 190, 16, q, size=11.5, color=TITLE, bold=True)
        line(sl, x + 198, y + 25, x + 222, y + 25, color=MINT, w=1.25)
        img(sl, ic, x + 230, y + 11, w=28, h=28)
        text(sl, x + 266, y + 16, 162, 16, a, size=11, color=MINT_L, bold=True)
    takeaway(sl, "Nuestra API es stateless: hoy no necesita S3 ni base de datos. Los añadiríamos cuando exista un dato que deba persistir.",
             "Idea guía")
    footer(sl, 20, 2)
    notes(sl, """
TIEMPO 19:01–19:02 (1 min).
QUÉ EXPLICAR: tres formas de almacenar. Bloques (EBS): un disco para una instancia. Objetos (S3): archivos completos por API. Registros (RDS): base de datos relacional gestionada con consultas y transacciones. Recorrer la lista de destinos de nuestra API: imagen en ECR, logs en CloudWatch, clave en Secrets Manager, adjuntos en S3, historial en una base de datos, temporales en el almacenamiento efímero de la tarea (se pierde al reemplazarla).
CONSOLA: opcional, Aurora and RDS › Databases (vacío) solo para situarlo; no abrir el asistente de creación. RDS no se profundiza en S16.
PREGUNTA: «Si el contenedor se reemplaza, ¿dónde debe vivir una conversación que queremos conservar?». Respuesta: en una base de datos u otro almacenamiento persistente, fuera del contenedor.
FUENTES: Amazon EBS, Amazon S3 y Amazon RDS User Guides (descripciones generales); guion de S16 (la API es stateless).
IMÁGENES: AWS Architecture Icons: EBS, S3, RDS, ECR, CloudWatch, Secrets Manager, Fargate.""")
    return sl


def s21_div3(d):
    sl = divider(d, 3, "Red", "La red: de Internet a nuestro contenedor",
                 "VPC, subredes, tablas de rutas, internet gateway y security groups.",
                 ["¿Qué es una VPC y cómo se divide en subredes?",
                  "¿Qué hace pública a una subred?",
                  "¿Cómo se lee una regla de security group?",
                  "¿Por qué tener una IP no basta para conectar?",
                  "¿Qué recorrido hace una petición hasta la aplicación?"],
                 [("aws-vpc.png", "Amazon VPC"), ("r-igw.png", "Internet\ngateway"), ("r-router.png", "Tabla de\nrutas"),
                  ("g-firewall.png", "Security\ngroup")], "19:02–19:12")
    notes(sl, """
TIEMPO 19:02 (10 s). Bloque 3 de 6: Red, de 19:02 a 19:12 (10 min).
QUÉ EXPLICAR: la red decide qué conexiones llegan a nuestra API y cuáles pueden salir hacia el modelo. Es la segunda puerta que vimos en el bloque 1.
IMÁGENES: AWS Architecture Icons: VPC; recursos Internet Gateway y Router; genérico Firewall.""")
    return sl


def s22_vpc(d):
    sl = d.slide(tag="vpc")
    header(sl, "Amazon VPC", "VPC: nuestra red privada dentro de una región",
           "Una VPC es un rango de direcciones privadas que reservamos en una región. Se divide en subredes y cada subred "
           "vive en una zona de disponibilidad. Las tablas de rutas deciden adónde va el tráfico.")
    box(sl, 43, 140, 450, 326, fill=None, line="00A4A6", lw=1, radius=0, dash=True)
    text(sl, 53, 144, 300, 12, "Región eu-west-1", size=9, color="5FD0D2", bold=True)
    box(sl, 55, 172, 426, 284, fill=None, line="8C4FFF", lw=1, radius=0)
    img(sl, "grp-vpc.png", 55, 172, w=18, h=18)
    text(sl, 78, 175, 200, 12, "VPC 10.216.0.0/24", size=9.5, color=VIOLET, bold=True)
    img(sl, "r-igw.png", 250, 154, w=34, h=34)
    text(sl, 290, 162, 150, 14, "Internet gateway", size=9.5, color=TITLE, bold=True)
    box(sl, 67, 200, 200, 118, fill="132620", line="7AA116", lw=1, radius=0)
    img(sl, "grp-public.png", 67, 200, w=16, h=16)
    text(sl, 88, 202, 175, 26, "Subred pública\n10.216.0.0/25 · zona a", size=8.5, color="A6D05A", bold=True)
    img(sl, "aws-fargate.png", 82, 240, w=30, h=30)
    text(sl, 120, 240, 140, 70, "Tarea de nuestra API con IP privada 10.216.0.x e IP pública", size=9.5, color=TEXT)
    box(sl, 275, 200, 196, 118, fill=None, line="5F7279", lw=1, radius=0, dash=True)
    img(sl, "grp-private.png", 275, 200, w=16, h=16)
    text(sl, 296, 202, 172, 26, "Subred privada (ejemplo)\n10.216.0.128/25", size=8.5, color=MUTED, bold=True)
    img(sl, "aws-rds.png", 290, 240, w=30, h=30)
    text(sl, 328, 240, 136, 70, "Aquí iría una base de datos sin IP pública. No está en el laboratorio.", size=9.5, color=MUTED)
    line(sl, 266, 188, 200, 238, color=MINT, w=1.25, head="both")
    for i, (x, rows, col) in enumerate([(67, ["10.216.0.0/24 → local", "0.0.0.0/0 → igw-…"], MINT),
                                       (275, ["10.216.0.0/24 → local", "sin ruta a Internet"], MUTED)]):
        box(sl, x, 326, 200 if i == 0 else 196, 120, fill=CARD)
        img(sl, "r-router.png", x + 8, 334, w=22, h=22)
        text(sl, x + 36, 338, 150, 14, "Tabla de rutas", size=10, color=TITLE, bold=True)
        text(sl, x + 10, 364, 182, 40, "\n".join(rows), size=9.5, font=MONO, color=col, bold=True)
        text(sl, x + 10, 404, 182, 40, "Pública: envía 0.0.0.0/0 al gateway." if i == 0 else "Para salir haría falta un NAT gateway, con coste por hora.",
             size=9, color=TEXT)
    box(sl, 508, 140, 409, 196, fill="FFFFFF", radius=4)
    img(sl, "shot-vpc-map.png", 514, 146, w=397)
    text(sl, 508, 340, 409, 36,
         "Resource map de Amazon VPC · captura de la documentación oficial de AWS (ejemplo en us-east-1 con subredes públicas y privadas en dos zonas).",
         size=9, color=MUTED)
    console_panel(sl, 508, 380, 409, 86, "VPC › Your VPCs › (VPC por defecto) › Resource map",
                  ["La VPC por defecto de cada región sirve para enseñarlo sin crear nada."], size=10)
    takeaway(sl, "Una subred es pública por su tabla de rutas, no por su nombre.", "Idea guía")
    footer(sl, 22, 3)
    notes(sl, """
TIEMPO 19:02–19:05 (3 min).
QUÉ ES: una red virtual aislada en una región, con un rango CIDR privado (nuestra plantilla: 10.216.0.0/24). Se divide en subredes; cada subred está en una zona. Una tabla de rutas asociada a la subred decide el siguiente salto: la ruta «local» comunica toda la VPC; 0.0.0.0/0 → internet gateway hace pública la subred. Una subred privada no tiene esa ruta; para salir a Internet necesitaría un NAT gateway (cargo por hora y por GB). QUÉ RESUELVE: aislar y conectar nuestros recursos. COSTE: la VPC y las subredes no tienen cargo; sí lo tienen las IPv4 públicas, NAT gateways, endpoints de interfaz y el tráfico.
CONSOLA: VPC › Your VPCs → seleccionar la VPC por defecto (existe en cada región salvo que se haya borrado) → pestaña Resource map: subredes por zona, tablas de rutas y conexiones de red (internet gateway). Después VPC › Route tables → Routes (0.0.0.0/0 → igw-…) y Subnet associations.
SEÑALAR: CIDR de la VPC y de cada subred, zona de cada subred, ruta 0.0.0.0/0.
PREGUNTA: «Si la subred tiene IP pública automática pero su tabla no tiene ruta al gateway, ¿es accesible?». Respuesta: no.
FUENTES: Amazon VPC User Guide, «How Amazon VPC works» e «Internet gateways» (docs.aws.amazon.com/vpc/latest/userguide/); plantilla infra/s16/servicio.json (VPC 10.216.0.0/24, subred 10.216.0.0/25, ruta 0.0.0.0/0 → gateway). La subred privada es un ejemplo, no forma parte del laboratorio.
IMÁGENES: captura «vpc-resource-map-update.PNG» de la VPC User Guide (docs.aws.amazon.com), recortada; iconos de grupo VPC, Public subnet, Private subnet y recursos Internet Gateway y Router de AWS Architecture Icons.""")
    return sl


def s23_sg(d):
    sl = d.slide(tag="sg")
    header(sl, "Security groups", "Security group: origen, protocolo y puerto",
           "Un security group es un cortafuegos con estado asociado a la interfaz de red de una instancia o de una tarea. "
           "Solo contiene reglas de permiso: lo que no está permitido no entra ni sale.")
    ui_panel(sl, 43, 132, 574, 236, title="sg-0a1b2c3d (s16-lab)", crumbs="VPC  ›  Security groups  ›  sg-0a1b2c3d")
    esquema_label(sl, 462, 135)
    cols = [("Type", 74), ("Protocol", 58), ("Port range", 66), ("Source", 116), ("Description", 220)]
    def rule_table(y, title, row, src_lab="Source"):
        text(sl, 51, y, 300, 14, title, size=10, color=UI_TEXT, bold=True)
        x = 51
        box(sl, 51, y + 16, 558, 18, fill="E9EBED", radius=0)
        for (c, w) in cols:
            text(sl, x + 4, y + 19, w, 12, src_lab if c == "Source" else c, size=8.5, color=UI_LABEL, bold=True, check=False)
            x += w + 6
        box(sl, 51, y + 34, 558, 20, fill=UI_CARD, line="DDE1E5", lw=0.5, radius=0)
        x = 51
        for (c, w), v in zip(cols, row):
            text(sl, x + 4, y + 38, w, 12, v, size=9, color=UI_TEXT, font=MONO if c in ("Port range", "Source") else SANS,
                 bold=c in ("Port range", "Source"), check=False)
            x += w + 6
    rule_table(186, "Inbound rules (1)", ["Custom TCP", "TCP", "8000", "203.0.113.10/32", "Profesor, solo laboratorio"])
    rule_table(266, "Outbound rules (1)", ["HTTPS", "TCP", "443", "0.0.0.0/0", "Imagen, secreto, logs y modelo"], src_lab="Destination")
    for n, x, y in [(1, 176, 204), (2, 249, 204), (3, 304, 204), (4, 324, 284)]:
        badge(sl, x, y, n, fill=AMBER, d=13, size=7.5)
    ann = [("Protocolo", "TCP para HTTP y HTTPS. «Custom TCP» permite elegir el puerto."),
           ("Puerto", "El que escucha el contenedor: 8000. Debe coincidir con portMappings de la tarea."),
           ("Origen", "/32 es una sola IPv4. 0.0.0.0/0 sería todo Internet."),
           ("Destino de salida", "HTTPS para descargar la imagen, leer el secreto, enviar logs y llamar al modelo.")]
    y = 136
    for i, (t, b) in enumerate(ann):
        badge(sl, 632, y + 2, i + 1, fill=AMBER, d=16)
        text(sl, 656, y, 261, 52, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10.5, color=TEXT)
        y += 56
    cards = [("ERRORES TÍPICOS", CORAL, CORAL_BG, "0.0.0.0/0 en el puerto de la API o en el 22; regla en el security group de otra interfaz; puerto distinto del que escucha el contenedor."),
             ("NETWORK ACL", BLUE, BLUE_BG, "Segunda capa, sin estado y por subred. La de la VPC por defecto permite todo el tráfico."),
             ("CON ESTADO", MINT, TAKE_BG, "La respuesta a una petición permitida vuelve sin otra regla de salida.")]
    x = 43
    for (t, col, bg, b), w in zip(cards, [330, 268, 256]):
        box(sl, x, 378, w, 88, fill=bg)
        text(sl, x + 12, 388, w - 24, 12, t, size=9, color=col, bold=True)
        text(sl, x + 12, 404, w - 24, 58, b, size=10.5, color=TITLE)
        x += w + 10
    takeaway(sl, "Una regla abierta a 0.0.0.0/0 publica el servicio para todo Internet. Empezamos por /32 y ampliamos con un motivo.",
             "Idea guía")
    footer(sl, 23, 3)
    notes(sl, """
TIEMPO 19:05–19:08 (3 min). Recorrido en consola.
QUÉ ES: un cortafuegos virtual con estado asociado a interfaces de red (ENI) de instancias EC2, tareas de Fargate, balanceadores, etc. Solo tiene reglas de permiso. Cada regla de entrada indica protocolo, puerto y origen (CIDR o otro security group); cada regla de salida, protocolo, puerto y destino. Con estado: la respuesta vuelve automáticamente. La Network ACL es otra capa, sin estado, que se aplica a la subred.
NUESTRA PLANTILLA: entrada TCP 8000 desde el /32 del profesor (parámetro AllowedCidr); salida TCP 443 a 0.0.0.0/0.
CONSOLA: VPC › Security groups → seleccionar el security group «default» de la VPC por defecto → pestañas Inbound rules y Outbound rules → Edit inbound rules → «Add rule» para enseñar Type, Protocol, Port range, Source (My IP, Custom, Anywhere-IPv4) y Description → Cancel. NO guardar cambios.
SEÑALAR: la opción «My IP» rellena un /32; «Anywhere-IPv4» es 0.0.0.0/0.
PREGUNTA: «La API escucha en 8000 y la regla abre el 80. ¿Qué pasa?». Respuesta: timeout; el puerto de la regla debe coincidir con el del contenedor.
FUENTES: Amazon VPC User Guide, «Control traffic to your AWS resources using security groups» y «Network ACLs»; plantilla infra/s16/servicio.json. 203.0.113.10 pertenece al rango de documentación TEST-NET-3; sg-0a1b2c3d es un identificador ficticio.
IMÁGENES: ESQUEMA propio de la pantalla de reglas (no es una captura).""")
    return sl


def s24_recorrido(d):
    sl = d.slide(tag="recorrido")
    header(sl, "Recorrido de una petición", "Tener una IP no basta: cinco condiciones",
           "Una petición desde el portátil del profesor llega al contenedor solo si se cumplen todas las condiciones del "
           "recorrido. Si falla una, el síntoma suele ser el mismo: un timeout.")
    nodes = [("g-client.png", "Portátil", "203.0.113.10", None),
             ("g-internet.png", "Internet", "", None),
             ("r-igw.png", "Internet gateway", "igw-…", 2),
             ("r-router.png", "Tabla de rutas", "0.0.0.0/0 → igw", 3),
             ("g-firewall.png", "Security group", "TCP 8000 · /32", 4),
             ("r-eni.png", "ENI de la tarea", "IP pública + 10.216.0.x", 1),
             ("docker-mark-white.png", "Contenedor", "uvicorn :8000", 5)]
    w = 116
    gap = (874 - 7 * w) / 6
    for i, (ic, t, sub, n) in enumerate(nodes):
        x = 43 + i * (w + gap)
        box(sl, x, 140, w, 104, fill=CARD if n is None else CARD2, line=None if n is None else "2A5246")
        if ic.startswith("docker"):
            img(sl, ic, x + (w - 40) / 2, 154, h=30)
        else:
            img(sl, ic, x + (w - 34) / 2, 150, w=34, h=34)
        text(sl, x + 4, 192, w - 8, 16, t, size=10.5, color=TITLE, bold=True, align="c")
        text(sl, x + 4, 210, w - 8, 30, sub, size=8.5, font=MONO, color=MINT_L, align="c", bold=True)
        if n:
            badge(sl, x + w - 20, 144, n, fill=AMBER, d=16)
        if i < 6:
            line(sl, x + w + 1, 192, x + w + gap - 1, 192, color=MINT, w=1.5)
    conds = [("IP pública en la ENI", "AssignPublicIp=ENABLED en el servicio. Sin ella, la tarea solo tiene IP privada."),
             ("Gateway conectado", "Un internet gateway asociado a la VPC de la tarea."),
             ("Ruta 0.0.0.0/0 → igw", "En la tabla de rutas asociada a la subred de la tarea."),
             ("Regla de entrada", "TCP 8000 desde el /32 del profesor, en el security group de esa ENI."),
             ("Proceso escuchando", "uvicorn en 0.0.0.0:8000 dentro del contenedor, no solo en 127.0.0.1.")]
    for i, (t, b) in enumerate(conds):
        x = 43 + i * 177
        box(sl, x, 256, 167, 120, fill=CARD)
        badge(sl, x + 10, 266, i + 1, fill=AMBER, d=18, size=10)
        text(sl, x + 34, 266, 128, 32, t, size=11, color=TITLE, bold=True)
        text(sl, x + 10, 302, 150, 70, b, size=10, color=TEXT)
    box(sl, 43, 386, 430, 80, fill=BLUE_BG)
    text(sl, 55, 394, 400, 12, "VUELTA Y SALIDA", size=9, color=BLUE, bold=True)
    text(sl, 55, 410, 408, 52, "La respuesta vuelve por el mismo camino (el security group tiene estado). Las llamadas al modelo "
                               "salen por HTTPS 443 por el mismo gateway.", size=10.5, color=TITLE)
    box(sl, 483, 386, 434, 80, fill=AMBER_BG)
    text(sl, 495, 394, 400, 12, "EXPOSE NO ABRE NADA", size=9, color=AMBER, bold=True)
    text(sl, 495, 410, 412, 52, "EXPOSE 8000 en el Dockerfile solo documenta el puerto. En AWS deciden portMappings, "
                                "el security group, la ruta y la IP pública.", size=10.5, color=TITLE)
    takeaway(sl, "Diagnosticamos siguiendo el recorrido: IP, gateway, ruta, regla y proceso. Abrir todos los puertos solo oculta cuál faltaba.",
             "Idea guía")
    footer(sl, 24, 3)
    notes(sl, """
TIEMPO 19:08–19:12 (4 min).
QUÉ EXPLICAR: seguir una petición de izquierda a derecha y comprobar cinco condiciones: (1) la ENI de la tarea tiene IP pública (en ECS, AssignPublicIp=ENABLED en el servicio); (2) la VPC tiene un internet gateway; (3) la tabla de rutas de la subred envía 0.0.0.0/0 al gateway; (4) el security group de esa ENI permite TCP 8000 desde el /32 del profesor; (5) el proceso escucha en 0.0.0.0:8000 dentro del contenedor. La respuesta vuelve por el mismo camino. Las llamadas al modelo salen por HTTPS 443.
DIAGNÓSTICO: un timeout sin mensaje suele indicar red (IP, ruta o regla). Un 4xx/5xx con request_id indica que sí llegamos a la API.
CONSOLA: con la VPC por defecto, enseñar VPC › Subnets (Auto-assign public IPv4 address), Route tables (Routes) e Internet gateways (State: Attached). En ECS, la pestaña Networking de una tarea mostraría ENI, IP privada y pública; si no hay tareas, explicarlo con la plantilla.
PREGUNTA: «Tenemos IP pública y regla correcta, pero la subred no tiene ruta al gateway. ¿Qué vemos?». Respuesta: timeout.
FUENTES: Amazon ECS Developer Guide, «Fargate task networking» (ENI por tarea, IP pública opcional); VPC User Guide, «Internet gateways»; Dockerfile del proyecto (EXPOSE 8000, uvicorn --host 0.0.0.0 --port 8000).
IMÁGENES: AWS Architecture Icons: genéricos Client, Internet y Firewall; recursos Internet Gateway, Router y Elastic Network Interface; logotipo de Docker (docker.com).""")
    return sl


PART2 = [s14_div2, s15_ec2, s16_launch, s17_ebs, s18_s3, s19_bucket, s20_almacen, s21_div3, s22_vpc, s23_sg, s24_recorrido]
