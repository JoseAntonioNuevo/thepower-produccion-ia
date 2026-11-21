"""Diapositivas 19–24: bloque 6 (observar y desplegar) y bloque 7 (entrega y cierre)."""

from comun import AWS, EVIDENCIA, LAURA, TEMARIO
from deck_lib import *  # noqa: F401,F403

LANGFUSE_DOCS = ("Documentación oficial de Langfuse, integración con LangChain/LangGraph y «Sessions» (langfuse.com/"
                 "integrations/frameworks/langchain y langfuse.com/docs/observability/features/sessions, consultadas el "
                 "16/11/2026): CallbackHandler en config['callbacks'] y propagate_attributes(session_id, user_id) dentro "
                 "de una observación que envuelve la llamada. SDK de Python 5.2.0 fijado en uv.lock.")


def s19_observar(d):
    sl = d.slide(tag="observar")
    header(sl, "Integración con Langfuse", "Seguir un turno de principio a fin",
           "Siempre, una línea JSON por turno con request_id, ruta y herramientas. Si hay claves, además una traza en "
           "Langfuse con cada nodo, llamada al modelo y herramienta, agrupada por conversación y usuario.")
    lineas = ['{"evento": "turno",',
              ' "request_id": "ae2ce887-f7c8-4518-…",',
              ' "thread_id": "api-1",',
              ' "ruta": ["inicio", "agente",',
              '          "herramientas", "agente"],',
              ' "herramientas": [{"nombre":',
              '   "buscar_documentacion", "ok": true, "ms": 3}],',
              ' "perfil": "doble", "prompt_version": "v1",',
              ' "duracion_ms": 16, "usuario": "ana"}']
    codigo(sl, 43, 134, 430, 206, lineas, "Log del turno · salida real (terminal de uvicorn)", size=9.5)
    side_note(sl, 43, 350, 430, 76, "Lo que nunca va al log",
              "El texto del usuario, los tokens de acceso, el cuerpo de un error del proveedor y la URL de la base con "
              "su contraseña.", accent=CORAL, size=10)
    y0 = panel(sl, 487, 134, 430, 292, "Traza en Langfuse · esquema, no es una captura", accent=AMBER)
    arbol = [(0, "turno-agente", "agent · session = thread_id · user = ana", BLOCK_COLORS[5]),
             (1, "agente-soporte", "LangGraph", MINT),
             (2, "inicio", "nodo", MUTED),
             (2, "agente", "llamada al modelo: tokens y coste si se informan", PINK),
             (2, "herramientas", "consultar_ticket · buscar_documentacion", AMBER),
             (2, "agente", "respuesta final", PINK)]
    y = y0 + 4
    for nivel, nombre, detalle, color in arbol:
        x = 499 + nivel * 22
        if nivel:
            line(sl, x - 12, y - 6, x - 12, y + 9, color=BORDER, w=1, head="none")
            line(sl, x - 12, y + 9, x - 3, y + 9, color=BORDER, w=1, head="none")
        chip(sl, x, y, 112, 20, nombre, fill=CARD2, color=color, size=9, font=MONO, radius=4, line=BORDER)
        text(sl, x + 120, y + 3, 290 - nivel * 22, 14, detalle, size=9, color=TEXT, check=False)
        y += 30
    text(sl, 499, y + 4, 406, 44,
         "CallbackHandler convierte cada nodo y cada llamada en un span; propagate_attributes añade sesión, usuario y "
         "etiquetas a todos los spans del turno.", size=9.5, color=TEXT)
    tag(sl, 499, y + 54, "pendiente", t="PENDIENTE · sin traza real: falta un proyecto Langfuse de laboratorio")
    en_vivo(sl, 43, 436, 874, "S20_LANGFUSE=1 LANGFUSE_PUBLIC_KEY=… LANGFUSE_SECRET_KEY=… uv run python -m agente.cli chat …",
            size=9)
    takeaway(sl, "Con el request_id del log se encuentra la traza; con la traza se explica el turno sin repetirlo.",
             "Idea guía")
    footer(sl, block=6)
    nota(sl, "19:38", "19:42",
         "BLOQUE 6 de 7 · Observar y desplegar (19:38–19:48). Temario: «integración con lagfuse». Dos niveles. El log "
         "estructurado existe siempre (también en AWS, en CloudWatch) y basta para responder «qué nodos recorrió y qué "
         "herramientas usó» sin repetir la petición. Langfuse añade la traza completa como en S6: el turno envuelto en "
         "una observación de tipo agent, la sesión es el thread_id y el usuario es el autenticado. La parte derecha es "
         "un ESQUEMA: no se ha enviado ninguna traza real durante la preparación porque no hay un proyecto Langfuse de "
         "laboratorio con claves. La ruta de código de Langfuse sí se ejecutó con el envío desactivado "
         "(LANGFUSE_TRACING_ENABLED=false) para comprobar que no falla.",
         vivo="enseñar la línea JSON en la terminal de uvicorn y copiar su request_id. Langfuse solo si hay claves de "
              "un proyecto de laboratorio (nunca las del curso de otro programa).",
         pregunta="«Un alumno dice que el agente “a veces no cita”. ¿Qué buscaríais en el log?» (Las herramientas "
                  "del turno: si buscar_documentacion devolvió ok: false.)",
         fuentes="proyecto-final/agente/observabilidad.py y servicios.py (anotar). " + LANGFUSE_DOCS + " Telemetría "
                 "de S6: 1-langGraph/app/soporte/telemetry.py. " + EVIDENCIA,
         imagenes="sin imágenes externas: esquema dibujado con formas nativas (rotulado como esquema).")
    return sl


