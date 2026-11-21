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

Git ignora todo lo que generes aquí, salvo `ejemplo-doble/`.

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
