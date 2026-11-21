# Proyecto final · Agente conversacional de soporte

**thePower · AI Engineer · S20 · miércoles 02/12/2026 (L/X) · 18:30–20:00**

Un agente que ayuda a un técnico de soporte de **AetherCloud** (una plataforma cloud
inventada para el curso). Junta en un solo proyecto pequeño lo que hemos visto por separado:

| Pieza del temario | Dónde está | Sesión de origen |
|---|---|---|
| Prompts y configuración del agente | `agente/config.py`, `agente/prompts.py` | S2, S5 |
| Construcción del grafo | `agente/grafo.py` | S5 (LangGraph) |
| Módulos y herramientas | `agente/herramientas.py`, `agente/cerebro.py` | S5 |
| Integración con PostgreSQL | `agente/almacen.py`, `esquema.sql`, `compose.yaml` | S9 |
| Integración con Langfuse | `agente/observabilidad.py` | S6 |
| Exposición vía FastAPI | `agente/api.py` | S16 |
| Integración con MCP | `servidor_mcp/tickets.py`, `agente/mcp_cliente.py` | S15 |
| Deep Research + RAG | `agente/investigacion.py`, `agente/rag.py` | S10–S12 |
| Despliegue en AWS | `Dockerfile`, `infra/plantilla.json` | S16–S17 |
| Integración de todos los componentes | `agente/servicios.py`, `agente/cli.py`, `tests/` | S18–S19 |

Son doce archivos de Python cortos y comentados. Cada uno empieza diciendo qué paso es.

## El caso

> «El ticket T-100 sigue abierto. Resume el problema, consulta la política aplicable y
> prepara una recomendación con fuentes. Si falta información pública, investígala.»

Para responder, el agente usa tres fuentes de verdad que **no se mezclan**:

1. **El sistema de tickets** — solo accesible a través de un servidor MCP propio.
2. **La documentación interna** — diez documentos ficticios, consultados con RAG.
3. **Información pública** — una lista blanca de fuentes, leída por una investigación acotada.

## Empezar en dos minutos (sin claves, sin Docker)

