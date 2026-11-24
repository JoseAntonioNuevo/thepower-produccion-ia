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

## Langfuse Cloud · 22/11/2026

Región UE (`https://cloud.langfuse.com`), organización `thePower`, plan Hobby y
proyecto [s19-evaluacion](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l).
La sesión [langfuse-prueba-hydrogen](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions/langfuse-prueba-hydrogen)
muestra 16 trazas: 8 de consulta y 8 del evaluador.

### Ejecución

Los comandos de Python se ejecutaron con `UV_NO_SYNC=1` y los entornos ya instalados.
El portapapeles se vació después de copiar las claves. Los dos archivos de clase
ignorados por Git quedaron con `S19_LANGFUSE=on` y el host de la UE. El `.env`
activo siguió en `off`. Ambos preflights mostraron «Langfuse: activado»,
«Preflight correcto» y el índice A presente con 41 fragmentos.

```bash
uv run python s19.py preflight --env .env.hydrogen-sol
uv run python s19.py preflight --env .env.sol-opus
uv run python s19.py lote --env .env.hydrogen-sol --conjunto validacion --config A \
  --run langfuse-prueba-hydrogen --salida resultados/langfuse-prueba-hydrogen --execute
uv run python s19.py informe resultados/langfuse-prueba-hydrogen
(cd evaluador && uv run python evaluar.py ../resultados/langfuse-prueba-hydrogen \
  --env ../.env.hydrogen-sol --modo real --execute)
uv run python s19.py informe resultados/langfuse-prueba-hydrogen
uv run python -c 'from pathlib import Path; from rag.config import cargar_env; from s19 import main; cargar_env(Path(".env.hydrogen-sol")); raise SystemExit(main())' \
  publicar-evaluador resultados/langfuse-prueba-hydrogen --env .env.hydrogen-sol
```

La publicación precargó el perfil con el lector de la demo porque
`cmd_publicar_evaluador` inicializa el trazador antes de cargar la configuración.
Como comprobación previa, el lector de `uv run --env-file` devolvió
``Failed to parse environment file `.env.hydrogen-sol` at position 14`` en
la línea JSON de configuración de razonamiento.

### Casos y comprobación en Brave

Antes de publicar Ragas, **Sessions** mostró 8 trazas `consulta-rag`.
**Tracing** mostró sus 22 observaciones con `s19`, `config:A` y `perfil:real`.
En V02 se comprobó el árbol con `recuperacion` y `generacion`, el prompt,
la respuesta con la fuente `03-limites-y-cuotas-api`, la latencia de generación
de 1,66 s, el modelo `google/gemini-4-hydrogen`, 390 tokens de entrada,
161 de salida y 0,001793 USD en Langfuse. En **Scores** constaban
`precision_at_5`, `recall_at_5`, `rechazo` y `acierto_criterio`.
V07 y V08 tenían únicamente `recuperacion`, sin tokens ni coste visibles.

| Caso | Resultado del lote local | Scores Ragas en la traza de consulta (faithfulness / answer_relevancy) | Traza del juez en Tracing |
|---|---|---|---|
| V01 | Respondió | 1,0000 / 0,9125 | Presente |
| V02 | Respondió | 1,0000 / 0,9566 | Presente |
| V03 | Respondió | 1,0000 / 0,9617 | Presente |
| V04 | Respondió | 1,0000 / 0,9316 | Presente |
| V05 | Rechazo del generador en pregunta respondible | Sin scores Ragas | Presente, cero llamadas al juez |
| V06 | Rechazo del generador | Sin scores Ragas | Presente, cero llamadas al juez |
| V07 | Rechazo previo por `evidencia_insuficiente` | Sin scores Ragas | Presente, cero llamadas al juez |
| V08 | Rechazo previo por `evidencia_insuficiente` | Sin scores Ragas | Presente, cero llamadas al juez |

La interfaz de claves pide un nombre y un perfil de permisos. Se usó
`Application`, que permite crear trazas y guardar scores. **Sessions** y
**Tracing** son secciones separadas del proyecto. **Tracing** lista observaciones.
Según el ancho del panel, los scores se abren desde **More tabs → Scores** y el
modelo y los tokens desde **Show more details**.

