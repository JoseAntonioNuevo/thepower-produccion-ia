# Evaluador aislado · Ragas 0.4.3

Este directorio es un **proyecto uv independiente**. Tiene su propio `pyproject.toml`, su
`uv.lock` y su `.venv`. No importa el paquete `rag/` y el RAG no importa Ragas.

¿Por qué aislarlo? Ragas arrastra más de cien dependencias (LangChain, OpenAI, instructor…).
Mezcladas con las del sistema que evalúas, una actualización del evaluador puede cambiar el
comportamiento del RAG, y al revés. Separados, cada lado se actualiza y se bloquea por su cuenta.

```text
RAG (s19.py lote) ──► respuestas.jsonl ──► evaluar.py ──► puntuaciones.jsonl ──► s19.py informe
                      s19.respuestas.v1                    s19.puntuaciones.v1
```

## Uso

```bash
uv sync
uv run python evaluar.py ../resultados/mi-test-A                    # juez doble, sin coste
uv run python evaluar.py ../resultados/mi-test-A --modo real --execute   # juez de pago
uv run pytest                                                        # 19 tests, sin red
```

| Modo | Métricas | Juez y embeddings | Sirve para |
|---|---|---|---|
| `doble` | Clases reales de `ragas.metrics.collections` | Dobles locales deterministas | Probar el recorrido: formato, no evaluables, cobertura |
| `real` | Las mismas | Modelos de OpenRouter elegidos en `../.env` (de pago) | Medir |

El modo `real` **nunca** cae al doble: sin `OPENROUTER_API_KEY` o sin `--execute` termina con error.

## Juez real: siempre OpenRouter

El juez y sus embeddings se eligen en `../.env` y se cambian sin tocar el código:

| Variable | Para qué | Por defecto |
|---|---|---|
| `S19_EVAL_LLM_MODEL` | Modelo juez | `anthropic/claude-opus-5.5` |
| `S19_EVAL_EMBEDDING_MODEL` | Embeddings de AnswerRelevancy | `openai/text-embedding-3-small` |
| `S19_EVAL_MAX_TOKENS` | Máximo de salida por llamada | 4096 |
| `S19_EVAL_LLM_PROVEEDORES` · `S19_EVAL_EMBEDDING_PROVEEDORES` | Orden fijo de proveedores de OpenRouter, sin cambios automáticos | vacío |
| `S19_EVAL_LLM_EXTRA` | Campos extra en JSON en cada petición al juez | vacío |
| `S19_EVAL_QUITAR_PARAMETROS` | Parámetros que se quitan, además de los que el catálogo dice que el juez no admite (Ragas siempre envía `temperature` y `top_p`; Opus 5.5 no admite ninguno y se quitan solos) | vacío |

Ragas recibe un `AsyncOpenAI` apuntando a OpenRouter. Como Ragas construye las peticiones por
dentro, un transporte HTTP (`TransporteOpenRouter`) añade el orden de proveedores y los campos
extra, y quita los parámetros indicados. Todos estos ajustes forman parte de la identidad del
evaluador: dos ejecuciones solo se comparan si los comparten.

Conviene un juez de **otra familia** que el generador (por defecto, Anthropic juzga a Google)
y el **mismo** juez en las dos ejecuciones que se comparan. El adaptador de Ragas pide la
salida en JSON (`response_format`): `python s19.py preflight` avisa si el catálogo de
OpenRouter dice que el modelo no lo admite.

## Lo que pide el enunciado y lo que hay en ragas 0.4.3

Comprobado el 17/11/2026 instalando las versiones fijadas e inspeccionando el paquete:

| Enunciado | Encontrado | Estado |
|---|---|---|
| `ragas==0.4.3`, `langchain-community==0.3.31` | Instalados; el resto queda en `uv.lock` (100 paquetes) | Coincide |
| `ragas.metrics.collections` con `Faithfulness` y `AnswerRelevancy` | Existen | Coincide |
| `Faithfulness.ascore(user_input, response, retrieved_contexts)` | Firma exacta | Coincide |
| Puntuación en `.value` | `MetricResult.value` | Coincide |
| `AnswerRelevancy` necesita evaluador y embeddings | `AnswerRelevancy(llm, embeddings, strictness=3)` | Coincide |

Tres cosas que el enunciado no dice y conviene saber:

1. **`AnswerRelevancy.ascore` no recibe `retrieved_contexts`.** Su firma es
   `ascore(user_input, response)`. Compara la pregunta original con preguntas que el juez
   genera a partir de la respuesta. Pasarle contextos da `TypeError`.
2. **La llamada de la guía «Ragas con Gemini» falla con `ascore`.**
   `llm_factory("…", provider="google", client=genai.Client(...))` devuelve un cliente
   síncrono y `ascore` lanza `TypeError: Cannot use agenerate() with a synchronous client`
   (comprobado el 17/11/2026). Por eso el juez usa siempre un cliente **asíncrono**
   compatible con OpenAI, ahora contra OpenRouter: también puede juzgar Gemini
   (`google/gemini-…`) sin instalar el SDK de Google. **Es una sustitución explícita respecto a
   la guía.** Ejecutado contra la API real el 22/11/2026 con Claude Opus 5.5 como juez: puntuó
   todas las respuestas emitidas (cobertura 1,00 en test) y su coste medido fue 0,43–0,46 USD por test de 20 casos.
3. **Ragas envía telemetría de uso** salvo que `RAGAS_DO_NOT_TRACK=true`. `evaluar.py` la desactiva.

Además, Faithfulness devuelve **NaN** cuando el juez no extrae ninguna afirmación, y lanza
`ValueError` si el contexto está vacío. Por eso el contexto vacío se filtra antes
(`contexto_vacio`) y el NaN se registra como `nan`.

## Qué hace cada métrica (leído en el código de 0.4.3)

**Faithfulness** — 2 llamadas al juez por respuesta:

1. Descompone la respuesta en afirmaciones atómicas.
2. Decide, afirmación por afirmación, si se deduce del contexto (0 o 1).

`faithfulness = afirmaciones apoyadas / afirmaciones totales`.
Mide apoyo en el contexto. **No** mide si la respuesta es correcta ni si está completa.

**AnswerRelevancy** — 3 llamadas al juez + embeddings:

1. A partir de la respuesta, el juez genera 3 preguntas y marca si la respuesta es evasiva.
2. Se compara por coseno cada pregunta generada con la pregunta original.

`answer_relevancy = media de los cosenos` (0 si la respuesta es evasiva).
Mide si la respuesta habla de lo que se preguntó. **No** mide si lo que dice es verdad.

## Consumo del juez

Ragas no devuelve tokens ni coste. `ContadorUso` lee el campo `usage` de cada respuesta HTTP
de OpenRouter (tokens y `cost`, lo cobrado, incluidos los embeddings del juez) y lo reparte por
caso y métrica. Va en `puntuaciones.jsonl` → `consumo`, separado del consumo del RAG, con
`coste_fuente: "openrouter"`. Si alguna respuesta llega sin `cost`, se estima con
`../tarifas.json` (`"tarifa"`); si faltan tokens, quedan en `null`: desconocido no es cero.
