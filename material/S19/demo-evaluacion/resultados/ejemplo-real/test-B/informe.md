# Informe · test-B-real-20261122-003930

Conjunto `test` (20 casos, huella `18d20c777136`) · configuración `B` · perfil `real` · generación `google/gemini-4-hydrogen` · embeddings `openai/text-embedding-3-small`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,23 | 14 respondibles (techo 0,24) |
| Recuperación | recall@5 | 0,96 | 14 respondibles |
| Rechazo | rechazos correctos | 6/6 | sin respuesta |
| Rechazo | abstenciones incorrectas | 3/14 | respondibles |
| Corrección | aciertos por criterio | 11/14 | respondibles |
| Generación | faithfulness | 0,98 | 11/11 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,89 | 11/11 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 1748,6 ms | 20 consultas |
| Operación | coste del sistema | 0,045344 USD | medido en cada respuesta de OpenRouter (con BYOK, lo factura el proveedor) |
| Operación | errores del sistema | 0 | 20 casos |
| Producción | latencia p95 | 2764,7 ms | 20 consultas (máxima 2837,2 ms) |
| Producción | tasa de error | 0,00 | 0/20 consultas |
| Producción | tasa de rechazo | 0,45 | 5 sin llamar al modelo · 15 llamadas al modelo |
| Producción | coste por consulta | 0,002268 USD | generación + embeddings · 1.000 consultas ≈ 2,27 USD |
| Producción | peso del juez en el coste | 90 % | evaluar frente a responder |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| T08 | se abstuvo en una pregunta respondible |
| T12 | se abstuvo en una pregunta respondible |
| T14 | se abstuvo en una pregunta respondible |
