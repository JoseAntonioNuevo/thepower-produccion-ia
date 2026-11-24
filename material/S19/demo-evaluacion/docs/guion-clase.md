# S19 · Guion de clase (90 minutos)

**Evaluación y testing de sistemas de IA** · AI Engineer · 18:30–20:00 Europe/Madrid.
Mismo guion para M/J (24/11/2026) y L/X (30/11/2026). La demo es autónoma y usa su
PostgreSQL local. El perfil `doble` permite recorrer gratis la ingesta y los tests.
El chat y los ensayos con modelos reales tienen comandos y resultados guardados.

Aplica la indicación de Laura de explicar teoría mientras se hace algo visible. La pregunta
que conduce la clase es «¿Cómo comprobamos qué ha cambiado y si empeoró el sistema?». Tras un
repaso breve del sistema (diapositivas 3–6) hay tres pruebas reales, cada una con una
diapositiva de pregunta y otra de resultado. Pide una predicción al grupo antes de cada
resultado y contrástala con la salida. Las pruebas son cambiar el generador, cambiar el juez
sobre una respuesta congelada y detectar una regresión del evaluador al sustituir su modelo.
Los comandos y las cifras del ensayo están en el [guion del directo](../../guion-directo-modelos.md).

## Antes de conectar (18:15)