def s20_aws(d):
    sl = d.slide(tag="aws")
    header(sl, "Despliegue en AWS", "La misma imagen en AWS: ECS Fargate y RDS PostgreSQL",
           "Al desplegar cambia dónde corre cada pieza y de dónde salen los secretos, no el código. La plantilla de "
           "CloudFormation describe toda la infraestructura del laboratorio.")
    nodo(sl, 43, 196, 122, 52, "g-user.png", "Tu IP /32", "puerto 8020", icon_s=26)
    box(sl, 181, 134, 420, 194, fill=None, line="5A7A86", dash=True)
    encajar(sl, "aws-vpc.png", 189, 140, 20, 20)
    text(sl, 215, 143, 300, 14, "VPC del laboratorio · tu Región", size=9, color=MUTED, bold=True)
    box(sl, 195, 166, 196, 150, fill=CARD, line=BORDER)
    text(sl, 205, 172, 180, 12, "SUBRED PÚBLICA", size=8, color=MUTED, bold=True)
    encajar(sl, "aws-fargate.png", 205, 190, 30, 30)
    text(sl, 243, 192, 140, 28, "Tarea ECS Fargate\n0,5 vCPU · 1 GB", size=9.5, color=TITLE, bold=True)
    chip(sl, 205, 232, 176, 26, "api · uvicorn :8020", fill=CARD2, color=MINT_L, size=9, font=MONO, radius=4,
         line=BORDER)
    chip(sl, 205, 266, 176, 26, "ejecutor · investigar", fill=CARD2, color=MINT_L, size=9, font=MONO, radius=4,
         line=BORDER)
    box(sl, 405, 166, 182, 150, fill=CARD, line=BORDER)
    text(sl, 415, 172, 170, 12, "SUBREDES PRIVADAS", size=8, color=MUTED, bold=True)
    encajar(sl, "aws-rds.png", 415, 190, 30, 30)
    text(sl, 453, 192, 130, 28, "RDS PostgreSQL\ndb.t4g.micro", size=9.5, color=TITLE, bold=True)
    text(sl, 415, 232, 164, 70, "Sin IP pública. Solo acepta el grupo de seguridad del agente.", size=9, color=TEXT)
    line(sl, 167, 222, 193, 222, color=MINT)
    line(sl, 383, 262, 403, 262, color=MINT)
    text(sl, 384, 246, 24, 12, "5432", size=7.5, color=MINT, align="c", check=False)
    servicios = [("aws-ecr.png", "ECR", "imagen por digest"), ("aws-secrets.png", "Secrets Manager",
                                                              "contraseña de RDS"),
                 ("aws-cloudwatch.png", "CloudWatch Logs", "log JSON · 3 días")]
    for i, (ic, t, s) in enumerate(servicios):
        nodo(sl, 181 + i * 143, 340, 134, 52, ic, t, s, icon_s=26, tsize=9.5)
    text(sl, 181, 400, 420, 26, "Servicios regionales que usa la tarea: fuera de la VPC.", size=9, color=MUTED)
    filas = [["Pieza", "Local", "AWS"],
             ["Imagen", "docker build", "ECR, por digest"],
             ["Config.", ".env", "variables de la tarea"],
             ["Clave BD", "ficticia", "Secrets Manager"],
             ["PostgreSQL", "Docker", "RDS privado"],
             ["Logs", "terminal", "CloudWatch"],
             ["Tokens", "de ejemplo", "propios"]]
    table(sl, 615, 134, 302, [30, 30, 40], filas, size=9, row_h=24, bold_cols=(0,))
    side_note(sl, 615, 318, 302, 108, "No desplegado",
              "La plantilla pasa cfn-lint y la imagen arranca en local. Desplegar crea recursos de pago: presupuesto, "
              "inventario y borrado al terminar.", accent=AMBER, size=9.5)
    en_vivo(sl, 43, 436, 874, "abrir infra/plantilla.json   ·   docker build -t thepower-s20-agente:local .   ·   docker run -p 8021:8020 …",
            size=9)
    takeaway(sl, "Desplegar no cambia la arquitectura: cambia dónde se ejecuta y de dónde salen los secretos.",
             "Idea guía")
    footer(sl, block=6)
    nota(sl, "19:42", "19:46",
         "temario: «despliegue en aws». Enlazar con S16 (contenedor en Fargate) y S17 (IAM y secretos). La plantilla "
         "crea una VPC propia, una tarea Fargate con dos contenedores de la misma imagen (API y ejecutor de "
         "investigaciones), una base RDS PostgreSQL privada con contraseña gestionada por RDS en Secrets Manager, logs "
         "con retención de tres días y la entrada restringida a una IPv4 /32. El servidor MCP no se despliega aparte: "
         "es un subproceso dentro del contenedor. Estado real: plantilla validada con cfn-lint sin avisos; imagen "
         "construida y probada en local (usuario no root, /health y /chat). No se ha desplegado en ninguna cuenta y "
         "pgvector en RDS no se ha comprobado. Guía paso a paso y limpieza: docs/despliegue-aws.md.",
         vivo="abrir infra/plantilla.json (Parameters, BaseDatos, Tarea) y, si da tiempo, construir y arrancar la "
              "imagen en local con los comandos de la franja.",
         pregunta="«¿Por qué la base no tiene IP pública si la API sí?»",
         fuentes="proyecto-final/infra/plantilla.json, Dockerfile y docs/despliegue-aws.md. Plantilla de S16: "
                 "4-produccion-ia/infra/s16/servicio.json. cfn-lint ejecutado con uvx el 16/11/2026: sin avisos.",
         imagenes=AWS)
    return sl


