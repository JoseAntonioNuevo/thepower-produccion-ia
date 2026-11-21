# Guion completo del profesor S16

**Cloud deployment: AWS basics y Docker.** Versión común: 12 de noviembre (M/J) y 18 de noviembre (L/X) de 2026, 18:30–20:00 Europe/Madrid. Son 90 minutos con preguntas. La presentación acompaña el recorrido; el código, la terminal y AWS muestran la ejecución.

## Preparación del directo

Mostrar `S16-inicio.zip` como punto de entrada para el alumno. Para ejecutar la demo del profesor, abrir la referencia con Docker y scripts AWS preparados. Mostrar solo archivos de S16 y explicar la finalidad de cada uno antes de ejecutar.

Abrir cinco ventanas: presentación, editor en la raíz del proyecto, terminal local, consola AWS del laboratorio y carpeta de recibos. Fuente de terminal de al menos 20 puntos. Cerrar ventanas con credenciales y desactivar vistas que muestren variables de entorno. Tener preparado el QR de AI Engineer, actualizado por Laura el 19/10, que evalúa S15, la sesión anterior de cada grupo.

Antes de clase: ejecutar la lista `checklist.md`, disponer de una imagen con versión única y verificar la conexión desde la IP pública que tendrá el profesor. Si se usa VPN, esa salida condiciona el /32. Preparar una ejecución real anterior, con fecha, modelo y recibo, para continuar si un proveedor o AWS falla. A día de preparación local, el ensayo AWS sigue pendiente y no debe inventarse ese respaldo.

La API usa Anthropic como proveedor remoto para mantener continuidad con S8. El objetivo de S16 es desplegar la aplicación que consume IA; no entrenar ni alojar pesos. Bedrock se sitúa en el mapa de servicios y se trabajará en S17.

## Objetivos observables

Al terminar, el alumno debe poder dibujar el recorrido desde una petición al contenedor y al proveedor; explicar imagen, registro y ejecución; distinguir las tres identidades de AWS; localizar el digest desplegado; comprobar salud y función; calcular coste y retirar recursos propios. La práctica es opcional, según confirmó Laura el 04/11. Quien la complete deberá realizar ese recorrido real y aportar evidencias.

## Recorrido visible y participación

En cada paso: indicar qué vamos a hacer, ejecutarlo, mostrar el recurso o respuesta y preguntar qué acredita. Los scripts automatizan tareas repetitivas; se explica su finalidad y se leen sus resultados en la consola. Mantener la explicación centrada en los archivos de S16 y sus resultados.

| Paso | Acción en directo | Comprobación visible |
|---|---|---|
| 1 · Docker local | Leer Dockerfile y arrancar Compose | /health, /clasificar demo y UID 10001 |
| 2 · ECR | Crear registro y publicar | Images: versión, tag y digest |
| 3 · Tarea | Abrir Task definitions y la revisión usada | Imagen por digest, CPU/RAM, arquitectura, modelo y ARN del secreto |
| 4 · Red | Abrir servicio/tarea, Networking y security group | IP pública, entrada /32:8000, ruta y salida HTTPS |
| 5 · Función | Consultar salud y ejecutar una clasificación | execution real, versión, request ID y log correspondiente |
| 6 · Retirada | Mostrar destino, retirar lo propio y revisar | Inventario eliminado, conservado o borrado programado |

Preguntas breves: «¿Una imagen en ECR ya responde a HTTP?», «¿Quién lee el secreto al arrancar?», «¿Qué falta si /health funciona pero el modelo falla?» y «¿Qué sigue costando si paro la tarea?». Hacer una pausa en cada resultado; no esperar al final para comprobar comprensión.

## 18:30–18:35 · Apertura y QR · 5 minutos

Diapositivas 1–3. Presentar el objetivo: «Vamos a llevar una API que ya entendemos desde nuestro equipo hasta AWS. Al final tendremos que demostrar qué imagen se ejecuta, que responde y cuánto cuesta mantenerla».

Mostrar el QR: «La encuesta valora la sesión anterior, S15 de vuestro grupo. Hoy aprenderemos a desplegar». Dar un minuto para escanear. Explicar que las preguntas se pueden hacer durante las comprobaciones y que habrá diez minutos finales.

