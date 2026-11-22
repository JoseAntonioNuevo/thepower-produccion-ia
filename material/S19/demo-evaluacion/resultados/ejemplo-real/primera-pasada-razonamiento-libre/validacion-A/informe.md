# Informe · validacion-A-real-20261122-001314

Conjunto `validacion` (8 casos, huella `38340dbddf01`) · configuración `A` · perfil `real` · generación `google/gemini-4-hydrogen` · embeddings `openai/text-embedding-3-small`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 5 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 5 respondibles |
| Rechazo | rechazos correctos | 2/3 | sin respuesta |
| Rechazo | abstenciones incorrectas | 0/5 | respondibles |
| Corrección | aciertos por criterio | 4/5 | respondibles |
| Generación | faithfulness | 1,00 | 4/6 evaluables (cobertura 0,67) |
| Generación | answer_relevancy | 0,92 | 4/6 evaluables (cobertura 0,67) |
| Operación | latencia mediana | 2450,0 ms | 8 consultas |
| Operación | coste del sistema | 0,043794 USD | medido en cada respuesta de OpenRouter (con BYOK, lo factura el proveedor) |
| Operación | errores del sistema | 0 | 8 casos |
| Producción | latencia p95 | 11622,6 ms | 8 consultas (máxima 11622,6 ms) |
| Producción | tasa de error | 0,00 | 0/8 consultas |
| Producción | tasa de rechazo | 0,25 | 2 sin llamar al modelo · 6 llamadas al modelo |
| Producción | coste por consulta | 0,005475 USD | generación + embeddings · 1.000 consultas ≈ 5,47 USD |
| Producción | peso del juez en el coste | 74 % | evaluar frente a responder |

## No evaluables

| Caso | Métrica | Motivo |
|---|---|---|
| V05 | faithfulness | respuesta_vacia |
| V06 | faithfulness | respuesta_vacia |
| V05 | answer_relevancy | respuesta_vacia |
| V06 | answer_relevancy | respuesta_vacia |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| V05 | faltan datos clave: 100 GiB, AES-256-GCM |
| V06 | respondió una pregunta sin respuesta |
