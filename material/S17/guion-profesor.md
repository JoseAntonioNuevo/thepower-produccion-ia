# Guion completo del profesor S17

**Guion histórico.** El recorrido vigente está en el
[guion corto](demo-bedrock/docs/guion-clase.md), el
[README](demo-bedrock/README.md) y las notas del Power actualizado.
El material que sigue corresponde al paquete avanzado anterior.

**Serverless AI: AWS Bedrock y Lambda.** M/J: martes 17/11/2026. L/X: lunes 23/11/2026. Ambas clases de 18:30 a 20:00 Europe/Madrid, incluidas las preguntas.

El QR evalúa S16 del **12/11 para M/J** y del **18/11 para L/X**. Anunciar la fecha del grupo; el mismo núcleo de materiales sirve para ambos. L/X dispone de la base ejecutable dentro del paquete, aunque su S16 la imparta otro profesor.

## Preparación y criterio de la clase

Abrir presentación, editor en la raíz, terminal, consola AWS de laboratorio, CloudWatch y carpeta de recibos. Compartir una pantalla sin credenciales, headers de firma o archivos de acceso. Fuente de terminal legible. El código del alumno y los enunciados deben estar disponibles antes del directo; los 4–6 h del ejercicio son trabajo autónomo.

La función, permisos y acceso al modelo se preparan antes de clase. No dedicar el directo a solucionar una cuota inicial de la cuenta. Tener un lote real completo y sus REPORT como respaldo fechado. Hoy la preparación local no acredita ese ensayo cloud: el profesor debe realizarlo en el laboratorio autorizado antes de presentarlo como resultado real.

Objetivo: que el alumno explique dónde se valida y autoriza cada paso, siga una llamada firmada, distinga latencias, interprete cold/warm con evidencia y estime 1.000 solicitudes. La clasificación de soporte es conocida; el foco cambia a operación serverless.

## 18:30–18:35 · QR y continuidad · 5 minutos

Diapositivas 1 y 2. «Hoy conservamos la incidencia y el JSON de la clase anterior. Cambiaremos quién ejecuta la API, quién llama al modelo y cómo se controla el acceso».

Dar un minuto para el QR. En M/J recordar el contenedor de S16; en L/X mostrar brevemente `datos/peticion.json` y `contratos.py` sin asumir el mismo repositorio. Recoger una respuesta a: «¿Qué seguiría siendo nuestra responsabilidad si el proveedor gestiona los servidores?». Conservar en la pizarra código, permisos, límites y costes.

## 18:35–18:47 · Serverless y alternativas · 12 minutos

Diapositivas 3–5. Dibujar el recorrido: cliente con credenciales temporales → API Gateway HTTP API → Lambda → Bedrock. API Gateway recibe HTTPS, autoriza y traduce la respuesta proxy; Lambda ejecuta código y valida; Bedrock ejecuta el modelo. IAM conecta las identidades y permisos. No son tres nombres para el mismo servicio.

**Serverless.** El proveedor aprovisiona y opera los servidores; nosotros configuramos función, dependencias, memoria, tiempo, concurrencia e identidades. Cobro por uso no significa coste cero ni capacidad infinita. La función tiene un ciclo de inicialización e invocaciones; un entorno puede reutilizarse, pero no debe guardar el estado de negocio que necesitamos conservar después. El SDK puede reutilizar conexiones dentro de un entorno caliente.

**Lambda.** Explicar evento, contexto y respuesta. La integración HTTP API v2 transforma la petición en un evento; el handler devuelve `statusCode`, headers y body JSON. Lambda no es FastAPI: no necesitamos arrancar uvicorn para este ejemplo. El paquete Linux incluye las dependencias que usa el handler, no todo el entorno del Mac.

**Bedrock.** Es el acceso gestionado a modelos, no el servidor de nuestra API. Modelo, región, perfil de inferencia, parámetros y permisos forman parte de la configuración. La referencia del ejercicio es `eu.amazon.nova-2-lite-v1:0`; el prefijo europeo acota una geografía, no una única región fija. El preflight lee las regiones de destino; no se atribuye una región concreta a una llamada si el proveedor no la informa.

**Alternativas.** Azure Functions + Foundry y Cloud Run functions + Vertex AI cubren funciones y modelos gestionados. Los gateways, permisos, límites y precios deben comprobarse para el servicio y plan concretos. No llamar «equivalentes» a productos con distinta semántica. Mostrar que una VM o un contenedor siguen siendo opciones válidas para procesos continuos, dependencias especiales o tráfico sostenido.

