# S18 · Guion de la clase (90 minutos)

**Miércoles 25/11/2026 · grupo L/X · 18:30–20:00 (hora de Madrid).**
Presentación: `material/S18/presentaciones/S18-cicd-monitorizacion.pptx` (40 diapositivas).
Comandos exactos, en el mismo orden: [comandos.md](comandos.md).

La teoría y la demo se alternan: cada bloque termina en algo que se ve en pantalla y en una
pregunta para el grupo. La práctica posterior es **opcional** (aclaración de Laura del 04/11).

## Antes de conectar

- Terminal con letra grande en `demo-cicd/` (o en tu copia `~/thepower-cicd`), `uv sync --locked` hecho.
- Docker arrancado y las dos imágenes del ensayo local construidas (comandos.md, paso 0).
- **Si el ensayo real en GitHub y AWS está hecho y autorizado:** pestañas abiertas con el
  repositorio, la PR roja ya ejecutada, la ejecución de `Publicar · main` con el digest de A y B,
  el despliegue de B, el panel de CloudWatch y Logs Insights. Ejecuciones largas (publicar,
  desplegar) **ya terminadas**: en directo se lanzan, y mientras corren se enseña la anterior.
- **Si no lo está:** todo el recorrido tiene una versión local real (pytest, Docker, logs) y las
  diapositivas rotulan como «ilustrativo» lo que no se ha ejecutado. No se presenta como hecho.
- Nada de credenciales, claves, IDs de proyecto ni el archivo `.env` en pantalla.

## Recorrido

| Hora | Min | Diapositivas | Qué se enseña en diapositiva | Qué se hace en vivo |
|---|---:|---|---|---|
| 18:30–18:33 | 3 | 1–2 | Objetivo; QR de **S17 (23/11)** | Responder al QR un minuto |
| 18:33–18:39 | 6 | 3–5 | **Punto de partida:** qué es CI/CD (bucle código → construir → probar → publicar → desplegar → monitorizar; sin y con CI/CD); qué es monitorizar (cuatro señales doradas, señales propias de IA, ciclo de un incidente); seis casos de uso y las cinco métricas DORA | Preguntar cómo publican hoy y cuál de los seis casos les ha pasado |
| 18:39–18:45 | 6 | 6–9 | Caso conductor: la API de S16 con garantías; CI, entrega continua y despliegue continuo; entornos y configuración; la cadena commit → digest → servicio | Abrir el repositorio: `app.py`, `.github/workflows/`, `infra/` |
| 18:45–19:05 | 20 | 10–18 | Anatomía de un workflow; **qué es una action** (action.yml, tipos, runners); los cinco workflows; comprobaciones de la PR; tests con dobles; ramas protegidas y acciones por SHA; **alternativas** (Cloudflare Workers Builds, GitLab, CodeBuild, VPS propio) con precios | **PR con fallo**: aplicar `cambios/01`, ver dos tests rojos y la PR bloqueada |
| 19:05–19:17 | 12 | 19–23 | Construir una vez; etiqueta frente a digest; variables y secretos; OIDC; `sub` y `aud` | Leer el `sub` real (`Diagnóstico · OIDC`); **publicar** y anotar el digest |
| 19:17–19:34 | 17 | 24–29 | Despliegue por digest sin reconstruir; rolling sin corte y circuit breaker; smoke contra la API real; despliegue progresivo (rolling, blue/green, canary, lineal); **cómo se demuestra un despliegue sin corte** (endpoint estable, readiness, drenaje, peticiones continuas) | `extras/despliegue_sin_corte.py` (7 s); **desplegar B** a staging y leer el resumen Antes/Después |
| 19:34–19:50 | 16 | 30–36 | Logging y monitoring; log estructurado; **APM** (cascada de spans, cuello de botella en el proveedor, `trace_id` frente a `request_id`); **error tracking** (eventos agrupados por huella en una incidencia con frecuencia, usuarios y release); métricas, panel y alarma | **Error de B** → `request_id` → causa en el log; panel; **rollback a A** |
| 19:50–19:54 | 4 | 37–38 | Migraciones expand/contract; backups, RPO/RTO y restauración | `extras/migracion_y_restauracion.py` (30 s) |
| 19:54–20:00 | 6 | 39–40 | Práctica opcional, evidencias que se piden y cierre | Preguntas; recordar el QR |