Abrir `datos/peticion.json` para recordar la incidencia ficticia. La salida sigue teniendo categoría, prioridad y respuesta; el problema conocido permite concentrarse en despliegue.

Pregunta de entrada: «Si en mi equipo responde, ¿qué cosas todavía pueden fallar al llevarlo a otra máquina?». Recoger arquitectura, dependencias, puertos, permisos y configuración. Volver a esta lista durante el diagnóstico.

## 18:35–18:47 · Cloud y mapa de servicios · 12 minutos

Diapositivas 4–7. Mostrar la consola y situar cuenta y región. La 6 introduce IA gestionada dentro del bloque principal.

**Cloud y AWS básico.** Explicar que se consumen recursos por API y que la región determina ubicación, servicios y precios. Una región contiene zonas de disponibilidad; repartir una aplicación entre ellas puede mejorar disponibilidad, pero este laboratorio de una tarea y una subred no lo hace. Una cuenta es una frontera de identidad, permisos y facturación. Aclarar responsabilidad compartida: el proveedor gestiona la infraestructura física; nosotros seguimos siendo responsables de aplicación, permisos, secretos, datos y configuración de red.

**Compute.** Distinguir VM, contenedor y función. Una VM ofrece un sistema que administramos; el contenedor empaqueta proceso y dependencias; Fargate ejecuta la tarea sin que administremos hosts; una función responde a invocaciones con otro contrato de ejecución. No deducir que serverless es gratuito ni que un contenedor elimina el sistema operativo subyacente.

**Storage.** Distinguir objetos, disco/bloque y datos estructurados. S3/Blob/Cloud Storage conservan objetos; EBS/Managed Disks/Persistent Disk son discos; RDS/Azure Database/Cloud SQL son servicios de bases de datos. ECR guarda imágenes; CloudWatch guarda logs; ninguno sustituye una base de datos del producto. La API de hoy es stateless y no necesita añadir almacenamiento de negocio.

**Networking.** Presentar VPC, subred, tabla de rutas, internet gateway, IP y security group. Tener una IP no implica que exista una ruta ni que el firewall permita entrar. La salida es necesaria para descargar imagen, recuperar secretos y llamar al proveedor. Explicar que DNS resuelve nombres y que un endpoint privado sería otra decisión de diseño.

**Seguridad.** Identidad dice quién eres; política dice qué puedes hacer; red dice qué conexión puede llegar. Un puerto cerrado no sustituye autorización y una clave válida no arregla una ruta de red. En nuestro laboratorio el acceso se limita a una IP y usa datos sintéticos; una API para usuarios necesitaría autenticación y HTTPS.

**Comparación.** Recorrer la tabla AWS/Azure/GCP por función: EC2/VMs/Compute Engine, Fargate/Container Apps/Cloud Run, S3/Blob/Cloud Storage, VPC/VNet/VPC e IAM/Entra ID + RBAC/Cloud IAM. Son correspondencias funcionales, no compatibilidad de API ni equivalencia de todas las capacidades.

**IA gestionada.** Bedrock, Microsoft Foundry en Azure y Vertex AI permiten consumir modelos y capacidades gestionadas; varían catálogo, regiones, permisos, cuotas y precios. Diferenciar consumir un modelo de desplegar la API que lo utiliza. Hoy Fargate ejecuta nuestra API y esta llama a Anthropic; no hay un modelo descargado dentro de la imagen.

Pregunta: «¿Dónde persistiría una conversación si el contenedor se reemplaza?». Respuesta esperada: fuera del filesystem efímero, en almacenamiento apropiado. PostgreSQL se incorporará cuando el caso lo requiera.

## 18:47–19:02 · API y Docker local · 15 minutos

Diapositivas 8–10. Abrir `src/curso_ia/contratos.py`: entrada acotada, campos extras rechazados y categorías conocidas. Mostrar que el cliente no puede escoger el modelo. Abrir `api.py`: `/health` no llama al proveedor; `/clasificar` valida y añade metadatos medidos. Abrir `proveedores.py` para distinguir reglas demo y cliente real.

En una terminal de la raíz:

```bash
uv sync --frozen --all-extras
uv run python scripts/preflight.py
docker compose up --build -d
```

