# Comparación A/B · variable `chunk_size`

A = `320` (`test-A-real-20261122-002805`) · B = `900` (`test-B-real-20261122-003930`) · mismo conjunto `test` de 20 casos, mismos modelos y mismo evaluador.

| Métrica | A | B | B − A |
|---|---:|---:|---:|
| precision@5 | 0,24 | 0,23 | -0,01 |
| recall@5 | 1,00 | 0,96 | -0,04 |
| rechazos correctos (tasa) | 1,00 | 1,00 | 0,00 |
| abstenciones incorrectas (tasa) | 0,07 | 0,21 | +0,14 |
| aciertos por criterio (tasa) | 0,93 | 0,79 | -0,14 |
| faithfulness (media) | 0,92 | 0,98 | +0,05 |
| faithfulness (cobertura) | 1,00 | 1,00 | 0,00 |
| answer_relevancy (media) | 0,87 | 0,89 | +0,02 |
| answer_relevancy (cobertura) | 1,00 | 1,00 | 0,00 |
| latencia mediana (ms) | 2462,8 | 1748,6 | -714,2 |
| latencia p95 (ms) | 3771,6 | 2764,7 | -1006,9 |
| coste por consulta (USD) | 0,002045 | 0,002268 | +0,000200 |
| coste del sistema (USD) | 0,040881 | 0,045344 | +0,004500 |
| coste del evaluador (USD) | 0,459948 | 0,429915 | -0,030000 |

## Casos cuyo resultado cambia

| Caso | A | B |
|---|---|---|
| T08 | acierta | falla |
| T14 | acierta | falla |

Con 20 preguntas, una diferencia pequeña puede ser ruido: es evidencia de laboratorio, no una prueba estadística.
