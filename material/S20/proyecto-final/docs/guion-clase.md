# Guion de clase · S20 Proyecto final: agente conversacional

**Miércoles 02/12/2026 · grupo L/X · 18:30–20:00 (Europe/Madrid) · 90 minutos con preguntas.**

Método acordado con la escuela (Laura, 04/11): **teoría de la mano de la práctica**. Cada bloque
tiene una o dos diapositivas de concepto y termina en un momento **EN VIVO** con el proyecto.
Los comandos, en el mismo orden, están en [comandos.md](comandos.md).

La clase se da entera en el **perfil doble** (sin modelo, sin coste, sin claves). Decirlo al
principio y recordarlo cuando aparezca el rótulo `[perfil doble · reglas, sin modelo]`: lo que
se enseña es la arquitectura y la integración, no la calidad de un modelo.

## Cómo se lleva la demo: modo clase

El proyecto ya está terminado: en clase no se programa, se enseña funcionando. Para no teclear
comandos en directo, el modo clase recorre el proyecto en el orden de las diapositivas:

```bash
uv run python demo_clase.py            # 14 pasos; Enter para avanzar
uv run python demo_clase.py --solo 7   # repetir un paso si alguien pregunta
uv run python demo_clase.py --lista    # índice de pasos
```

Cada paso muestra la diapositiva que acompaña, el archivo que hay que abrir, la frase clave, el
comando equivalente (el que pueden escribir los alumnos) y la salida que hay que señalar. Si
PostgreSQL está arrancado lo usa y empieza con las tablas vacías; si no, sigue en memoria y lo dice.

| Paso | Diapositiva | Qué se ve |
|---:|---|---|
| 1 | 6 | Diez comprobaciones de aceptación en verde |
| 2 | 7 | Configuración efectiva y primeras líneas del prompt v1 |
| 3 | 8 | Ruta sin herramientas y ruta con herramientas |
| 4 | 9 | Con el límite a 1, la segunda herramienta no se ejecuta |
| 5 | 10 | Dos procesos: en memoria se olvida, en PostgreSQL se recuerda |
| 6 | 11 | Luis no entra en el hilo de Ana |
| 7 | 12 | API real: 200, 401, 200 y 404; Swagger abierto hasta pulsar Enter |
| 8 | 13 | Herramienta y recurso descubiertos por MCP |
| 9 | 14 | T-100, T-999, T-1 y una herramienta no permitida |
| 10 | 15 | Reingesta sin duplicados y un fragmento con título y sección |
| 11 | 16 | Similitud frente al umbral: cita o «no consta» |
| 12 | 17–18 | Trabajo pendiente → ejecutor → informe → no se duplica |
| 13 | 19 | La línea JSON del turno con su request_id |
| 14 | 22 | `pytest` y `pytest -m db` |

Los comandos sueltos siguen en [comandos.md](comandos.md) por si se prefiere teclearlos.

## Antes de las 18:30

Seguir [checklist.md](../../checklist.md). Lo mínimo: Docker arrancado, `docker compose up -d --wait`,
un ensayo con `uv run python demo_clase.py --sin-pausa`, una terminal en `proyecto-final/` con
fuente grande y el editor con `agente/grafo.py`.

## Recorrido

