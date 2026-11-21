# Fuentes de S19

## Fuentes de la escuela (Gmail, solo lectura)

Leídas en Gmail el **16/11/2026 por la sesión anterior** de esta preparación. La reanudación
del 17/11 no tuvo acceso al conector de Gmail y trabajó con las copias guardadas.

| Fuente | Fecha | Id | Copia |
|---|---|---|---|
| Temario de AI Engineer (cuerpo del correo) | 17/07/2026 | mensaje `19f6f7569cc093d9` | [fuentes/temario-S19-original.txt](fuentes/temario-S19-original.txt) |
| `ejercicios.docx` (S5, S6, S11, S18, S19) | 29/09/2026 | mensaje `1a0ebc9b585e70bc`, hilo `1a0d7bb5a23dc200` | [fuentes/ejercicio-S19-original.txt](fuentes/ejercicio-S19-original.txt) |
| Indicaciones de Laura (prácticas opcionales, método, QR) | 28/09–16/11/2026 | hilo `1a0d7bb5a23dc200` | [fuentes/indicaciones-laura.md](fuentes/indicaciones-laura.md) |

## Documentación técnica oficial

«Consultada» indica la fecha en que se leyó la página. Las del 16/11 las leyó la sesión
anterior con Firecrawl autoalojado; hay copia en `.build/s19/research/`. El 17/11 no se
volvieron a descargar: lo que se afirma de cada librería se comprobó **ejecutando la versión
instalada**, que es la fuente que manda para este paquete.

| Tema | Fuente | Consultada | Qué se usa |
|---|---|---|---|
| Faithfulness en Ragas 0.4.3 | <https://github.com/vibrantlabsai/ragas/blob/v0.4.3/src/ragas/metrics/collections/faithfulness/metric.py> | 17/11/2026, código instalado (`ragas==0.4.3`) | Firma de `ascore`, dos pasos, NaN sin afirmaciones |
| AnswerRelevancy en Ragas 0.4.3 | Paquete instalado: `ragas/metrics/collections/answer_relevancy/metric.py` | 17/11/2026, código instalado | `ascore(user_input, response)`, `strictness=3`, coseno |
| Ragas con Gemini | <https://docs.ragas.io/en/stable/howtos/integrations/gemini/> | 16/11/2026 | `llm_factory(provider="google")`; discrepancia documentada |
| Métricas de Ragas (conceptos) | <https://docs.ragas.io/en/stable/concepts/metrics/> | 16/11/2026 (enlazada desde la guía) | Definiciones |
| Tokens y coste en Langfuse | <https://langfuse.com/docs/observability/features/token-and-cost-tracking> | 16/11/2026 | `usage_details`, definiciones de modelo y precios |
| Puntuaciones en Langfuse por SDK | <https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk> | 16/11/2026 | `create_score(trace_id, name, value, data_type)` |
| SDK de Langfuse (Python) | <https://langfuse.com/docs/observability/sdk/overview> | 16/11/2026; firmas probadas el 17/11 con `langfuse==5.2.0` sin red | `start_as_current_observation`, `propagate_attributes`, `create_trace_id` |
| Precios de la API de Gemini | <https://ai.google.dev/gemini-api/docs/pricing> | 16/11/2026 | `tarifas.json` |
| Modelos de Gemini | <https://ai.google.dev/gemini-api/docs/models> | 16/11/2026 | Identificadores `gemini-3.5-flash-lite`, `gemini-3.8-flash` |
| Embeddings de Gemini | <https://ai.google.dev/gemini-api/docs/embeddings> | 16/11/2026 | `gemini-embedding-2`, `gemini-embedding-001`, dimensión 768 |
| Gemini compatible con OpenAI | <https://ai.google.dev/gemini-api/docs/openai> | 16/11/2026 | Endpoint `…/v1beta/openai/` de la ruta `openai_compat` |
| pgvector | <https://github.com/pgvector/pgvector> | No releída el 17/11; operador `<=>` y HNSW comprobados ejecutando contra `pgvector/pgvector:pg17` | Distancia coseno, `vector(768)` |
| pytest · marcadores | <https://docs.pytest.org/en/stable/how-to/mark.html> | No releída el 17/11; `-m 'not llm and not db'` comprobado ejecutando `pytest==9.1.1` | `@pytest.mark.llm`, `addopts` |
| uv · proyectos y bloqueo | <https://docs.astral.sh/uv/concepts/projects/> | No releída el 17/11; `uv lock --check` ejecutado en los dos proyectos | Dos entornos bloqueados |

Los precios cambian. `tarifas.json` guarda fuente y fecha; vuelve a comprobarlos antes de
ejecutar el perfil real.

## Material propio reutilizado

| Qué | De dónde | Cómo |
|---|---|---|
| Universo ficticio AetherCloud | `3-rag/lab/corpus/sources` (S10) | Diez documentos reescritos para S19; ver `demo-evaluacion/corpus/PROCEDENCIA.md` |
| Esquema `vector(768)` + HNSW coseno | `3-rag/lab/schema.sql` | Adaptado en `demo-evaluacion/esquema.sql` |
| Sistema visual de la presentación | `material/S17/fuentes/rediseno-visual/deck_lib.py` | Copiado y adaptado en `fuentes/presentacion/` |
| QR de AI Engineer | `material/S16/assets/qr-ai-engineer.jpg` | Copia byte a byte en `assets/` |
| Logotipo | `material/S17/assets/thepower-logo.png` | Copia byte a byte en `assets/` |

Procedencia de cada imagen de la presentación: [fuentes/presentacion/README.md](fuentes/presentacion/README.md).

## Punto de partida (diapositivas 3–5, consultadas el 20/11/2026)

- Anthropic, [Define success criteria and build evaluations](https://docs.claude.com/en/docs/test-and-evaluate/develop-tests): criterios de éxito antes de evaluar y tres formas de puntuar (código, persona, LLM) con sus ventajas e inconvenientes.
- Langfuse, [Evaluation overview](https://langfuse.com/docs/evaluation/overview): evaluación **online** sobre trazas de producción y **offline** antes de publicar, y ejemplos de producción convertidos en datasets.
- Ragas, [conceptos](https://docs.ragas.io/en/stable/concepts/): experimentos, datasets y métricas de RAG.
- Copias leídas con Firecrawl en `.build/s19/research/`.
