# Verificación de S19

Preparación del 16–17/11/2026. Todo lo que sigue se ejecutó en local, en macOS, sin llamadas
a APIs de pago. La sesión del 16/11 la cortó el límite de uso; la del 17/11 la retomó desde
el disco. Los resultados son los de la última ejecución del 17/11.

## Fuentes de la escuela

- Leídas en Gmail el 16/11/2026 por la sesión anterior: temario (mensaje `19f6f7569cc093d9`),
  `ejercicios.docx` (mensaje `1a0ebc9b585e70bc`) e hilo `1a0d7bb5a23dc200`.
- El 17/11 **no hubo acceso a Gmail**: se trabajó con las copias de `fuentes/`. Se comprobó que
  contienen el temario de S19, el ejercicio completo y las indicaciones de Laura.

## Demo · comandos y resultado

Directorio: `material/S19/demo-evaluacion`. Contenedor `thepower-s19-pgvector`
(`pgvector/pgvector:pg17`, `127.0.0.1:54519`).

| Comando | Resultado |
|---|---|
| `uv run --frozen ruff check .` | `All checks passed!` |
| `uv run --frozen pytest -q` | `66 passed, 2 deselected` |
| `uv run --frozen pytest -q -m db` | `1 passed, 67 deselected` (pgvector real) |
| `uv lock --check` (demo) | `Resolved 53 packages` · bloqueo coherente |
| `(cd evaluador && uv lock --check)` | `Resolved 107 packages` · bloqueo coherente |
| `(cd evaluador && uv run --frozen pytest -q)` | `15 passed, 1 deselected` |
| `s19.py preflight` | 20 casos de test, 8 de validación, 10 documentos; «Preflight correcto» |
| `s19.py ingestar --config A` / `B` | 41 y 13 fragmentos; filas leídas de PostgreSQL iguales |
| `s19.py calibrar --config A` | Umbral 0,2787; 7/8 decisiones correctas en validación |
| `s19.py lote` + `evaluar.py` + `informe` | Validación A y B, test A y B: sin errores del sistema |
| `s19.py umbrales …/validacion-A` | 9 reglas en `datos/umbrales.doble.json` |
| `s19.py regresion …/validacion-A` | **PASA**, código de salida 0 |
| `s19.py regresion …/validacion-B` | **FALLA**, código 1: abstenciones 0,40 > 0,10; aciertos 0,20 < 0,50 |
| `degradar --modo recuperacion` + `regresion` | **FALLA**, código 1: recall 0,10; precision 0,04; aciertos 0,00 |
| `degradar --modo sin-rechazo` + `regresion` | **FALLA**, código 1: rechazos 0,00; cobertura 0,75 |
| `degradar --modo juez-caido` + `regresion` | **FALLA**, código 1: cobertura 0,50 en las dos métricas |
| `degradar --modo incompleto` + `informe` | `informe` termina con código 2: no resume un conjunto parcial |
| `s19.py regresion …/test-A` | **FALLA**, código 1 (3 reglas). Ver «Hallazgos» |
| `s19.py comparar test-A test-B` | Tabla con una sola variable (`chunk_size`) |
| `s19.py revision …/test-A` | Plantilla con 6 casos |
| `s19.py estimar` | 566 llamadas máx.; 0,5680 USD estimados; 4,6552 USD de cota |

Resultados guardados en `demo-evaluacion/resultados/ejemplo-doble/`.

### Resultado del perfil doble (no mide ningún modelo)

| Métrica | Validación A | Test A | Test B |
|---|---:|---:|---:|
| precision@5 (techo 0,24) | 0,24 | 0,24 | 0,24 |
| recall@5 | 1,00 | 1,00 | 1,00 |
| Rechazos correctos | 2/3 | 2/6 | 4/6 |
| Abstenciones incorrectas | 0/5 | 4/14 | 8/14 |
| Aciertos por criterio | 3/5 | 6/14 | 3/14 |
| faithfulness · cobertura | 1,00 · 6/6 | 1,00 · 14/14 | 1,00 · 8/8 |
| answer_relevancy · cobertura | 0,41 · 6/6 | 0,44 · 14/14 | 0,53 · 8/8 |

