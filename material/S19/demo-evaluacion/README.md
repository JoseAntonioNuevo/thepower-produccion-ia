# S19 · RAG mínimo con evaluación y tests integrados

Proyecto de aula del programa **AI Engineer** de thePower. Construye un RAG pequeño desde
documentos en bruto y un índice vacío, mide **recuperación y generación por separado**,
compara dos configuraciones y demuestra que un control de regresión **falla cuando debe**.

Todo funciona **sin claves y sin coste** con el perfil `doble`. Ese perfil no usa ningún
modelo: comprueba que el sistema de evaluación funciona, **no mide la calidad de un modelo**.
Para medir de verdad se usa el perfil `real`, que exige `--execute`. Todos sus modelos pasan
por **OpenRouter** y se eligen en `.env`: generación, embeddings y juez se cambian sin tocar
el código (OpenAI, Anthropic, Google y otros con una sola clave).

La consulta es un **grafo de LangGraph** (`rag/grafo.py`), y se puede seguir paso a paso
en un chat de terminal con la misma librería de la TUI de S5/S6 (`python s19.py chat`).

```text
grafo de consulta:  START → recuperar ─┬─ similitud ≥ umbral → generar → comprobar → END
                                       └─ similitud < umbral → rechazo_previo → END (sin modelo)

corpus/ (10 .md ficticios) ──► fragmentar ──► embeddings ──► PostgreSQL + pgvector
                                                                    │
pregunta ──► embedding ──► 12 fragmentos ──► 5 documentos distintos ┤──► precision@5 · recall@5
                                   │                                │
                          ¿evidencia suficiente? ── no ──► «No consta…»   ──► rechazo (aparte)
                                   │ sí
                          generar con 4 fragmentos y citar [documento]
                                   │
                    respuestas.jsonl ──► evaluador/ (Ragas 0.4.3, entorno aparte)
                                   │                    │
                               informe ◄── puntuaciones.jsonl (valor o «no evaluable» + motivo)
                                   │
                 comparar A/B · control de regresión · Langfuse (opcional)
```

## Qué hay en cada carpeta

| Ruta | Para qué |
|---|---|
| `corpus/` | Diez documentos ficticios de «AetherCloud». Es lo único que se indexa |
| `datos/` | `test.jsonl` (14 + 6), `validacion.jsonl` (5 + 3), `criterios.md`, variantes A/B, calibración, umbrales |
| `rag/` | Ingesta, almacén pgvector, proveedores (doble y OpenRouter), catálogo de modelos, **grafo de consulta (LangGraph)**, costes, Langfuse |
| `evaluacion/` | Métricas, lote, informe, comparación, regresión, degradación de prueba, contrato JSONL |
| `evaluador/` | **Entorno aislado** con `ragas==0.4.3` y `langchain-community==0.3.31` |
| `ampliacion/` | Opcional: agente CRAG en LangGraph para practicar tests de trayectoria y límites |
| `ui/` | Chat en la terminal (OpenTUI, reutilizado de S5/S6): el grafo paso a paso, con criterio y trazas |
| `tests/` | pytest con dobles; `db` y `llm` excluidos por defecto |
| `resultados/ejemplo-doble/` | Resultados de ejemplo del perfil doble (rotulados) |
| `resultados/ejemplo-real/` | Ejecuciones reales del 22/11/2026: A/B de fragmentación y comparación de modelos |
| `s19.py` | Único punto de entrada |

## Antes de empezar

Para repetir las demos de clase, abre el [taller de S19](docs/taller-s19.md).
La [práctica opcional](docs/ejercicio.md) contiene el ejercicio paso a paso.