Mientras arranca, leer el Dockerfile en orden: base fijada por digest; dependencias con hashes; copia de `src/`; usuario 10001; versión; healthcheck; comando. Abrir `.dockerignore`: claves, recibos y materiales no entran en el build. Mostrar el mapeo loopback de Compose y `read_only`.

```bash
curl --fail http://127.0.0.1:8016/health
curl --fail -H 'Content-Type: application/json' \
  --data-binary @datos/peticion.json http://127.0.0.1:8016/clasificar
docker compose exec api id
uv run python scripts/ensayo_local.py
```

Decir expresamente: «Este resultado está marcado como demo: prueba la API y el empaquetado, no una llamada a Claude». Señalar request ID y `coste_usd: null`. No explicar ese nulo como coste cero; la etiqueta `sin_llamada` es la evidencia de que esta variante no usa proveedor.

**Imagen y contenedor.** La imagen es el artefacto; puede originar varias ejecuciones. Cambiar el código local no modifica una imagen ya construida. El tag es un nombre legible; el digest identifica contenido. El contenedor no debe correr como root por defecto ni llevar las claves en sus capas.

**Arquitectura.** En Apple Silicon, un build por defecto puede producir ARM64. La tarea de este laboratorio es X86_64. Mostrar `--platform linux/amd64` y el resultado de `docker image inspect`. Elegir ARM64 también sería válido si se configura y prueba de extremo a extremo.

Pregunta: «¿`EXPOSE 8000` permite entrar desde Internet?». Respuesta: no; faltan publicación, ruta y reglas de red. Terminar el bloque con la API respondiendo y el UID visible.

## 19:02–19:20 · Publicación y Fargate · 18 minutos

Diapositivas 11–15. Seguir el diagrama: construir → ECR → task definition → tarea Fargate. La task definition describe imagen, CPU, memoria, arquitectura, puertos, variables, secretos, healthcheck y logs. El servicio mantiene el número deseado de tareas.

Usar las variables `S16_ARGS` ya preparadas con cuenta y región correctas. La configuración de acceso y la creación inicial del laboratorio se ensayan antes; no mostrar pantallas de credenciales.

```bash
uv run python scripts/aws_lab.py bootstrap "${S16_ARGS[@]}" --execute
uv run python scripts/aws_lab.py publicar "${S16_ARGS[@]}" \
  --version "$S16_VERSION" --execute
```

Abrir ECR → repositorio del laboratorio → Images. Señalar etiqueta y digest, y después abrir el recibo `publicacion.json`, no el token de login. Relacionar tag y digest con ECR. Las etiquetas son inmutables: cada versión lleva un nombre nuevo. No reutilizar una etiqueta cuyo contenido ya exista.

**Definición de tarea.** Antes de desplegar, leer `infra/s16/servicio.json`. Al terminar el despliegue, abrir ECS → Task definitions → revisión usada por el servicio para comprobar los valores. Relacionar imagen por digest, 0,25 vCPU, 512 MiB, X86_64, puerto 8000, `API_MODE=real`, modelo, ARN del secreto y grupo de logs con la plantilla. Mostrar configuración sin mostrar el valor del secreto.

**Las tres identidades.** El operador crea recursos. El execution role lo usa ECS para descargar imagen, escribir logs y leer el secreto al arrancar. El task role lo utiliza el código para acceder a AWS durante la ejecución. El de esta API no necesita permisos adicionales. Dar a task role acceso al secreto no arregla por sí solo un fallo del execution role. KMS propia requiere `kms:Decrypt` y una key policy que permita ese acceso.

**Secretos.** Mostrar solo el ARN en la definición de tarea. Secrets Manager es nuestra implementación; Parameter Store es la alternativa permitida por el ejercicio. Una variable de entorno permite inyectar configuración, pero no convierte un valor escrito en Dockerfile en un secreto protegido. Rotar un secreto inyectado requiere reemplazar/actualizar la tarea para que lo vuelva a leer; no asumir que cambia dentro de un proceso existente.

**Red.** Abrir ECS → servicio → tarea → Networking y después el security group. Mostrar VPC y subred, ruta a internet gateway, ENI/IP de la tarea y security group. Entrada 8000 desde el /32 del profesor; salida TLS 443. El contenedor llama al proveedor por HTTPS. Por HTTP de laboratorio solo circulan peticiones y respuestas sintéticas sin credenciales de cliente.

