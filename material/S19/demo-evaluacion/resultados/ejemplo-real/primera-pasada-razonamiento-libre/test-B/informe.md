# Informe · test-B-real-20261122-001903

Conjunto `test` (20 casos, huella `18d20c777136`) · configuración `B` · perfil `real` · generación `google/gemini-4-hydrogen` · embeddings `openai/text-embedding-3-small`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,23 | 14 respondibles (techo 0,24) |
| Recuperación | recall@5 | 0,96 | 14 respondibles |
| Rechazo | rechazos correctos | 6/6 | sin respuesta |
| Rechazo | abstenciones incorrectas | 2/14 | respondibles |
| Corrección | aciertos por criterio | 11/14 | respondibles |
| Generación | faithfulness | 1,00 | 11/12 evaluables (cobertura 0,92) |
| Generación | answer_relevancy | 0,87 | 11/12 evaluables (cobertura 0,92) |
| Operación | latencia mediana | 2985,2 ms | 20 consultas |
| Operación | coste del sistema | 0,078726 USD | medido en cada respuesta de OpenRouter (con BYOK, lo factura el proveedor) |
| Operación | errores del sistema | 0 | 20 casos |
| Producción | latencia p95 | 7750,4 ms | 20 consultas (máxima 10458,6 ms) |
| Producción | tasa de error | 0,00 | 0/20 consultas |
| Producción | tasa de rechazo | 0,40 | 5 sin llamar al modelo · 15 llamadas al modelo |
| Producción | coste por consulta | 0,003937 USD | generación + embeddings · 1.000 consultas ≈ 3,94 USD |
| Producción | peso del juez en el coste | 85 % | evaluar frente a responder |

## No evaluables

| Caso | Métrica | Motivo |
|---|---|---|
| T12 | faithfulness | respuesta_vacia |
| T12 | answer_relevancy | respuesta_vacia |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| T08 | se abstuvo en una pregunta respondible |
| T12 | faltan datos clave: 24x7, 15 minutos |
| T14 | se abstuvo en una pregunta respondible |
