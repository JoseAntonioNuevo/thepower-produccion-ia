# S19 · Guion del directo: el grafo en el chat, dos modelos y Langfuse

Material del profesor; no va en el ZIP de los alumnos. El chat usa preguntas del test.
La prueba de juez usa V02 de validación y la de regresión usa T09 del test.
En cada prueba pide al grupo una predicción y localiza con ellos la evidencia en el código,
el informe o Langfuse. La práctica completa se hace de forma opcional después del directo.

| Prueba | Qué cambia | Qué comprobamos en directo |
|---|---|---|
| 1 · Generador | Hydrogen → Terra | En T01 y T12, compara respuesta, cita o abstención, tokens y coste con los mismos fragmentos y prompt. |
| 2 · Juez | Sol → Opus | Comprueba que ambos jueces reciben exactamente el mismo V02. Contrasta notas y cobertura con la fuente, y compara el coste de juzgar. |
| 3 · Regresión | Juez Sol → Opus en T09 | La misma respuesta pasa de fidelidad 1,00 a 0,00. Compara las afirmaciones que extrajo cada juez y ejecuta la comprobación del caso. |

La parte 3 conserva la comparación histórica por lotes entre Hydrogen y Sol.

| Archivo de entorno | Genera | Juzga (Ragas, solo en lotes) |
|---|---|---|
| `.env.hydrogen-sol` | `google/gemini-4-hydrogen` (temperatura 0) | `openai/gpt-6.2-sol` |
| `.env.terra-opus` | `openai/gpt-6.1-terra` (sin temperatura: no la admite) | `anthropic/claude-opus-5.5` |

En los dos, los embeddings son `openai/text-embedding-3-small` (768), el prompt es `v1`, el umbral
de evidencia es 0,5223 y la configuración es A (fragmentos de 320). Como el índice y el umbral son
los mismos, **la recuperación es idéntica**: cualquier diferencia en las respuestas viene del
modelo de generación. Los dos archivos llevan `S19_PERFIL=real`; nada gasta sin `--execute`.

## Qué enseñar: cinco ideas (una por bloque del temario)

1. **Testing de agentes y pipelines: el camino importa.** La consulta es un grafo de LangGraph:
   `recuperar → generar → comprobar`, o bien `recuperar → rechazo_previo` sin llamar al modelo.
   El chat enseña qué rama toma cada pregunta y los tests comprueban esa trayectoria.
2. **Dos formas de rechazar.** Por umbral (0 tokens de generación tras calcular el embedding) o por el modelo
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

## Checklist de ensayo antes de clase

### Arrancar y hacer el preflight · sin coste

- [ ] Abre Terminal de macOS, entra en la demo y arranca Docker.

```bash
cd /Users/jose/Documents/the-power/4-produccion-ia/material/S19/demo-evaluacion
open -a Docker
```

- [ ] Cuando Docker Desktop esté listo, arranca PostgreSQL y comprueba los dos perfiles.

```bash
docker compose up -d --wait
uv run python s19.py preflight --env .env.hydrogen-sol
uv run python s19.py preflight --env .env.terra-opus
```

- [ ] En los dos preflights, busca «índice presente (41 fragmentos)», «Langfuse: activado» y
  «Preflight correcto». Si faltan dependencias, ejecuta estos comandos y repite los preflights.

```bash
uv sync --frozen
(cd evaluador && uv sync --frozen)
```

- [ ] Si el índice A está vacío, créalo una vez con este comando y repite los preflights.
  La ingesta consume OpenRouter. Para ensayar también la pregunta 7 con `/config B`,
  repite la ingesta con `--config B` si ese índice falta.

```bash
uv run python s19.py ingestar --config A --env .env.hydrogen-sol --execute
```

- [ ] Si Langfuse aparece apagado, comprueba en privado que ambos archivos de clase tengan
  `S19_LANGFUSE=on`, las dos claves `LANGFUSE_*` y el host `https://cloud.langfuse.com`.
  Mantén los `.env` fuera de la pantalla compartida.

### Prueba 1 · Cambiar el generador en el chat

- [ ] Inicia OpenTUI en Terminal. Ambos turnos usan `v1`, razonamiento bajo y el mismo
  máximo del perfil. Se deja la temperatura sin fijar en los dos. El chat consume OpenRouter.

```bash
S19_PROMPT_VERSION=v1 S19_GEN_TEMPERATURE='' \
  uv run python s19.py chat --env .env.hydrogen-sol --config A --execute
```

- [ ] Escribe `3` y pulsa Enter. Espera la respuesta de Gemini 4 Hydrogen.
- [ ] Escribe `/perfil terra-opus` y pulsa Enter. Comprueba que la cabecera muestra
  `openai/gpt-6.1-terra`.
