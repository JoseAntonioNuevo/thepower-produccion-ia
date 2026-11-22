# S19 · Guion del directo: el grafo en el chat, dos modelos y Langfuse

Material del profesor; no va en el ZIP de los alumnos. Usa **solo preguntas del conjunto de
test** (`demo-evaluacion/datos/test.jsonl`), las mismas de las pruebas reales del 22/11/2026, así
que cada resultado tiene una referencia medida con la que compararlo.

| Archivo de entorno | Genera | Juzga (Ragas, solo en lotes) |
|---|---|---|
| `.env.hydrogen-sol` | `google/gemini-4-hydrogen` (temperatura 0) | `openai/gpt-6.2-sol` |
| `.env.sol-opus` | `openai/gpt-6.2-sol` (sin temperatura: no la admite) | `anthropic/claude-opus-5.5` |

En los dos, los embeddings son `openai/text-embedding-3-small` (768), el prompt es `v1`, el umbral
de evidencia es 0,5223 y la configuración es A (fragmentos de 320). Como el índice y el umbral son
los mismos, **la recuperación es idéntica**: cualquier diferencia en las respuestas viene del
modelo de generación. Los dos archivos llevan `S19_PERFIL=real`; nada gasta sin `--execute`.

## Qué enseñar: cinco ideas (una por bloque del temario)

1. **Testing de agentes y pipelines: el camino importa.** La consulta es un grafo de LangGraph:
   `recuperar → generar → comprobar`, o bien `recuperar → rechazo_previo` sin llamar al modelo.
   El chat enseña qué rama toma cada pregunta y los tests comprueban esa trayectoria.
2. **Dos formas de rechazar.** Por umbral (rechazo previo: 0 tokens, 0 USD) o por el modelo
   («No consta» tras leer los fragmentos: se paga). «Plan Gratuito» se parece mucho a los
   documentos (0,77), así que lo frena el prompt y no el umbral.
3. **recall@5 no es lo que lee el modelo.** En T12 el documento correcto está entre los cinco
   recuperados (recall 1,00), pero los cuatro fragmentos que llegan al prompt son de otro.
4. **El criterio automático se equivoca en los dos sentidos y los modelos varían.** En T14 Sol
   escribe «800 ms» y el criterio exige «800 milisegundos» (falso fallo). En T12 Sol respondió en
   una pasada con «24x7» (acierto por casualidad: el dato sale de otro documento), en otra con
   «24×7» (fallo) y en otra dijo «No consta». Por eso hay revisión manual y **no se reajustan las
   reglas después de ver el test**.
5. **Evaluación de modelos con método.** Solo cambia el generador, mismo juez, mismo test:
   Hydrogen 13/14 y Sol 12/14 por criterio, pero Sol es más rápido (p95 1,9 s frente a 3,6 s) y
   cuesta la mitad por consulta (1,00 frente a 2,13 USD por 1.000). La decisión depende de qué se
   priorice, y 20 preguntas son evidencia de laboratorio, no una prueba estadística.

## Antes de clase (sin público)

```bash
cd material/S19/demo-evaluacion
open -a Docker                       # si no está abierto
docker compose up -d --wait
uv run python s19.py preflight --env .env.hydrogen-sol    # gratis: modelos ✓, umbral 0,5223, PostgreSQL
```

Si `preflight` dice «índice de esta configuración todavía vacío», el volumen se borró y hay que
reconstruirlo (menos de 0,001 USD):

```bash
uv run python s19.py ingestar --config A --env .env.hydrogen-sol --execute
uv run python s19.py ingestar --config B --env .env.hydrogen-sol --execute
```

**Langfuse (comprobarlo antes).** El envío a un servidor Langfuse **no se ha probado todavía**;
están probadas las llamadas al SDK sin red y la jerarquía de la traza con el SDK real. Crea un
proyecto en https://cloud.langfuse.com y añade a **los dos** archivos `.env.hydrogen-sol` y
`.env.sol-opus`:

```bash
S19_LANGFUSE=on
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com   # la URL de tu región o de tu servidor
```

Haz una pregunta en el chat (parte 1) y comprueba que aparece la traza. No uses LangSmith: el
código solo integra Langfuse, y es lo que pide el enunciado.

Mantén la pantalla lejos de los `.env`: contienen la clave de OpenRouter.

## Parte 1 · El chat con los dos modelos

```bash
uv run python s19.py chat --env .env.hydrogen-sol --execute
```

Necesita una terminal real con letra grande (no la salida de un IDE). A la izquierda, el chat;
a la derecha, el grafo con el nodo activo (◉), los recorridos (●) y los no recorridos (○), el
perfil, los modelos, el umbral y el coste de la sesión. Cada pregunta cuesta menos de 0,002 USD.

Escribe el número de la pregunta del guion. Para el otro modelo, sin salir:
`/perfil sol-opus`, y repite el número. Para volver: `/perfil hydrogen-sol`.
Con una pregunta del test, el chat añade al final la tarjeta **criterio** con el veredicto
automático, recall@5, precision@5 y la respuesta de referencia.