| Hora | Diap. | Bloque | Qué se explica | EN VIVO |
|---|---|---|---|---|
| 18:30 | 1 | Apertura | Qué vamos a montar: un agente que integra todo el curso | — |
| 18:31 | 2 | Apertura | QR de la encuesta de **S19 (30/11)** y plan de la sesión | Dejar el QR un minuto |
| 18:33 | 3 | Apertura | El caso del técnico y las tres fuentes de verdad | — |
| 18:36 | 4 | 1 · Proyecto | Cada pieza viene de una sesión que ya dimos | — |
| 18:39 | 5 | 1 · Proyecto | Planificar: requisitos, alcance, orden y criterio de aceptación | — |
| 18:42 | 6 | 1 · Proyecto | Arquitectura completa | `uv sync` · `uv run python -m agente.cli recorridos` (todo verde) |
| 18:45 | 7 | 2 · Agente | Prompt versionado y configuración por entorno | Abrir `config.py` y `prompts.py` |
| 18:49 | 8 | 2 · Agente | Estado, nodos, aristas y bucle | Abrir `grafo.py` · `chat "Hola, ¿qué puedes hacer?"` y leer `ruta` |
| 18:54 | 9 | 2 · Agente | El modelo propone, el código ejecuta; límite por turno | `S20_MAX_HERRAMIENTAS=1 … chat "Mira el ticket T-100 y consulta la política aplicable"` |
| 18:58 | 10 | 3 · Memoria y API | Checkpointer por `thread_id`; tres familias de tablas | Turno con T-200, **otro proceso** pregunta «¿Qué ticket estábamos viendo?» |
| 19:03 | 11 | 3 · Memoria y API | `thread_id` no autoriza | Mismo hilo con `--usuario luis` → rechazado |
| 19:07 | 12 | 3 · Memoria y API | Contrato de la API; `/health` no llama al modelo | `uvicorn` · `/docs` · `curl /health` · `curl /chat` con y sin token |
| 19:12 | 13 | 4 · MCP y RAG | Servidor MCP propio: herramienta y recurso | `cli mcp` · abrir `servidor_mcp/tickets.py` |
| 19:17 | 14 | 4 · MCP y RAG | Qué pasa en una llamada: descubrir, comprobar, llamar | T-100 (existe) · T-999 (no existe) |
| 19:20 | 15 | 4 · MCP y RAG | De documento a fragmento con cita | `cli ingestar` dos veces · pregunta del plan Estándar |
| 19:25 | 16 | 4 · MCP y RAG | Umbral de evidencia: responder o rechazar | Pregunta de teletrabajo → «No consta» |
| 19:28 | 17 | 5 · Deep Research | Investigar con límites; interno y público no se mezclan | — |
| 19:33 | 18 | 5 · Deep Research | La investigación es un trabajo con estado | Caso completo → `cli investigar` → repetir el caso → `--ver INV-…` |
| 19:38 | 19 | 6 · Observar y desplegar | Seguir un turno: `request_id`, ruta, traza | Línea JSON del turno en la terminal de `uvicorn` (Langfuse si hay claves) |
| 19:42 | 20 | 6 · Observar y desplegar | Lo mismo en AWS: qué cambia y qué no | Abrir `infra/plantilla.json`; no se despliega en directo |
| 19:46 | 21 | 6 · Observar y desplegar | Los límites están en el código | — |
| 19:48 | 22 | 7 · Entrega y cierre | Recorridos de aceptación y pirámide de tests | `uv run pytest` · `uv run pytest -m db` |
| 19:51 | 23 | 7 · Entrega y cierre | Qué se entrega y cómo se valora (propuesta) | Abrir `docs/ejercicio.md` |
| 19:54 | 24 | 7 · Entrega y cierre | Lo que nos llevamos y preguntas | — |

## Frases que conviene decir tal cual

- «El perfil doble no es un modelo: son reglas. Lo que es real es todo lo demás.»
- «`thread_id` dice qué conversación es; no dice quién puede leerla.»
- «El modelo no ejecuta nada: propone. El código decide.»
- «Un ticket que no existe es una respuesta, no un error.»
- «Si no hay evidencia, la respuesta correcta es "no consta".»
- «Un informe parcial que dice lo que falta es mejor que uno completo inventado.»
- «La información pública nunca sustituye a una política interna.»

## Preguntas de comprobación (una por bloque)

1. ¿Qué pieza del proyecto cambiarías para usar otro proveedor de modelos? (`config.py`: una variable.)
2. ¿Dónde está el límite de herramientas por turno: en el prompt o en el código? (En `grafo.py`.)
3. Si conozco el `thread_id` de otra persona, ¿puedo leer su conversación? (No: 404.)
4. ¿Por qué el agente no abre directamente `tickets.json`? (El sistema de tickets tiene su propio contrato: MCP.)
5. ¿Qué devuelve la investigación si una de las preguntas no tiene fuente? (Informe parcial con `faltan`.)
6. ¿Qué demuestra `/health`? (Que el proceso vive; no que el modelo responda.)
7. ¿Qué evidencia enseñarías para decir que tu proyecto funciona? (Los recorridos de aceptación.)

## Si algo falla en directo

| Fallo | Qué hacer |
|---|---|
| Docker no arranca | Seguir con `S20_ALMACEN=memoria` y `cli recorridos`; enseñar la memoria con el test `test_postgres.py` leído en el editor |
| Puerto 54520 u 8020 ocupado | Cambiar el puerto en `compose.yaml` / `--port` y `S20_DATABASE_URL` |
| No hay internet | Todo funciona sin red; no usar `S20_FUENTES=red` |
| Langfuse no disponible | Enseñar la línea JSON del turno: lleva el mismo `request_id` |
| Se alarga un bloque | Recortar las diapositivas 14, 16 y 21: su contenido está también en 13, 15 y 9 |

## Lo que NO se afirma en clase

- No se ha ejecutado el perfil real: no hay tokens, coste ni latencia medidos con modelo.
- No se ha desplegado en AWS: la plantilla está validada con `cfn-lint`, no probada en una cuenta.
- La propuesta de valoración de la entrega no es una norma de thePower hasta que la escuela la confirme.
