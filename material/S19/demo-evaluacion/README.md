# S19 · RAG mínimo con evaluación y tests integrados

Proyecto de aula del programa **AI Engineer** de thePower. Construye un RAG pequeño desde
documentos en bruto y un índice vacío, mide **recuperación y generación por separado**,
compara dos configuraciones y demuestra que un control de regresión **falla cuando debe**.

Todo funciona **sin claves y sin coste** con el perfil `doble`. Ese perfil no usa ningún
modelo: comprueba que el sistema de evaluación funciona, **no mide la calidad de un modelo**.
Para medir de verdad se usa el perfil `real` (API de Gemini), que exige `--execute`.

```text
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
| `rag/` | Ingesta, almacén pgvector, proveedores (doble y Gemini), consulta, costes, Langfuse |
| `evaluacion/` | Métricas, lote, informe, comparación, regresión, degradación de prueba, contrato JSONL |
| `evaluador/` | **Entorno aislado** con `ragas==0.4.3` y `langchain-community==0.3.31` |
| `ampliacion/` | Opcional: bucle CRAG para practicar tests de decisiones de un agente |
| `tests/` | pytest con dobles; `db` y `llm` excluidos por defecto |
| `resultados/ejemplo-doble/` | Resultados de ejemplo del perfil doble (rotulados) |
| `s19.py` | Único punto de entrada |

## Antes de empezar

Necesitas **Python 3.12**, [uv](https://docs.astral.sh/uv/) y **Docker** en marcha. Los
comandos son los mismos en macOS, Linux y Windows (PowerShell o Git Bash).

```bash
cd demo-evaluacion
uv sync                      # entorno del RAG (psycopg, google-genai, langfuse, pytest, ruff)
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

## Paso 7 · Revisión manual

```bash
uv run python s19.py revision resultados/mi-test-A
```

Crea `revision-manual.csv` con los seis casos elegidos **antes** de ejecutar el test
(`datos/revision-casos.json`). Las columnas humanas van vacías: las rellena una persona.
Hay un ejemplo relleno en `resultados/ejemplo-doble/test-A/revision-manual-EJEMPLO-rellena.csv`.

## Paso 8 · Tests

```bash
uv run pytest                 # 73 tests con dobles; no usa red, Docker ni claves
uv run pytest -m db           # integración con pgvector (necesita el contenedor)
uv run ruff check .
(cd evaluador && uv run pytest)   # 15 tests del evaluador, también sin red
```

Los tests marcados `llm` llaman a modelos de pago y **no se ejecutan por defecto**.

## Paso 9 · Recoger

```bash
docker compose down -v
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

## Perfil real · pendiente de autorización de gasto

No se ha ejecutado. Requiere `GEMINI_API_KEY` en `.env`, `S19_PERFIL=real` y `--execute`.

```bash
uv run python s19.py estimar        # no llama a nada
```

| Partida | Llamadas (máx.) | Estimación | Cota superior |
|---|---:|---:|---:|
| Embeddings del RAG | 118 | 0,004 USD | 0,004 USD |
| Generación del RAG | 56 | 0,061 USD | 0,162 USD |
| Juez (Ragas) | 280 | 0,504 USD | 4,490 USD |
| Embeddings del juez | 112 | ≈ 0 | ≈ 0 |
| **Total** | **566** | **0,57 USD** | **4,66 USD** |

Tarifas de `tarifas.json` (Gemini Developer API, consultadas el 16/11/2026). La estimación
usa los tamaños supuestos de `datos/supuestos-coste.json`; la cota supone que cada respuesta
agota su máximo de tokens. Secuencia exacta en [docs/comandos.md](docs/comandos.md#perfil-real).

## Langfuse (opcional)

Con `S19_LANGFUSE=on` y las claves `LANGFUSE_*`, cada consulta deja una traza `consulta-rag`
con pregunta, respuesta, fuentes, documentos recuperados, latencia por paso, tokens y coste
de la generación, y las métricas como puntuaciones. El consumo del juez va en **otra traza**
(`evaluador-ragas`), que se publica con:

```bash
uv run python s19.py publicar-evaluador resultados/mi-test-A
```

Cuando los tokens y la tarifa en `tarifas.json` son conocidos, el cliente envía además el
coste calculado (`cost_details`: `input`, `output` y `total` en USD en la generación; `total`
en la traza del evaluador si todas las filas del caso tienen `coste_usd`) y la versión de
modelo servida por la API (`model_version`) en los metadatos de generación. Si falta algún
dato, no se envía coste (nunca `0`). Conviene definir igualmente el precio del modelo en
Project Settings → Models en Langfuse para los modelos cuyo coste se calcule en servidor. El
envío a un servidor Langfuse **no se ha probado** en esta preparación; sí las llamadas al SDK,
sin red.

## Límites conocidos

- Veinte preguntas son evidencia de laboratorio, no una prueba estadística.
- El criterio automático de acierto busca cadenas: la revisión manual decide los casos dudosos.
- El perfil doble no entiende sinónimos ni redacta. Sus cifras no se trasladan a un modelo.
- Una frase más larga que `chunk_size` no se corta: queda sola en su fragmento.
