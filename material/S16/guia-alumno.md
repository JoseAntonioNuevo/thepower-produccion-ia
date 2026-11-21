# Guía del alumno S16

Versión común para las clases del 12 y 18 de noviembre de 2026. La práctica es opcional.

## 1. Preparación y resultado esperado

Empieza por `S16-inicio.zip`: contiene la API preparada y sus pruebas. Usa `S16-referencia.zip` para consultar la solución por pasos; no necesitas estudiar los módulos de otras sesiones.

Trabajarás con datos ficticios. El resultado final es una API FastAPI en un contenedor Fargate que invoca un modelo, con imagen identificada, secretos protegidos, coste y retirada documentados. La demo local es el primer ensayo; la ejecución real se hace únicamente en la cuenta y presupuesto del laboratorio.

Necesitas Python 3.12, uv, Docker Desktop y acceso al código. Para AWS, una identidad de laboratorio con perfil configurado, región, cuenta y permisos delegados. El script utiliza boto3; AWS CLI v2 sirve para configurar/iniciar una sesión SSO si ese es el acceso proporcionado. Nunca pegues contraseñas o claves en un chat de ayuda.

Abre la raíz del proyecto descargado, la carpeta que contiene `pyproject.toml`. Los comandos siguientes se ejecutan ahí. En Windows usa el terminal Bash del entorno del curso o adapta la asignación de variables a PowerShell; Python y las plantillas son comunes.

## Mapa de la práctica

| Paso | Qué haces | Cuándo avanzar |
|---|---|---|
| 1 · Local | Instalar, leer la API y ejecutar Docker | Salud ok, clasificación demo y usuario 10001 |
| 2 · Imagen | Publicar en ECR | Images muestra el tag y el digest de tu versión |
| 3 · Tarea | Revisar imagen, recursos, modelo y secreto | Configuración coherente y ARN sin revelar la clave |
| 4 · Red | Revisar servicio, IP, ruta y reglas | Tarea RUNNING, healthcheck HEALTHY y acceso desde tu /32 |
| 5 · Función | Probar salud y una clasificación real | execution real, versión y request ID localizable en logs |
| 6 · Cierre | Calcular y retirar recursos propios | Inventario revisado y remanentes identificados |

Completa una comprobación antes de pasar a la siguiente. Si falla, utiliza el diagnóstico de la sección 12 y conserva un error saneado.

## 2. Instalar y comprobar offline

```bash
uv sync --frozen --all-extras
uv run python scripts/preflight.py
uv run pytest
uv run cfn-lint infra/s16/*.json
```

Esperado: modo `demo`, ninguna comprobación remota, tests correctos y plantillas sin errores. Si la instalación falla, conserva el error, la versión de Python y el sistema operativo. No actualices paquetes al azar: el lock es parte de la práctica.

## 3. Entender el contrato y ejecutar la API

```bash
uv run uvicorn curso_ia.api:create_app --factory --host 127.0.0.1 --port 8016 --no-access-log
```

Abre `http://127.0.0.1:8016/docs`. En otra terminal:

```bash
curl --fail http://127.0.0.1:8016/health
curl --fail -H 'Content-Type: application/json' \
  --data-binary @datos/peticion.json http://127.0.0.1:8016/clasificar
curl -i -H 'Content-Type: application/json' \
  --data-binary @datos/peticion-invalida.json http://127.0.0.1:8016/clasificar
uv run python scripts/ensayo_local.py
```

Salud debe mostrar `status: ok` y `provider_check: no_ejecutado`. La clasificación debe mostrar `execution: demo`, `modelo_devuelto: reglas-demo-v1`, categoría `facturacion` y una respuesta identificada como simulada. La entrada vacía devuelve 422. El ensayo guarda `evidencias/local/ensayo.json`.

Recorre el código en este orden: `contratos.py`, `config.py`, `proveedores.py`, `api.py`. La aplicación valida antes y después del proveedor. Modelo y clave pertenecen a la configuración del servidor; el cliente no puede seleccionarlos en el cuerpo de la petición.

## 4. Contenedor y arquitectura

Detén uvicorn con Ctrl+C para liberar el puerto.

```bash
docker compose up --build -d
docker compose ps
uv run python scripts/ensayo_local.py
docker compose exec api id
docker compose logs --tail 10 api
docker compose down
```

Esperado: UID 10001, API disponible solo en `127.0.0.1:8016` y logs con request ID, versión, estado y duración. El contenido de la incidencia y la clave no aparecen en ellos.

La imagen es una receta construida; un contenedor es una ejecución de esa imagen. `EXPOSE 8000` documenta el puerto; el mapeo de Compose publica 8016 del host hacia 8000 del contenedor. Un contenedor efímero no conserva una base de datos por el hecho de estar en cloud.