Las respuestas de abajo son las de las pruebas del 22/11. Un modelo puede redactar o incluso
decidir distinto en cada llamada, sobre todo Sol, que no admite temperatura. Si pasa, mejor:
es la idea 4.

### `1` · T01 · El caso fácil (calentamiento)

*¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?*

- **Referencia:** TLS 1.3, de `01-arquitectura-aethercloud`.
- **Esperado:** similitud 0,78 ≥ 0,5223 → `generar` → `comprobar`. Los dos responden «TLS 1.3»
  citando `[01-arquitectura-aethercloud]`. Criterio: ✓.
- **Qué señalar:** la ruta en el panel y la cita que exige el prompt.

### `2` · T13 · Una respuesta que combina dos documentos

*¿Qué datos personales se enmascaran antes de enviar trazas a observabilidad y cuántos días se retienen esas trazas?*

- **Referencia:** correos, IBAN y documentos de identidad; 14 días (`08-…` y `09-…`).
- **Esperado:** los dos aciertan y citan **cada dato con su documento**.

### `3` · T12 · Mismo contexto, decisión distinta (el caso estrella)

*Una organización del plan Empresa sufre un SEV-1: ¿qué soporte incluye su plan y cuál es el tiempo máximo de primera respuesta?*

- **Referencia:** soporte 24x7 para SEV-1 (`07-facturacion-y-planes`) y primera respuesta en 15
  minutos (`06-respuesta-a-incidentes`).
- **Esperado:**
  - **Hydrogen:** «No consta…» tras pasar por `generar`: rechazo del modelo. Criterio: ✗ abstención incorrecta.
  - **Sol:** en el test respondió «15 minutos … (24x7). Los fragmentos no especifican qué soporte
    incluye el plan Empresa.»; en otras llamadas, «24×7» o «No consta». El veredicto cambia.
- **Qué señalar:** los cuatro fragmentos que llegan al prompt son de `06-…`; `07-…` está entre los
  cinco recuperados (recall 1,00) pero no llega al modelo (`S19_K_CONTEXTO=4`). El «24x7» de Sol
  sale del documento de incidentes, no del plan: si el criterio le da acierto, es un falso acierto.

### `4` · T14 · Una respuesta bien dada que el criterio suspende

*¿Qué percentil de latencia dispara el rollback automático y a partir de qué latencia se conserva siempre una traza?*

- **Referencia:** p95 por encima de 800 milisegundos durante tres minutos; trazas de más de 1500 milisegundos.
- **Esperado:** Hydrogen escribe «800 milisegundos» (✓); Sol escribe «800 ms» (✗ «faltan datos clave»).
- **Qué señalar:** falso negativo del criterio, fijado el 16/11 antes del test. Se anota, se
  corrige con validación y se repite todo; no se cambia tras ver el test.

### `5` · T15 · Pregunta sin respuesta que el umbral no frena

*¿Cuál es el precio mensual del plan Gratuito de AetherCloud?*

- **Referencia:** no existe un plan Gratuito.
- **Esperado:** similitud 0,77 ≥ umbral → **se llama al modelo**; los dos dicen «No consta» (rechazo
  del modelo, con tokens y coste). Criterio: ✓ rechazo correcto.

### `6` · T17 · Rechazo previo: el modelo ni se llama

*¿En qué fecha se inauguró la región eu-par-1 de París?*

- **Referencia:** esa región no existe.
- **Esperado:** similitud 0,38 < 0,5223 → rama `rechazo_previo`: «no se llama al modelo · 0 tokens ·
  0 USD». **Igual con los dos modelos.** En el panel, `generar` y `comprobar` quedan sin recorrer.
- **Qué señalar:** comparado con T15, esto es lo que compra el umbral calibrado con validación.

### `7` · T08 con fragmentos de 900 (opcional)

*¿Qué plazo hay para pedir un crédito de servicio y qué hay que adjuntar a la solicitud?*

- Con A (`7`): acierta (similitud 0,62). Después `/config B` y `7` otra vez: la similitud baja a
  0,46 y se rechaza sin llamar al modelo, con cualquiera de los dos. Vuelve con `/config A`.
- **Qué señalar:** no falla el modelo, sino la fragmentación: por eso B pierde aciertos en el A/B.

## Parte 2 · Langfuse

Cada pregunta del chat es una traza `consulta-rag` en la **sesión** `chat-<fecha-hora>` (la que
aparece en el panel), etiquetada `s19`, `config:A` y `perfil:real`. El caso del test va en los
metadatos (`caso_test`) y el criterio como puntuaciones (`acierto_criterio`, `recall_at_5`,
`precision_at_5`, `rechazo`). La traza se envía al terminar cada pregunta.

Recorrido sugerido:

1. **T01:** dos observaciones, `recuperacion` (retriever: documentos y mejor similitud) y
   `generacion` (generation: modelo, parámetros, prompt completo, respuesta, tokens y coste). El
   coste lo calcula el programa y se envía tal cual: Langfuse no necesita conocer el precio.
