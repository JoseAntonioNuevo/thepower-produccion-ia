# S19 · Comandos en el orden de la presentación

Ejecuta los comandos desde la carpeta que contiene `s19.py`. Los bloques iniciales usan el perfil `doble` (sin claves, sin coste).
Sustituye `mi-` por el prefijo que quieras: `resultados/` está ignorado por Git.

## Preparación (antes de clase)

```bash
uv sync
(cd evaluador && uv sync)
cp .env.example .env
docker compose up -d --wait
uv run python s19.py preflight
uv run python s19.py ingestar --config A
uv run python s19.py ingestar --config B
```

## Vivo 1 · Reconstruir desde cero (diapositivas 4–5)

```bash
uv run python s19.py preflight
head -n 1 datos/test.jsonl | python -m json.tool
uv run python s19.py ingestar --config A
uv run python s19.py preguntar "¿Qué versión de TLS exigen las pasarelas perimetrales?"
uv run python s19.py preguntar "¿Cuál es el horario de la cafetería de la oficina de Madrid?"
uv run python s19.py chat          # el mismo grafo paso a paso en la TUI (1-7 guion, /ayuda, Esc sale)
```

## Vivo 2 · Recuperación y rechazo (anexo, diapositiva 16)

```bash
uv run python s19.py calibrar --config A
uv run python s19.py lote --conjunto validacion --config A --salida resultados/mi-validacion-A
uv run python s19.py informe resultados/mi-validacion-A
```

Si ya existe calibración fijada para ese perfil en `datos/calibracion.json`, `calibrar` muestra
el umbral calculado junto al fijado sin sobrescribir el archivo (añade `--fijar` para
actualizarlo).

## Vivo 3 · Generación con el evaluador aislado (diapositivas 11–12)

```bash
(cd evaluador && uv run python evaluar.py ../resultados/mi-validacion-A)
head -n 2 resultados/mi-validacion-A/puntuaciones.jsonl | python -m json.tool --json-lines
uv run python s19.py informe resultados/mi-validacion-A
```

Revisión manual de ejemplo: `resultados/ejemplo-doble/test-A/revision-manual-EJEMPLO-rellena.csv`.

## Vivo 4 · Tests y control de regresión (diapositivas 14 y 19)

```bash
uv run pytest
uv run python s19.py umbrales resultados/mi-validacion-A
uv run python s19.py regresion resultados/mi-validacion-A; echo "código de salida: $?"

uv run python s19.py degradar resultados/mi-validacion-A --modo recuperacion --salida resultados/mal-recuperacion
uv run python s19.py informe resultados/mal-recuperacion
uv run python s19.py regresion resultados/mal-recuperacion; echo "código de salida: $?"
```

Variantes: `--modo sin-rechazo`, `--modo juez-caido`, `--modo incompleto`. Como con `calibrar`,
si ya existe `datos/umbrales.<perfil>.json`, `umbrales` muestra las reglas nuevas junto a las
fijadas sin sobrescribir el archivo (usa `--fijar` para reemplazarlas).

## Vivo 5 · Comparar A y B (anexo, diapositiva 17)

```bash
for c in A B; do
  uv run python s19.py lote --conjunto test --config $c --salida resultados/mi-test-$c
  (cd evaluador && uv run python evaluar.py ../resultados/mi-test-$c)
  uv run python s19.py informe resultados/mi-test-$c > /dev/null
done
uv run python s19.py comparar resultados/mi-test-A resultados/mi-test-B
uv run python s19.py revision resultados/mi-test-A
```

En PowerShell, sustituye el bucle por los tres comandos escritos una vez con `A` y otra con `B`.

## Práctica (diapositiva 15)

```bash
uv run python s19.py estimar
```

## Otros

```bash
uv run pytest -m db              # integración con pgvector
uv run ruff check .
(cd evaluador && uv run pytest)  # tests del evaluador
docker compose stop              # conservar los índices para la próxima sesión
```

## Perfil real