**Redistribución del 17/11/2026** (tres diapositivas nuevas: 27 APM, 29 error tracking, 33 despliegue
sin corte, 8 minutos): se recorta un minuto a 10 (comprobaciones de la PR), 17 (secretos), 21
(desplegar), 22 (rolling), 25 (mapa de observabilidad), 32 (progresivos), 34 (migraciones) y 37
(cierre). La franja exacta de cada diapositiva está al principio de sus notas.

**Redistribución del 20/11/2026** (tres diapositivas de punto de partida al principio: 3 qué es CI/CD, 4 qué es
monitorizar, 5 casos de uso; 6 minutos): se recorta un minuto al caso conductor (6), dos a «tres automatizaciones»
(7, que ahora repasa lo visto en la 3), uno a entornos (8), uno a la cadena (9) y uno a la demo de desplegar B (27).
Desde la 3, todas las diapositivas citadas antes del 20/11 suben tres números.

**Revisión del 20/11/2026.** Progresivos y «sin corte, cómo se demuestra» pasan del bloque 6 al bloque 4, detrás de la
verificación (ahora 27 y 28). Van antes de desplegar B (29), que debe seguir justo antes del bloque 5 porque el fallo de B
se investiga en la demo 4. Observabilidad y rollback pasan a 30–36 (19:34–19:50); el bloque 6 queda en migraciones y
backups (37–38). No cambia la duración de ninguna diapositiva; la 7 ahora sitúa CI y CD en los workflows de la demo.

## Bloque a bloque

### 18:30 · Apertura (diapositivas 1–2)

- El objetivo no es «tener un pipeline», sino **poder demostrar** tres cosas: un cambio
  defectuoso no llega a desplegarse, lo desplegado es exactamente lo que se probó y se puede
  volver a una versión conocida.
- QR: evalúa la **S17 del 23/11** (Bedrock + Lambda). Un minuto para rellenarlo; Laura insiste
  en que las respuestas son importantes.
- El grupo L/X tuvo la S16 con otro profesor: la demo trae su propia API (la misma tarea de
  clasificación de incidencias ficticias), no hace falta haber hecho la de José.
- **Pregunta:** «¿Qué tendría que pasar para que os fiarais de desplegar un viernes a las 19:00?».

### 18:33 · Punto de partida · qué es CI/CD y qué es monitorizar (3–5)

- **3 · Qué es CI/CD.** Bucle infinito: a la izquierda CI (código, construir, probar), a la derecha CD
  (publicar, desplegar) y la monitorización cerrando el círculo. Columna «sin CI/CD» frente a «con CI/CD»:
  cada línea de «con» es una parte de la clase.
- **4 · Qué es monitorizar.** Panel ilustrativo con las cuatro señales doradas (latencia, tráfico, errores,
  saturación); señales propias de una app de IA (tokens, coste, latencia del modelo, calidad → S19); ciclo de
  un incidente: detectar → avisar → diagnosticar → recuperar → aprender, que es lo que se hará en el bloque 5.
- **5 · Casos de uso.** Seis situaciones típicas con «sin» y «con» (un cambio rompe la API, cambiar de modelo,
  error de madrugada, volver atrás, factura de tokens, publicar a menudo) y las cinco métricas DORA.
- **Preguntas:** «¿A cuál de las dos columnas se parece cómo publicáis hoy?» y «¿Cuál de los seis casos os ha pasado?».

### 18:39 · Caso conductor y bloque 1 · CI/CD y entornos (6–9)

- CI = integrar a menudo y comprobar cada cambio automáticamente. CD tiene dos lecturas:
  *entrega continua* (siempre hay un artefacto listo; desplegar es una decisión) y *despliegue
  continuo* (se despliega solo). La demo hace **entrega continua**: a staging se despliega a mano.
- Entornos: local, CI, staging, producción. La **misma imagen** en todos; cambia la configuración.
- La cadena que conecta todo: commit → comprobaciones → imagen → **digest** → definición de tarea →
  tarea → cada petición lleva `version` = commit. Con ella se responde «¿qué código atendió esta
  petición?».