## API de Ragas 0.4.3 (entorno aislado)

Instaladas `ragas==0.4.3` y `langchain-community==0.3.31` en `evaluador/.venv` e inspeccionadas.

| Comprobación | Resultado |
|---|---|
| `ragas.metrics.collections` exporta `Faithfulness` y `AnswerRelevancy` | Sí |
| `Faithfulness.ascore(user_input, response, retrieved_contexts)` | Firma exacta |
| Lectura en `.value` | `MetricResult.value`; NaN si no hay afirmaciones |
| `AnswerRelevancy(llm, embeddings)` | Sí; `strictness=3` |
| `AnswerRelevancy.ascore` | **Discrepancia:** recibe `user_input` y `response`; no `retrieved_contexts` |
| Guía «Ragas con Gemini»: `llm_factory(provider="google", client=genai.Client())` | **Discrepancia:** cliente síncrono; `ascore` lanza `TypeError` antes de usar la red |
| Ruta `openai_compat` (`AsyncOpenAI` + endpoint compatible de Gemini) | Construye y es asíncrona; probada de extremo a extremo con **HTTP simulado** (tokens y coste del juez) |
| Ruta `google_genai` (`instructor.from_genai(use_async=True)`) | Construye y es asíncrona; no ejecutada |
| Telemetría de Ragas | Activa por defecto; `evaluar.py` fija `RAGAS_DO_NOT_TRACK=true` |

La ruta por defecto (`openai_compat`) es una **sustitución explícita** respecto a la guía que
enlaza el enunciado. Está declarada en el README del evaluador, en `.env.example`, en
`enunciado.md` y en la diapositiva 15.

## Presentación

| Comprobación | Resultado |
|---|---|
| `check.py` | 29 diapositivas, 29 notas completas, 15 tablas nativas, 42 imágenes, solo Arial/Georgia/Courier New, nada fuera del lienzo, QR de S16 y logotipo byte a byte: **CORRECTO** |
| Render | LibreOffice del runtime local → PDF de 29 páginas (960 × 540 pt) → PNG con `pdftoppm` |
| Revisión visual | Las 29 diapositivas vistas sobre el render; 22 a tamaño completo y todas en hoja de contactos. Comparadas con los renders del ejemplo (`.build/s19/ref/`) |
| Correcciones tras verlas | Flecha del índice (6); rótulo partido en dos líneas (15, 20); etiquetas solapadas del diagrama (21); marcas de umbral poco visibles (22); marcas de verificación y barras invertidas dobles, y comando incoherente con el error mostrado (24); etiquetas de puntuación solapadas (26) |
| SHA-256 PPTX | `e9ae8dcddf4df4a16fcbd44fe7d818d39a63c33b2486dc422671934d415dc6fb` |
| SHA-256 PDF | `34bc80d16f1a0fd51bf36b39ababdfe181ebba2a039c9233e812220555abba5f` |

No se ha abierto el PPTX en PowerPoint ni en Keynote: el render es de LibreOffice.

## Hallazgos que se dejan a la vista

1. **El test A del perfil doble no cumple los umbrales de validación** (rechazos 0,33 < 0,56;
   abstenciones 0,29 > 0,10; aciertos 0,43 < 0,50). Ocho casos de validación son pocos para
   generalizar. No se han retocado las reglas ni los conjuntos después de verlo. Por eso el
   control se demuestra sobre validación, que es donde se usa en cada cambio.
2. **El umbral de evidencia calibrado con A no vale para B.** B se abstiene el doble. El
   control lo detecta en validación.
3. **Fidelidad 1,00 en respuestas incompletas o indebidas** (T07, T12, T16) con el juez doble.

## Pendiente

