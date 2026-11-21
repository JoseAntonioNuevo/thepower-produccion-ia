# S19 · Guion de clase (90 minutos)

**Evaluación y testing de sistemas de IA** · AI Engineer · 18:30–20:00 Europe/Madrid.
Mismo guion para M/J (24/11/2026) y L/X (30/11/2026). La clase **no depende de la demo de
S18**: todo corre en local con el perfil `doble`, sin claves y sin coste.

Método pedido por la escuela: teoría de la mano de la práctica. Cada bloque termina con un
momento **EN VIVO** en la terminal. Los comandos, en orden, están en [comandos.md](comandos.md).

> Todo lo que se ejecuta en directo usa el perfil doble. Dilo en voz alta la primera vez:
> «estas cifras comprueban el sistema de evaluación; no miden ningún modelo».

## Antes de conectar (18:15)

Contenedor arrancado, `preflight` correcto, índices A y B creados, terminal con letra grande
en `demo-evaluacion/`, editor con `datos/test.jsonl` y `evaluacion/metricas.py` abiertos.
Lista completa en [../../checklist.md](../../checklist.md).

## Horario

| Hora | Min | Bloque | Diapositivas | En diapositiva | En vivo |
|---|---:|---|---|---|---|
| 18:30 | 3 | Apertura | 1–2 | QR de la sesión anterior y plan | — |
| 18:33 | 6 | Punto de partida | 3–5 | **Qué es evaluar** (casos → ejecutar → puntuar → agregar → decidir; software clásico frente a IA; código, juez LLM o persona); **tests, evaluación offline y online** (tres redes); **seis casos de uso** y herramientas | Preguntar cómo deciden hoy si un cambio mejora y cuál de los seis casos les ha pasado |
| 18:39 | 2 | Caso conductor | 6 | Caso AetherCloud: chunk_size 320 → 900 | — |
| 18:41 | 10 | 1 · Qué medir | 7–10 | Modelo frente a sistema, anatomía de una evaluación, dónde se mide en un RAG | **Vivo 1:** `preflight`, `test.jsonl`, `ingestar`, dos `preguntar` |
| 18:51 | 15 | 2 · Recuperación | 11–14 | precision@5, recall@5, denominadores, ejemplo con fichas, rechazo aparte | **Vivo 2:** `calibrar`, `lote` de validación, `informe` |
| 19:06 | 18 | 3 · Generación | 15–21 | Faithfulness, Answer Relevancy, LLM como juez, evaluador aislado, no evaluables, revisión humana | **Vivo 3:** `evaluar.py`, `puntuaciones.jsonl`, CSV de revisión (T16) |
| 19:24 | 14 | 4 · Testing | 22–26 | Pirámide, dobles y `@pytest.mark.llm`, tests de agentes, umbrales con margen | **Vivo 4:** `pytest`, `umbrales`, `regresion` pasa, `degradar`, `regresion` falla |
| 19:38 | 13 | 5 · Producción | 27–30 | Una sola variable, métricas de producción, Langfuse, ciclo offline ↔ online | **Vivo 5:** `comparar` A/B, `rag/observabilidad.py` |
| 19:51 | 4 | Práctica | 31 | Enunciado opcional, entrega, coste estimado | `estimar` |
| 19:55 | 5 | Cierre | 32 | Cinco ideas y preguntas | — |

Si vas con retraso: recorta Vivo 5 a la tabla de la diapositiva 27 y salta la 24 (agentes),
que queda como lectura. No recortes Vivo 4: es la demostración central.

## Apertura · 18:30–18:33

- **Diapositiva 2.** QR: evalúa la sesión anterior de cada grupo (S18 del 19/11 para M/J;
  S18 del 25/11 para L/X). Dos minutos con el QR en pantalla.
- **Diapositiva 6 (18:39).** Caso: el asistente de soporte de AetherCloud (ficticio). Alguien propone
  cambiar el tamaño de fragmento de 320 a 900. Pregunta de la sesión: *¿cómo sabemos si mejora?*

## Punto de partida · 18:33–18:39

- **Diapositiva 3 · Qué es evaluar.** Los cinco pasos (casos fijados antes → ejecutar → puntuar →
  agregar → decidir con un umbral) y la vuelta: lo que falla entra al conjunto. Tabla «software clásico
  frente a sistema con IA» y las tres formas de puntuar (código, juez LLM, persona) según la guía de
  evaluación de Anthropic.
- **Diapositiva 4 · Tests, evaluación y producción.** El recorrido de un cambio (desarrollo → PR → antes
  de publicar → producción) con tres carriles: tests con dobles, evaluación offline y evaluación online.
  Enlaza con S18 (CI en la PR) y con el bloque 5 (Langfuse).
- **Diapositiva 5 · Casos de uso.** Seis situaciones con «sin» y «con» y su etiqueta (TEST, EVALUACIÓN,
  PRODUCCIÓN); abajo, pytest, Ragas y Langfuse (las de la demo) y otras herramientas solo nombradas.
- **Preguntas:** «¿Cómo decidís hoy si un cambio de prompt es mejor?» y «¿Cuál de los seis casos os ha pasado?».

## Bloque 1 · Qué medir · 18:41–18:51

