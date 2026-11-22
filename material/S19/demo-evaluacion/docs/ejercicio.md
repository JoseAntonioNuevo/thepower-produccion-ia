# S19 · Práctica opcional

**Construir un sistema RAG completo desde cero con evaluación y testing integrados.**

La práctica es **opcional**: no es obligatoria para superar el programa. El enunciado
completo está en `ENUNCIADO.md`, en la raíz del paquete que se entrega a los alumnos
(en el repositorio del curso, `material/S19/enunciado.md`). Dedicación orientativa: 7–9 horas
con el entorno preparado.

Puedes hacerla de dos formas:

- **Sin gastar:** todo con el perfil `doble`. Practicas el método completo; tus cifras no miden un modelo.
- **Con modelos:** perfil `real`, siempre a través de OpenRouter con una sola clave
  (`OPENROUTER_API_KEY`). Elige en `.env` los modelos de generación, embeddings y juez
  (los de OpenAI, Anthropic, Google…). Antes ejecuta `uv run python s19.py catalogo` y
  `uv run python s19.py estimar`, y revisa el gasto previsto.

## Paso a paso

Usa este repositorio como punto de partida. En cada paso, **cambia algo tuyo**.

| # | Qué haces | Cómo lo compruebas | Parte del enunciado |
|---|---|---|---|
| 1 | Sustituye el corpus por **al menos ocho documentos ficticios tuyos** en `corpus/` (nombres `NN-tema.md`) | `s19.py preflight` cuenta tus documentos | Ingesta desde documentos en bruto |
| 2 | Reconstruye el índice desde vacío: `docker compose down -v`, `up -d --wait`, `ingestar` | Ejecuta `ingestar` dos veces: mismo número de filas | Índice vacío, sin duplicados |
| 3 | Escribe `datos/test.jsonl`: **14 respondibles** (con `documentos_relevantes`, `datos_clave`, `respuesta_referencia`) y **6 sin respuesta** | `preflight` valida 14 + 6 y que nada está en el corpus | Datos de evaluación |
| 4 | Escribe `datos/validacion.jsonl` con preguntas **distintas** | `preflight` falla si comparten casos | Validación aparte |
| 5 | Revisa `datos/criterios.md` y fecha tus criterios **antes** de ejecutar el test | El archivo está en tu entrega con fecha anterior a los resultados | Criterios fijados antes |
| 6 | `calibrar` con validación; `lote` + `informe` | Explica con tus palabras los dos denominadores | precision@5, recall@5, rechazo |
| 7 | Evalúa la generación en `evaluador/` | `puntuaciones.jsonl` tiene valor o motivo en cada fila | Ragas aislado, no evaluables, cobertura |
| 8 | `revision` y rellena a mano **al menos cinco** filas | El CSV tiene tu nombre y tus notas | Revisión manual |
| 9 | Compara dos configuraciones cambiando **una** variable (`chunk_size` o `prompt_version`) | `comparar` produce la tabla; si cambias dos, se niega | Comparación A/B |
| 10 | `umbrales` con validación y `regresion` | Pasa con la buena; **falla** con `degradar` | Regresión útil |
| 11 | Añade **dos tests tuyos** en `tests/` con respuestas simuladas | `uv run pytest` | pytest con dobles |
| 12 | Opcional: activa Langfuse y publica el consumo del evaluador aparte | Dos trazas por caso: `consulta-rag` y `evaluador-ragas` | Observabilidad |

**Ampliación opcional.** Añade un caso a `tests/test_enrutado.py` para el agente de
`ampliacion/crag.py` (un grafo de LangGraph): por ejemplo, que nunca haga más de tres
recuperaciones o que su trayectoria (`Trayectoria.ruta`) sea la esperada.

## Qué entregas

1. Implementación (tu copia del repositorio) con `uv.lock` y `evaluador/uv.lock`.
2. `corpus/`, `datos/test.jsonl`, `datos/validacion.jsonl` y `datos/criterios.md`.
3. Tests y la salida de `uv run pytest`.
4. La **tabla comparativa** A/B con fallos y cobertura (`comparacion.md`).
5. La revisión manual rellena.
6. Media página: qué configuración eliges y por qué, y qué no has podido medir.

No entregues `.env`, claves ni datos reales de personas o empresas.

## Cómo se valora

Según el enunciado: **reconstrucción completa**, **métricas separadas**, **trazabilidad**
y **regresiones útiles**. Una entrega con cifras modestas y bien explicadas vale más que
una con cifras altas sin denominadores.

## Errores frecuentes

- Indexar las preguntas o las respuestas de referencia.
- Contar tres fragmentos del mismo documento como tres aciertos.
- Calcular recall en preguntas sin respuesta.
- Dar la media de Faithfulness sin decir sobre cuántas respuestas.
- Cambiar el umbral después de ver el test.
- Comparar dos ejecuciones con distinto evaluador.
