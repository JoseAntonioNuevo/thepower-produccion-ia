# Actualización OpenRouter · 11/11/2026

- Presentación canónica y PDF actualizados a 33 diapositivas con el diseño existente.
- Seis diapositivas prácticas añadidas antes de práctica y cierre.
- Región, arquitectura local/AWS, secreto, respuesta JSON, logs y notas alineados
  con la API mínima y el ensayo real; retiro de los ejemplos antiguos de metadata.
- Costes de Estocolmo recalculados: 730 h de cómputo+IPv4+secreto = 13,95975 USD
  como total parcial; dos horas de cómputo+IPv4 = 0,03715 USD. Sin inferencia,
  impuestos ni créditos; ECR/logs/tráfico/lecturas se añaden según uso.
- Finalizador de Presentations: integridad, dimensiones, tipografías de referencia
  y reimportación correctas. Render de las 33 páginas y revisión visual del conjunto
  y de las diapositivas modificadas. QR y logo preservados byte a byte.
- Evidencia privada y recibo del finalizador en `.build/ppt-audit/`.
- Fuente reproducible en `fuentes/rediseno-visual/actualizar-demo-openrouter.mjs`,
  con base histórica archivada y ordenación OOXML mediante biblioteca estándar.
- Sin commit, push ni actualización de la copia anterior alojada en Google Drive.
- OpenViking: pendiente, workspace sin cuenta asignada; no se ha usado otro tenant.

---

## Evidencia histórica anterior

# Verificación de la base común y S16

## Rediseño visual para el recorrido por la consola (06/11/2026)

**Versión reducida vigente (misma fecha):** a petición de José, 27 diapositivas (25 de clase y 2 de consulta), generadas con `fuentes/rediseno-visual/build_clase.py`. Se quitan separadores y diapositivas que repetían lo que se enseña en vivo (formularios de EC2, S3, security group, task definition, Bedrock y calculadora; ARN, mínimo privilegio, Dockerfile, cadena, diagnóstico, optimización, proveedores, comandos y fuentes). Su contenido pasa a las notas de la diapositiva que las sustituye. Horario continuo 18:30–20:00 con el tiempo de consola incluido; agenda de la diapositiva 2 actualizada. Comprobado: 27 páginas revisadas, QR decodificado desde el PDF, cifras 13,78/0,46 sin cambios, Arial/Georgia/Courier New incrustadas. Lo descrito a continuación corresponde a la versión completa de 51 diapositivas, que puede regenerarse con `build.py`.

Nueva presentación `presentaciones/S16-cloud-aws-rediseno-visual.pptx` y su PDF, con la estética de S12 (fondo oscuro, Georgia/Arial/Courier New, navegación por seis bloques, idea guía). Centro de la clase: recorrer la consola de AWS sin crear recursos ni invocar modelos. La presentación original `S16-cloud-docker.pptx` queda intacta (SHA-256 `9fc24902…0b60ae`, el mismo registrado abajo).

- **51 diapositivas y 51 notas**: 47 de clase con horario continuo de 18:30 a 20:00 y 4 de consulta. Cada nota incluye qué explicar, qué abrir en la consola, qué señalar, una pregunta, el tiempo y las fuentes técnicas y de imágenes. Sin formas fuera del lienzo; texto, tablas y diagramas editables.
- **PDF de 51 páginas** exportado con LibreOffice usando las fuentes reales del sistema (`fuentes/rediseno-visual/fonts.conf`): Arial, Georgia y Courier New incrustadas. Todas las páginas se renderizaron y revisaron; se corrigieron solapamientos, recortes y marcadores desalineados.
- **QR**: bytes idénticos al adjunto de Laura (SHA-256 `29c9041e…8c6`); decodificado desde la página 2 del PDF: `https://kb.tools.thepower.education/feedback/feedback-form.html?form=ai-engineer`. Encuesta rotulada como S15, sin fecha fija. Fechas: 12 y 18 de noviembre de 2026.
- **Costes recalculados** desde `datos/costes-ejemplo.json`: 13,775035 → 13,78 USD (730 h) y 0,45710875 → 0,46 USD (demo), con desglose 0,02601375 / 0,4253 / 0,005795 USD. Región, fecha de tarifas y supuestos visibles; inferencia aparte. No se actualizaron tarifas.
- **Imágenes**: iconos y logotipos oficiales (AWS Architecture Icons 31/07/2026, Azure Public Service Icons V25, Microsoft Entra icons, Google Cloud icons y logotipo, Docker logos), diagrama oficial de responsabilidad compartida, captura del Resource map de la VPC User Guide y captura propia de calculator.aws. Las pantallas dibujadas están rotuladas «ESQUEMA». Procedencia en la diapositiva 51 y en `fuentes/rediseno-visual/README.md`.
- **Datos verificados en documentación oficial el 06/11/2026**: campos de Create bucket y de Launch instance, opciones de Create repository de ECR, acceso a modelos de Bedrock y lista de proveedores del catálogo.
- No se crearon recursos AWS, no hubo inferencias ni gasto. El ensayo AWS real, la inferencia real y el ensayo oral siguen pendientes. Sin commit, push ni envío. OpenViking: el selector devolvió código 1 para este repositorio; memoria externa pendiente.

