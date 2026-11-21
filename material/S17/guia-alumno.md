# Guía del alumno S17

**Guía histórica del paquete avanzado.** Para la clase actual utiliza el
[README de la demo sencilla en eu-north-1](demo-bedrock/README.md).
Los pasos de ZIP/S3, perfil europeo y reserva que siguen no corresponden al aula actual.

## 1. Punto de partida y modos de trabajo

Usa el paquete de referencia para ejecutar el recorrido guiado. El paquete de inicio contiene la base de API y contratos para construir tu solución; no contiene la infraestructura resuelta. Los comandos siguientes se ejecutan desde la raíz del proyecto de referencia, donde están `pyproject.toml` y `scripts/`.

Necesitas Python 3.12 y uv. Docker Desktop permite construir y ensayar el paquete Lambda en Linux amd64. Para AWS necesitas una identidad temporal del laboratorio, región europea, cuenta esperada, permiso de preparación de recursos y acceso al perfil de Bedrock. No uses claves de otros proyectos.

Hay tres evidencias distintas: la demo prueba lógica con un doble; RIE prueba el contrato del runtime Lambda local; AWS prueba IAM, firma aceptada, modelo real, latencia y recursos desplegados. Completar la demo no sustituye la práctica real.

## 2. Instalar y probar sin gasto

```bash
uv sync --frozen --all-extras
uv run pytest
uv run python scripts/demo_s17.py
uv run python -m scripts.aws_s17 plan
uv run cfn-lint infra/s17/*.json
```

Esperado: pruebas correctas, demo con `execution: demo`, respuesta de `facturacion`, error 422 para entrada vacía y tokens nulos. `plan` no lee credenciales ni llama a AWS. El código de cuenta se ejecuta como módulo (`python -m scripts.aws_s17`) para reutilizar las operaciones de la base común.

Lee en este orden: `contratos.py`, `serverless/config.py`, `bedrock.py`, `handler.py`, `firma.py` y `evidencia.py`. La entrada conserva `texto`; la salida conserva `categoria`, `prioridad` y `respuesta`. El modelo no decide los metadatos de medición.

## 3. Entender la estructura y los errores

`request_for` prepara Converse con `modelId`, mensajes, `maxTokens=300` y `toolConfig`. Nova 2 admite seleccionar una herramienta concreta mediante `toolChoice.tool`. Aquí `emitir_clasificacion` es un esquema de salida: no ejecuta una acción de negocio ni requiere una segunda llamada al modelo.

Lambda comprueba `stopReason`, nombre/número de herramientas y el esquema Pydantic. Una salida inválida produce 502; no se repara, reintenta o reemplaza por la demo. Las credenciales de Bedrock proceden del rol de Lambda; no se copia una API key de Anthropic de S16.

| Situación | Resultado esperado | ¿Se llama a Bedrock? |
|---|---|---|
| Cuerpo vacío, campos extras o texto inválido | 422 | No |
| JSON/base64 mal formado | 400 | No |
| Content-Type distinto de JSON | 415 | No |
| Cuerpo mayor de 8 KiB | 413 | No |
| Menos de 20 s de margen antes de empezar | 504 controlado | No |
| Bedrock limita solicitudes | 503 | Hubo un intento; no se repite |
| Timeout de Bedrock | 504 | Un intento; gasto posible aunque no haya respuesta |
| Permisos de Bedrock o salida inválida | 502 saneado | Un intento |

La falta de firma produce 403 en **API Gateway**, antes de Lambda. No se demuestra con un test que solo invoque el handler.

## 4. Construir el ZIP y ensayar Lambda local

```bash
uv run python scripts/build_lambda_s17.py
```

El script utiliza una imagen oficial Lambda Python 3.12 fijada por digest, instala dependencias con hashes en Linux amd64, comprueba imports y crea `.build/s17/lambda-s17.zip`. El manifiesto `package.json` guarda hash, versión, arquitectura, tamaños y límites de evidencia. No incluye FastAPI ni uvicorn en el runtime Lambda: solo contratos, código serverless, Pydantic y SDK.

