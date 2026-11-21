# S16 Desplegar una aplicación de IA con Docker

Enunciado de referencia: ejercicio redactado por José y enviado el 28/09/2026 en `AI_Engineer_enunciados.docx`, páginas 5 y 6 para S16/S17. Esta guía desarrolla S16 sin convertir las ampliaciones en obligaciones nuevas.

## Práctica opcional

La práctica es voluntaria, según la indicación de Laura del 04/11/2026. Si decides completarla, sigue estos criterios. Versión común para las clases del 12 y 18 de noviembre.

Construye una API FastAPI con un endpoint de salud y otro que invoque un modelo. Configura el modelo por variable, fija dependencias, añade Dockerfile y `.dockerignore` y ejecuta como usuario no root.

Comprueba ambos endpoints localmente. Publica una imagen identificable en ECR y despliega en ECS/Fargate. Si construyes desde Apple Silicon, usa `linux/amd64` o configura ARM64 de forma coherente en la tarea.

Protege las claves mediante Secrets Manager o Parameter Store y referencias desde la definición de tarea. Explica la diferencia entre execution role y task role. Si usas KMS propia, configura el descifrado y la política correspondiente.

Para esta demo basta IP pública temporal, puerto restringido a la IP de prueba y salida necesaria. Usa solo información ficticia y no envíes claves o credenciales de cliente por HTTP. No presentes esta opción como publicación de producción.

Empieza con `S16-inicio.zip` y utiliza la guía por pasos. La referencia completa permite consultar cada configuración.

Estima 730 horas en tu región: CPU, memoria, ECR, logs, IPv4 y tráfico. Añade los servicios adicionales utilizados e inferencia por separado. Cita tarifas, fecha y supuestos. No mantengas los recursos un mes para calcularlo.

Documenta y comprueba la retirada de tareas/servicios, imágenes, secretos, logs y red propios. No borres recursos compartidos. Compara mantener el mes entero con ejecutar la demo y apagar/retirar. El ejemplo de 0,46 USD incluye 90 minutos de cómputo/IP y 30 días de ECR, secreto y logs almacenados; la inferencia se calcula aparte.

## Entrega

- Código y dependencias bloqueadas.
- Dockerfile, `.dockerignore` e instrucciones o infraestructura declarativa.
- Evidencia local y AWS: imagen identificada, tarea, salud y petición funcional real.
- Cálculo de costes con supuestos, región y fecha.
- Procedimiento e inventario de limpieza; recursos conservados y motivo.
- README reproducible sin secretos y límites de la demostración.

Se valora repetibilidad, protección de secretos, arquitectura coherente y control de gasto. Dedicación orientativa: **4–6 horas activas con cuenta y permisos preparados**.

## Ampliación opcional

Balanceador HTTPS y tareas privadas, incluyendo su coste y limpieza. S3 y base de datos no son obligatorios. El modo demo permite estudiar el recorrido offline, pero no sustituye la invocación real ni el despliegue exigidos para completar el ejercicio.

