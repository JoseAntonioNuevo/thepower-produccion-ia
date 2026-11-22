# Informe · validacion-B-real-20261122-002712

Conjunto `validacion` (8 casos, huella `38340dbddf01`) · configuración `B` · perfil `real` · generación `google/gemini-4-hydrogen` · embeddings `openai/text-embedding-3-small`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 5 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 5 respondibles |
| Rechazo | rechazos correctos | 3/3 | sin respuesta |
| Rechazo | abstenciones incorrectas | 1/5 | respondibles |
| Corrección | aciertos por criterio | 4/5 | respondibles |
| Generación | faithfulness | 1,00 | 4/4 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,93 | 4/4 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 2174,1 ms | 8 consultas |
| Operación | coste del sistema | 0,012814 USD | medido en cada respuesta de OpenRouter (con BYOK, lo factura el proveedor) |
| Operación | errores del sistema | 0 | 8 casos |
| Producción | latencia p95 | 3287,3 ms | 8 consultas (máxima 3287,3 ms) |
| Producción | tasa de error | 0,00 | 0/8 consultas |
| Producción | tasa de rechazo | 0,50 | 3 sin llamar al modelo · 5 llamadas al modelo |
| Producción | coste por consulta | 0,001602 USD | generación + embeddings · 1.000 consultas ≈ 1,60 USD |
| Producción | peso del juez en el coste | 91 % | evaluar frente a responder |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| V02 | se abstuvo en una pregunta respondible |
