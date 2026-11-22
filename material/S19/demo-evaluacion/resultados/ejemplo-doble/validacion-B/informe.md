# Informe · validacion-B

> **PERFIL DOBLE: embeddings por hash de palabras y generador extractivo locales. Estas cifras comprueban el funcionamiento del sistema de evaluación; NO miden ningún modelo.**

Conjunto `validacion` (8 casos, huella `38340dbddf01`) · configuración `B` · perfil `doble` · generación `doble-extractivo` · embeddings `doble-hash-768`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 5 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 5 respondibles |
| Rechazo | rechazos correctos | 3/3 | sin respuesta |
| Rechazo | abstenciones incorrectas | 2/5 | respondibles |
| Corrección | aciertos por criterio | 1/5 | respondibles |
| Generación | faithfulness | 1,00 | 3/3 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,42 | 3/3 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 9,9 ms | 8 consultas |
| Operación | coste del sistema | sin dato USD | estimación |
| Operación | errores del sistema | 0 | 8 casos |
| Producción | latencia p95 | 19,8 ms | 8 consultas (máxima 19,8 ms) |
| Producción | tasa de error | 0,00 | 0/8 consultas |
| Producción | tasa de rechazo | 0,62 | 5 sin llamar al modelo · 3 llamadas al modelo |
| Producción | coste por consulta | sin dato USD | generación + embeddings · 1.000 consultas ≈ sin dato USD |
| Producción | peso del juez en el coste | sin dato | evaluar frente a responder |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| V01 | se abstuvo en una pregunta respondible |
| V02 | se abstuvo en una pregunta respondible |
| V03 | faltan datos clave: 25 % |
| V05 | faltan datos clave: AES-256-GCM |
