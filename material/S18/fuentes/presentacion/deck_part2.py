"""Diapositivas 19–29: bloque 3 (artefacto, secretos y OIDC) y bloque 4 (despliegue a staging, progresivo y sin corte)."""
from deck_lib import *  # noqa: F401,F403

SRC_AWS = ("Iconos de AWS: AWS Architecture Icons, paquete oficial del 31/07/2026 "
           "(aws.amazon.com/architecture/icons).")


def s13_digest(d):
    sl = d.slide(tag="digest")
    header(sl, "Artefacto inmutable", "Construir una vez y desplegar siempre ese artefacto",
           "Una etiqueta es un nombre que alguien puede mover a otra imagen. El digest es la huella SHA-256 del "
           "contenido: si cambia un solo byte, cambia el digest.")
    section_label(sl, 43, 134, 440, "Etiqueta frente a digest", color=PINK)
    box(sl, 43, 151, 440, 176, fill=CARD)
    # etiqueta que se mueve
    chip(sl, 57, 166, 110, 24, "api:latest", fill=CARD2, color=TITLE, size=10, font=MONO, line=BORDER, radius=4)
    for i, (lab, sub, y) in enumerate([("imagen v1", "lunes", 160), ("imagen v2", "martes", 196)]):
        box(sl, 300, y, 168, 30, fill=BG, line=BORDER)
        img(sl, "r-ecr-image.png", 307, y + 4, w=22, h=22)
        text(sl, 336, y + 3, 128, 13, lab, size=9.5, color=TITLE, bold=True)
        text(sl, 336, y + 16, 128, 12, sub, size=8.5, color=MUTED)
    line(sl, 169, 178, 298, 175, color=MUTED, w=1.25, dash=True)
    line(sl, 169, 178, 298, 211, color=CORAL, w=1.5)
    text(sl, 176, 154, 118, 12, "la etiqueta se movió", size=8.5, color=CORAL, check=False)
    box(sl, 55, 240, 416, 0.8, fill=BORDER, radius=0)
    chip(sl, 57, 258, 180, 24, "api@sha256:7d1e…", fill=TAKE_BG, color=MINT_L, size=10, font=MONO, line="2A5246", radius=4)
    box(sl, 300, 255, 168, 30, fill=BG, line=MINT)
    img(sl, "r-ecr-image.png", 307, 259, w=22, h=22)
    text(sl, 336, 258, 128, 13, "imagen v1", size=9.5, color=TITLE, bold=True)
    text(sl, 336, 271, 128, 12, "siempre esta", size=8.5, color=MUTED)
    line(sl, 239, 270, 298, 270, color=MINT, w=1.5)
    text(sl, 57, 296, 410, 28, "El digest no se elige: lo calcula el registro a partir del contenido de la imagen.",
         size=9, color=TEXT)
    section_label(sl, 499, 134, 418, "Por qué no reconstruir al desplegar", color=PINK)
    why = [("Otra base", "La imagen base o una dependencia pueden haber cambiado desde que se probó."),
           ("Otro resultado", "Un build no es necesariamente reproducible byte a byte."),
           ("Otra identidad", "Lo probado ya no sería lo desplegado, y el rollback no tendría a qué volver.")]
    y = 151
    for t, b in why:
        box(sl, 499, y, 418, 54, fill=CARD)
        box(sl, 499, y, 3.5, 54, fill=PINK, radius=0)
        text(sl, 512, y + 7, 396, 14, t, size=10.5, color=TITLE, bold=True)
        text(sl, 512, y + 24, 396, 28, b, size=9, color=TEXT)
        y += 59
    node(sl, 43, 341, 440, 124, "aws-ecr.png", "ECR con etiquetas inmutables",
         "ImageTagMutability: IMMUTABLE. Subir otra imagen con una etiqueta ya usada devuelve "
         "ImageTagAlreadyExistsException. Cada imagen se etiqueta con su commit de 40 caracteres.",
         icon_s=40, tsize=12, ssize=9.5)
    box(sl, 499, 341, 418, 124, fill=CARD)
    text(sl, 511, 349, 396, 12, "EN LA DEMO", size=8.5, color=PINK, bold=True)
    bullets(sl, 511, 366, 398, 96, [
        "Dockerfile: imagen base fijada por digest y dependencias por hash.",
        "Una imagen linux/amd64 con --provenance=false: un artefacto, un digest.",
        "Se prueba con smoke la misma imagen que se sube.",
        "Staging recibe repositorio@sha256:…, nunca :latest."], size=9, mark_color=PINK, space=2)
    takeaway(sl, "Se prueba un digest, se publica ese digest y se despliega ese digest: el mismo artefacto en cada paso.",
             label="Idea guía", lab_color=PINK)
    footer(sl, block=3)
    notes(sl, f"""
19:05–19:07. El enunciado pide desplegar «usando repo@sha256:… o un tag inmutable, sin reconstruir la imagen», y valora «el uso del mismo artefacto». Etiqueta: puntero con nombre; se puede reasignar (por eso :latest no identifica nada). Digest: hash SHA-256 del manifiesto de la imagen; lo calcula el registro y cambia si cambia el contenido. En ECR, con IMMUTABLE, un push con una etiqueta ya usada falla con ImageTagAlreadyExistsException: la etiqueta-commit queda ligada a una imagen. Aun así, la definición de tarea usa el digest.
--provenance=false evita que buildx publique un índice con atestaciones: así hay un único manifiesto y un único digest que desplegar. linux/amd64 porque la tarea de Fargate es X86_64 (el Mac del profesor es arm64).
Los valores 7d1e… son ilustrativos.
En vivo: docker image inspect --format '{{{{.Id}}}}' s18:A s18:B (dos contenidos, dos identificadores); mostrar el FROM con @sha256 del Dockerfile.
Pregunta: «¿Qué identifica una imagen: el nombre que le ponemos o su contenido?».
Fuentes: https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html · https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_ECS.html (consultadas 16/11/2026); demo-cicd/Dockerfile e infra/01-registro-y-publicacion.yaml. {SRC_AWS}""")
    return sl


