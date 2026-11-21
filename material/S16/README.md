# S16 · Cloud deployment con AWS y Docker

**Versión común: 12 de noviembre (M/J) y 18 de noviembre (L/X) de 2026 · 18:30–20:00 Europe/Madrid.** El QR evalúa S15. La práctica es opcional.

## Presentación vigente · 11/11/2026

- [PowerPoint editable](presentaciones/S16-cloud-aws-rediseno-visual.pptx).
- [PDF](presentaciones/S16-cloud-aws-rediseno-visual.pdf).
- [Fuente de la actualización](fuentes/rediseno-visual/README.md).

**33 diapositivas:** 1–23 conceptos; 24–29 demo manual, validación, limpieza y agente;
30 práctica; 31 cierre; 32–33 consulta. Región Estocolmo `eu-north-1`, API pequeña
con OpenRouter y `openai/gpt-6-luna`. Las notas están actualizadas al recorrido
ensayado el 11/11 y distinguen lo preparado de lo que se despliega en clase.

## Material vigente para la demo

- [Guion breve para Obsidian](demo-openrouter/GUION-OBSIDIAN.md).
- [Prompt del agente para el profesor](demo-openrouter/PROMPT-AGENTE-AWS.md).
- [Resultado de la prueba completa del agente](demo-openrouter/DEMO-AGENTE-RESULTADO.md).
- [README de la API](demo-openrouter/README.md).
- [Guion adaptado para alumnos](demo-openrouter/docs/guion-clase.md).
- [Prompt adaptado para alumnos](demo-openrouter/docs/prompt-agente.md).
- [Repositorio público](https://github.com/JoseAntonioNuevo/thepower-aws).

El despliegue y la retirada se han probado realmente: salud, clasificación con
OpenRouter, logs, imagen por digest y limpieza verificada. Antes del directo
comprobar sesión, conexión/VPN, IP permitida y saldo del proveedor. La IP de una
tarea es temporal. El secreto y los logs conservados pueden generar coste.

## Material anterior

`S16-cloud-docker.*`, los guiones generales y paquetes S16-inicio/S16-referencia
corresponden a la implementación anterior con Anthropic. Se conservan como
referencia; para esta demo prevalecen la presentación y `demo-openrouter/`.
