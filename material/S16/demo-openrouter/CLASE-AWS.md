# S16 · Guion del directo: Docker → ECR → ECS/Fargate

Preparado el **11/11/2026** para José. Los identificadores de `aws/` pertenecen exclusivamente al proyecto **For Each and Every**, ID `123456789012`, perfil `thepower-aws`, región seleccionada **Estocolmo / eu-north-1**. Los alumnos deben usar sus propios proyectos, secretos y permisos. El README público contiene un ejemplo genérico en Irlanda: para este directo prevalecen los valores de esta guía.

**Recorrido de una mirada:** Docker local y `/docs` → crear ECR, login y push → explicar el JSON y registrar tarea → crear servicio Fargate → obtener IP, probar salud/clasificación y abrir logs → mostrar costes y retirar los recursos propios. Los comandos de cada parada están debajo; `aws/` ya contiene las plantillas con los valores del profesor.

## Antes de compartir pantalla · 10 minutos

Abre Docker Desktop; una terminal en esta carpeta; el editor con `app.py`, `Dockerfile` y `aws/task-definition.json`; el navegador con ECR, ECS y CloudWatch. Ten AWS Settings en otra pestaña. Cierra `.env`, cualquier visor de secretos y paneles de variables del contenedor. Usa exclusivamente incidencias ficticias.

```bash
cd /Users/jose/Documents/the-power/4-produccion-ia/material/S16/demo-openrouter
source aws/contexto.sh
s16_comprobar_identidad
aws_demo freetier get-account-plan-state
docker info
```

**Detente si la identidad falla o es otro proyecto.** Si ha caducado la sesión, renueva tú la sesión con `aws login --profile thepower-aws` y repite la comprobación. No uses un perfil global alternativo. Comprueba la región también en **AWS Settings → View all projects → Overview → Additional Info → Region**. El MCP está cargado y registra `thepower-aws`; su conexión técnica a `us-east-1` no cambia la región de los recursos.

En **AWS Settings → Billing**, revisa plan, créditos y límites de gasto existentes, sin cambiarlos. La lectura inicial indicó plan FREE activo, 100 USD de crédito y vencimiento el 09/05/2027; vuelve a consultarlo el día de clase. No se ha creado un presupuesto. En Billing and Cost Management puedes consultar costes por servicio: los datos pueden tardar en aparecer y los créditos no equivalen a coste de catálogo cero. Revisa por separado saldo y consumo de OpenRouter.

Deja la imagen construida para que la primera descarga no consuma el tiempo del directo:

```bash
docker build --platform linux/amd64 -t s16-clasificador:1 .
docker image inspect s16-clasificador:1 --format '{{.Os}}/{{.Architecture}}'
# Esperado: linux/amd64. No muestres docker inspect sobre un contenedor con claves.
bash aws/actualizar-ip.sh --execute
```

El último comando consulta tu IPv4 pública por HTTPS, la valida, comprueba el grupo propio y añade o sustituye una única regla **TCP 8000 desde tu IP /32**. Ejecútalo desde la red/VPN que hará las pruebas; repítelo si cambia. Ahora mismo el grupo está **sin entrada**. El script pasa validación de sintaxis y cuatro casos con dobles locales (alta, sustitución, rechazo de entrada amplia y rechazo de otro proyecto). No se ha ejecutado contra AWS durante la preparación para mantenerlo cerrado.

## 1. Docker local · 5 minutos

```bash
docker run --platform linux/amd64 --rm -d --name s16-demo \
  --env-file .env -p 127.0.0.1:8000:8000 s16-clasificador:1
curl --fail-with-body --max-time 10 http://127.0.0.1:8000/health
curl --fail-with-body --max-time 40 http://127.0.0.1:8000/clasificar \
  -H 'Content-Type: application/json' -d '{"texto":"No puedo entrar en mi cuenta ficticia"}'
```

