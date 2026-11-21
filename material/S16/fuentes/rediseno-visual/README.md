# Fuente editable de S16

## Versión vigente · OpenRouter y Estocolmo · 11/11/2026

La presentación canónica tiene **33 diapositivas**: 23 de conceptos, 6 de demo,
práctica, cierre y dos de consulta. Conserva el diseño de la versión original
(paleta oscura, Arial/Georgia/Courier New, QR, iconos y diagramas editables).

`actualizar-demo-openrouter.mjs` importa la base archivada con Artifact Tool,
actualiza textos/notas y crea el bloque práctico. `ordenar-demo-openrouter.py`
ordena el bloque antes de práctica y cierre y ajusta los números de página
mediante OOXML; solo usa la biblioteca estándar de Python.

Desde la raíz de `4-produccion-ia`, con Node y `@oai/artifact-tool` disponibles:

```bash
mkdir -p .build/ppt-audit
node material/S16/fuentes/rediseno-visual/actualizar-demo-openrouter.mjs \
  material/S16/fuentes/rediseno-visual/referencias/S16-base-2026-11-06.pptx \
  .build/ppt-audit/updated-draft.pptx
python3 material/S16/fuentes/rediseno-visual/ordenar-demo-openrouter.py \
  .build/ppt-audit/updated-draft.pptx .build/ppt-audit/ordered-draft.pptx
```

Validar el candidato con el finalizador de Presentations antes de reemplazar
el PPTX canónico; exportar y revisar el PDF desde ese mismo archivo final.
La validación y el render del 11/11 están en `.build/ppt-audit/`.
Las cifras de Estocolmo se basan en `demo-openrouter/aws/tarifas-2026-11-11.json`.

Los generadores `build_clase.py` y `build.py` descritos debajo conservan la versión
histórica del 06/11; no regeneran la demo vigente de OpenRouter.

---

# Fuente editable del rediseño visual de S16

Genera `presentaciones/S16-cloud-aws-rediseno-visual.pptx` y, con LibreOffice, su PDF. La versión vigente para clase es la reducida (27 diapositivas, `build_clase.py`): los formularios se enseñan en la consola en vivo y el contenido de las diapositivas retiradas pasa a las notas. `build.py` genera la versión completa de 51 diapositivas como consulta.
Es la versión centrada en recorrer la consola de AWS; `S16-cloud-docker.pptx` se conserva como fuente original.

## Archivos

- `deck_lib.py`: sistema visual tomado de S12 (paleta, Georgia/Arial/Courier New, cabecera, navegación por bloques, idea guía, esquemas de consola, tablas).
- `deck_part1.py` … `deck_part5.py`: diapositivas y notas del orador por bloques (apertura y orientación; cómputo, datos y red; contenedores; operar y pagar; IA gestionada, cierre y consulta).
- `build.py`: construye el PPTX. `check.py`: notas, límites del lienzo, QR y logotipo byte a byte.
- `fonts.conf`: hace que LibreOffice use las fuentes del sistema macOS (Arial, Georgia, Courier New) en lugar de sustitutas.
- `assets/`: iconos y logotipos oficiales convertidos a PNG y recortes de capturas. El logotipo de thePower y el QR se leen de `../../assets/` sin modificar.

## Regenerar

Desde esta carpeta, con un Python que tenga `python-pptx` y `pillow`:

```bash
python build_clase.py ../../presentaciones/S16-cloud-aws-rediseno-visual.pptx
# versión completa (51): python build.py SALIDA.pptx deck_part1 deck_part2 deck_part3 deck_part4 deck_part5
python check.py ../../presentaciones/S16-cloud-aws-rediseno-visual.pptx
FONTCONFIG_FILE="$PWD/fonts.conf" soffice --headless --convert-to pdf \
  --outdir ../../presentaciones ../../presentaciones/S16-cloud-aws-rediseno-visual.pptx
```

Después: renderizar el PDF y revisar todas las páginas, comprobar que `pdffonts` muestra Arial, Georgia y Courier New, decodificar el QR de la página 2 y, si cambian tarifas o cantidades, recalcular con `scripts/costes.py` y actualizar las diapositivas de coste mensual, coste de la demo y la tabla de consulta.

## Procedencia de imágenes

- AWS Architecture Icons, paquete del 31/07/2026 (aws.amazon.com/architecture/icons).
- Logotipo de AWS: `a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png`, recortado; la versión para fondo claro es su variante monocroma en Squid Ink (#232F3E).
- Azure Public Service Icons V25 y Microsoft Entra architecture icons (Microsoft permite su uso en diagramas, formación y documentación).
- Google Cloud: `www.gstatic.com/cgc/google-cloud-logo-fullcolor.svg`, core products icons y legacy icons de cloud.google.com/icons.
- Docker: `docker.com/static/Docker-Logos-1.zip`.
- Capturas oficiales: modelo de responsabilidad compartida (aws.amazon.com/compliance/shared-responsibility-model) y Resource map de la VPC User Guide; captura propia de la página pública calculator.aws del 06/11/2026.
- Las pantallas rotuladas «ESQUEMA» son dibujos propios, no capturas.