2. **T17:** solo `recuperacion`; sin `generacion`, sin tokens y sin coste.
3. **T15:** sí hay `generacion`, y en su salida se lee «No consta».
4. **T12 de los dos modelos:** el mismo prompt de entrada y dos salidas distintas.
5. Filtra por la puntuación `acierto_criterio = 0` para ver los fallos de la sesión.

## Parte 3 · Evaluación de modelos (resultados ya medidos)

No hace falta ejecutarla en clase (tarda unos minutos y cuesta unos 1,0 USD por el juez). Está en
`demo-evaluacion/resultados/ejemplo-real/modelos/comparacion/comparacion.md`:

| Métrica (test, 20) | Hydrogen (MH) | Sol (MS) |
|---|---:|---:|
| Aciertos por criterio | 13/14 (falla T12) | 12/14 (T12 «24×7», T14 «ms») |
| Abstenciones incorrectas | 1/14 | 0/14 |
| faithfulness · answer_relevancy | 0,92 · 0,86 | 1,00 · 0,88 |
| Latencia p50 / p95 | 2,54 s / 3,65 s | 1,61 s / 1,88 s |
| Coste por 1.000 consultas | 2,13 USD | 1,00 USD |

Mismo índice, prompt v1, sin temperatura en ninguno, razonamiento bajo y **el mismo juez**
(Claude Opus 5.5, que no es ninguno de los candidatos). Por eso `comparar` la acepta: solo cambia
`gen_modelo`. Con tus dos archivos de clase no sería válida: cambian el juez y la temperatura.

Para repetirla en directo (comandos exactos en `docs/comandos.md`, «Evaluación de modelos»):
`lote --config MH` y `--config MS` con `--env .env.sol-opus --execute`, `evaluar.py … --env
../.env.sol-opus`, `informe` y `comparar`. Con Langfuse activo, cada lote es una sesión con 20
trazas; `publicar-evaluador` añade las puntuaciones de Ragas y el consumo del juez aparte.

## Al terminar

```bash
docker compose stop      # «down -v» borraría el índice
```

El `.env` activo sigue en perfil doble: los archivos de clase solo se usan con `--env`.
Coste previsto del directo: menos de 0,05 USD en el chat; unos 1,0 USD si se repite la parte 3.

## Anexo · Las 20 preguntas del test (configuración A, 22/11/2026)

La similitud es la misma con los dos modelos. «Rechazo previo» = por umbral, sin llamar al modelo.
La columna de Sol es la de la evaluación `MS`.

| Caso | Pregunta (resumida) | Similitud | Hydrogen | Sol |
|---|---|---:|---|---|
| T01 | Versión de TLS de las pasarelas | 0,78 | ✓ TLS 1.3 | ✓ |
| T02 | X-Aether-Tenant no coincide | 0,74 | ✓ 403 `TENANT_MISMATCH` | ✓ |
| T03 | Algoritmo y cabecera del token | 0,56 | ✓ EdDSA, `Authorization` | ✓ |
| T04 | Peticiones del plan Estándar | 0,68 | ✓ 120/min, 10 concurrentes | ✓ |
| T05 | Estado y cabecera al superar cuota | 0,61 | ✓ 429, `Retry-After` | ✓ |
| T06 | Enfriamiento antes de destruir CMK | 0,68 | ✓ 72 horas | ✓ |
| T07 | Copia diaria y prueba de restauración | 0,58 | ✓ 02:00 UTC, semanal | ✓ |
| T08 | Plazo del crédito de servicio | 0,62 | ✓ 15 días hábiles | ✓ |
| T09 | Mantenimiento fuera del SLA | 0,64 | ✓ 45 min, 7 días | ✓ |
| T10 | SEV-2: primera respuesta y avisos | 0,66 | ✓ 60 min, cada 2 h | ✓ |
| T11 | Mínimo facturable y día de factura | 0,61 | ✓ 60 s, día 2 | ✓ |
| T12 | Plan Empresa + SEV-1 | 0,75 | ✗ se abstiene | ✗ «24×7» (varía entre pasadas) |
| T13 | Datos enmascarados y retención | 0,67 | ✓ IBAN…, 14 días | ✓ |
| T14 | Percentil del rollback y trazas | 0,60 | ✓ | ✗ por criterio («ms») |
| T15 | Precio del plan Gratuito (no existe) | 0,77 | ✓ rechaza el modelo | ✓ rechaza el modelo |
| T16 | Primera respuesta de SEV-4 (no existe) | 0,75 | ✓ rechaza el modelo | ✓ rechaza el modelo |
| T17 | Región eu-par-1 (no existe) | 0,38 | ✓ rechazo previo | ✓ rechazo previo |
| T18 | Compresión de instantáneas (no consta) | 0,43 | ✓ rechazo previo | ✓ rechazo previo |
| T19 | Plantilla del centro de operaciones | 0,65 | ✓ rechaza el modelo | ✓ rechaza el modelo |
| T20 | Descuento por pago anual (no consta) | 0,50 | ✓ rechazo previo | ✓ rechazo previo |

Respuestas completas en `demo-evaluacion/resultados/ejemplo-real/modelos/test-MH/` y `test-MS/`.
El prompt del sistema es `v1`, en `rag/proveedores.py`.
