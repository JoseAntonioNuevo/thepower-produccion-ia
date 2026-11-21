"""Diapositivas 34–41: bloque 5 (operar y pagar)."""
from deck_lib import *  # noqa: F401,F403

COST_SRC = ("Tarifas: catálogo público AWS Price List para eu-west-1 leído el 17/10/2026 "
            "(docs/fuentes/tarifas-aws-2026-10-17.json); cantidades supuestas en datos/costes-ejemplo.json; "
            "cálculo reproducible con scripts/costes.py. USD sin impuestos, descuentos ni créditos. No es una factura.")


def s34_div5(d):
    sl = divider(d, 5, "Operar y pagar", "Observar la API y controlar el gasto",
                 "CloudWatch, Billing and Cost Management, Budgets y la calculadora pública de AWS.",
                 ["¿Qué son logs, métricas y alarmas?",
                  "¿Dónde buscamos un error concreto?",
                  "Factura, estimación, presupuesto y alerta: ¿qué es cada una?",
                  "¿Cuánto cuesta un mes y cuánto una demo de 90 minutos?",
                  "¿Qué decisiones reducen el gasto?"],
                 [("aws-cloudwatch.png", "Amazon\nCloudWatch"), ("aws-costexplorer.png", "Cost Explorer"),
                  ("aws-budgets.png", "AWS Budgets")], "19:29–19:42")
    notes(sl, """
TIEMPO 19:29 (10 s). Bloque 5 de 6: Operar y pagar, de 19:29 a 19:42 (13 min).
QUÉ EXPLICAR: una API en la nube no termina al desplegarla: hay que poder ver qué hace y saber cuánto cuesta mantenerla o retirarla.
IMÁGENES: AWS Architecture Icons: CloudWatch, Cost Explorer, Budgets.""")
    return sl


def s35_cloudwatch(d):
    sl = d.slide(tag="cloudwatch")
    header(sl, "Amazon CloudWatch", "CloudWatch: logs, métricas y alarmas",
           "Los logs cuentan qué pasó en cada petición; las métricas resumen el comportamiento en el tiempo; una alarma "
           "vigila una métrica y avisa cuando cruza un umbral.")
    nodes = [("g-client.png", "Petición", "POST /clasificar"),
             ("r-cw-logs.png", "Log group", "/thepower/s16-lab"),
             ("g-logs.png", "Log stream", "api/api/<id de tarea>"),
             ("g-metrics.png", "Métrica", "5xx · CPU · memoria"),
             ("r-cw-alarm.png", "Alarma", "OK · ALARM"),
             ("g-alert.png", "Aviso", "SNS · email")]
    w = 132
    gap = (874 - 6 * w) / 5
    for i, (ic, t, sub) in enumerate(nodes):
        x = 43 + i * (w + gap)
        box(sl, x, 136, w, 92, fill=CARD)
        img(sl, ic, x + 10, 148, w=30, h=30)
        text(sl, x + 46, 150, w - 50, 16, t, size=11, color=TITLE, bold=True)
        text(sl, x + 10, 186, w - 16, 36, sub, size=9, font=MONO, color=MINT_L, bold=True)
        if i < 5:
            line(sl, x + w + 1, 182, x + w + gap - 1, 182, color=BLUE, w=1.5)
    box(sl, 43, 238, 874, 62, fill="0B151B", line=BORDER)
    text(sl, 55, 244, 700, 12, "LÍNEA DE LOG DE NUESTRA API · forma real del registro, valores de ejemplo", size=9, color=MINT, bold=True)
    text(sl, 55, 262, 850, 32, '{"request_id": "6f1c2d9e-…", "version": "2026-11-12.1", "execution": "real", '
                               '"status": 200, "duration_ms": 842.5}', size=10.5, font=MONO, color=TITLE, bold=True)
    cards = [("Logs", "Grupo con retención de 7 días en nuestra plantilla; por defecto un grupo no caduca. Un stream por tarea.",
              'fields @timestamp, status, duration_ms\n| filter request_id = "6f1c2d9e-…"'),
             ("Métricas", "ECS publica CPUUtilization y MemoryUtilization por servicio (espacio AWS/ECS). Un filtro de métricas puede contar respuestas 5xx en los logs.", None),
             ("Alarmas", "Vigilan una métrica y cambian entre OK, ALARM e INSUFFICIENT_DATA. Al cambiar, notifican, por ejemplo por SNS a un correo.", None)]
    for i, (t, b, code) in enumerate(cards):
        x = 43 + i * 296
        box(sl, x, 310, 284, 116, fill=CARD)
        text(sl, x + 12, 318, 260, 18, t, size=14, font=SERIF, color=TITLE)
        text(sl, x + 12, 340, 262, 46 if code else 80, b, size=10, color=TEXT)
        if code:
            box(sl, x + 10, 388, 264, 32, fill=BG, radius=3)
            text(sl, x + 16, 391, 254, 28, code, size=8, font=MONO, color=MINT_L, bold=True, check=False)
    cost_chip(sl, 43, 434, 874, "Ingesta 0,57 USD/GB y almacenamiento 0,03 USD/GB-mes en eu-west-1 (17/10/2026). "
                                "Métricas personalizadas y alarmas tienen tarifa propia.", h=34)
    takeaway(sl, "Con el request_id de la respuesta encontramos su línea de log: estado, duración y versión, sin guardar el texto del usuario ni la clave.",
             "Idea guía")
    footer(sl, 35, 5)
    notes(sl, """
TIEMPO 19:29–19:32 (3 min). Recorrido en consola.
QUÉ ES: servicio de observabilidad. Logs: grupos (por aplicación) con streams (por tarea) y retención configurable; por defecto los datos se conservan indefinidamente. Métricas: series temporales; ECS publica CPUUtilization y MemoryUtilization por servicio en el espacio AWS/ECS; un metric filter convierte patrones de logs (p. ej. status ≥ 500) en métricas. Alarmas: evalúan una métrica frente a un umbral y pasan a ALARM; pueden notificar por SNS.
NUESTRA API: escribe una línea JSON por petición con request_id, version, execution, status y duration_ms; no registra el texto de la incidencia ni la clave. La respuesta devuelve el mismo request_id (cabecera x-request-id y metadata).
CONSOLA: CloudWatch › Logs › Log groups (en una cuenta nueva puede estar vacío o tener grupos de otros servicios) → abrir un grupo y señalar Retention y Log streams. Logs › Logs Insights: elegir un grupo y mostrar la consulta sin ejecutarla si no hay datos. Alarms › All alarms → Create alarm → Select metric → Cancel. CloudWatch no requiere crear nada para enseñarlo.
PREGUNTA: «Un alumno nos envía el request_id de una respuesta fallida. ¿Dónde lo buscamos?». Respuesta: en el grupo /thepower/<lab> con Logs Insights.
FUENTES: Amazon CloudWatch Logs User Guide (log groups, retention, Logs Insights); Amazon ECS Developer Guide, «Amazon ECS CloudWatch metrics»; src/curso_ia/api.py (campos del log); infra/s16/servicio.json (RetentionInDays 7); datos/costes-ejemplo.json.
IMÁGENES: AWS Architecture Icons: CloudWatch Logs, CloudWatch Alarm; genéricos Client, Logs, Metrics y Alert.""")
    return sl