**Ejecutado el 22/11/2026 (resultados en `resultados/ejemplo-real/`). Consume la API de OpenRouter: solo con el gasto autorizado.**
Una pasada completa costó 1,29 USD medidos (1,20 del juez Claude Opus 5.5).
Previsión de `estimar` con los modelos por defecto: 566 llamadas como máximo, 2,91 USD
estimados, cota superior 24,90 USD (casi todo, el juez Claude Opus 5.5).

En `.env`: `S19_PERFIL=real`, `OPENROUTER_API_KEY=…` y, si quieres, otros modelos
(`S19_GEN_MODEL`, `S19_EMBEDDING_MODEL`, `S19_EVAL_LLM_MODEL`…; ver `.env.example`). Después:

```bash
uv run python s19.py catalogo      # precios y parámetros de los modelos elegidos (gratis)
uv run python s19.py estimar
uv run python s19.py preflight     # clave, modelos y parámetros; no llama a ningún modelo
uv run python s19.py ingestar --config A --execute          # 41 embeddings
uv run python s19.py ingestar --config B --execute          # 13 embeddings
uv run python s19.py calibrar --config A --execute          # 8 embeddings (escribe la primera vez; usa --fijar para sobrescribir)
for c in A B; do
  uv run python s19.py lote --conjunto validacion --config $c --salida resultados/real-validacion-$c --execute
  (cd evaluador && uv run python evaluar.py ../resultados/real-validacion-$c --modo real --execute)
  uv run python s19.py informe resultados/real-validacion-$c
done
uv run python s19.py umbrales resultados/real-validacion-A   # → datos/umbrales.real.json (escribe si no existe; --fijar para sobrescribir)
uv run python s19.py regresion resultados/real-validacion-B
for c in A B; do
  uv run python s19.py lote --conjunto test --config $c --salida resultados/real-test-$c --execute
  (cd evaluador && uv run python evaluar.py ../resultados/real-test-$c --modo real --execute)
  uv run python s19.py informe resultados/real-test-$c
done
uv run python s19.py comparar resultados/real-test-A resultados/real-test-B --salida resultados/real-comparacion
uv run python s19.py revision resultados/real-test-A
```

Si cambias el modelo de embeddings, su dimensión o sus plantillas, vuelve a `ingestar` A y B y
a `calibrar --config A --execute --fijar`. Para comparar dos modelos de generación, añade a
`datos/configuraciones.json` dos variantes que solo cambien `gen_modelo` y usa el mismo índice.

### Evaluación de modelos (misma configuración, solo cambia el generador)

```bash
for m in MH MS; do
  uv run python s19.py lote --env .env.sol-opus --conjunto test --config $m --salida resultados/real-test-$m --execute
  (cd evaluador && uv run python evaluar.py ../resultados/real-test-$m --env ../.env.sol-opus --modo real --execute)
  uv run python s19.py informe resultados/real-test-$m
done
uv run python s19.py comparar resultados/real-test-MH resultados/real-test-MS --salida resultados/real-comparacion-modelos
```

Ejecutado el 22/11/2026: `resultados/ejemplo-real/modelos/` (unos 1,0 USD, casi todo el juez).

### Chat con modelos reales

```bash
uv run python s19.py chat --env .env.hydrogen-sol --execute
```

En el chat, escribe `3` para T12, espera la respuesta y ejecuta `/perfil terra-opus`.
Escribe `3` otra vez para consultar a GPT‑6.1 Terra en la misma sesión.
Usa `/perfil hydrogen-sol` para volver a Gemini 4 Hydrogen.

Tests reales, también de pago:

```bash
S19_EJECUTAR_REAL=1 uv run pytest -m llm
(cd evaluador && S19_EJECUTAR_REAL=1 uv run pytest -m llm)
```

Con Langfuse: añade `S19_LANGFUSE=on` y las claves `LANGFUSE_*` antes de los lotes, y al final
`uv run python s19.py publicar-evaluador resultados/real-test-A`.
