# S17 · Comandos de clase en el orden de la presentación

Chuleta para el directo del 17/11 (M/J) y el 23/11 (L/X). Sigue el orden del
Power de 34 diapositivas y reúne **todos los comandos que se ejecutan o se
enseñan**, incluidas las lecturas de AWS que acompañan a las diapositivas de
conceptos. El paso a paso explicado sigue en el [README](../README.md).

Los bloques son Bash (macOS, Linux o Git Bash en Windows) y se ejecutan desde la
carpeta del repositorio, con el entorno virtual activado.

| Marca | Significado |
|---|---|
| 🔍 lectura | Solo consulta AWS. No crea nada ni consume el modelo. |
| 🛠 crea o borra | Crea, actualiza o elimina recursos de tu stack. |
| 💸 inferencia | Llama a Bedrock y consume tokens (si hay cuota). |
| 💻 local | No llama a AWS. |

## 0. Antes de clase (la víspera y 15 minutos antes)

La sesión de `aws login` caduca: renuévala el mismo día. Comprueba la cuota
**antes** de decidir si la demo incluye una clasificación real.

```bash
export AWS_PROFILE=tu-perfil
export AWS_REGION=eu-north-1
export S17_ACCOUNT=123456789012
export S17_STACK=s17-clasificador-tu-nombre
aws login --profile "$AWS_PROFILE" --region "$AWS_REGION"
aws sts get-caller-identity --profile "$AWS_PROFILE" --region "$AWS_REGION"
python cliente.py preflight
```

🔍 `Account` debe coincidir con `S17_ACCOUNT`. El preflight lee identidad,
modelo, las tres cuotas de Nova Lite y la concurrencia de Lambda.

- **Cuotas mayores que cero:** demo completa (apartados 5 a 7).
- **Cuota cero** (última lectura válida: 11/11/2026): recorrido local y lectura
  del [ensayo previo](../ENSAYO.md). No se despliega un stack nuevo ni se
  ejecutan clasificaciones. Se explica el código, se ejecutan las pruebas
  offline y la calculadora, y se muestran como evidencia histórica los
  resultados 200/403/422/503 y la retirada del ensayo.
  [Detalle de la cuota](cuotas-aws.md).

El 16/11 la sesión del perfil del profesor estaba caducada: no se ha podido
releer la cuota. Renueva la sesión y ejecuta el preflight antes de clase.
Si sigue bloqueado, omite los apartados 2 a 6 y 8; en el 7 utiliza solo la
calculadora local. Los comandos de AWS que leen un modelo o una cuota se
pueden enseñar sin afirmar que se hayan ejecutado ese día.

Comprobación rápida en local, sin AWS 💻:

```bash
python -m pytest -q
python preparar.py
```

## 1. Bedrock: catálogo, modelo, modos y cuota · diapositivas 8 a 15

Acompañan a «Qué es Bedrock», «Formas de invocar» y «Nova Lite». Todas son 🔍.

Modelos de texto de Amazon en Estocolmo y su modo de inferencia:

```bash
aws bedrock list-foundation-models \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" \
  --by-provider amazon --by-output-modality TEXT \
  --query 'modelSummaries[].[modelId,join(`,`,inferenceTypesSupported)]' \
  --output table
```

Ficha del modelo de la demo (modalidades, streaming e inferencia admitida):

```bash
aws bedrock get-foundation-model \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" \
  --model-identifier amazon.nova-lite-v1:0 \
  --query 'modelDetails.{id:modelId,entrada:inputModalities,salida:outputModalities,streaming:responseStreamingSupported,inferencia:inferenceTypesSupported}'
```

Disponibilidad en nuestro proyecto (catálogo y autorización, no cuota):

```bash
aws bedrock get-foundation-model-availability \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" \
  --model-id amazon.nova-lite-v1:0
```

Perfiles de inferencia entre regiones que existen en Estocolmo (la demo **no**
los usa):

```bash
aws bedrock list-inference-profiles \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" \
  --query 'inferenceProfileSummaries[].[inferenceProfileId,status]' \
  --output table
```

Las tres cuotas de Nova Lite (solicitudes/minuto, tokens/minuto y tokens/día):