## Actualización docente del 06/11/2026

Alcance: misma versión para el 12/11 M/J y el 18/11 L/X. Cambios en presentación, notas, QR, guion, guía, enunciado, cobertura, checklist y paquetes. La práctica se presenta como opcional. El guion ampliado de Word también se actualizó en la carpeta general y se incorporó al paquete de S16.

- Presentación final: **24 diapositivas y 24 notas del orador**. Integridad, geometría, Arial/Courier New, tablas editables, sumas e importación con Artifact Tool correctas. PDF: **24 páginas**, revisadas visualmente. SHA-256 PPTX: `9fc24902425bce04c7faa9fc69e5d4879124aa5768b49b9cb61d89ab9f0b60ae`.
- QR: bytes exactos del adjunto de Laura del 19/10; SHA-256 `29c9041e732152679956162fe522a0433d70ad633145990f14327853fddde8c6`. Se decodificó también desde el PDF renderizado: formulario AI Engineer en `kb.tools.thepower.education`.
- Recorrido: seis pasos con acción, comprobación esperada y preguntas; lectura explícita en consola de ECR, definición de tarea, red y CloudWatch. IA gestionada forma parte del bloque principal.
- Guion PDF: **7 páginas**; guía PDF: **6 páginas**, renderizadas y revisadas. Word ampliado: **13 páginas**; cronograma de 90 minutos y referencias ajustados a las 24 diapositivas.
- Costes reproducidos: **13,78 USD/730 horas**; **0,46 USD con 90 minutos de cómputo/IP y 30 días de ECR, secreto y logs almacenados**. Desglose visible de 0,0260 / 0,4253 / 0,0058 USD; total calculado antes de redondear. Inferencia aparte. No son importes facturados.
- Checks del repositorio: Ruff lint y formato correctos, **45 tests**, `cfn-lint` de S16/S17 y preflight offline correctos. Se conserva la advertencia conocida de TestClient/httpx.
- Distribución: inicio **20 archivos**, referencia **53 archivos**, con listas de inclusión de S16. Se excluyen módulos serverless/S17, secretos, entornos y evidencias operativas. Los ZIP se extrajeron en carpetas limpias: instalación con lock, **16 tests del inicio** y **24 de referencia**, preflight demo y `cfn-lint` S16 correctos. Las revisiones finales de documentos no alteran código ni lock comprobados.
- El ensayo AWS real, la inferencia real, la limpieza remota y el ensayo oral siguen pendientes. No se han creado recursos ni hecho llamadas de pago en esta actualización.
- OpenViking: el selector `/Users/jose/.config/openviking/workspace-account.sh` para este repositorio devolvió código 1; no hay cuenta verificada. Registro local; memoria externa pendiente. Sin commit, push, envío a Laura ni publicación en plataforma.

## Preparación original del 17/10/2026

El registro siguiente corresponde a la versión inicial de 20 diapositivas; sus hashes, números de páginas y conteos de pruebas son históricos. Para la versión vigente se utiliza la actualización anterior.

Fecha: 17/10/2026. Alcance: código local, contenedor y materiales docentes. No se ha creado ningún recurso AWS, no se ha publicado una imagen en ECR y no se han hecho llamadas reales a Anthropic desde este proyecto.

## Cobertura docente

- Matriz con **26 puntos de cobertura** del temario/ejercicio y una ampliación opcional.
- Cada requisito tiene diapositivas y bloque del guion identificados.
- Guion con ocho bloques continuos de 18:30 a 20:00: **90 minutos**.
- S17–S20 conservan su inventario en `docs/cobertura-S16-S20.md`; todavía no son entregas implementadas.

## Código y plantillas

