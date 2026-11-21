# Informe · test-A

> **PERFIL DOBLE: embeddings por hash de palabras y generador extractivo locales. Estas cifras comprueban el funcionamiento del sistema de evaluación; NO miden ningún modelo.**

Conjunto `test` (20 casos, huella `18d20c777136`) · configuración `A` · perfil `doble` · generación `doble-extractivo` · embeddings `doble-hash-768`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 14 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 14 respondibles |
| Rechazo | rechazos correctos | 2/6 | sin respuesta |
| Rechazo | abstenciones incorrectas | 4/14 | respondibles |
| Corrección | aciertos por criterio | 6/14 | respondibles |
| Generación | faithfulness | 1,00 | 14/14 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,44 | 14/14 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 9,4 ms | 20 consultas |
| Operación | coste del sistema | sin dato USD | estimación |
| Operación | errores del sistema | 0 | 20 casos |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| T03 | se abstuvo en una pregunta respondible |
| T05 | faltan datos clave: Retry-After |
| T06 | se abstuvo en una pregunta respondible |
| T07 | faltan datos clave: semana |
| T08 | se abstuvo en una pregunta respondible |
| T10 | faltan datos clave: 60 minutos, 2 horas |
| T12 | faltan datos clave: 15 minutos |
| T14 | se abstuvo en una pregunta respondible |
| T15 | respondió una pregunta sin respuesta |
| T16 | respondió una pregunta sin respuesta |
| T17 | respondió una pregunta sin respuesta |
| T19 | respondió una pregunta sin respuesta |
