# Despliegue en AWS (ECS Fargate + RDS PostgreSQL)

> **No ejecutado.** Esta guía y `infra/plantilla.json` no se han probado en una cuenta de AWS.
> La plantilla pasa `cfn-lint` sin avisos y la imagen se ha construido y arrancado en local.
> Desplegar **crea recursos de pago**: hazlo solo con un presupuesto fijado y borra todo al
> terminar. En el directo no se despliega salvo que el profesor lo haya preparado antes.

## Qué crea la plantilla

| Recurso | Para qué | Nota |
|---|---|---|
| VPC, subred pública y dos subredes de datos | Red propia del laboratorio | Sin NAT ni balanceador |
| Grupo de seguridad del agente | Entrada al puerto 8020 **solo desde tu IP /32**; salida 443 | Y salida 5432 solo hacia la base |
| Grupo de seguridad de datos | PostgreSQL solo acepta al agente | La base no tiene IP pública |
| RDS PostgreSQL `db.t4g.micro` | Memoria, fragmentos y trabajos | Contraseña gestionada por RDS en Secrets Manager |
| ECS Fargate: una tarea con dos contenedores | `api` (uvicorn) y `ejecutor` (investigaciones) | La misma imagen, distinto comando |
| CloudWatch Logs | Una línea JSON por turno | Retención de tres días |
| Roles IAM | Arranque del contenedor y lectura de los secretos | El rol de tarea no tiene permisos |

El servidor MCP no se despliega aparte: es un subproceso (stdio) dentro del contenedor `api`.

## Qué cambia respecto a local y qué no

| | Local | AWS |
|---|---|---|
| Código e imagen | Los mismos | Los mismos (imagen por digest) |
| Configuración | `.env` o variables | Variables de la tarea |
| Contraseña de la base | Ficticia en `compose.yaml` | Secrets Manager, inyectada como `S20_DB_PASSWORD` |
| Clave del modelo | Variable local | Secrets Manager (solo perfil real) |
| PostgreSQL | Contenedor en tu portátil | RDS privado |
| Logs | Terminal | CloudWatch Logs |
| Tokens de laboratorio | Los del ejemplo | **Otros**, propios (parámetro `Usuarios`) |

## Pasos

Sustituye `<…>` por tus valores. Usa tu Región asignada en todos los comandos.

```bash
LAB=s20-<tu-nombre>
REGION=<tu-region>
CUENTA=$(aws sts get-caller-identity --query Account --output text)

# 1. Repositorio de imágenes y publicación (la arquitectura debe ser linux/amd64)
aws ecr create-repository --repository-name "$LAB" --region "$REGION"
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$CUENTA.dkr.ecr.$REGION.amazonaws.com"
docker build --platform linux/amd64 -t "$CUENTA.dkr.ecr.$REGION.amazonaws.com/$LAB:v1" .
docker push "$CUENTA.dkr.ecr.$REGION.amazonaws.com/$LAB:v1"
DIGEST=$(aws ecr describe-images --repository-name "$LAB" --image-ids imageTag=v1 --region "$REGION" --query 'imageDetails[0].imageDigest' --output text)

# 2. Versión de PostgreSQL disponible en tu Región (elige una 17.x de la lista)
aws rds describe-db-engine-versions --engine postgres --region "$REGION" --query 'DBEngineVersions[].EngineVersion' --output text

# 3. Crear la pila (RDS tarda varios minutos)
aws cloudformation deploy --region "$REGION" --stack-name "$LAB" \
  --template-file infra/plantilla.json --capabilities CAPABILITY_IAM \
  --parameter-overrides Lab="$LAB" \
    ImageUri="$CUENTA.dkr.ecr.$REGION.amazonaws.com/$LAB@$DIGEST" \
    AllowedCidr="$(curl -s https://checkip.amazonaws.com)/32" \
    VersionPostgres="<17.x>" \
    Usuarios="<token-largo-1>:ana,<token-largo-2>:luis"

# 4. IP pública de la tarea y comprobación
TAREA=$(aws ecs list-tasks --cluster "$LAB" --region "$REGION" --query 'taskArns[0]' --output text)
ENI=$(aws ecs describe-tasks --cluster "$LAB" --tasks "$TAREA" --region "$REGION" --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text)
IP=$(aws ec2 describe-network-interfaces --network-interface-ids "$ENI" --region "$REGION" --query 'NetworkInterfaces[0].Association.PublicIp' --output text)
curl -s "http://$IP:8020/health"
```

La primera vez hay que crear el índice dentro de la tarea (o desde un equipo con acceso a la
base): `python -m agente.cli ingestar`. Con ECS Exec activado se puede lanzar en el contenedor;
la plantilla no lo activa.

## Limpieza

```bash
aws cloudformation delete-stack --stack-name "$LAB" --region "$REGION"
aws cloudformation wait stack-delete-complete --stack-name "$LAB" --region "$REGION"
aws ecr delete-repository --repository-name "$LAB" --force --region "$REGION"
```

La pila borra la base con sus copias automáticas y el secreto que creó RDS. El repositorio
ECR y el secreto de la clave del modelo (si creaste uno) se borran aparte.

## Avisos

- **HTTP sin TLS.** La API queda en `http://IP:8020`, accesible solo desde tu IP. Es un
  laboratorio: en producción va detrás de un balanceador con HTTPS.
- **Coste.** Fargate, RDS, almacenamiento, Secrets Manager y logs facturan mientras existan.
  No se incluye una estimación: consulta la [calculadora de AWS](https://calculator.aws/) para tu
  Región y borra la pila al terminar.
- **Copias de seguridad.** Retención de un día y borrado con la instancia: adecuado para una
  práctica, no para datos que importen.
- **pgvector en RDS.** `esquema.sql` ejecuta `CREATE EXTENSION vector` con el usuario maestro.
  No se ha comprobado en RDS en esta preparación.