def s36_diagnostico(d):
    sl = d.slide(tag="diagnostico")
    header(sl, "Diagnóstico", "Dónde buscar un error, capa por capa",
           "El síntoma indica la capa. Empezamos por el lugar de la consola donde AWS deja la evidencia de esa capa, "
           "no por cambiar permisos o abrir puertos.")
    hdr = ["SÍNTOMA", "DÓNDE MIRAR EN LA CONSOLA", "QUÉ BUSCAR"]
    xs = [43, 286, 588]
    ws = [235, 294, 329]
    for x, w, h_ in zip(xs, ws, hdr):
        text(sl, x + 10, 136, w, 12, h_, size=9, color=MUTED, bold=True)
    rows = [("La tarea se para al arrancar", "ECS › servicio › Tasks › Stopped › Stopped reason",
             "CannotPullContainerError, imagen arm64 en tarea X86_64 o un comando que termina.", CORAL),
            ("No obtiene la imagen o el secreto", "Stopped reason de la tarea · IAM › execution role",
             "ResourceInitializationError: unable to pull secrets or registry auth.", CORAL),
            ("Timeout desde el portátil", "Tarea › Networking · VPC › Security groups · Route tables",
             "IP pública, regla TCP 8000 desde el /32 y ruta 0.0.0.0/0 → internet gateway.", VIOLET),
            ("/health 200, pero /clasificar 5xx", "CloudWatch › Log groups › /thepower/s16-lab · Logs Insights",
             "request_id, status y duration_ms: plazo o error del proveedor del modelo.", BLUE),
            ("/clasificar responde 422", "La propia respuesta JSON de la API",
             "Entrada inválida rechazada antes de llamar al modelo: no es un fallo de AWS.", MINT)]
    y = 152
    for sym, where, what, col in rows:
        for x, w in zip(xs, ws):
            box(sl, x, y, w, 50, fill=CARD)
        box(sl, 43, y, 4, 50, fill=col, radius=0)
        text(sl, 55, y + 8, 222, 36, sym, size=11.5, color=TITLE, bold=True, anchor="m")
        text(sl, 296, y + 6, 280, 40, where, size=9.5, font=MONO, color=MINT_L, bold=True, anchor="m")
        text(sl, 598, y + 6, 312, 40, what, size=10.5, color=TEXT, anchor="m")
        y += 55
    box(sl, 43, 430, 874, 38, fill=BLUE_BG)
    text(sl, 55, 432, 850, 34, [[("PREGUNTA PARA LA CLASE  ", {"bold": True, "color": BLUE, "size": 9}),
                                 ("Health devuelve 200 y clasificar devuelve 504. ¿Abrimos todos los puertos o seguimos el request_id?", {})]],
         size=11, color=TITLE, anchor="m")
    takeaway(sl, "Health 200 prueba que el proceso responde; no prueba que el modelo, la clave y el plazo funcionen.", "Idea guía")
    footer(sl, 36, 5)
    notes(sl, """
TIEMPO 19:32–19:34 (2 min).
QUÉ EXPLICAR: diagnosticar por capas siguiendo el recorrido. (1) Arranque: ECS muestra la razón de parada de cada tarea (Stopped reason) y los eventos del servicio; errores típicos: CannotPullContainerError, plataforma incompatible, comando que termina. (2) Permisos de arranque: «ResourceInitializationError: unable to pull secrets or registry auth» apunta al execution role, al ARN, a la región, a la salida de red o a KMS. (3) Red: un timeout sin respuesta apunta a IP pública, regla o ruta. (4) Aplicación/proveedor: si /health responde y /clasificar falla, buscar el request_id en CloudWatch (status, duration_ms). (5) 422: validación de entrada, antes del proveedor.
CONSOLA: ECS › Clusters › (servicio) › Tasks con el filtro «Stopped» y la pestaña Events del servicio (en una cuenta vacía, explicar dónde aparecerían). CloudWatch › Logs Insights.
PREGUNTA (en la diapositiva): health 200 y clasificar 504. Respuesta: no abrir puertos; seguir el request_id, revisar el plazo y la conexión con el proveedor y conservar la evidencia.
NO PROVOCAR fallos en directo cambiando claves ni gastando inferencias: para errores remotos usar los tests preparados (tests/test_api.py y tests/test_proveedor.py) o explicarlos.
FUENTES: Amazon ECS Developer Guide, «Amazon ECS stopped tasks errors» y «Troubleshooting ResourceInitializationError»; guion de S16 (tabla de diagnóstico); src/curso_ia/api.py (422 antes del proveedor).
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


def s37_billing(d):
    sl = d.slide(tag="billing")
    header(sl, "Billing and Cost Management", "Factura, estimación, presupuesto y alerta",
           "Son herramientas distintas: una mira lo ya consumido, otra estima antes de crear y otras vigilan mientras los "
           "recursos existen. Billing and Cost Management es global y exige permisos de facturación.")
    line(sl, 60, 146, 900, 146, color=FAINT, w=1, head="end")
    text(sl, 60, 132, 200, 12, "LO YA CONSUMIDO", size=8.5, color=MUTED, bold=True, check=False)
    text(sl, 700, 132, 200, 12, "ANTES DE CREAR", size=8.5, color=MUTED, bold=True, align="r", check=False)
    cards = [("g-document.png", "Bills · factura", "Lo que AWS ha facturado cada mes, por servicio y región. Es consumo pasado: retirar recursos no lo borra.",
              "Billing and Cost Management › Bills", BLUE),
             ("aws-costexplorer.png", "Cost Explorer · análisis", "Coste por servicio, región o etiqueta, con previsión. Tras activarlo puede tardar hasta 24 h en mostrar datos.",
              "… › Cost Explorer", VIOLET),
             ("aws-budgets.png", "Budgets · presupuesto y alerta", "Un importe con umbrales de gasto real o previsto que avisan por correo o SNS. La alerta avisa; no apaga recursos.",
              "… › Budgets › Create budget", AMBER),
             ("g-data-table.png", "Pricing Calculator · estimación", "Estimar antes de crear nada. Es pública y no necesita cuenta.",
              "calculator.aws", MINT)]
    for i, (ic, t, b, path, col) in enumerate(cards):
        x = 43 + i * 221
        box(sl, x, 156, 211, 206, fill=CARD)
        box(sl, x, 156, 211, 4, fill=col, radius=0)
        img(sl, ic, x + 12, 170, w=30, h=30)
        text(sl, x + 50, 168, 155, 36, t, size=11.5, color=TITLE, bold=True, anchor="m")
        text(sl, x + 12, 210, 190, 104, b, size=10.5, color=TEXT)
        box(sl, x + 10, 318, 191, 34, fill=BG, radius=3)
        text(sl, x + 16, 322, 180, 28, path, size=8.5, font=MONO, color=col, bold=True, anchor="m")
    text(sl, 43, 374, 600, 12, "PARTIDAS QUE APARECEN CON NUESTRA API", size=9, color=MUTED, bold=True)
    parts = [("Cómputo", AMBER), ("IPv4 pública", VIOLET), ("Almacenamiento", BLUE), ("Logs", BLUE), ("Secretos", CORAL),
             ("Tráfico de salida", PINK), ("Inferencia · aparte", MINT)]
    x = 43
    for t, col in parts:
        w = len(t) * 6.2 + 26
        chip(sl, x, 392, w, 24, t, fill=CARD2, color=col, size=10, line=col)
        x += w + 8
    text(sl, 43, 426, 874, 40,
         [[("Factura ≠ estimación ≠ presupuesto ≠ alerta. ", {"bold": True, "color": TITLE}),
           ("Una estimación usa tarifas y cantidades supuestas; la factura refleja el uso real; el presupuesto fija un límite de referencia; la alerta solo avisa.", {})]],
         size=10.5, color=TEXT)
    takeaway(sl, "Una alerta de presupuesto no detiene nada: parar o retirar recursos es una acción nuestra.", "Idea guía")
    footer(sl, 37, 5)
    notes(sl, """
TIEMPO 19:34–19:36 (2 min). Recorrido en consola.
QUÉ EXPLICAR: cuatro conceptos. Factura (Bills): importes del periodo por servicio y región; refleja uso pasado. Cost Explorer: análisis y previsión del coste; hay que activarlo y puede tardar hasta 24 horas en mostrar datos. AWS Budgets: un importe de referencia con umbrales sobre gasto real o previsto que notifica por correo o SNS; por sí solo no apaga nada (existen «budget actions» configurables que pueden aplicar políticas IAM/SCP o detener instancias EC2/RDS concretas, pero hay que configurarlas expresamente y no detienen una tarea de Fargate). AWS Pricing Calculator: estimación pública antes de crear recursos.
CONSOLA: menú de cuenta › Billing and Cost Management. Home → Bills (mes actual) → Cost Explorer → Budgets → Create budget (ver la siguiente diapositiva) → Cancel. Si la identidad de clase no tiene permisos de facturación, explicarlo: el acceso de IAM a Billing debe estar habilitado y concedido.
SEÑALAR: que el selector de región indica «Global»; las partidas por servicio; la diferencia entre coste real y previsto.
PREGUNTA: «Si retiro hoy todos los recursos, ¿desaparece la factura de este mes?». Respuesta: no; se deja de generar consumo nuevo, pero lo ya consumido se factura.
FUENTES: AWS Billing User Guide (Bills); AWS Cost Management User Guide, «Analyzing your costs with AWS Cost Explorer» y «Managing your costs with AWS Budgets» / «Configuring budget actions»; AWS Pricing Calculator (calculator.aws).
IMÁGENES: AWS Architecture Icons: Cost Explorer, Budgets; genéricos Document y Data Table.""")
    return sl


def s38_mes(d):
    sl = d.slide(tag="mes")
    header(sl, "Coste mensual", "730 horas de nuestra API: 13,78 USD sin inferencia",
           "Estimación con tarifas públicas de eu-west-1 (Irlanda) leídas el 17/10/2026 y cantidades supuestas. "
           "USD sin impuestos, descuentos ni créditos. No es una factura.")
    text(sl, 43, 130, 260, 46, "13,78 USD", size=36, font=SERIF, color=MINT_L)
    text(sl, 290, 140, 330, 32, "por mes · una tarea de 0,25 vCPU y 0,5 GB encendida 730 horas · sin inferencia", size=10.5, color=TEXT)
    chip(sl, 640, 136, 130, 20, "eu-west-1 · Irlanda", fill=TAKE_BG, color=MINT_L, size=9)
    chip(sl, 776, 136, 141, 20, "tarifas del 17/10/2026", fill=TAKE_BG, color=MINT_L, size=9)
    chip(sl, 640, 160, 277, 20, "cantidades supuestas · no es una factura", fill=AMBER_BG, color=AMBER, size=9)
    items = [("CPU", 7.3876, AMBER), ("IPv4 pública", 3.65, VIOLET), ("Memoria", 1.622425, "C99A3A"), ("Logs", 0.60, BLUE),
             ("Secreto", 0.40001, CORAL), ("Salida", 0.09, PINK), ("ECR", 0.025, MINT)]
    tot = sum(v for _, v, _ in items)
    x = 43
    for n, v, col in items:
        w = 874 * v / tot
        box(sl, x, 188, max(w, 1.5), 26, fill=col, radius=0)
        if w > 60:
            text(sl, x + 6, 194, w - 8, 14, f"{n} {v:.2f}".replace(".", ","), size=9.5, color=DARK, bold=True, check=False)
        x += w
    comp = 7.3876 + 1.622425 + 3.65
    wcomp = 874 * comp / tot
    line(sl, 43, 220, 43 + wcomp, 220, color=MINT_L, w=1, head="none")
    text(sl, 43, 223, wcomp, 14, "92 % es tiempo encendido: CPU, memoria e IPv4", size=9.5, color=MINT_L, bold=True, align="c")
    text(sl, 43 + wcomp + 4, 223, 874 - wcomp - 4, 14, "8 % resto", size=9, color=MUTED, align="c", check=False)
    rows = [("CPU", "0,25 vCPU × 730 h × 0,04048 USD/vCPU-h", "7,3876"),
            ("Memoria", "0,5 GB × 730 h × 0,004445 USD/GB-h", "1,6224"),
            ("IPv4 pública", "1 IP × 730 h × 0,005 USD/IP-h", "3,6500"),
            ("Logs", "1 GB ingerido × 0,57 + 1 GB-mes × 0,03", "0,6000"),
            ("Secreto", "1 × 0,40 + 2 lecturas × 0,000005", "0,4000"),
            ("Salida a Internet", "1 GB facturable × 0,09", "0,0900"),
            ("ECR", "0,25 GB-mes × 0,10", "0,0250")]
    y = 244
    for i, (c, f, v) in enumerate(rows):
        box(sl, 43, y, 576, 24, fill=CARD if i % 2 == 0 else "15232A", radius=0)
        text(sl, 53, y + 5, 120, 14, c, size=10.5, color=TITLE, bold=True)
        text(sl, 175, y + 5, 340, 14, f, size=10, font=MONO, color=TEXT, bold=True)
        text(sl, 520, y + 5, 90, 14, v, size=10.5, font=MONO, color=MINT_L, bold=True, align="r")
        y += 24
    box(sl, 43, y, 576, 28, fill=TAKE_BG, radius=0)
    text(sl, 53, y + 6, 300, 16, "Total (redondeo al final)", size=11, color=TITLE, bold=True)
    text(sl, 380, y + 6, 230, 16, "13,7750 → 13,78 USD", size=11.5, font=MONO, color=MINT_L, bold=True, align="r")
    box(sl, 633, 244, 284, 224, fill=CARD, line=BORDER)
    text(sl, 645, 252, 260, 12, "SUPUESTOS", size=9, color=AMBER, bold=True)
    sup = ["Una tarea Linux x86 con almacenamiento efímero incluido.",
           "0,25 GB en ECR, 1 GB de logs, un secreto con dos lecturas y 1 GB de salida ya facturable.",
           "No se descuenta el tramo gratuito de tráfico.",
           "Sin NAT, balanceador, base de datos ni KMS propia: si se añaden, se suman.",
           "Inferencia aparte: tokens × tarifa del modelo."]
    text(sl, 645, 270, 264, 196, [{"runs": [("•  ", {"color": AMBER, "bold": True}), (t, {})], "space": 4} for t in sup],
         size=10, color=TEXT, space=4)
    takeaway(sl, "El 92 % del mes es tiempo encendido. Apagar cuando no se usa es la primera optimización.", "Idea guía")
    footer(sl, 38, 5)
    notes(sl, """
TIEMPO 19:36–19:38 (2 min).
QUÉ EXPLICAR: coste = cantidad × tarifa de la región, partida a partida. 730 horas es la base mensual del ejercicio, no una invitación a dejar recursos encendidos. CPU 0,25 × 730 × 0,04048 = 7,3876; memoria 0,5 × 730 × 0,004445 = 1,622425; IPv4 730 × 0,005 = 3,65 (subtotal de tiempo encendido 12,660025, el 92 %). Añadir ECR 0,025, logs ingeridos 0,57 y almacenados 0,03, secreto 0,40 y dos lecturas 0,00001, salida 0,09. Total 13,775035 → 13,78 USD (se redondea al final).
SUPUESTOS VISIBLES: región eu-west-1, tarifas del 17/10/2026, USD sin impuestos/descuentos/créditos, salida ya facturable tras el tramo gratuito global, sin NAT/ALB/BD/KMS propia, inferencia separada. Son cantidades supuestas, no consumo observado.
CÓDIGO (opcional): uv run python scripts/costes.py datos/costes-ejemplo.json reproduce las cifras.
PREGUNTA: «¿Qué partida desaparece si quitamos la IP pública y ponemos un balanceador?». Respuesta: baja la IPv4 de la tarea, pero el balanceador añade su propio cargo por hora y por uso (y su IP); no es gratis.
FUENTES: """ + COST_SRC + """ Fargate Pricing (aws.amazon.com/fargate/pricing/), Amazon VPC pricing (IPv4 pública), Amazon ECR, CloudWatch y Secrets Manager pricing.
IMÁGENES: gráfico propio (barras proporcionales a los importes).""")
    return sl


def s39_demo(d):
    sl = d.slide(tag="demo")
    header(sl, "Coste de la demo", "La demo de 0,46 USD: 90 minutos y 30 días retenidos",
           "Este escenario no es «90 minutos de todo»: suma 90 minutos de cómputo e IPv4 y 30 días de imagen, secreto y "
           "logs que seguimos conservando. La inferencia va aparte.")
    text(sl, 43, 128, 240, 46, "0,46 USD", size=36, font=SERIF, color=MINT_L)
    text(sl, 260, 138, 440, 32, "eu-west-1 · tarifas del 17/10/2026 · sin inferencia · total sin redondear 0,45710875 USD",
         size=10.5, color=TEXT)
    segs = [("Cómputo e IPv4", 0.02601375, MINT), ("Recursos retenidos", 0.4253, AMBER), ("Uso", 0.005795, BLUE)]
    tot = sum(v for _, v, _ in segs)
    x = 43
    for n, v, col in segs:
        w = 874 * v / tot
        box(sl, x, 182, w, 26, fill=col, radius=0)
        if w > 100:
            text(sl, x + 8, 188, w - 12, 14, f"Recursos retenidos · 93 %", size=10, color=DARK, bold=True, check=False)
        x += w
    text(sl, 43, 211, 200, 14, "↑ cómputo e IPv4: 6 %", size=9, color=MINT, bold=True, check=False)
    text(sl, 717, 211, 200, 14, "uso: 1 % ↑", size=9, color=BLUE, bold=True, align="r", check=False)
    blocks = [("CÓMPUTO E IPv4 · 1,5 HORAS", "0,0260 USD", MINT, TAKE_BG,
               [("CPU", "0,375 vCPU-h", "0,0152"), ("Memoria", "0,75 GB-h", "0,0033"), ("IPv4 pública", "1,5 IP-h", "0,0075")]),
              ("RECURSOS RETENIDOS · 30 DÍAS", "0,4253 USD", AMBER, AMBER_BG,
               [("Secreto", "1 secreto-mes", "0,4000"), ("ECR", "0,25 GB-mes", "0,0250"), ("Logs almacenados", "0,01 GB-mes", "0,0003")]),
              ("USO DEL ESCENARIO", "0,0058 USD", BLUE, BLUE_BG,
               [("Logs ingeridos", "0,01 GB", "0,0057"), ("Salida", "0,001 GB", "0,0001"), ("Lectura del secreto", "1 petición", "0,000005")])]
    for i, (t, v, col, bg, rows) in enumerate(blocks):
        x = 43 + i * 296
        box(sl, x, 232, 284, 120, fill=bg)
        text(sl, x + 12, 240, 180, 12, t, size=8.5, color=col, bold=True)
        text(sl, x + 160, 236, 112, 20, v, size=13, font=SERIF, color=TITLE, align="r")
        yy = 262
        for n, q, u in rows:
            text(sl, x + 12, yy, 110, 14, n, size=10, color=TITLE, bold=True)
            text(sl, x + 120, yy, 90, 14, q, size=9.5, color=TEXT)
            text(sl, x + 205, yy, 68, 14, u, size=10, font=MONO, color=col, bold=True, align="r")
            yy += 28
    ifs = [("Si paramos la tarea", "DesiredCount 0: desaparecen CPU, memoria e IPv4. ECR, secreto y logs siguen generando coste."),
           ("Si retiramos todo al terminar", "El remanente se recalcula por los días reales. El consumo pasado sigue en la factura."),
           ("Si añadimos inferencia", "Tokens de entrada y salida × tarifa del modelo, en una partida separada.")]
    for i, (t, b) in enumerate(ifs):
        x = 43 + i * 296
        box(sl, x, 362, 284, 104, fill=CARD)
        text(sl, x + 12, 370, 260, 16, t, size=11.5, color=TITLE, bold=True)
        text(sl, x + 12, 392, 262, 70, b, size=10.5, color=TEXT)
    takeaway(sl, "En una demo corta, lo que más cuesta es lo que olvidamos retirar.", "Idea guía")
    footer(sl, 39, 5)
    notes(sl, """
TIEMPO 19:38–19:39 (1–2 min).
QUÉ EXPLICAR: la cifra de 0,46 USD NO representa únicamente 90 minutos de todos los servicios. Es la suma de: (1) 90 minutos de cómputo e IPv4: CPU 0,375 vCPU-h × 0,04048 = 0,01518; memoria 0,75 GB-h × 0,004445 = 0,00333375; IPv4 1,5 IP-h × 0,005 = 0,0075 → 0,02601375 USD; (2) 30 días de recursos retenidos: ECR 0,25 GB-mes × 0,10 = 0,025; secreto 0,40; logs almacenados 0,01 GB-mes × 0,03 = 0,0003 → 0,4253 USD; (3) uso del escenario: logs ingeridos 0,01 GB × 0,57 = 0,0057; una lectura del secreto 0,000005; salida 0,001 GB × 0,09 = 0,00009 → 0,005795 USD. Total 0,45710875 → 0,46 USD. El 93 % es retención.
CONSECUENCIA: parar la tarea elimina el cómputo y la IPv4, pero no ECR, secreto ni logs. Retirarlos al terminar reduce el remanente; no borra el consumo pasado. La inferencia se calcula aparte con proveedor, modelo, tokens y tarifa; un coste nulo o desconocido no significa gratis.
PREGUNTA: «¿Qué seguiría costando si ponemos DesiredCount a 0 y nos olvidamos?». Respuesta: imagen en ECR, secreto, logs almacenados y cualquier recurso añadido.
FUENTES: """ + COST_SRC + """
IMÁGENES: gráfico propio (barra proporcional a los importes; las etiquetas de los segmentos pequeños están fuera de la barra).""")
    return sl


def s40_calculadora(d):
    sl = d.slide(tag="calculadora")
    header(sl, "Estimar y vigilar", "Calculadora pública y presupuesto: antes y durante",
           "La calculadora estima antes de crear recursos y no necesita cuenta. Un presupuesto compara después el gasto real "
           "o previsto con un umbral y envía avisos.")
    box(sl, 43, 132, 444, 336, fill="FFFFFF", radius=4)
    y = 138
    for name, w in [("shot-calc-nav.png", 380), ("shot-calc-region.png", 380), ("shot-calc-fields2.png", 380)]:
        iw, ih = img_size(name, w=w)
        img(sl, name, 75, y, w=w)
        y += ih + 3
    marks = [(1, 461, 196), (2, 461, 260), (3, 461, 350), (4, 461, 438)]
    for n, x, yy in marks:
        badge(sl, x, yy, n, fill=AMBER, d=16)
    ann = [("Región", "Abre con una por defecto: elegir Europa (Irlanda) para comparar con nuestras cifras."),
           ("Sistema y arquitectura", "Linux y x86, como la tarea."),
           ("Número de tareas", "Una tarea, por día o por mes."),
           ("Duración", "Por segundo, con un mínimo de 1 minuto en Linux. Después: vCPU, memoria y almacenamiento.")]
    y = 136
    for i, (t, b) in enumerate(ann):
        badge(sl, 502, y + 1, i + 1, fill=AMBER, d=15, size=8.5)
        text(sl, 524, y, 393, 34, [[(t + "  ", {"bold": True, "color": TITLE}), (b, {})]], size=10, color=TEXT)
        y += 38
    ui_panel(sl, 500, 292, 417, 176, title="Create budget", crumbs="Billing and Cost Management  ›  Budgets  ›  Create budget")
    esquema_label(sl, 762, 295, w=150, t="ESQUEMA · simplificado")
    f1 = [("Budget type", "Cost budget"), ("Period", "Monthly"), ("Budgeted amount", "5,00 USD")]
    yy = 346
    for i, (lab, v) in enumerate(f1):
        ui_field(sl, 508 + i * 136, yy, 128, lab, v, kind="input")
    ui_field(sl, 508, 382, 400, "Alert thresholds", [("Actual cost > 80 %", True), ("Forecasted cost > 100 %", True)], kind="check")
    ui_field(sl, 508, 420, 260, "Notification", "Email o tema de SNS", kind="input")
    chip(sl, 780, 434, 128, 16, "avisa · no detiene nada", fill=CORAL, color=DARK, size=8, radius=3)
    takeaway(sl, "Estimar, vigilar y retirar: la calculadora no gasta, el presupuesto avisa y la retirada es lo que detiene el coste.",
             "Idea guía")
    footer(sl, 40, 5)
    notes(sl, """
TIEMPO 19:39–19:41 (2 min). Página pública y consola.
CALCULADORA: abrir calculator.aws (no necesita cuenta) → Create estimate → buscar «Fargate» → Configure. Cambiar la región a Europe (Ireland). Señalar: sistema operativo (Linux), arquitectura (x86), número de tareas, duración media (facturación por segundo con mínimo de 1 minuto en Linux), vCPU, memoria y almacenamiento efímero (20 GB incluidos). Introducir 0,25 vCPU y 0,5 GB y comparar con la partida de cómputo de la diapositiva de coste mensual. No guardar ni compartir la estimación si no es necesario.
BUDGETS: Billing and Cost Management › Budgets › Create budget. Mostrar las plantillas (por ejemplo «Zero spend budget» y «Monthly cost budget») y la opción personalizada: tipo Cost budget, periodo Monthly, importe, umbrales sobre coste real y previsto, destinatarios por correo o SNS. Cancel. Recordar que una alerta avisa pero no detiene la tarea.
PREGUNTA: «¿Qué configuraríais para enteraros de cualquier gasto en una cuenta de prácticas?». Respuesta: un presupuesto de gasto cero o de importe bajo con aviso por correo, además de retirar al terminar.
FUENTES: AWS Pricing Calculator (calculator.aws), consultada el 06/11/2026; AWS Cost Management User Guide, «Creating a budget» y plantillas de presupuesto.
IMÁGENES: recortes de una captura real de la página pública calculator.aws (Create estimate: Configure AWS Fargate), tomada el 06/11/2026 en español; la región por defecto (US East, Ohio) se ha dejado tal cual. El formulario de Budgets es un ESQUEMA simplificado, no una captura.""")
    return sl


def s41_optimizar(d):
    sl = d.slide(tag="optimizar")
    header(sl, "Optimización de costes", "Optimizar sin adivinar: seis decisiones",
           "Cada ahorro debe corresponder a una decisión que podamos observar en la consola o en la factura.")
    items = [("Apagar lo que no se usa", "DesiredCount 0 o retirar el servicio al terminar. Las horas son el 92 % del mes.", "CPU · memoria · IPv4", AMBER),
             ("Dimensionar con datos", "Medir CPU y memoria en CloudWatch antes de subir de 0,25 vCPU y 512 MiB.", "CPU · memoria", AMBER),
             ("Retener logs lo justo", "Fijar días de retención: por defecto un grupo no caduca. Nuestra plantilla usa 7 días.", "Logs", BLUE),
             ("Limpiar imágenes", "Una lifecycle policy en ECR borra las versiones antiguas que ya no se despliegan.", "ECR", CORAL),
             ("Evitar cargos por hora innecesarios", "IPv4 pública, NAT gateway o balanceador solo si la arquitectura los necesita.", "Red", VIOLET),
             ("Controlar la inferencia", "Limitar tokens, no reintentar a ciegas y elegir el modelo adecuado para la tarea.", "Inferencia", MINT)]
    for i, (t, b, ch, col) in enumerate(items):
        r, c = divmod(i, 3)
        x = 43 + c * 296
        y = 128 + r * 172
        box(sl, x, y, 284, 162, fill=CARD)
        badge(sl, x + 12, y + 12, i + 1, fill=col, d=22, size=11)
        text(sl, x + 44, y + 12, 230, 40, t, size=13.5, font=SERIF, color=TITLE)
        text(sl, x + 12, y + 58, 260, 64, b, size=10.5, color=TEXT)
        chip(sl, x + 12, y + 128, len(ch) * 6 + 24, 20, ch, fill=CARD2, color=col, size=9, line=col)
    takeaway(sl, "Un presupuesto ayuda a detectar el gasto; la optimización consiste en cambiar la arquitectura o retirar recursos.",
             "Idea guía")
    footer(sl, 41, 5)
    notes(sl, """
TIEMPO 19:41–19:42 (1 min).
QUÉ EXPLICAR: seis decisiones observables. (1) Apagar: el tiempo encendido es el 92 % del mes del ejemplo. (2) Dimensionar con métricas reales, no a ojo. (3) Fijar la retención de logs (por defecto, indefinida). (4) Política de ciclo de vida en ECR. (5) No añadir IPv4, NAT gateway o balanceador sin necesidad; si se añaden, sumar su coste y su limpieza. (6) Inferencia: limitar tokens de salida, evitar reintentos ocultos y elegir el modelo según la tarea.
CONSOLA: opcional, CloudWatch › Log groups › (grupo) › Actions › Edit retention setting (abrir y cancelar); ECR › repositorio › Lifecycle policy.
PREGUNTA: «¿Cuál de las seis tendría más efecto en nuestro ejemplo mensual?». Respuesta: apagar o retirar cuando no se usa.
FUENTES: AWS Well-Architected Framework, pilar de optimización de costes; CloudWatch Logs (retención); Amazon ECR (lifecycle policies); datos/costes-ejemplo.json.
IMÁGENES: diapositiva sin imágenes externas.""")
    return sl


PART4 = [s34_div5, s35_cloudwatch, s36_diagnostico, s37_billing, s38_mes, s39_demo, s40_calculadora, s41_optimizar]
