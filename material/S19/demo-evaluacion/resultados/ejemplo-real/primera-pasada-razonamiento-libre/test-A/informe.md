# Informe · test-A-real-20261122-001530

Conjunto `test` (20 casos, huella `18d20c777136`) · configuración `A` · perfil `real` · generación `google/gemini-4-hydrogen` · embeddings `openai/text-embedding-3-small`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 14 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 14 respondibles |
| Rechazo | rechazos correctos | 6/6 | sin respuesta |
| Rechazo | abstenciones incorrectas | 1/14 | respondibles |
| Corrección | aciertos por criterio | 13/14 | respondibles |
| Generación | faithfulness | 0,90 | 13/13 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,84 | 13/13 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 3314,8 ms | 20 consultas |
| Operación | coste del sistema | 0,070319 USD | medido en cada respuesta de OpenRouter (con BYOK, lo factura el proveedor) |
| Operación | errores del sistema | 0 | 20 casos |
| Producción | latencia p95 | 5322,8 ms | 20 consultas (máxima 5554,2 ms) |
| Producción | tasa de error | 0,00 | 0/20 consultas |
| Producción | tasa de rechazo | 0,35 | 3 sin llamar al modelo · 17 llamadas al modelo |
| Producción | coste por consulta | 0,003516 USD | generación + embeddings · 1.000 consultas ≈ 3,52 USD |
| Producción | peso del juez en el coste | 87 % | evaluar frente a responder |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| T12 | se abstuvo en una pregunta respondible |