**Incidencia en la primera publicación del consumo del juez.** Las ocho trazas
`evaluador-ragas` llegaron con la etiqueta `evaluador`. En V02,
`openai/gpt-6.2-sol` apareció en los metadatos, con cinco llamadas al juez.
Las columnas de tokens y coste quedaron sin valor incluso en V01–V04, donde
`puntuaciones.jsonl` sí registra consumo. Por ejemplo, V02 registró localmente
3.745 tokens de entrada, 253 de salida y 0,01064334 USD. En el SDK instalado
(`langfuse==5.2.0`), `start_as_current_observation` aplica `model`,
`usage_details` y `cost_details` a observaciones de tipo generación.
`as_type="evaluator"` sigue la rama de spans y descarta esos campos. La
publicación salió con código 0 y Langfuse mostró un total de sesión de unos
0,013 USD, correspondiente al RAG. El juez Sol completó la evaluación, así
que no se ejecutó la alternativa con Opus. Tras constatar el fallo de
instrumentación, quedó sin ejecutar la prueba opcional del chat.

**Gasto.** La lectura de `GET /api/v1/key` de OpenRouter pasó de
10,12133902 a 10,06454528 USD de saldo. La diferencia fue 0,05679374 USD.
Los resultados locales registraron aproximadamente 0,013036 USD del RAG y
0,04375410 USD del evaluador. El índice ya estaba cargado y no hubo ingesta.

### Corrección del consumo del juez · 22/11/2026

El publicador usa una observación `generation` llamada `consumo-juez` cuando
hay consumo. Así Langfuse conserva el modelo, los tokens y el coste en la traza
`evaluador-ragas` del caso. El subcomando ya carga `--env` antes de inicializar
Langfuse. Se reutilizaron `respuestas.jsonl` y `puntuaciones.jsonl`.

```bash
UV_NO_SYNC=1 uv run python s19.py publicar-evaluador resultados/langfuse-prueba-hydrogen \
  --env .env.hydrogen-sol --solo-consumo
```

En Brave, **Tracing** mostró estas cuatro observaciones con el modelo
`openai/gpt-6.2-sol`. La tabla redondea el coste a seis decimales.

| Caso | Entrada | Salida | Coste visible (USD) |
|---|---:|---:|---:|
| V01 | 3.821 | 274 | 0,011023 |
| V02 | 3.745 | 253 | 0,010643 |
| V03 | 3.794 | 284 | 0,011057 |
| V04 | 3.776 | 285 | 0,011031 |

El desglose de V02 en **Show more details** confirmó 3.998 tokens en total.
**Sessions** mantuvo las 16 trazas y mostró aproximadamente 0,057 USD
de consumo histórico conjunto. **Scores** mantuvo las ocho puntuaciones de
Ragas, dos por cada caso respondido. Las observaciones originales del juez
se conservaron. En V02, la duración de la traza histórica que muestra Langfuse
abarca el intervalo entre ambas publicaciones.

El gasto nuevo en OpenRouter fue **0 USD**. La corrección solo envió a Langfuse
consumo medido en la ejecución anterior. Pasaron 132 tests locales de la demo,
2 de integración con PostgreSQL y 65 del repositorio, además de Ruff y
`cfn-lint`.

### Chat T12 con Hydrogen y Terra · 22/11/2026

Se añadió el perfil local ignorado `.env.terra-opus` con
`openai/gpt-6.1-terra` para generar y `anthropic/claude-opus-5.5` como juez.
Se incorporó Terra al catálogo de precios y parámetros. El preflight del
perfil confirmó Langfuse activo y el índice A de 41 fragmentos. Se conservó
`.env.sol-opus` para los comandos de comparación ya documentados.

```bash
UV_NO_SYNC=1 uv run python s19.py preflight --env .env.terra-opus
UV_NO_SYNC=1 uv run python s19.py chat --env .env.hydrogen-sol --execute
```

Se ejecutó el chat OpenTUI en una pseudoterminal interactiva porque la
automatización de la app Terminal de macOS estaba bloqueada. En el mismo
proceso se introdujo `3`, luego `/perfil terra-opus` y después `3`.
El chat cerró con Esc y código 0.

En Brave, [chat-20261122-155649](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions/chat-20261122-155649)
mostró exactamente dos trazas `consulta-rag`. Ambas tenían `origen=chat`,
`caso_test=T12` y las observaciones `recuperacion` y `generacion`.

