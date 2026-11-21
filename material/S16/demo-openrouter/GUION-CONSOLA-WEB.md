# S16 · Demo manual desde la consola AWS

## 0. Punto de partida

- Proyecto: **123456789012** · región: **Estocolmo / eu-north-1**.
- Preparados: cluster, red, rol, secreto OpenRouter y logs.
- Sin tareas, servicio ni repositorio ECR. Entrada de red cerrada.
- Crear hoy: **ECR → imagen → tarea → servicio → prueba → limpieza**.

## 1. Comprobar el apoyo — web

1. Elegir **eu-north-1** en la consola.
2. ECS → Clusters → **s16-thepower** → comprobar cero tareas.
3. IAM → Roles → **s16-thepower-ecs-execution** → enseñar permisos.
4. Secrets Manager → **s16/thepower/openrouter** → enseñar ARN, **sin revelar la clave**.
5. CloudWatch → Log groups → **/s16/thepower/api** → retención **3 días**.

## 2. Crear ECR — web

ECR → Private repositories → **Create repository**:

- Nombre: **s16-clasificador**.
- Etiquetas de imagen: **Immutable**.
- Cifrado: **AES-256**.
- Tags: `Project=thepower-s16`, `Purpose=classroom-demo`.
- Pulsar **Create repository**.

## 3. Subir la imagen — terminal

**Único bloque fuera de la web:** construir y publicar Docker.

```bash
cd /Users/jose/Documents/the-power/4-produccion-ia/material/S16/demo-openrouter
docker build --platform linux/amd64 -t s16-clasificador:1 .
```

```bash
aws ecr get-login-password --profile thepower-aws --region eu-north-1 \
  | docker login --username AWS --password-stdin \
    123456789012.dkr.ecr.eu-north-1.amazonaws.com
```

```bash
docker tag s16-clasificador:1 \
  123456789012.dkr.ecr.eu-north-1.amazonaws.com/s16-clasificador:1
docker push \
  123456789012.dkr.ecr.eu-north-1.amazonaws.com/s16-clasificador:1
```

Volver a ECR → repositorio → **Images** → comprobar etiqueta **1**.

Si caducó la sesión: `aws login --profile thepower-aws --region eu-north-1`.

## 4. Crear la receta de la tarea — web

1. Abrir el archivo **aws/task-definition.json** de la demo y copiarlo completo.
2. ECS → Task definitions → **Create new task definition with JSON**.
3. Pegar el JSON y revisar:

| Campo | Valor |
|---|---|
| Familia | s16-thepower-api |
| Cómputo / arquitectura | Fargate · Linux · X86_64 |
| CPU / memoria | 0,25 vCPU · 512 MiB |
| Execution role | s16-thepower-ecs-execution |
| Task role | Sin asignar |
| Contenedor / puerto | api · TCP 8000 |
| Imagen | ECR s16-clasificador:1 |
| Variables | API_MODE=real · OPENROUTER_MODEL=openai/gpt-6-luna · OPENROUTER_PROVIDER=openai/fast |
| OPENROUTER_API_KEY | Referencia al ARN del secreto existente |
| Logs | /s16/thepower/api · eu-north-1 · prefijo api |

4. Pulsar **Create**. Anotar la nueva revisión: todavía no ejecuta nada.

## 5. Abrir acceso desde mi IP — web

VPC → Security groups → **s16-thepower-api** (`sg-0b634fb83eb28d501`):

1. Inbound rules → **Edit inbound rules → Add rule**.
2. **Custom TCP · puerto 8000 · origen My IP (/32)**.
3. Guardar. Si cambia la VPN o conexión, actualizar My IP.

## 6. Crear el servicio — web

ECS → Clusters → **s16-thepower → Services → Create**:

| Campo | Valor |
|---|---|
| Task definition | s16-thepower-api · revisión recién creada |
| Service name | s16-thepower-api |
| Compute options | Launch type → Fargate |
| Platform version | 1.4.0 |
| Service type / Desired tasks | Replica · 1 |
| Min / Max running tasks | 0 % / 100 % |
| Circuit breaker / rollback | Activados |
| VPC | vpc-0125b801d92c9910b |
| Subredes | Las tres de esta VPC por defecto |
| Security group | Solo s16-thepower-api |
| Public IP | Enabled |

Subredes: `subnet-0866346d3f77d89b0`, `subnet-0619a5a72bc97ecab`, `subnet-01fc2f9a98693f522`.

Dejar sin activar balanceador, autoescalado, Service Connect y service discovery.
Pulsar **Create**.

## 7. Probar — navegador

1. Servicio → **Tasks** → esperar **RUNNING / HEALTHY**.
2. Abrir la tarea → Networking → copiar **Public IP**.
3. Abrir `http://IP_PUBLICA:8000/health` → esperar `estado: ok`, `modo: real`.
4. Abrir `http://IP_PUBLICA:8000/docs`.
5. POST /clasificar → **Try it out** → pegar:

```json
{"texto":"No puedo entrar en mi cuenta ficticia"}
```

6. **Execute** → comprobar **200**, modelo y clasificación real.

Solo permite entrar desde nuestra IP. La IP de la tarea puede cambiar.

## 8. Ver logs — web

CloudWatch → **/s16/thepower/api** → stream de la tarea → enseñar arranque de Uvicorn.

## 9. Limpiar — web

1. ECS → servicio → **Update → Desired tasks = 0**.
2. Esperar **cero tareas** y eliminar el servicio.
3. ECR → eliminar **s16-clasificador**, incluidas imágenes y manifiestos sin etiqueta.
4. Security group → eliminar la regla de entrada **8000 / My IP**.
5. Comprobar: **cero tareas/servicios · ECR eliminado · entrada vacía**.

Conservar cluster, rol, secreto, logs y red para repetir. Secreto y logs pueden seguir generando coste.