```bash
docker build --platform linux/amd64 --provenance=false \
  --build-arg APP_VERSION=s16-ensayo-01 -t thepower-s16:ensayo .
docker image inspect thepower-s16:ensayo --format '{{.Os}}/{{.Architecture}} {{.Config.User}}'
```

Esperado: `linux/amd64 10001:10001`. La plantilla Fargate usa X86_64. Si eliges ARM64, debes cambiar y verificar ambos extremos; no basta con cambiar el nombre de la etiqueta.

## 5. Preparar el destino AWS

La cuenta del curso debe facilitar identidad, región, permisos y presupuesto. No uses una cuenta ajena por comodidad. Para una identidad SSO ya acordada:

```bash
aws configure sso --profile curso-s16
aws sso login --profile curso-s16
```

Si la escuela entrega otro mecanismo temporal, sigue sus instrucciones. No crees claves permanentes como sustituto de un acceso que falla. El operador necesita crear los recursos de CloudFormation de la práctica, ECR, ECS, VPC/red, logs y roles limitados, además de `iam:PassRole`; la cuenta puede necesitar el service-linked role de ECS. Esos permisos deben quedar preparados antes de la clase, no resolverse concediendo AdministratorAccess al alumno.

Sustituye estos valores por los del laboratorio autorizado:

```bash
S16_PROFILE=curso-s16
S16_REGION=eu-west-1
S16_ACCOUNT=123456789012
S16_LAB=s16-mi-nombre
S16_VERSION=ensayo-01
S16_ARGS=(--profile "$S16_PROFILE" --region "$S16_REGION"
  --cuenta "$S16_ACCOUNT" --lab "$S16_LAB")
uv run python scripts/aws_lab.py plan "${S16_ARGS[@]}"
```

`123456789012` es un marcador, no la cuenta del curso. Los comandos comprueban STS contra el valor esperado y se detienen si no coincide. El nombre del laboratorio debe ser propio y comenzar por `s16-`. Guarda los recibos de cada etapa y usa una versión nueva para cada imagen: las etiquetas de ECR son inmutables.

## 6. Crear ECR y publicar

Estos comandos crean recursos y pueden generar gasto; ejecútalos dentro del alcance autorizado de la práctica.

```bash
uv run python scripts/aws_lab.py bootstrap "${S16_ARGS[@]}" --execute
uv run python scripts/aws_lab.py publicar "${S16_ARGS[@]}" --version "$S16_VERSION" --execute
```

El segundo construye amd64, autentica Docker por stdin, publica y obtiene el digest desde ECR. Lee `evidencias/aws/<tu-lab>/publicacion.json`: debe identificar cuenta, región, laboratorio, versión, plataforma e imagen `repositorio@sha256:...`. Abre en consola **ECR → repositorio de tu laboratorio → Images** y localiza los mismos valores. Tener la imagen en ECR todavía no inicia la API. No confundas el tag elegido con el digest calculado sobre el artefacto.

## 7. Guardar el secreto

Puedes seleccionar un secreto existente de la cuenta/región, respetando su propiedad, o crear uno propio con:

```bash
uv run python scripts/aws_lab.py crear-secreto "${S16_ARGS[@]}" --execute
```

El programa pide la clave mediante entrada oculta; no aparece en el comando ni se guarda en el recibo. Conserva el ARN de `evidencias/aws/<tu-lab>/secreto.json`. Si la creación acaba con timeout, consulta Secrets Manager y el nombre `<tu-lab>/anthropic` antes de repetir. Una repetición ciega no es un procedimiento de recuperación.

La plantilla lee ese ARN mediante el **execution role** al arrancar. El **task role** sería la identidad de la aplicación para llamar a APIs de AWS; en S16 no necesita permisos. El operador que crea la infraestructura es una tercera identidad distinta.

Secrets Manager es la opción implementada; Parameter Store es una alternativa del ejercicio que exige adaptar la referencia y los permisos de lectura. Con KMS propia añade `--kms-arn` en creación y despliegue y verifica que la key policy permite al execution role descifrar. No escribas claves en Dockerfile, build args, Git ni parámetros CloudFormation.

## 8. Desplegar Fargate

```bash
S16_IP=TU_IPV4_PUBLICA/32
S16_SECRET_ARN=ARN_DEL_SECRETO
S16_MODEL=ID_DISPONIBLE_EN_TU_CUENTA
uv run python scripts/aws_lab.py desplegar "${S16_ARGS[@]}" \
  --ip "$S16_IP" --secret-arn "$S16_SECRET_ARN" --modelo "$S16_MODEL" --execute
uv run python scripts/aws_lab.py estado "${S16_ARGS[@]}"
```

En consola, abre **ECS → Task definitions → revisión usada**: comprueba imagen por digest, 0,25 vCPU, 512 MiB, Linux/X86_64, puerto 8000, modelo y referencia al secreto. Después abre **ECS → servicio → tarea → Networking** y sigue el enlace al security group. El script crea los recursos, pero conviene leer esta configuración para entenderlos.

