# Arquitectura y decisiones de S17

El flujo es cliente SigV4 → HTTP API AWS_IAM → alias de Lambda Python → Converse de Bedrock → validación del contrato → JSON. Reutiliza `Incidencia` y `Clasificacion` de S16. La API FastAPI de S16 y sus materiales conservan su comportamiento; no se instala FastAPI en el paquete Lambda.

## Código y despliegue

El paquete incluye Pydantic y SDK fijados y se construye en Linux amd64 con el runtime oficial Lambda. Dos stacks separan el bucket de artefactos del servicio. La carga verifica SHA-256 y versión de objeto. Lambda publica una versión y la integración usa el alias `aula`.

La identidad de despliegue depende del hash del ZIP, la selección de perfil y la plantilla. También cambia cuando se modifica configuración con el mismo código; así CloudFormation publica una nueva versión en lugar de dejar el alias en una configuración anterior. `CodeSha256` conserva la identidad independiente del artefacto. La comprobación de estado lee versión, configuración y ruta de vuelta.

## Identidad y límites

No hay API key de modelo dentro del ZIP. El rol de Lambda obtiene credenciales temporales del runtime. Permite `bedrock:InvokeModel` sobre el perfil y los modelos europeos leídos de AWS, con condición del perfil para los modelos. El llamante y API Gateway tienen permisos distintos. El CLI reutiliza la verificación STS/etiquetas/recibos de la base común, con prefijo `s17-` e infraestructura separada de `s16-`.

Cliente 35 s, integración 29 s, Lambda 24 s, SDK 2 s de conexión/15 s de lectura y un intento total. El handler exige al menos 20 s de margen considerando contexto Lambda y tiempo de recepción del gateway. Entrada 8 KiB/2.000 caracteres, salida 300 tokens y concurrencia reservada 2. Rutas de tiempo/error no reparan ni repiten llamadas.

## Evidencia y costes

La primera ejecución del entorno es una pista de proceso, no una medición de Init Duration. El resumen confirma frío mediante REPORT, cuenta entornos reutilizados y conserva cobertura y errores. La lectura de logs no vuelve a invocar el modelo.

La calculadora separa cantidades supuestas y medidas, no ejecuta 1.000 llamadas y no sustituye errores o tokens ausentes por cero. Billed Duration no se incrementa otra vez con Init Duration. La frecuencia de frío no se infiere de la muestra pequeña.

## Límites de esta entrega

Demo local y RIE acreditan lógica, empaquetado y contrato de runtime. IAM aceptado, permisos efectivos, Bedrock real, cuotas, cold/warm AWS y retirada cloud requieren el ensayo autorizado de cuenta. Streaming es opcional y no está implementado. No se han creado recursos AWS ni hecho inferencias reales durante la preparación.

OpenViking sigue sin una cuenta mapeada para el repositorio. La entrega de memoria se conserva localmente, sin atribuirla a otro tenant.
