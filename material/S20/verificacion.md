# Verificación del material de S20

Ejecutado en el Mac de preparación, desde `material/S20/proyecto-final/`, el 16 y 17/11/2026.
Python 3.12.16 (uv 0.13.7), Docker 29.9.3. Todo en el **perfil doble** (sin modelo, sin coste),
salvo donde se indica.

## Comprobado

| Qué | Comando | Resultado |
|---|---|---|
| Lock al día | `uv lock --check` | 90 paquetes resueltos, sin cambios |
| Tests sin red ni coste | `uv run pytest` | **38 pasados**, 5 deseleccionados, ~4 s |
| Tests con PostgreSQL | `docker compose up -d --wait && uv run pytest -m db` | **5 pasados** |
| Estilo | `uv run ruff check .` · `uv run ruff format --check .` | sin avisos · 42 archivos ya formateados |
| Plantilla AWS | `uvx cfn-lint infra/plantilla.json` | sin avisos (salida 0) |
| Modo clase | `uv run python demo_clase.py --sin-pausa` y `uv run pytest -m demo` | 14 pasos sin fallos con PostgreSQL (~14 s); ensayo automático de los pasos 1–13 en memoria: 1 pasado |
| Aceptación en memoria | `uv run python -m agente.cli recorridos --guardar` | `todo_ok: true`, 10/10 |
| Aceptación en PostgreSQL | `S20_ALMACEN=postgres … recorridos --guardar` | `todo_ok: true`, 10/10 |
| Aceptación con fuentes en red | `S20_ALMACEN=postgres S20_FUENTES=red … recorridos --guardar` | `todo_ok: true`, 10/10; 2 fuentes, 520.105 bytes, 0,62 s |
| MCP real por stdio | `uv run python -m agente.cli mcp` y tests | descubrir 0,29 s; llamada 0,25 s; T-999 → `ok: false`; T-1 → error del servidor; herramienta no permitida → rechazada en el cliente |
| Memoria entre procesos | dos `cli chat` con `--thread reinicio-1` | el segundo proceso recuerda T-200; 10 checkpoints guardados |
| Aislamiento | `cli chat … --usuario luis` | «Esa conversación pertenece a otro usuario.» |
| Reingesta idempotente | `cli ingestar` ×2 | 10 documentos, 20 fragmentos las dos veces |
| API | `uvicorn agente.api:app --port 8020` + `curl` | `/health` 200; `/chat` sin token 401; con token 200; hilo ajeno 404; 4 rutas en OpenAPI; una línea JSON por turno |
| Imagen Docker | `docker build -t thepower-s20-agente:local .` + `docker run` | 613 MB; `/health` y `/chat` (con MCP dentro del contenedor) correctos; proceso como usuario `agente` |
| Ruta de código de Langfuse | `S20_LANGFUSE=1` con claves ficticias y `LANGFUSE_TRACING_ENABLED=false` | el turno termina sin errores; no se envía nada |
| Secretos en evidencias | `grep` de tokens y contraseña en `evidencias/*.json` | ninguno |
| Presentación | `python check.py presentaciones/S20-proyecto-final.pptx` | 24 diapositivas, 0 problemas; QR vigente 1 (idéntico al de S16), QR antiguo 0, logotipo 2 |
| Render de la presentación | LibreOffice del runtime local → PDF → `pdftoppm` | 24 páginas revisadas una a una frente a los renders del ejemplo S17 |
| Tipografías | `pdffonts` del PDF | Georgia, Arial y Courier New, como el ejemplo; DejaVu Sans solo para dos símbolos (✓ y ⇄) que Arial no tiene |

Evidencias guardadas: `proyecto-final/evidencias/recorridos-doble-{memoria-locales,postgres-locales,postgres-red}.json`.

## Pendiente o no verificado

| Qué | Por qué | Cómo cerrarlo |
|---|---|---|
| Perfil real (Gemini) | Llamadas de pago; no autorizadas | `S20_PERFIL=real GOOGLE_API_KEY=… uv run python -m agente.cli recorridos`. Previsto: 20 embeddings de ingesta + unas 10–15 llamadas de chat y 1 de redacción por recorrido. Coste: consultar la tarifa vigente de la Gemini API antes de ejecutarlo; no se incluye estimación |
| Umbral de evidencia con modelo real | Depende del modelo de embeddings | Medir con preguntas reservadas, como en S19 |
| Traza real en Langfuse | Falta un proyecto Langfuse de laboratorio con claves | `S20_LANGFUSE=1` + claves; comprobar sesión, usuario y spans |
| Despliegue en AWS | Crea recursos de pago | Seguir `proyecto-final/docs/despliegue-aws.md` con presupuesto y limpieza |
| pgvector en RDS | No desplegado | `CREATE EXTENSION vector` con el usuario maestro tras desplegar |
| Construcción `linux/amd64` | La imagen se probó en arm64 (Mac) | `docker build --platform linux/amd64` antes de publicar en ECR |
| Ejecutor caído a mitad de trabajo | El trabajo queda `en_curso` sin plazo | Mejora pendiente: tiempo máximo y reintento |
| Formato del directo, fecha y rúbrica | No constan en los correos revisados | Confirmar con Laura |
| Rendimiento | Tiempos de un portátil, sin carga | No usar como compromiso de latencia |

## Avisos sobre el perfil doble

El «cerebro» doble son reglas escritas a mano (`agente/cerebro.py`) y el embedding doble es una
bolsa de palabras (`agente/rag.py`). El umbral 0,20 se eligió mirando ocho preguntas propias: el
margen es pequeño (0,232 frente a 0,192) y no mide calidad. Todas las salidas del doble llevan el
rótulo `[perfil doble · reglas, sin modelo]`.