Pregunta: «Si Lambda permite configurar más tiempo, ¿desaparece el límite de una llamada HTTP?». Respuesta: no; el gateway y el cliente tienen límites propios. Retomar esta pregunta en la diapositiva de timeouts.

## 18:47–19:00 · Handler, JSON e identidades · 13 minutos

Diapositivas 6–10 y anexo de IAM si hace falta. Abrir `config.py`, `bedrock.py` y `handler.py` del módulo serverless.

**Perfil y permisos.** Mostrar el recibo del perfil leído antes de clase. El rol de Lambda necesita `bedrock:InvokeModel` sobre el ARN del perfil y los modelos base en origen/destinos. La condición del modelo se vincula al perfil. No conceder todos los modelos con un comodín para evitar estudiar los recursos. `Converse` es el nombre del método SDK; `bedrock:Converse` no es la acción que usamos en la política.

Hay tres comprobaciones distintas: la identidad del cliente puede invocar esa ruta de API Gateway; API Gateway puede invocar el alias Lambda; el rol de Lambda puede acceder a Bedrock. Una firma correcta no arregla un permiso faltante. El 403 del cliente y un `bedrock_denegado` de la función están en capas distintas.

**Contrato.** Abrir el esquema compartido: categorías `acceso`, `facturacion`, `tecnico`, `consulta`; prioridades `alta`, `media`, `baja`. El handler valida el texto antes del SDK, exige tiempo restante y hace una sola llamada. El proveedor devuelve una herramienta `emitir_clasificacion`, cuyo input se valida nuevamente. La herramienta se usa como estructura de salida: no se ejecuta una acción ni se llama una segunda vez al modelo.

**Diferencia con S8.** Allí se comparaba la capacidad del modelo para devolver JSON sin ayudas. Aquí se construye un servicio robusto: se solicita estructura compatible con `toolConfig` y se valida en el servidor. No mezclar estos resultados con el benchmark de S8.

Mostrar demo local si conviene:

```bash
uv run python scripts/demo_s17.py
```

Señalar `execution: demo`, tokens nulos y error 422. No convertir sus milisegundos en una medición de Bedrock. Para ver el runtime real de Python/Linux, usar el recibo de RIE: es un emulador local, sin IAM ni modelo real.

Pregunta: «¿Qué hacemos si el modelo devuelve una prioridad que no existe?». Respuesta: error de salida controlado, sin reparar o reintentar de forma oculta.

## 19:00–19:15 · Petición firmada y prueba de acceso · 15 minutos

Diapositivas 7, 8 y 14. El entorno ya está desplegado y la identidad del profesor autorizada. Mostrar la versión de Lambda, el alias y su hash, y la ruta `POST /clasificar` con AWS_IAM. No mostrar una política global como solución didáctica.

```bash
uv run python -m scripts.aws_s17 estado "${S17_ARGS[@]}"
uv run python -m scripts.aws_s17 politica-cliente "${S17_ARGS[@]}"
```

La segunda orden genera la política específica, pero no modifica la identidad. Explicar `execute-api:Invoke` sobre la ruta y stage, y cómo la configura el administrador del laboratorio.

**SigV4.** Abrir `firma.py`. Mostrar método, URL, región, servicio `execute-api` y bytes del JSON; los valores de credenciales permanecen ocultos. La firma se calcula sobre la petición canónica con fecha y session token. Si se cambian los bytes después de firmar, no es la misma petición. HTTPS cifra el transporte; la firma no reemplaza TLS. Las credenciales temporales caducan y se renuevan mediante el acceso acordado.

```bash
uv run python -m scripts.aws_s17 verificar "${S17_ARGS[@]}" --execute
```

Recorrido: sin firma → 403; firmada con entrada vacía → 422 sin modelo; firmada válida → 200 con JSON. El comando consume una inferencia real y conserva las comprobaciones parciales si algo falla. Mostrar request ID, versión, modelo y resultado; no headers Authorization.

Si se desea capturar el cold start del despliegue nuevo durante el mismo directo, invertir el orden operativo: ejecutar `medir` antes de este bloque y conservarlo para analizar a las 19:28. Verificar primero calienta el entorno. La exposición puede mostrar los recibos en el orden docente aunque se hayan generado antes, indicando fecha y origen.

Si hay problemas de credenciales o cuota, conservar el error y usar el ensayo fechado. No conceder permisos amplios ni cambiar a un perfil global en directo.