Explica (7–9): una métrica de modelo (exactitud en un benchmark) no dice si **tu** sistema
funciona; el sistema añade recuperación, prompt, rechazo, latencia y coste. Una evaluación
tiene cuatro piezas: casos, referencias, criterios fijados antes, y un conjunto de validación
distinto del test. En un RAG se mide en dos sitios: después de recuperar y después de generar.

**Vivo 1 (4 min).**
1. `preflight`: 20 casos de test, 8 de validación, 10 documentos, nada indexado de los conjuntos.
2. Abre `datos/test.jsonl`: enseña T01 (respondible, con `documentos_relevantes` y `datos_clave`) y T16 (sin respuesta).
3. `ingestar --config A` → 41 fragmentos. Repítelo: mismo índice, no duplica.
4. `preguntar` una respondible y una sin respuesta.

Pregunta de comprobación: *¿por qué las preguntas del test no pueden estar en el corpus?*

## Bloque 2 · Recuperación · 18:51–19:06

Explica (11–13): unidad = documento. precision@5 divide entre 5 siempre; recall@5 divide entre
los documentos relevantes de esa pregunta. Con un solo relevante, precision@5 tiene techo 0,20.
Las preguntas sin respuesta no tienen recall: su métrica es el rechazo correcto.

**Vivo 2 (5 min).**
1. `calibrar --config A`: similitudes de validación y umbral 0,2787 (7/8 decisiones), comparado
   con el fijado en `datos/calibracion.json` sin sobrescribirlo (solo se actualiza con `--fijar`).
2. `lote --conjunto validacion` e `informe`.
3. Lee en voz alta: precision@5 0,24 con techo 0,24; recall@5 1,00; rechazos 2/3.
4. Abre `evaluacion/metricas.py`: quince líneas, sin modelo.

Pregunta: *si recall@5 es 1,00, ¿por qué solo acierta 3 de 5?* (El fallo está en generar.)

## Bloque 3 · Generación · 19:06–19:24

Explica (15–20): Faithfulness = afirmaciones apoyadas / afirmaciones. Answer Relevancy =
parecido entre la pregunta y las preguntas que el juez deduce de la respuesta. El juez es un
modelo: cuesta, varía y se equivoca. Por eso va aislado, con versiones fijadas, y lo que no
puede puntuar se registra con motivo.

**Vivo 3 (6 min).**
1. `cd evaluador && uv run python evaluar.py ../resultados/mi-validacion-A` (juez doble; dilo).
2. Abre `puntuaciones.jsonl`: una fila evaluable y una `rechazo_sin_respuesta`.
3. `informe` otra vez: aparecen media **y cobertura**.
4. Abre `resultados/ejemplo-doble/test-A/revision-manual-EJEMPLO-rellena.csv`, fila T16:
   fidelidad 1,00 en una respuesta indebida. *Fiel no es correcta.*
5. Menciona los dos hallazgos de `evaluador/README.md` (firma de AnswerRelevancy y cliente síncrono).

Pregunta: *el juez falla en 3 de 14 respuestas y la media sale 0,95. ¿Qué número falta?* (Cobertura.)

## Bloque 4 · Testing automatizado · 19:24–19:38

Explica (22–25): base ancha de tests deterministas con dobles; pocos tests con modelo real,
marcados y fuera de la ejecución por defecto. En un agente se prueban decisiones y límites de
llamadas, no el texto. Los umbrales salen de validación con margen y se congelan.

**Vivo 4 (7 min) · la demostración central.**
1. `uv run pytest` → 73 pasan, 2 excluidos. Enseña `addopts` en `pyproject.toml`.
2. `umbrales resultados/mi-validacion-A` → nueve reglas comparadas con las fijadas en
   `datos/umbrales.doble.json` sin sobrescribir el archivo (solo se actualiza con `--fijar`).
3. `regresion resultados/mi-validacion-A` → PASA. `echo $?` → 0.
4. `degradar … --modo recuperacion`, `informe`, `regresion` → FALLA con tres reglas. `echo $?` → 1.
5. Si hay tiempo: `--modo juez-caido` → solo cae la cobertura; la media sigue en 1,00.

Pregunta: *¿qué pasaría si el control tratara un «sin dato» como aprobado?*

## Bloque 5 · Producción y observabilidad · 19:38–19:51

Explica (27–30): comparar cambiando una variable; en producción no hay referencias, así que
se miran latencia p50/p95, coste y tokens por consulta, tasa de rechazo, errores, feedback y
deriva. Langfuse une ambas cosas: traza por consulta con puntuaciones, y el consumo del juez
en una traza distinta. Las trazas malas de producción alimentan el siguiente conjunto.

**Vivo 5 (4 min).**
1. `comparar` test A y B: B rechaza mejor (4/6) pero se abstiene el doble (8/14). Una sola variable.
2. Abre `rag/observabilidad.py`: `consulta()` y `registrar_evaluador()`. Langfuse está apagado:
   no se enseña ninguna captura como si fuera real.

Pregunta: *¿por qué no sumar el coste del juez al coste por consulta?*

## Práctica y cierre · 19:51–20:00

- **Diapositiva 31.** Práctica **opcional** (7–9 h). `estimar`: 566 llamadas como máximo,
  0,57 USD estimados, cota 4,66 USD. Guía en [ejercicio.md](ejercicio.md).
- **Diapositiva 32.** Cinco ideas; preguntas. Siguiente sesión: S20, proyecto final.