La IPv4 es la pública desde la que probarás, incluida la salida de VPN si la utilizas. No pongas `0.0.0.0/0`. El script exige /32 pública. La subred tiene ruta al internet gateway, la ENI recibe una IP y el security group permite entrada 8000 desde esa IP y salida 443. DNS y la ruta de salida también son necesarios para resolver y alcanzar los servicios.

El estado devuelve una URL temporal y comprueba la task definition y el digest que ECS observa. Es todavía una lectura de infraestructura, no una respuesta del modelo. El coste continúa mientras la tarea permanezca activa. La configuración de una tarea acepta interrupción al actualizar; no es alta disponibilidad.

## 9. Verificar función real y observar

```bash
uv run python scripts/aws_lab.py verificar "${S16_ARGS[@]}" --execute
```

Hace un GET de salud y **una** clasificación sintética real. Guarda la versión y el resultado en `verificacion.json`. El coste de inferencia permanece nulo si el proveedor no lo informa; usa tokens y tarifas separadas para estimarlo. La demo no envía credenciales de cliente por HTTP. La clave de Anthropic sale del contenedor hacia el proveedor por HTTPS.

En CloudWatch abre el grupo `/thepower/<tu-lab>`. Busca el request ID de la respuesta y comprueba versión, estado y duración. Si el stack está verde pero la petición falla, el ejercicio aún no está completado.

## 10. Calcular costes

```bash
uv run python scripts/costes.py datos/costes-ejemplo.json
```

Revisa las nueve partidas: CPU, memoria, IPv4, almacenamiento ECR, ingesta y almacenamiento de logs, secreto, lecturas del secreto y salida a Internet. Incluye cualquier recurso que añadas. Las cantidades del ejemplo son supuestos, las tarifas proceden del catálogo público en Irlanda del 17/10/2026. La salida a Internet representa GB ya facturables después del tramo gratuito global.

El ejemplo mensual suma 13,78 USD sin inferencia. La demo suma 0,46 USD con **90 minutos de cómputo/IP y 30 días de ECR, secreto y logs almacenados**. Aproximadamente 0,0260 USD corresponden al cómputo/IP, 0,4253 USD a esa retención y 0,0058 USD a ingesta, lectura y salida; el total se redondea al final. No son 0,46 USD por solo 90 minutos de todos los recursos: parar cómputo no elimina esos remanentes. Calcula la inferencia aparte con proveedor, modelo, tokens y tarifas. No mezcles un coste estimado con un importe de factura ni presupongas que el crédito gratuito está disponible.

## 11. Limpiar e inventariar

```bash
uv run python scripts/aws_lab.py limpiar "${S16_ARGS[@]}" --execute
# Solo si creaste el secreto con este laboratorio y ya no se utiliza:
uv run python scripts/aws_lab.py retirar-secreto "${S16_ARGS[@]}" --execute
```

La limpieza elimina el servicio y su red/roles/logs, vacía únicamente el repositorio ECR etiquetado como propio y elimina su stack. El secreto se conserva hasta el segundo comando, que programa su borrado con recuperación de siete días. Comprueba el estado de retirada y la fecha; no anuncies que ya desapareció. Los secretos compartidos y una KMS externa no se borran automáticamente.

Completa el inventario en ECS, ECR, CloudWatch, VPC/ENI/IP y Secrets Manager. Revisa también cualquier recurso añadido manualmente (ALB, NAT, Elastic IP, almacenamiento, KMS). Conserva un registro de qué se eliminó, qué quedó y quién es su propietario. Una factura puede reflejar consumo anterior después de haber retirado los recursos.

## 12. Diagnóstico y ayuda sin secretos

| Síntoma | Revisar |
|---|---|
| Puerto 8016 ocupado | Detener el otro uvicorn/Compose propio o elegir otro puerto y pasarlo al ensayo |
| Imagen no arranca | Arquitectura, comando de inicio y logs; no adivinar un problema de IA |
| No descarga imagen o secreto | Execution role, ARN, región, red, KMS si procede |
| API no responde desde el Mac | Tarea activa, IP actual, /32 del profesor, puerto y ruta |
| Salud correcta; clasificación 502/503/504 | Modelo/clave disponible, límites, conectividad y tiempo del proveedor |
| Stack en rollback | Leer eventos de CloudFormation y reconciliar recursos antes de repetir |
| Cleanup no termina | Revisar recurso bloqueante y referencias; nunca borrar recursos compartidos |

Para pedir ayuda a una IA: «Estoy en S16. Este es mi sistema operativo, versión de Python/Docker, comando sin secretos, código de salida, error saneado y la parte del README que sigo. Explica la causa probable y una comprobación de solo lectura antes de proponer cambios». No adjuntes `.env`, tokens, claves, cookies ni cuerpos con datos reales.
