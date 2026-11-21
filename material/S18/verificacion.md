# Verificación de S18

Comprobaciones ejecutadas de verdad el 16–17/11/2026 en el Mac del profesor (uv 0.13.7, Docker
29.9.3), sin cuentas de GitHub ni de AWS. Registros en `4-produccion-ia/.build/s18/logs/`.

## Demo (`demo-cicd/`)

| Comprobación | Comando | Resultado |
|---|---|---|
| Dependencias bloqueadas | `uv sync --locked` | Correcto (33 paquetes resueltos) |
| Lock de Docker igual al de uv | `uv export --locked --no-dev … \| diff requirements.lock -` | Sin diferencias |
| Análisis | `uv run ruff check .` · `uv run ruff format --check .` | Correctos |
| Tests | `uv run pytest -q` | **23 passed** (aviso de deprecación de Starlette, no es un fallo) |
| Plantillas | `uv run cfn-lint infra/*.yaml` (también `--regions eu-north-1`) | Sin errores ni avisos; JSON del panel válido |
| Workflows | `actionlint` 1.7.12 en Docker sobre una copia con Git | 0 errores (shellcheck incluido) |
| Scripts | `shellcheck scripts/*.sh` | Correcto |
| SHA de las acciones | `gh api repos/<acción>/git/ref/tags/<versión>` | 4/4 coinciden con los workflows (`acciones-sha.txt`) |
| Build Docker | `docker build --platform linux/amd64 --provenance=false` (16/11) y builds locales (17/11) | Correcto (`docker-build-amd64.log`) |
| Parches de la demo | `.build/s18/gen_cambios.py` | A 23 passed; 01: **2 failed**; 02: 24 passed y **500** con prioridad baja; 03 solo test: 1 failed; 03 completo: **27 passed** (`gen_cambios.json`) |
| Recorrido A → B → A | `.build/s18/ensayo_local.sh` | A smoke ✓; B smoke ✓ y consulta baja → 500 con `KeyError` en el log; A otra vez (misma imagen) smoke ✓ y → 200 (`ensayo-local.txt`) |
| Comandos de clase | todos los bloques «Local» de `docs/comandos.md` en una copia | Todos con el resultado indicado (`ensayo-comandos.txt`) |
| Migración y restauración | `uv run python extras/migracion_y_restauracion.py` | CORRECTO (`extras-migracion.txt`) |

Las imágenes del ensayo local usan versiones ficticias (`aaaa…`, `bbbb…`, `version-A`, `version-B`);
los digests de las diapositivas que no proceden de ese ensayo están rotulados como ilustrativos.

## Presentación

| Comprobación | Resultado |
|---|---|
| Archivo | `presentaciones/S18-cicd-monitorizacion.pptx`, 31 diapositivas, 960 × 540 pt; SHA-256 `8ca88822…0076c` |
| PDF | `presentaciones/S18-cicd-monitorizacion.pdf`, 31 páginas (LibreOffice); SHA-256 `231f620f…199da` |
| `check.py` | 0 incidencias: nada fuera del lienzo; 31 notas con franja horaria, pregunta (salvo la del QR) y fuentes; QR vigente 1 (idéntico al de S16), QR antiguo 0, logotipo 2; 9 tablas nativas; fuentes Arial, Georgia y Courier New |
| Revisión visual | Las 31 diapositivas renderizadas (80 ppp) y revisadas; se corrigieron solapes en 1, 6, 13, 15, 17, 23 y 25. Comparadas con los renders del ejemplo final de S17 (`.build/s18/ejemplo-final/`): misma paleta, tipografías, cabeceras, bandas y pies |
| Texto | Editable; ninguna imagen de texto. Los ✓ y ✗ se sustituyen en el PDF por una fuente de respaldo |

## Pendiente (requiere autorización de José)

1. Publicar el repositorio de la demo en GitHub (público), environment `staging` solo `main` y ruleset.
2. Crear `infra/01` y `infra/02` en eu-north-1 con el perfil del aula; leer el `sub` real con `Diagnóstico · OIDC`.
3. Ensayo: PR roja bloqueada, publicación de A y B, despliegue de B, dispatch desde otra rama rechazado,
   error localizado en CloudWatch, panel y alarma, rollback a A y retirada (README de la demo, pasos 4–9).