| Caso de la traza | `perfil_env` en Metadata | Modelo | Tokens totales | Coste visible (USD) |
|---|---|---|---:|---:|
| `01-T12` | `.env.hydrogen-sol` | `google/gemini-4-hydrogen` | 544 | 0,001782 |
| `02-T12` | `.env.terra-opus` | `openai/gpt-6.1-terra` | 550 | 0,001338 |

OpenRouter pasó de 10,06454528 a 10,06142396 USD de saldo. El gasto adicional
fue 0,00312132 USD y solo corresponde a las consultas del chat. Pasaron
los 18 tests locales de TUI y observabilidad.

### Ensayo de las tres pruebas del directo · 22/11/2026

- **Generador.** Hydrogen y Terra recibieron los mismos fragmentos, en el mismo orden,
  para T01 y T12. Se usaron el perfil base `.env.terra-opus`, la variante A y `v1`.
  Ambos citaron la fuente de TLS 1.3 en T01 y se abstuvieron después de generar en T12.
  Se guardaron respuestas, fuentes, latencia, tokens y coste de las cuatro llamadas.
- **Juez.** Se ejecutó Ragas con Sol y Opus sobre dos copias idénticas de V02,
  manteniendo los mismos embeddings, parámetros y máximo de 1024 tokens. Ambos dieron
  fidelidad 1,0000. La relevancia fue 0,9566 y 0,9585, con costes de 0,01064334 y
  0,02860928 USD, respectivamente.
- **Prompt.** Sobre la misma validación A, la configuración de las tres ejecuciones
  difería solo en `prompt_version`. En `v1`, `v2` y `regresion-rechazo`, recall@5 fue
  1,00. El prompt defectuoso pasó de 0/5 a 5/5 abstenciones incorrectas y de 4/5 a
  0/5 aciertos frente a `v1`. El control dio 0 para la referencia y 1 para el
  prompt defectuoso con `umbrales.real.json`. Ragas hizo cero llamadas en ese lote.

Los resultados nuevos se guardaron en `demo-evaluacion/resultados/ensayo-tres-pruebas-20261122/`,
ignorado por Git. Las comprobaciones nuevas se hicieron sobre esos archivos y la demostración
de Langfuse enlaza las sesiones ya verificadas. El saldo de OpenRouter pasó de 10,06142388
a 9,99732636 USD. El gasto nuevo fue **0,06409752 USD**.

### Regresión al sustituir el juez en T09 · 22/11/2026

Se compararon Hydrogen y Terra en los ocho casos de validación con `v1` y el mismo perfil
base. Ambos acertaron 4/5. En V06, el criterio de rechazo penalizó una respuesta
sustentada de Terra («Ninguna», seguida de las dos regiones que recoge el corpus), así que
ese caso se reservó para hablar del criterio. En el diagnóstico de T08, T13 y T14, ambos
modelos dieron los datos de referencia. En T14, Terra escribió `ms` donde el criterio
literal esperaba «milisegundos».

Se reprodujo una regresión del evaluador con T09 del test A. Sol y Opus recibieron
exactamente la misma respuesta, pregunta y fragmentos, con las mismas opciones de Ragas,
embeddings y máximo de 1024 tokens. La respuesta une un máximo de 45 minutos de mantenimiento
al mes y un aviso con al menos 7 días naturales, tal como hace la fuente.

| Juez | Faithfulness | Answer Relevancy | Coste de evaluar (USD) |
|---|---:|---:|---:|
| GPT‑6.2 Sol | 1,0000 | 0,7491 | 0,01283984 |
| Claude Opus 5.5 | 0,0000 | 0,6911 | 0,05257002 |

Se repitió Faithfulness conservando las afirmaciones y veredictos que devolvió cada juez.
Sol extrajo una afirmación con ambas condiciones y la verificó. Opus extrajo dos
afirmaciones que convertían cada condición en suficiente por sí sola. El verificador
dio 0 a cada una por la condición omitida. La repetición volvió a dar 1,00 y 0,00.

Los artefactos están en `demo-evaluacion/resultados/ensayo-regresion-modelo-20261122/`.
El saldo de OpenRouter pasó de 9,99732636 a 9,90512232 USD. El gasto nuevo fue
**0,09220404 USD**.

## Presentación rehecha: sistema y tres pruebas · 22/11/2026