```bash
for q in L-E386A278 L-70423BF8 L-45E0AD92; do
  aws service-quotas get-service-quota \
    --profile "$AWS_PROFILE" --region "$AWS_REGION" \
    --service-code bedrock --quota-code "$q" \
    --query 'Quota.[QuotaCode,QuotaName,Value,Adjustable]' --output text
done
```

Disponible y autorizado no significa que se pueda invocar: si las tres cuotas
valen 0, Bedrock responde `ThrottlingException`.

## 2. Crear el laboratorio · antes de las diapositivas 16 a 22

Solo después de un preflight correcto. Se puede lanzar al empezar el bloque
de Lambda para tener recursos que enseñar.
CloudFormation tarda uno o dos minutos.

```bash
python preparar.py
aws cloudformation deploy \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" \
  --stack-name "$S17_STACK" --template-file .demo-aws/plantilla.json \
  --capabilities CAPABILITY_IAM --tags Project=thepower-s17 Purpose=classroom-demo
python cliente.py estado
```

`preparar.py` es 💻; `deploy` es 🛠; `estado` es 🔍.

Inventario del stack 🔍:

```bash
aws cloudformation describe-stack-resources \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --stack-name "$S17_STACK" \
  --query 'StackResources[].[LogicalResourceId,ResourceType,ResourceStatus]' \
  --output table
```

## 3. Lambda y API Gateway · diapositivas 16 a 20

Acompañan a «Anatomía de una función», «Qué dispara una función» y «La puerta
HTTP». Todas son 🔍.

Configuración de la función (512 MB, 24 s, python3.12, x86_64, rol y variables):

```bash
aws lambda get-function-configuration \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --function-name "$S17_STACK" \
  --query '{runtime:Runtime,handler:Handler,memoriaMB:MemorySize,timeoutS:Timeout,arquitectura:Architectures[0],rol:Role,variables:Environment.Variables}'
```

Concurrencia del proyecto (diez compartidas en el aula):

```bash
aws lambda get-account-settings \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" \
  --query 'AccountLimit.{total:ConcurrentExecutions,sinReservar:UnreservedConcurrentExecutions}'
```

Identificador de la API, rutas con `AWS_IAM`, integración y límite de ritmo:

```bash
API_ID=$(aws cloudformation describe-stacks \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --stack-name "$S17_STACK" \
  --query "Stacks[0].Outputs[?OutputKey=='ApiId'].OutputValue" --output text)
aws apigatewayv2 get-routes \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --api-id "$API_ID" \
  --query 'Items[].[RouteKey,AuthorizationType]' --output table
aws apigatewayv2 get-integrations \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --api-id "$API_ID" \
  --query 'Items[].[IntegrationType,PayloadFormatVersion,TimeoutInMillis]' --output table
aws apigatewayv2 get-stage \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --api-id "$API_ID" \
  --stage-name '$default' --query DefaultRouteSettings
```

Resultado esperado: dos rutas `AWS_IAM`, integración `AWS_PROXY` con payload
2.0 y 29.000 ms, y ritmo 1 solicitud/s con ráfaga 1.

## 4. IAM y CloudWatch · diapositivas 21 y 22

Los tres permisos del recorrido. Todas son 🔍.

Permiso 2 · API Gateway puede invocar la función (política de recurso):

```bash
aws lambda get-policy \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --function-name "$S17_STACK" \
  --query Policy --output text
```

Permiso 3 · la función puede invocar el modelo (rol de ejecución). IAM es
global, así que no lleva región:

```bash
ROL=$(aws cloudformation describe-stack-resources \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --stack-name "$S17_STACK" \
  --logical-resource-id RolLambda \
  --query 'StackResources[0].PhysicalResourceId' --output text)
aws iam get-role-policy --profile "$AWS_PROFILE" \
  --role-name "$ROL" --policy-name modelo-y-logs --query PolicyDocument
```

Debe aparecer `bedrock:InvokeModel` sobre un único modelo de Estocolmo. El
permiso 1 (`execute-api:Invoke` del cliente) depende de tu identidad: se
comprueba con una petición firmada admitida. La salud 200 acredita la ruta
GET y la validación 422 acredita la ruta POST sin consumir el modelo. El 403
sin firma demuestra el rechazo de llamadas anónimas; por sí solo no prueba
que el llamante tenga permiso.

