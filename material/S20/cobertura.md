# Cobertura del temario de S20

Fuente: [fuentes/temario-S20-original.txt](fuentes/temario-S20-original.txt) (correo de Laura del
17/07/2026). Diapositivas de `presentaciones/S20-proyecto-final.pptx`; archivos relativos a
`proyecto-final/`. «Verificado» = ejecutado en local el 16/11/2026 en el perfil doble.

| Punto del temario | Diapositivas | En vivo | Archivo | Estado |
|---|---|---|---|---|
| Integrar todo lo aprendido en un único proyecto | 1, 4, 6 | `cli recorridos` | `README.md`, `agente/servicios.py` | Verificado |
| Introducción al proyecto y planificación | 3, 5 | — | `docs/arquitectura.md`, `agente/cli.py` (recorridos) | Verificado |
| Prompts y configuración del agente | 7 | abrir `config.py`, `prompts.py` | `agente/config.py`, `agente/prompts.py`, `.env.example` | Verificado |
| Construcción del grafo | 8 | `chat "Hola…"` → ruta | `agente/grafo.py` | Verificado |
| Módulos y herramientas | 9, 21 | `S20_MAX_HERRAMIENTAS=1 …` | `agente/herramientas.py`, `agente/cerebro.py` | Verificado |
| Aplicación | 12 | `uvicorn` + `/docs` + `curl` | `agente/api.py`, `agente/cli.py` | Verificado |
| Integración con PostgreSQL | 10, 11 | dos procesos, mismo hilo; otro usuario | `agente/almacen.py`, `esquema.sql`, `compose.yaml` | Verificado (Docker local) |
| Integración con Langfuse | 19 | línea JSON del turno | `agente/observabilidad.py` | Log verificado; **traza real pendiente** (sin claves) |
| Exposición vía FastAPI | 12 | `curl /health`, `/chat` 401/200/404 | `agente/api.py` | Verificado |
| Integración con MCPs | 13, 14 | `cli mcp`; T-100 y T-999 | `servidor_mcp/tickets.py`, `agente/mcp_cliente.py` | Verificado (stdio real) |
| Despliegue en AWS | 6, 20 | abrir plantilla; `docker build/run` | `Dockerfile`, `infra/plantilla.json`, `docs/despliegue-aws.md` | Imagen verificada; plantilla con `cfn-lint`; **no desplegado** |
| Deep Research: investigación autónoma | 17, 18 | caso completo → `investigar` → caso | `agente/investigacion.py` | Verificado (copias de aula y red) |
| … combinada con recuperación propia (RAG) | 15, 16, 17 | `ingestar`; cita y rechazo | `agente/rag.py` | Verificado (perfil doble) |
| Integración de todos los componentes | 22 | `pytest`, `pytest -m db`, `recorridos --guardar` | `tests/`, `evidencias/` | Verificado |
| Entrega de este proyecto final | 23 | abrir `docs/ejercicio.md` | `docs/ejercicio.md`, `../enunciado.md` | Propuesta; **rúbrica pendiente con la escuela** |

## Criterios de cierre del plan (PLAN-S16-S20, sección 7)

| Criterio | Estado |
|---|---|
| Turno directo, tool MCP válida, tool inexistente, RAG con cita, rechazo y research con evidencia | Hecho: `evidencias/recorridos-doble-*.json` |
| La memoria continúa tras reinicio y una identidad no accede a otra conversación | Hecho: `tests/test_postgres.py`, `tests/test_api.py`, recorridos |
| PostgreSQL y FastAPI funcionan en el despliegue AWS del laboratorio | **Pendiente**: no desplegado |
| La traza Langfuse permite seguir una consulta de extremo a extremo | **Pendiente**: sin proyecto Langfuse de laboratorio |
| Una investigación real tiene resultado, fuentes y consumo; volver a consultarla no duplica | Hecho con fuentes reales en red; sin modelo (perfil doble) |
| Se observan límites y un fallo controlado; el informe parcial no se presenta como completo | Hecho: tests de límite, herramienta inventada, fallo del modelo e informe parcial |
| Starter, solución y ensayo funcionan sin rutas privadas del Mac | Hecho: el proyecto es autónomo (rutas relativas, `uv.lock`) |
| Formato del directo, entrega y rúbrica acordados antes de publicarlos | **Pendiente** con la escuela |

## Cambio respecto al plan del 17/10

El plan proponía reutilizar el RAG de S19 y la API desplegada de S16/S18. El proyecto final es
**autónomo** (no importa nada de otras carpetas) para que el grupo L/X lo pueda ejecutar entero sin
depender de material de otras sesiones, siguiendo la petición de un repositorio menos denso.