4. Coste: no estimado con tarifas actuales de eu-north-1 (una tarea Fargate de 0,25 vCPU/0,5 GB, logs
   y métricas personalizadas); revisar antes del ensayo.
5. Enviar el PPTX/PDF a la escuela para la plataforma.

No se ha hecho commit ni push, no se ha creado ningún repositorio ni recurso en AWS y no se ha
consumido ninguna API de pago.

## Ampliación del 17/11/2026: diapositivas 8, 14 y 15

Petición de José: una diapositiva que explique a fondo qué es una GitHub Action y otra con alternativas
(Cloudflare Workers Builds, VPS propio…) comparando precios, ventajas e inconvenientes, con logotipos.

| Comprobación | Resultado |
|---|---|
| Generación | `build.py` → 34 diapositivas, sin avisos de desborde |
| `check.py` | 0 incidencias; QR vigente 1, antiguo 0; logotipo 2; 10 tablas nativas; solo Arial, Georgia y Courier New |
| Render | PDF de 34 páginas (LibreOffice), SHA-256 `0dd1ad3b…`; 8, 14 y 15 revisadas a 150 ppp y 7–18 en hoja de contactos; corregidos el color del logotipo de Hetzner, rótulos partidos y la altura de la cabecera de la tabla |
| `action.yml` citado | Extracto real de `aws-actions/configure-aws-credentials` en `e1253824…` (etiqueta v6.3.0), leído con `gh api` |
| Precios | Páginas oficiales de GitHub, Cloudflare, GitLab, AWS CodeBuild y Hetzner leídas el 17/11/2026 con Firecrawl; copias en `.build/s18/investigacion/` |
| Horario | Bloque 2 pasa a 18:44–19:05 (21 min); bloques 1 y cierre se acortan (9 y 7 min); notas, guion y comandos renumerados |

Sin verificar: el ejemplo de coste de la diapositiva 15 es un cálculo ilustrativo (rotulado), no una factura; CodePipeline y el IVA no están incluidos.

## Ampliación del 17/11/2026 (noche): diapositivas 27, 29 y 33

Petición de José: ampliar APM, error tracking y despliegue sin corte, muy visual y con el diseño existente.
Nuevas: 27 APM (cascada de spans, `trace_id` frente a `request_id`), 29 error tracking (eventos → huella →
incidencia con el `KeyError: 'baja'` de B) y 33 cómo se demuestra un despliegue sin corte (ALB, readiness,
drenaje, peticiones continuas). El resto conserva orden, diseño y notas; las antiguas 27–34 pasan a 28, 30–32 y 34–37.

| Comprobación | Resultado |
|---|---|
| Generación | `build.py` → 37 diapositivas, sin avisos de desborde |
| `check.py` | 0 incidencias; QR vigente 1, antiguo 0; logotipo 2; 11 tablas nativas; solo Arial, Georgia y Courier New |
| Render | PDF de 37 páginas, 960 × 540 pt (LibreOffice); PPTX SHA-256 `9ea5d448…`, PDF `11da3e5d…`; 27, 29 y 33 y sus vecinas (25, 26, 28, 30, 32, 34) revisadas; corregidos solapes de la cascada, de la tabla del ensayo y del rótulo de sección |
| Horario | Franjas de las notas continuas de 18:30 a 20:00; 8 min para las nuevas: −1 min en 10, 17, 21, 22, 25, 32, 34 y 37 |
| `extras/despliegue_sin_corte.py` | 3 ejecuciones (`uv run --locked`): sin corte 0 fallos; con corte 60–64; «IP» directa de A falla; smoke posterior 200 en ambos (`.build/s18/logs/despliegue-sin-corte.txt`) |
| Demo | `ruff check`, `ruff format --check` y `pytest` (23 passed) correctos; `app.py`, plantillas y workflows sin cambios |

Valores ilustrativos rotulados: tiempos de la cascada (27) y contadores, request_id adicionales y gráfico de la incidencia (29).
Sin verificar en AWS: no hay ALB en el laboratorio y no se ha creado; la diapositiva 33 lo trata como referencia.

