# Informe · modelos-test-MS

Conjunto `test` (20 casos, huella `18d20c777136`) · configuración `MS` · perfil `real` · generación `openai/gpt-6.2-sol` · embeddings `openai/text-embedding-3-small`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 14 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 14 respondibles |
| Rechazo | rechazos correctos | 6/6 | sin respuesta |
| Rechazo | abstenciones incorrectas | 0/14 | respondibles |
| Corrección | aciertos por criterio | 12/14 | respondibles |
| Generación | faithfulness | 1,00 | 14/14 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,88 | 14/14 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 1607,1 ms | 20 consultas |
| Operación | coste del sistema | 0,020072 USD | medido en cada respuesta de OpenRouter (con BYOK, lo factura el proveedor) |
| Operación | errores del sistema | 0 | 20 casos |
| Producción | latencia p95 | 1875,8 ms | 20 consultas (máxima 3234,0 ms) |
| Producción | tasa de error | 0,00 | 0/20 consultas |
| Producción | tasa de rechazo | 0,30 | 3 sin llamar al modelo · 17 llamadas al modelo |
| Producción | coste por consulta | 0,001004 USD | generación + embeddings · 1.000 consultas ≈ 1,00 USD |
| Producción | peso del juez en el coste | 96 % | evaluar frente a responder |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| T12 | faltan datos clave: 24x7 |
| T14 | faltan datos clave: 800 milisegundos, 1500 milisegundos |