Abre [Swagger local](http://127.0.0.1:8000/docs). Esperado: salud `estado=ok, modo=real`; clasificación con `modo=real`, modelo `openai/gpt-6-luna` y resultado validado. La segunda petición consume OpenRouter. Explica: **imagen = paquete; contenedor = proceso; puerto publicado = acceso al proceso**. `EXPOSE` documenta; `-p` conecta. La clave entra al ejecutar, no al construir. `/health` no prueba el modelo. Al terminar: `docker stop s16-demo`.

Si falla el proveedor, muestra explícitamente el modo simulado: detén el contenedor y arráncalo sin `--env-file .env`. La respuesta indicará `modo=demo`; no lo presentes como inferencia real.

## 2. Crear ECR y publicar · 5 minutos

**Este repositorio no se ha creado todavía.** En ECR muestra primero la lista vacía. Ejecuta en la misma terminal con el contexto cargado:

```bash
aws_demo ecr create-repository --repository-name "$S16_REPOSITORY" \
  --image-tag-mutability IMMUTABLE --encryption-configuration encryptionType=AES256 \
  --tags Key=Project,Value=thepower-s16 Key=Purpose,Value=classroom-demo
aws_demo ecr get-login-password | docker login --username AWS --password-stdin "$S16_REGISTRY"
docker tag s16-clasificador:1 "$S16_IMAGE"
docker push "$S16_IMAGE"
aws_demo ecr describe-images --repository-name "$S16_REPOSITORY" --image-ids imageTag=1 \
  --query 'imageDetails[].{tag:imageTags,digest:imageDigest,bytes:imageSizeInBytes}'
```

Espera al push completo. Muestra **ECR → s16-clasificador → Images**: etiqueta `1` y digest. Explica: **ECR almacena la imagen; aún no ejecuta nada**. El registro usa escaneo BASIC actualmente; no se cambió la configuración compartida. Si quieres enseñar el escaneo, lanza un escaneo básico manual del repositorio propio; no actives Inspector para toda la región. Una etiqueta inmutable no se sobrescribe: para repetir una versión cambia la etiqueta y la referencia de la tarea, o retira antes la imagen propia tras comprobar su uso.

## 3. Completar y registrar la tarea · 5 minutos

Abre `aws/task-definition.json` en el editor y explica sus campos antes de registrarlo:

| Campo | Valor / explicación |
|---|---|
| Familia / contenedor | `s16-thepower-api` / `api` |
| Plataforma | Linux X86_64, Fargate, `awsvpc` |
| CPU / memoria | 256 unidades = 0,25 vCPU / 512 MiB |
| Imagen / puerto | URI de ECR con etiqueta `1` / TCP 8000 |
| Entorno | `API_MODE=real`, modelo `openai/gpt-6-luna`, proveedor `openai/fast` |
| Secreto | `OPENROUTER_API_KEY` referencia un ARN; nunca contiene la clave |
| Execution role | Descarga ECR, crea streams/escribe logs y obtiene este secreto |
| Task role | Omitido: la aplicación no llama al SDK de AWS |
| Logs / salud | Grupo `/s16/thepower/api`, prefijo `api`; healthcheck local sin inferencia |

El execution role tiene una política propia más restringida que `AmazonECSTaskExecutionRolePolicy`: solo este repositorio, streams `api/*` de este grupo y el ARN completo del secreto. `ecr:GetAuthorizationToken` requiere `Resource=*`. El secreto es texto completo cifrado con la clave administrada por AWS; no hay KMS propia ni rotación que pueda invalidar una clave externa. Si actualizas la clave en el futuro, las tareas existentes necesitan reiniciarse para recibirla.

Puedes pegar el JSON en **ECS → Task definitions → Create new task definition with JSON**, o ejecutar:

```bash
S16_TASK_DEF_ARN="$(aws_demo ecs register-task-definition \
  --cli-input-json file://aws/task-definition.json \
  --query 'taskDefinition.taskDefinitionArn' --output text)"
printf '%s\n' "$S16_TASK_DEF_ARN"
```

Esperado: ARN terminado en `task-definition/s16-thepower-api:1` en el primer registro. No registres dos veces si ya lo hiciste en consola; usa el ARN de esa revisión. **Una definición describe cómo arrancar; todavía no hay una aplicación ejecutándose.**

## 4. Lanzar en Fargate · 5–10 minutos

En **ECS → Clusters → s16-thepower**, muestra el cluster vacío preparado. Abre `aws/network.json`: tres subredes públicas existentes, grupo propio e IP pública habilitada. Hay DNS y ruta `0.0.0.0/0` a internet gateway; la salida HTTPS permite ECR/S3, secretos, logs y OpenRouter. Se usa el DNS de la VPC, que no requiere abrir entrada DNS en el grupo. No hay NAT ni balanceador.

```bash
aws_demo ecs create-service --cluster "$S16_CLUSTER" --service-name "$S16_SERVICE" \
  --task-definition "$S16_TASK_DEF_ARN" --desired-count 1 --launch-type FARGATE \
  --platform-version 1.4.0 --network-configuration file://aws/network.json \
  --deployment-configuration 'minimumHealthyPercent=0,maximumPercent=100,deploymentCircuitBreaker={enable=true,rollback=true}' \
  --tags key=Project,value=thepower-s16 key=Purpose,value=classroom-demo
aws_demo ecs wait services-stable --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
aws_demo ecs describe-services --cluster "$S16_CLUSTER" --services "$S16_SERVICE" \
  --query 'services[].{status:status,desired:desiredCount,running:runningCount,pending:pendingCount,deployments:deployments,events:events[:5]}'
```

Esperado: una tarea `RUNNING`, contenedor `HEALTHY`, despliegue `COMPLETED`. Si el waiter falla, revisa eventos y tareas detenidas; no lances servicios duplicados. En el primer despliegue no existe una revisión anterior a la que volver: el circuit breaker ayuda a detener intentos fallidos, pero exige corregir la causa. El servicio mantiene la tarea viva y la repone si falla: **parar una tarea no para el servicio**. Se acepta interrupción al actualizar para mantener una sola tarea en esta demo.

En consola selecciona **Tasks → tarea → Networking → Public IP**, o usa:

```bash
S16_TASK_ARN="$(aws_demo ecs list-tasks --cluster "$S16_CLUSTER" --service-name "$S16_SERVICE" \
  --desired-status RUNNING --query 'taskArns[0]' --output text)"
S16_ENI="$(aws_demo ecs describe-tasks --cluster "$S16_CLUSTER" --tasks "$S16_TASK_ARN" \
  --query 'tasks[0].attachments[].details[?name==`networkInterfaceId`].value[] | [0]' --output text)"
S16_PUBLIC_IP="$(aws_demo ec2 describe-network-interfaces --network-interface-ids "$S16_ENI" \
  --query 'NetworkInterfaces[0].Association.PublicIp' --output text)"
printf 'http://%s:8000/docs\n' "$S16_PUBLIC_IP"
```

La IP es efímera y cambia al reemplazar la tarea. HTTP sin autenticación se limita a tu `/32`, datos ficticios y una sesión temporal; no es un servicio de producción ni un endpoint público para todos los alumnos.

## 5. Salud, clasificación y logs · 5 minutos

```bash
curl --fail-with-body --connect-timeout 5 --max-time 10 "http://$S16_PUBLIC_IP:8000/health"
curl --fail-with-body --connect-timeout 5 --max-time 40 "http://$S16_PUBLIC_IP:8000/clasificar" \
  -H 'Content-Type: application/json' -d '{"texto":"No puedo entrar en mi cuenta ficticia"}'
aws_demo logs tail "$S16_LOG_GROUP" --since 10m
```

Muestra también **CloudWatch → Log groups → /s16/thepower/api → api/api/ID_TAREA**. Los logs contienen arranque y errores de proceso; Uvicorn tiene desactivado el access log, así que cada petición HTTP no genera necesariamente una línea. La retención es de 3 días; el grupo no se elimina automáticamente.

| Fallo | Comprobación práctica |
|---|---|
| `ExpiredToken` / sesión caducada | Renueva el login del perfil y vuelve a comprobar identidad. |
| `AccessDenied` tras funcionar | Revisa el plan, créditos y spend limit en AWS Settings; conserva el error y revisa permiso/rol/región. No amplíes permisos generales. |
| Push sin autorización | Repite login de ECR; el token dura 12 h. Comprueba el perfil, la URI y la etiqueta inmutable. |
| `exec format error` / plataforma incompatible | Imagen `linux/amd64` y tarea `X86_64`; reconstruye y publica una nueva etiqueta. |
| `ResourceInitializationError` | Mira el motivo de parada: execution role, ARN exacto del secreto, AWSCURRENT, logs, IP pública, ruta IGW y salida 443. |
| `CannotPullContainerError` | Confirma push/digest y permisos de ECR; DNS, salida HTTPS e IP pública. |
| Tarea pendiente o sin capacidad | Lee eventos, cuota de vCPU y disponibilidad Fargate en las subredes; no cambies de región. |
| Timeout HTTP | Verifica IP nueva de tarea y profesor, regla /32, puerto 8000, tarea sana e IP pública. Ejecuta otra vez el actualizador de IP si cambió la red. |
| Salud correcta, 503 al clasificar | Falta la clave en el entorno; revisa la referencia del secreto, nunca muestres su valor. |
| 502 al clasificar | Conectividad HTTPS, saldo/estado de OpenRouter, modelo, proveedor rápido o respuesta inválida. No hay fallback automático. |
| 422 | El JSON debe incluir `texto` no vacío y de hasta 1.000 caracteres. |

## 6. Costes y retirada · 5 minutos

Tarifas públicas consultadas para **eu-north-1** mediante Price List API el 11/11/2026; detalle/SKU/fechas en `aws/tarifas-2026-11-11.json`. Son estimaciones antes de créditos e impuestos, no una factura real:

| Concepto | Tarifa de catálogo |
|---|---|
| Fargate Linux X86_64 | 0,0445 USD/vCPU-h + 0,0049 USD/GB-h |
| Una IPv4 pública | 0,005 USD/h mientras se utiliza |
| ECR | 0,10 USD/GB-mes almacenado |
| CloudWatch Logs | 0,54 USD/GB ingerido + 0,028 USD/GB-mes almacenado |
| Secrets Manager | 0,40 USD/secreto-mes prorrateado + 0,05 USD/10.000 llamadas |

Una tarea de 0,25 vCPU y 0,5 GB más IPv4: **0,018575 USD/h**, aproximadamente **0,03715 USD en dos horas**, más los otros conceptos. Dejarla 730 h con un secreto: **13,95975 USD**, antes de imágenes/logs/tráfico/inferencia. El secreto preparado cuesta aproximadamente 0,01315 USD/día usando un mes de 730 h. No hay cargos fijos propios por el rol, grupo de seguridad, cluster vacío o grupo de logs vacío. El tráfico a Internet y OpenRouter van aparte; consulta sus tarifas y consumo antes del directo. El crédito puede cubrir uso elegible, no evita tener que limpiar.

**Retirada manual al terminar, no ejecutada durante la preparación.** Repite identidad. Comprueba etiquetas `Project=thepower-s16`, nombres y uso; no ejecutes estas órdenes sobre recursos compartidos. Esta secuencia presupone un servicio y una revisión creados en este directo:

```bash
s16_comprobar_identidad
# Guarda la revisión antes de borrar el servicio (también sirve si reiniciaste la terminal).
S16_TASK_DEF_ARN="$(aws_demo ecs describe-services --cluster "$S16_CLUSTER" --services "$S16_SERVICE" \
  --query 'services[0].taskDefinition' --output text)"
aws_demo ecs update-service --cluster "$S16_CLUSTER" --service "$S16_SERVICE" --desired-count 0
aws_demo ecs wait services-stable --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
aws_demo ecs list-tasks --cluster "$S16_CLUSTER" --desired-status RUNNING
aws_demo ecs describe-clusters --clusters "$S16_CLUSTER" \
  --query 'clusters[].{running:runningTasksCount,pending:pendingTasksCount}'
# Lista vacía y contadores 0. Si hubiera tareas independientes, identifica su origen antes de detenerlas.
aws_demo ecs delete-service --cluster "$S16_CLUSTER" --service "$S16_SERVICE"
aws_demo ecs wait services-inactive --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
aws_demo ecs deregister-task-definition --task-definition "$S16_TASK_DEF_ARN"
# La revisión INACTIVE no ejecuta ni factura cómputo. Revisa si registraste más revisiones propias.
aws_demo ecs delete-cluster --cluster "$S16_CLUSTER"
aws_demo ecr batch-delete-image --repository-name "$S16_REPOSITORY" --image-ids imageTag=1
aws_demo ecr delete-repository --repository-name "$S16_REPOSITORY"
aws_demo logs delete-log-group --log-group-name "$S16_LOG_GROUP"
aws_demo secretsmanager delete-secret --secret-id "$S16_SECRET_ARN" --recovery-window-in-days 7
aws_demo iam delete-role-policy --role-name "$S16_EXECUTION_ROLE" --policy-name s16-runtime-only
aws_demo iam delete-role --role-name "$S16_EXECUTION_ROLE"
aws_demo ec2 describe-network-interfaces --filters "Name=group-id,Values=$S16_SECURITY_GROUP"
# Espera a que ECS libere todas sus interfaces antes de borrar el grupo; no las fuerces.
aws_demo ec2 delete-security-group --group-id "$S16_SECURITY_GROUP"
```

Si ECR tiene otras imágenes, la eliminación sin `--force` falla: revisa que todas sean propias antes de retirarlas. Si no se llegó a crear el servicio o ECR, omite sus pasos y retira únicamente lo que consta creado. No pegues toda la limpieza a ciegas tras un despliegue fallido.

**Conserva** la VPC, las tres subredes, rutas, ACL, gateway, DNS, grupo `default` y los roles existentes. Conserva también `AWSServiceRoleForECS`: es un rol gestionado por el servicio a nivel de proyecto, sin cargo fijo. No borres la clave de OpenRouter del proveedor ni el `.env` local al retirar el secreto de AWS.

Comprueba después: cluster `INACTIVE` o ausente, servicio `INACTIVE`, cero tareas `RUNNING/PENDING`, ECR ausente, logs ausentes, ninguna ENI del grupo propio y grupo borrado. `describe-secret` debe mostrar `DeletedDate` con recuperación de 7 días; programar el borrado no equivale a borrado inmediato. [AWS no cobra los secretos programados para eliminación](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html). Revisa AWS Settings/Billing y OpenRouter de nuevo cuando se actualicen los consumos. Ningún presupuesto nuevo ni cambio de gasto se ha aplicado.

## Evidencia y límites de esta preparación

- **Reales:** MCP y perfil coincidentes; identidad/nombre/plan/región; catálogo regional; inventario sin duplicados; red/DNS/rutas/ACL revisados; cuota Fargate On-Demand 12 vCPU; secreto nuevo con versión AWSCURRENT y coincidencia comprobada en memoria con la clave local, sin imprimirla; permisos y confianza leídos de nuevo; validación Access Analyzer sin hallazgos; simulación IAM positiva y negativa con contexto regional, PassRole y operaciones del directo permitidas; cluster vacío; logs con 3 días; grupo sin entrada y solo salida 443; build Docker amd64; salud/clasificación simulada y entrada inválida en Docker; contenedor de prueba detenido. JSON validado contra los esquemas del SDK sin registrar tareas.
- **Reservado al directo:** crear ECR, autenticarse/push, registrar la definición, crear servicio, asignar IPv4, descarga/inyección de secreto/logs desde Fargate, llamadas HTTP remotas, inferencia desde AWS y limpieza. Las plantillas están preparadas localmente, no registradas. La simulación IAM y el análisis de red no garantizan el camino de datos ni la capacidad efectiva del día de clase.
- **Inferencia real local:** ya probada anteriormente según José; no repetida en esta preparación. Solo se usó modo demo para clasificar ahora.
- **Comprobaciones del repositorio:** 45 pruebas pasan, `cfn-lint` de S16/S17 y preflight offline pasan. Ruff y formato de la demo pasan; las comprobaciones globales fallan en generadores de presentaciones preexistentes ajenos a este cambio (4.733 avisos de lint y 19 archivos por formatear). No se han modificado esos archivos.
- No se necesita un ensayo AWS para preparar este apoyo. Un ensayo integral exigiría otro ECR con imagen, revisión de tarea, servicio/tarea Fargate, ENI/IPv4 y logs, más una inferencia OpenRouter. No se ha realizado ni se realizará sin presentar ese alcance y recibir autorización específica.
- Sin commit, push, despliegue ni cambios en facturación/credenciales. OpenViking sigue pendiente: el repositorio no tiene tenant mapeado; el recibo y las decisiones se conservan aquí.

Fuentes: [servicios del plan nuevo](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html), [restricciones regionales de proyectos](https://docs.aws.amazon.com/accounts/latest/reference/scps-and-rcps-for-projects.html), [rol de ejecución de ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html), [precios Fargate](https://aws.amazon.com/fargate/pricing/), [precios Secrets Manager](https://aws.amazon.com/secrets-manager/pricing/). Las tarifas numéricas proceden de las respuestas Price List guardadas, no de una estimación de factura.
