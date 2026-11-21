# Informe · test-B

> **PERFIL DOBLE: embeddings por hash de palabras y generador extractivo locales. Estas cifras comprueban el funcionamiento del sistema de evaluación; NO miden ningún modelo.**

Conjunto `test` (20 casos, huella `18d20c777136`) · configuración `B` · perfil `doble` · generación `doble-extractivo` · embeddings `doble-hash-768`.

| Bloque | Métrica | Valor | Sobre |
|---|---|---:|---|
| Recuperación | precision@5 | 0,24 | 14 respondibles (techo 0,24) |
| Recuperación | recall@5 | 1,00 | 14 respondibles |
| Rechazo | rechazos correctos | 4/6 | sin respuesta |
| Rechazo | abstenciones incorrectas | 8/14 | respondibles |
| Corrección | aciertos por criterio | 3/14 | respondibles |
| Generación | faithfulness | 1,00 | 8/8 evaluables (cobertura 1,00) |
| Generación | answer_relevancy | 0,53 | 8/8 evaluables (cobertura 1,00) |
| Operación | latencia mediana | 9,8 ms | 20 consultas |
| Operación | coste del sistema | sin dato USD | estimación |
| Operación | errores del sistema | 0 | 20 casos |

## Casos fallados (se conservan todos)

| Caso | Qué pasó |
|---|---|
| T01 | se abstuvo en una pregunta respondible |
| T03 | se abstuvo en una pregunta respondible |
| T05 | se abstuvo en una pregunta respondible |
| T06 | se abstuvo en una pregunta respondible |
| T07 | faltan datos clave: semana |
| T08 | se abstuvo en una pregunta respondible |
| T09 | se abstuvo en una pregunta respondible |
| T10 | faltan datos clave: 60 minutos, 2 horas |
| T12 | faltan datos clave: 15 minutos |
| T13 | se abstuvo en una pregunta respondible |
| T14 | se abstuvo en una pregunta respondible |
| T16 | respondió una pregunta sin respuesta |
| T17 | respondió una pregunta sin respuesta |