Necesitas **Python 3.12**, [uv](https://docs.astral.sh/uv/) y **Docker** en marcha. Los
comandos son los mismos en macOS, Linux y Windows (PowerShell o Git Bash).

```bash
git clone https://github.com/JoseAntonioNuevo/thepower-evaluacion.git
cd thepower-evaluacion
```

Si has descargado el ZIP, abre la carpeta que contiene `s19.py`. Desde esa carpeta:

```bash
uv sync --frozen             # instala las versiones del proyecto fijadas en uv.lock
cp .env.example .env         # perfil doble por defecto; no hace falta ninguna clave
docker compose up -d --wait  # PostgreSQL 17 + pgvector en 127.0.0.1:54519
uv run python s19.py preflight
```

El preflight debe terminar con «Preflight correcto: no se ha llamado a ningún modelo».

## Paso 1 · Reconstruir el índice desde cero

```bash
uv run python s19.py ingestar --config A    # chunk_size = 320 → 41 fragmentos
uv run python s19.py ingestar --config B    # chunk_size = 900 → 13 fragmentos
```

Cada configuración tiene **su propio índice**, identificado por una huella de corpus +
fragmentación + modelo de embeddings. Repetir el comando sustituye el índice: no duplica.

```bash
uv run python s19.py preguntar "¿Qué versión de TLS exigen las pasarelas perimetrales?"
uv run python s19.py preguntar "¿Cuál es el horario de la cafetería de la oficina de Madrid?"
```

La primera responde citando `[01-arquitectura-aethercloud]`; la segunda se rechaza.

### El grafo paso a paso: `chat`

```bash
uv run python s19.py chat                                  # perfil doble: sin coste
uv run python s19.py chat --env .env.hydrogen-sol --execute  # perfil real: Gemini 4 Hydrogen
```

Abre un chat en la terminal (necesita una terminal real: no funciona en una tubería). Cada
pregunta ejecuta **el mismo grafo que el lote** y enseña cada nodo al terminar: los documentos
recuperados con la similitud frente al umbral, la generación con tokens y coste, la comprobación
de fuentes o la rama de **rechazo previo**, que no llama al modelo. El panel lateral resalta el
nodo activo y el camino recorrido.

| Entrada | Qué hace |
|---|---|
| `1` … `7` | Preguntas del guion del directo (T01, T13, T12, T14, T15, T17, T08) |
| `T01` … `T20` | Cualquier pregunta del test, con el veredicto del criterio y la respuesta de referencia |
| `/perfil terra-opus` | Carga `.env.terra-opus` y cambia a GPT‑6.1 Terra en la misma sesión. `/perfil` lista los archivos |
| `/config B` | Fragmentos de 900; también `A`, `MH`, `MS` |
| `/casos`, `/ayuda`, `salir` o Esc | Lista del test, ayuda, salir |

Con Langfuse activo, cada pregunta del chat deja una traza igual a las del lote (sesión
`chat-<fecha>`). El juez de Ragas no actúa en el chat: se aplica a los lotes.

## Paso 2 · Decidir con validación, no con el test

```bash
uv run python s19.py calibrar --config A
```

Elige el **umbral de evidencia** (similitud mínima para intentar responder) con las ocho
preguntas de validación y lo guarda en `datos/calibracion.json` la primera vez que se ejecuta
ese perfil. Si el perfil ya tiene calibración fijada, calcula y muestra el valor nuevo junto
al fijado sin sobrescribir el archivo; para reemplazarlo hace falta `--fijar`. El test no se toca.

## Paso 3 · Ejecutar un conjunto y medir recuperación

```bash
uv run python s19.py lote --conjunto validacion --config A --salida resultados/mi-validacion-A
uv run python s19.py informe resultados/mi-validacion-A
```

El informe da cada métrica con su denominador:

- `precision@5` = documentos relevantes entre los 5 recuperados / **5**.
- `recall@5` = documentos relevantes entre los 5 recuperados / **documentos de referencia de esa pregunta**.
- Se cuentan **documentos distintos**: tres fragmentos del mismo documento son un acierto.
- Las preguntas sin respuesta no tienen recall: se mide aparte si el sistema las rechazó.

Con un solo documento relevante, `precision@5` no puede pasar de 0,20. Por eso el informe
enseña también el **techo**.

## Paso 4 · Medir la generación en el entorno aislado

```bash
cd evaluador
uv sync
uv run python evaluar.py ../resultados/mi-validacion-A     # juez doble: sin coste
cd ..
uv run python s19.py informe resultados/mi-validacion-A
```

El evaluador lee `respuestas.jsonl` y escribe `puntuaciones.jsonl`. No importa el código del
RAG: solo comparten archivos con `schema_version`. Detalles y hallazgos sobre la API de
Ragas en [evaluador/README.md](evaluador/README.md).

Lo que no se puede puntuar queda como **no evaluable con su motivo** (`rechazo_sin_respuesta`,
`error_sistema`, `respuesta_vacia`, `contexto_vacio`, `error_evaluador:…`, `nan`) y **resta
cobertura**. Nunca se convierte en acierto ni en cero.

## Paso 5 · Fijar umbrales y probar el control de regresión

```bash
uv run python s19.py umbrales resultados/mi-validacion-A      # calcula validación ± 0,10 (si ya existen, compara sin sobrescribir; usa --fijar para actualizar)
uv run python s19.py regresion resultados/mi-validacion-A     # PASA (código de salida 0)

uv run python s19.py degradar resultados/mi-validacion-A --modo recuperacion --salida resultados/mal-recuperacion
uv run python s19.py informe resultados/mal-recuperacion
uv run python s19.py regresion resultados/mal-recuperacion    # FALLA (código de salida 1)
```

Otros modos de `degradar`: `sin-rechazo`, `juez-caido`, `incompleto`. Un control que nunca
has visto fallar no demuestra nada.

## Paso 6 · Medir el test y comparar dos configuraciones

```bash
for c in A B; do
  uv run python s19.py lote --conjunto test --config $c --salida resultados/mi-test-$c
  (cd evaluador && uv run python evaluar.py ../resultados/mi-test-$c)
  uv run python s19.py informe resultados/mi-test-$c
done
uv run python s19.py comparar resultados/mi-test-A resultados/mi-test-B --salida resultados/mi-comparacion
```

`comparar` se niega a trabajar si las dos ejecuciones difieren en más de una variable, o si
no comparten conjunto, modelos y evaluador.

**Evaluar modelos** (solo perfil real): las variantes `MH` y `MS` de `datos/configuraciones.json`
solo cambian el modelo de generación. Se ejecutan con el **mismo** archivo de entorno, así que
comparten índice, prompt, parámetros y juez:

```bash
for m in MH MS; do
  uv run python s19.py lote --env .env.sol-opus --conjunto test --config $m --salida resultados/mi-test-$m --execute
  (cd evaluador && uv run python evaluar.py ../resultados/mi-test-$m --env ../.env.sol-opus --modo real --execute)
  uv run python s19.py informe resultados/mi-test-$m
done
uv run python s19.py comparar resultados/mi-test-MH resultados/mi-test-MS
```

El juez no debe ser ninguno de los candidatos: puntuaría mejor su propio estilo.

## Paso 7 · Revisión manual

```bash
uv run python s19.py revision resultados/mi-test-A
```

Crea `revision-manual.csv` con los seis casos elegidos **antes** de ejecutar el test
(`datos/revision-casos.json`). Las columnas humanas van vacías: las rellena una persona.
Hay un ejemplo relleno en `resultados/ejemplo-doble/test-A/revision-manual-EJEMPLO-rellena.csv`.

## Paso 8 · Tests

```bash
uv run pytest                 # 137 pasan; 1 fallo esperado por fuentes contradictorias
uv run pytest -m db           # integración con pgvector (necesita el contenedor)
uv run ruff check .
(cd evaluador && uv run pytest)   # 19 tests del evaluador, también sin red
```

Los tests marcados `llm` llaman a modelos de pago y **no se ejecutan por defecto**.

Para ver cómo cambia la respuesta al añadir, retirar o actualizar un documento, ejecuta
`uv run pytest -q -s tests/test_cambios_corpus.py`. Cada caso reindexa una copia temporal
y consulta el grafo con proveedores dobles. Para proyectar el conflicto de fuentes como
un fallo visible, añade `-k conflicto --runxfail --tb=short`: llegan ambos plazos al contexto
y el generador extractivo reproduce los dos. El criterio de este ejercicio exige abstención.

Para contrastar los mismos cambios **en el chat real**, ejecuta desde la demo:

```bash
uv run --frozen python s19.py preparar-corpus --config A --env .env.hydrogen-sol --execute
S19_PROMPT_VERSION=v1 S19_GEN_TEMPERATURE='' uv run --frozen python s19.py chat --config A --env .env.hydrogen-sol --execute
```

El ejemplo usa el perfil local del profesor. En otro equipo usa tu archivo de perfil real.
La primera preparación crea índices y consume embeddings; repetirla reutiliza los índices completos.
Dentro del chat, `/corpus base|alta|baja|actualizacion|conflicto` selecciona una versión ya preparada.
En Langfuse, la raíz de cada turno contiene `corpus`, `indice_id` y `fragmentos_en_prompt`.
El cambio solo afecta a ese chat; los lotes de evaluación siguen usando el corpus de referencia.

Además de formato, fuentes y errores, los tests comprueban **trayectorias**: qué nodos recorre
cada pregunta en el grafo de consulta (`tests/test_grafo.py`), que el rechazo previo no llama al
modelo, que el agente CRAG respeta su límite de intentos y que `recursion_limit` de LangGraph
corta una regla rota (`tests/test_enrutado.py`). El chat se prueba sin pantalla (`tests/test_tui.py`).

## Paso 9 · Recoger

```bash
docker compose stop           # conserva los índices para la siguiente sesión
```

## Resultados de ejemplo (perfil doble, 17/11/2026)

> No son una medición. El «sistema» doble copia frases y busca por palabras.

| Métrica (test, 20 casos) | A · 320 | B · 900 |
|---|---:|---:|
| precision@5 (techo 0,24) | 0,24 | 0,24 |
| recall@5 | 1,00 | 1,00 |
| Rechazos correctos | 2/6 | 4/6 |
| Abstenciones incorrectas | 4/14 | 8/14 |
| Aciertos por criterio | 6/14 | 3/14 |
| faithfulness (cobertura) | 1,00 (14/14) | 1,00 (8/8) |
| answer_relevancy (cobertura) | 0,44 (14/14) | 0,53 (8/8) |

Tres cosas que este ejemplo ya enseña:

1. **Recuperar bien no basta.** recall@5 = 1,00 y solo 6 de 14 aciertos: el fallo está después.
2. **Fiel no es correcta.** En T16 (pregunta sin respuesta) el juez doble da fidelidad 1,00 a un
   encabezado copiado. La revisión manual lo marca como respuesta indebida.
3. **El umbral depende del índice.** El umbral calibrado con A hace que B se abstenga el doble.
   El control de regresión lo detecta en validación antes de llegar al test.

Además, el test A **no cumple** los umbrales derivados de validación (3 reglas): ocho casos de
validación son pocos para generalizar. Se deja a la vista; no se retocan las reglas tras ver el test.

## Perfil real con OpenRouter · ejecutado el 22/11/2026

Requiere `OPENROUTER_API_KEY` en `.env`, `S19_PERFIL=real` y `--execute`. Recorrido completo
ejecutado el 22/11/2026 con Gemini 4 Hydrogen (generación), `openai/text-embedding-3-small`
(embeddings, 768) y Claude Opus 5.5 (juez). Resultados en `resultados/ejemplo-real/`:

| Métrica | Validación A | Validación B | Test A | Test B |
|---|---:|---:|---:|---:|
| precision@5 (techo 0,24) | 0,24 | 0,24 | 0,24 | 0,23 |
| recall@5 | 1,00 | 1,00 | 1,00 | 0,96 |
| Rechazos correctos | 3/3 | 3/3 | 6/6 | 6/6 |
| Abstenciones incorrectas | 0/5 | 1/5 | 1/14 | 3/14 |
| Aciertos por criterio | 4/5 | 4/5 | 13/14 | 11/14 |
| faithfulness · cobertura | 1,00 · 5/5 | 1,00 · 4/4 | 0,92 · 13/13 | 0,98 · 11/11 |
| answer_relevancy · cobertura | 0,90 · 5/5 | 0,93 · 4/4 | 0,87 · 13/13 | 0,89 · 11/11 |
| Coste del RAG (USD, medido) | 0,018 | 0,013 | 0,041 | 0,045 |
| Coste del juez (USD, medido) | 0,175 | 0,137 | 0,460 | 0,430 |

- **Umbral de evidencia calibrado con validación A:** 0,5223 (7 de 8 decisiones correctas).
- **Regresión:** pasa con validación A y con test A (código 0); falla con validación B
  (código 1: abstenciones 0,20 > 0,10). Los umbrales salen de validación A y se fijaron antes del test.
- **Comparación A/B (`chunk_size` 320 frente a 900):** B se abstiene más (3 de 14 frente a 1 de
  14) y acierta menos (11 frente a 13), aunque su fidelidad media es mayor. Cambian T08 y T14.
- **Coste:** una pasada completa (validación y test, A y B) costó **1,29 USD medidos**: 0,09 el
  RAG y 1,20 el juez. Coincide con lo que bajó el saldo de la clave (1,288 USD).
- **BYOK:** la cuenta usa claves propias de los proveedores. OpenRouter cobra solo su comisión
  (`cost` = 0) y la inferencia la factura cada proveedor (`cost_details.upstream_inference_cost`).
  El código suma las dos; sin eso, el coste habría salido 0.
- **Primera pasada (`ejemplo-real/primera-pasada-razonamiento-libre/`):** con razonamiento libre y
  2048 tokens, Gemini 4 Hydrogen gastó todo el máximo pensando en 3 casos y devolvió respuestas
  vacías. Quedaron como `respuesta_vacia` (no evaluables, no aciertos). Desde entonces el razonamiento
  va en `low` por defecto (`S19_GEN_EXTRA`) y se avisa `max_tokens_agotado`.
- **Coste del RAG:** incluye también los rechazos del modelo («No consta» tras leer los
  fragmentos), que se pagan igual. Hasta el 22/11 el informe solo sumaba las respuestas emitidas.
- **Pendiente:** la revisión manual humana de `ejemplo-real/test-A/revision-manual.csv`.

### Evaluación de modelos · 22/11/2026

Variantes `MH` (Gemini 4 Hydrogen) y `MS` (GPT-6.2 Sol): mismo índice A, prompt v1, sin
temperatura, razonamiento bajo y el mismo juez (Claude Opus 5.5). Resultados en
`resultados/ejemplo-real/modelos/`:

| Métrica (test, 20 casos) | Hydrogen (MH) | Sol (MS) |
|---|---:|---:|
| recall@5 | 1,00 | 1,00 |
| Rechazos correctos | 6/6 | 6/6 |
| Abstenciones incorrectas | 1/14 (T12) | 0/14 |
| Aciertos por criterio | 13/14 | 12/14 (T12, T14) |
| faithfulness · cobertura | 0,92 · 13/13 | 1,00 · 14/14 |
| answer_relevancy · cobertura | 0,86 · 13/13 | 0,88 · 14/14 |
| Latencia p50 / p95 | 2,54 s / 3,65 s | 1,61 s / 1,88 s |
| Coste por consulta · por 1.000 | 0,0021 USD · 2,13 USD | 0,0010 USD · 1,00 USD |
| Peso del juez en el coste | 91 % | 96 % |

Los dos fallos de Sol son del **criterio automático**, no del contenido: en T14 escribe «800 ms»
y el criterio exige «800 milisegundos»; en T12 escribe «24×7» (signo de multiplicar) en lugar de
«24x7» y deja sin responder qué soporte incluye el plan Empresa. En otra ejecución anterior Sol
escribió «24x7» y T12 contó como acierto: **el mismo modelo cambia de veredicto entre pasadas**.
Por eso existe la revisión manual y por eso no se retocan las reglas tras ver el test.

### Métricas de producción

Cada informe añade las cifras que se vigilan en producción, por consulta: **latencia p50 y p95**
(rango más cercano: con 20 consultas, p95 es la 19.ª más lenta), **tasa de error**, **tasa de
rechazo** separando los rechazos sin llamar al modelo, **coste por consulta y por 1.000
consultas** (generación + embeddings de la pregunta) y el **peso del juez** en el coste total.
`comparar` incluye p95 y coste por consulta.

**El proveedor es siempre OpenRouter**: una sola clave da acceso a modelos de OpenAI,
Anthropic, Google y otros, con una API compatible con la de OpenAI.

### Cambiar cualquier modelo desde `.env`

| Pieza | Variable | Por defecto |
|---|---|---|
| Generación | `S19_GEN_MODEL` | `google/gemini-4-hydrogen` |
| Embeddings del RAG | `S19_EMBEDDING_MODEL` · `S19_EMBEDDING_DIM` | `openai/text-embedding-3-small` · 768 |
| Juez de Ragas | `S19_EVAL_LLM_MODEL` | `anthropic/claude-opus-5.5` |
| Embeddings del juez | `S19_EVAL_EMBEDDING_MODEL` | `openai/text-embedding-3-small` |

Los nombres son los del [catálogo de OpenRouter](https://openrouter.ai/models) (`proveedor/modelo`).
Además se pueden ajustar desde `.env`, sin tocar código: tokens máximos y temperatura de la
generación, plantillas con las que se presentan los textos al modelo de embeddings, si se pide
la dimensión, el orden fijo de proveedores de OpenRouter (`S19_*_PROVEEDORES`), campos extra
en JSON (`S19_*_EXTRA`) y parámetros que se quitan al juez. Todo está explicado en
[.env.example](.env.example).

Para tener varias combinaciones sin copiar archivos, guarda cada una en su `.env.<nombre>` y
elígela con `--env` en cualquier comando (`python s19.py lote --env .env.sol-opus …`) o con
`/perfil <nombre>` dentro del chat. El evaluador acepta lo mismo: `evaluar.py … --env ../.env.<nombre>`.

Después de cambiar un modelo:

```bash
uv run python s19.py catalogo     # precios y parámetros admitidos (API pública, sin clave ni coste)
uv run python s19.py preflight    # comprueba clave, modelos y parámetros sin llamar a ninguno
uv run python s19.py estimar      # llamadas y coste previstos con los modelos nuevos
```

Reglas que el código hace cumplir:

- **Otro modelo de embeddings, otra dimensión u otra plantilla = otro índice.** Hay que volver a
  `ingestar` y a `calibrar --fijar`: un umbral de evidencia calibrado con otro modelo no vale y
  `preflight` lo avisa. La base guarda la dimensión de cada índice, así que conviven índices de
  modelos distintos (la columna `vector` no tiene dimensión fija; por eso no hay índice HNSW).
- **El modelo de generación puede ser la variable de una comparación A/B** (`gen_modelo` en
  `datos/configuraciones.json`, solo en el perfil real) con el mismo índice y el mismo juez.
- **Fija el proveedor al comparar.** OpenRouter puede servir un modelo desde varios proveedores.
  `S19_GEN_PROVEEDORES=Google` fija cuál y desactiva los cambios automáticos; el manifiesto
  guarda qué proveedor sirvió cada respuesta (`proveedores_servidos`).
- **Anthropic no tiene modelos de embeddings**: para embeddings usa OpenAI, Google, Qwen, etc.

### Coste

Cada respuesta de OpenRouter trae `usage.cost`, lo que cobró. Ese es el coste que se guarda
(`coste_fuente: "openrouter"`) para el RAG y, aparte, para el juez. Si una respuesta no lo
trae, se estima con `tarifas.json` y se rotula `"tarifa"`; si tampoco hay tarifa, queda sin dato.

```bash
uv run python s19.py estimar        # no llama a nada
```

| Partida | Llamadas (máx.) | Estimación | Cota superior |
|---|---:|---:|---:|
| Embeddings del RAG | 118 | 0,0004 USD | 0,0004 USD |
| Generación del RAG | 56 | 0,218 USD | 0,953 USD |
| Juez (Ragas) | 280 | 2,688 USD | 23,946 USD |
| Embeddings del juez | 112 | 0,0001 USD | 0,0001 USD |
| **Total** | **566** | **2,91 USD** | **24,90 USD** |

Con los modelos por defecto (Gemini 4 Hydrogen genera, Claude Opus 5.5 juzga) y los precios de
OpenRouter del 22/11/2026 (`tarifas.json`). La estimación usa los tamaños supuestos de
`datos/supuestos-coste.json`; la cota supone que cada respuesta agota su máximo de tokens. Casi
todo el gasto es del juez (Opus: 4 USD de entrada y 20 de salida por millón). Para abaratar,
baja `S19_EVAL_MAX_TOKENS` (acota la cota) o elige un juez más barato en `.env`. Secuencia exacta en [docs/comandos.md](docs/comandos.md#perfil-real).

## Langfuse (opcional)

Con `S19_LANGFUSE=on` y las claves `LANGFUSE_*`, cada consulta (del lote o del chat) deja una traza `consulta-rag`
con pregunta, respuesta, fuentes, documentos recuperados, latencia por paso, tokens y coste
de la generación, y las métricas como puntuaciones. El consumo del juez va en **otra traza**
(`evaluador-ragas`), que se publica con:

```bash
uv run python s19.py publicar-evaluador resultados/mi-test-A
```

Cada generación envía a Langfuse su coste (`cost_details`): el `total` cobrado por OpenRouter
o, si no llegó, el desglose `input`/`output`/`total` estimado con `tarifas.json`. La traza del
evaluador lleva el `total` del juez si todas las filas del caso lo tienen. Los metadatos de la
generación guardan el modelo exacto que sirvió la API (`model_version`) y el proveedor
(`proveedor_servido`). Si falta algún dato, no se envía coste (nunca `0`). Si en Langfuse un
modelo aparece sin coste, comprueba el nombre del modelo y define su precio en
Project Settings → Models. Cada paso del grafo (`recuperacion`, `generacion`) cuelga
explícitamente de la raíz de la traza, aunque LangGraph ejecute el nodo en otro hilo. El
envío a un servidor Langfuse **no se ha probado** en esta preparación; sí las llamadas al SDK,
sin red, y la jerarquía de observaciones con el SDK real.

## Límites conocidos

- Veinte preguntas son evidencia de laboratorio, no una prueba estadística.
- El criterio automático de acierto busca cadenas: la revisión manual decide los casos dudosos.
- El perfil doble no entiende sinónimos ni redacta. Sus cifras no se trasladan a un modelo.
- Una frase más larga que `chunk_size` no se corta: queda sola en su fragmento.
