# Fuente editable de la presentación de S18

Genera `material/S18/presentaciones/S18-cicd-monitorizacion.pptx` (40 diapositivas, 960 × 540 pt,
texto y tablas editables, notas del orador en todas). El PDF de la misma carpeta se exportó con
LibreOffice desde ese PPTX.

## Diseño

Reproduce la presentación **final de S17** (`S17-serverless-ai.pptx`, 30 diapositivas) que pasó
José el 17/11/2026; manda sobre cualquier otro modelo. `deck_lib.py` es una copia adaptada de
`material/S17/fuentes/rediseno-visual/deck_lib.py` (que no se ha modificado):

- Paleta, tipografías (Georgia, Arial, Courier New), cabecera, banda «IDEA GUÍA» y pie con
  navegación numerada por bloques, con las medidas del ejemplo.
- Colores de bloque en el orden del ejemplo final (bloque 2 ámbar, bloque 3 rosa…).
- Diapositivas «simples» del ejemplo (encuesta, caso conductor, práctica) con su cabecera, banda
  y pie plano propios (`header_simple`, `band_simple`, `footer_simple`, `rows_simple`).
- Rótulos de procedencia: «RESULTADO REAL · ensayo local», «VALORES ILUSTRATIVOS», «ESQUEMA ·
  no es una captura», «PENDIENTE DE ENSAYO EN GITHUB Y AWS».

## Construir y comprobar

```bash
cd material/S18/fuentes/presentacion
uv run --no-project --with python-pptx --with pillow --with lxml python build.py ../../presentaciones/S18-cicd-monitorizacion.pptx
uv run --no-project --with python-pptx python check.py ../../presentaciones/S18-cicd-monitorizacion.pptx
```

`check.py` comprueba límites del lienzo, notas (franja horaria, pregunta y fuentes), QR vigente
(idéntico a `material/S16/assets/qr-ai-engineer.jpg`, ninguno antiguo), logotipo y tablas nativas.
Render a PDF/PNG: `.build/s18/render.sh` (LibreOffice y pdftoppm del runtime local).

| Archivo | Contenido |
|---|---|
| `deck_part1.py` | 1–18: portada, encuesta, qué es CI/CD, qué es monitorizar y casos de uso (3–5), caso conductor, CI/CD y entornos, GitHub Actions, qué es una action (11) y alternativas con precios (17–18) |
| `deck_part2.py` | 19–29: artefacto inmutable, secretos, OIDC, despliegue a staging, rolling, progresivos (27) y despliegue sin corte (28) |
| `deck_part3.py` | 30–40: observabilidad, logging, APM (32), error y error tracking (33–34), métricas y alarma (35), rollback (36), migraciones, backups, práctica y cierre |

## Procedencia de las imágenes

| Imagen | Origen |
|---|---|
| `aws-ecr`, `aws-secrets`, `aws-cloudformation`, `aws-backup`, `aws-rds`, `r-ecr-image`, `r-cw-alarm`, `r-cw-logs`, `r-ecs-task`, `r-ecs-service`, `r-rds-bluegreen`, `g-git`, `g-source-code`, `g-database`, `g-users`, `g-client`, `g-disk` | AWS Architecture Icons, paquete oficial del 31/07/2026, descargado el 17/11/2026 de aws.amazon.com/architecture/icons (zip sha256 `d2d166c4…dc6526`); SVG convertidos a PNG con PyMuPDF (`.build/s18/iconos/svg2png.py`) sin modificar el dibujo |
| `aws-ecs`, `aws-fargate`, `aws-cloudwatch`, `aws-iam`, `aws-console`, `r-iam-*`, `g-alert`, `g-logs`, `g-metrics`, `g-json-script`, `g-padlock`, `g-shield`, `g-user`, `g-magnifier`, `g-gear`, `g-document`, `g-credentials`, `g-servers`, `g-globe`, `aws-logo-dark` | Copiados de `material/S17/fuentes/rediseno-visual/assets/` (mismo paquete oficial de AWS; logotipo de aws.amazon.com) |
| `az-appinsights`, `az-monitor`, `gc-logging`, `gc-monitoring` | Copiados de S17: Azure Public Service Icons V25 e iconos oficiales de Google Cloud |
| `docker-mark-white` | Copiado de S17: logotipo oficial de Docker |
| `gh-actions`, `gh-fastapi`, `gh-opentelemetry`, `gh-python` | Repositorio oficial `github/explore` (temas), leído con `gh api` el 17/11/2026 |
| `github-mark-white` | Octicon `mark-github-24.svg` del repositorio oficial `primer/octicons`, rellenado en blanco para fondo oscuro |
| `pytest` | `doc/en/img/pytest_logo_curves.svg` del repositorio oficial `pytest-dev/pytest` (no usado en la versión final) |
| `thepower-logo` y QR | Recursos del curso: `material/S18/assets/` (copias idénticas de los de S16/S17; el QR es el vigente de S16) |

Los gráficos del panel, las líneas de tiempo, los diagramas de flujo y de secuencia están
dibujados con formas nativas. No hay capturas de pantalla: el formulario de GitHub y el panel de
CloudWatch son esquemas rotulados como tales.

### Añadidas el 17/11/2026 (hoy diapositivas 11, 17 y 18)

| Archivo en `assets/` | Procedencia |
|---|---|
| `gh-gitlab.png`, `gh-cloudflare.png` | github/explore, `topics/<nombre>/<nombre>.png` (repositorio oficial de GitHub), descargados el 17/11/2026 |
| `hetzner-logo.png` | `https://www.hetzner.com/_resources/themes/hetzner/images/logo/hetzner-logo.svg`, convertido a PNG con PyMuPDF y recoloreado al rojo del propio SVG (#D50C2D) |
| `aws-codebuild.png` | AWS Architecture Icons 31/07/2026, `Arch_AWS-CodeBuild_48.svg`, convertido con `.build/s18/iconos/svg2png.py` |

Precios de las diapositivas 17–18: páginas oficiales de GitHub, Cloudflare, GitLab, AWS y Hetzner
consultadas el 17/11/2026; copias en `.build/s18/investigacion/` (`gh-billing.md`, `gh-runner-pricing.md`,
`cf-builds-pricing.md`, `cf-workers-pricing.md`, `gitlab-pricing.md`, `aws-codebuild-pricing.md`, `hetzner-cloud.md`).

### Añadidas el 17/11/2026 (hoy diapositivas 32, 34 y 28)

Funciones `s23a_apm` y `s24a_error_tracking` de `deck_part3.py`, y `s20b_sin_corte` de `deck_part2.py` (antes `s27a_sin_corte`; el sufijo de letra las
ordena tras la diapositiva que amplían). Formas nativas; nada de capturas: la incidencia de la 34 es un
esquema rotulado sin logotipo de Sentry.

| Archivo en `assets/` | Procedencia |
|---|---|
| `r-alb.png` | AWS Architecture Icons 31/07/2026, `Res_Elastic-Load-Balancing_Application-Load-Balancer_48.svg`, convertido con `.build/s18/iconos/svg2png.py` |