Para ejecutar RIE, el emulador oficial incluido en la imagen:

```bash
docker run --rm --detach --name thepower-s17-rie --platform linux/amd64 \
  -p 127.0.0.1:9017:8080 thepower-s17:build \
  curso_ia.serverless.local_handler.lambda_handler
uv run python scripts/ensayo_s17.py
docker stop thepower-s17-rie
```

La entrada local se llama `local_handler` de forma explícita. La plantilla AWS despliega `handler.lambda_handler`, que usa Bedrock real. El ensayo espera `statusCode: 200` y `422` dentro del contrato proxy. RIE puede devolver HTTP 200 para transportar una ejecución cuyo resultado interno es 422; API Gateway es quien convierte ese resultado al HTTP de la API final.

El recibo queda en `evidencias/local/s17-rie.json`. RIE no acredita IAM, regiones de inferencia, escalado, facturación ni cold start de AWS.

## 5. Configurar identidad y comprobar perfil/cuota

Si la cuenta del laboratorio usa SSO y el perfil ya está preparado:

```bash
aws sso login --profile curso-s17
S17_PROFILE=curso-s17
S17_REGION=eu-west-1
S17_ACCOUNT=123456789012
S17_LAB=s17-mi-nombre
S17_ARGS=(--profile "$S17_PROFILE" --region "$S17_REGION"
  --cuenta "$S17_ACCOUNT" --lab "$S17_LAB")
uv run python -m scripts.aws_s17 preflight "${S17_ARGS[@]}"
```

Sustituye la cuenta de ejemplo. Los comandos comparan la identidad STS con la cuenta esperada. El perfil, nombres y credenciales deben pertenecer a este laboratorio, no a otro producto.

El preflight lee `GetInferenceProfile` para la referencia europea y sus modelos. Rechaza respuestas de otra cuenta, perfil o destinos no europeos. Construye la lista de modelos de origen/destino que necesita IAM; no usa `Resource: *` para permitir todos los modelos.

También comprueba la cuota de concurrencia. La referencia reserva dos ejecuciones y AWS exige dejar cien sin reservar. En una primera creación se necesitan al menos 102 disponibles en ese conjunto. Si la cuenta tiene una cuota inicial menor, pide una cuenta/cuota de laboratorio adecuada; no retires el límite silenciosamente para que el despliegue pase.

Esta lectura no acredita permisos efectivos de inferencia, disponibilidad de cuota de tokens ni una llamada real. Conserva `preflight-s17.json` y comprueba el funcionamiento después del despliegue. Si se necesita otro modelo, debe ser una elección explícita, con compatibilidad, permisos y tarifas revisadas; no una sustitución automática por un perfil global.

## 6. Publicar el artefacto y desplegar

Estas operaciones crean recursos facturables. Ejecútalas únicamente dentro del destino y presupuesto autorizados del laboratorio.

```bash
uv run python -m scripts.aws_s17 bootstrap "${S17_ARGS[@]}" --execute
uv run python -m scripts.aws_s17 subir "${S17_ARGS[@]}" --execute
uv run python -m scripts.aws_s17 desplegar "${S17_ARGS[@]}" --execute
uv run python -m scripts.aws_s17 estado "${S17_ARGS[@]}"
```

El primer stack crea un bucket privado, cifrado y versionado para el ZIP. `subir` verifica su hash, usa una clave de contenido y lee el checksum de vuelta. El segundo stack crea logs, rol, función, versión publicada, alias `aula`, HTTP API, integración y ruta IAM. S3 contiene un artefacto de despliegue; no datos de alumnos.

La función usa Python 3.12 x86_64, 512 MiB, 24 s y concurrencia reservada 2. La integración espera hasta 29 s y la ruta limita el ritmo. Se comprueba el código SHA-256 de la versión a la que apunta el alias, la configuración real, la ruta IAM y su integración. Un stack verde no sustituye una petición funcional.

