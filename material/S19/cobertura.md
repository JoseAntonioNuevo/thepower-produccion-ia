# Cobertura de S19

Cada punto del temario y del enunciado, y dónde se cubre. «Demo» es `demo-evaluacion/`.
Fuentes: [temario](fuentes/temario-S19-original.txt) y [enunciado](fuentes/ejercicio-S19-original.txt),
leídos en Gmail el 16/11/2026 por la sesión anterior.

## Temario

| # | Punto del temario | Diapositivas | Demo y documentos |
|---|---|---|---|
| T0 | Cerrar el ciclo de calidad: medir antes y después de cada cambio | 1, 2, 15 | Tres pruebas reales con predicción y resultado (`guion-directo-modelos.md`) |
| T1 | Evaluación de modelos y métricas específicas | 7–12, 16, 18 | `evaluacion/metricas.py`, `evaluador/`; ensayos de generador y juez (`resultados/ensayo-tres-pruebas-20261122/`); evaluación real `MH` frente a `MS` con el mismo juez (`resultados/ejemplo-real/modelos/`) |
| T2 | Análisis avanzado y métricas de producción | 6, 8, 12, 17, 18 | Latencia, tokens y coste por llamada en Langfuse; bloque «Producción» del informe (p50/p95, coste por consulta y por 1.000, peso del juez); `comparar`; `tests/test_produccion.py` |
| T3 | Testing automatizado de agentes y pipelines RAG | 5, 13, 14, 19 | Grafo LangGraph y tests de trayectoria (`rag/grafo.py`, `tests/test_grafo.py`, `tests/test_enrutado.py`); comprobación por caso de T09; `evaluacion/regresion.py` |
| T4 | Integración de la evaluación con la observabilidad | 6, 12, 14 | `rag/observabilidad.py`: scores en `consulta-rag` y `consumo-juez` en `evaluador-ragas`; sesiones verificadas en Langfuse Cloud el 22/11/2026 |
| T5 | Práctica: RAG completo desde cero con evaluación y testing | 15 | `docs/ejercicio.md`, [enunciado.md](enunciado.md) |

Conceptos de la presentación del 22/11/2026: herramientas y su función (3); qué guarda un RAG y
separación de los datos de evaluación (4); grafo con rechazo previo y embudo 12 → 5 → 4 (5);
trazas, scores y consumo del juez (6); cambiar el generador con una sola variable (7–8);
recall@5 frente a lo que lee el modelo (9–10); Faithfulness, Answer Relevancy y coste del juez
(11–12); regresión del evaluador y control por caso frente a umbral del lote (13–14); tabla de
métricas, comparación controlada, histórico Hydrogen–Sol y control por umbrales (16–19).

## Enunciado

