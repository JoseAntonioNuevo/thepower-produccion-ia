# Cobertura de S19

Cada punto del temario y del enunciado, y dónde se cubre. «Demo» es `demo-evaluacion/`.
Fuentes: [temario](fuentes/temario-S19-original.txt) y [enunciado](fuentes/ejercicio-S19-original.txt),
leídos en Gmail el 16/11/2026 por la sesión anterior.

## Temario

| # | Punto del temario | Diapositivas | Demo y documentos |
|---|---|---|---|
| T0b | Punto de partida: qué es evaluar, tests frente a evaluación, casos de uso (añadido a petición de José, 20/11) | 3, 4, 5 | Guía de evaluación de Anthropic, Langfuse y Ragas leídas el 20/11/2026 |
| T0 | Cerrar el ciclo de calidad: medir antes y después de cada cambio | 6, 30, 32 | Recorrido completo del README |
| T1 | Evaluación de modelos y métricas específicas | 7, 8, 9, 11, 12, 13, 15, 16, 17 | `evaluacion/metricas.py`, `evaluador/`; evaluación de modelos real `MH` frente a `MS` con el mismo juez (`resultados/ejemplo-real/modelos/`) |
| T2 | Análisis avanzado y métricas de producción | 27, 28, 30 | Bloque «Producción» del informe (p50/p95, tasas de error y rechazo, coste por consulta y por 1.000, peso del juez); `comparar`; `tests/test_produccion.py` |
| T3 | Testing automatizado de agentes y pipelines RAG | 22, 23, 24, 25, 26 | `tests/` (131); consulta como grafo LangGraph (`rag/grafo.py`, `tests/test_grafo.py`); agente CRAG en LangGraph con trayectoria y `recursion_limit` (`ampliacion/crag.py`, `tests/test_enrutado.py`); `evaluacion/regresion.py` |
| T4 | Integración de la evaluación con la observabilidad | 29, 30 | `rag/observabilidad.py`, `tests/test_observabilidad.py`; trazas también desde el chat (`ui/motor.py`); envío real pendiente de claves |
| T5 | Práctica: RAG completo desde cero con evaluación y testing | 31 | `docs/ejercicio.md`, [enunciado.md](enunciado.md) |

Conceptos pedidos para la presentación: métricas de modelos y de sistemas (7); evaluación de
RAG separando recuperación y generación (9); precision/recall@k con denominadores (11, 12);
fidelidad (15) y relevancia de respuesta (16); LLM como juez y sus límites (17); no
evaluables y cobertura (19); revisión humana (20); testing automatizado y pirámide (22, 23);
agentes (24); control de regresión con umbrales (25, 26); análisis de producción (28);
integración con observabilidad (29).

## Enunciado