El deck pasa de 32 a **20 diapositivas**: 15 de recorrido (portada, QR y recorrido, cuatro de
repaso del sistema y tres pruebas con su diapositiva de pregunta y de resultado, más el cierre)
y 5 de anexo (métricas, A/B 320 → 900, histórico Hydrogen–Sol, prompt NO_CONSTA y comandos).
Se retiraron del recorrido los casos de uso genéricos, las tablas repetidas de conceptos, el
detalle de denominadores, instalación y versiones, la ampliación CRAG y el esquema que daba
Langfuse por no probado. Fuentes en `fuentes/presentacion/`; guion docente renumerado.

| Comprobación | Resultado |
|---|---|
| `build.py` | 20 diapositivas; dos avisos conservadores de desborde (2 y 13) que caben en el render |
| `check.py` | **CORRECTO**: 20 diapositivas con notas completas (franja, QUÉ ABRIR, PREGUNTA, Fuentes), 4 tablas nativas, 23 imágenes, solo Arial/Georgia/Courier New, nada fuera del lienzo, QR de S16 y logotipo de thePower byte a byte. El recuento esperado pasa de 32 a 20 |
| Render | LibreOffice del runtime local → PDF de 20 páginas (960 × 540 pt) → PNG con `pdftoppm`; las 20 revisadas a tamaño completo o en hojas de dos y en hoja de contactos del PDF final |
| Correcciones tras verlas | Resaltado del Markdown (4), latencias tapadas por las marcas (6), fragmento partido (8), fichas fuera de su columna (10, 11), barras de coste sin ancho (12), texto de la respuesta sobre el pie (13), rótulos solapados (14), comillas invertidas literales (15, 17) |
| Logotipos nuevos | OpenTUI (opentui.com), LangGraph (repositorio oficial), OpenRouter (kit de marca openrouter.ai/brand), descargados el 22/11/2026 a `.build/s19/descargas/` y convertidos con `preparar_assets.py`; pgvector sin marca propia: nombre e icono genérico |
| Datos de las diapositivas | Tomados de archivos guardados; no se llamó a ningún modelo. Se ejecutaron en local, sin coste, la comprobación de T09 (Sol 0, Opus 1), `s19.py regresion` sobre `ejemplo-real/test-A` (PASA con T09 = 0 y fidelidad media 0,9231), `validacion-A` (PASA) y `regresion-rechazo` (FALLA), y `s19.py estimar` |
| Históricos intactos | SHA-256 de los 64 archivos de `resultados/ejemplo-real/modelos/`, `ensayo-tres-pruebas-20261122/`, `ensayo-regresion-modelo-20261122/` y `langfuse-prueba-hydrogen/` idénticos antes y después; `guion-directo-modelos.md` sin cambios |
| `ruff` de la raíz | Limpio (`material/*/fuentes` está excluido en `pyproject.toml`) |
| Ajustes tras la revisión de José | 2: la línea pregunta «¿coinciden los jueces en T09?» y no adelanta el fallo. 5: el rechazo previo tiene «0 tokens de generación», porque `recuperar` ya calculó el embedding de la pregunta. 9: en la misma sesión se vuelve antes con `/perfil hydrogen-sol` (o se usa el comando completo de la 7). 13: «si el contexto respalda todas las afirmaciones, esperamos fidelidad 1,00». 4, 6 y 10 aligeradas: documento, fragmento y vector; qué recuperó, qué respondió y cuánto costó; el fragmento del plan en el puesto 6 frente a los 4 leídos. Guion docente y anexo de comandos alineados |
| SHA-256 PPTX | `64ac05c7c2644cda3d13e5b2d595aceaeda6c1dd808a9e99a77b37d7985346fc` |
| SHA-256 PDF | `e6fee4d1b8de78cb1fcd4de5c7d29c17f01486106e33bc26b50a5a9e732529be` |

La traza de la diapositiva 6 es una recreación rotulada con los datos de V02 comprobados en
Brave; no hay capturas. Los veredictos de T09 se rotulan como resultado local. No se ha abierto
el PPTX en PowerPoint ni en Keynote. El ZIP de alumnos no se ha regenerado: `docs/comandos.md`
cambió solo en los números de diapositiva de sus encabezados.

## Ensayo del directo · 24/11/2026