Necesitas [uv](https://docs.astral.sh/uv/). Desde esta carpeta:

```bash
uv sync                                  # instala exactamente las versiones de uv.lock
uv run pytest                            # 38 tests, sin red ni coste
uv run python -m agente.cli recorridos   # los recorridos de aceptación, de principio a fin
```

Para recorrerlo paso a paso, en el orden de la clase:

```bash
uv run python demo_clase.py              # 14 pasos; Enter para avanzar
```

Eso ejecuta el proyecto completo en el **perfil doble**: en vez de un modelo de lenguaje hay
unas reglas escritas a mano (`agente/cerebro.py`), y en vez de un modelo de embeddings, una
bolsa de palabras (`agente/rag.py`). Todo lo demás es real: el grafo, las llamadas MCP, la
recuperación, la API, la base de datos.

> **Lee esto antes de sacar conclusiones.** El perfil doble no mide ningún modelo. Sus
> respuestas llevan el rótulo `[perfil doble · reglas, sin modelo]`. Solo acierta cuando la
> pregunta comparte palabras con el documento y el umbral de evidencia (0,20) se ajustó con una
> lista corta de preguntas, con poco margen. Sirve para entender y probar el recorrido, no para
> evaluar calidad. Con un modelo real hay que volver a medir el umbral (eso es S19).

## Paso a paso

Cada paso añade una pieza. Puedes parar en cualquiera y el proyecto sigue funcionando.

### Paso 1 · Configuración — `agente/config.py`

Todo lo que cambia entre tu portátil y AWS llega por variables de entorno `S20_`. Dos
interruptores lo explican casi todo:

| Variable | Valores | Qué cambia |
|---|---|---|
| `S20_PERFIL` | `doble` (por defecto) · `real` | Reglas sin coste, o un modelo de un proveedor |
| `S20_ALMACEN` | `memoria` (por defecto) · `postgres` | RAM que se pierde, o PostgreSQL que persiste |
| `S20_FUENTES` | `locales` (por defecto) · `red` | Copias de aula, o descarga de la lista blanca |

Copia `.env.example` a `.env` si quieres fijar valores, y úsalo con `uv run --env-file .env …`.

### Paso 2 · Prompt y cerebro — `agente/prompts.py`, `agente/cerebro.py`

El prompt de sistema tiene versión (`v1`) y la versión viaja en cada respuesta. El «cerebro»
es quien decide el siguiente paso: un modelo real o el doble. Los dos se usan igual.

```bash
uv run python -m agente.cli chat "Hola, ¿qué puedes hacer?"
```

### Paso 3 · MCP — `servidor_mcp/tickets.py`, `agente/mcp_cliente.py`

El agente no abre `datos/tickets.json`: pregunta a un servidor MCP que expone una herramienta
(`consultar_ticket`) y un recurso (`tickets://abiertos`).

```bash
uv run python -m agente.cli mcp                                   # descubrir herramientas
uv run python -m agente.cli chat "¿Cómo está el ticket T-100?"    # ticket que existe
uv run python -m agente.cli chat "Consulta el ticket T-999"       # ticket que no existe
```

### Paso 4 · Herramientas y grafo — `agente/herramientas.py`, `agente/grafo.py`

Tres herramientas con contrato (argumentos validados, salida JSON con `ok`). El grafo tiene
tres nodos: `inicio` → `agente` ⇄ `herramientas`. El límite de llamadas por turno
(`S20_MAX_HERRAMIENTAS`) está en el código, no en el prompt.

```bash
S20_MAX_HERRAMIENTAS=1 uv run python -m agente.cli chat "Mira el ticket T-100 y consulta la política aplicable"
```

### Paso 5 · Memoria en PostgreSQL — `agente/almacen.py`, `esquema.sql`

```bash
docker compose up -d --wait              # PostgreSQL 17 + pgvector en 127.0.0.1:54520
export S20_ALMACEN=postgres
uv run python -m agente.cli ingestar     # crea tablas e índice (repetirlo no duplica)
uv run python -m agente.cli chat "¿Cómo está el ticket T-200?" --thread demo
uv run python -m agente.cli chat "¿Qué ticket estábamos viendo?" --thread demo   # otro proceso: se acuerda
uv run python -m agente.cli chat "¿Qué ticket estábamos viendo?" --thread demo --usuario luis   # no es suyo
```

`thread_id` identifica la conversación, **no autoriza**: quién puede leerla lo decide la tabla
`conversaciones`.

### Paso 6 · RAG — `agente/rag.py`

```bash
uv run python -m agente.cli chat "¿Cuál es el límite de peticiones del plan Estándar?"     # responde con cita
uv run python -m agente.cli chat "¿Cuál es la política de teletrabajo de los empleados?"   # no consta
```

### Paso 7 · Deep Research + RAG — `agente/investigacion.py`

Una investigación es un trabajo con estado. El agente la registra; un **ejecutor** aparte la
termina; consultar su estado no crea otro trabajo.

```bash
uv run python -m agente.cli chat "El ticket T-100 sigue abierto. Resume el problema, consulta la política aplicable y prepara una recomendación con fuentes. Si falta información pública, investígala." --thread caso
uv run python -m agente.cli investigar                  # el ejecutor procesa los pendientes
uv run python -m agente.cli investigar --ver INV-xxxxxxxx   # informe completo
S20_FUENTES=red uv run python -m agente.cli investigar  # lee las fuentes reales de la lista blanca
```

(Con `S20_ALMACEN=memoria` cada comando empieza de cero; para este paso usa PostgreSQL o
`recorridos`, que lo hace todo en un mismo proceso.)

### Paso 8 · Observabilidad — `agente/observabilidad.py`

Siempre: una línea JSON por turno con `request_id`, ruta, herramientas y duración.
Opcional: Langfuse, con `S20_LANGFUSE=1` y las claves `LANGFUSE_PUBLIC_KEY` y `LANGFUSE_SECRET_KEY`.

### Paso 9 · API — `agente/api.py`

```bash
uv run uvicorn agente.api:app --port 8020     # documentación interactiva en http://127.0.0.1:8020/docs
curl -s localhost:8020/health
curl -s -X POST localhost:8020/chat -H 'authorization: Bearer token-ana' \
  -H 'content-type: application/json' -d '{"thread_id":"api-1","mensaje":"¿Cómo está el ticket T-100?"}'
```

### Paso 10 · Contenedor y AWS — `Dockerfile`, `infra/plantilla.json`

```bash
docker build -t thepower-s20-agente:local .
docker run --rm -p 8020:8020 thepower-s20-agente:local
```

El despliegue en AWS (ECS Fargate + RDS PostgreSQL) está descrito en
[docs/despliegue-aws.md](docs/despliegue-aws.md). **No se ha desplegado**: crea recursos de pago.

## Perfil real (con un modelo)

```bash
export S20_PERFIL=real GOOGLE_API_KEY=…      # la clave nunca va en Git ni en la imagen
uv run python -m agente.cli ingestar          # calcula embeddings reales (cuesta dinero)
uv run python -m agente.cli chat "¿Cómo está el ticket T-100?"
```

Usa `google_genai:gemini-3.5-flash-lite` y `gemini-embedding-2` por defecto (los mismos que
S19); se cambian con `S20_MODELO_CHAT` y `S20_MODELO_EMBEDDINGS`. **Este perfil no se ha
ejecutado en la preparación del material**: ver [verificacion.md](../verificacion.md).

## Qué se ha comprobado y qué no

| Comprobado en local (16/11/2026) | Pendiente |
|---|---|
| 38 tests sin red + 5 de PostgreSQL | Ejecución con modelo real (perfil `real`) |
| Diez comprobaciones de aceptación, en memoria y en PostgreSQL | Traza real en Langfuse |
| Llamadas MCP reales por stdio | Despliegue en AWS |
| Investigación leyendo las fuentes reales (RFC 6585 y RFC 9110) | |
| API con `curl`, imagen Docker construida y arrancada | |

## Mapa de archivos

```text
agente/            el agente (un archivo por paso)
servidor_mcp/      servidor MCP propio de tickets
datos/             tickets ficticios, corpus AetherCloud y lista blanca de fuentes públicas
tests/             38 tests sin coste + 5 de PostgreSQL (-m db) + ensayo del modo clase (-m demo)
demo_clase.py      modo clase: el proyecto paso a paso, en el orden de las diapositivas
docs/              guion de clase, comandos, práctica, arquitectura y despliegue
infra/             plantilla CloudFormation (no desplegada)
evidencias/        resultado de los recorridos de aceptación
```

Todos los datos son ficticios. No hay datos personales ni secretos en el repositorio.