- **En vivo:** recorrer el repositorio (un archivo de app, 23 tests, 5 workflows cortos, 2 plantillas).
- **Pregunta:** «Si mañana falla una petición, ¿qué dato necesitáis para saber qué versión la atendió?».

### 18:45 · Bloque 2 · GitHub Actions (10–18)

- Workflow, evento, job, step, runner, action, `permissions`. Un job no tiene más permisos de
  los que declara.
- **Qué es una action (11):** un paso reutilizable que vive en su propio repositorio y se describe
  con `action.yml`: `inputs`, `outputs` y `runs`. Extracto real de
  `aws-actions/configure-aws-credentials` v6.3.0 (el SHA que usa la demo). Tres tipos: JavaScript,
  contenedor y compuesta. Runner de GitHub (máquina limpia, por minuto) frente a runner propio.
- Los cinco workflows y quién puede pedir credenciales (solo `publicar-main` y `desplegar-staging`).
- `comprobaciones.yml`: `uv sync --locked`, comparar `requirements.lock`, ruff, cfn-lint, pytest,
  `docker build` y smoke del contenedor. Lo llaman la PR y `main`: una sola definición de «validado».
- Tests: el proveedor de IA se sustituye por un doble. Tres casos del enunciado: entrada
  inválida (422), respuesta válida y fallo del proveedor (504 sin inventar respuesta).
- **Demo · PR con fallo.** `cambios/01` «mejora» la API devolviendo una respuesta por defecto
  cuando el proveedor falla. Parece razonable; dos tests lo detectan. La PR no se puede integrar
  (regla de rama) y no recibió credenciales. Si no hay GitHub ensayado, se ve igual en local con
  `uv run pytest`.
- Acciones fijadas al SHA de 40 caracteres: un tag se puede mover; un SHA no.
- **Alternativas (17–18):** Cloudflare Workers Builds (sin YAML, solo despliega en Cloudflare),
  GitLab CI/CD, AWS CodeBuild + CodePipeline y un VPS propio (runner self-hosted, Jenkins o
  Coolify). Tabla de precios oficiales consultados el 17/11/2026 y ejemplo ilustrativo de coste
  para 5.000 min/mes. Mensaje: cambia quién mantiene la máquina; las garantías de la clase no.
- **Pregunta:** «¿Por qué el fallo lo detecta un test y no el build de Docker?».
- **Pregunta (alternativas):** «¿Por qué el VPS, que parece el más barato, no es siempre la mejor opción?».

### 19:05 · Bloque 3 · Artefacto, secretos y OIDC (19–23)

- Construir **una vez**. Una etiqueta es un nombre que puede apuntar a otra imagen; el digest es
  la huella del contenido. ECR con etiquetas inmutables: el commit no se puede reutilizar.
- Dónde vive cada dato: `.env` local (fuera de Git), variables de GitHub (no secretas), Secrets
  Manager (la clave del modelo, que ECS inyecta al arrancar). En la imagen, nada secreto.
- OIDC: GitHub firma un token para ese job; AWS STS lo cambia por credenciales de una hora si
  la confianza del rol lo permite. No hay claves de AWS guardadas en GitHub.
- `aud = sts.amazonaws.com` y `sub` exacto. Con `environment: staging` el `sub` termina en
  `:environment:staging`, no en `:ref:refs/heads/main`. Los repositorios creados desde el
  15/07/2026 incluyen además los identificadores del propietario y del repositorio.
- **Demo:** `Diagnóstico · OIDC` muestra el `sub` real; `Publicar · main` deja el digest en el resumen.
- **Pregunta:** «¿Qué ocurre si la confianza usa `repo:ORG/*`?».

### 19:17 · Bloque 4 · Despliegue a staging (24–29)

- `desplegar-staging.yml`: el digest entra como dato; se comprueba que existe y tiene etiqueta
  de commit; se registra una definición de tarea igual salvo la imagen; ECS sustituye la tarea.
- Rolling sin corte (100 % mínimo, 200 % máximo) y *circuit breaker* con rollback automático si
  la tarea nueva no arranca. Por eso el workflow comprueba **qué quedó en marcha**.
- Un job verde no basta: smoke contra la API real con la versión esperada. El puerto se abre
  solo a la IP del runner y se cierra al terminar.
