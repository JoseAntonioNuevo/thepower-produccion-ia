# S16 · Preparación revisada para el directo

Comprobación del 12/11/2026, desde las 13:09 (Madrid). Resultado: preparada para repetir la demo desde el estado limpio actual.

## Estado comprobado en AWS

- Identidad del proyecto 123456789012 correcta; región eu-north-1; plan Free activo.
- Cluster s16-thepower activo, cero tareas en ejecución o pendientes y cero servicios activos. El servicio anterior consta INACTIVE: permite volver a crearlo con el mismo nombre.
- Repositorio s16-clasificador ausente: el bloque de creación puede ejecutarse de nuevo y la etiqueta inmutable 1 está libre en el nuevo repositorio.
- Grupo s16-thepower-api sin entradas y sin interfaces asociadas. Salida HTTPS conservada. El guion abre 8000 solo para la IPv4 actual y lo cierra al terminar.
- Tres subredes disponibles, ruta de Internet activa, puerta de enlace conectada, DNS habilitado y ACL compatibles.
- Rol de ejecución conservado: confianza para ECS y permisos de lectura de esa imagen y ese secreto, y escritura en los registros de la demo.
- Secreto s16/thepower/openrouter disponible con versión AWSCURRENT, sin eliminación programada. No se leyó su valor.
- Registros /s16/thepower/api disponibles, retención de tres días.
- Definición s16-thepower-api:1 activa y compatible con el JSON local: Fargate Linux X86_64, 256 CPU, 512 MiB, puerto 8000, modo real, OpenRouter y referencia al secreto correcto.

## Archivos y ordenador

- Docker responde. Imagen s16-clasificador:1 disponible: linux/amd64, identificador sha256:debc95f008999c8815154541090e41d139d6d3441798023ca4c63abaec7ced55.
- app.py dentro de la imagen y archivo local coinciden: SHA256 f996aeeb04a478682d74556f43984e3ef7932fc259fde7a3bc83f67410934440.
- La lectura de la imagen usó un contenedor efímero --rm sin clave ni inferencia; no se dejó arrancado.
- Perfil local thepower-aws configurado en eu-north-1; herramientas necesarias disponibles y curl admite --fail-with-body.
- GUION-DEMO-MIXTA.md y la nota de Obsidian contienen los mismos 27 bloques de comandos; sintaxis validada en Bash y zsh. Se respetaron las diferencias de texto editadas en Obsidian.
- JSON de tarea y red válidos y referencias correctas. Scripts auxiliares pasan bash -n.
- Recuperación independiente del identificador de la configuración antes de create-service y comprobación de variable no vacía presentes.
- Flujo revisado: crear ECR → autenticar Docker → subir imagen → registrar configuración → abrir IP actual → arrancar servicio → esperar → obtener IP nueva → probar salud y clasificación → registros → parar/borrar/cerrar acceso.
- Nota S16 - Demo mixta AWS abierta y observada en Obsidian en modo lectura.

## Alcance de la validación

Esta revisión comprueba la preparación; no volvió a desplegar ni a llamar al modelo. El ensayo real completo fue realizado correctamente por José hoy antes de la limpieza. Las comprobaciones actuales no detectan bloqueos para repetirlo. La sesión AWS, la conexión y la disponibilidad de OpenRouter deben seguir vigentes al ejecutar la demo; el guion incluye la renovación del inicio de sesión y actualiza la IPv4 y la dirección de la tarea.

Sin cambios de permisos, facturación, recursos de AWS, código o comandos del guion; sin commit ni publicación. Evidencia AWS obtenida mediante el MCP oficial, verificando sus api_calls. No se expusieron valores de secretos.

OpenViking: espacio de trabajo sin cuenta mapeada; memoria pendiente. Se conserva esta nota local, sin usar otro tenant.