def s14_secretos(d):
    sl = d.slide(tag="secretos")
    header(sl, "Variables de entorno y secretos", "Cada dato vive en un sitio, según quién puede verlo",
           "Configuración no es lo mismo que secreto. Un nombre de modelo o un ARN pueden estar a la vista; una clave "
           "de API solo debe existir donde se usa: nunca en Git, en la imagen ni en los logs.")
    rows = [["Dato", "Ejemplo", "Dónde vive", "Quién lo lee"],
            ["Configuración local", "API_MODE=demo", ".env, ignorado por Git", "tu terminal"],
            ["Configuración de staging", "ApiMode, ModelId", "parámetros del stack → variables de la tarea", "el contenedor"],
            [("Clave del modelo", {"color": AMBER, "bold": True}), "OPENROUTER_API_KEY", "Secrets Manager; ECS la inyecta al arrancar", "el rol de ejecución de la tarea"],
            ["Datos para los workflows", "AWS_ROLE_DESPLEGAR", "variables de GitHub (no son secretas)", "los jobs"],
            [("Credenciales de AWS", {"color": AMBER, "bold": True}), "clave temporal", "no se guardan: OIDC las crea en cada job", "ese job, durante 1 hora"],
            ["Versión", "APP_VERSION=<commit>", "dentro de la imagen", "/health y cada log"]]
    table(sl, 43, 134, 874, [1.15, 1.05, 1.75, 1.05], rows, size=9.5, row_h=24, font_cols={1: MONO},
          colors={1: MINT_L})
    section_label(sl, 43, 312, 430, "En la definición de tarea de staging", color=PINK)
    code_panel(sl, 43, 329, 430, 90, [
        "Environment:",
        "  - {Name: API_MODE, Value: !Ref ApiMode}",
        "  - {Name: OPENROUTER_MODEL, Value: !Ref ModelId}",
        "Secrets:",
        "  - Name: OPENROUTER_API_KEY",
        "    ValueFrom: !Ref SecretArn   # el ARN, no el valor"], size=8.5, fill=CARD, line=BORDER, pad=10)
    img(sl, "aws-secrets.png", 43, 427, w=34, h=34)
    text(sl, 85, 428, 388, 34, "Para cambiar la clave se actualiza el secreto y se arrancan tareas nuevas; no se "
         "reconstruye ni se cambia el código.", size=9, color=TEXT)
    section_label(sl, 489, 312, 428, "Nunca", color=CORAL)
    nev = [("g-source-code.png", "En el código ni en Git", ".env y .env.* están en .gitignore; solo se sube .env.example."),
           ("docker-mark-white.png", "En la imagen", "Ni ENV ni ARG con secretos: quedan en las capas y en el historial."),
           ("g-logs.png", "En logs ni resúmenes", "Ni el texto del usuario ni Authorization; GitHub enmascara secretos, pero no adivina.")]
    y = 329
    for ic, t, b in nev:
        box(sl, 489, y, 428, 42, fill=CORAL_BG)
        img(sl, ic, 498, y + 9, w=24, h=24)
        text(sl, 532, y + 5, 377, 14, t, size=10, color=TITLE, bold=True)
        text(sl, 532, y + 21, 377, 20, b, size=8.5, color=TEXT)
        y += 46
    takeaway(sl, "Quien no necesita un secreto no debe poder leerlo: ni el repositorio, ni la imagen, ni la pull request, ni el log.",
             label="Idea guía", lab_color=PINK)
    footer(sl, block=3)
    notes(sl, f"""
19:07–19:09. Contenido del temario «gestión de variables de entorno y secretos en despliegue». Recorrer la tabla por filas. Lo importante: (1) configuración y secreto se tratan distinto; (2) cada secreto lo lee solo quien lo usa: la clave del modelo la lee el rol de ejecución de ECS al arrancar la tarea, no GitHub ni la imagen; (3) las credenciales de AWS ni siquiera existen como secreto guardado: OIDC (siguiente diapositiva).
Variables de GitHub (vars.*) para ARN y nombres: no son secretos (un ARN no da acceso). Los secretos de GitHub (secrets.*) existen, se enmascaran en los logs y no se pasan a workflows lanzados desde forks; en esta demo no hace falta ninguno.
Secrets de ECS: la definición de tarea solo contiene el ARN (ValueFrom); el valor se inyecta como variable de entorno al arrancar el contenedor. Si se rota el secreto, hay que arrancar tareas nuevas (por ejemplo, forzar un nuevo despliegue) para que lo lean.
Si ApiMode=demo (por defecto), la plantilla no declara el secreto ni concede GetSecretValue.
En vivo: grep -n "Secrets" -A3 infra/02-staging.yaml; cat .gitignore.
Pregunta: «¿Es un secreto el ARN del rol de despliegue?».
Fuentes: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html · https://docs.github.com/en/actions/reference/security/secure-use (16/11/2026); infra/02-staging.yaml; .gitignore. {SRC_AWS} Docker: logotipo oficial.""")
    return sl


def s15_oidc(d):
    sl = d.slide(tag="oidc")
    header(sl, "OIDC · credenciales temporales", "Sin claves de AWS en GitHub: un token para cada job",
           "GitHub firma un token que dice qué repositorio, rama o entorno ejecuta el job. AWS comprueba la firma y la "
           "confianza del rol, y devuelve credenciales que caducan en una hora.")
    cols = [("gh-actions.png", "Job de GitHub", "desplegar-staging"), ("github-mark-white.png", "Proveedor OIDC", "de GitHub: firma el JWT"),
            ("r-iam-sts.png", "AWS STS", "AssumeRoleWithWebIdentity"), ("aws-ecs.png", "ECS y ECR", "las llamadas del despliegue")]
    xs = [143, 362, 581, 800]
    for (ic, t, s), cx in zip(cols, xs):
        box(sl, cx - 100, 134, 200, 44, fill=CARD, line=BORDER)
        img(sl, ic, cx - 92, 142, w=28, h=28)
        text(sl, cx - 58, 139, 152, 15, t, size=10.5, color=TITLE, bold=True)
        text(sl, cx - 58, 156, 154, 16, s, size=7.5, color=MUTED, font=MONO if "." in s or "With" in s else SANS)
        line(sl, cx, 180, cx, 382, color=BORDER, w=1, head="none", dash=True)
    msgs = [(0, 1, 202, VIOLET, "1  pide un token (id-token: write)"),
            (1, 0, 230, VIOLET, "2  JWT firmado: aud, sub, repository…"),
            (0, 2, 258, BLUE, "3  AssumeRoleWithWebIdentity(token, rol)"),
            (2, 0, 326, MINT, "5  credenciales temporales · 1 hora"),
            (0, 3, 360, MINT, "6  llamadas firmadas: describe-images, register-task-definition, update-service"),
            ]
    for a, b, y, col, t in msgs:
        x1, x2 = xs[a], xs[b]
        line(sl, x1 + (4 if x2 > x1 else -4), y, x2 + (-4 if x2 > x1 else 4), y, color=col, w=1.5)
        lx = min(x1, x2) + 8
        text(sl, lx, y - 15, abs(x2 - x1) - 16, 12, t, size=8.5, color=TITLE, bold=True, check=False)
    box(sl, 593, 268, 200, 38, fill=BLUE_BG, line=BLUE)
    text(sl, 601, 271, 186, 34, "4  comprueba la firma, aud y sub contra la confianza del rol", size=8.5, color=TITLE,
         bold=True)
    side_note(sl, 43, 392, 431, 73, "Con una clave guardada",
              "Una clave de acceso de AWS en los secretos de GitHub no caduca sola, sirve desde cualquier sitio y hay "
              "que rotarla. Si se filtra, se filtra el acceso.", accent=CORAL, size=9.5)
    side_note(sl, 486, 392, 431, 73, "Con OIDC",
              "Nada que guardar ni rotar. El token dura minutos, solo vale para STS y las credenciales caducan "
              "en una hora. La confianza del rol decide qué jobs pueden obtenerlas.", accent=MINT, size=9.5)
    takeaway(sl, "Si alguien copia el workflow en otro repositorio o lo lanza desde otra rama, el token dirá otra cosa y AWS no dará credenciales.",
             label="Idea guía", lab_color=PINK)
    footer(sl, block=3)
    notes(sl, f"""
19:09–19:11. Secuencia de OIDC. 1 El job pide un token al proveedor de GitHub; solo puede hacerlo si declara permissions: id-token: write. 2 GitHub devuelve un JWT firmado con claims: iss (el emisor), aud (para quién es), sub (quién lo pide: repositorio y rama o entorno), repository, environment, ref… 3 La acción aws-actions/configure-aws-credentials llama a STS AssumeRoleWithWebIdentity con ese token y el ARN del rol. 4 STS verifica la firma con el proveedor OIDC registrado en el proyecto de AWS y compara aud y sub con las condiciones de la confianza del rol. 5 Devuelve credenciales temporales (aquí, como máximo una hora: MaxSessionDuration 3600) con las que el job llama a ECS y ECR.
El proveedor OIDC de IAM (token.actions.githubusercontent.com, audiencia sts.amazonaws.com) se crea una vez por proyecto; en la demo lo crea infra/01 salvo que ya exista.
En vivo: abrir publicar-main.yml y señalar id-token: write y role-to-assume: vars.AWS_ROLE_PUBLICAR.
Pregunta: «¿Qué tendría que robar un atacante para desplegar en nuestro staging?».
Fuentes: https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws · https://docs.github.com/en/actions/reference/security/oidc · https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html (16/11/2026). {SRC_AWS} Logotipos: GitHub Actions (github/explore) y octicon mark-github (primer/octicons).""")
    return sl