- **Progresivos (27):** rolling, blue/green, canary, lineal. Las tres últimas necesitan repartir tráfico
  (balanceador o Service Connect); la demo no lo tiene.
- **Sin corte, cómo se demuestra (28):** ALB como endpoint estable; B entra en el reparto tras
  pasar `/health` (readiness); A pasa a *draining* y termina sus peticiones antes de pararse.
  Criterio: cero fallos por el mismo endpoint antes, durante y después. En vivo,
  `uv run python extras/despliegue_sin_corte.py`: sin corte 0 fallos; parar y arrancar ≈60 fallos;
  la «IP» directa de A falla y el smoke posterior sale bien en los dos casos. La IP directa y el
  smoke del laboratorio ECS/Fargate actual no demuestran continuidad.
- **Demo (29):** lanzar el despliegue de B; mientras corre, enseñar una ejecución ya terminada.
- **Pregunta:** «¿Qué diferencia hay entre "el servicio está estable" y "el servicio ejecuta B"?».

### 19:34 · Bloque 5 · Observabilidad y rollback (30–36)

- Cuatro herramientas para cuatro preguntas: logging (qué pasó en una petición), monitoring
  (cómo va el servicio: errores, latencia), APM/trazas (dónde se va el tiempo entre servicios) y
  error tracking (agrupar excepciones y avisar). La demo implementa logs y métricas; APM y
  error tracking se explican, **no se integran**.
- Log estructurado: una línea JSON con `request_id`, `version`, `ruta`, `estado`, `duracion_ms`,
  `proveedor_ms`. Nunca el texto del usuario ni secretos.
- **APM (32):** una petición a `/clasificar` en cascada: span raíz de 2.400 ms y span cliente de
  OpenRouter (`openai/gpt-6-luna`) de 2.370 ms, el 99 %: el cuello de botella es el proveedor.
  `trace_id` (32 hex, cabecera `traceparent`, une servicios) frente a `request_id` (lo crea
  nuestra API, une cliente y log). Valores ilustrativos; no hay OpenTelemetry en la demo.
- **Demo · el fallo que los tests no cubrían.** B responde 500 a una consulta de prioridad baja.
  El cliente solo ve un `request_id`; con él se encuentra la línea `excepcion` con `KeyError`
  y la `version` de B. El panel muestra el pico de 5xx y la alarma cambia de estado.
- **Error tracking (34):** el mismo `KeyError: 'baja'` visto en un tracker tipo Sentry: los
  eventos con la misma huella forman una incidencia con frecuencia, usuarios afectados y la
  release B como primera aparición. Esquema rotulado; Sentry no está integrado.
- **Rollback:** el mismo workflow con el digest de A. Sin reconstruir. Repetir la petición: 200.
  Después, arreglar hacia delante con `cambios/03` (el test que faltaba).
- **Pregunta:** «¿El rollback arregla el código?».

### 19:50 · Bloque 6 · Datos y recuperación (37–38)

- Expand → migrar → contract. Durante un despliegue y un rollback conviven dos versiones: el
  esquema debe valer para las dos. **Volver a una imagen antigua no revierte los datos.**
- Backups: RPO y RTO; una copia solo vale si se ha restaurado. `extras/` lo demuestra con SQLite.
- **Pregunta:** «Si B escribió datos en una columna nueva y volvemos a A, ¿qué pasa con ellos?».

### 19:54 · Práctica y cierre (39–40)

- Práctica opcional: [ejercicio.md](ejercicio.md). Evidencias: PR roja, digest publicado,
  despliegue, error localizado, rollback y retirada de recursos.
- Recordar el QR de S17. Próxima sesión: S19, evaluación y testing de sistemas de IA.

## Si algo falla en directo

| Situación | Qué hacer |
|---|---|
| Un workflow tarda más de 2 minutos | Seguir con la ejecución ya terminada; volver al final del bloque |
| GitHub o AWS no responden | Recorrido local equivalente (comandos.md, columna «Local») y decirlo |
| El smoke falla en staging | Es la demo de que «un job verde no basta»: leer el error, no forzarlo |
| Pregunta fuera de alcance (Kubernetes, Terraform…) | Responder en una frase y apuntarla para el cierre |