| Qué | Por qué | Cómo |
|---|---|---|
| Ejecutar el perfil real | Requiere autorización de gasto de José | Sección «Perfil real» de `docs/comandos.md`; previsión 0,57 USD, cota 4,66 USD |
| Confirmar las dos rutas del juez contra la API | Ídem | `S19_EJECUTAR_REAL=1 uv run pytest -m llm` en `evaluador/` |
| Volver a comprobar tarifas e identificadores de modelo | Son del 16/11/2026 | `tarifas.json`, `.env.example` |
| Ver las trazas en Langfuse | No se usa Langfuse cloud | `S19_LANGFUSE=on` + claves; `publicar-evaluador` |
| Revisión manual humana | Debe hacerla una persona con resultados reales | `s19.py revision` |
| Abrir el PPTX en PowerPoint | No disponible en esta máquina sin interfaz | Abrir y pasar las 29 diapositivas |
| Ensayo cronometrado de los 90 minutos | No se ha hecho | `docs/guion-clase.md` |

## Recogida

Contenedor `thepower-s19-pgvector` retirado el 17/11/2026 (`docker rm -f`). Para recrearlo:
`cd demo-evaluacion && docker compose up -d --wait` y `s19.py ingestar --config A` y `--config B`.

## Ampliación del 20/11/2026: punto de partida (diapositivas 3–5)

Petición de José: una introducción a la evaluación y el testing, muy visual, como la de S18.

| Comprobación | Resultado |
|---|---|
| Generación | `build.py` → 32 diapositivas; los dos avisos de siempre (pie del QR y título de agentes, ahora la 24), que caben en el render |
| `check.py` | CORRECTO: 32 diapositivas, notas completas (franja, QUÉ ABRIR, PREGUNTA, Fuentes), 17 tablas nativas, solo Arial, Georgia y Courier New, QR y logotipo byte a byte |
| Render | PDF de 32 páginas (LibreOffice), SHA-256 `f451c9b8…`; 3, 4 y 5 revisadas a 150 ppp; 1–12 en hoja de contactos; plan de la diapositiva 2 con las horas nuevas |
| Fuentes | Guía de evaluación de Anthropic, resumen de evaluación de Langfuse y conceptos de Ragas, leídos el 20/11/2026 con Firecrawl; copias en `.build/s19/research/` |
| Horario | 32 franjas contiguas de 18:30 a 20:00; desde la 3, todas las referencias suben tres números en notas, guion, comandos, cobertura y README |

Las secciones anteriores de este archivo conservan la numeración que tenían cuando se escribieron.

## Revisión completa del 20/11/2026

Se leyeron las 32 diapositivas (texto y notas), se comprobaron las referencias cruzadas, los pies y los horarios, y se revisó el
render de cada diapositiva. No había referencias rotas. Cambios aplicados:

| Cambio | Diapositivas |
|---|---|
| Portada con fechas y grupos: martes 24/11 (M/J) y lunes 30/11 (L/X), 18:30–20:00 | 1 |
| La anatomía de una evaluación se presenta como la idea de la 3 aplicada a los archivos de la demo («· en la demo») | 8 |
| Idea guía coherente con el título: el enunciado pide cinco lecturas; la demo hace seis | 20 |
| Tablas y textos algo más grandes | 17, 19 |
| Cabecera de `deck_part1.py` con el rango real (1–14) | código |

| Comprobación | Resultado |
|---|---|
| `check.py` | CORRECTO: 32 diapositivas, notas completas, 17 tablas nativas, QR y logotipo byte a byte |
| Render | PDF de 32 páginas, SHA-256 `c53944e1…`; diapositivas cambiadas revisadas |

## Endurecimiento y comprobación del 21/11/2026

Cambios aplicados en `material/S19/demo-evaluacion/`, `material/S19/checklist.md` y el
`[tool.ruff]` de `pyproject.toml` raíz (sin tocar la presentación ni otros módulos):

- **Coste en Langfuse (`rag/costes.py`, `rag/consulta.py`, `rag/observabilidad.py`).** Añadido
  `desglose_coste_usd` (`input`, `output`, `total` en USD con `tarifas.json`) y envío de
  `cost_details` en la observación de generación cuando tarifa y tokens son conocidos (nunca `0`
  si falta dato). En `registrar_evaluador`, envío de `cost_details` (`total`) solo si todas las
  filas del caso traen `coste_usd`. Validado contra el SDK real (`langfuse==5.2.0`) con
  `tracing_enabled=False`.
