# S16 · Limpieza y preparación para el directo · 12/11/2026

José confirmó ensayo real correcto y pidió limpiar para repetir la demo.
Se verificó el proyecto autorizado y se inspeccionaron recursos de S16.
El servicio ya estaba INACTIVE y ECR ya había sido eliminado; no se repitieron
esas mutaciones. Se retiró únicamente la entrada temporal TCP 8000 /32 del
grupo propio, después de comprobar propietario, nombre y etiquetas.

Lectura final: cluster ACTIVE, cero tareas ejecutándose/pendientes y cero
servicios activos; servicio INACTIVE con deseadas cero; repositorio propio
no encontrado; ninguna interfaz de red del grupo; entrada vacía, salida
HTTPS preparada. Rol, secreto AWSCURRENT y logs con tres días conservados.
Se conserva la definición de tarea activa de referencia, que no ejecuta cómputo.

Docker local: no hay contenedores s16-demo; imagen s16-clasificador:1 existe
y es linux/amd64. Se conservaron imágenes para evitar reconstrucción en clase.
No se invocó OpenRouter ni se leyó el valor de ningún secreto.

El siguiente directo comienza con la infraestructura de apoyo y las imágenes
locales, y crea ECR, publica imagen, registra la configuración y crea servicio
siguiendo GUION-DEMO-MIXTA.md. La IP pública se obtiene de nuevo en cada ejecución.
El secreto y registros conservados pueden seguir generando coste.

OpenViking pendiente: workspace sin mapeo; evidencia y decisiones locales,
sin acceso a otros tenants. Sin commit ni publicación en esta tarea.
