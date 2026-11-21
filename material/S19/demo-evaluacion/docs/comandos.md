# S19 · Comandos en el orden de la presentación

Todos se ejecutan desde `demo-evaluacion/` con el perfil `doble` (sin claves, sin coste).
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

## Vivo 1 · Reconstruir desde cero (diapositiva 10)

```bash
uv run python s19.py preflight
head -n 1 datos/test.jsonl | python -m json.tool
uv run python s19.py ingestar --config A
uv run python s19.py preguntar "¿Qué versión de TLS exigen las pasarelas perimetrales?"
uv run python s19.py preguntar "¿Cuál es el horario de la cafetería de la oficina de Madrid?"
```

## Vivo 2 · Recuperación y rechazo (diapositiva 14)

```bash
uv run python s19.py calibrar --config A
uv run python s19.py lote --conjunto validacion --config A --salida resultados/mi-validacion-A
uv run python s19.py informe resultados/mi-validacion-A
```

Si ya existe calibración fijada para ese perfil en `datos/calibracion.json`, `calibrar` muestra
el umbral calculado junto al fijado sin sobrescribir el archivo (añade `--fijar` para
actualizarlo).

## Vivo 3 · Generación con el evaluador aislado (diapositiva 21)

```bash
(cd evaluador && uv run python evaluar.py ../resultados/mi-validacion-A)
head -n 2 resultados/mi-validacion-A/puntuaciones.jsonl | python -m json.tool --json-lines
uv run python s19.py informe resultados/mi-validacion-A
```

Revisión manual de ejemplo: `resultados/ejemplo-doble/test-A/revision-manual-EJEMPLO-rellena.csv`.

## Vivo 4 · Tests y control de regresión (diapositiva 26)

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

## Vivo 5 · Comparar A y B (diapositiva 27)

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

## Práctica (diapositiva 31)

```bash
uv run python s19.py estimar
```

## Otros

```bash
uv run pytest -m db              # integración con pgvector
uv run ruff check .
(cd evaluador && uv run pytest)  # tests del evaluador
docker compose down -v           # recoger
```

## Perfil real

**No ejecutado en esta preparación. Consume la API de Gemini: solo con el gasto autorizado.**
Previsión de `estimar`: 566 llamadas como máximo, 0,57 USD estimados, cota superior 4,66 USD.

En `.env`: `S19_PERFIL=real`, `GEMINI_API_KEY=…`. Después:

```bash
uv run python s19.py preflight
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

Tests reales, también de pago:

```bash
S19_EJECUTAR_REAL=1 uv run pytest -m llm
(cd evaluador && S19_EJECUTAR_REAL=1 uv run pytest -m llm)
```

Con Langfuse: añade `S19_LANGFUSE=on` y las claves `LANGFUSE_*` antes de los lotes, y al final
`uv run python s19.py publicar-evaluador resultados/real-test-A`.
