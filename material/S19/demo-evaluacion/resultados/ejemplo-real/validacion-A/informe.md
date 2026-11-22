# Informe · validacion-A-real-20261122-002455

Conjunto `validacion` (8 casos, huella `38340dbddf01`) · configuración `A` · perfil `real` · generación `google/gemini-4-hydrogen` · embeddings `openai/text-embedding-3-small`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 5 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 5 respondibles |
| Rechazo | rechazos correctos | 3/3 | sin respuesta |
| Rechazo | abstenciones incorrectas | 0/5 | respondibles |
| Corrección | aciertos por criterio | 4/5 | respondibles |
| Generación | faithfulness | 1,00 | 5/5 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,90 | 5/5 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 2380,1 ms | 8 consultas |
| Operación | coste del sistema | 0,017972 USD | medido en cada respuesta de OpenRouter (con BYOK, lo factura el proveedor) |
| Operación | errores del sistema | 0 | 8 casos |
| Producción | latencia p95 | 6460,1 ms | 8 consultas (máxima 6460,1 ms) |
| Producción | tasa de error | 0,00 | 0/8 consultas |
| Producción | tasa de rechazo | 0,38 | 2 sin llamar al modelo · 6 llamadas al modelo |
| Producción | coste por consulta | 0,002247 USD | generación + embeddings · 1.000 consultas ≈ 2,25 USD |
| Producción | peso del juez en el coste | 91 % | evaluar frente a responder |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| V05 | faltan datos clave: 100 GiB |