| # | Requisito | Diapositivas | Demo | Evidencia |
|---|---|---|---|---|
| E1 | Al menos ocho documentos ficticios | 4 | `corpus/` (10) | `test_el_corpus_tiene_al_menos_ocho_documentos_ficticios` |
| E2 | Ingesta, fragmentación, embeddings, búsqueda vectorial | 4, 5 | `rag/corpus.py`, `ingesta.py`, `almacen.py` | `ingestar` A y B ejecutado en pgvector |
| E3 | Generación con fuentes y rechazo por falta de evidencia | 5 | `rag/grafo.py` (nodos), `rag/consulta.py` (piezas) | `tests/test_consulta.py`, `tests/test_grafo.py` |
| E4 | Python y PostgreSQL con pgvector | 3, 4 | `compose.yaml`, `esquema.sql` | `pytest -m db` (1 pasa) |
| E5 | Modelos por variables de entorno y versiones registradas | 3, 7, 20 | `.env.example`, `rag/config.py`, `manifiesto.json` | Manifiestos de `resultados/ejemplo-doble` |
| E6 | Reconstruir desde documentos en bruto e índice vacío | 4 | `reconstruir_indice` | `test_reconstruir_dos_veces_no_duplica` |
| E7 | 20 preguntas: 14 respondibles con referencia y 6 sin respuesta | 4 | `datos/test.jsonl` | `test_el_test_tiene_14_respondibles_y_6_sin_respuesta` |
| E8 | Validación distinta para prompts, umbrales y configuración | 4, 19 | `datos/validacion.jsonl`, `calibrar`, `umbrales` | `datos/calibracion.json` |
| E9 | No indexar preguntas ni respuestas esperadas | 4 | `comprobar_separacion` | `preflight` |
| E10 | Criterios de corrección fijados antes del test | 16, 18 | `datos/criterios.md` (16/11/2026) | Documento fechado |
| E11 | precision@5 y recall@5 sobre documentos, sin contar dos fragmentos como dos aciertos | 5, 10, 16 | `evaluacion/metricas.py` | `tests/test_metricas.py` |
| E12 | Explicar los denominadores | 10, 16 | Informe con «Sobre» y techo | `informe.md` |
| E13 | Rechazo correcto aparte; sin recall cuando no hay relevantes | 5, 16 | `evaluar_caso`, `recall_at_k` lanza error | `test_sin_documentos_relevantes_no_existe_recall` |
| E14 | Evaluador aislado con `ragas==0.4.3` y `langchain-community==0.3.31`; bloqueo del resto | 3, 11 | `evaluador/pyproject.toml`, `evaluador/uv.lock` | `uv lock --check`; `test_versiones_fijadas_por_el_enunciado` |
| E15 | `ragas.metrics.collections`, `Faithfulness`, `AnswerRelevancy` con evaluador y embeddings | 11, 12 | `evaluador/evaluar.py` | `test_firmas_de_ascore` |
| E16 | `Faithfulness.ascore(user_input, response, retrieved_contexts)` y `.value` | 11, 14 | `puntuar()` | `test_respuesta_apoyada_es_evaluable_y_se_lee_en_value` |
| E17 | Revisar manualmente al menos cinco respuestas | 15 | `revision`, `datos/revision-casos.json` (6) | CSV de plantilla y ejemplo relleno |
| E18 | La fidelidad no demuestra que la respuesta sea correcta | 14, 16 | Criterio de acierto aparte | T07 y T16 del ejemplo |
| E19 | Errores del evaluador, contexto vacío y NaN como no evaluables, con motivo y cobertura | 12, 16, 19 | `intercambio.py`, `evaluar.py`, `informe.py` | Tests del evaluador y de `test_evaluacion.py` |
| E20 | Abstenciones incorrectas aparte | 10, 16 | Bloque «rechazo» del informe | `test_abstencion_incorrecta_y_rechazo_correcto_se_cuentan_aparte` |
| E21 | Dos configuraciones cambiando una sola variable; mismo test y evaluador | 7, 8, 17, 18 | `datos/configuraciones.json`, `comparar` | `test_comparar_exige_una_sola_variable` |
| E22 | Langfuse: respuesta, fuentes, métricas, latencia, tokens y coste; consumo del evaluador separado | 6, 12 | `rag/observabilidad.py`, `publicar-evaluador` | `tests/test_observabilidad.py` (sin red) |
| E23 | Si falta el coste, comprobar el modelo y definir su precio | 6 | README de la demo, `tarifas.json` | `test_modelo_sin_tarifa_deja_el_coste_sin_dato` |
| E24 | No reajustar las reglas después de ver el test | 18, 19 | Umbrales derivados solo de validación | `derivar_umbrales` rechaza el test |
| E25 | pytest: ingesta sin duplicados, formato, fuentes y errores con respuestas simuladas | 5, 13 | `tests/` | 131 pasan |
| E26 | Evaluaciones reales con `@pytest.mark.llm`, excluidas por defecto | — | `pyproject.toml`, `tests/test_integracion.py` | «3 deselected» (2 `db` y 1 `llm`) |
| E27 | Umbrales con margen usando validación | 19 | `umbrales`, `datos/umbrales.doble.json` | `test_los_umbrales_salen_de_validacion_con_margen` |
| E28 | Demostrar con resultados degradados que el control falla | 19 | `degradar`, `regresion` | Código de salida 1 en tres modos; informe rechazado en el cuarto |
| E29 | Ampliación opcional: tests de enrutado de un agente o CRAG | 5 (trayectoria); CRAG fuera del recorrido | `ampliacion/crag.py` (grafo LangGraph) | `tests/test_enrutado.py` (decisiones, trayectoria, `recursion_limit`) |
| E30 | Entrega: implementación, datos, entorno bloqueado, tests y tabla comparativa | 15 | `docs/ejercicio.md` | `resultados/ejemplo-doble/comparacion-A-B` |

## Lo que no queda acreditado

| Requisito | Qué falta | Por qué |
|---|---|---|
| E15, E16 con juez real | Ragas contra la API | **Hecho el 22/11/2026** (juez Claude Opus 5.5 vía OpenRouter; `resultados/ejemplo-real/`) |
| E2, E3 con modelos reales | Embeddings y generación con modelos de OpenRouter elegidos en `.env` | **Hecho el 22/11/2026** (Gemini 4 Hydrogen y `openai/text-embedding-3-small`) |
| E22 de extremo a extremo | Ver las trazas en un servidor Langfuse | **Hecho el 22/11/2026** en Langfuse Cloud (UE); ver [verificacion.md](verificacion.md) |
| E17 con resultados reales | Revisión humana de José | La del ejemplo la hizo el agente sobre el perfil doble |
