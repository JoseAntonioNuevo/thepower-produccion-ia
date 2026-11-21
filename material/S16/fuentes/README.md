# Fuentes editables de los materiales

El PPTX contiene texto, tablas y notas editables. Los Markdown de guion y guía son la fuente de sus PDF. Para el alumno basta con los archivos finales; no necesita ejecutar los generadores.

`generar-presentacion.mjs` utiliza `@oai/artifact-tool` del runtime de documentos de Codex y LibreOffice para exportar el PDF. Ejecutarlo desde una copia en `.build/deck/`, con un enlace `node_modules` al runtime y las variables:

- `S16_ROOT`: raíz absoluta de este proyecto.
- `S16_PRESENTATION_SKILL`: carpeta de la skill Presentations instalada.
- `S16_RUNTIME_PYTHON`: Python del runtime de documentos.
- `RUNTIME_NODE_MODULES`: módulos Node del runtime de documentos.
- `S16_SOFFICE`: opcional, ejecutable de LibreOffice si no está en PATH.

La herramienta `load_workspace_dependencies` informa de esas rutas en cada host. No instalar un paquete distinto con el mismo nombre ni copiar rutas de otro equipo. El finalizador conserva candidato, comprobaciones y revisiones en `.build`, y copia el PPTX validado a la carpeta canónica.

`generar-pdf.py RAIZ` usa ReportLab y las fuentes Arial/Courier New del Mac. Se ejecutó con el Python del runtime de documentos. En otro host deben proporcionarse fuentes disponibles equivalentes y revisarse el renderizado. Los generadores no son dependencias de la API ni de sus tests.

Después de cambiar contenido: regenerar, revisar todas las páginas/diapositivas afectadas, comprobar notas/cifras/QR, actualizar la matriz si cambia la numeración y volver a generar los paquetes con `uv run python scripts/empaquetar.py`.
