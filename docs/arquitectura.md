# Base común y decisiones de S16

## Flujo

`HTTP → Incidencia validada → Proveedor → Clasificacion validada → respuesta + metadata`.

La API no tiene memoria ni herramientas. El límite de S16 es una pequeña API de IA con despliegue, no la integración de todas las sesiones. La interfaz Proveedor permite añadir Bedrock en S17 sin duplicar la taxonomía.

## Reutilización concreta

- Taxonomía de `2-modelos/curso/common.py`: cuatro categorías y tres prioridades. Se ha extraído a un contrato limpio; no se importan su `.env`, constantes Qwen o código de entrenamiento.
- Criterio de S6: request ID, versión, latencia y consumo desconocido explícito. Los logs de S16 son JSON y omiten entradas, respuestas y claves. Langfuse se añadirá donde lo exija la sesión.
- Patrón de ensayos anteriores: pruebas locales separadas de proveedor real, recibos fechados y error conservado. Un fallo real no se disfraza de resultado demo.
- Los documentos y el código de RAG/research siguen en sus repositorios. No se han copiado como implementación Python de S19/S20.

## Dependencias y ejecución

Python 3.12, dependencias directas fijadas, resolución completa en `uv.lock`. El lock de contenedor solo incluye ejecución. La imagen base está fijada por digest multi-arquitectura; el build AWS fija `linux/amd64` y la tarea `X86_64`. La imagen local de aula puede usar ARM64 si se construye así; no se publicará como amd64 sin construir esa variante.

El entorno se carga explícitamente con `uv --env-file` o inyección del contenedor. El repositorio no lee claves de otros proyectos. La API usa un único pool HTTP por proceso y lo cierra al terminar. La respuesta remota se limita a 64 KiB descomprimidos y a un plazo total; la entrada HTTP a 16 KiB y el texto a 2.000 caracteres.

## AWS

Dos stacks propios: `registro` contiene ECR; `servicio` contiene VPC, subred pública, internet gateway, rutas, security group, roles, logs, cluster, task definition y servicio. Se separan porque la imagen debe estar en ECR antes de arrancar la tarea.

Se despliega una imagen por digest. `estado` comprueba task definition y digest en ECS; `verificar` añade HTTP de salud y una clasificación real. El despliegue didáctico de una tarea admite interrupción durante actualización (`MinimumHealthyPercent=0`); no se presenta como alta disponibilidad ni como despliegue sin downtime.

El secreto se crea fuera del stack para que su valor no pase por parámetros o plantillas. `limpiar` conserva secretos externos. `retirar-secreto` solo programa el borrado de uno creado por el propio laboratorio, comprobando recibo, cuenta, región, nombre y etiquetas. KMS propia queda fuera de la creación automática y no se borra.

## Estados de evidencia

La cobertura de una explicación, la ejecución local, la compilación Docker, la inferencia real y el despliegue AWS son hechos diferentes. `material/S16/cobertura.md` identifica dónde se enseña cada requisito; `verificacion.md` identifica qué se ejecutó realmente.

## OpenViking

El selector de cuenta devolvió código 1 para este repositorio el 17/10/2026. No hay tenant verificado. La sesión queda documentada localmente; la entrega en OpenViking permanece pendiente.


## Material docente común de S16 desde el 06/11/2026

La misma presentación sirve para M/J del 12/11 y L/X del 18/11: ambas fechas en portada y QR referido a S15 de cada grupo sin fecha fija. Se utiliza el QR de Laura del 19/10 y se mantiene la práctica voluntaria, según su confirmación del 04/11.

El alumno empieza por una API preparada en S16-inicio; el profesor ejecuta los pasos sobre la referencia. Los ZIP de S16 seleccionan explícitamente sus módulos y excluyen serverless/S17. Los scripts automatizan, y la explicación conecta sus resultados con ECR, definición de tarea, red y logs en consola.

El coste de demo de 0,46 USD presupone 90 minutos de cómputo/IP y 30 días de ECR, secreto y logs almacenados. Es distinto del coste de retirar todos los recursos tras 90 minutos; la inferencia va aparte.
