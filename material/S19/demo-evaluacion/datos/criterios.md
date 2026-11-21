# Criterios de corrección de S19

Fijados el **16/11/2026**, antes de ejecutar el test. No se cambian después de ver resultados:
si un criterio resulta ser malo, se anota, se corrige con **validación** y se repite todo.

## Conjuntos

| Conjunto | Archivo | Casos | Para qué |
|---|---|---|---|
| Validación | `validacion.jsonl` | 8 (5 respondibles + 3 sin respuesta) | Elegir umbral de evidencia, prompt y umbrales de regresión |
| Test | `test.jsonl` | 20 (14 respondibles + 6 sin respuesta) | Medir una vez la configuración ya decidida |

Ninguna pregunta ni respuesta de referencia está en `corpus/`: lo comprueba `python s19.py preflight`.

## Qué cuenta como acierto (comprobación automática)

**Pregunta respondible.** Acierta si se cumplen las tres condiciones:

1. El sistema responde (no se abstiene).
2. La respuesta contiene **todos** los `datos_clave` del caso (sin distinguir tildes ni mayúsculas; `10` no vale por `100`).
3. La respuesta cita entre corchetes al menos un documento de `documentos_relevantes`.

**Pregunta sin respuesta.** Acierta si el sistema se abstiene («No consta…»). Cualquier otra respuesta es una *respuesta indebida*.

Una abstención en una pregunta respondible es una **abstención incorrecta** y se cuenta aparte.

## Recuperación

- Unidad: el **documento**. Varios fragmentos del mismo documento ocupan un solo puesto.
- `precision@5` = documentos relevantes entre los 5 recuperados / **5** (siempre 5).
- `recall@5` = documentos relevantes entre los 5 recuperados / **documentos relevantes de la pregunta**.
- Las preguntas sin respuesta no tienen recall: solo se mide su rechazo.

## Generación (Ragas)

- `faithfulness` y `answer_relevancy` solo se calculan sobre respuestas emitidas.
- No evaluable (con motivo, resta cobertura): `rechazo_sin_respuesta`, `error_sistema`, `respuesta_vacia`, `contexto_vacio`, `error_evaluador:<tipo>`, `nan`.
- Una media con cobertura inferior a la de validación menos el margen **no aprueba**.

## Revisión manual

Casos elegidos de antemano en `revision-casos.json` (seis). La persona que revisa lee pregunta,
respuesta y contexto, y rellena: ¿es correcta?, ¿las fuentes la respaldan?, ¿es fiel pero
incompleta?, ¿discrepa del juez? Si discrepa, manda la persona y se anota el caso.

## Control de regresión

Umbral = valor medido en **validación** ± margen de 0,10 (`python s19.py umbrales`). Un dato
ausente, un NaN, un caso que falta o un error del sistema hacen fallar el control.
