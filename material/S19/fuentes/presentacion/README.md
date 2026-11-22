# Fuente editable de la presentación de S19

Genera `../../presentaciones/S19-evaluacion-testing.pptx` (32 diapositivas, 32 notas, 15 tablas
nativas) y, con LibreOffice, su PDF. Texto, tablas, diagramas y barras son **formas nativas
editables**; las únicas imágenes son logotipos, iconos y el QR.

## Diseño: manda el ejemplo

El diseño reproduce el PowerPoint de ejemplo que pasó José (19 diapositivas de S17; copia de
trabajo y renders en `.build/s19/ref/`). Se desmontó su XML y se midieron posiciones, tamaños,
tipografías y colores. El ejemplo combina **dos estilos**, y esta presentación usa los dos
con las mismas medidas:

| Estilo del ejemplo | Medidas (pt, lienzo 960 × 540) | Dónde se usa aquí |
|---|---|---|
| Portada | Fondo `123630`; logotipo en 38,34 (alto 32); antetítulo Arial 10 negrita `4FD1A1` en y=104; título Georgia 36 en y=124; descripción Arial 12,5; autor en y=322; panel 497,52 de 420 × 410 con borde `2A5246` | 1 |
| Sencillo | Antetítulo Arial 9,75 en y=25,5; título Georgia 27 en y=51,8; entradilla Arial 13,5 en y=100,5; paneles rectos `18272E` con borde `33474F`; filas clave → texto a 15,75; banda `133A30` en y=463,5; pie en y=511,5 con navegación en texto corrido | 2, 3, 7, 11, 18, 23, 28 |
| Completo | Antetítulo Arial 9 en y=25; título Georgia 27 en y=41; entradilla Arial 12,5 en y=85; tarjetas redondeadas; banda «IDEA GUÍA» en y=476; pie en y=513 con bloques numerados y el activo en su color | 4–6, 8–10, 12–17, 19–22, 24–27 |
| Cierre | Fondo `123630`; «CIERRE» en y=84; título Georgia 32; lista numerada con círculos `A8F0D0`; panel `1A463C` con «¿Preguntas?» | 29 |

Paleta: fondo `0F1B22`, tarjetas `18272E`, bordes `33474F`, títulos `EAF1F2`, texto `C3D0D4`,
menta `4FD1A1`. Tipografías: Georgia (títulos), Arial (texto), Courier New (código).
Color por bloque: 1 menta, 2 rosa, 3 ámbar, 4 violeta, 5 azul, cierre menta claro.

Diferencia deliberada con el ejemplo: la diapositiva 2 conserva el QR y su pie en la misma
posición, y añade a los lados el plan de la sesión y qué sesión se valora en cada grupo,
porque una sola presentación sirve para las dos fechas.

## Archivos

- `deck_lib.py`: copia adaptada de `material/S17/fuentes/rediseno-visual/deck_lib.py` (no se
  modifica el original). Cambian los bloques, el pie y las rutas; al final van los añadidos de
  S19: estilo sencillo, portada, cierre, barras, fichas de documento y paneles de terminal.
- `deck_part1.py` (1–14), `deck_part2.py` (15–26), `deck_part3.py` (27–32): diapositivas y notas.
- `build.py`: genera el PPTX. `check.py`: 32 diapositivas, notas completas, límites del lienzo,
  tipografías, QR y logotipo byte a byte.
- `preparar_assets.py`: crea las teselas blancas de pytest y Ragas a partir de las descargas.
- `fonts.conf`: copia del de S17; hace que LibreOffice use Arial, Georgia y Courier New.

## Regenerar

```bash
cd material/S19/fuentes/presentacion
uv run --no-project --with python-pptx --with pillow --with lxml python -I build.py ../../presentaciones/S19-evaluacion-testing.pptx
uv run --no-project --with python-pptx --with pillow --with lxml python -I check.py ../../presentaciones/S19-evaluacion-testing.pptx
```

PDF e imágenes (LibreOffice y Poppler del runtime local; no hay `soffice` en el PATH):

```bash
RT=~/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override
FONTCONFIG_FILE="$PWD/fonts.conf" $RT/soffice --headless --convert-to pdf --outdir ../../presentaciones ../../presentaciones/S19-evaluacion-testing.pptx
$RT/pdftoppm -png -r 80 ../../presentaciones/S19-evaluacion-testing.pdf /tmp/s19
```

`build.py` imprime dos avisos de «posible desborde» (pie del QR y título de la 24). Son
estimaciones conservadoras: en el render ambos caben; el título de la 24 ocupa una línea.

## Procedencia de las imágenes

| Archivo en `assets/` | Qué es | Origen | Fecha |
|---|---|---|---|
| `../../assets/qr-ai-engineer.jpg` | QR vigente de AI Engineer | Copia byte a byte de `material/S16/assets/qr-ai-engineer.jpg` (Laura, 19/10/2026) | 17/11/2026 |
| `../../assets/thepower-logo.png` | Logotipo de thePower | Copia byte a byte de `material/S17/assets/thepower-logo.png` | 17/11/2026 |
| `postgresql.png` | Logotipo de PostgreSQL | <https://www.postgresql.org/media/img/about/press/elephant.png> (kit de prensa oficial) | 17/11/2026 |
| `python.png` | Logotipo de Python | <https://www.python.org/static/img/python-logo.png> | 17/11/2026 |
| `pytest-tile.png` | Logotipo de pytest sobre tesela blanca | <https://raw.githubusercontent.com/pytest-dev/pytest/main/doc/en/img/pytest_logo_curves.svg>, convertido con Quick Look | 17/11/2026 |
| `ragas-tile.png`, `ragas-wordmark.png` | Logotipo de Ragas (tesela con el símbolo; marca completa sin usar) | <https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/_static/imgs/logo.png> | 17/11/2026 |
| `langfuse.png` | Icono de Langfuse | <https://raw.githubusercontent.com/langfuse/langfuse/main/web/public/icon256.png> | 17/11/2026 |
| `docker-mark-white.png` | Marca de Docker | Copia de `material/S17/fuentes/rediseno-visual/assets/` | 17/11/2026 |
| `g-*.png` | Iconos genéricos de línea | Copia de `material/S17/fuentes/rediseno-visual/assets/` (su procedencia está en el README de S17) | 17/11/2026 |

Los logotipos pertenecen a sus titulares y se usan solo para identificar cada herramienta.
No hay capturas de pantalla ni diagramas de documentación de terceros: todos los diagramas
están dibujados con formas nativas.

## Rótulos de procedencia de los datos en las diapositivas

| Rótulo | Significado | Diapositivas |
|---|---|---|
| SALIDA REAL DEL PERFIL DOBLE · 17/11/2026 | Salida de la demo ejecutada en local con dobles. No mide ningún modelo | 11, 22, 23, 24 |
| PERFIL DOBLE · no mide ningún modelo | Cifras de `resultados/ejemplo-doble` | 7, 10, 17 |
| EJEMPLO ILUSTRATIVO · no es una medición | Números construidos para explicar un cálculo | 9, 12, 13, 16, 25 |
| ESQUEMA · no es una captura | Dibujo de lo que registra el código; Langfuse no se ejecutó | 26 |
| PERFIL REAL · MEDIDO EL 22/11/2026 | Coste y aciertos medidos con modelos reales vía OpenRouter (`resultados/ejemplo-real`) | 31 |
