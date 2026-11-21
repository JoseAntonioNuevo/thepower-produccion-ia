# Fuente editable de la presentación S20

`presentaciones/S20-proyecto-final.pptx`: **24 diapositivas**, todas con notas del orador (tiempo,
qué explicar, qué ejecutar en vivo, pregunta de comprobación, fuentes e imágenes).

El diseño es el del PowerPoint de ejemplo `S17-serverless-ai.pptx`: lienzo 960 × 540 pt, fondo
`0F1B22`, portada y cierre en `123630`, tarjetas `18272E`, acento menta `4FD1A1`, Georgia para
títulos, Arial para texto y Courier New para código; antetítulo, título, entradilla, banda
«IDEA GUÍA» y pie con navegación por bloques. Texto y tablas son editables.

## Archivos

- `deck_lib.py`: copia del sistema visual de S17 (`material/S17/fuentes/rediseno-visual/deck_lib.py`)
  con los bloques de S20 y cinco añadidos: `en_vivo`, `panel`, `codigo`, `encajar` (logotipos sin
  deformar), `nodo` y `nota` (notas con formato fijo). El archivo de S17 no se ha modificado.
- `comun.py`: textos de procedencia compartidos.
- `deck_part1.py` … `deck_part4.py`: diapositivas 1–6, 7–12, 13–18 y 19–24.
- `build.py`: construye la presentación. `check.py`: notas, límites del lienzo, QR vigente y logotipo.
- `scripts/preparar_assets.py`: convierte los logotipos de `descargas/` a PNG en `assets/` y copia los
  iconos de AWS de S16/S17.
- `fonts.conf`: hace que LibreOffice use las fuentes del sistema al exportar a PDF.

## Regenerar

Desde esta carpeta:

```bash
uv run --no-project --with resvg-py --with pillow python scripts/preparar_assets.py   # solo si cambian los logotipos
uv run --no-project --with python-pptx --with pillow --with lxml python build.py ../../presentaciones/S20-proyecto-final.pptx
uv run --no-project --with python-pptx --with pillow --with lxml python check.py ../../presentaciones/S20-proyecto-final.pptx
FONTCONFIG_FILE="$PWD/fonts.conf" soffice --headless --convert-to pdf \
  --outdir ../../presentaciones ../../presentaciones/S20-proyecto-final.pptx
```

En este Mac `soffice` y `pdftoppm` no están en el PATH: se usaron los del runtime local
`~/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/`.

Después de regenerar: revisar las 24 páginas del PDF y, si cambian resultados del proyecto,
actualizar los valores medidos (diapositivas 10, 14, 16, 17 y 22) con las evidencias nuevas.

## Valores que aparecen en las diapositivas

Todos salen de ejecuciones locales del perfil doble: similitudes de la diapositiva 16
(`agente.rag.recuperar` con ocho preguntas), tiempos MCP de la 14, recorridos de
`proyecto-final/evidencias/`, línea de log y `curl` de la 12 y la 19 (prueba de la API del 16/11).
Ninguno es una medición de un modelo.

Procedencia de los logotipos: [../../fuentes.md](../../fuentes.md#imágenes-de-la-presentación).
