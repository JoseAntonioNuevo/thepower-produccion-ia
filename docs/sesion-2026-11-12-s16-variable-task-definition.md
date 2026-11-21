# S16: ARN vacío al crear servicio · 12/11/2026

AWS confirmó definición s16-thepower-api:1 activa, imagen esperada y servicio
ausente. El comando del usuario enviaba task-definition vacío. Se añadió al
guion mixto la recuperación explícita del ARN activo antes de create-service
y expansión requerida de variable. Copia de Obsidian sincronizada. Sintaxis
Bash/zsh y rechazo de variable vacía comprobados sin ejecutar mutaciones AWS.

OpenViking pendiente: workspace sin mapeo; evidencia local, sin otro tenant.

Añadidas explicaciones al apartado 5: describe/variable, printf, create-service
y sus opciones, y espera de estado estable antes de la prueba HTTP.
Copias del repo y Obsidian idénticas, sintaxis validada sin ejecutar AWS.

Simplificada la frase de recuperación del identificador: explica la conexión
con el paso 4 y el uso de imagen, CPU y memoria, sin jerga de familia/revisión/ARN.
Copias de repo y Obsidian verificadas idénticas; sin cambios de comandos.

Reescrito todo el guion mixto con una frase sencilla por comando. Se
separaron los comandos agrupados para facilitar la explicación en clase;
se comprobó que todas las líneas Bash permanecen idénticas y en el mismo
orden. Sintaxis Bash/zsh correcta; copia de Obsidian idéntica. No se ejecutó
AWS ni Docker. OpenViking sigue pendiente por workspace sin mapeo.

Sustituido «app.py clasifica» por un ejemplo de mensaje y sus tres salidas:
tipo de problema, prioridad y respuesta sugerida mediante IA. Ambas copias
idénticas; sin cambios de comandos ni ejecución de recursos.

Apartado 6 adaptado a comandos: helper aws/ip-publica.sh de solo lectura
recupera IP con comprobación de proyecto y errores explícitos. Guion usa
curl para salud y una clasificación, y logs tail para arranque. Sintaxis
Bash/zsh del guion y Bash del helper correctas; apartado 6 idéntico en ambas
copias, conservando diferencias del usuario fuera de ese apartado. No se
ejecutaron consultas AWS ni inferencias durante esta edición.

Helper de IP probado offline con un sustituto local del comando AWS: devuelve
una dirección válida y falla sin salida si no hay tarea. Sin conexiones AWS
ni HTTP en estas comprobaciones.
