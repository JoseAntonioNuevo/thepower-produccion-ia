# Fuente editable de la presentación de S19

Genera `../../presentaciones/S19-evaluacion-testing.pptx` (20 diapositivas, 20 notas, 4 tablas
nativas) y, con LibreOffice, su PDF. Texto, tablas, diagramas, barras y la traza recreada de
Langfuse son **formas nativas editables**; las únicas imágenes son logotipos, iconos y el QR.

Versión del 22/11/2026. Sustituye al deck de 32 diapositivas que arrancaba con el cambio de
fragmentación 320 → 900: ahora el recorrido es un repaso breve del sistema y tres pruebas
reales, cada una con una diapositiva de pregunta (con predicción del grupo) y otra de resultado.

## Recorrido

| # | Diapositiva | Qué muestra |
|---|---|---|
| 1 | Portada | Título, autor, dos fechas y grupos; objetivo y cuatro partes del temario; práctica opcional |
| 2 | QR y recorrido | QR vigente y qué sesión valora cada grupo; pregunta del día; tres pruebas en una línea con su predicción |
| 3 | Qué vamos a usar | OpenTUI, LangGraph, PostgreSQL + pgvector, OpenRouter, Ragas y Langfuse; Python, Docker y pytest; color por etapa |
| 4 | Qué es un RAG | Documento → fragmento #03 → vector en PostgreSQL; `test.jsonl` y `validacion.jsonl` fuera del índice |
| 5 | El grafo | `recuperar` → umbral → `generar`/`comprobar` o `rechazo_previo`; embudo 12 → 5 → 4 con los datos reales de T01 |
| 6 | Langfuse | Recreación rotulada de la traza de V02: qué recuperó, qué respondió y cuánto costó; `consumo-juez` aparte |
| 7–8 | T01 | Generador Hydrogen → Terra; ambos TLS 1.3 con la misma cita; coste de dos llamadas medidas |
| 9–10 | T12 | Dos fuentes; recall@5 = 1,00, el fragmento del plan en el puesto 6 y los 4 que leyó el generador; ensayo y otro turno del chat por separado |
| 11–12 | V02 | Juez Sol → Opus sobre la respuesta congelada; Faithfulness y Answer Relevancy; coste de juzgar frente a generar |
| 13–14 | T09 | Regresión del evaluador: Sol 1 afirmación (PASA 0), Opus 2 afirmaciones (FALLA 1); control por caso frente a umbral del lote |
| 15 | Cierre | Evidencia para aprobar un cambio; práctica opcional; preguntas; S20 |
| 16–20 | Anexo | Métricas, A/B 320 → 900, histórico Hydrogen–Sol, prompt NO_CONSTA (respaldo de laboratorio) y comandos |

## Diseño

Mantiene el sistema visual del ejemplo de S17 (lienzo 960 × 540 pt): fondo `0F1B22`, tarjetas
`18272E`, bordes `33474F`, títulos `EAF1F2`, texto `C3D0D4`, menta `4FD1A1`; Georgia para
títulos, Arial para texto y Courier New para código. Portada y cierre usan el fondo `123630`.

**Un color por etapa en todo el deck** (constantes `ST_*` de `deck_lib.py`): datos e índice
menta, recuperar rosa, generar ámbar, juzgar violeta, observar (Langfuse) azul, fallo coral y
rama sin modelo gris. El pie marca el bloque activo con el mismo color: Sistema, Prueba 1 ·
Generador, Prueba 2 · Juez, Prueba 3 · Regresión, Cierre y Anexo.

Plantillas: las diapositivas de prueba llevan la pregunta exacta, lo que cambiamos (y lo que no),
qué vamos a mirar, el recuadro de predicción y el comando del directo. Las de resultado llevan
las respuestas, la evidencia (fragmento con el dato resaltado) y por qué ocurrió.

## Archivos

- `deck_lib.py`: helpers visuales (copia adaptada de S17). Al final, los añadidos del 22/11/2026:
  `logo` (logotipo sin deformar), `quote`, `prediccion`, `frag`, `answer`, `chip_row` y colores de etapa.
- `deck_part1.py` (1–6), `deck_part2.py` (7–14), `deck_part3.py` (15–20): diapositivas y notas.
- `build.py`: genera el PPTX. `check.py`: 20 diapositivas, notas completas (franja horaria,
  QUÉ ABRIR, PREGUNTA, Fuentes), límites del lienzo, tipografías, QR y logotipo byte a byte.
- `preparar_assets.py`: prepara los logotipos a partir de las descargas oficiales.
- `fonts.conf`: hace que LibreOffice use Arial, Georgia y Courier New.

## Regenerar

```bash
cd material/S19/fuentes/presentacion
# solo si cambian los logotipos (descargas en .build/s19/descargas, fuera de Git):
uv run --no-project --with pillow --with resvg-py python -I preparar_assets.py ../../../../.build/s19/descargas
uv run --no-project --with python-pptx --with pillow --with lxml python -I build.py ../../presentaciones/S19-evaluacion-testing.pptx
uv run --no-project --with python-pptx --with pillow --with lxml python -I check.py ../../presentaciones/S19-evaluacion-testing.pptx
```

