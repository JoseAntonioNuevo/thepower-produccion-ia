# Demo AWS · Guion breve

Cargar el proyecto y comprobar la identidad de AWS.

```bash
cd /Users/jose/Documents/the-power/4-produccion-ia/material/S16/demo-openrouter
source aws/contexto.sh
s16_comprobar_identidad
```

Arrancar la API nativa en el Mac; detener antes `s16-demo` si sigue ejecutándose.

```bash
docker run --rm -d --name s16-demo --env-file .env -p 127.0.0.1:8000:8000 s16-clasificador:local
```

Comprobar salud y realizar una clasificación real con OpenRouter.

```bash
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body --max-time 40 http://127.0.0.1:8000/clasificar \
  -H 'Content-Type: application/json' -d '{"texto":"No puedo entrar en mi cuenta ficticia"}'
```

Detener el contenedor local, conservando la imagen.

```bash
docker stop s16-demo
```

Crear ECR, el almacén privado de nuestra imagen.

```bash
aws_demo ecr create-repository --repository-name "$S16_REPOSITORY" \
  --image-tag-mutability IMMUTABLE \
  --tags Key=Project,Value=thepower-s16 Key=Purpose,Value=classroom-demo
```

Autenticar Docker y subir la imagen AMD64 ya preparada para AWS.

```bash
set -o pipefail
aws_demo ecr get-login-password | docker login --username AWS --password-stdin "$S16_REGISTRY"
docker tag s16-clasificador:1 "$S16_IMAGE"
docker push "$S16_IMAGE"
```

Registrar la configuración de ejecución: imagen, recursos, puerto, secreto y logs.

```bash
S16_TASK_DEF_ARN="$(aws_demo ecs register-task-definition \
  --cli-input-json file://aws/task-definition.json \
  --query 'taskDefinition.taskDefinitionArn' --output text)"
printf '%s\n' "$S16_TASK_DEF_ARN"
```

Permitir el puerto 8000 solo desde nuestra IP pública actual.

```bash
bash aws/actualizar-ip.sh --execute
```

Crear un servicio con una tarea en Fargate y esperar a que arranque.

```bash
aws_demo ecs create-service --cluster "$S16_CLUSTER" --service-name "$S16_SERVICE" \
  --task-definition "$S16_TASK_DEF_ARN" --desired-count 1 --launch-type FARGATE \
  --platform-version 1.4.0 --network-configuration file://aws/network.json \
  --deployment-configuration 'minimumHealthyPercent=0,maximumPercent=100,deploymentCircuitBreaker={enable=true,rollback=true}' \
  --tags key=Project,value=thepower-s16 key=Purpose,value=classroom-demo
aws_demo ecs wait services-stable --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
```

Obtener la IP pública temporal de la tarea.

```bash
S16_TASK_ARN="$(aws_demo ecs list-tasks --cluster "$S16_CLUSTER" --service-name "$S16_SERVICE" \
  --desired-status RUNNING --query 'taskArns[0]' --output text)"
S16_ENI="$(aws_demo ecs describe-tasks --cluster "$S16_CLUSTER" --tasks "$S16_TASK_ARN" \
  --query 'tasks[0].attachments[].details[?name==`networkInterfaceId`].value[] | [0]' --output text)"
S16_PUBLIC_IP="$(aws_demo ec2 describe-network-interfaces --network-interface-ids "$S16_ENI" \
  --query 'NetworkInterfaces[0].Association.PublicIp' --output text)"
printf 'http://%s:8000/docs\n' "$S16_PUBLIC_IP"
```

Probar salud y clasificación desde AWS; la segunda llamada consume crédito de OpenRouter.

```bash
curl --fail-with-body --connect-timeout 5 --max-time 10 "http://$S16_PUBLIC_IP:8000/health"
curl --fail-with-body --connect-timeout 5 --max-time 40 "http://$S16_PUBLIC_IP:8000/clasificar" \
  -H 'Content-Type: application/json' -d '{"texto":"No puedo entrar en mi cuenta ficticia"}'
```

Ver los mensajes de arranque en CloudWatch.

```bash
aws_demo logs tail "$S16_LOG_GROUP" --since 30m
```

Al terminar, detener las tareas y eliminar el servicio para dejar de mantener cómputo activo.

```bash
s16_comprobar_identidad
aws_demo ecs update-service --cluster "$S16_CLUSTER" --service "$S16_SERVICE" \
  --desired-count 0 --query 'service.desiredCount'
aws_demo ecs wait services-stable --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
aws_demo ecs delete-service --cluster "$S16_CLUSTER" --service "$S16_SERVICE" --query 'service.status'
aws_demo ecs wait services-inactive --cluster "$S16_CLUSTER" --services "$S16_SERVICE"
```

Borrar únicamente el repositorio de la demo con sus imágenes y manifiestos sin etiqueta.

```bash
aws_demo ecr delete-repository --repository-name "$S16_REPOSITORY" --force
```

Cerrar la entrada de red de la demo, buscando el identificador actual de su regla.

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

Comprobar ceros y listas vacías; quedan secreto, rol, cluster y logs para repetir la clase.

```bash
aws_demo ecs describe-clusters --clusters "$S16_CLUSTER" \
  --query 'clusters[].{tareas:runningTasksCount,pendientes:pendingTasksCount,servicios:activeServicesCount}'
aws_demo ecr describe-repositories --query 'repositories[].repositoryName'
aws_demo ec2 describe-security-groups --group-ids "$S16_SECURITY_GROUP" \
  --query 'SecurityGroups[0].IpPermissions'
aws_demo ec2 describe-network-interfaces --filters "Name=group-id,Values=$S16_SECURITY_GROUP" \
  --query 'NetworkInterfaces[].NetworkInterfaceId'
```
