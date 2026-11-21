# Comandos de la clase, en el orden de la presentación

> **Forma cómoda:** `uv run python demo_clase.py` ejecuta todo lo de esta página en el mismo
> orden, paso a paso (Enter para avanzar). Esta página es la versión manual, la que pueden
> teclear los alumnos.

Todos se ejecutan desde `proyecto-final/`. Terminal A para los comandos; terminal B para la API.

## Antes de empezar (una vez)

```bash
uv sync
docker compose up -d --wait
export S20_ALMACEN=postgres
uv run python -m agente.cli ingestar
```

## Diapositiva 6 · El proyecto entero, en verde

```bash
uv run pytest
S20_ALMACEN=memoria uv run python -m agente.cli recorridos
```

## Diapositivas 8–9 · Grafo y herramientas

```bash
uv run python -m agente.cli chat "Hola, ¿qué puedes hacer?" --thread d8
# mirar "ruta": ["inicio", "agente"]  -> respuesta directa, sin herramientas

S20_MAX_HERRAMIENTAS=1 uv run python -m agente.cli chat "Mira el ticket T-100 y consulta la política aplicable" --thread d9
# solo se ejecuta la primera herramienta: el límite está en el código
```

## Diapositivas 10–11 · Memoria y propiedad

```bash
uv run python -m agente.cli chat "¿Cómo está el ticket T-200?" --thread clase
uv run python -m agente.cli chat "¿Qué ticket estábamos viendo?" --thread clase
# es OTRO proceso: la memoria viene de PostgreSQL

uv run python -m agente.cli chat "¿Qué ticket estábamos viendo?" --thread clase --usuario luis
# "Esa conversación pertenece a otro usuario."

docker exec thepower-s20-postgres psql -U s20 -d s20_agente -c "\dt"
docker exec thepower-s20-postgres psql -U s20 -d s20_agente -c "select * from conversaciones"
```

## Diapositiva 12 · API

```bash
# terminal B
S20_ALMACEN=postgres uv run uvicorn agente.api:app --port 8020
# navegador: http://127.0.0.1:8020/docs

# terminal A
curl -s localhost:8020/health
curl -s -o /dev/null -w "%{http_code}\n" -X POST localhost:8020/chat \
  -H 'content-type: application/json' -d '{"thread_id":"api-1","mensaje":"hola"}'          # 401
curl -s -X POST localhost:8020/chat -H 'authorization: Bearer token-ana' \
  -H 'content-type: application/json' -d '{"thread_id":"api-1","mensaje":"¿Cómo está el ticket T-100?"}'
curl -s -w " -> %{http_code}\n" -X POST localhost:8020/chat -H 'authorization: Bearer token-luis' \
  -H 'content-type: application/json' -d '{"thread_id":"api-1","mensaje":"hola"}'          # 404
curl -s localhost:8020/conversaciones/api-1 -H 'authorization: Bearer token-ana'
```

## Diapositivas 13–14 · MCP

```bash
uv run python -m agente.cli mcp
uv run python -m agente.cli chat "¿Cómo está el ticket T-100?" --thread mcp
uv run python -m agente.cli chat "Consulta el ticket T-999" --thread mcp
```

## Diapositivas 15–16 · RAG

```bash
uv run python -m agente.cli ingestar      # dos veces: sigue habiendo 20 fragmentos
uv run python -m agente.cli chat "¿Cuál es el límite de peticiones del plan Estándar?" --thread rag
uv run python -m agente.cli chat "¿Cuál es la política de teletrabajo de los empleados?" --thread rag
docker exec thepower-s20-postgres psql -U s20 -d s20_agente -c \
  "select fragmento_id, seccion from fragmentos order by 1 limit 6"
```

## Diapositiva 18 · Investigación como trabajo

```bash
CASO="El ticket T-100 sigue abierto. Resume el problema, consulta la política aplicable y prepara una recomendación con fuentes. Si falta información pública, investígala."
uv run python -m agente.cli chat "$CASO" --thread caso     # registra INV-… (pendiente)
uv run python -m agente.cli investigar                      # el ejecutor lo termina
uv run python -m agente.cli chat "$CASO" --thread caso     # ahora trae el informe; no crea otro trabajo
uv run python -m agente.cli investigar                      # {"procesados": []}
uv run python -m agente.cli investigar --ver INV-xxxxxxxx   # informe completo, con consumo

# opcional, con internet: leer las fuentes reales de la lista blanca
S20_FUENTES=red uv run python -m agente.cli chat "Mira el ticket T-100 e investiga la tecnología implicada" --thread red
S20_FUENTES=red uv run python -m agente.cli investigar
```

## Diapositiva 19 · Observabilidad

```bash
# en la terminal B (uvicorn) aparece una línea JSON por turno: copiar su request_id
# con Langfuse (solo si hay claves de un proyecto de laboratorio):
S20_LANGFUSE=1 LANGFUSE_PUBLIC_KEY=… LANGFUSE_SECRET_KEY=… uv run python -m agente.cli chat "¿Cómo está el ticket T-100?" --thread lf
```

## Diapositiva 20 · Contenedor

```bash
docker build -t thepower-s20-agente:local .
docker run --rm -p 8021:8020 thepower-s20-agente:local      # otra terminal: curl localhost:8021/health
```

## Diapositiva 22 · Validación

```bash
uv run pytest                 # 38 tests sin coste
uv run pytest -m db           # 5 tests con PostgreSQL
uv run ruff check .
uv run python -m agente.cli recorridos --guardar
```

## Al terminar

```bash
docker compose down           # conserva los datos
docker compose down -v        # los borra
```
