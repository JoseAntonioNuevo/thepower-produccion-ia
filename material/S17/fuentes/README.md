# Fuentes editables de S17

`generar-presentacion.mjs` utiliza la misma composición, fuentes y herramientas de S16. Las notas del orador tienen una fuente única legible en `notas.json`. El PPTX final contiene texto y tablas editables.

Copiar el generador a `.build/s17/deck/` y enlazar allí los módulos del runtime de documentos de Codex. La herramienta `load_workspace_dependencies` informa las rutas del host. Variables: `S17_ROOT`, `S17_PRESENTATION_SKILL`, `S17_RUNTIME_PYTHON`, `RUNTIME_NODE_MODULES` y, opcionalmente, `S17_SOFFICE`. El finalizador crea versiones privadas y copia la validada al destino canónico; LibreOffice genera el PDF.

`generar-pdf.py RAIZ` transforma los Markdown del guion y guía con ReportLab y fuentes Arial/Courier New del Mac. En otro host hay que proporcionar fuentes disponibles y revisar la maquetación. El alumno no necesita las herramientas de autoría para ejecutar la API o la práctica.

Después de una modificación: regenerar, revisar las páginas afectadas, comprobar QR/notas/cifras, actualizar cobertura si cambia la numeración y generar de nuevo los paquetes. Los materiales de S16 se conservan como referencia independiente.

