# Comparación A/B · variable `chunk_size`

A = `320` (`test-A-real-20261122-001530`) · B = `900` (`test-B-real-20261122-001903`) · mismo conjunto `test` de 20 casos, mismos modelos y mismo evaluador.

| Métrica | A | B | B − A |
|---|---:|---:|---:|
| precision@5 | 0,24 | 0,23 | -0,01 |
| recall@5 | 1,00 | 0,96 | -0,04 |
| rechazos correctos (tasa) | 1,00 | 1,00 | 0,00 |
| abstenciones incorrectas (tasa) | 0,07 | 0,14 | +0,07 |
| aciertos por criterio (tasa) | 0,93 | 0,79 | -0,14 |
| faithfulness (media) | 0,90 | 1,00 | +0,10 |
| faithfulness (cobertura) | 1,00 | 0,92 | -0,08 |
| answer_relevancy (media) | 0,84 | 0,87 | +0,04 |
| answer_relevancy (cobertura) | 1,00 | 0,92 | -0,08 |
| latencia mediana (ms) | 3314,8 | 2985,2 | -329,6 |
| latencia p95 (ms) | 5322,8 | 7750,4 | +2427,6 |
| coste por consulta (USD) | 0,003516 | 0,003937 | +0,000400 |
| coste del sistema (USD) | 0,070319 | 0,078726 | +0,008400 |
| coste del evaluador (USD) | 0,472349 | 0,433728 | -0,038600 |

## Casos cuyo resultado cambia

| Caso | A | B |
|---|---|---|
| T08 | acierta | falla |
| T14 | acierta | falla |

## No evaluables en B

- T12 · faithfulness · respuesta_vacia
- T12 · answer_relevancy · respuesta_vacia

Con 20 preguntas, una diferencia pequeña puede ser ruido: es evidencia de laboratorio, no una prueba estadística.