- [ ] Escribe `3` de nuevo, espera la segunda respuesta y sal con Esc.
- [ ] En Brave, abre [Sessions de S19](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions)
  y busca la sesión nueva `chat-…`. Debe contener exactamente dos trazas `consulta-rag`.
- [ ] En **Metadata**, verifica `caso_test=T12` y `origen=chat` en ambas.
  En **generacion**, verifica el modelo, los tokens y el coste de cada turno.

| Turno | `perfil_env` | Modelo |
|---|---|---|
| `01-T12` | `.env.hydrogen-sol` | `google/gemini-4-hydrogen` |
| `02-T12` | `.env.terra-opus` | `openai/gpt-6.1-terra` |

Los dos turnos del [ensayo registrado](verificacion.md) costaron 0,00312 USD.

**En el directo.** Antes de responder T12, enseña la referencia (24x7 y 15 minutos).
Pide al grupo que localice los dos datos y la cita en cada salida. Abre `recuperacion`
y `generacion` para comprobar que los cuatro fragmentos del prompt son los mismos y
que el documento del plan figura entre los recuperados. Para T01, repite el recorrido
con `1` en otra sesión si quieres conservar las dos trazas de T12 juntas.

**Ensayo controlado adicional.** Se usó el mismo perfil base `.env.terra-opus`, índice A y
`v1`, cambiando solo `S19_GEN_MODEL`. Los IDs de fragmento y su orden coincidieron para cada
pregunta. Los costes son de generación.

| Caso | Hydrogen | Terra |
|---|---|---|
| T01 | TLS 1.3 con cita. 0,001551 USD | TLS 1.3 con cita. 0,000516 USD |
| T12 | Se abstuvo tras generar. 0,003327 USD | Se abstuvo tras generar. 0,001093 USD |

En otro turno real de T12, Terra sí dio los dos datos y citó el documento de incidentes.
Muestra ambas ejecuciones si sale un resultado distinto en clase. Cada coste corresponde a
su llamada y cada respuesta se revisa frente a los fragmentos que recibió.

### Prueba 2 · Cambiar el juez sobre una respuesta congelada

- [ ] Abre V02 del lote de validación. Pregunta cuánto admite un cuerpo `POST` y comprueba
  con el grupo que la respuesta, **4 MiB**, está respaldada por `03-limites-y-cuotas-api`.
- [ ] Compara las dos copias de la fila completa. Cambia solo el modelo de juez y conserva
  el evaluador, sus opciones y embeddings. Para proyectar el ensayo ya ejecutado, lee
  `puntuaciones.jsonl` en las carpetas `juez-sol` y `juez-opus`.

```bash
s19_ensayo=resultados/ensayo-tres-pruebas-20261122
cmp "$s19_ensayo/juez-sol/respuestas.jsonl" "$s19_ensayo/juez-opus/respuestas.jsonl"
cat "$s19_ensayo/juez-sol/puntuaciones.jsonl" "$s19_ensayo/juez-opus/puntuaciones.jsonl"
```

| Juez de V02 | Faithfulness | Answer Relevancy | Coste de evaluar |
|---|---:|---:|---:|
| GPT‑6.2 Sol | 1,0000 | 0,9566 | 0,01064334 USD |
| Claude Opus 5.5 | 1,0000 | 0,9585 | 0,02860928 USD |

**En el directo.** Pide al grupo que decida si la cita respalda la respuesta antes de enseñar
las notas. Ambos jueces coincidieron en fidelidad y puntuaron las dos métricas. La diferencia
de relevancia fue 0,0019 y el coste de Opus fue unas 2,7 veces el de Sol en este caso.
Abre el [lote verificado en Langfuse](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions/langfuse-prueba-hydrogen)
y muestra en V02 los **Scores** de la consulta y el modelo, tokens y coste del juez en
`evaluador-ragas → consumo-juez`. Las dos evaluaciones del ensayo se guardaron en carpetas
distintas para poder compararlas sobre el mismo material.

Para repetir el ensayo con una respuesta congelada, extrae V02 del JSONL y ejecútalo con cada
juez. Los dos comandos del evaluador consumen OpenRouter.

