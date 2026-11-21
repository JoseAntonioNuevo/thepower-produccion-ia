# Prueba del prompt del agente · 11/11/2026

**Resultado: despliegue, clasificación real y limpieza completados.**

## Ejecución

- Proyecto `123456789012`, perfil `thepower-aws`, región `eu-north-1`.
- Ejecución: `agent-20261111-a1cafb89`.
- Se construyeron imágenes nativa `linux/arm64` y AWS `linux/amd64`.
- API local: salud HTTP 200 y una clasificación real de OpenRouter.
- Imagen publicada con etiqueta propia y desplegada por digest:
  `sha256:7ffd96fd001b0e63f60b677d21f287752b47f5894b8cb769fd92e48754862830`.
- Definición de tarea: `arn:aws:ecs:eu-north-1:123456789012:task-definition/s16-thepower-api:2`.
- Una tarea Fargate X86_64, 0,25 vCPU y 512 MiB: `RUNNING` y `HEALTHY`.
- API en AWS: `/health` HTTP 200 y `/clasificar` HTTP 200.
- Clasificación real: `openai/gpt-6-luna`; categoría
  `acceso`, prioridad
  `media`.
- Se comprobaron los mensajes de arranque de esta tarea en CloudWatch.
- Se realizaron dos llamadas al modelo: una local y otra desde AWS.

## Limpieza verificada

- Servicio de la prueba: `INACTIVE`.
- Cluster: cero tareas ejecutándose, cero pendientes y cero servicios activos.
- Repositorio ECR creado para la prueba, imágenes y manifiestos: eliminados.
- Revisión de tarea `:2` creada por la prueba: desregistrada (`INACTIVE`).
- Grupo de seguridad: sin entradas; salida HTTPS idéntica a la inicial.
- Sin interfaces de red de la demo; la IP temporal ya no está asociada a una ENI.
- Contenedor y tres etiquetas Docker locales de la prueba: retirados.
- Contenedor previo `s16-demo` y las imágenes de la clase: conservados.
- Se conservaron cluster, secreto y su versión AWSCURRENT, rol, red y logs
  con retención de tres días. Las revisiones de tarea anteriores se conservaron.

## Condiciones de la prueba

La autenticación AWS inicial había caducado y requirió que José completase
`aws login`. Tras renovarla, funcionaron tanto el MCP oficial como el SDK local.
Las operaciones de infraestructura se ejecutaron con el MCP; el token de ECR
se obtuvo mediante el SDK local y se pasó a Docker por stdin, sin mostrarlo.
No fue necesario modificar el código ni los permisos de la aplicación.

Esta prueba valida el recorrido con el acceso y los servicios disponibles hoy;
una sesión nueva necesita conservar el acceso a la carpeta, Docker y AWS.

Se generó consumo temporal de AWS y OpenRouter. No se ha consultado una factura
ni se presenta un importe como gasto real. El secreto y el almacenamiento de
logs conservados pueden seguir generando coste. No queda cómputo temporal activo.

No se hizo commit, push ni cambio de facturación. La evidencia técnica sin
secretos está en `.build/agent-prompt-test/`. Memoria OpenViking pendiente por
workspace sin cuenta mapeada.