def s21_limites(d):
    sl = d.slide(tag="limites")
    header(sl, "Límites y seguridad", "Los límites están en el código, no en el prompt",
           "Un agente que decide solo necesita frenos que no dependan de que el modelo obedezca. Cada límite tiene un "
           "valor por defecto, un lugar en el código y un comportamiento conocido al superarse.")
    filas = [["Límite", "Valor", "Dónde", "Al superarlo"],
             ["Herramientas por turno", "4", "grafo.py", "el agente responde sin más herramientas"],
             ["Pasos del grafo", "2 × herramientas + 6", "observabilidad.py", "LangGraph corta el turno"],
             ["Herramientas permitidas", "3 + lista blanca", "herramientas.py · mcp_cliente.py",
              "error controlado; no se ejecuta"],
             ["Espera de MCP", "10 s", "mcp_cliente.py", "ErrorMCP: timeout"],
             ["Consultas / fuentes", "3 / 3", "investigacion.py", "informe parcial con «faltan»"],
             ["Bytes por fuente / tiempo", "1,5 MB / 30 s", "investigacion.py", "se deja de leer"],
             ["Longitud del mensaje", "2.000 caracteres", "api.py", "422 antes del agente"]]
    table(sl, 43, 134, 874, [24, 20, 26, 30], filas, size=9.5, row_h=26, bold_cols=(0, 2), font_cols={2: MONO},
          colors={2: MINT_L})
    tarjetas = [("Datos, no instrucciones", "Tickets, documentos y webs entran como datos; ninguna herramienta "
                                            "escribe ni borra.", MINT),
                ("Solo lectura", "El servidor MCP solo expone consultas: no hay nada que un texto malicioso pueda "
                                 "ordenar borrar.", BLUE),
                ("Errores sin datos sensibles", "Se guarda la etiqueta (modelo:RuntimeError), nunca el cuerpo del "
                                                "error del proveedor.", CORAL)]
    w = (874 - 20) / 3
    for i, (t, b, c) in enumerate(tarjetas):
        side_note(sl, 43 + i * (w + 10), 352, w, 108, t, b, accent=c, size=10.5)
    takeaway(sl, "El prompt pide; el código impide. Lo que de verdad protege está en el código.", "Idea guía")
    footer(sl, block=6)
    nota(sl, "19:46", "19:48",
         "repaso rápido: esta tabla reúne los frenos que han ido apareciendo. Ninguno depende del modelo. Si un "
         "documento o una web contuviera instrucciones («ignora tus reglas»), lo peor que puede pasar es una respuesta "
         "mal redactada: no existe una herramienta que escriba, la lista blanca no deja usar otras y el número de "
         "llamadas está acotado. Los valores son los de config.py y se cambian por variables. Si vamos tarde, esta "
         "diapositiva se puede saltar: su contenido ya se dijo en las diapositivas 9, 14 y 17.",
         pregunta="«¿Qué límite añadiríais si el agente pudiera crear tickets?» (Confirmación humana antes de "
                  "escribir.)",
         fuentes="proyecto-final/docs/arquitectura.md («Límites que están en el código»); agente/config.py, grafo.py, "
                 "mcp_cliente.py, investigacion.py y api.py.")
    return sl