```bash
s19_ensayo="resultados/mi-juez-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$s19_ensayo/juez-sol" "$s19_ensayo/juez-opus"
python3 -c 'import json; from pathlib import Path; print(next(l for l in Path("resultados/ejemplo-real/validacion-A/respuestas.jsonl").read_text().splitlines() if json.loads(l)["caso_id"] == "V02"))' \
  > "$s19_ensayo/juez-sol/respuestas.jsonl"
cp "$s19_ensayo/juez-sol/respuestas.jsonl" "$s19_ensayo/juez-opus/respuestas.jsonl"

(cd evaluador && S19_EVAL_LLM_MODEL=openai/gpt-6.2-sol S19_EVAL_MAX_TOKENS=1024 \
  uv run python evaluar.py "../$s19_ensayo/juez-sol" --env ../.env.hydrogen-sol --modo real --execute)
(cd evaluador && S19_EVAL_LLM_MODEL=anthropic/claude-opus-5.5 S19_EVAL_MAX_TOKENS=1024 \
  uv run python evaluar.py "../$s19_ensayo/juez-opus" --env ../.env.hydrogen-sol --modo real --execute)
```

### Prueba 3 · Detectar una regresión al cambiar el juez

- [ ] Proyecta **T09**. Pregunta cuánto mantenimiento programado queda fuera del cálculo de
  disponibilidad y con cuánta antelación hay que avisar. La fuente exige las dos condiciones
  juntas: **hasta 45 minutos al mes y aviso de al menos 7 días naturales**.
- [ ] Muestra la respuesta guardada, que recoge ambas condiciones, y comprueba con `cmp` que
  Sol y Opus recibieron exactamente la misma pregunta, respuesta y fragmentos.
- [ ] Abre los veredictos de Ragas. Con Sol, las dos condiciones quedaron en una afirmación y
  el juez la dio por respaldada. Con Opus, la extracción creó dos afirmaciones, cada una
  presentaba una condición como suficiente y el verificador rechazó ambas.
- [ ] Ejecuta la comprobación de T09. Para este caso con ambas condiciones explícitas en la
  fuente, esperamos fidelidad 1,00. Muestra que la prueba pasa con Sol y falla con Opus.

```bash
s19_ensayo=resultados/ensayo-regresion-modelo-20261122
cmp "$s19_ensayo/juez-sol-T09/respuestas.jsonl" "$s19_ensayo/juez-opus-T09/respuestas.jsonl"
for s19_juez in sol opus; do
  python3 - "$s19_ensayo/juez-$s19_juez-T09/detalle-faithfulness.json" <<'PY'
import json
import sys
from pathlib import Path

detalle = json.loads(Path(sys.argv[1]).read_text())
assert detalle["caso"] == "T09"
nota = detalle["faithfulness"]
pasa = nota == 1.0
print(f'{detalle["modelo"]} · T09 · fidelidad {nota:.2f} · {"PASA" if pasa else "FALLA"}')
raise SystemExit(0 if pasa else 1)
PY
  echo "Código de salida: $?"
done
```

| Juez | Faithfulness | Answer Relevancy | Coste de evaluar |
|---|---:|---:|---:|
| GPT‑6.2 Sol | 1,0000 | 0,7491 | 0,01283984 USD |
| Claude Opus 5.5 | 0,0000 | 0,6911 | 0,05257002 USD |

**En el directo.** Pregunta «¿qué parte cambió si la respuesta y el contexto son idénticos?».
La regresión está en cómo se puntúa la respuesta. Ejecutamos Ragas con los dos jueces y
repetimos Faithfulness capturando las afirmaciones y los veredictos de cada modelo. La
segunda pasada reprodujo 1,00 con Sol y 0,00 con Opus.

Para comparar los generadores con los ocho casos de validación, abre el informe guardado
`resultados/ensayo-regresion-modelo-20261122/comparacion/comparacion.md`. Ambos acertaron
4/5 preguntas respondibles. En V06, el criterio de rechazo marcó como fallo una respuesta
de Terra que decía correctamente que AetherCloud opera en Madrid y Fráncfort. Úsalo como
ejemplo de revisión del criterio. T09 ofrece el caso del juez con una causa comprobada.