## 7. Autorizar al llamante y firmar

```bash
uv run python -m scripts.aws_s17 politica-cliente "${S17_ARGS[@]}"
```

El archivo generado contiene `execute-api:Invoke` sobre el ARN exacto de `POST /clasificar` en `$default`. El administrador del laboratorio lo incorpora a la identidad temporal prevista. El comando no modifica usuarios ni roles existentes.

Hay tres comprobaciones: el cliente firma y tiene permiso para la ruta; API Gateway tiene permiso de invocar el alias Lambda; el rol de Lambda tiene `bedrock:InvokeModel` sobre el perfil y los modelos. `bedrock:Converse` no es la acción IAM que se concede.

El cliente usa la cadena de credenciales del SDK, exige session token, firma con servicio `execute-api` y región correcta y envía exactamente los bytes firmados por HTTPS. No imprime Authorization, access key, secret key ni token. Una firma aporta autenticidad/integridad; TLS protege el transporte. No copies credenciales a un comando visible en pantalla.

## 8. Medir primero y verificar después

Si quieres tener la oportunidad de observar un cold start del despliegue nuevo, mide antes de hacer llamadas de calentamiento:

```bash
uv run python -m scripts.aws_s17 medir "${S17_ARGS[@]}" --execute
uv run python -m scripts.aws_s17 logs "${S17_ARGS[@]}"
uv run python -m scripts.aws_s17 verificar "${S17_ARGS[@]}" --execute
```

`medir` hace **como máximo seis clasificaciones reales**, secuenciales y sin reintentos. Conserva cada intento y se detiene ante un fallo. No ejecuta llamadas hasta que aparezca un cold start. `logs` solo relee CloudWatch; se puede usar después si los REPORT aún no habían llegado.

`verificar` hace una petición sin firma (403), una firmada inválida (422, sin modelo) y una clasificación válida (una inferencia). El ciclo completo descrito hace hasta siete inferencias reales, además de las pruebas sin modelo. No hay permiso implícito para repetir lotes sin mirar el consumo.

`mediciones-s17.json` conserva el estado HTTP, duración total del cliente, respuesta, request ID, duración del handler, duración del paso de modelo, tokens y errores. Los originales fechados se mantienen; el nombre corto apunta a la última lectura.

## 9. Interpretar cold, warm y tiempos

| Dato | Qué mide |
|---|---|
| `http_duration_ms` | Cliente a respuesta; incluye red y recorrido completo |
| `duration_ms` de metadata | Trabajo dentro del handler; no la inicialización previa |
| `model_duration_ms` | Paso del SDK de Bedrock observado por la aplicación |
| `provider_latency_ms` | Latencia informada por Bedrock, si existe |
| `Init Duration` | Inicialización confirmada por el REPORT asociado al request ID |
| `Billed Duration` | Duración facturable de Lambda; no sumes Init otra vez |

`first_in_environment` es una pista de primera ejecución del proceso. El resumen solo marca cold confirmado cuando encuentra `Init Duration`. Una petición con entorno reutilizado se cuenta como warm. Se requieren al menos cinco warm; si el lote no los alcanza, se conserva como incompleto. Si no se observa cold, se declara `no_capturado`.

No extrapoles que un sexto de las llamadas de producción serán frías porque una de seis lo fue en el ensayo. No compares modelos o arquitecturas a partir de una muestra tan pequeña sin declarar sus condiciones.

S16 usaba Anthropic directamente y esta referencia usa Nova en Bedrock. El contrato es común, pero una diferencia de latencia o coste no puede atribuirse solo a Fargate frente a Lambda: también cambia el modelo/proveedor. Para una comparación de arquitectura, mantén iguales modelo, entrada y parámetros.

Los límites de la referencia son: 8 KiB de cuerpo, 2.000 caracteres, 300 tokens de salida, un intento total del SDK, conexión 2 s, lectura 15 s, Lambda 24 s, integración 29 s y cliente 35 s. Antes del SDK se exige margen de 20 s considerando también el tiempo transcurrido desde la entrada en API Gateway. La inicialización fría consume parte del plazo HTTP.

