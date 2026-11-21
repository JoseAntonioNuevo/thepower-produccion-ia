# Verificación local de S17

## Versión vigente · demo sencilla del 11/11/2026

La evidencia actual está en [ENSAYO.md](demo-bedrock/ENSAYO.md).
Se creó y retiró realmente el stack pequeño en eu-north-1. Se comprobaron
salud 200, IAM 403, entrada 422 y error controlado 503 por cuota cero.
No hubo clasificación exitosa ni lote válido de cold/warm. Se mantiene Free.

65 pruebas pasan; lint/formato del código nuevo y cfn-lint correctos.
El Power conserva 26 diapositivas/notas, fuentes, QR y marca; usa el mismo
modelo, región, configuración y comandos que el README de demo-bedrock.

## Evidencia anterior · preparación de octubre y rediseño del 06/11

Preparación del 17/10/2026. Cobertura documental y comprobaciones locales; no se ha desplegado en AWS ni invocado Bedrock real desde este proyecto.

## Temario y materiales

- **30/30 puntos obligatorios de comprobación** del temario y ejercicio mapeados a diapositivas, guion y código/procedimiento. Una ampliación opcional de streaming identificada aparte, sin presentarla como implementada.
- Fechas de ambas promociones y QR correcto: M/J 17/11 evalúa S16 del 12/11; L/X 23/11 evalúa S16 del 18/11.
- Guion continuo de ocho bloques, **90 minutos**, incluyendo preguntas.
- **22 diapositivas y 22 notas del orador**, texto y tablas editables. QR original conservado byte a byte.
- Validación de paquete, geometría, fuentes, tablas nativas, suma de costes e importación correcta.
- SHA-256 PPTX: `124edd39b36da461162e66fb30d140579d27d8f3d841f8f27277bf6ffe20be81`.
- PDF de presentación: 22 páginas. Todo el texto del PPTX está presente en el PDF; sin texto fuera del lienzo. Se revisaron las diapositivas renderizadas y las revisiones de etiquetas/código.
- Guion y guía: **6 páginas PDF cada uno**, todas renderizadas y revisadas. El PDF de presentación embebe Liberation Sans/Mono tras exportación de LibreOffice; el PPTX declara Arial/Courier New, como S16.

## Código e infraestructura

| Comprobación | Resultado |
|---|---|
| Suite del repositorio | **45 pruebas correctas**, incluidas las 24 previas y 21 de S17 |
| Ruff lint/formato | Correctos |
| CloudFormation S16 y S17 | Cuatro plantillas validadas con cfn-lint |
| Petición Converse | Validada contra el SDK instalado mediante Stubber, sin red |
| Contrato de Lambda | Entrada/salida, base64, tipos, tamaño, plazo y errores probados |
| SigV4 | Firma temporal construida localmente; rechazo de destinos ajenos y credenciales sin session token |
| Perfil europeo | Rechazo de ARN/modelos/regiones inesperados; origen incluido en permisos |
| Cold/warm | No confirmar cold por orden; REPORT unido por request ID y criterio de cinco warm probado |
| Identidad de despliegue | Cambiar configuración con el mismo ZIP cambia la versión de despliegue |
| Limpieza | Objetos inesperados del bucket no se borran; destinos/etiquetas limitan la operación |
| Coste | Estimación offline de 1.000 peticiones y rechazo de evidencia incompleta/simulada |

Se conserva la advertencia de deprecación de Starlette sobre la compatibilidad de TestClient/httpx de la base S16; no es un fallo y las pruebas terminan correctamente. S17 no utiliza FastAPI dentro de Lambda.

## ZIP y runtime Linux