Se ejecutó OpenTUI en una terminal interactiva de tmux y se abrió Langfuse en Brave.
Computer Use denegó el control directo de Warp. En la repetición descrita al final, José
conectó Warp como espectador de la sesión de tmux y confirmó que veía la TUI.
Los dos perfiles reales pasaron el preflight con el índice A de 41 fragmentos.
Ambos usaron el prompt v1 y dejaron la temperatura sin fijar.

| Caso | Resultado del chat | Tokens de generación (entrada → salida) | Coste de generación mostrado (USD) |
|---|---|---|---:|
| T17 · Hydrogen | Rechazo previo, similitud 0,3807 frente a umbral 0,5223 | 0 → 0 | 0 |
| T01 · Hydrogen | TLS 1.3 con cita de arquitectura | 404 → 149 | 0,001723 |
| T01 · Terra | TLS 1.3 con la misma cita | 366 → 30 | 0,000516 |
| T12 · Hydrogen | Abstención tras generar, recall@5 de 1,00 | 383 → 203 | 0,002097 |
| T12 · Terra | Abstención tras generar, recall@5 de 1,00 | 353 → 51 | 0,000608 |

En Brave se vieron las tres trazas de [T17 y T01](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions/chat-20261124-131903)
y las dos de [T12](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions/chat-20261124-131914).
Se comprobaron el perfil, el modelo, los tokens y el coste de cada turno de T12. La suma
de las cifras de generación mostradas es 0,004944 USD. El coste del embedding de cada
consulta queda fuera de esa suma.
Se corrigieron los rótulos de coste de OpenTUI y se repitió T17 con la versión corregida.

En V02 se compararon las entradas congeladas byte a byte y se leyeron las puntuaciones
guardadas. Ambos jueces dieron fidelidad 1,00. En Brave se comprobó el respaldo de
«4 MiB», la puntuación de la consulta y la observación `consumo-juez` de Sol (0,010643 USD).
En T09 se volvió a ejecutar el control por caso sobre los veredictos guardados.
Sol devolvió 0 y Opus devolvió 1. El control agregado del test A pasó.

Se regeneró el ZIP del alumno, se verificaron sus 197 archivos contra las fuentes y se
instalaron los dos entornos desde los locks en una extracción limpia. El recorrido doble
completó los 56 casos de los cuatro lotes A/B sin errores de ejecución. Se generaron los
informes, la comparación y la plantilla de revisión. El control pasó en la referencia y
falló con la recuperación degradada. Pasaron 132 pruebas de la demo, 2 de pgvector,
19 del evaluador y 65 del repositorio, además de Ruff, cfn-lint y el preflight offline.

### Repetición visible en Warp · 24/11/2026

Warp mostró la ventana compartida en modo de solo lectura. Otro cliente de tmux
envió las teclas a OpenTUI. Se comprobó la respuesta en pantalla tras cada turno.

| Caso y generador | Resultado | Tokens de entrada → salida | USD de generación mostrados |
|---|---|---:|---:|
| T17 · Hydrogen | Rechazo previo, similitud 0,3807 por debajo del umbral 0,5223 | 0 → 0 | 0 |
| T01 · Hydrogen | TLS 1.3 con cita de arquitectura | 404 → 137 | 0,001633 |
| T01 · Terra | TLS 1.3 con la misma cita | 366 → 30 | 0,000516 |
| T12 · Hydrogen | Abstención tras generar, recall@5 de 1,00 | 383 → 290 | 0,002750 |
| T12 · Terra | Abstención tras generar, recall@5 de 1,00 | 353 → 54 | 0,000623 |

En Brave se comprobaron las tres trazas de [T17 y T01](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions/chat-20261124-132521)
y las dos de [T12](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions/chat-20261124-133413).
En T17 apareció solo recuperación. En T12 se verificaron los dos perfiles, el modelo,
el coste de generación y la abstención de los dos turnos. La suma de generación de
esta repetición fue 0,005522 USD según los importes mostrados.

En la ventana de jueces se compararon las entradas congeladas de V02 y T09 con
`cmp`. En V02 ambos jueces dieron fidelidad 1,00 y relevancias 0,9566 y 0,9585.
En T09 el control por caso devolvió 0 con Sol y 1 con Opus. El control agregado
del test A pasó, al igual que las 132 pruebas locales de la demo.