| Comprobación | Resultado |
|---|---|
| Instalación Python 3.12 con lock | Correcta; dependencias directas fijadas y resolución completa conservada |
| Ruff lint y formato | Correctos |
| Pytest del proyecto | **24 pruebas correctas** |
| CloudFormation registro y servicio | `cfn-lint` correcto, sin hallazgos |
| Preflight | Demo; sin clave/configuración real, sin comprobaciones remotas |
| CLI AWS sin `--execute` | Plan offline, sin inicializar una sesión operativa |
| Guardas | Recibo de otra cuenta/región/imagen rechazado; stack ajeno rechazado; cuenta STS errónea detenida; secreto compartido no borrado |

Los tests del adaptador usan `httpx.MockTransport`: acreditan formato, errores, tiempo/límites y ausencia de reintentos/redirecciones, no disponibilidad de un modelo real. Starlette emite una advertencia de deprecación de su compatibilidad de TestClient con httpx; la suite termina correctamente. El adaptador HTTP de la aplicación utiliza httpx de forma explícita.

## Contenedor y HTTP

- Build real `linux/amd64` correcto sobre la base Python fijada por digest.
- Contenedor ejecutado con usuario **10001:10001**, raíz de solo lectura, sin capabilities y `no-new-privileges`.
- Healthcheck del contenedor observado como `healthy`.
- GET `/health` correcto; POST sintético devuelve categoría `facturacion` y `execution: demo`.
- Entrada vacía devuelve 422; cuerpo excesivo devuelve 413.
- Ensayo repetido tras limitar el contenedor a **0,25 CPU y 512 MiB**, coherente con la tarea prevista. La instantánea local observó 57,6 MiB de memoria; no es una medición de producción ni una garantía de dimensionamiento.
- Recibos en `evidencias/local/`, fuera de Git y de los paquetes públicos.

## Presentación y documentos

- PPTX con **20 diapositivas y 20 notas del orador**, texto y tablas editables.
- Validaciones de integridad, geometría, fuentes, tablas nativas, suma de costes e importación correctas.
- SHA-256 del PPTX validado: `bc2c114d6b5d33165ecabe63d917d279a5a3876d024540aee36d9425892ea241`.
- Las 20 diapositivas se renderizaron y revisaron; se ajustó la separación de los encabezados de servicios de IA.
- PDF de presentación: 20 páginas, exportado desde el PPTX con LibreOffice. Todo el texto de las diapositivas aparece en el PDF; no se encontraron caracteres fuera del lienzo. El PDF embebe Liberation Sans/Mono, mientras el PPTX declara Arial/Courier New; la composición se revisó visualmente.
- QR original de AI Engineer incorporado con los mismos bytes que el archivo de referencia.
- Guion: 6 páginas PDF. Guía del alumno: 5 páginas PDF. Todas sus páginas se renderizaron y revisaron; los comandos tienen tipografía monoespaciada legible y se evitaron encabezados aislados al final de página.

## Costes y distribución

- Tarifas públicas de nueve partidas leídas para `eu-west-1`; SKU, unidad, publicación, efectividad y URL en `docs/fuentes/tarifas-aws-2026-10-17.json`.
- Calculadora ejecutada: **13,78 USD/730 horas** y **0,46 USD/demo de 90 minutos con ECR y secreto conservados un mes**, sin inferencia. Son estimaciones con cantidades supuestas, no consumo de una cuenta.
- Paquete de inicio extraído en carpeta limpia: instalación desde lock y **16 pruebas correctas**.
- Paquete de referencia extraído en carpeta limpia: instalación desde lock y **24 pruebas correctas**. Las revisiones finales de presentación y documentación no cambian esos archivos de código/lock.
- Los ZIP excluyen entornos, caches, claves y evidencia operativa. Sus hashes se generan en `paquetes/manifiesto.json`.

## Pendiente para el ensayo real de la clase

1. Identificar cuenta, región, perfil, permisos, presupuesto y modelo disponible del laboratorio.
2. Publicar la imagen, crear/seleccionar el secreto y desplegar las plantillas con autorización de esa operación.
3. Verificar digest/task definition, salud e inferencia real; guardar recibo y respaldo fechado.
4. Ensayar retirada e inventario de recursos y secretos, distinguiendo borrado programado y recursos compartidos.
5. Completar ensayo oral de José, reunión, pantalla y grabación.

La preparación local y la cobertura documental están verificadas. La ejecución AWS, la inferencia real y la aceptación oral del profesor no se declaran completadas. Repositorio local iniciado sin commit, push ni remoto. OpenViking pendiente por falta de cuenta mapeada.