```bash
uv run python scripts/aws_lab.py desplegar "${S16_ARGS[@]}" \
  --ip "$S16_IP" --secret-arn "$S16_SECRET_ARN" --modelo "$S16_MODEL" --execute
```

**Corte a las 19:12.** Si la nueva ejecución tarda, recorrer el recibo de un ensayo anterior y su task definition, explicando la fecha. No presentar ese servicio como el despliegue que acaba de terminar. El objetivo es enseñar el proceso completo conservando los bloques de costes y limpieza.

## 19:20–19:32 · Evidencia funcional y diagnóstico · 12 minutos

Diapositivas 16–17. Primero:

```bash
uv run python scripts/aws_lab.py estado "${S16_ARGS[@]}"
uv run python scripts/aws_lab.py verificar "${S16_ARGS[@]}" --execute
```

El primer comando lee la tarea, verifica task definition y digest y obtiene la IP. El segundo ejecuta salud y una clasificación real. Comprobar versión de aplicación, `execution: real`, modelo solicitado/devuelto y tokens observados. Un job correcto o un stack completo no prueban que la función de negocio responda.

Abrir CloudWatch `/thepower/<lab>` y localizar el request ID del recibo. Mostrar estado, duración y versión. Los logs no contienen texto del alumno, cuerpo del proveedor ni clave. Health aporta disponibilidad del proceso; la clasificación aporta la prueba del modelo. Tener ambas evidencias evita diagnosticar todo como «AWS funciona/no funciona».

Probar entrada vacía con el archivo sintético: devuelve 422 antes del proveedor. Para fallo remoto y timeout usar los tests preparados, no provocar gasto o cambiar claves en vivo:

```bash
uv run pytest tests/test_api.py tests/test_proveedor.py -q
```

Recorrer la tabla de diagnóstico: si no arranca, imagen/arquitectura/comando; si no obtiene imagen/secreto, execution role/red/KMS; si no entra el Mac, IP/ruta/SG; si salud responde pero clasificación falla, configuración/proveedor/timeout. El 429 se presenta como limitación del proveedor y no dispara reintentos ocultos.

Pregunta: «Tenemos salud 200 y clasificación 504. ¿Dónde empezamos?». Esperado: plazo y conexión del proveedor; conservar request ID y no dar el ejercicio por terminado.

## 19:32–19:42 · Costes y optimización · 10 minutos

Diapositivas 18–20. Mostrar `datos/costes-ejemplo.json` y el recibo de tarifas. Las tarifas fueron leídas del catálogo público de AWS para Irlanda; las cantidades son supuestos docentes, no consumo observado.

```bash
uv run python scripts/costes.py
```

Desarrollar el cálculo: CPU `0,25 × 730 × 0,04048 = 7,3876 USD`; memoria `0,5 × 730 × 0,004445 = 1,622425 USD`; IPv4 `730 × 0,005 = 3,65 USD`. Añadir ECR, ingesta y almacenamiento de logs, secreto y lecturas y salida facturable. Resultado redondeado: **13,78 USD sin inferencia, impuestos, descuentos o créditos**.

El ejemplo supone 0,25 GB en ECR, 1 GB de logs ingeridos/almacenados, un secreto, dos lecturas y 1 GB de salida facturable. El tramo gratuito global de tráfico no se puede descontar sin conocer el resto de la cuenta. No se suman NAT, balanceador ni base de datos porque no están en esta arquitectura.

La demo de 90 minutos mantiene imagen, secreto y logs almacenados durante 30 días y suma **0,46 USD sin inferencia**. Mostrar la diapositiva 20: 0,0260 USD de cómputo/IP, 0,4253 USD de retención y 0,0058 USD de uso, con total calculado antes de redondear. Explicar que apagar cómputo reduce CPU, memoria e IP, pero conservar ECR, logs o secretos deja partidas. Retirar todo reduce esos remanentes; no equivale a borrar una factura de consumo pasado.

**Inferencia.** Tokens de entrada/salida observados por tarifa del modelo, separados del hosting. No inventar el precio de un modelo o interpretar un campo nulo como gratis. El consumo de caché tiene categorías propias; no se sumará sin distinguir su tarifa.

