# Fuente editable del rediseño visual de S17

## Versión vigente · 12/11/2026

La presentación vigente es la ampliación de **34 diapositivas: 33 de clase
y una de consulta**, con 34 notas y agenda de 18:30 a 20:00. La copia del
profesor es `the-power/S17-serverless-ai-v2.pptx`; su copia idéntica de entrega
está en `material/S17/presentaciones/S17-serverless-ai-rediseno-visual.pptx`.
Los comandos corresponden a `demo-bedrock/docs/comandos.md`.

Los generadores de este directorio reconstruyen versiones anteriores:
**no reproducen la ampliación de 34 diapositivas**. No ejecutarlos sobre la
presentación vigente. Antes de reconstruirla habría que incorporar esa
ampliación a sus fuentes y verificarla de nuevo.

## Versión anterior · 11/11/2026

Esta versión tenía **26 diapositivas: 25 de clase y una de consulta**,
con demo de Lambda/HTTP API IAM/Nova Lite en eu-north-1. Conserva paleta,
fuentes, QR y marca de la base anterior. Las notas siguen 90 minutos.
Los comandos vienen de `material/S17/demo-bedrock/README.md`.

Desde la raíz, con Node y `@oai/artifact-tool` disponibles:

```bash
node material/S17/fuentes/rediseno-visual/actualizar-demo-bedrock.mjs \
  material/S17/fuentes/rediseno-visual/referencias/S17-base-2026-11-06.pptx \
  .build/s17-demo-borrador.pptx
python material/S17/fuentes/rediseno-visual/ordenar-demo-bedrock.py \
  .build/s17-demo-borrador.pptx .build/s17-demo-ordenado.pptx
```

La segunda herramienta solo reordena XML y renumera el pie. Antes de sustituir
los entregables, validar paquete, geometría, fuentes, 26 notas y tablas;
exportar PDF, revisar todas las páginas y comprobar QR/logotipo contra la base.
La cuota cero de Bedrock se explica en diapositiva 9 y notas.

## Generadores y datos anteriores · históricos

**No ejecutar build_clase.py sobre el Power vigente:** repondría región,
perfil de modelo, agenda y pasos avanzados anteriores. Los datos siguientes
documentan la versión del 06/11, conservada en `referencias/`.

Genera `presentaciones/S17-serverless-ai-rediseno-visual.pptx` y, con LibreOffice, su PDF. La versión vigente para clase es la reducida (`build_clase.py`): **26 diapositivas, 23 de clase y 3 de consulta**. Las diapositivas explican los conceptos y las pantallas se enseñan en vivo en la consola de AWS; el contenido de las diapositivas retiradas (ficha del modelo, playground, página de la función, configuración, rutas, integraciones, CloudWatch, evidencias, política IAM, empaquetado y fuentes) pasa completo a las notas de la diapositiva que las sustituye, como «AMPLIACIÓN PARA EL RECORRIDO EN VIVO». No hay separadores de bloque: el bloque activo se indica en el pie y en las notas. `build.py` genera la versión completa de 49 diapositivas como consulta. `S17-serverless-ai.pptx` se conserva sin cambios como fuente original.

## Estructura de la clase (90 minutos, misma versión para el 17/11 M/J y el 23/11 L/X)

| Hora | Bloque | Diapositivas | Consola en vivo |
|---|---|---|---|
| 18:30 | Apertura: QR de S16, plan y caso conductor | 1–3 | — |
| 18:35 | 1 · Serverless frente al contenedor de S16 | 4–6 | — |
| 18:45 | 2 · Bedrock | 7–9 | catálogo, ficha, Cross-Region inference, playground |
| 19:00 | 3 · Lambda y API Gateway | 10–12 | función; Routes, Integrations, Stages, Throttling |
| 19:20 | 4 · IAM y CloudWatch | 13–14 | IAM › Roles; CloudWatch Logs y métricas |
| 19:30 | 5 · Latencia y límites | 15–18 | REPORT, si existe |
| 19:40 | 6 · Costes y alternativas | 19–21 | — |
| 19:50 | 7 · Práctica opcional y cierre | 22–23 | — |
| — | Consulta: recorrido por la consola, límites y cálculo del coste | 24–26 | — |