- Construcción real con la imagen oficial Lambda Python 3.12, digest fijado, objetivo `linux/amd64` y dependencias con hashes.
- ZIP final: 19.368.078 bytes comprimidos, 30.393.926 bytes descomprimidos y 2.373 archivos.
- SHA-256 del ZIP: `0195a544766e680610584298d12feb716473e8b7c9d932867e2ad6070f96f073`.
- Importación y ejecución del contrato dentro del runtime Linux correctas.
- Ensayo HTTP mediante RIE correcto: resultado proxy 200 válido y 422 inválido, con `execution: demo`.
- El contenido Python serverless del ZIP coincide con los archivos finales del proyecto.
- Recibo local: `evidencias/local/s17-rie.json`, excluido de los paquetes de distribución.

RIE no prueba API Gateway, IAM efectivo, escalado, cuota, facturación ni Bedrock real. La firma generada localmente tampoco prueba que una identidad esté autorizada en AWS.

## Distribución y conservación

- Paquete de inicio extraído en carpeta limpia: instalación desde lock y **16 tests correctos**.
- Referencia completa extraída de nuevo tras el último cambio de runtime: instalación desde lock y **45 tests correctos**.
- Los paquetes excluyen credenciales, `.env`, entornos, caches y recibos operativos. El ZIP Lambda se entrega aparte, sin anidarlo dentro del ZIP de referencia.
- Los archivos de ejecución/tests/lock verificados se conservan al regenerar las últimas revisiones documentales.
- Los materiales de S16 mantienen los mismos hashes del inicio de la tarea. La única adaptación del helper de operaciones común permite el prefijo/infraestructura de S17, conservando S16 como valor predeterminado.

## Coste y límites pendientes

Tarifas estándar de Irlanda leídas del catálogo público AWS el 17/10/2026. El ejemplo de **0,4249 USD** usa cantidades hipotéticas declaradas; no deriva de la demo ni es una factura. El cálculo con muestras reales exige REPORT, tokens y condiciones comparables y no descarta errores de gasto desconocido.

Antes de impartir la práctica real quedan: cuenta/permisos/presupuesto, preflight del perfil/cuotas, publicación y despliegue, aceptación de SigV4 por IAM, inferencia real, muestra warm/cold con REPORT, limpieza/readback y ensayo oral del profesor. No se ha ejecutado ninguno de esos cambios cloud durante esta preparación.

Estado de entrega: archivos locales, sin commit, push ni remoto. OpenViking pendiente porque el selector no devuelve una cuenta para el repositorio; no se ha utilizado otro tenant.


## Rediseño visual del 06/11/2026

- `presentaciones/S17-serverless-ai-rediseno-visual.pptx` y `.pdf`: versión de clase reducida a petición de José, 26 diapositivas (23 de clase y 3 de consulta) con 26 notas; las pantallas que se enseñan en vivo pasan a las notas. Generadas con `fuentes/rediseno-visual/build_clase.py`; la versión completa de 49 se regenera con `build.py`. El PPTX original conserva su SHA-256 `124edd39…be81`.
- `check.py`: sin elementos fuera del lienzo; QR vigente de S16 (SHA-256 `29c9041e…8c6`) presente una vez y QR antiguo de S17 ausente. QR de la página 2 del PDF decodificado: `https://kb.tools.thepower.education/feedback/feedback-form.html?form=ai-engineer`.
- PDF de 26 páginas con Arial, Georgia y Courier New incrustadas; todas las páginas renderizadas y revisadas.
- Coste: `scripts/costes_s17.py` reproduce 0,4249 USD (cero peticiones). Las 11 tarifas del 17/10/2026 coinciden con la lista pública de precios de AWS para eu-west-1 leída el 06/11/2026.
- Límites y datos de modelo comprobados en la documentación oficial el 06/11/2026 (HTTP API 30 s y 10 MB; cuotas de API Gateway y Lambda; INIT facturado desde el 01/08/2025; perfil EU de Nova 2 Lite y sus seis destinos desde eu-west-1).
- Sin despliegue, inferencia, envío, commit ni push. La consola de AWS no tenía sesión abierta en el navegador integrado y no se inició sesión: las pantallas sin captura oficial se muestran como esquemas rotulados.