Revisión final: actualizado el criterio de salud inicial del ALB y aclarada la captura explícita en Sentry.
Ensayo local independiente: 0 fallos de 235 peticiones en el cambio sin corte, 66 fallos de 75 durante el corte deliberado
y HTTP 200 en ambos smoke posteriores.

## Ampliación del 20/11/2026: punto de partida (diapositivas 3–5)

Petición de José: diapositivas al principio que expliquen qué es CI/CD y la monitorización, con casos de uso, muy visuales.

| Comprobación | Resultado |
|---|---|
| Generación | `build.py` → 40 diapositivas; un aviso de posible desborde en la 3 descartado al ver el render (la línea cabe) |
| `check.py` | 0 incidencias; QR vigente 1, antiguo 0; logotipo 2; 11 tablas nativas; solo Arial, Georgia y Courier New |
| Render | PDF de 40 páginas (LibreOffice), SHA-256 `da0f06cc…`; 3, 4 y 5 revisadas a 150 ppp y 1–12 en hoja de contactos |
| Fuentes | Señales doradas (Google SRE) y cinco métricas DORA leídas el 20/11/2026 con Firecrawl; copias en `.build/s18/investigacion/` |
| Horario | Notas con 40 franjas contiguas de 18:30 a 20:00; desde la 3, todas las referencias a diapositivas suben tres números en notas, guion, comandos, cobertura, fuentes y README de la presentación |

Las secciones anteriores de este archivo conservan la numeración que tenían cuando se escribieron. El panel de la diapositiva 4 usa valores ilustrativos, rotulados.

## Revisión completa del 20/11/2026

Se leyeron las 40 diapositivas (texto y notas), se comprobó con un script cada referencia «diapositiva N», «la N» o «(N)»
frente al título real de destino, el bloque activo de cada pie y la continuidad de los horarios, y se revisó el render de cada
diapositiva. Cambios aplicados:

| Cambio | Diapositivas |
|---|---|
| Referencias que habían quedado desfasadas: «Enlace con el log», «El rolling… y el smoke», nota de la 28 y nota de la 4 | 32, 28, 4 |
| Plan de la sesión con hora de inicio de cada parte, qué sesión se valora y cómo trabajamos | 2 |
| «Del commit a staging: qué automatiza la demo y qué no»: ya no repite las definiciones de la 3; tarjetas con el workflow y el disparador de cada tramo | 7 |
| Progresivos y «sin corte, cómo se demuestra» pasan del bloque 6 al 4, detrás de la verificación; la 25 se rotula «Rolling update · sin corte» | 27, 28, 25 |
| El cierre incluye la monitorización: «Un panel y una alarma avisan antes que el usuario…» | 40 |
| Versión B ilustrativa unificada (a8b0d4c) y aclaración de la versión ficticia del ensayo local | 34, 33 |
| Antetítulo en español («Diseño del sistema») y «✓» que quedaba suelto en la franja de resultados | 9, 13 |
| Letra más grande en las diapositivas densas, con textos más cortos donde hacía falta | 7, 17, 18, 34, 35 |
| Cabeceras de módulo con el rango real de diapositivas (estaban desplazadas dos veces) | `deck_part1–3.py` |

| Comprobación | Resultado |
|---|---|
| `check.py` | 0 incidencias; 40 diapositivas, 11 tablas nativas, QR vigente 1, antiguo 0, logotipo 2; solo Arial, Georgia y Courier New |
| Referencias cruzadas | Todas apuntan a la diapositiva correcta |
| Pies y horarios | Bloques en orden 1→7; 40 franjas seguidas de 18:30 a 20:00 |
| Render | PDF de 40 páginas, SHA-256 `2531a9e3…`; diapositivas cambiadas revisadas a 80–150 ppp |

Documentos actualizados con la nueva numeración: `demo-cicd/docs/guion-clase.md` (bloques 4–6), `demo-cicd/docs/comandos.md`
(la sección «sin corte» pasa delante de la demo de B), `cobertura.md`, `fuentes.md` y `fuentes/presentacion/README.md`.