**Optimización.** Elegir tamaño medido de CPU/memoria, apagar cuando no se usa, limitar tokens, evitar reintentos innecesarios, limitar retención de logs, eliminar imágenes sobrantes y no añadir NAT/ALB sin necesidad de la arquitectura. Los presupuestos y alertas ayudan a detectar gasto, pero no se presentarán como un interruptor universal que lo detiene.

Pregunta: «¿Qué coste sigue existiendo si ponemos DesiredCount a cero?». Respuesta: los recursos que permanezcan, según su facturación; revisar imagen, logs, secretos y cualquier recurso extra.

## 19:42–19:50 · Limpieza e inventario · 8 minutos

Diapositiva 21. Antes de ejecutar, mostrar nombre, cuenta y región. Confirmar que los recursos pertenecen al laboratorio de la sesión. La etiqueta y el recibo complementan esa identificación.

```bash
uv run python scripts/aws_lab.py limpiar "${S16_ARGS[@]}" --execute
uv run python scripts/aws_lab.py retirar-secreto "${S16_ARGS[@]}" --execute
```

El segundo comando solo corresponde si se creó ese secreto con la herramienta y ya no lo utiliza otra práctica. Su borrado queda programado con ventana de recuperación; mostrar ese estado y la fecha. Si el secreto es compartido, conservarlo y registrar quién lo gestiona.

La primera operación espera a retirar el stack del servicio (incluye tarea, logs, roles, ENI/red) y después vacía el ECR propio y retira su stack. Si CloudFormation queda en DELETE_FAILED, localizar el recurso bloqueante; no usar un borrado masivo de toda la cuenta.

Completar el inventario: servicio/tareas; repositorio/imágenes; logs; VPC/subred/SG/IGW; ENI/IP; secreto; KMS externa; cualquier ALB/NAT/EIP añadido. Distinguir eliminado, conservado y borrado programado. No afirmar cero recursos cobrables si queda algo pendiente de revisar.

Si la retirada tarda, mostrar el recibo de un ensayo anterior y dejar la operación actual marcada como pendiente. La comprobación final del profesor continúa después de clase sobre los recursos de este directo.

## 19:50–20:00 · Ejercicio y preguntas · 10 minutos

Diapositiva 22. La práctica es voluntaria; sus criterios explican cómo completarla si el alumno decide hacerla. Comprobar que el enunciado y los materiales estén disponibles antes de la clase. Recordar cinco entregables: código reproducible, imagen/despliegue identificados, salud y función reales, coste con supuestos y limpieza con inventario. Las 4–6 horas son una estimación de trabajo autónomo para quien decida hacer la práctica, no una tarea obligatoria.

Repasar tres preguntas: «¿Qué identidad lee el secreto?», «¿Qué prueba el digest?», «¿Qué evidencia falta si solo tengo health 200?». Respuestas: execution role al arrancar; identidad del artefacto; una petición funcional real y su correspondencia con la versión desplegada.

La ampliación HTTPS/ALB y tareas privadas es opcional: aporta acceso TLS y otra topología, pero añade permisos, recursos, coste y limpieza. No exigir S3 o una base de datos para una API que no los necesita.

Conectar con S17: conservaremos el contrato y cambiaremos el recorrido a API Gateway, Lambda y Bedrock. El alumno podrá comparar operaciones, límites y costes usando el mismo problema.

## Respaldo y límites de interpretación

| Incidencia durante el directo | Continuación preparada |
|---|---|
| Docker no arranca | API local y recibo del ensayo de contenedor, rotulado como anterior |
| AWS tarda o falta un permiso | Plantillas, eventos y ejecución anterior; no crear permisos amplios en directo |
| Modelo rechaza o está limitado | Error real conservado, test de contrato y respuesta anterior identificada |
| Falla la conectividad del aula | Presentación, logs saneados y recibos locales; demo offline explícita |
| Coste no disponible | Tokens observados y fórmula, sin convertir ausencia de dato en cero |
| Limpieza queda pendiente | Inventario y revisión posterior del recurso concreto; no afirmar retirada completa |

El profesor debe ensayar la exposición con cronómetro. La verificación técnica local no acredita que la explicación oral quepa en el tiempo ni que una cuenta AWS tenga los permisos adecuados. La matriz de cobertura distingue esos estados.

