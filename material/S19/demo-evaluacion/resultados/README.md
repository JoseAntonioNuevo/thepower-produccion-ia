# Resultados

Cada ejecución deja una carpeta con:

| Archivo | Quién lo escribe | Contenido |
|---|---|---|
| `respuestas.jsonl` | `s19.py lote` | Una línea por caso: respuesta, contextos, fuentes, documentos recuperados, latencia, tokens, coste, error |
| `manifiesto.json` | `s19.py lote` | Configuración, modelos, versiones, huella del conjunto, índice y número de llamadas |
| `puntuaciones.jsonl` | `evaluador/evaluar.py` | Una línea por caso y métrica: valor o motivo de no evaluable, identidad del evaluador y su consumo |
| `evaluador.json` | `evaluador/evaluar.py` | Resumen de cobertura por métrica |
| `informe.json` / `informe.md` | `s19.py informe` | Métricas con numerador, denominador y cobertura |
| `revision-manual.csv` | `s19.py revision` | Plantilla de revisión humana (columnas humanas vacías) |

Git ignora todo lo que generes aquí, salvo `ejemplo-doble/` y `ejemplo-real/`.

## `ejemplo-real/` · medición real del 22/11/2026

Perfil real por OpenRouter: Gemini 4 Hydrogen genera (razonamiento `low`), `openai/text-embedding-3-small`
indexa (768) y Claude Opus 5.5 juzga. Mismas carpetas que `ejemplo-doble/`, sin copias degradadas.
`test-A/revision-manual.csv` es la plantilla sin rellenar: la revisión humana está pendiente.
`primera-pasada-razonamiento-libre/` es la primera ejecución, con 3 respuestas vacías porque el
modelo agotó el máximo de tokens razonando; se conserva como ejemplo de fallo bien registrado.
`modelos/` es la evaluación de modelos: `test-MH` (Gemini 4 Hydrogen) y `test-MS` (GPT-6.2 Sol)
con el mismo índice, prompt, parámetros y juez (Claude Opus 5.5), y su `comparacion/`.
Las cifras están en el README de la demo («Perfil real con OpenRouter»). Los informes se
regeneraron el 22/11/2026 tras corregir el coste del sistema, que ahora incluye los rechazos del
modelo, y añadir el bloque «Producción» (p95, tasas, coste por consulta y peso del juez).

## `ejemplo-doble/` · resultados de EJEMPLO, no mediciones

Generados el 17/11/2026 con el **perfil doble** (embeddings por hash, generador extractivo y
juez léxico locales) contra PostgreSQL 17 + pgvector en Docker. Sirven para ver el formato
y para que la clase funcione sin claves. **No miden ningún modelo.**

| Carpeta | Qué es |
|---|---|
| `validacion-A`, `validacion-B` | Validación (8 casos) con `chunk_size` 320 y 900. De `validacion-A` salen los umbrales |
| `test-A`, `test-B` | Test (20 casos) de las dos configuraciones |
| `comparacion-A-B` | Tabla comparativa del test |
| `degradado-*` | Copias de `validacion-A` **estropeadas a propósito**: el control de regresión debe fallar |
| `test-A/revision-manual-EJEMPLO-rellena.csv` | Revisión de seis respuestas hecha por el agente de preparación, como ejemplo. No sustituye a la revisión humana de una ejecución real |

`degradado-incompleto` no tiene `informe.json`: el informe se niega a resumir un conjunto al que le faltan casos.
