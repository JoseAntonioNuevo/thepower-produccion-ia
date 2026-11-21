# S20 · Proyecto final: agente conversacional

**AI Engineer · grupo L/X · miércoles 02/12/2026 · 18:30–20:00 (Europe/Madrid)**
Profesor: José Antonio Nuevo. Última sesión del programa para el grupo L/X.
La S20 del grupo M/J (26/11) la imparte Ignacio: este material no la sustituye.

El QR de la diapositiva 2 evalúa **S19 del lunes 30/11** (la sesión anterior del grupo L/X).

## Qué hay en esta carpeta

| Pieza | Para qué |
|---|---|
| [presentaciones/S20-proyecto-final.pptx](presentaciones/S20-proyecto-final.pptx) | Teoría de la clase: 24 diapositivas con notas del orador (y [PDF](presentaciones/S20-proyecto-final.pdf)) |
| [proyecto-final/](proyecto-final/README.md) | Proyecto de referencia: agente LangGraph + MCP + RAG + Deep Research + PostgreSQL + Langfuse + FastAPI, listo para AWS |
| [proyecto-final/demo_clase.py](proyecto-final/demo_clase.py) | Modo clase: `uv run python demo_clase.py` enseña el proyecto en 14 pasos, en el orden de las diapositivas |
| [proyecto-final/docs/guion-clase.md](proyecto-final/docs/guion-clase.md) | Guion de 90 minutos: hora, diapositiva y qué se hace en vivo |
| [proyecto-final/docs/comandos.md](proyecto-final/docs/comandos.md) | Comandos en el orden de la presentación |
| [proyecto-final/docs/ejercicio.md](proyecto-final/docs/ejercicio.md) | Proyecto final paso a paso para el alumno (entregables y valoración propuestos) |
| [proyecto-final/docs/arquitectura.md](proyecto-final/docs/arquitectura.md) | Arquitectura, decisiones y límites |
| [proyecto-final/docs/despliegue-aws.md](proyecto-final/docs/despliegue-aws.md) | Despliegue en ECS Fargate + RDS (no ejecutado) |
| [enunciado.md](enunciado.md) | Enunciado del proyecto final para publicar, con lo que consta y lo que falta confirmar |
| [cobertura.md](cobertura.md) | Cada punto del temario → diapositiva, demo y archivo |
| [checklist.md](checklist.md) | Lista previa al directo |
| [verificacion.md](verificacion.md) | Qué se comprobó, con qué comando y resultado; qué queda pendiente |
| [fuentes.md](fuentes.md) | Correos, documentación oficial y procedencia de imágenes |
| [fuentes/presentacion/](fuentes/presentacion/README.md) | Fuente editable de la presentación (python-pptx) y logotipos |

## Estado real (17/11/2026)

- **Verificado en local, perfil doble (sin modelo):** 38 tests sin red, 5 tests con PostgreSQL,
  diez comprobaciones de aceptación en memoria, en PostgreSQL y con fuentes leídas en red, API con
  `curl`, imagen Docker construida y arrancada, plantilla de CloudFormation sin avisos de `cfn-lint`.
- **No ejecutado:** perfil real con un modelo (coste), traza real en Langfuse (faltan claves de un
  proyecto de laboratorio) y despliegue en AWS (recursos de pago).
- **Sin confirmar con la escuela:** formato del directo, fecha de entrega y rúbrica del proyecto
  final. La valoración del material es una propuesta.

## Enfoque de la clase

Laura pidió el 04/11 «contar la teoría de la mano de la práctica» y un repositorio «menos denso».
Por eso cada bloque de la presentación termina en una franja **EN VIVO** con el comando que se
ejecuta, y el proyecto son doce archivos de Python cortos, uno por paso, que funcionan sin claves.

En clase no se programa: el proyecto ya está terminado y se enseña paso a paso con
`uv run python demo_clase.py` (Enter para avanzar). Los alumnos lo construyen después, como
entrega, con la [guía paso a paso](proyecto-final/docs/ejercicio.md).