def s16_sub(d):
    sl = d.slide(tag="sub-aud")
    header(sl, "OIDC · la confianza del rol", "El rol confía en un sub exacto, no en «mi repositorio»",
           "El claim sub cambia según el contexto del job. Con environment: staging, GitHub emite un sub que nombra el "
           "entorno, y solo lo emite si las reglas del entorno permiten esa ejecución.")
    section_label(sl, 43, 134, 400, "Confianza del rol desplegar · infra/02-staging.yaml", color=PINK)
    code_panel(sl, 43, 151, 400, 206, [
        "Effect: Allow",
        "Principal:",
        "  Federated: arn:aws:iam::<proyecto>:",
        "    oidc-provider/token.actions.",
        "    githubusercontent.com",
        "Action: sts:AssumeRoleWithWebIdentity",
        "Condition:",
        "  StringEquals:",
        "    token.actions…:aud: sts.amazonaws.com",
        "    token.actions…:sub: !Ref SubDesplegar",
        "",
        "# SubDesplegar, leído con Diagnóstico · OIDC:",
        "# repo:ORG@111/REPO@222:environment:staging"], size=8.5, fill=CARD, line=BORDER, pad=10)
    section_label(sl, 459, 134, 458, "Qué sub emite cada job", color=PINK)
    rows = [["Contexto del job", "sub (formato clásico)", "¿Rol desplegar?"],
            ["Pull request hacia main", "repo:ORG/REPO:pull_request", ("No", {"color": CORAL, "bold": True})],
            ["Push a main (publicar)", "repo:ORG/REPO:ref:refs/heads/main", ("No · es el de publicar", {"color": AMBER, "bold": True})],
            ["environment: staging, desde main", "repo:ORG/REPO:environment:staging", ("Sí", {"color": MINT, "bold": True})],
            ["environment: staging, otra rama", "no se emite: el entorno lo rechaza", ("No", {"color": CORAL, "bold": True})]]
    table(sl, 459, 151, 458, [1.2, 1.65, 0.85], rows, size=8.5, row_h=30, font_cols={1: MONO}, colors={1: MINT_L})
    text(sl, 459, 305, 458, 50, [[("Repositorios creados desde el 15/07/2026: ", {"bold": True, "color": TITLE}),
         ("el sub incluye identificadores inmutables, repo:ORG@<id>/REPO@<id>:…. Por eso se copia el sub real en "
          "lugar de escribirlo a mano.", {})]], size=9, color=TEXT)
    side_note(sl, 43, 370, 431, 95, "aud = sts.amazonaws.com",
              "Dice para quién es el token: solo para AWS STS. Lo exige StringEquals; un token pedido para otro "
              "destinatario no sirve aquí.", accent=PINK, size=9.5)
    side_note(sl, 486, 370, 431, 95, "Environment staging · solo main",
              "Deployment branches: Selected branches → main. Un workflow_dispatch se puede lanzar desde cualquier "
              "rama con el YAML de esa rama; esta regla lo detiene antes de que exista el token.", accent=PINK, size=9.5)
    takeaway(sl, "aud dice para quién es el token y sub quién lo pide. Con StringEquals y el sub real, ni una PR ni otra rama despliegan.",
             label="Idea guía", lab_color=PINK)
    footer(sl, block=3)
    notes(sl, """
19:11–19:14. El enunciado: «El job declarará environment: staging: el sub debe referirse a ese entorno, no a ref:refs/heads/main. Ajusta la confianza al sub real emitido (por ejemplo, repo:ORG/REPO:environment:staging), que puede incorporar IDs inmutables, y a aud = sts.amazonaws.com». Y: «El environment staging de GitHub debe permitir despliegues únicamente desde la rama main. Esto es necesario porque un workflow_dispatch puede lanzarse manualmente desde otras ramas».
Tabla: cuando un job declara environment, el sub pasa a ser …:environment:<nombre> (ya no incluye la rama); por eso la regla de ramas del environment es la que limita desde dónde se despliega. El rol de publicar confía en …:ref:refs/heads/main (job sin environment). Desde el 15/07/2026, los repositorios nuevos (o los que optan) usan el formato inmutable repo:OWNER@ID/REPO@ID:…; el workflow diagnostico-oidc.yml lo imprime sin imprimir el token.
StringEquals en lugar de StringLike: sin comodines. repo:ORG/* permitiría a cualquier repositorio de la organización.
Doble barrera en el workflow: además comprueba GITHUB_REF == refs/heads/main (ayuda, no barrera).
En vivo: gh workflow run diagnostico-oidc.yml y leer sub y aud en el resumen (si hay repositorio publicado). Configuración del environment con gh api (README de la demo, paso 4).
Pregunta: «¿Qué ocurriría si la confianza usara StringLike con repo:ORG/*?».
Fuentes: https://docs.github.com/en/actions/reference/security/oidc (formato del sub y sub inmutable) · https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments · https://docs.github.com/en/rest/deployments/branch-policies (16/11/2026); infra/02-staging.yaml.""")
    return sl