- **Protección con `--fijar` en `calibrar` y `umbrales` (`s19.py`).** Si ya existe entrada del
  perfil en `datos/calibracion.json` o `datos/umbrales.<perfil>.json`, el comando calcula y
  muestra los valores nuevos junto a los fijados sin sobrescribir el archivo; solo escribe si
  no existe aún o si se pasa `--fijar`. Los comandos de las diapositivas 14 y 26 siguen
  funcionando tal cual, sin alterar `datos/` durante el directo.
- **Versión servida de modelo (`model_version`).** `GeneradorGemini.generar` lee
  `r.model_version` (`google-genai==3.3.0`) y se propaga a `Generacion`, `Respuesta`, filas de
  `respuestas.jsonl` (campo aditivo compatible con `s19.respuestas.v1` y con los ejemplos
  existentes), `manifiesto.json` (`versiones_modelo`) y metadatos de la observación de generación
  en Langfuse. En el perfil doble es `None` (`[]` en el manifiesto).
- **Segmentación de `GeneradorDoble` (no aplicada).** Corregir `frases()` en `rag/proveedores.py`
  para no partir dentro de backticks (`` `Authorization: Bearer <token>` `` y
  `` `error_code: "RATE_LIMIT_EXCEEDED"` ``) cambia las métricas del ejemplo doble: en `test-A`,
  T05 pasa a acertar (`aciertos` 6/14 → 7/14, `tasa_aciertos` 0,4286 → 0,5000) y
  `answer_relevancy` varía en `validacion-A` (0,4136 → 0,4044), `test-A` (0,4423 → 0,4290) y
  `test-B` (0,5250 → 0,5070), alterando también `comparacion-A-B` y los umbrales derivados. Para
  conservar idénticas las cifras publicadas en `resultados/ejemplo-doble/` y en la presentación,
  se deja sin aplicar.
- **Formato y lint.** Reformateada la demo con `ruff format .` (26 archivos) y añadido
  `extend-exclude = [".build", "material/*/fuentes"]` en `[tool.ruff]` de la raíz.

| Comprobación | Resultado |
|---|---|
| `uv lock --check` (demo y `evaluador/`) | `Resolved 53 packages` y `Resolved 107 packages` |
| `uv run --frozen ruff check .` (demo) | `All checks passed!` |
| `uv run --frozen ruff format --check .` (demo) | `58 files already formatted` |
| `uv run --frozen pytest -q` (demo) | `73 passed, 2 deselected` |
| `(cd evaluador && uv run --frozen pytest -q)` | `15 passed, 1 deselected` |
| `uv run --frozen ruff check .` (raíz) | `All checks passed!` |
| `uv run --frozen ruff format --check .` (raíz) | `222 files already formatted` |
| `uv run --frozen pytest -q` (raíz) | `65 passed, 1 warning` |
| `uv run --frozen pytest -q -m db` (Docker pgvector) | `1 passed, 74 deselected` |
| Recorrido doble completo (`docs/comandos.md`) | `preflight`, `ingestar` A/B, Vivo 1, `calibrar` y `umbrales` sin sobrescribir `datos/`, lotes + Ragas + informes, `regresion` (0 en val-A; 1 en val-B y 3 degradados; 2 en informe incompleto) y `comparar`: **sin diferencias** frente a `resultados/ejemplo-doble/` ni en `datos/` |

Contenedor `thepower-s19-pgvector` retirado (`docker compose down -v`), carpeta `resultados/ensayo-*`
eliminada y Docker Desktop cerrado. Nota para las diapositivas: las notas de la diapositiva 26
siguen mencionando «66 pasan» (ahora son 73 tests offline en la demo); los comandos de las
diapositivas no requieren cambios.

## Cierre de pendientes · 21/11/2026 (noche)

