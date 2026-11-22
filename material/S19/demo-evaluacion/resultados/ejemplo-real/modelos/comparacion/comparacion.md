# Comparación A/B · variable `gen_modelo`

A = `google/gemini-4-hydrogen` (`modelos-test-MH`) · B = `openai/gpt-6.2-sol` (`modelos-test-MS`) · mismo conjunto `test` de 20 casos, mismos modelos y mismo evaluador.

| Métrica | A | B | B − A |
|---|---:|---:|---:|
| precision@5 | 0,24 | 0,24 | 0,00 |
| recall@5 | 1,00 | 1,00 | 0,00 |
| rechazos correctos (tasa) | 1,00 | 1,00 | 0,00 |
| abstenciones incorrectas (tasa) | 0,07 | 0,00 | -0,07 |
| aciertos por criterio (tasa) | 0,93 | 0,86 | -0,07 |
| faithfulness (media) | 0,92 | 1,00 | +0,08 |
| faithfulness (cobertura) | 1,00 | 1,00 | 0,00 |
| answer_relevancy (media) | 0,86 | 0,88 | +0,02 |
| answer_relevancy (cobertura) | 1,00 | 1,00 | 0,00 |
| latencia mediana (ms) | 2540,4 | 1607,1 | -933,3 |
| latencia p95 (ms) | 3645,7 | 1875,8 | -1769,9 |
| coste por consulta (USD) | 0,002132 | 0,001004 | -0,001100 |
| coste del sistema (USD) | 0,042636 | 0,020072 | -0,022600 |
| coste del evaluador (USD) | 0,457113 | 0,496587 | +0,039500 |

## Casos cuyo resultado cambia

| Caso | A | B |
|---|---|---|
| T14 | acierta | falla |

Con 20 preguntas, una diferencia pequeña puede ser ruido: es evidencia de laboratorio, no una prueba estadística.