Logs de la función y del gateway (retención de tres días):

```bash
aws logs tail "/aws/lambda/$S17_STACK" \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --since 30m --format short
aws logs tail "/s17/$S17_STACK/http" \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --since 30m --format short
```

## 5. Medir · diapositiva 24 (solo con cuota)

Antes de llamar a `/health`, para tener opción de capturar un frío. Máximo seis
clasificaciones secuenciales; se detiene en el primer fallo.

```bash
python cliente.py medir --execute
python cliente.py logs
```

`medir` es 💸; `logs` es 🔍 y se puede repetir sin consumir el modelo.

Líneas REPORT con `Init Duration` y `Billed Duration` 🔍:

```bash
aws logs filter-log-events \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" \
  --log-group-name "/aws/lambda/$S17_STACK" --filter-pattern REPORT \
  --query 'events[].message' --output text
```

## 6. Probar salud, IAM y validación · diapositiva 24

Ninguna de las tres llama al modelo. Esperado: **200**, **403** y **422**; las
dos últimas terminan con código 1 porque comprueban un rechazo.
Deja al menos 1,1 segundos entre peticiones para respetar el ritmo 1/s.

```bash
python cliente.py probar --health --execute
python cliente.py probar --sin-firma --execute
python cliente.py probar --texto "" --execute
```

Una clasificación adicional 💸, solo con cuota y si no se ha ejecutado el
lote de seis. No forma parte de las pruebas anteriores. Con cuota cero no
la ejecutes: enseña el 503 `bedrock_sin_cuota_o_limitado` del ensayo previo.

```bash
python cliente.py probar --texto "Me han cobrado dos veces una factura ficticia" --execute
```

## 7. Coste · diapositivas 12 y 29

Estimación de 1.000 solicitudes con supuestos 💻 (0,05722 USD de coste parcial):

```bash
python coste.py
```

Con las mediciones reales de la clase, si existen:

```bash
python coste.py --mediciones .demo-aws/mediciones.json --fraccion-fria 0.05
```

Tokens que Bedrock ha contado para el modelo 🔍. Las horas van en UTC: las
18:30 de Madrid en noviembre son las 17:30 UTC. Cambia la fecha por la de tu
grupo.

```bash
aws cloudwatch get-metric-statistics \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" \
  --namespace AWS/Bedrock --metric-name InputTokenCount \
  --dimensions Name=ModelId,Value=amazon.nova-lite-v1:0 \
  --start-time 2026-11-17T17:00:00Z --end-time 2026-11-17T19:00:00Z \
  --period 3600 --statistics Sum
```

Repite con `--metric-name OutputTokenCount` para los tokens de salida.

## 8. Retirar · antes del cierre

Comprueba que `$S17_STACK` es solo tu demo 🛠:

```bash
aws cloudformation delete-stack \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --stack-name "$S17_STACK"
aws cloudformation wait stack-delete-complete \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --stack-name "$S17_STACK"
aws cloudformation describe-stacks \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --stack-name "$S17_STACK"
```

La última lectura debe decir que el stack no existe. Los consumos anteriores
pueden aparecer en la factura más tarde.

## Si algo falla

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `Your session has expired` | Sesión de `aws login` caducada | `aws login --profile "$AWS_PROFILE" --region "$AWS_REGION"` |
| `Account` distinto de `S17_ACCOUNT` | Perfil equivocado | Corrige `AWS_PROFILE` antes de crear nada |
| Preflight con cuota 0 | Cuota de Nova Lite sin habilitar | Demo de infraestructura; ver [cuotas](cuotas-aws.md) |
| `AccessDenied` en algo que antes funcionaba | Permisos o límite de gasto del proyecto | Revisa AWS Settings → Billing |
| 403 con firma | Falta `execute-api:Invoke` en tu identidad | Lo concede el administrador del laboratorio |
| 503 `bedrock_sin_cuota_o_limitado` | Bedrock limita o la cuota es 0 | No repetir; enseñar el log |
| `logs` sin REPORT | Los logs aún no han llegado | Esperar y repetir solo `python cliente.py logs` |