El enunciado advierte de no dejar Lambda en el valor predeterminado de tres segundos: la plantilla fija explícitamente 24 s. Ampliar ese valor no amplía el plazo independiente del gateway.

## 10. Estimar 1.000 peticiones

```bash
uv run python scripts/costes_s17.py
# Con un lote real y REPORT completos:
uv run python scripts/costes_s17.py \
  --mediciones "evidencias/aws/$S17_LAB/mediciones-s17.json"
# Si no hubo cold, escenario explícito de solo peticiones calientes:
uv run python scripts/costes_s17.py \
  --mediciones "evidencias/aws/$S17_LAB/mediciones-s17.json" --fraccion-fria 0
```

La calculadora no ejecuta peticiones. El ejemplo utiliza 512 MiB, 1.500 ms facturados warm, 1.800 ms cold, frecuencia fría hipotética del 5%, 250 tokens de entrada y 100 de salida. Con las tarifas estándar de Irlanda leídas el 17/10/2026, más los supuestos de logs, tráfico y almacenamiento del ZIP, da **0,4249 USD**. Es una estimación, no una factura ni una medición del laboratorio.

Con mediciones reales exige cinco warm, REPORT, memoria coherente y tokens disponibles. La frecuencia de frío, logs, tráfico y retención del artefacto siguen siendo supuestos que debes justificar. Si no hay cold confirmado, no inventa su duración. Si la muestra utiliza caché, hay que incorporar sus tarifas antes de estimar. Los descuentos, impuestos, créditos y tramos gratuitos no se presuponen disponibles.

## 11. Alternativas y limpieza

Compara Lambda + Bedrock con Azure Functions + Foundry y Cloud Run functions + Vertex AI. Son correspondencias funcionales, no garantías de igualdad de cuotas o precios. Fargate puede convenir para un proceso continuo o carga sostenida; los trabajos asíncronos permiten separar tareas largas del tiempo de una petición HTTP. Streaming necesita un transporte y permisos compatibles; no se activa automáticamente al usar `ConverseStream`.

```bash
uv run python -m scripts.aws_s17 limpiar "${S17_ARGS[@]}" --execute
```

La retirada comprueba las etiquetas de los stacks y del bucket. Elimina API/integración/ruta, función/alias/versiones, rol y logs; después retira todas las versiones y delete markers del bucket propio y su stack. Las identidades y permisos externos del llamante se conservan: el administrador revisa la política que ya no se necesita.

Revisa el inventario final en Lambda, API Gateway, CloudWatch, CloudFormation y S3. No existe un modelo Bedrock propio que haya que eliminar. Si añadiste alarmas, capas, provisioned concurrency u otros recursos, incorpóralos al inventario y al cálculo. Un consumo ya generado puede aparecer después en facturación.

## 12. Diagnóstico y ayuda

403 sin firma es esperado. 403 con firma exige revisar expiración/token, región, servicio de firma, bytes y permiso sobre la ruta. 502 con `bedrock_denegado` corresponde al rol/perfil/regiones de Bedrock, no al permiso del cliente sobre la API. 503 indica limitación; no repetir en bucle. 504 puede ser el margen agotado antes del modelo o un timeout del SDK; cruza request ID, tiempo total y REPORT.

Si el ZIP no importa en Lambda, revisar runtime/arquitectura y dependencias nativas; no subir las librerías de macOS. Si los REPORT faltan, releer logs sin repetir inferencia. Si falla el despliegue o la limpieza, revisar el recurso concreto y el estado antes de reintentar.

Para pedir ayuda: proporciona sistema operativo, comando saneado, versiones, código de error, región, capa implicada y resultado esperado. Omite tokens, Authorization, claves, cookies, `.env` y cuerpos con datos personales. Pide una comprobación de solo lectura antes de cambios.
