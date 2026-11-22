# Sesión 22/11/2026 · S19: LangGraph, chat en terminal y evaluación de modelos

**Alcance.** Refactorizar la consulta del RAG de S19 a LangGraph, añadir un chat de terminal
con la OpenTUI de S5/S6 y cubrir los cuatro bloques del temario de S19 (evaluación de modelos,
métricas de producción, testing de agentes y pipelines, observabilidad). Langfuse queda
preparado; su envío real se hará cuando José facilite las claves.

**Decisiones.**
- El modelo se sigue llamando con el cliente `openai` hacia OpenRouter dentro de los nodos:
  conserva el coste medido con BYOK, el razonamiento bajo y el aviso de tokens agotados.
- Solo Langfuse (lo pide el enunciado); LangSmith no se integra.
- `responder()` mantiene firma y salida: lote, informe, Ragas y regresión no cambian.
- La TUI se copia y adapta (sin importar `1-langGraph`): el módulo sigue siendo independiente.
- Evaluación de modelos con variantes `MH`/`MS` que solo cambian `gen_modelo`, mismo archivo de
  entorno y juez ajeno a los candidatos (Opus 5.5).
- El coste del sistema incluye los rechazos del modelo; el rechazo previo es el único sin coste.

**Cambios.** `rag/grafo.py`, `ampliacion/crag.py` (agente LangGraph), `ui/` (motor + TUI),
`--env` en `s19.py` y `evaluar.py`, bloque «Producción» en `evaluacion/informe.py`, variantes en
`datos/configuraciones.json`, tests `test_grafo.py`, `test_tui.py`, `test_produccion.py`,
documentación, presentación (22–24, 32) y ZIP. Archivos de clase `.env.hydrogen-sol` y
`.env.sol-opus` (ignorados por Git) con bloque de Langfuse vacío.

**Verificación.** Ver `material/S19/verificacion.md`, sección del 22/11 «LangGraph, chat…».

**Lecciones.**
- Un refactor de orquestación se valida comparando la salida completa antes y después (56/56).
- Con LangGraph, las observaciones de Langfuse deben colgar explícitamente de la raíz.
- Los criterios de cadena son frágiles («ms», «24×7») y un modelo sin temperatura cambia de
  veredicto entre pasadas: la revisión manual no es opcional.
- Las cuentas de coste deben contar toda llamada pagada, no solo las respuestas emitidas.

**Pendiente.** Claves de Langfuse y prueba real; José abre el chat en su terminal; revisión
manual humana; commit (no solicitado).
