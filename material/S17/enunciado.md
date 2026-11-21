# S17 Construir una API de IA serverless con AWS Bedrock

**Enunciado vigente, práctica opcional:** [ejercicio adaptado a la demo](demo-bedrock/docs/ejercicio.md).
El texto que sigue conserva la referencia enviada en septiembre. La aclaración
de Laura del 04/11 prevalece sobre «trabajo obligatorio»; la adaptación actual
usa Nova Lite directo en eu-north-1 y la cuota compartida real del proyecto.

Referencia: ejercicio redactado por José y enviado el 28/09/2026 en `AI_Engineer_enunciados.docx`, página 6. La guía desarrolla ese encargo; las decisiones de empaquetado y alias son preparación local.

## Trabajo obligatorio

Crear un endpoint HTTP que reciba una incidencia ficticia, la valide en Lambda e invoque Bedrock con el SDK de AWS. Devolver categoría, prioridad y respuesta JSON. Utilizar **API Gateway HTTP API con autorización IAM**. Configurar `BEDROCK_MODEL_ID`; la referencia europea es `eu.amazon.nova-2-lite-v1:0`. No sustituirla por un perfil global sin justificar el lugar de procesamiento.

Autorizar Converse mediante `bedrock:InvokeModel`, no `bedrock:Converse`. Limitar el rol de Lambda al perfil y modelo base de las regiones de destino. El llamante necesita `execute-api:Invoke` sobre la ruta y debe firmar con SigV4, usando credenciales temporales sin guardarlas en el repositorio.

Pedir una estructura mediante `toolConfig` o una salida estructurada compatible y validarla de nuevo en Lambda. Limitar entrada, tokens, reintentos y concurrencia. Ajustar timeouts de cliente y Lambda para manejar el error antes del corte de API Gateway. S8 medía al modelo sin ayudas de formato; aquí la robustez del servicio es el objetivo.

Registrar tiempo total, tiempo del modelo, tokens y errores. Identificar un cold start con `Init Duration` o evidencia equivalente y compararlo con **al menos cinco peticiones calientes**. Si no se captura un arranque frío, declararlo; la primera petición del cliente no es una prueba suficiente.

Estimar **1.000 peticiones sin ejecutarlas**, incluyendo duración/memoria de Lambda, solicitudes de API Gateway, tokens de Bedrock y logs relevantes. Indicar región, tarifas y supuestos. Explicar alternativas en Azure y Google Cloud y cuándo cambiar de arquitectura por latencia, timeouts, streaming o tráfico sostenido.

## Entrega y valoración

Código y configuración reproducibles, petición válida, errores controlados, medidas, cálculo de coste y limpieza de recursos. Se valora autenticación, permisos, JSON validado y análisis con datos observados. Dedicación orientativa: **4–6 horas activas con accesos preparados**, fuera del directo.

Streaming es una ampliación opcional si el modelo y el transporte lo admiten, con permisos y límites propios. La implementación de referencia de este paquete es no streaming; no se presenta ese extra como completado.

