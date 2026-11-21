# Comparación A/B · variable `chunk_size`

> **PERFIL DOBLE: embeddings por hash de palabras y generador extractivo locales. Estas cifras comprueban el funcionamiento del sistema de evaluación; NO miden ningún modelo.**

A = `320` (`test-A`) · B = `900` (`test-B`) · mismo conjunto `test` de 20 casos, mismos modelos y mismo evaluador.

| Métrica | A | B | B − A |
|---|---:|---:|---:|
| precision@5 | 0,24 | 0,24 | 0,00 |
| recall@5 | 1,00 | 1,00 | 0,00 |
| rechazos correctos (tasa) | 0,33 | 0,67 | +0,33 |
| abstenciones incorrectas (tasa) | 0,29 | 0,57 | +0,29 |
| aciertos por criterio (tasa) | 0,43 | 0,21 | -0,21 |
| faithfulness (media) | 1,00 | 1,00 | 0,00 |
| faithfulness (cobertura) | 1,00 | 1,00 | 0,00 |
| answer_relevancy (media) | 0,44 | 0,53 | +0,08 |
| answer_relevancy (cobertura) | 1,00 | 1,00 | 0,00 |
| latencia mediana (ms) | 9,4 | 9,8 | +0,4 |
| coste del sistema (USD, estimado) | sin dato | sin dato | sin dato |
| coste del evaluador (USD, estimado) | sin dato | sin dato | sin dato |

## Casos cuyo resultado cambia

| Caso | A | B |
|---|---|---|
| T01 | acierta | falla |
| T09 | acierta | falla |
| T13 | acierta | falla |
| T15 | falla | acierta |
| T19 | falla | acierta |

Con 20 preguntas, una diferencia pequeña puede ser ruido: es evidencia de laboratorio, no una prueba estadística.
