# Demo AWS con un agente

Copia el siguiente bloque en una sesión nueva de Claude Code, Codex u otro agente con terminal y acceso AWS ya configurado. El prompt despliega, prueba y limpia: genera consumo temporal de AWS y hasta dos llamadas a OpenRouter.

```text
Realiza la demo completa de despliegue de nuestra API de clasificación en AWS.
Ejecuta el trabajo; no te limites a explicar los pasos. Antes de cada fase,
escribe una frase breve que yo pueda enseñar a los alumnos.

TRABAJA AQUÍ
/Users/jose/Documents/the-power/4-produccion-ia/material/S16/demo-openrouter

Lee las instrucciones del proyecto, README.md, aws/contexto.sh,
aws/task-definition.json y aws/network.json. El guion GUION-OBSIDIAN.md
describe el recorrido que ya hemos ensayado.

DESTINO AUTORIZADO
- Perfil AWS: thepower-aws.
- Proyecto: 123456789012, For Each and Every.
- Región de todos los recursos de esta demo: eu-north-1 (Estocolmo).
- Modelo: openai/gpt-6-luna mediante OpenRouter, proveedor openai/fast.

Ya están preparados el cluster s16-thepower, el rol de ejecución, el secreto
de OpenRouter, el grupo de logs y la red identificados en los archivos aws/.
Reutilízalos y verifica que existen y corresponden al proyecto indicado.
No necesitas crear nuevas credenciales, roles, redes ni secretos.

AUTORIZACIÓN PARA ESTA DEMO
Te autorizo a crear el repositorio ECR s16-clasificador si no existe,
publicar la imagen, registrar una definición de tarea y crear un servicio
temporal s16-thepower-api en el cluster s16-thepower. También a permitir
TCP 8000 exclusivamente desde mi IPv4 pública actual en el grupo de
seguridad propio de la demo. Una tarea Fargate de 0,25 vCPU y 512 MiB basta.
No cambies a otro proyecto, región o proveedor ni amplíes permisos.

HAZ EL RECORRIDO COMPLETO
1. Comprueba identidad AWS, región, Docker e infraestructura de apoyo.
   Usa el MCP oficial de AWS cuando esté disponible y terminal para Docker
   y las pruebas HTTP. Si no hay MCP, usa AWS CLI con perfil y región
   explícitos. Si la sesión caducó, abre el login y espera mi autenticación.

2. Comprueba el estado previo. No interrumpas contenedores ni servicios
   ya activos. Si hay un servicio AWS previo con el mismo nombre, detente
   antes de modificarlo. Registra qué recursos creas en esta ejecución.

3. Construye la imagen nativa para probar en mi Mac y otra linux/amd64
   para Fargate X86_64. Usa nombres de contenedor y etiquetas propios de
   esta ejecución, un puerto local libre y una versión de imagen nueva.
   No sobrescribas etiquetas inmutables ni modifiques el código de la API.

4. Arranca la API local con --env-file .env. Prueba /health y una única
   clasificación ficticia. Detén tu contenedor local después de probarlo.
   No muestres .env, tokens, variables privadas ni el valor del secreto.

5. Crea ECR si hace falta, autentica Docker mediante --password-stdin y
   publica la imagen AMD64. Obtén su digest desde ECR. Genera una copia
   temporal de la definición que apunte a ese digest, manteniendo el modelo,
   referencia al secreto, rol, logs, recursos y arquitectura preparados.

6. Comprueba la propiedad del grupo de seguridad, guarda sus reglas previas
   y permite solo mi IP /32 en TCP 8000. Nunca uses entrada 0.0.0.0/0.
   Registra la definición de tarea y lanza un servicio con una sola tarea,
   usando la red preparada y una IP pública temporal. Espera como máximo
   diez minutos al arranque; si falla, lee eventos y logs antes de actuar.

7. Obtén la IP actual y prueba /health y una única clasificación real desde
   AWS, con tiempos de espera limitados y datos ficticios. Exige modo real,
   modelo esperado y respuesta válida; una simulación no cuenta como éxito.
   Muestra la URL, la clasificación y los logs de arranque antes de limpiar.

8. Tras validar, limpia automáticamente lo temporal, sin otra confirmación:
   escala tu servicio a cero, espera a que pare y elimínalo; desregistra
   solo la revisión de tarea creada por ti; retira tus imágenes y manifiestos
   de ECR y elimina el repositorio solo si lo creaste tú. Si el repositorio
   existía antes, conserva sus otras imágenes y referencias. Restaura las
   reglas de entrada anteriores y conserva la salida HTTPS.

9. Conserva el cluster, rol, secreto, grupo de seguridad, VPC, subredes,
   logs y todos los recursos de apoyo que existían al empezar. Verifica
   que no queden tareas, servicios o interfaces de tu despliegue, ni acceso
   de red añadido por ti. Si falla una fase, recoge el error sin secretos y
   limpia igualmente lo que hayas creado. No declares limpieza completa
   sin verificarla; si hay un bloqueo, informa qué queda y si sigue costando.

ENTREGA
Guarda DEMO-AGENTE-RESULTADO.md en esta carpeta, sin secretos, con las
pruebas reales, imagen/digest, revisión de tarea, resultado funcional y
estado final de limpieza. Distingue el coste estimado del gasto facturado.
No hagas commit, push ni cambios de facturación. Al finalizar, explica en
pocas líneas qué has desplegado, qué funcionó y qué recursos conservamos.
```