| # | Requisito | Diapositivas | Demo | Evidencia |
|---|---|---|---|---|
| E1 | Al menos ocho documentos ficticios | 6, 9 | `corpus/` (10) | `test_el_corpus_tiene_al_menos_ocho_documentos_ficticios` |
| E2 | Ingesta, fragmentación, embeddings, búsqueda vectorial | 9, 10 | `rag/corpus.py`, `ingesta.py`, `almacen.py` | `ingestar` A y B ejecutado en pgvector |
| E3 | Generación con fuentes y rechazo por falta de evidencia | 9, 13 | `rag/grafo.py` (nodos), `rag/consulta.py` (piezas) | `tests/test_consulta.py`, `tests/test_grafo.py` |
| E4 | Python y PostgreSQL con pgvector | 9, 10 | `compose.yaml`, `esquema.sql` | `pytest -m db` (1 pasa) |
| E5 | Modelos por variables de entorno y versiones registradas | 18 | `.env.example`, `rag/config.py`, `manifiesto.json` | Manifiestos de `resultados/ejemplo-doble` |
| E6 | Reconstruir desde documentos en bruto e índice vacío | 10 | `reconstruir_indice` | `test_reconstruir_dos_veces_no_duplica` |
| E7 | 20 preguntas: 14 respondibles con referencia y 6 sin respuesta | 8 | `datos/test.jsonl` | `test_el_test_tiene_14_respondibles_y_6_sin_respuesta` |
| E8 | Validación distinta para prompts, umbrales y configuración | 8, 14 | `datos/validacion.jsonl`, `calibrar`, `umbrales` | `datos/calibracion.json` |
| E9 | No indexar preguntas ni respuestas esperadas | 8 | `comprobar_separacion` | `preflight` |
| E10 | Criterios de corrección fijados antes del test | 8 | `datos/criterios.md` (16/11/2026) | Documento fechado |
| E11 | precision@5 y recall@5 sobre documentos, sin contar dos fragmentos como dos aciertos | 11, 12 | `evaluacion/metricas.py` | `tests/test_metricas.py` |
| E12 | Explicar los denominadores | 11, 12 | Informe con «Sobre» y techo | `informe.md` |
| E13 | Rechazo correcto aparte; sin recall cuando no hay relevantes | 13 | `evaluar_caso`, `recall_at_k` lanza error | `test_sin_documentos_relevantes_no_existe_recall` |
| E14 | Evaluador aislado con `ragas==0.4.3` y `langchain-community==0.3.31`; bloqueo del resto | 18 | `evaluador/pyproject.toml`, `evaluador/uv.lock` | `uv lock --check`; `test_versiones_fijadas_por_el_enunciado` |
| E15 | `ragas.metrics.collections`, `Faithfulness`, `AnswerRelevancy` con evaluador y embeddings | 15, 16, 18 | `evaluador/evaluar.py` | `test_firmas_de_ascore` |
| E16 | `Faithfulness.ascore(user_input, response, retrieved_contexts)` y `.value` | 18 | `puntuar()` | `test_respuesta_apoyada_es_evaluable_y_se_lee_en_value` |
| E17 | Revisar manualmente al menos cinco respuestas | 20, 21 | `revision`, `datos/revision-casos.json` (6) | CSV de plantilla y ejemplo relleno |
| E18 | La fidelidad no demuestra que la respuesta sea correcta | 15, 20 | Criterio de acierto aparte | T07 y T16 del ejemplo |
| E19 | Errores del evaluador, contexto vacío y NaN como no evaluables, con motivo y cobertura | 19 | `intercambio.py`, `evaluar.py`, `informe.py` | Tests del evaluador y de `test_evaluacion.py` |
| E20 | Abstenciones incorrectas aparte | 13 | Bloque «rechazo» del informe | `test_abstencion_incorrecta_y_rechazo_correcto_se_cuentan_aparte` |
| E21 | Dos configuraciones cambiando una sola variable; mismo test y evaluador | 27 | `datos/configuraciones.json`, `comparar` | `test_comparar_exige_una_sola_variable` |
| E22 | Langfuse: respuesta, fuentes, métricas, latencia, tokens y coste; consumo del evaluador separado | 29 | `rag/observabilidad.py`, `publicar-evaluador` | `tests/test_observabilidad.py` (sin red) |
| E23 | Si falta el coste, comprobar el modelo y definir su precio | 29 | README de la demo, `tarifas.json` | `test_modelo_sin_tarifa_deja_el_coste_sin_dato` |
| E24 | No reajustar las reglas después de ver el test | 8, 25 | Umbrales derivados solo de validación | `derivar_umbrales` rechaza el test |
| E25 | pytest: ingesta sin duplicados, formato, fuentes y errores con respuestas simuladas | 22, 23 | `tests/` | 131 pasan |
| E26 | Evaluaciones reales con `@pytest.mark.llm`, excluidas por defecto | 23 | `pyproject.toml`, `tests/test_integracion.py` | «3 deselected» (2 `db` y 1 `llm`) |
| E27 | Umbrales con margen usando validación | 25 | `umbrales`, `datos/umbrales.doble.json` | `test_los_umbrales_salen_de_validacion_con_margen` |
| E28 | Demostrar con resultados degradados que el control falla | 26 | `degradar`, `regresion` | Código de salida 1 en tres modos; informe rechazado en el cuarto |
| E29 | Ampliación opcional: tests de enrutado de un agente o CRAG | 24 | `ampliacion/crag.py` (grafo LangGraph) | `tests/test_enrutado.py` (decisiones, trayectoria, `recursion_limit`) |
| E30 | Entrega: implementación, datos, entorno bloqueado, tests y tabla comparativa | 31 | `docs/ejercicio.md` | `resultados/ejemplo-doble/comparacion-A-B` |

## Lo que no queda acreditado

| Requisito | Qué falta | Por qué |
|---|---|---|
| E15, E16 con juez real | Ragas contra la API | **Hecho el 22/11/2026** (juez Claude Opus 5.5 vía OpenRouter; `resultados/ejemplo-real/`) |
| E2, E3 con modelos reales | Embeddings y generación con modelos de OpenRouter elegidos en `.env` | **Hecho el 22/11/2026** (Gemini 4 Hydrogen y `openai/text-embedding-3-small`) |
| E22 de extremo a extremo | Ver las trazas en un servidor Langfuse | No se usa Langfuse cloud en esta preparación |
| E17 con resultados reales | Revisión humana de José | La del ejemplo la hizo el agente sobre el perfil doble |
