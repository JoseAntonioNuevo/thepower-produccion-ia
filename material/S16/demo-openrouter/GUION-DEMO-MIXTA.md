# S16 · Demo mixta AWS

**Enseñar en la web → ejecutar por bloques → comprobar en la web.**
Si falla un comando, parar. No mostrar `.env` ni la clave.

## Antes de clase · Preparar la terminal

La imagen ya debe estar construida y probada. Los nombres con `$` son datos que guardamos para usarlos después.

**Entrar en la carpeta de nuestra aplicación.**

```bash
cd /Users/jose/Documents/the-power/4-produccion-ia/material/S16/demo-openrouter
```

**Cargar los nombres y el acceso de nuestro proyecto AWS.**

```bash
source aws/contexto.sh
```

**Detectar fallos cuando un comando pasa su resultado a otro.**

```bash
set -o pipefail
```

**Comprobar que estamos trabajando en el proyecto correcto.**

```bash
s16_comprobar_identidad
```

**Mostrar el tipo de imagen para comprobar que sirve en AWS.**

```bash
docker image inspect s16-clasificador:1 --format '{{.Os}}/{{.Architecture}}'
```

Esperado: proyecto **123456789012** e imagen **linux/amd64**.
Si la sesión ha caducado, `aws login --profile thepower-aws --region eu-north-1` abre el navegador para volver a entrar.

## 1 · WEB — Qué tenemos preparado

> «Tenemos la configuración preparada, pero la aplicación aún no está funcionando en AWS».

- Región: **Estocolmo / eu-north-1**.
- ECS → **s16-thepower** → cero servicios y tareas.
- ECR → todavía no hay imagen de la demo.
- IAM → **s16-thepower-ecs-execution** → permisos para leer imagen, clave y guardar mensajes.
- Secrets Manager → **s16/thepower/openrouter** → clave guardada, sin mostrarla.
- VPC → Security groups → **s16-thepower-api** → acceso cerrado.

## 2 · EDITOR — Qué vamos a subir

> «app.py recibe un mensaje como “no puedo entrar en mi cuenta” y usa IA para devolver el tipo de problema, su prioridad y una respuesta sugerida».

Dockerfile prepara el paquete; .dockerignore deja fuera archivos como la clave.

Abrir **app.py**, **Dockerfile** y **.dockerignore**. No construir la imagen durante el directo.

## 3 · COMANDOS — Subir la imagen

**Crear en AWS el lugar donde guardaremos la imagen Docker.** La etiqueta `1` no podrá sobrescribirse con otra imagen.

```bash
aws_demo ecr create-repository --repository-name "$S16_REPOSITORY" \
  --image-tag-mutability IMMUTABLE \
  --encryption-configuration encryptionType=AES256 \
  --tags Key=Project,Value=thepower-s16 Key=Purpose,Value=classroom-demo
```

**Dar permiso a Docker para subir imágenes a nuestro almacén de AWS.**

```bash
aws_demo ecr get-login-password \
  | docker login --username AWS --password-stdin "$S16_REGISTRY"
```

**Poner a la imagen la dirección de destino que tendrá en AWS.**

```bash
docker tag s16-clasificador:1 "$S16_IMAGE"
```

**Subir la imagen desde el ordenador a AWS.**

```bash
docker push "$S16_IMAGE"
```

**WEB:** ECR → **s16-clasificador → Images** → mostrar la imagen con etiqueta **1**.

## 4 · COMANDOS — Guardar cómo se ejecutará

> «Indicamos qué imagen usar, cuánta CPU y memoria darle y dónde encontrar la clave».

Abrir **aws/task-definition.json**: contiene esa configuración y una referencia a la clave, sin su valor.

**Guardar esta configuración en AWS y guardar su identificador para utilizarlo después.**

```bash
S16_TASK_DEF_ARN="$(aws_demo ecs register-task-definition \
  --cli-input-json file://aws/task-definition.json \
  --query 'taskDefinition.taskDefinitionArn' --output text)"
```

**Mostrar el identificador para comprobar que se ha guardado.**

```bash
printf '%s\n' "$S16_TASK_DEF_ARN"
```

**Abrir el puerto 8000 solo para nuestra conexión actual. Así podremos probar la aplicación.**

```bash
bash aws/actualizar-ip.sh --execute
```

## 5 · COMANDOS — Arrancar la aplicación

> «Pedimos a AWS que ejecute una copia de la aplicación y que la vuelva a arrancar si falla».

**Buscar la configuración del paso 4 y guardar su identificador en esta terminal.** El siguiente comando lo necesita para saber qué ejecutar.

```bash
S16_TASK_DEF_ARN="$(aws_demo ecs describe-task-definition \
  --task-definition s16-thepower-api \
  --query 'taskDefinition.taskDefinitionArn' --output text)"
```

**Mostrar el identificador y comprobar que no está vacío.**

```bash
printf '%s\n' "$S16_TASK_DEF_ARN"
```