| Qué | Resultado |
|---|---|
| Docker Desktop | La VM se cayó a las 23:26 porque se cerró Docker justo después de `docker compose down -v`, con el borrado aún en curso. Quedó un contenedor a medio borrar (`RWLayer … unexpectedly nil`); se eliminó y se recreó. Después: pgvector 0.8.7, `pytest -m db` 1 pasa y dos ciclos `up`/`down` limpios. Al terminar se recoge con `docker compose down -v` y no se cierra Docker en el mismo instante |
| Presentación | Cifras de tests actualizadas (66 → 73) en las diapositivas 4 (notas), 22, 23 y 32 y en las notas de la 26. Terminal de la 14 y notas de la 14 y la 26 con la salida nueva de `calibrar` y `umbrales` (no sobrescriben sin `--fijar`). `check.py` CORRECTO (32 diapositivas, 17 tablas); PDF de 32 páginas; 14, 22, 23 y 32 revisadas sobre el render. SHA-256 PPTX `8832c351…`, PDF `4cb427b8…` |
| Keynote | No se pudo abrir el PPTX por automatización (Keynote no llega a crear el documento sin intervención). Sigue pendiente abrirlo a mano |
| Paquete para alumnos | `scripts/empaquetar_s19.py` → `paquetes/S19-demo-evaluacion.zip` (114 archivos, determinista, SHA-256 en `paquetes/manifiesto.json`). Respeta los `.gitignore`, añade `ENUNCIADO.md` sin identificadores de correo y excluye el guion del profesor |
| Prueba del paquete | Descomprimido en una carpeta limpia: `uv sync --frozen` (demo y evaluador), `ruff check` limpio, 73 + 15 tests, y recorrido de clase completo con pgvector (preflight, ingesta A/B, Vivo 1, calibrar y umbrales sin escribir, lote + Ragas + informe, regresión 0 y 1 con la copia degradada, comparar, revisión, estimar). Cifras iguales que `resultados/ejemplo-doble/` |
| Cobertura y README | `cobertura.md` y `README.md` con 73 tests; `docs/ejercicio.md` apunta a `ENUNCIADO.md` del paquete |

Pendiente de José: perfil real (gasto), publicar el paquete o un repositorio para los alumnos,
validar los recortes de tiempo del 20/11, ensayo cronometrado y abrir el PPTX en Keynote o PowerPoint.

## Perfil real sobre OpenRouter · 21/11/2026

Petición de José: el perfil real usa siempre OpenRouter y cualquier modelo (generación,
embeddings, juez y embeddings del juez) se cambia desde `.env`, sin tocar el código.

| Qué | Cambio |
|---|---|
| Proveedor | `google-genai` retirado de los dos proyectos; cliente `openai==3.3.0` contra `https://openrouter.ai/api/v1` (`S19_OPENROUTER_BASE_URL`). Clave única: `OPENROUTER_API_KEY` |
| Configuración | Todo desde `.env`: modelos, dimensión de embeddings y si se pide, plantillas de documento y consulta, tokens máximos y temperatura (vacía = no se envía), orden fijo de proveedores (`S19_*_PROVEEDORES`), campos extra en JSON (`S19_*_EXTRA`) y parámetros que se quitan al juez. Un test comprueba que `.env.example` documenta todas las variables que lee el código |
| Valores por defecto | Generación `google/gemini-3.5-flash-lite`; embeddings `openai/text-embedding-3-small` (768); juez `anthropic/claude-haiku-5.5`, de otra familia; embeddings del juez `openai/text-embedding-3-small`. Verificados en el catálogo de OpenRouter el 21/11 |
| Coste | Se guarda lo que cobra OpenRouter (`usage.cost`, `coste_fuente: "openrouter"`) en el RAG y, aparte, en el juez; si falta, estimación con `tarifas.json` (`"tarifa"`). Langfuse recibe ese coste |
| Catálogo | `python s19.py catalogo`: lee la API pública de OpenRouter (sin clave ni coste) y escribe `tarifas.json` con precios, tipo y parámetros admitidos. Un modelo inexistente es un error con sugerencias |
| Preflight real | Comprueba clave (sin mostrarla), que cada modelo está en el catálogo, parámetros no admitidos y si el umbral de evidencia está calibrado para el modelo de embeddings actual |
| Índice | La columna `vector` ya no tiene dimensión fija y se retira el HNSW (exige dimensión fija; la evaluación usaba búsqueda exacta). Migración idempotente en `esquema.sql`. La identidad del índice real incluye plantilla y envío de dimensión. Conviven índices de dimensiones distintas |
| Comparación | `gen_modelo` puede ser la variable de una A/B (solo perfil real); el modelo de embeddings debe coincidir. El manifiesto guarda `proveedores_servidos`, `versiones_modelo` y `coste_embeddings_usd` |
| Estimación | Con los modelos por defecto: 566 llamadas como máximo, **0,13 USD** estimados, **0,76 USD** de cota (antes 0,57 y 4,66 con Gemini directo) |