Cada diapositiva lleva notas con tiempo, qué explicar, qué pantalla abrir y qué campo señalar, una pregunta de comprobación, fuentes técnicas e imágenes.

## Archivos

- `deck_lib.py`: sistema visual (paleta, Georgia/Arial/Courier New, cabecera, navegación por bloques, separadores, rótulos de procedencia, esquemas de consola, tablas nativas).
- `deck_part1.py` … `deck_part6.py`: diapositivas y notas por bloques.
- `build_clase.py`: versión de clase (26) y reparto de notas. `build.py`: versión completa (49). `check.py`: notas, límites del lienzo, QR vigente de S16 y logotipo byte a byte, y ausencia del QR antiguo de S17.
- `preparar_assets.py`: convierte a PNG los iconos oficiales y recorta las capturas de documentación (reproducible a partir de los paquetes descargados).
- `fonts.conf`: hace que LibreOffice use Arial, Georgia y Courier New del sistema.
- `assets/`: iconos, logotipos y capturas. El logotipo de thePower se lee de `../../assets/`; el QR, de `material/S16/assets/qr-ai-engineer.jpg` (el de `material/S17/assets/` es antiguo y no se usa).

## Regenerar

Desde esta carpeta, con un Python que tenga `python-pptx` y `pillow`:

```bash
python build_clase.py ../../presentaciones/S17-serverless-ai-rediseno-visual.pptx
# versión completa (49): python build.py SALIDA.pptx
python check.py ../../presentaciones/S17-serverless-ai-rediseno-visual.pptx
FONTCONFIG_FILE="$PWD/fonts.conf" soffice --headless --convert-to pdf \
  --outdir ../../presentaciones ../../presentaciones/S17-serverless-ai-rediseno-visual.pptx
```

Después: revisar todas las páginas renderizadas, comprobar con `pdffonts` que aparecen Arial, Georgia y Courier New, decodificar el QR de la página 2 y, si cambian tarifas o cantidades, recalcular con `uv run python scripts/costes_s17.py` y actualizar `COST` en `deck_part5.py` y las diapositivas de coste (playground, coste estimado y cálculo).

## Datos y rigor

- Coste: `datos/s17/costes-ejemplo.json` (cantidades hipotéticas) y `docs/fuentes/tarifas-s17-2026-10-17.json`. Las 11 tarifas se compararon el 06/11/2026 con la lista pública de precios de AWS para eu-west-1: sin cambios. Total del ejemplo: 0,4249 USD.
- Límites de AWS citados (consultados el 06/11/2026): integración HTTP API 30 s y payload 10 MB; 10.000 rps y ráfaga 5.000 por cuenta y región; Lambda 900 s, 6 MB síncrono, 1.000 de concurrencia por defecto y 100 sin reservar; INIT facturado desde el 01/08/2025 en funciones ZIP con runtime gestionado.
- Nova 2 Lite: ficha oficial (perfil `eu.` con destinos eu-central-1, eu-north-1, eu-south-1, eu-south-2, eu-west-1 y eu-west-3 desde eu-west-1; sin In-Region en eu-west-1; «Structured outputs» no compatible).
- Ninguna diapositiva presenta un despliegue, una inferencia o una medición como realizados. Los valores de las líneas de log y las barras de tiempo están rotulados como ilustrativos.

## Procedencia de imágenes

- AWS Architecture Icons, paquete del 31/07/2026 (aws.amazon.com/architecture/icons). Logotipo de AWS como en S16.
- Azure Public Service Icons V25 (incluidos API Management y Monitor) y Microsoft Entra architecture icons.
- Google Cloud: core products icons y legacy icons de cloud.google.com/icons (API Gateway, Cloud Logging) y logotipo de gstatic.com.
- Diagramas y capturas oficiales de la AWS Lambda Developer Guide (Overview-Successful-Invokes, perf-optimize-figure-1, concurrency-7-reserved-vs-provisioned, python_code_editor, log-stream) y del tutorial de HTTP API de la API Gateway Developer Guide (ddb-create-routes, ddb-attach-integrations, ddb-invoke-url), recortados sin alterar su contenido. Los valores de esas capturas son del tutorial, no de nuestra API.
- Las pantallas rotuladas «ESQUEMA» (ficha del modelo, playground, página de la función, formulario de configuración) son dibujos propios: la consola del laboratorio no se capturó porque no había una sesión abierta.