**Arrancar una copia de la aplicación con la imagen, recursos, clave y red que hemos preparado.**

```bash
aws_demo ecs create-service \
  --cluster "$S16_CLUSTER" --service-name "$S16_SERVICE" \
  --task-definition "${S16_TASK_DEF_ARN:?Falta recuperar la definicion de tarea}" --desired-count 1 \
  --launch-type FARGATE --platform-version 1.4.0 \
  --network-configuration file://aws/network.json \
  --deployment-configuration 'minimumHealthyPercent=0,maximumPercent=100,deploymentCircuitBreaker={enable=true,rollback=true}' \
  --tags key=Project,value=thepower-s16 key=Purpose,value=classroom-demo \
  --query 'service.{nombre:serviceName,deseadas:desiredCount,estado:status}'
```

Para explicarlo: `1` pide una copia; Fargate pone CPU y memoria sin preparar una máquina; `network.json` indica la red y el acceso. Si el arranque falla, AWS detiene el intento y puede volver al anterior si había uno correcto.

**Esperar a que AWS termine de poner en marcha el servicio. Después comprobaremos que la aplicación responde.**

```bash
aws_demo ecs wait services-stable \
  --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
```

**Mientras espera:** ECS → **s16-thepower → Tasks** → ver cómo arranca.

## 6 · COMANDOS — Probar el resultado

Ejecutar estos bloques en la misma terminal.

**Buscar la dirección de la aplicación en AWS y guardarla para las pruebas.**

```bash
S16_PUBLIC_IP="$(bash aws/ip-publica.sh)"
printf 'http://%s:8000/docs\n' "${S16_PUBLIC_IP:?No se pudo obtener la direccion}"
```

**Comprobar que la aplicación responde. Debe devolver `ok` y `real`.**

```bash
curl --fail-with-body --connect-timeout 5 --max-time 10 \
  "http://${S16_PUBLIC_IP:?Falta la direccion}:8000/health"
```

**Enviar el mensaje a la IA y mostrar el tipo de problema, su prioridad y una respuesta sugerida.**

```bash
curl --fail-with-body --connect-timeout 5 --max-time 40 \
  "http://${S16_PUBLIC_IP:?Falta la direccion}:8000/clasificar" \
  -H 'Content-Type: application/json' \
  -d '{"texto":"No puedo entrar en mi cuenta ficticia"}'
```

**Mostrar los mensajes de arranque de la aplicación guardados en AWS.**

```bash
aws_demo logs tail "$S16_LOG_GROUP" --since 30m
```

Consultar `/health` no llama al modelo; la prueba del mensaje sí.
Opcional: abrir la dirección `/docs` que imprime el primer bloque para enseñar la aplicación en el navegador.

## 7 · COMANDOS — Terminar y limpiar

> «Paramos la aplicación, borramos la imagen de AWS y cerramos el acceso».

**Comprobar de nuevo que vamos a modificar el proyecto correcto.**

```bash
s16_comprobar_identidad
```

**Pedir cero copias para que AWS pare la aplicación y no vuelva a arrancarla.**

```bash
aws_demo ecs update-service --cluster "$S16_CLUSTER" --service "$S16_SERVICE" \
  --desired-count 0 --query 'service.desiredCount'
```

**Esperar a que AWS termine de pararla.**

```bash
aws_demo ecs wait services-stable --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
```

**Eliminar el servicio que se encargaba de mantenerla funcionando.**

```bash
aws_demo ecs delete-service --cluster "$S16_CLUSTER" --service "$S16_SERVICE" \
  --query 'service.status'
```

**Esperar a que el servicio quede retirado.**

```bash
aws_demo ecs wait services-inactive --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
```

**Borrar el almacén de esta demo con todas sus imágenes. La imagen local se conserva.**

```bash
aws_demo ecr delete-repository --repository-name "$S16_REPOSITORY" --force
```

**Buscar la regla que abría el puerto 8000 y eliminarla si existe. Así cerramos el acceso.**

```bash
S16_RULE_ID="$(aws_demo ec2 describe-security-group-rules \
  --filters "Name=group-id,Values=$S16_SECURITY_GROUP" \
  --query 'SecurityGroupRules[?IsEgress==`false` && IpProtocol==`tcp` && FromPort==`8000` && ToPort==`8000`].SecurityGroupRuleId | [0]' \
  --output text)"
if [ -n "$S16_RULE_ID" ] && [ "$S16_RULE_ID" != "None" ]; then
  aws_demo ec2 revoke-security-group-ingress --group-id "$S16_SECURITY_GROUP" \
    --security-group-rule-ids "$S16_RULE_ID"
fi
```

## 8 · WEB — Comprobar que hemos terminado

> «La aplicación está parada y conservamos lo necesario para repetir la clase».

- ECS → **cero tareas y servicios**.
- ECR → **s16-clasificador eliminado**.
- Security group → **sin reglas de entrada**.

Conservamos red, permisos, clave y registros. La clave guardada y los registros pueden seguir generando coste.