| Comprobación | Resultado |
|---|---|
| `uv lock --check` | Demo 46 paquetes · evaluador 100 paquetes |
| Demo: `ruff check` / `ruff format --check` | Limpio · 61 archivos formateados |
| Demo: `pytest -q` | **95 passed, 3 deselected** (21 tests nuevos en `tests/test_openrouter.py`, con el cliente `openai` real y HTTP simulado) |
| Demo: `pytest -m db` | **2 passed** (nuevo: índices de 768 y 1536 dimensiones en la misma base) |
| Evaluador: `pytest -q` | **17 passed, 1 deselected** (OpenRouter simulado: coste cobrado, coste estimado, proveedores, extra y parámetros quitados en cada petición) |
| Migración del esquema | Base creada con el esquema del commit `ea0f863` (`vector(768)`) → esquema nuevo aplicado dos veces: `vector`, sin HNSW, sin errores |
| Recorrido doble completo en pgvector | Métricas, casos y comparación **idénticos** a `resultados/ejemplo-doble/`; `datos/` sin cambios; regresión 0 / 1 / 1 |
| Perfil real sin clave | `ingestar` sin `--execute` y con él, y `evaluar.py --modo real`, terminan con error claro sin llamar a nada |
| Raíz | `ruff check` limpio · 226 archivos formateados · 65 tests |
| Presentación | Diapositivas 18 (entorno: openai, 46 y 100 paquetes; juez vía OpenRouter), 22, 23 y 32 (95 tests) y 31 (estimación nueva); notas de 4, 18, 22, 26 y 31. `check.py` CORRECTO; PDF de 32 páginas; 18 y 31 revisadas sobre el render. SHA-256 PPTX `38d06b24…`, PDF `fa22cc1e…` |
| Paquete de alumnos | Regenerado (117 archivos) y probado en carpeta limpia: 95 + 17 tests y `estimar` |

Pendiente: ninguna llamada real a OpenRouter (sin clave ni gasto autorizado). Sin verificar
contra la API: que OpenRouter respete `dimensions` en `openai/text-embedding-3-small`, que el
juez `anthropic/claude-haiku-5.5` devuelva JSON válido para Ragas con `response_format` y que
`usage.cost` llegue en las respuestas de embeddings.

### Modelos por defecto del perfil real · 22/11/2026

Petición de José: generación con **Gemini 4 Hydrogen** y juez de Ragas con **Claude Opus 5.5**.

| Qué | Resultado |
|---|---|
| Identificadores en OpenRouter (catálogo del 22/11) | `google/gemini-4-hydrogen` (1,50 / 7,50 USD por millón; admite `temperature`) y `anthropic/claude-opus-5.5` (4 / 20 USD; admite `response_format`, **no** `temperature` ni `top_p`) |
| Juez sin `temperature`/`top_p` | El evaluador quita automáticamente los parámetros que Ragas envía y que el catálogo dice que el juez no admite; queda registrado en sus ajustes. Test nuevo |
| Margen de tokens | `S19_GEN_MAX_TOKENS` por defecto 2048: Gemini 4 puede razonar y esos tokens cuentan dentro del máximo |
| Estimación | 566 llamadas como máximo; **2,91 USD** estimados y **24,90 USD** de cota (antes 0,13 y 0,76). Casi todo es el juez |
| Comprobaciones | Demo 95 passed, 3 deselected · evaluador 18 passed · ruff limpio (demo y raíz) · raíz 65 tests · preflight real reconoce los cuatro modelos · presentación regenerada (diapositiva 31 revisada; `check.py` CORRECTO; PPTX `2f968daf…`, PDF `5f69c5bd…`) · ZIP regenerado |