Arranca el contenedor y comprueba el índice A. Deja preparados el chat, las dos puntuaciones
guardadas de V02, los veredictos de T09 y la vista Sessions de Langfuse.
Sigue la [checklist de ensayo](../../guion-directo-modelos.md#checklist-de-ensayo-antes-de-clase).
La diapositiva 20 (anexo) resume los comandos de las tres pruebas.

## Horario

| Hora | Min | Bloque | Diapositivas | En diapositiva | En vivo |
|---|---:|---|---|---|---|
| 18:30 | 3 | Apertura | 1–2 | Pregunta del día, objetivos del temario, QR de la sesión anterior y recorrido | — |
| 18:33 | 4 | Sistema · herramientas | 3 | OpenTUI, LangGraph, PostgreSQL + pgvector, OpenRouter, Ragas y Langfuse; color por etapa | Árbol de `demo-evaluacion/` |
| 18:37 | 5 | Sistema · RAG | 4 | Documento Markdown → 5 fragmentos → fila de `fragmentos`; `test.jsonl` y `validacion.jsonl` fuera del índice | `preflight` (opcional) |
| 18:42 | 5 | Sistema · grafo | 5 | Grafo real con sus dos ramas (el rechazo previo no genera, pero ya calculó el embedding); embudo 12 → 5 → 4 con T01 | Chat: `6` (T17, rechazo previo) |
| 18:47 | 5 | Sistema · Langfuse | 6 | Traza anotada de V02 y `consumo-juez` aparte | Sessions → `langfuse-prueba-hydrogen` |
| 18:52 | 8 | Prueba 1 · T01 | 7–8 | Pregunta y predicción; resultado: TLS 1.3 con la misma cita, coste distinto | Chat: `1`, `/perfil terra-opus`, `1` |
| 19:00 | 16 | Prueba 1 · T12 | 9–10 | Dos fuentes; resultado: recall@5 = 1,00 y el plan fuera del prompt | Chat: `/perfil hydrogen-sol`, `3`, `/perfil terra-opus`, `3` y Langfuse |
| 19:16 | 16 | Prueba 2 · V02 | 11–12 | Respuesta congelada; Faithfulness y Answer Relevancy; notas y coste de Sol y Opus | `cmp` y `cat` de las puntuaciones |
| 19:32 | 18 | Prueba 3 · T09 | 13–14 | ¿Está respaldada?; Sol PASA (0) y Opus FALLA (1); control por caso frente a umbral del lote | `cmp`, comprobación de T09 y `pytest` |
| 19:50 | 10 | Cierre | 15 | Evidencia para aprobar un cambio, práctica opcional y preguntas | `estimar` (opcional) |
| — | — | Anexo | 16–20 | Métricas, A/B de fragmentación, histórico Hydrogen–Sol, prompt NO_CONSTA y comandos | Solo si surge la pregunta |

Si vas con retraso, usa las respuestas y puntuaciones ya guardadas en lugar del chat, abre una
sola sesión en Langfuse y acorta la diapositiva 12. Reserva tiempo para la diapositiva 14 y para
mostrar los códigos 0 y 1 de la tercera prueba.

## Apertura · 18:30–18:33

- **Diapositiva 1.** Pregunta del día y objetivo del temario; las cuatro partes del temario
  con el lugar donde aparecen en las pruebas.
- **Diapositiva 2.** QR: evalúa la sesión anterior de cada grupo (S18 del 19/11 para M/J;
  S18 del 25/11 para L/X). Dos minutos con el QR en pantalla. Recorrido en una línea y método
  de cada prueba: predecís, ejecutamos, contrastamos. La línea solo pregunta si los jueces
  coinciden en T09; el fallo se revela en la diapositiva 14.

## Repaso del sistema · 18:33–18:52

- **Diapositiva 3 · Qué vamos a usar.** Seis piezas en el orden en que las recorre una pregunta
  y su función en la demo; Python, Docker y pytest como base. Presenta la leyenda de colores.
- **Diapositiva 4 · Qué es un RAG y qué guarda el nuestro.** `01-arquitectura-aethercloud.md` se
  convierte en 5 fragmentos (41 en el índice A) y el fragmento `#03` en una fila con documento,
  texto, huella y vector. Las preguntas y referencias quedan fuera del índice.
- **Diapositiva 5 · Cómo funciona una pregunta.** `recuperar` → umbral 0,5223 → `generar` y
  `comprobar`, o `rechazo_previo` sin generador (0 tokens de generación; el embedding de la
  pregunta ya se calculó y puede tener coste). Embudo real de T01: 12 fragmentos, 5 documentos
  distintos y 4 fragmentos al prompt. En el chat, `6` (T17) recorre el rechazo previo.
- **Diapositiva 6 · Langfuse.** Recreación rotulada de la traza `consulta-rag` de V02 con tres
  lecturas: qué recuperó, qué respondió y cuánto costó. `Metadata`, `Scores` y `consumo-juez`
  se enseñan en Brave. El coste lo devuelve OpenRouter y la demo lo envía.

Pregunta de comprobación: *¿por qué las preguntas del test no pueden estar en el corpus?*

## Prueba 1 · Cambiar el generador · 18:52–19:16

1. **Diapositiva 7.** Lee T01 y pide la predicción: dato, cita y qué modelo costará más. Ejecuta
   el chat con `1`, `/perfil terra-opus` y `1`.
2. **Diapositiva 8.** Ambos dieron TLS 1.3 y citaron `01-arquitectura-aethercloud`. Coste de
   generación en el ensayo: 0,001551 USD con Hydrogen y 0,000516 USD con Terra (dos llamadas).
3. **Diapositiva 9.** Lee T12 y la referencia (24x7 y 15 minutos, dos documentos). Pide qué
   fuente acredita cada parte. Tras T01 el chat quedó en Terra: en la misma sesión empieza con
   `/perfil hydrogen-sol` y comprueba la cabecera; después `3`, `/perfil terra-opus` y `3`. Si
   abres otro chat, copia el comando completo de la diapositiva 7 (temperatura sin fijar en ambos).
   Abre la sesión en Langfuse.
4. **Diapositiva 10.** El documento del plan está entre los 5 recuperados, pero los 4 fragmentos
   del prompt son de incidentes. Explica recall@5 aquí. En el ensayo controlado ambos se
   abstuvieron; en otro turno del chat Terra dio los dos datos y citó incidentes. Preséntalos
   como ejecuciones distintas.

Pregunta: *¿cómo afecta a la respuesta que un documento recuperado quede fuera del prompt?*

## Prueba 2 · Cambiar el juez · 19:16–19:32

1. **Diapositiva 11.** Enseña la fila congelada de V02 y la frase que acredita «4 MiB». Explica
   en una frase Faithfulness y Answer Relevancy. Ejecuta `cmp` sobre las dos copias y pide la
   predicción de la nota de fidelidad.
2. **Diapositiva 12.** Fidelidad 1,0000 con los dos; relevancia 0,9566 y 0,9585; coste de juzgar
   0,01064334 y 0,02860928 USD. El coste de generar (0,0015375 USD) va aparte.

Pregunta: *el juez falla en 3 de 14 respuestas y la media sale 0,95. ¿Qué número falta?* (Cobertura.)

## Prueba 3 · Detectar una regresión · 19:32–19:50

1. **Diapositiva 13.** Proyecta T09, el fragmento y la respuesta guardada. Pide que decidan si
   está respaldada antes de enseñar las notas: si el contexto respalda todas las afirmaciones,
   esperamos fidelidad 1,00 (fidelidad mide respaldo, no corrección). Opcional: `uv run pytest` y las comprobaciones
   de trayectoria de `tests/test_grafo.py` y `tests/test_enrutado.py`.
2. **Diapositiva 14.** Sol mantuvo las dos condiciones en una afirmación: 1,00, **PASA (0)**.
   Opus las separó y rechazó ambas: 0,00, **FALLA (1)**. Ejecuta la comprobación de T09 del
   guion del directo. Distingue ese control por caso del umbral agregado: el test A con juez
   Opus tiene fidelidad media 0,92 y `s19.py regresion` pasa con este 0 dentro.

Pregunta: *¿qué parte del evaluador falló si dos modelos recibieron la misma respuesta?*

## Cierre y práctica · 19:50–20:00

- **Diapositiva 15.** Evidencia antes de aprobar un cambio: misma entrada, una variable cambiada,
  resultado comprobable y coste visible. Práctica **opcional** (7–9 h) con guía en
  [ejercicio.md](ejercicio.md); `estimar` antes de gastar (566 llamadas como máximo). Preguntas.
  Siguiente sesión: S20, proyecto final.
- **Diapositivas 16–20 (anexo).** Consulta: tabla de métricas, comparación controlada 320 → 900,
  comparación histórica Hydrogen–Sol, prompt que responde siempre NO_CONSTA como respaldo de
  laboratorio y comandos de las tres pruebas.
