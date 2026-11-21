# Informe · validacion-A-DEGRADADO-juez-caido

> **RESULTADO DEGRADADO A PROPÓSITO (juez-caido) para probar el control de regresión. No es una medición. PERFIL DOBLE: embeddings por hash de palabras y generador extractivo locales. Estas cifras comprueban el funcionamiento del sistema de evaluación; NO miden ningún modelo.**

Conjunto `validacion` (8 casos, huella `38340dbddf01`) · configuración `A` · perfil `doble` · generación `doble-extractivo` · embeddings `doble-hash-768`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 5 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 5 respondibles |
| Rechazo | rechazos correctos | 2/3 | sin respuesta |
| Rechazo | abstenciones incorrectas | 0/5 | respondibles |
| Corrección | aciertos por criterio | 3/5 | respondibles |
| Generación | faithfulness | 1,00 | 3/6 evaluables (cobertura 0,50) |
| Generación | answer_relevancy | 0,42 | 3/6 evaluables (cobertura 0,50) |
| Operación | latencia mediana | 9,8 ms | 8 consultas |
| Operación | coste del sistema | sin dato USD | estimación |
| Operación | errores del sistema | 0 | 8 casos |

## No evaluables

| Caso | Métrica | Motivo |
|---|---|---|
| V01 | faithfulness | error_evaluador:TimeoutError |
| V03 | faithfulness | error_evaluador:TimeoutError |
| V05 | faithfulness | error_evaluador:TimeoutError |
| V01 | answer_relevancy | error_evaluador:TimeoutError |
| V03 | answer_relevancy | error_evaluador:TimeoutError |
| V05 | answer_relevancy | error_evaluador:TimeoutError |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| V03 | faltan datos clave: 25 % |
| V05 | faltan datos clave: AES-256-GCM |
| V06 | respondió una pregunta sin respuesta |