## Perfil real ejecutado · 22/11/2026

Gasto autorizado por José; clave de OpenRouter entregada con el sistema de secretos de T3 Code y
guardada solo en `demo-evaluacion/.env` (ignorado por Git; no aparece en resultados ni en el ZIP).
Modelos: Gemini 4 Hydrogen (generación), `openai/text-embedding-3-small` (768) y Claude Opus 5.5 (juez).

| Paso | Resultado |
|---|---|
| Clave | Válida; límite 15 USD, que también descuenta lo que facturan los proveedores con BYOK |
| Prueba corta | Embeddings de 768 dimensiones; Gemini responde y cita; Opus devuelve JSON con `response_format` |
| **Fallo encontrado: coste 0 con BYOK** | La cuenta usa claves propias de los proveedores: `usage.cost` es solo la comisión de OpenRouter (0) y la inferencia va en `cost_details.upstream_inference_cost`. Corregido en el RAG y en el juez, con tests |
| **Fallo encontrado: respuestas vacías** | Primera pasada: 3 casos con los 2048 tokens gastados razonando (`finish_reason=length`). Con `reasoning.effort=low` responde y cuesta menos de la mitad. Ahora es el valor por defecto (`S19_GEN_EXTRA`) y se avisa `max_tokens_agotado`. La primera pasada se conserva en `resultados/ejemplo-real/primera-pasada-razonamiento-libre/` |
| **Fallo encontrado: test `llm` del evaluador** | Se saltaba porque no cargaba `../.env`. Corregido; ahora pasa |
| Indexación y calibración | A 41 y B 13 fragmentos; umbral de evidencia 0,5223 (7/8 en validación) |
| Segunda pasada (definitiva) | Sin respuestas vacías. Test A: precision@5 0,24, recall@5 1,00, rechazos 6/6, abstenciones 1/14, aciertos 13/14, faithfulness 0,92 y answer_relevancy 0,87 con cobertura 13/13. Test B: aciertos 11/14, abstenciones 3/14 |
| Regresión (umbrales de validación A, fijados antes del test) | Validación A y test A: PASA (0). Validación B: FALLA (1), abstenciones 0,20 > 0,10 |
| Tests de pago | `pytest -m llm`: RAG 1 passed; evaluador 1 passed |
| Coste | Segunda pasada: 1,292 USD registrados (0,091 RAG + 1,201 juez) frente a 1,288 USD que bajó el saldo. Total de toda la jornada (pruebas, diagnóstico y dos pasadas): **2,76 USD** (saldo 15 → 12,24) |
| Después | Demo 103 passed, 3 deselected · `-m db` 2 passed · evaluador 19 passed · ruff limpio (demo y raíz) · raíz 65 tests · presentación regenerada (31 con el rótulo «PERFIL REAL · MEDIDO EL 22/11/2026»; 22, 23 y 32 con 103 tests; `check.py` CORRECTO; PPTX `00a8f0b0…`, PDF `8880ce5b…`) · ZIP regenerado con `resultados/ejemplo-real/` (173 archivos, sin la clave) |

Pendiente: revisión manual humana de `resultados/ejemplo-real/test-A/revision-manual.csv`; Langfuse contra un servidor.

## LangGraph, chat en terminal, evaluación de modelos y métricas de producción · 22/11/2026

Petición de José: refactorizar el RAG a **LangGraph** con una interfaz de terminal como la de la
primera clase (OpenTUI de `1-langGraph`), cubrir los cuatro bloques del temario y dejar Langfuse
listo para cuando haya claves. Código copiado y adaptado, sin depender de aquel repositorio.