PDF e imágenes (LibreOffice y Poppler del runtime local; no hay `soffice` en el PATH):

```bash
RT=~/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override
FONTCONFIG_FILE="$PWD/fonts.conf" $RT/soffice --headless --convert-to pdf --outdir ../../presentaciones ../../presentaciones/S19-evaluacion-testing.pptx
$RT/pdftoppm -png -r 110 ../../presentaciones/S19-evaluacion-testing.pdf /tmp/s19
```

`build.py` imprime dos avisos de «posible desborde» (pie del QR en la 2 y pregunta de la 13).
Son estimaciones conservadoras: en el render los dos caben.

## Procedencia de las imágenes

| Archivo en `assets/` | Qué es | Origen | Fecha |
|---|---|---|---|
| `../../assets/qr-ai-engineer.jpg` | QR vigente de AI Engineer | Copia byte a byte de `material/S16/assets/qr-ai-engineer.jpg` (Laura, 19/10/2026) | 17/11/2026 |
| `../../assets/thepower-logo.png` | Logotipo de thePower | Copia byte a byte de `material/S17/assets/thepower-logo.png` | 17/11/2026 |
| `opentui-logo.png` | Logotipo de OpenTUI (variante para fondo oscuro de su SVG) | <https://opentui.com/opentui-logo-auto.svg>, enlazado desde el README de <https://github.com/anomalyco/opentui>. La demo usa el enlace Python `opentui` 0.1.2 (<https://github.com/banditburai/opentui-python>) | 22/11/2026 |
| `langgraph-logo.png`, `langgraph-icon.png` | Logotipo de LangGraph y su símbolo | <https://raw.githubusercontent.com/langchain-ai/langgraph/main/.github/images/logo-dark.svg> | 22/11/2026 |
| `openrouter-logo.png`, `openrouter-glyph.png` | Logotipo horizontal y glifo de OpenRouter, variante «cloud» | Kit de marca oficial <https://openrouter.ai/brand> (`horizontal-cloud@2x.png`, `glyph-cloud@2x.png`) | 22/11/2026 |
| `postgresql.png` | Logotipo de PostgreSQL | <https://www.postgresql.org/media/img/about/press/elephant.png> (kit de prensa oficial) | 17/11/2026 |
| `python.png` | Logotipo de Python | <https://www.python.org/static/img/python-logo.png> | 17/11/2026 |
| `pytest-tile.png` | Logotipo de pytest sobre tesela blanca | <https://raw.githubusercontent.com/pytest-dev/pytest/main/doc/en/img/pytest_logo_curves.svg>, convertido con Quick Look | 17/11/2026 |
| `ragas-tile.png`, `ragas-wordmark.png` | Logotipo de Ragas (tesela con el símbolo; marca completa sin usar) | <https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/_static/imgs/logo.png> | 17/11/2026 |
| `langfuse.png` | Icono de Langfuse | <https://raw.githubusercontent.com/langfuse/langfuse/main/web/public/icon256.png> | 17/11/2026 |
| `docker-mark-white.png` | Marca de Docker | Copia de `material/S17/fuentes/rediseno-visual/assets/` | 17/11/2026 |
| `g-*.png` | Iconos genéricos de línea | Copia de `material/S17/fuentes/rediseno-visual/assets/` (su procedencia está en el README de S17) | 17/11/2026 |

pgvector no publica un logotipo propio en su repositorio (<https://github.com/pgvector/pgvector>):
se rotula con su nombre junto al icono genérico `g-data-table.png`, sin inventarle marca. Los
logotipos pertenecen a sus titulares, se usan solo para identificar cada herramienta y se
escalan sin deformar. No hay capturas de pantalla: la traza de Langfuse es una recreación.

## Rótulos de procedencia de los datos

| Rótulo | Significado | Diapositivas |
|---|---|---|
| ENSAYO REAL · 22/11/2026 | Cifras de llamadas reales guardadas en `demo-evaluacion/resultados/ensayo-*-20261122/` | 5, 8, 10, 12, 14 |
| OTRO TURNO REAL · chat del 22/11/2026 | Turno de T12 de la sesión `chat-20261122-155649` (Langfuse), distinto del ensayo controlado | 10 |
| RESULTADO LOCAL · no está en Langfuse | Veredictos de T09 en `detalle-faithfulness.json`; no se publicaron | 14 |
| RECREACIÓN · no es una captura | Traza dibujada con datos de V02 comprobados en Brave (sesión `langfuse-prueba-hydrogen`) | 6 |
| PERFIL REAL · MEDIDO EL 22/11/2026 | Lotes reales en `resultados/ejemplo-real/` y en el ensayo del prompt defectuoso | 17, 18, 19 |
| ANTES DE VER EL RESULTADO | Recuadro de predicción del grupo | 7, 9, 11, 13 |

Las cifras se tomaron de los archivos guardados; para preparar el deck no se llamó a ningún
modelo. Las salidas de terminal de las diapositivas 14 y 19 se volvieron a ejecutar en local,
sin coste, sobre esos archivos.
