# Cobertura de S17

## Demo sencilla vigente · 11/11/2026

El recorrido actual es [demo-bedrock](demo-bedrock/README.md). Conserva el caso
de soporte, HTTP API con IAM, Lambda/SDK, salida validada, firma temporal,
límites, cold/warm, costes, alternativas y limpieza. Adapta explícitamente el
modelo a Nova Lite directo en eu-north-1 y utiliza la cuota compartida real sin reserva.

| Requisito | Ubicación actual | Evidencia |
|---|---|---|
| Serverless, Bedrock y Lambda | Power 3–11 y README | Código, recursos y configuración observados |
| IAM y petición firmada | Power 12–16, plantilla y cliente | Salud 200, sin firma 403, entrada vacía 422 |
| JSON y límites | lambda_function.py y Power 10, 19–20 | Tests de contrato, SDK y error sin fallback |
| Cold/warm y tokens | Power 17–18, cliente y README | Instrumentación probada; lote exitoso pendiente de cuota |
| Coste de 1.000 peticiones | Power 21/26, coste.py y tarifas.json | Cálculo offline y catálogo de Estocolmo |
| Azure/Google y elección | Power 22–23 y README | Comparación conceptual |
| Práctica opcional | Power 24 y docs/ejercicio.md | Enunciado simplificado y cambios explícitos |
| Limpieza | README paso 8 | Stack, API, función, rol y logs del ensayo ausentes |

La cuota cero impide acreditar clasificación real y cinco warm. El error 503
ensayado y los tests con Stubber no completan esos requisitos.

## Matriz del paquete avanzado anterior · histórica

Los **30 puntos obligatorios de comprobación** se derivan del temario y del ejercicio original. La división en IDs es una herramienta de revisión, no una ampliación de los requisitos de la escuela. Cada punto se localiza en presentación, guion y código/procedimiento. Streaming se registra aparte como opcional.

Fuente original: `docs/fuentes/temario-ai-engineer.txt` y `docs/fuentes/S17-ejercicio-original.txt`. T = temario; E = ejercicio; O = opcional.

| ID | Requisito | Slides | Bloque del guion | Evidencia y límite |
|---|---|---|---|---|
| T01 | AWS Bedrock: modelos y API gestionada | 3, 6, 9 | Serverless y alternativas; Handler e identidades | Explicado; disponibilidad real pendiente |
| T02 | AWS Lambda: evento, contexto y ciclo de ejecución | 3, 4, 10, 15, 16 | Serverless y alternativas; Medir frío y caliente | Handler y RIE locales verificados |
| T03 | Arquitectura serverless y responsabilidades | 3, 4, 14 | Serverless y alternativas | Explicación y plantillas |
| T04 | Alternativas Azure y Google Cloud | 5, 19 | Serverless y alternativas; Coste y alternativas | Comparación funcional y criterios |
| T05 | Coste | 17, 18, 19 | Coste, alternativas y retirada | Tarifas leídas y calculadora ejecutada; cantidades supuestas |
| T06 | Latencia | 11, 15, 16 | Límites y errores; Medir frío y caliente | Instrumentación y parser probados; muestra AWS pendiente |
| T07 | Límites de arquitecturas y elección | 11, 12, 19 | Límites y errores; Coste y alternativas | Plazos, cuotas, streaming y carga sostenida explicados |
| E01 | HTTP API IAM → Lambda → Bedrock | 3, 7, 14 | Handler e identidades; Petición firmada | Plantilla validada; flujo real pendiente |
| E02 | SDK de AWS en Lambda | 9, 10 | Handler e identidades | Petición validada con Stubber y paquete Linux |
| E03 | BEDROCK_MODEL_ID y referencia eu.amazon.nova-2-lite-v1:0 | 6 | Handler e identidades | Configuración y perfil esperado explícitos |
| E04 | No sustituir por perfil global sin justificación | 6, 21 | Handler e identidades | Guardas europeas y error sin fallback |
| E05 | Converse se autoriza con bedrock:InvokeModel | 7, 21 | Handler e identidades | Acción correcta en política y explicación |
| E06 | Permisos sobre perfil y modelos/regiones de destino | 6, 7, 21 | Handler e identidades | ARNs desde GetInferenceProfile; prueba local de validación |
| E07 | Llamante con execute-api:Invoke sobre la ruta | 7, 8, 21 | Petición firmada | Política específica generable; asignación externa pendiente |
| E08 | SigV4 con credenciales temporales, sin guardarlas | 8, 22 | Petición firmada | Firma local probada; aceptación IAM pendiente |
| E09 | Solicitar estructura y validar de nuevo | 9, 10, 13 | Handler e identidades; Límites y errores | Tool forzada y Pydantic; errores probados |
| E10 | Acotar entrada | 10, 12, 13 | Límites y errores | 8 KiB/2000 caracteres y rechazo antes del SDK |
| E11 | Acotar tokens | 9, 12 | Límites y errores | 300 por configuración de la referencia |
| E12 | Acotar reintentos | 12, 13 | Límites y errores | Un intento SDK; fallos sin repetición |
| E13 | Acotar concurrencia | 4, 12 | Límites y errores | Reserva 2 y preflight de cuota; aplicación AWS pendiente |
| E14 | Timeout cliente/Lambda antes del corte del gateway | 11 | Límites y errores | 35/29/24 y SDK 2/15; margen probado localmente |
| E15 | Registrar total, modelo, tokens y errores | 10, 15, 16 | Medir frío y caliente | Metadatos y recibos implementados; reales pendientes |
| E16 | Identificar cold start con evidencia | 15, 16 | Medir frío y caliente | REPORT unido por request ID; parser probado |
| E17 | Comparar con al menos cinco warm | 16 | Medir frío y caliente | Lote acotado y criterio de completitud implementados |
| E18 | Declarar cold no capturado sin inferir por orden | 16 | Medir frío y caliente | Caso sin REPORT probado y explicado |
| E19 | Estimar 1000 solicitudes sin ejecutarlas | 17, 18 | Coste y alternativas | Calculadora offline ejecutada |
| E20 | Lambda/API/Bedrock/logs con región y tarifas | 17, 18 | Coste y alternativas | Desglose reproducible y fuentes; S3/tráfico adicionales visibles |
| E21 | Elegir otra arquitectura por tiempo, streaming, latencia o carga | 5, 11, 19 | Coste y alternativas | Criterios y límites de comparaciones explicados |
| E22 | Entregar código, configuración, petición, errores y medidas | 20, 22 | Entrega y preguntas | Paquete local; evidencias cloud pendientes |
| E23 | Limpieza de recursos | 20 | Coste, alternativas y retirada | Procedimiento con propiedad/etiquetas; retirada real pendiente |
| O01 | Streaming si se soporta, permisos/límites propios | 19, 20 | Coste y alternativas; Entrega | Explicado como opcional; no implementado |

## Controles comunes

El guion suma 90 minutos, identifica las dos promociones y el QR de S16 correspondiente. El enunciado y los archivos están preparados para entrega previa; la subida a la plataforma no se ha ejecutado en esta preparación.

**Cobertura documental no equivale a ensayo cloud.** Para cerrar la ejecución se necesitan acceso, permiso, presupuesto, llamada IAM real, Bedrock real, muestra/REPORT, coste interpretado e inventario de retirada. Tampoco sustituye el ensayo oral del profesor.
