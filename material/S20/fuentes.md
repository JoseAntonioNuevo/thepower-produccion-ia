# Fuentes de S20

## Correos (Gmail, solo lectura)

| Id | Fecha | Qué aporta | Cómo se leyó |
|---|---|---|---|
| `19f6f7569cc093d9` | 17/07/2026 | Temario de AI Engineer, bloque «Proyecto final: agente conversacional» | Mensaje completo leído en Gmail el 16/11/2026 durante la preparación de S19–S20; coincide con la copia local `docs/fuentes/temario-ai-engineer.txt`. Bloque de S20 en [fuentes/temario-S20-original.txt](fuentes/temario-S20-original.txt) |
| `1a1a6346ce2eb942` | 04/11/2026 | Laura: prácticas no obligatorias, teoría de la mano de la práctica, repositorio menos denso. Cita el correo de José del 03/11 («lo obligatorio es el proyecto final») | Leído completo en Gmail el 16/11/2026 |
| `1a1533d7800144ad` | 19/10/2026 | QR vigente de AI Engineer | Por su extracto (ver `material/S19/fuentes/indicaciones-laura.md`) |
| `1a0ebc9b585e70bc` / `1a0e699466bafc2e` | 28–29/09/2026 | Enunciados de ejercicios enviados: no hay ejercicio de S20 en ninguno | Guía de clases y plan S16–S20 |

**Límite de la lectura.** En esta sesión el conector de Gmail no estaba autorizado, así que no se
pudo buscar de nuevo en el buzón. El contenido de los dos primeros correos procede de la lectura
en Gmail hecha el 16/11/2026 por el agente que preparó S19 en la misma tarea, y coincide con las
copias locales. No se ha comprobado si después de esa fecha la escuela envió rúbrica, fecha o
formato del proyecto final.

## Documentos locales

- `GUIA-DE-CLASES-2026.md`: fecha (02/12, L/X), alcance del temario y límites de la información.
- `PLAN-S16-S20-NOVIEMBRE-DICIEMBRE-2026.md`, sección 7: caso, arquitectura, guion de 90 minutos,
  propuesta de valoración y criterios de cierre.
- Grafo, herramientas y telemetría de S5/S6: `1-langGraph/app/soporte/` (patrón de límite por turno
  y de trazas; no se importa).
- Corpus AetherCloud: `3-rag/lab/corpus/aethercloud-s10/` (copiado sin cambios).
- Sistema visual: `material/S17/fuentes/rediseno-visual/deck_lib.py` y el PowerPoint de ejemplo
  `S17-serverless-ai.pptx` aportado por José.

## Documentación técnica (consultada el 16/11/2026)

- LangGraph, «Persistence» y «Memory»: <https://docs.langchain.com/oss/python/langgraph/persistence>
- Langfuse, integración LangChain/LangGraph y «Sessions»:
  <https://langfuse.com/integrations/frameworks/langchain>, <https://langfuse.com/docs/observability/features/sessions>
- Gemini API, modelos y embeddings: <https://ai.google.dev/gemini-api/docs/models>,
  <https://ai.google.dev/gemini-api/docs/embeddings>. El índice de modelos lista también
  `gemini-embedding-2-preview`; comprobar el identificador vigente antes de usar el perfil real.
- SDK de MCP para Python 2.3.0: comprobado en el entorno del proyecto que `mcp.server.fastmcp` ya
  no existe y que la clase es `MCPServer` (`from mcp.server.mcpserver import MCPServer`); el error
  remite a <https://py.sdk.modelcontextprotocol.io/v2/migration/>.
- RFC 6585, sección 4 (429) y RFC 9110, sección 10.2.3 (Retry-After): <https://www.rfc-editor.org/>.
- Amazon Builders' Library, «Timeouts, retries, and backoff with jitter».
- Validación de la plantilla: `cfn-lint` (versiones de PostgreSQL admitidas por RDS: 17.1–17.11).

Versiones exactas de las librerías: `proyecto-final/pyproject.toml` y `uv.lock`.

## Imágenes de la presentación

| Imagen | Procedencia |
|---|---|
| Logotipo de thePower, QR de AI Engineer | Recursos del curso (`material/S20/assets`, copias byte a byte de S17/S16) |
| LangGraph, LangChain | Repositorios oficiales `langchain-ai/langgraph` y `langchain-ai/langchain`, `.github/images` |
| Model Context Protocol | Repositorio oficial `modelcontextprotocol/modelcontextprotocol`, `docs/logo` |
| FastAPI | <https://fastapi.tiangolo.com/img/> |
| Langfuse | <https://langfuse.com> y repositorio `langfuse/langfuse` |
| PostgreSQL | Kit de prensa de <https://www.postgresql.org> |
| Python | <https://www.python.org> |
| Iconos de AWS y genéricos | AWS Architecture Icons, paquete del 31/07/2026 (copiados de S16/S17) |

Diagramas, tablas y la gráfica de similitudes están dibujados con formas nativas. El árbol de la
traza de Langfuse (diapositiva 19) está rotulado como esquema: no es una captura.