def s22_validar(d):
    sl = d.slide(tag="validar")
    header(sl, "Integración de todos los componentes", "¿Cómo sabemos que funciona? Aceptación y pruebas",
           "Los recorridos de aceptación ejecutan el proyecto entero y comprueban los requisitos de la planificación. "
           "Debajo, tests rápidos sin coste y tests con PostgreSQL. Lo que no se ha ejecutado se dice.")
    y0 = panel(sl, 43, 134, 430, 292, "Recorridos de aceptación · 16/11/2026")
    checks = ["Respuesta directa sin herramientas", "Ticket consultado por MCP", "Ticket inexistente dicho claro",
              "Respuesta con cita", "Rechazo sin fuentes", "Caso completo con tres herramientas",
              "Investigación sin duplicar", "Informe con fuentes públicas", "Memoria del hilo",
              "Aislamiento entre usuarios"]
    for i, c in enumerate(checks):
        x = 55 + (i % 2) * 206
        y = y0 + 2 + (i // 2) * 34
        circle(sl, x, y + 2, 16, MINT)
        text(sl, x, y + 3, 16, 14, "✓", size=9, color=DARK, bold=True, align="c", check=False)
        text(sl, x + 22, y, 180, 30, c, size=9.5, color=TITLE)
    box(sl, 55, y0 + 178, 406, 70, fill="14222A", radius=4)
    text(sl, 67, y0 + 184, 382, 60,
         [[("10 de 10 ", {"bold": True, "color": MINT_L}), ("en las tres configuraciones: memoria, PostgreSQL y "
                                                             "PostgreSQL con fuentes leídas en red.", {})],
          [("evidencias/recorridos-doble-*.json", {"font": MONO, "color": MINT_L, "bold": True, "size": 8.5})]],
         size=10, color=TEXT, space=4)
    niveles = [("Perfil real con modelo", "pendiente de autorización", 200, CORAL, CORAL_BG),
               ("Recorridos de aceptación", "10 comprobaciones · 3 configuraciones", 270, MINT, TAKE_BG),
               ("Integración con PostgreSQL", "5 tests · uv run pytest -m db", 340, BLUE, BLUE_BG),
               ("Tests sin red ni coste", "38 tests · uv run pytest · unos 4 s", 410, VIOLET, VIOLET_BG)]
    y = 134
    for t, s, w, c, f in niveles:
        x = 487 + (430 - w) / 2
        box(sl, x, y, w, 56, fill=f, line=c)
        text(sl, x + 8, y + 9, w - 16, 16, t, size=10.5, color=TITLE, bold=True, align="c")
        text(sl, x + 8, y + 29, w - 16, 16, s, size=9, color=c, align="c", bold=True)
        y += 62
    text(sl, 487, y + 4, 430, 28, "Además: ruff check y ruff format sin avisos · cfn-lint sin avisos · imagen Docker "
                                  "construida y arrancada.", size=9.5, color=MUTED, align="c")
    en_vivo(sl, 43, 436, 874, "uv run pytest   ·   uv run pytest -m db   ·   uv run python -m agente.cli recorridos --guardar")
    takeaway(sl, "«Funciona» significa que hay una evidencia que otra persona puede repetir.", "Idea guía")
    footer(sl, block=7)
    nota(sl, "19:48", "19:51",
         "BLOQUE 7 de 7 · Entrega y cierre (19:48–20:00). Temario: «integración de todos los componentes». Conectar con "
         "S18 (tests automáticos en CI) y S19 (evaluación): la pirámide va de lo más barato y rápido (38 tests con "
         "dobles, sin red) a lo más caro (el perfil real, que necesita claves y gasta dinero y que no se ha ejecutado). "
         "Los recorridos de aceptación son la evidencia de que los requisitos de la diapositiva 5 se cumplen; se "
         "guardan en JSON para entregarlos. Separar siempre lo verificado de lo pendiente.",
         vivo="«uv run pytest» (unos 4 s) y, con Docker, «uv run pytest -m db». Terminar con «recorridos --guardar».",
         pregunta="«¿Qué test añadiríais antes de pasar al perfil real?» (Uno marcado llm con presupuesto y un umbral "
                  "medido, como en S19.)",
         fuentes="proyecto-final/tests (test_mcp, test_rag, test_grafo, test_investigacion, test_api, test_postgres) y "
                 "agente/cli.py (recorridos). Resultados de la ejecución local del 16/11/2026: 38 pasados sin marca, 5 "
                 "con -m db, ruff y cfn-lint sin avisos. " + EVIDENCIA)
    return sl


def s23_entrega(d):
    sl = d.slide(tag="entrega")
    header(sl, "Entrega del proyecto final", "Qué se entrega y cómo se valora",
           "El temario pide la «entrega de este proyecto final». La escuela no ha publicado todavía formato, fecha ni "
           "rúbrica: lo que sigue es la propuesta del profesor; si la plataforma dice otra cosa, manda la plataforma.")
    y0 = panel(sl, 43, 134, 430, 178, "Qué se entrega")
    entregables = ["Repositorio o ZIP con un README: el caso y cómo ejecutarlo desde cero.",
                   "evidencias/recorridos-….json generado con --guardar.",
                   "Tus ocho preguntas (cinco con respuesta, tres sin) y su resultado.",
                   "Media página de límites: qué no hace, qué falló y qué mejorarías."]
    for i, e in enumerate(entregables, 1):
        badge(sl, 55, y0 + (i - 1) * 36 + 1, i, fill=MINT, d=17, size=8.5)
        text(sl, 80, y0 + (i - 1) * 36, 380, 32, e, size=10.5, color=TITLE)
    y1 = panel(sl, 43, 322, 430, 104, "Paso a paso · docs/ejercicio.md")
    pasos = ["0 Arrancar", "1 Caso", "2 Datos", "3 MCP", "4 Prompt", "5 Memoria", "6 Citar o rechazar",
             "7 Investigar", "8 API y traza", "9 Opcional"]
    x, y = 55, y1
    for p in pasos:
        w = len(p) * 5.6 + 18
        if x + w > 461:
            x, y = 55, y + 28
        chip(sl, x, y, w, 22, p, fill=CARD2, color=MINT_L, size=8.5, line=BORDER)
        x += w + 6
    filas = [["Criterio propuesto", "Peso"],
             ["Funcionamiento y recorrido completo", "25 %"],
             ["RAG, fuentes y rechazo", "20 %"],
             ["Memoria, aislamiento y límites", "15 %"],
             ["Herramienta MCP e investigación integrada", "15 %"],
             ["Observabilidad, evaluación y tests", "15 %"],
             ["Reproducción, despliegue, coste y documentación", "10 %"]]
    table(sl, 487, 134, 430, [82, 18], filas, size=10, row_h=26, bold_cols=(1,), colors={1: MINT_L})
    tag(sl, 487, 322, "propuesta", w=430, h=18, size=8.5)
    side_note(sl, 487, 348, 430, 78, "Sin claves ni datos personales",
              "Los pasos 0–8 no necesitan claves ni gastan dinero. Ningún secreto en el repositorio.", size=10.5)
    en_vivo(sl, 43, 436, 874, "paso 0:  uv sync && uv run pytest && uv run python -m agente.cli recorridos   →   \"todo_ok\": true")
    takeaway(sl, "Empezad por el paso 0: en quince minutos tenéis el proyecto en verde en vuestro ordenador.",
             "Siguiente paso")
    footer(sl, block=7)
    nota(sl, "19:51", "19:54",
         "temario: «Proyecto final: Entrega de este proyecto final». Lo que sí consta: el temario pide la entrega; las "
         "prácticas de cada sesión son opcionales (Laura, 04/11) y a los alumnos se les dijo que lo obligatorio es el "
         "proyecto final (correo de José del 03/11). Lo que NO consta: formato, fecha límite y rúbrica. Presentar los "
         "entregables y los pesos como propuesta pendiente de confirmar con la escuela, sin dar una fecha. Abrir "
         "docs/ejercicio.md: diez pasos pequeños, cada uno con un comando para comprobarlo y una señal de «hecho»; "
         "responde a la petición de los alumnos de ejercicios paso a paso.",
         vivo="abrir proyecto-final/docs/ejercicio.md y enseñar el paso 0 y el paso 6.",
         pregunta="«¿Qué caso vais a elegir? ¿Mantenéis AetherCloud o lo adaptáis a vuestro trabajo?»",
         fuentes=TEMARIO + " " + LAURA + " Correo de José del 03/11/2026 en el mismo hilo (citado en 1a1a6346ce2eb942): "
                 "«lo obligatorio es el proyecto final». Propuesta de valoración: PLAN-S16-S20, sección 7 («Material y "
                 "propuesta de valoración»).")
    return sl


def s24_cierre(d):
    sl = d.slide(BG_SECTION, tag="cierre")
    img(sl, "thepower-logo.png", 38, 34, h=30)
    text(sl, 43, 84, 300, 14, "CIERRE", size=10, color=MINT, bold=True)
    text(sl, 43, 102, 520, 44, "Lo que nos llevamos", size=32, font=SERIF, color=TITLE)
    puntos = ["Un agente es un grafo con estado: el modelo propone y el código decide.",
              "Cada fuente tiene su contrato: tickets por MCP, política por RAG, lo público por investigación.",
              "thread_id identifica la conversación; su dueño, guardado en la base, autoriza.",
              "Citar o rechazar: «no consta» e «informe parcial» son respuestas correctas.",
              "Lo que tarda es un trabajo con estado: repetir la petición no lo duplica.",
              "«Funciona» = recorridos de aceptación que cualquiera puede repetir."]
    y = 158
    for i, p in enumerate(puntos):
        circle(sl, 43, y, 22, MINT_L)
        text(sl, 43, y + 3, 22, 16, str(i + 1), size=10.5, color=DARK, bold=True, align="c", check=False)
        text(sl, 76, y + 1, 470, 44, p, size=12, color=TITLE)
        y += 50
    box(sl, 584, 130, 333, 336, fill="1A463C", radius=8)
    text(sl, 604, 146, 300, 40, "¿Preguntas?", size=30, font=SERIF, color=MINT_L)
    text(sl, 604, 198, 300, 12, "PARA COMPROBAR", size=9, color=MINT, bold=True)
    preguntas = ["¿Dónde está el límite de herramientas por turno?",
                 "¿Qué responde la API si usas el thread_id de otra persona?",
                 "¿Qué devuelve la investigación si no encuentra fuente?"]
    bullets(sl, 604, 216, 300, 96, preguntas, size=10.5, color=TITLE, mark_color=MINT, space=4)
    text(sl, 604, 322, 300, 12, "ÚLTIMA SESIÓN DEL PROGRAMA", size=9, color=MINT, bold=True)
    text(sl, 604, 338, 300, 40, "Gracias por el curso. El proyecto final es vuestra entrega: empezad por el paso 0.",
         size=10.5, color=TITLE)
    text(sl, 604, 388, 300, 12, "MATERIALES DE S20", size=9, color=MINT, bold=True)
    text(sl, 604, 404, 300, 56, "proyecto-final: código, tests, guion, comandos y práctica paso a paso; y esta "
                                "presentación.", size=10.5, color=TITLE)
    nota(sl, "19:54", "20:00",
         "dos minutos de recapitulación y cuatro de preguntas. Leer los seis puntos y pedir a un alumno que recorra en "
         "voz alta el dibujo de la diapositiva 6 nombrando qué pieza toca cada paso del caso T-100. RESPUESTAS: límite "
         "de herramientas → grafo.py, S20_MAX_HERRAMIENTAS; thread_id ajeno → 404 «Conversación no encontrada»; sin "
         "fuente → informe parcial con la lista «faltan». SI NADIE PREGUNTA: «¿Cómo paso al perfil real?» "
         "(S20_PERFIL=real, clave en una variable, reingestar y volver a medir el umbral) y «¿Puedo cambiar MCP por una "
         "función Python?» (funcionaría, pero no cubre el temario: hace falta una llamada MCP real con descubrimiento). "
         "Al terminar: «docker compose down» (conserva los datos) y cerrar uvicorn. Es la última sesión del grupo L/X.",
         pregunta="las tres del recuadro «Para comprobar».",
         fuentes="guion de S20 (proyecto-final/docs/guion-clase.md). " + TEMARIO,
         imagenes="logotipo de thePower (recurso original del curso).")
    return sl


PART4 = [s19_observar, s20_aws, s21_limites, s22_validar, s23_entrega, s24_cierre]