def s17_publicar(d):
    sl = d.slide(tag="demo-publicar")
    header(sl, "Demo 2 · publicar desde main", "Integrar en main deja una imagen validada y su digest",
           "Al integrar la PR, publicar-main.yml repite las comprobaciones sobre ese commit y, solo si pasan, construye, "
           "prueba y sube una imagen. El resumen anota el digest con el que desplegaremos y volveremos atrás.")
    steps = [("Comprobaciones", "SIN AWS", "ok", ["needs: comprobaciones", "uses: ./…/comprobaciones.yml"],
              "Las mismas que en la PR, sobre el commit integrado."),
             ("Credenciales OIDC", "ROL PUBLICAR · 1 h", "warn", ["role-to-assume:", "  ${{ vars.AWS_ROLE_PUBLICAR }}"],
              "Solo para el job publicar; el sub es …:ref:refs/heads/main."),
             ("¿Ya está publicado?", "SOLO LECTURA", "ok", ["aws ecr describe-images \\", "  --image-ids imageTag=$GITHUB_SHA"],
              "Si se relanza, reutiliza la imagen: las etiquetas son inmutables."),
             ("Construir y probar", "SIN SUBIR", "ok", ["docker build --platform linux/amd64 …", "bash scripts/smoke.sh …"],
              "Smoke a la imagen exacta que se va a subir."),
             ("Publicar", "ESCRIBE EN ECR", "warn", ['docker push "$REGISTRO/$REPO:$GITHUB_SHA"'],
              "La etiqueta es el commit de 40 caracteres."),
             ("Registrar el digest", "RESUMEN", "info", ["imageDetails[0].imageDigest", "→ $GITHUB_STEP_SUMMARY"],
              "Queda en la ejecución para desplegar y para el rollback.")]
    cw, ch = (874 - 2 * 10.8) / 3, 113.8
    for i, (t, lab, kind, code, b) in enumerate(steps):
        x = 43 + (i % 3) * (cw + 10.8)
        y = 134 + (i // 3) * (ch + 8.6)
        box(sl, x, y, cw, ch, fill=CARD, line=AMBER if kind == "warn" else None)
        badge(sl, x + 8.6, y + 7.9, i + 1, fill=AMBER if kind == "warn" else MINT, d=16, size=8.5)
        text(sl, x + 30.2, y + 7.2, 140, 17.3, t, size=10.5, color=TITLE, bold=True)
        wl = len(lab) * 7 * 0.7 + 16
        chip_tag(sl, x + cw - 8.6 - wl, y + 8.6, lab, kind=kind, w=wl)
        code_panel(sl, x + 8.6, y + 31.7, cw - 17.2, 43.2, code, size=8.5)
        text(sl, x + 10.1, y + 80.6, cw - 20, 30, b, size=9, color=TEXT)
    box(sl, 43, 382, 874, 83, fill=CARD)
    text(sl, 54.5, 389, 600, 12.2, "RESUMEN DE LA EJECUCIÓN · «IMAGEN PUBLICADA»", size=8.5, color=BLUE, bold=True)
    tag(sl, 745, 387, "ilustrativo", w=162)
    rows = [["Commit", "a8b0d4c2f1e9…  (40 caracteres)", "Etiqueta inmutable", "a8b0d4c2f1e9…"],
            ["Repositorio ECR", "s18-tu-nombre", "Digest", ("sha256:c41b9e07…", {"color": AMBER, "bold": True})]]
    table(sl, 54.5, 409, 851, [0.8, 1.6, 0.9, 1.6], rows, size=9, row_h=22, font_cols={1: MONO, 3: MONO},
          colors={1: MINT_L, 3: MINT_L}, header_fill=CARD2, header_color=TITLE)
    takeaway(sl, "main no despliega: publica. El digest es el contrato entre publicar y desplegar.",
             label="Idea guía", lab_color=PINK)
    footer(sl, block=3)
    notes(sl, """
19:14–19:17. Segundo momento de demo. El enunciado: «Tras integrar en main, repite el análisis, los tests y la construcción sobre ese commit. Solo si pasan, publica esa imagen en ECR y registra su digest».
Pasos de publicar-main.yml: needs: comprobaciones (si fallan, no hay job publicar); OIDC con el rol de publicar (solo ECR de este laboratorio); comprobar si el commit ya existe en ECR (relanzar un workflow no intenta sobrescribir una etiqueta inmutable); construir linux/amd64 con --provenance=false y probar esa imagen con el smoke; docker push con la etiqueta = commit; leer el digest de ECR y escribirlo en el resumen de la ejecución; docker logout siempre.
El resumen de la diapositiva es ilustrativo: formato real del workflow, valores inventados (no hay ensayo en GitHub todavía).
En vivo · GitHub: gh pr merge de la PR de la versión B; gh run watch; aws ecr describe-images --repository-name $LAB (comandos.md). Mientras corre, enseñar una ejecución anterior ya terminada.
En vivo · local: docker image inspect de s18:A y s18:B.
Pregunta: «¿Por qué no desplegamos directamente al final de este workflow?» (separar responsabilidades y permisos; desplegar es una decisión).
Fuentes: demo-cicd/.github/workflows/publicar-main.yml; infra/01-registro-y-publicacion.yaml (rol publicar: GetAuthorizationToken + 7 acciones de ECR sobre un único repositorio).""")
    return sl


def s18_desplegar(d):
    sl = d.slide(tag="desplegar")
    header(sl, "Despliegue a staging", "Desplegar es cambiar qué digest ejecuta el servicio",
           "desplegar-staging.yml se lanza a mano desde main con un digest ya publicado. No construye nada: registra una "
           "definición de tarea igual a la anterior salvo la imagen y pide a ECS que la ejecute.")
    steps = [(MUTED, "Comprobar", "Rama main y digest con forma sha256: + 64 hex."),
             (BLUE, "OIDC", "Environment staging: regla de ramas y rol desplegar."),
             (VIOLET, "¿Existe?", "El digest está en ECR y tiene etiqueta de commit."),
             (AMBER, "Anotar", "Qué digest y qué revisión hay ahora (para volver)."),
             (CORAL, "Registrar", "Nueva definición: misma configuración, otra imagen."),
             (MINT, "Actualizar", "update-service y esperar a services-stable.")]
    w = (874 - 5 * 13) / 6
    for i, (col, t, b) in enumerate(steps):
        x = 43 + i * (w + 13)
        step_card(sl, x, 134, w, 92, i + 1, t, b, accent=col)
        if i < 5:
            line(sl, x + w + 1, 180, x + w + 12, 180, color=MINT, w=1.5)
    section_label(sl, 43, 240, 470, "Paso 5 · solo cambia la imagen", color=VIOLET)
    code_panel(sl, 43, 257, 470, 120, [
        "aws ecs describe-task-definition … > anterior.json",
        'jq --arg imagen "$CUENTA.dkr.ecr.$REGION…/$REPO@$DIGEST" \'',
        "  .containerDefinitions[0].image = $imagen",
        "  | del(.taskDefinitionArn, .revision, .status,",
        "        .requiresAttributes, .compatibilities,",
        "        .registeredAt, .registeredBy)",
        "' anterior.json > nueva.json",
        "aws ecs register-task-definition --cli-input-json …"], size=8.5, fill=CARD, line=BORDER, pad=10)
    text(sl, 43, 383, 470, 80, [[("Entradas como variables, no interpoladas. ", {"bold": True, "color": TITLE}),
         ("El digest y el motivo que escribe una persona pasan al script como DIGEST y MOTIVO en env:, nunca como "
          "${{ inputs.digest }} dentro de run:. Así no pueden inyectar comandos.", {})]], size=9.5, color=TEXT)
    section_label(sl, 531, 240, 386, "Run workflow · desplegar-staging", color=VIOLET)
    ui_panel(sl, 531, 257, 386, 206, title="Desplegar · staging", crumbs="Actions › Desplegar · staging › Run workflow")
    esquema_label(sl, 767, 243, w=150)
    yy = ui_field(sl, 543, 316, 360, "Use workflow from", "Branch: main", kind="select", lw=180)
    yy = ui_field(sl, 543, yy + 8, 360, "Digest publicado por «Publicar · main» (sha256:…)",
                  "sha256:c41b9e07…", kind="input")
    yy = ui_field(sl, 543, yy + 8, 360, "Motivo", [("despliegue", True), ("rollback", False)], kind="radio")
    ui_button(sl, 543, yy + 12, 110, "Run workflow", primary=True)
    takeaway(sl, "Desplegar y volver atrás son la misma operación con distinto digest.", label="Idea guía", lab_color=VIOLET)
    footer(sl, block=4)
    notes(sl, """
19:17–19:20. El enunciado: «Despliega a staging mediante workflow_dispatch desde main usando repo@sha256:... o un tag inmutable, sin reconstruir la imagen».
Recorrer los seis pasos del job de desplegar-staging.yml: 1 comprobación de rama y formato del digest (ayuda; la barrera es el environment); 2 environment: staging + id-token: write → credenciales del rol desplegar; 3 describe-images con el digest y búsqueda de una etiqueta de 40 hexadecimales (solo se despliega lo que publicó publicar-main); 4 se anota la definición y el digest actuales, que aparecerán en la columna «Antes» del resumen; 5 se copia la definición anterior cambiando solo image (jq elimina los campos de solo lectura que devuelve describe); 6 update-service y aws ecs wait services-stable. concurrency: group staging, sin cancelar.
Seguridad: los inputs pasan por env: (DIGEST, MOTIVO) para evitar inyección de comandos en run:, recomendación de GitHub.
El panel derecho es un esquema del formulario de GitHub, no una captura.
En vivo: abrir desplegar-staging.yml y señalar on: workflow_dispatch: inputs y environment: staging.
Pregunta: «¿Qué pasa si escribo :latest en el campo digest?» (el paso 1 lo rechaza por formato).
Fuentes: demo-cicd/.github/workflows/desplegar-staging.yml; https://docs.github.com/en/actions/reference/security/secure-use (inyección de scripts); https://docs.github.com/en/actions/how-tos/deploy/deploy-to-third-party-platforms/amazon-elastic-container-service.""")
    return sl


def s19_rolling(d):
    sl = d.slide(tag="rolling")
    header(sl, "Rolling update · sin corte", "ECS arranca la versión nueva antes de parar la anterior",
           "Con mínimo sano del 100 % y máximo del 200 %, durante el cambio conviven dos tareas. Si la nueva no llega a "
           "estar sana, el circuit breaker detiene el despliegue y vuelve a la última revisión completada.")
    section_label(sl, 43, 134, 590, "Si B arranca bien", color=VIOLET)
    X0, X1 = 150, 630
    def bar(y, x1, x2, fill, col, t):
        box(sl, x1, y, x2 - x1, 22, fill=fill, line=col, radius=3)
        text(sl, x1 + 6, y + 4, x2 - x1 - 10, 14, t, size=8.5, color=col, bold=True, check=False)
    text(sl, 43, 156, 100, 26, "Tarea A\nrevisión 4", size=9, color=TITLE, bold=True)
    bar(158, X0, 470, BLUE_BG, BLUE, "A atiende el tráfico")
    box(sl, 470, 158, 28, 22, fill=CARD2, line=BORDER, radius=3)
    text(sl, 43, 190, 100, 26, "Tarea B\nrevisión 5", size=9, color=TITLE, bold=True)
    bar(192, 230, 330, AMBER_BG, AMBER, "arranca")
    bar(192, 330, 430, VIOLET_BG, VIOLET, "health check")
    bar(192, 430, X1, TAKE_BG, MINT, "B sana: atiende el tráfico")
    marks = [(230, "t1 · update-service"), (430, "t2 · B sana"), (498, "t3 · A se para"), (600, "t4 · estable")]
    for x, t in marks:
        line(sl, x, 150, x, 222, color=MUTED, w=0.75, head="none", dash=True)
    for i, (x, t) in enumerate(marks):
        text(sl, x - 50, 224 + (i % 2) * 12, 100, 12, t, size=8, color=MUTED, align="c", check=False)
    section_label(sl, 43, 264, 590, "Si B no llega a estar sana", color=CORAL)
    text(sl, 43, 286, 100, 26, "Tarea A\nrevisión 4", size=9, color=TITLE, bold=True)
    bar(288, X0, X1, BLUE_BG, BLUE, "A sigue atendiendo: nunca se paró")
    text(sl, 43, 320, 100, 26, "Tarea B\nrevisión 5", size=9, color=TITLE, bold=True)
    bar(322, 230, 300, CORAL_BG, CORAL, "falla")
    bar(306 + 16, 304, 374, CORAL_BG, CORAL, "falla")
    bar(322, 378, 448, CORAL_BG, CORAL, "falla")
    box(sl, 456, 318, 174, 30, fill=CARD2, line=CORAL)
    text(sl, 462, 321, 164, 26, "circuit breaker → vuelve a la revisión 4", size=8.5, color=TITLE, bold=True, check=False)
    side_note(sl, 43, 364, 590, 101, "Por qué el workflow comprueba después",
              "Tras un rollback del circuit breaker el servicio también queda «estable». Por eso desplegar-staging lee el "
              "despliegue PRIMARY (definición y rolloutState = COMPLETED) y el imageDigest de la tarea en marcha, y falla "
              "si no son los pedidos. Un despliegue que vuelve atrás solo es un despliegue fallido.", accent=CORAL, size=9.5)
    section_label(sl, 649, 134, 268, "Configuración del servicio", color=VIOLET)
    code_panel(sl, 649, 151, 268, 132, [
        "DeploymentConfiguration:",
        "  MinimumHealthyPercent: 100",
        "  MaximumPercent: 200",
        "  DeploymentCircuitBreaker:",
        "    Enable: true",
        "    Rollback: true",
        "HealthCheck: /health cada 15 s",
        "  3 reintentos · gracia 20 s"], size=8.5, fill=CARD, line=BORDER, pad=10)
    node(sl, 649, 295, 268, 72, "aws-fargate.png", "ECS · Fargate",
         "Una tarea de 0,25 vCPU y 0,5 GB; sin balanceador ni NAT.", icon_s=34, tsize=11, ssize=9)
    side_note(sl, 649, 379, 268, 86, "Lo que no ve ECS",
              "Si B arranca y /health responde, ECS da el despliegue por bueno aunque /clasificar falle.", accent=VIOLET,
              size=9.5)
    takeaway(sl, "Sin corte no significa sin riesgo: ECS comprueba que B arranca, no que hace bien su trabajo.",
             label="Idea guía", lab_color=VIOLET)
    footer(sl, block=4)
    notes(sl, f"""
19:20–19:22. Temario: «despliegues sin downtime». Rolling update de ECS con una tarea: minimumHealthyPercent 100 obliga a mantener la tarea A mientras B no esté sana; maximumPercent 200 permite que haya dos a la vez. Secuencia: update-service; ECS arranca B; el health check del contenedor (python -c urllib a /health cada 15 s, 3 reintentos, 20 s de gracia) la marca sana; ECS para A; el servicio queda estable. Sin balanceador, la «entrada de tráfico» es la IP de la tarea (cambia al cambiar de tarea): en producción habría un balanceador.
Circuit breaker con rollback: si las tareas de B no llegan a estado estable, ECS marca el despliegue como fallido y vuelve al último despliegue COMPLETED. Diagrama ilustrativo (escala de tiempo no medida).
Por eso el workflow comprueba el despliegue PRIMARY y el digest de la tarea en marcha después de services-stable. Que el cliente no note el cambio no se demuestra aquí: hace falta un endpoint estable y peticiones continuas (diapositiva 28).
En vivo: aws ecs describe-services --query 'services[0].deployments' si hay staging.
Pregunta: «¿Qué diferencia hay entre "el servicio está estable" y "el servicio ejecuta B"?».
Fuentes: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html · https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html (16/11/2026); infra/02-staging.yaml. {SRC_AWS}""")
    return sl


def s20_smoke(d):
    sl = d.slide(tag="smoke")
    header(sl, "Verificar después de desplegar", "Un job en verde no basta: la API tiene que responder",
           "El despliegue termina probando el servicio real como lo haría un cliente: salud, versión esperada, una "
           "clasificación válida y el rechazo de una entrada inválida.")
    section_label(sl, 43, 134, 430, "scripts/smoke.sh · cuatro comprobaciones", color=VIOLET)
    checks = [("GET /health", "estado = ok (reintenta mientras arranca)"),
              ("version = commit esperado", "responde B y no otra cosa que siguiera en marcha"),
              ("POST /clasificar", "categoría y prioridad válidas, respuesta y request_id"),
              ('POST {"texto": ""}', "la API lo rechaza con 422")]
    y = 151
    for i, (t, b) in enumerate(checks, 1):
        box(sl, 43, y, 430, 44, fill=CARD)
        badge(sl, 52, y + 14, i, fill=VIOLET, d=16, size=8.5)
        text(sl, 76, y + 6, 390, 14, t, size=10, color=TITLE, bold=True, font=MONO)
        text(sl, 76, y + 23, 390, 16, b, size=9, color=TEXT)
        y += 49
    tag(sl, 43, 352, "real", w=172)
    code_panel(sl, 43, 370, 430, 95, [
        'GET /health -> {"estado":"ok","version":"version-B",…}',
        'POST /clasificar -> {…"categoria":"acceso",…}',
        "POST /clasificar con texto vacío -> 422",
        "SMOKE CORRECTO: versión version-B, modo demo"], size=8.5, fill="0B1418", line=BORDER, pad=10)
    section_label(sl, 489, 134, 428, "La red: abrir solo lo necesario y cerrarlo siempre", color=VIOLET)
    box(sl, 489, 151, 428, 196, fill=CARD)
    node(sl, 499, 166, 128, 50, "gh-actions.png", "Runner", "IP /32 del job", icon_s=24, tsize=10, ssize=8.5)
    box(sl, 657, 160, 118, 62, fill=BG, line=VIOLET, dash=True)
    img(sl, "g-shield.png", 668, 166, w=22, h=22)
    text(sl, 694, 166, 78, 26, "grupo de\nseguridad", size=8.5, color=TITLE, bold=True)
    text(sl, 665, 194, 106, 26, "8000 solo desde\nesa IP, temporal", size=8, color=MUTED)
    node(sl, 801, 166, 106, 50, "aws-fargate.png", "Tarea", "IP pública", icon_s=24, tsize=10, ssize=8.5)
    line(sl, 628, 191, 655, 191, color=VIOLET, w=1.5)
    line(sl, 776, 191, 799, 191, color=VIOLET, w=1.5)
    seq = [("abrir", "authorize-security-group-ingress con la IP del runner", AMBER),
           ("probar", "bash scripts/smoke.sh http://IP:8000 <commit>", MINT),
           ("cerrar", "revoke-… con if: always(), también si falla", CORAL)]
    yy = 236
    for t, b, col in seq:
        chip(sl, 501, yy, 58, 18, t, fill=col, color=DARK, size=8.5, radius=3)
        text(sl, 567, yy + 2, 340, 16, b, size=8.5, color=TEXT, font=MONO if "bash" in b else SANS)
        yy += 26
    text(sl, 501, 316, 406, 26, "Además retira reglas antiguas con la misma descripción que hubieran quedado.",
         size=8.5, color=MUTED)
    side_note(sl, 489, 359, 428, 106, "Alternativas más cerradas",
              "Una tarea efímera de smoke dentro de la VPC, autorizada por grupo de seguridad (sin abrir nada a "
              "Internet), o un balanceador con health checks. Para un laboratorio de una tarea, la regla /32 temporal "
              "es la opción más simple.", accent=VIOLET, size=9.5)
    takeaway(sl, "Comprobamos lo que recibiría un usuario, con la versión que esperábamos, y cerramos el puerto pase lo que pase.",
             label="Idea guía", lab_color=VIOLET)
    footer(sl, block=4)
    notes(sl, f"""
19:22–19:25. El enunciado: «Verifica /health y una petición funcional; un job correcto no basta si el servicio no responde». scripts/smoke.sh lo usan tres sitios: comprobaciones (contenedor local del runner), publicar-main (imagen antes de subirla) y desplegar-staging (servicio real). Comprueba también la versión: si ECS hubiera vuelto a A, el smoke fallaría.
Red: la API de staging solo admite tu IPv4 /32 (AllowedCidr). Un runner alojado de GitHub tiene otra IP; el workflow la consulta (checkip.amazonaws.com), añade una regla temporal al grupo de seguridad con la descripción smoke-github-actions, ejecuta el smoke y la revoca en un paso con if: always(). El rol desplegar solo puede autorizar y revocar reglas en ese grupo de seguridad.
Alternativa (la del plan de la clase): tarea de smoke dentro de la VPC; es más cerrada pero añade otra definición de tarea; se deja como mejora.
La salida del panel es real: ensayo local del 17/11/2026 con la imagen B.
En vivo: bash scripts/smoke.sh http://127.0.0.1:8000 version-B con el contenedor B en local.
Pregunta: «¿Por qué el smoke comprueba un 422 y no solo un 200?».
Fuentes: demo-cicd/scripts/smoke.sh; .github/workflows/desplegar-staging.yml (pasos «Abrir el puerto…», «Salud y petición funcional…», «Cerrar el puerto»); .build/s18/logs/ensayo-comandos.txt. {SRC_AWS}""")
    return sl


def s20a_progresivo(d):
    sl = d.slide(tag="progresivo")
    header(sl, "Despliegues progresivos", "Exponer la versión nueva a poco tráfico antes que a todo",
           "Rolling sustituye tareas. Blue/green, canary y lineal reparten tráfico entre dos versiones y vuelven atrás "
           "moviendo el tráfico. ECS ofrece las cuatro; las tres últimas necesitan un balanceador o Service Connect.")
    strategies = [("Rolling", "la de la demo", [[0, 0], [0, 1], [1, 1]], ["inicio", "conviven", "fin"],
                   "Arranca tareas nuevas y para las antiguas. Con circuit breaker, vuelve solo si no arrancan.",
                   "Servicio pequeño, sin balanceador."),
                  ("Blue/green", "dos entornos", [[0] * 4, [0] * 4, [1] * 4], ["azul", "verde probado", "cambio"],
                   "Se levanta el entorno verde completo, se prueba y el tráfico cambia de una vez.",
                   "Validar antes de recibir usuarios y volver al instante."),
                  ("Canary", "una muestra", [[0] * 10, [0] * 9 + [1], [1] * 10], ["0 %", "10 %", "100 %"],
                   "Un porcentaje pequeño de tráfico real va a la versión nueva; si va bien, el resto.",
                   "Cambios de riesgo con métricas fiables."),
                  ("Lineal", "por escalones", [[0, 0, 0, 1], [0, 0, 1, 1], [0, 1, 1, 1]], ["25 %", "50 %", "75 % → 100 %"],
                   "El tráfico se mueve en incrementos iguales y se observa cada escalón.",
                   "Despliegues largos con varios puntos de parada.")]
    cw = (874 - 3 * 10) / 4
    for i, (t, s, frames, labels, b, when) in enumerate(strategies):
        x = 43 + i * (cw + 10)
        box(sl, x, 134, cw, 262, fill=CARD, line=CORAL if i == 0 else None)
        text(sl, x + 12, 142, cw - 24, 18, t, size=13, font=SERIF, color=TITLE)
        text(sl, x + 12, 162, cw - 24, 12, s.upper(), size=8, color=CORAL, bold=True)
        yy = 182
        for fr, lab in zip(frames, labels):
            n = len(fr)
            bw = (cw - 24 - 74) / n
            for j, v in enumerate(fr):
                box(sl, x + 12 + j * bw, yy, bw - 1.5, 16, fill=MINT if v else BLUE, radius=1)
            text(sl, x + cw - 82, yy + 2, 72, 12, lab, size=8, color=MUTED, check=False)
            yy += 22
        text(sl, x + 12, 252, cw - 24, 64, b, size=9, color=TEXT)
        text(sl, x + 12, 322, cw - 24, 12, "CUÁNDO", size=8, color=MUTED, bold=True)
        text(sl, x + 12, 336, cw - 24, 56, when, size=9, color=TITLE)
    box(sl, 43, 402, 12, 10, fill=BLUE, radius=1)
    text(sl, 60, 400, 120, 12, "versión actual", size=8.5, color=MUTED)
    box(sl, 150, 402, 12, 10, fill=MINT, radius=1)
    text(sl, 167, 400, 120, 12, "versión nueva", size=8.5, color=MUTED)
    box(sl, 43, 418, 874, 47, fill=CARD)
    text(sl, 54.5, 424, 851, 38, [[("Plan para producción (README de la demo): ", {"bold": True, "color": CORAL}),
         ("canary del 10 %, vigilar 5xx y p95 durante unos minutos, continuar solo si no empeoran y volver al digest "
          "anterior en cuanto salte la alarma.", {})]], size=10, color=TEXT)
    takeaway(sl, "Cuanto menos tráfico ve una versión defectuosa, menos usuarios afecta; hacen falta métricas y un criterio de parada.",
             label="Idea guía", lab_color=CORAL)
    footer(sl, block=4)
    notes(sl, f"""
19:25–19:27. Temario: «despliegues sin downtime». El enunciado pide en el README «un plan breve de despliegue progresivo». Rolling: la de la demo (100/200 % y circuit breaker); sin balanceador. Blue/green: ECS levanta la revisión nueva junto a la actual, permite probarla (tráfico de prueba, hooks de ciclo de vida) y cambia el tráfico; mantiene la anterior durante un tiempo de espera para volver rápido. Canary: un porcentaje del tráfico a la nueva y, si va bien, el resto de una vez. Lineal: incrementos iguales con espera entre ellos. Según la documentación de ECS, el reparto lo gestiona ECS cuando el servicio usa balanceador, Service Connect o VPC Lattice.
Los diagramas son esquemáticos (no muestran tiempos reales).
Relación con la demo: B habría afectado solo al 10 % y la alarma de 5xx habría parado el canary. Todas necesitan un punto de entrada estable; la 28 muestra cómo se comprueba que el cambio no corta.
En vivo: nada; README de la demo, apartado «Despliegue progresivo».
Pregunta: «¿Qué necesitáis medir para decidir si un canary sigue adelante?».
Fuentes: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html · https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-blue-green.html · https://docs.aws.amazon.com/AmazonECS/latest/developerguide/canary-deployment.html · https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-linear.html (16/11/2026).""")
    return sl


def s20b_sin_corte(d):
    sl = d.slide(tag="sin-corte")
    header(sl, "Despliegue sin corte · cómo se demuestra", "Sin corte se mide desde el cliente, por el mismo endpoint",
           "Un balanceador (ALB) da una dirección estable delante de las tareas. B recibe tráfico solo cuando está lista y A "
           "deja de recibir peticiones nuevas, termina las que tiene y se para. Se prueba con peticiones continuas.")
    section_label(sl, 43, 134, 400, "Un endpoint estable delante de A y B", color=CORAL)
    tag(sl, 393, 132, "esquema", w=190, t="ESQUEMA · referencia con ALB")
    box(sl, 43, 151, 540, 196, fill=CARD, line=BORDER)
    node(sl, 53, 180, 112, 54, "g-users.png", "Cliente", "peticiones\ncontinuas", icon_s=26, tsize=10, ssize=8.5)
    node(sl, 183, 180, 128, 54, "r-alb.png", "ALB", "dirección DNS\nestable", icon_s=30, tsize=10, ssize=8.5)
    line(sl, 166, 207, 181, 207, color=CORAL, w=1.5)
    for (yy, lab, st, col, fill, txt_, dash) in [
            (161, "Tarea A · versión A", "draining", BLUE, BLUE_BG, "sin peticiones nuevas; termina las que tiene", True),
            (229, "Tarea B · versión B", "initial → healthy", MINT, TAKE_BG, "primer health check correcto", False)]:
        box(sl, 345, yy, 228, 58, fill=fill, line=col)
        text(sl, 355, yy + 6, 210, 13, lab, size=9.5, color=TITLE, bold=True)
        chip(sl, 355, yy + 23, 9 + len(st) * 5.2, 14, st, fill=col, color=DARK, size=7.5, radius=3)
        text(sl, 355, yy + 40, 212, 13, txt_, size=8, color=TEXT, check=False)
        line(sl, 312, 207, 343, yy + 29, color=col, w=1.5, dash=dash)
    steps = [("1", "B arranca y se registra en el grupo de destinos: estado initial, aún sin tráfico."),
             ("2", "Readiness: pasa su primer health check a /health y recibe tráfico (healthy)."),
             ("3", "A pasa a draining: ninguna petición nueva; las que tiene en curso terminan."),
             ("4", "Sin conexiones o al acabar el plazo, ECS para A (SIGTERM).")]
    for i, (n, t) in enumerate(steps):
        sx = 53 + (i % 2) * 262
        sy = 297 + (i // 2) * 24 - 2
        badge(sl, sx, sy, n, fill=CORAL, d=15, size=8)
        text(sl, sx + 21, sy - 1, 236, 24, t, size=8.5, color=TEXT)
    text(sl, 53, 283 - 6, 300, 12, "LOS CUATRO PASOS DEL CAMBIO", size=8, color=MUTED, bold=True)
    side_note(sl, 43, 357, 540, 108, "Por qué el laboratorio actual no lo demuestra",
              "En ECS/Fargate sin balanceador, el cliente llama a la IP pública de la tarea y cada tarea nueva tiene otra. "
              "El rolling 100/200 % (25) evita quedarse sin tareas, pero quien usaba la IP de A pierde la conexión. Y el "
              "smoke (26) prueba B por su IP nueva cuando el cambio ya terminó: dice que B funciona, no que nadie falló.",
              accent=CORAL, size=9.5)
    section_label(sl, 599, 134, 150, "Fallos / peticiones", color=CORAL)
    tag(sl, 745, 132, "real", w=172)
    rows = [["", "antes", "durante", "después"],
            ["Sin corte · endpoint", "0 / 102", ("0 / 36", {"color": MINT, "bold": True}), "0 / 97"],
            ["  versiones", "A", "A y B", "B"],
            ["Con corte · endpoint", "0 / 99", ("63 / 75", {"color": CORAL, "bold": True}), "0 / 96"],
            ["IP directa de A", "0 / 40", ("4 / 13", {"color": CORAL, "bold": True}), ("46 / 46", {"color": CORAL, "bold": True})],
            ["Smoke posterior a B", "", "", ("200 en ambos", {"color": AMBER, "bold": True})]]
    table(sl, 599, 151, 318, [1.55, 0.8, 0.85, 1.05], rows, size=8.5, row_h=21,
          colors={0: TITLE, 1: TEXT, 2: TEXT, 3: TEXT}, bold_cols=(0,))
    text(sl, 599, 293, 318, 26, "extras/despliegue_sin_corte.py: la API de la demo en loopback, con un balanceador "
         "mínimo. Sin AWS. Los conteos varían de una ejecución a otra.", size=8, color=MUTED)
    box(sl, 599, 325, 318, 64, fill=TAKE_BG, line=MINT)
    text(sl, 611, 331, 296, 12, "CRITERIO", size=8.5, color=MINT, bold=True)
    text(sl, 611, 345, 298, 42, "Cero respuestas fallidas (5xx o sin conexión) por el mismo endpoint antes, durante y "
         "después, mientras la versión pasa de A a B.", size=9.5, color=TITLE)
    side_note(sl, 599, 397, 318, 68, "En AWS con ALB",
              "ECS registra cada tarea en el grupo de destinos (health check a /health). Al retirar A, deregistration "
              "delay: 300 s por defecto, 5 s si las respuestas duran menos de 1 s.", accent=BLUE, size=8.5)
    takeaway(sl, "Sin corte es una medida: cero fallos por el mismo endpoint mientras cambia la versión, no un smoke verde al final.",
             label="Idea guía", lab_color=CORAL)
    footer(sl, block=4)
    notes(sl, f"""
19:27–19:30. Temario: «despliegues sin downtime». La 25 explicó el rolling del laboratorio y la 27 las estrategias; aquí, cómo se DEMUESTRA que no hay corte. Referencia: un Application Load Balancer delante del servicio. En este recorrido, A sigue sana mientras B se registra. B pasa de initial a healthy cuando supera su primer health check. El umbral de éxitos consecutivos se aplica al recuperar un destino unhealthy. El balanceador local de la demo usa su propio umbral de dos éxitos. Al retirar uno, pasa a draining: el balanceador deja de enviarle peticiones nuevas y espera a que terminen las que están en curso, hasta el deregistration delay (300 s por defecto, de 0 a 3.600). ECS espera a que el destino quede sin uso y entonces manda SIGTERM a la tarea (y SIGKILL si no termina). Para respuestas de menos de un segundo, AWS sugiere bajar el plazo a 5 s.
Criterio: peticiones continuas por el MISMO endpoint antes, durante y después del cambio; cero respuestas 5xx o sin conexión, y las respuestas pasan de versión A a A y B a B.
Resultado real del ensayo local (17/11/2026): extras/despliegue_sin_corte.py arranca la API de la demo dos veces (A y B) en 127.0.0.1 y un balanceador mínimo con readiness y drenaje. Sin corte: 0 fallos en 235 peticiones; con corte (parar A y luego arrancar B): 63 de 75 fallan durante el cambio (502/503); un cliente que apuntaba a la «IP» de A falla al pararse A; y el smoke posterior sale 200 en los dos casos. Tres ejecuciones: siempre 0 fallos sin corte y 60–64 con corte (.build/s18/logs/despliegue-sin-corte.txt).
El laboratorio de ECS/Fargate no tiene balanceador (IP pública temporal, regla /32): no puede demostrar continuidad y no se amplía para ello; el ALB cuesta por hora y por uso. El esquema de la izquierda es de referencia, no un ensayo en AWS.
En vivo: uv run python extras/despliegue_sin_corte.py (unos 7 segundos).
Pregunta: «¿Qué pasaría con las peticiones en curso si A se parara sin drenaje?».
Fuentes: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html (deregistration delay) · https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html (initial, healthy, draining) · https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-connection-draining.html · https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-healthcheck.html (consultadas con Context7 y en la web de AWS el 17/11/2026; copias en .build/s18/investigacion/ctx7-alb-*.txt y aws-ecs-connection-draining.txt); demo-cicd/extras/despliegue_sin_corte.py. {SRC_AWS}""")
    return sl


def s21_demo_b(d):
    sl = d.slide(tag="demo-b")
    header(sl, "Demo 3 · desplegar la versión B", "B pasa los tests, se publica y se despliega",
           "cambios/02 añade el plazo de atención (sla_horas) a cada respuesta, con su test. La PR queda en verde, main "
           "publica el digest de B y lo desplegamos en staging.")
    section_label(sl, 43, 134, 430, "El cambio · versión B", color=VIOLET)
    box(sl, 43, 151, 430, 178, fill=CARD, line=BORDER, radius=4)
    diff = [("+SLA_HORAS = {\"alta\": 4, \"media\": 24}", MINT), ("", TEXT),
            ("  return {", TEXT), ('      "resultado": resultado.model_dump(),', TEXT),
            ('+     "sla_horas": SLA_HORAS[resultado.prioridad],', MINT), ("  }", TEXT), ("", TEXT),
            ("+def test_la_respuesta_incluye_el_plazo_…():", MINT),
            ('+    datos = cliente.post("/clasificar", …).json()', MINT),
            ('+    assert datos["sla_horas"] == 24', MINT)]
    text(sl, 55, 160, 410, 165, [[(t, {"color": c})] for t, c in diff], size=8.5, font=MONO, check=False, lsp=Pt(15.2))
    section_label(sl, 487, 134, 250, "Resumen del despliegue", color=VIOLET)
    tag(sl, 745, 132, "ilustrativo", w=172)
    rows = [["", "Antes", "Después"],
            ["Digest", "sha256:7d1e40aa…", ("sha256:c41b9e07…", {"color": AMBER, "bold": True})],
            ["Definición de tarea", "s18-tu-nombre:4", "s18-tu-nombre:5"],
            ["Commit", "3f9c2e1d…", "a8b0d4c2…"],
            ["Smoke", "", ("correcto", {"color": MINT, "bold": True})]]
    table(sl, 487, 151, 430, [0.9, 1.1, 1.1], rows, size=9, row_h=24, font_cols={1: MONO, 2: MONO},
          colors={1: MINT_L, 2: MINT_L}, bold_cols=(0,))
    text(sl, 487, 278, 430, 50, [[("Para volver atrás: ", {"bold": True, "color": TITLE}),
         ("lanza este workflow con el digest de «Antes» y motivo «rollback». Lo escribe el propio resumen.", {})]],
         size=9.5, color=TEXT)
    section_label(sl, 43, 341, 874, "El comando", color=VIOLET)
    code_panel(sl, 43, 358, 874, 34, [
        'gh workflow run desplegar-staging.yml --ref main -f "digest=$DIGEST_B" -f motivo=despliegue'], size=9.5)
    box(sl, 43, 402, 874, 63, fill=CARD)
    text(sl, 54.5, 409, 600, 12.2, "ENSAYO LOCAL DEL 17/11/2026 · QUÉ ESTÁ COMPROBADO", size=8.5, color=BLUE, bold=True)
    text(sl, 54.5, 425, 851, 38, [[("Comprobado: ", {"bold": True, "color": TITLE}),
         ("tests de B 24 passed; imagen B construida y smoke correcto con versión B. ", {}),
         ("Pendiente: ", {"bold": True, "color": AMBER}),
         ("publicación en ECR y despliegue en ECS (ensayo en GitHub y AWS por autorizar).", {})]], size=9.5, color=TEXT)
    takeaway(sl, "Todo está en verde: tests, imagen, publicación, despliegue y smoke. Aun así, B tiene un fallo que nadie ha probado.",
             label="Idea guía", lab_color=VIOLET)
    footer(sl, block=4)
    notes(sl, """
19:30–19:34. Tercer momento de demo y preparación del bloque siguiente. cambios/02-version-b.patch añade SLA_HORAS y el campo sla_horas en la respuesta, y un test que comprueba 24 h para prioridad media. Está en verde (24 passed). El diccionario no tiene «baja»: es una regresión controlada que los tests de B no cubren (requisito del plan: «B tendrá una regresión docente controlada y observable…»). No lo reveléis todavía.
Recorrido GitHub: PR → checks verdes → merge → Publicar · main deja el digest de B → gh workflow run desplegar-staging.yml --ref main -f digest=$DIGEST_B -f motivo=despliegue → resumen Antes/Después. Lanzarlo y, mientras corre (unos minutos), enseñar una ejecución anterior. Los valores del resumen son ilustrativos.
Comprobar la regla del environment: lanzar el mismo workflow con --ref otra-rama debe fallar sin credenciales (comandos.md).
Local: docker run de s18:B y smoke (real, 17/11).
Pregunta: «Con todo en verde, ¿qué no hemos comprobado?».
Fuentes: demo-cicd/cambios/02-version-b.patch; .build/s18/logs/gen_cambios.json y ensayo-comandos.txt (17/11/2026).""")
    return sl
