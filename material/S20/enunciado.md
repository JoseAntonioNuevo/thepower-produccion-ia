# Proyecto final · Agente conversacional

**AI Engineer · thePower · S20**

> **Estado de este enunciado.** El temario de thePower describe el contenido del proyecto final y
> pide su entrega. En los correos revisados no constan formato de entrega, fecha límite ni rúbrica.
> Los apartados «Entrega» y «Valoración» son la **propuesta del profesor**, pendiente de confirmar
> con la escuela antes de publicarlos como requisito.

## Lo que pide el temario

Texto original del temario (correo de Laura del 17/07/2026; copia en
[fuentes/temario-S20-original.txt](fuentes/temario-S20-original.txt)):

> Integrar todo lo aprendido en un único proyecto. Agente conversacional: introducción al proyecto
> y planificación, prompts y configuración del agente, construcción del grafo, módulos y
> herramientas, aplicación, integración con PostgreSQL, integración con Langfuse, exposición vía
> FastAPI, integración con MCPs y despliegue en AWS / Deep-research + RAG: extensión del agente con
> capacidades de investigación autónoma combinadas con recuperación de información propia /
> Integración de todos los componentes. Entrega de este proyecto final.

(Erratas del original corregidas en esta cita; el texto literal está en la copia.)

## Qué tienes que construir

Un agente conversacional sobre un caso tuyo (puedes conservar el de referencia, AetherCloud) que:

1. responda directamente cuando no necesita herramientas;
2. consulte un dato de negocio a través de un **servidor MCP propio**;
3. diga explícitamente cuándo ese dato no existe;
4. responda **con cita** usando documentación propia (**RAG** con PostgreSQL + pgvector);
5. **rechace** cuando no hay evidencia suficiente;
6. registre y complete una **investigación** sobre fuentes públicas con límites, sin duplicarla;
7. **recuerde** la conversación tras reiniciar (**PostgreSQL**) y no la muestre a otro usuario;
8. se use a través de una **API FastAPI** y deje una traza por turno (log y, opcionalmente, **Langfuse**);
9. pueda empaquetarse en un contenedor y desplegarse en **AWS** (el despliegue real es opcional).

El proyecto de referencia [proyecto-final/](proyecto-final/README.md) cumple los nueve puntos y
se puede usar como punto de partida. La guía [paso a paso](proyecto-final/docs/ejercicio.md)
divide el trabajo en diez pasos con una comprobación cada uno; los pasos 0–8 no necesitan claves
ni tienen coste.

## Entrega (propuesta)

1. Repositorio o ZIP con un README que explique el caso y cómo ejecutarlo desde cero.
2. `evidencias/recorridos-….json`, generado con `uv run python -m agente.cli recorridos --guardar`.
3. Ocho preguntas propias (cinco con respuesta en tu documentación y tres sin respuesta) con su resultado.
4. Media página de límites: qué no hace tu agente, qué falló y qué mejorarías.

Sin claves, tokens ni datos personales en el repositorio. Todos los datos, ficticios.

## Valoración (propuesta)

| Criterio | Peso |
|---|---:|
| Funcionamiento y recorrido completo | 25 % |
| RAG, fuentes y rechazo | 20 % |
| Memoria, aislamiento y límites | 15 % |
| Herramienta MCP e investigación integrada | 15 % |
| Observabilidad, evaluación y tests | 15 % |
| Reproducción, despliegue, coste y documentación | 10 % |

## Dedicación orientativa

Pasos 0–8 de la guía: unas 6 horas con el proyecto de referencia como base. El paso 9 (modelo
real, AWS, Langfuse) es opcional y depende de los accesos de cada alumno.