## 19:15–19:28 · Límites y errores · 13 minutos

Diapositivas 11–13. Recorrer cada límite de la implementación y dónde se comprueba: cuerpo 8 KiB; texto 2.000 caracteres; salida 300 tokens; un intento total del SDK; concurrencia reservada 2; throttle de la ruta. Son decisiones del laboratorio que hacen el comportamiento explicable.

**Tiempo.** Cliente 35 s, integración 29 s, Lambda 24 s, SDK 2 s de conexión y 15 s de lectura. HTTP API tiene un máximo documentado de 30 s. Antes del SDK se comprueba margen de 20 s tanto respecto al tiempo restante de Lambda como al transcurrido desde que API Gateway recibió la petición. La inicialización fría también consume el plazo del cliente/gateway.

Mostrar `Timeout: 24` en la plantilla: responde a la advertencia del enunciado de no dejar Lambda con el valor predeterminado de tres segundos. Ningún cambio de ese timeout amplía por sí solo el del gateway.

No confundir timeout con cancelación garantizada de un trabajo remoto o gasto cero: una solicitud que no devolvió respuesta puede haber consumido recursos. No repetirla automáticamente sin entender el estado. Para investigación larga, separar inicio/estado/resultado mediante una arquitectura asíncrona; aumentar Lambda no aumenta el límite del gateway.

**Concurrencia.** Reservada limita y asigna capacidad dentro de la cuota; provisioned mantiene entornos preparados y tiene otra facturación. Reservar dos no significa tener dos entornos precalentados. El preflight comprueba que queden cien unidades sin reservar. Si la cuenta no permite la reserva, preparar el laboratorio; no quitar el control silenciosamente.

Mostrar las pruebas de errores sin provocar llamadas de pago innecesarias:

```bash
uv run pytest tests/test_s17.py -q
```

Seleccionar una entrada rechazada, un timeout y una salida inválida. Los dobles prueban esos caminos y la ausencia de reintentos, no disponibilidad real de AWS. Explicar 400/413/415/422 antes del proveedor, 503 por limitación, 504 por tiempo y 502 por permisos de Bedrock o salida inválida. Los mensajes remotos privados no se devuelven al alumno.

Pregunta: «La llamada está firmada, pero aparece `bedrock_denegado`. ¿Qué política revisamos primero?». Respuesta: rol de Lambda y recursos del perfil/modelo, además de restricciones de cuenta; no la firma del cliente.

## 19:28–19:40 · Medir frío y caliente · 12 minutos

Diapositivas 15 y 16. Abrir el lote real preparado; si el directo lo permite, ejecutar un lote acotado:

```bash
uv run python -m scripts.aws_s17 medir "${S17_ARGS[@]}" --execute
uv run python -m scripts.aws_s17 logs "${S17_ARGS[@]}"
```

Hay un máximo de seis llamadas secuenciales y se detiene ante un fallo. No ejecuta llamadas indefinidas para conseguir el resultado deseado. CloudWatch puede tardar; `logs` relee sin generar inferencias.

Separar los tiempos: HTTP del cliente incluye red y recorrido completo; handler mide su trabajo y excluye init; paso de modelo mide el SDK; `provider_latency_ms` es la medida que informa Bedrock si existe. REPORT aporta `Duration`, `Billed Duration`, memoria y `Init Duration` cuando corresponde. No sumar dos mediciones superpuestas como si fueran tramos independientes.

Cruzar el request ID de la respuesta con REPORT. La primera petición de nuestro cliente puede llegar a un entorno ya caliente; por eso no se etiqueta cold por su posición en la tabla. `first_in_environment` es una pista del proceso, y el resumen confirma cold mediante `Init Duration`. Cinco respuestas con entorno reutilizado satisfacen la muestra warm; si no se consiguen, se declara el lote incompleto.

Mostrar dos casos docentes: cold confirmado en REPORT y ausencia de cold capturado. Ambos son resultados válidos de observación, pero no aportan la misma comparación. No inventar una duración fría ni estimar una frecuencia del 16,7% a partir de una muestra de seis.

Recordar que S16 invocaba Anthropic y aquí usamos Nova en Bedrock. Conservamos el contrato, no el modelo. Si se comparan costes o latencia entre arquitecturas, hay que controlar esa diferencia; este ejemplo no demuestra por sí solo que Lambda o Fargate sea más rápido.

Si falta un REPORT, señalar cobertura pendiente. No convertir campos nulos en cero. Conservar errores y resultados parciales; la calculadora no descarta silenciosamente el posible gasto de llamadas fallidas.

