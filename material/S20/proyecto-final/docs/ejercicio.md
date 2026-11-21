# Proyecto final paso a paso

Esta guía convierte el proyecto de referencia en **tu** proyecto final. Está pensada para
hacerse por pasos pequeños: cada paso tiene una tarea, un comando para comprobarla y una
señal clara de «hecho». No hace falta ninguna clave para los pasos 0–8.

> **Estado de este documento.** El temario de thePower pide la «entrega de este proyecto
> final» y el profesor indicó el 03/11 que el proyecto final es la entrega obligatoria del
> programa. La escuela no ha comunicado todavía formato, fecha límite ni rúbrica. Lo que
> sigue —entregables y criterios— es la **propuesta del profesor**; si la escuela publica
> otra cosa en la plataforma, manda la plataforma.

## Qué tienes que conseguir

Un agente conversacional sobre **un caso tuyo** (puedes conservar AetherCloud) que:

1. responde directamente cuando no necesita herramientas;
2. consulta un dato de negocio a través de un **servidor MCP** propio;
3. dice explícitamente cuándo ese dato no existe;
4. responde con **cita** usando documentación propia (RAG);
5. **rechaza** cuando no hay evidencia;
6. registra y completa una **investigación** con fuentes públicas, sin duplicarla;
7. **recuerda** la conversación tras reiniciar (PostgreSQL) y no la enseña a otro usuario;
8. se usa a través de una **API** y deja una traza por turno.

Son los mismos recorridos que ejecuta `uv run python -m agente.cli recorridos`.

## Paso 0 · Arrancar (15 min)

```bash
uv sync && uv run pytest && uv run python -m agente.cli recorridos
```

**Hecho cuando:** 38 tests en verde y `"todo_ok": true`.

## Paso 1 · Elige tu caso (30 min)

Escribe en tu README, en cinco líneas: quién usa el agente, qué pregunta, de dónde sale cada
dato (sistema de negocio, documentación, información pública) y qué **no** va a hacer.

**Hecho cuando:** alguien que no conoce tu proyecto entiende el caso leyendo esas cinco líneas.

## Paso 2 · Tus datos (45 min)

- `datos/tickets.json`: al menos tres registros ficticios de tu sistema de negocio.
- `datos/corpus/`: al menos cinco documentos ficticios con secciones `## `.
- Sin datos personales ni de clientes reales.

**Comprobar:** `uv run python -m agente.cli ingestar` → documentos y fragmentos esperados.

## Paso 3 · Tu servidor MCP (45 min)

En `servidor_mcp/tickets.py`, adapta la herramienta a tu dato de negocio: nombre, descripción,
patrón del identificador y respuesta `ok`/`error`.

**Comprobar:** `uv run python -m agente.cli mcp` muestra tu herramienta con su esquema, y
`uv run pytest tests/test_mcp.py` pasa tras ajustar los identificadores del test.

## Paso 4 · Prompt y reglas (30 min)

Edita `agente/prompts.py`: crea la versión `v2` con tu caso. No borres `v1`.
Si trabajas en el perfil doble, ajusta las palabras clave de `agente/cerebro.py`.

**Comprobar:** `S20_PROMPT_VERSION=v2 uv run python -m agente.cli chat "…"` devuelve `"prompt_version": "v2"`.

## Paso 5 · Memoria que sobrevive (30 min)

```bash
docker compose up -d --wait && export S20_ALMACEN=postgres
uv run python -m agente.cli ingestar
uv run python -m agente.cli chat "<pregunta sobre un registro>" --thread mio
uv run python -m agente.cli chat "¿Qué ticket estábamos viendo?" --thread mio
uv run python -m agente.cli chat "¿Qué ticket estábamos viendo?" --thread mio --usuario luis
```

**Hecho cuando:** el segundo comando recuerda y el tercero es rechazado. Guarda la salida.

## Paso 6 · Citar o rechazar (45 min)

Prepara **cinco preguntas con respuesta** en tu corpus y **tres sin respuesta**. Ejecuta las
ocho y anota para cada una: herramientas usadas, fuentes y si la respuesta es correcta.

**Hecho cuando:** las cinco citan el documento correcto y las tres dicen que no consta. Si
alguna falla, explica por qué (en el perfil doble suele ser por vocabulario distinto): esa
explicación forma parte de la entrega.

## Paso 7 · Investigación (45 min)

Añade a `datos/fuentes_publicas/catalogo.json` dos fuentes públicas de tu tema, con su copia
de aula. Lanza una investigación completa y otra que deba salir parcial.

**Hecho cuando:** tienes un informe `completo` y uno `parcial`, y repetir la petición no crea
un segundo trabajo (`investigar` devuelve `{"procesados": []}`).

## Paso 8 · API y traza (30 min)

Arranca la API, repite un recorrido con `curl` y localiza su línea JSON por `request_id`.

**Hecho cuando:** puedes decir, para una petición concreta, qué nodos recorrió y qué
herramientas usó, sin volver a ejecutarla.

## Paso 9 · Opcional: modelo real y despliegue

- **Modelo real:** `S20_PERFIL=real` con tu clave. Vuelve a medir el umbral de evidencia con
  tus ocho preguntas del paso 6 y anota tokens y coste si el proveedor los informa.
- **AWS:** sigue [despliegue-aws.md](despliegue-aws.md). Crea recursos de pago: fija un
  presupuesto, anota lo que creas y bórralo al terminar.
- **Langfuse:** activa `S20_LANGFUSE=1` y enseña la traza de un turno.

Estos tres puntos **no son necesarios** para entregar el proyecto.

## Qué se entrega

1. Enlace a tu repositorio (o un ZIP) con el código y un README que explique el caso y cómo
   ejecutarlo desde cero.
2. `evidencias/recorridos-….json` generado con `uv run python -m agente.cli recorridos --guardar`.
3. Tus ocho preguntas del paso 6 con su resultado.
4. Media página de límites: qué no hace tu agente, qué falló y qué mejorarías.

Sin claves, tokens ni datos personales en el repositorio.

## Propuesta de valoración (pendiente de confirmar con la escuela)

| Criterio | Peso |
|---|---:|
| Funcionamiento y recorrido completo | 25 % |
| RAG, fuentes y rechazo | 20 % |
| Memoria, aislamiento y límites | 15 % |
| Herramienta MCP e investigación integrada | 15 % |
| Observabilidad, evaluación y tests | 15 % |
| Reproducción, despliegue, coste y documentación | 10 % |

## Si te atascas

Escribe al profesor con: el comando que ejecutaste, la salida completa y qué esperabas. Con
eso se resuelve en un mensaje.