| Qué | Resultado |
|---|---|
| Dependencias | `langgraph==1.2.11`, `langchain-core==1.5.5`, `opentui==0.1.2` (las de S5/S6). `uv lock --check` correcto; el evaluador no cambia |
| Consulta como grafo (`rag/grafo.py`) | `recuperar → generar → comprobar` o `recuperar → rechazo_previo`. `responder()` conserva firma y salida. Perfil doble antes y después: **56 de 56 respuestas idénticas** (validación y test, A y B; sin contar latencias) |
| Trazas desde nodos | Cada paso cuelga explícitamente de la raíz `consulta-rag`. Comprobado con el SDK real (tracing activo, envío a un puerto cerrado): `recuperacion` y `generacion` con padre = raíz y la misma traza |
| CRAG como agente LangGraph | `recuperar ⇄ reformular → responder | rechazar`, `Trayectoria.ruta`, `recursion_limit` como red de seguridad. Tests de trayectoria y de una regla rota cortada por `GraphRecursionError` |
| Chat `s19.py chat` | Motor sin pantalla (`ui/motor.py`) + TUI (`ui/tui.py`, `ui/rag_tui.py`). Probado en pseudo-terminal 160×45 con perfil doble (3 preguntas) y real (T12 con Hydrogen, `/perfil sol-opus`, T12 con Sol), pantalla reconstruida con `pyte`. Corregidos en esa prueba: cabecera que no cambiaba con `/perfil`, coste con punto y línea del juez demasiado larga |
| `--env` | En todos los comandos de `s19.py` y en `evaluar.py`; un archivo inexistente es un error. `/perfil` en el chat cambia de archivo sin arrastrar valores (`cargar_env(sustituir=True)`) |
| **Fallo encontrado: coste del sistema** | El informe solo sumaba las respuestas emitidas y dejaba fuera los rechazos del modelo, que se pagan. Corregido (rechazo previo = único sin llamada). Test A real de Hydrogen: 0,031 → **0,041 USD**. Informes y comparaciones versionados regenerados |
| Métricas de producción | Bloque «Producción» del informe: p50/p95 (rango más cercano), tasas de error y rechazo, rechazos sin modelo, coste por consulta y por 1.000, peso del juez. `comparar` añade p95 y coste por consulta |
| Evaluación de modelos (`MH`/`MS`, juez Opus, `--env .env.sol-opus`) | Hydrogen 13/14, Sol 12/14 (T12 «24×7», T14 «ms»: fallos del criterio); faithfulness 0,92 / 1,00; p95 3,65 / 1,88 s; 2,13 / 1,00 USD por 1.000 consultas. `comparar` la acepta (solo cambia `gen_modelo`); regresión PASA en las dos. `resultados/ejemplo-real/modelos/` |
| Variabilidad observada | T12 con Sol: «24x7» (test del 22/11, acierto), «24×7» (evaluación `MS`, fallo) y «No consta» (prueba del chat). Recogido en el guion del directo |
| Langfuse | Bloque de claves vacío en `.env.hydrogen-sol` y `.env.sol-opus`; con `on` y sin claves, `preflight` falla con mensaje claro. **Envío a un servidor sin probar** (faltan claves) |
| Gasto | 0,98 USD en chat real, evaluación de modelos y prueba `llm` (saldo 11,15 → 10,17) |
| Después | Demo **131 passed**, 3 deselected · `-m db` 2 passed · `-m llm` (Sol) 1 passed · evaluador 19 passed · ruff limpio (demo y raíz) · raíz 65 tests · `cfn-lint` correcto · presentación regenerada (22, 23, 32 con 131 tests; 24 con el agente LangGraph; `check.py` CORRECTO; PPTX `881d816a…`, PDF `ee766e49…`) · ZIP regenerado (197 archivos, sin claves ni guion del profesor) y probado descomprimido: 131 + 19 tests |

Pendiente: claves de Langfuse y prueba de envío; ver el chat en la terminal de José; revisión
manual humana de `resultados/ejemplo-real/test-A/revision-manual.csv`.