## 19:40–19:50 · Coste, alternativas y retirada · 10 minutos

Diapositivas 17–20. Ejecutar la calculadora, que no hace peticiones:

```bash
uv run python scripts/costes_s17.py
```

Ejemplo de planificación, no medición: 1.000 solicitudes, 512 MiB, 1.500 ms facturados warm, 1.800 ms cold, frío hipotético 5%, 250 tokens de entrada y 100 de salida. La duración media facturable es 1.515 ms y el consumo Lambda 757,5 GB-s. Las tarifas estándar leídas en Irlanda son 0,0000166667 USD/GB-s, 0,0000002 USD/solicitud Lambda, 0,00000111 USD/solicitud HTTP API, 0,000374 USD/1K tokens de entrada y 0,003157 USD/1K de salida para Nova 2 Lite no global.

Añadir logs relevantes, tráfico facturable y retención/publicación del ZIP. Resultado del ejemplo: **0,4249 USD**, con cantidades supuestas, sin impuestos, descuentos ni créditos asumidos. Los tokens dominan este ejemplo, pero eso no demuestra que ocurra en toda aplicación. La calculadora puede usar duración y tokens observados cuando el lote y los REPORT estén completos; la frecuencia fría y los volúmenes futuros siguen siendo supuestos.

**Optimizar y elegir.** Medir antes de cambiar memoria; más memoria puede reducir duración, no siempre coste. Acotar tokens y evitar reintentos innecesarios; limitar logs/retención. Con tráfico sostenido comparar con Fargate; para procesos largos usar trabajos asíncronos; para una experiencia interactiva evaluar streaming con transporte/modelo/permisos compatibles. La ruta entregada es no streaming y no promete ese extra.

**Retirada.** Mostrar el comando preparado, el inventario y la propiedad de los recursos:

```bash
uv run python -m scripts.aws_s17 limpiar "${S17_ARGS[@]}" --execute
```

Retirar API, integración/ruta, Lambda/alias/versiones, rol y logs, y todas las versiones/delete markers del bucket propio. Conservar identidades compartidas; el administrador revisa la política externa del llamante. No hay un modelo de Bedrock creado por nosotros que borrar. Si la eliminación tarda, seguir con recibo anterior y dejar el estado actual pendiente de revisar después de clase.

## 19:50–20:00 · Entrega y preguntas · 10 minutos

Diapositiva 20, anexos 21–22 como consulta. Recordar los entregables que el alumno ya tiene publicados: código/configuración, llamada firmada válida, errores, medidas cold/warm con sus límites, cálculo de 1.000 solicitudes y limpieza. Las 4–6 horas son trabajo autónomo con accesos preparados.

Tres preguntas finales: «¿Converse qué permiso necesita?», «¿Qué demuestra que una llamada fue fría?», «¿Por qué 24 s de Lambda no autorizan una investigación de varios minutos detrás de esta HTTP API?». Respuestas: `bedrock:InvokeModel`; Init Duration/registro equivalente, no el orden; existen límites independientes y debe cambiarse el patrón de trabajo.

Conectar con CI/CD y evaluación: una API que devuelve JSON aún necesita pruebas, entrega verificable y medidas de calidad. No asumir que ambos grupos tienen el mismo profesor o el mismo orden de prácticas. El código de referencia permite continuar de forma independiente.

## Respaldo y decisiones antes de cada grupo

| Incidencia | Continuación preparada |
|---|---|
| Perfil no disponible o cuota insuficiente | Explicar el preflight y el bloqueo concreto; usar código y evidencia anterior rotulada |
| Credenciales temporales caducadas | Renovación con el procedimiento acordado; no mostrar claves ni improvisar claves permanentes |
| Llamada real falla | Conservar el error; mostrar el contrato con dobles y el ensayo anterior, sin llamarlo ejecución actual |
| REPORT todavía no disponible | Releer logs, no repetir inferencia; declarar cobertura pendiente |
| No hay cold confirmado | Presentar warm y declarar no capturado; no perseguirlo con bucles de pago |
| Limpieza no concluye | Registrar recurso y estado pendiente; revisar después con identidad/destino correctos |

Antes del 23/11 realizar un preflight breve del mismo código/configuración, actualizar el contexto de L/X y comprobar el QR. No cambiar modelos o dependencias justo antes de clase. El ensayo oral con cronómetro y la comprobación de reunión/grabación corresponden al profesor.
