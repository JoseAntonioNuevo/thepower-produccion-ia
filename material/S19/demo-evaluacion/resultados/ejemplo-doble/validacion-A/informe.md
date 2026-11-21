# Informe · validacion-A

> **PERFIL DOBLE: embeddings por hash de palabras y generador extractivo locales. Estas cifras comprueban el funcionamiento del sistema de evaluación; NO miden ningún modelo.**

Conjunto `validacion` (8 casos, huella `38340dbddf01`) · configuración `A` · perfil `doble` · generación `doble-extractivo` · embeddings `doble-hash-768`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 5 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 5 respondibles |
| Rechazo | rechazos correctos | 2/3 | sin respuesta |
| Rechazo | abstenciones incorrectas | 0/5 | respondibles |
| Corrección | aciertos por criterio | 3/5 | respondibles |
| Generación | faithfulness | 1,00 | 6/6 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,41 | 6/6 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 9,8 ms | 8 consultas |
| Operación | coste del sistema | sin dato USD | estimación |
| Operación | errores del sistema | 0 | 8 casos |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| V03 | faltan datos clave: 25 % |
| V05 | faltan datos clave: AES-256-GCM |
| V06 | respondió una pregunta sin respuesta |