El [ensayo del prompt defectuoso](verificacion.md#ensayo-de-las-tres-pruebas-del-directo--22112026)
queda como prueba aparte del control de regresión sobre un lote completo.

### Pasar los tests y recoger · sin coste

- [ ] Con PostgreSQL arrancado, comprueba la demo, la integración y el evaluador.

```bash
uv run pytest
uv run pytest -m db
(cd evaluador && uv run pytest)
```

- [ ] Si quieres ensayar también regresión, degradación y la comparación A/B de fragmentación,
  sigue los bloques Vivo 4 y Vivo 5 del [recorrido con perfil doble](demo-evaluacion/docs/comandos.md).
- [ ] Cuando termines, detén PostgreSQL y conserva el índice.

```bash
docker compose stop
```

## Parte 1 · El chat con los dos modelos

```bash
S19_PROMPT_VERSION=v1 S19_GEN_TEMPERATURE='' \
  uv run python s19.py chat --env .env.hydrogen-sol --config A --execute
```

Necesita una terminal interactiva con letra grande. A la izquierda se ve el chat y a la derecha,
el grafo con el nodo activo (◉), los recorridos (●) y los no recorridos (○), el perfil, los
modelos, el umbral y el coste de la sesión.

Escribe el número de la pregunta del guion. Para repetirla con GPT‑6.1 Terra en la misma sesión,
ejecuta `/perfil terra-opus` y vuelve a introducir el número. Usa `/perfil hydrogen-sol` para volver.
Con una pregunta del test, el chat añade al final la tarjeta **criterio** con el veredicto
automático, recall@5, precision@5 y la respuesta de referencia.

Los casos de abajo sirven para comprobar el recorrido y el criterio en directo. Un modelo puede
redactar o decidir distinto en cada llamada. T12 es el caso ensayado con Hydrogen y Terra.

### `1` · T01 · El caso fácil (calentamiento)

*¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?*

- **Referencia:** TLS 1.3, de `01-arquitectura-aethercloud`.
- **Esperado:** similitud 0,78 ≥ 0,5223 → `generar` → `comprobar`. Busca «TLS 1.3»
  con la cita `[01-arquitectura-aethercloud]` y comprueba el criterio.
- **Qué señalar:** la ruta en el panel y la cita que exige el prompt.

### `2` · T13 · Una respuesta que combina dos documentos

*¿Qué datos personales se enmascaran antes de enviar trazas a observabilidad y cuántos días se retienen esas trazas?*

- **Referencia:** correos, IBAN y documentos de identidad; 14 días (`08-…` y `09-…`).
- **Qué comprobar:** que la respuesta cita **cada dato con su documento**.

### `3` · T12 · Mismo contexto con dos modelos (el caso estrella)

*Una organización del plan Empresa sufre un SEV-1: ¿qué soporte incluye su plan y cuál es el tiempo máximo de primera respuesta?*

- **Referencia:** soporte 24x7 para SEV-1 (`07-facturacion-y-planes`) y primera respuesta en 15
  minutos (`06-respuesta-a-incidentes`).
- **Ensayo del chat:** Terra respondió «24x7» y «15 minutos» y citó `06-respuesta-a-incidentes`.
  En la evaluación por lotes hubo una abstención de Hydrogen. En el directo, compara lo que
  devuelve cada turno con la referencia y con sus citas.
- **Qué señalar:** los cuatro fragmentos que llegan al prompt son de `06-…`; `07-…` está entre los
  cinco recuperados (recall 1,00) pero no llega al modelo (`S19_K_CONTEXTO=4`). Comprueba si la
  cita acredita las condiciones del plan Empresa o solo el procedimiento para SEV-1.

### `4` · T14 · Una respuesta bien dada que el criterio suspende

*¿Qué percentil de latencia dispara el rollback automático y a partir de qué latencia se conserva siempre una traza?*

- **Referencia:** p95 por encima de 800 milisegundos durante tres minutos; trazas de más de 1500 milisegundos.
- **Ejemplo de la comparación anterior:** Hydrogen escribió «800 milisegundos» (✓) y Sol escribió
  «800 ms» (✗ «faltan datos clave»). Comprueba cómo lo formulan Hydrogen y Terra en el chat.
- **Qué señalar:** falso negativo del criterio, fijado el 16/11 antes del test. Se anota, se
  corrige con validación y se repite todo; no se cambia tras ver el test.

### `5` · T15 · Pregunta sin respuesta que el umbral no frena

*¿Cuál es el precio mensual del plan Gratuito de AetherCloud?*

- **Referencia:** no existe un plan Gratuito.
- **Esperado:** similitud 0,77 ≥ umbral → **se llama al modelo**. Si responde «No consta», el
  criterio marca un rechazo correcto y la traza conserva los tokens y el coste.

### `6` · T17 · Rechazo previo: el modelo ni se llama

*¿En qué fecha se inauguró la región eu-par-1 de París?*

- **Referencia:** esa región no existe.
- **Esperado:** similitud 0,38 < 0,5223 → rama `rechazo_previo`. Se calcula el embedding de
  consulta y se consumen 0 tokens de generación. En el panel, `generar` y `comprobar` quedan sin recorrer.
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
2. **T17:** solo `recuperacion`. El embedding se calcula antes del umbral. El coste de generación es cero.
3. **T15:** sí hay `generacion`, y en su salida se lee «No consta».
4. **T12 de los dos modelos:** la misma sesión contiene una generación de Gemini 4 Hydrogen y
   otra de GPT‑6.1 Terra. Comprueba `caso_test=T12` y `perfil_env` en las dos trazas.
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
