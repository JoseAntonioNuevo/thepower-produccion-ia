# Comprobación antes del directo S19

Vale para las dos fechas: **M/J 24/11/2026** y **L/X 30/11/2026**, 18:30–20:00.

## El día anterior

- [ ] Docker Desktop arranca. Python 3.12 y `uv` disponibles.
- [ ] `cd demo-evaluacion && uv sync && (cd evaluador && uv sync)` sin errores.
- [ ] `docker compose up -d --wait` y `uv run python s19.py preflight` → «Preflight correcto».
- [ ] `uv run pytest` → 131 pasan, 3 excluidos. `(cd evaluador && uv run pytest)` → 19 pasan.
- [ ] `uv run python s19.py chat` abre el chat en tu terminal (no en una salida de IDE); `1` responde y Esc sale.
- [ ] Ensayo completo de [los comandos](demo-evaluacion/docs/comandos.md) con prefijo `ensayo-` (`calibrar` y `umbrales` comparan sin sobrescribir `datos/` salvo con `--fijar`).
- [ ] Decidido si se enseña el perfil real. Si sí: gasto autorizado, `OPENROUTER_API_KEY` en `.env`, `catalogo` y `estimar` revisados, `preflight` del perfil real correcto.
- [ ] Si se enseña Langfuse: claves `LANGFUSE_*` y `S19_LANGFUSE=on` en `.env.hydrogen-sol` y `.env.sol-opus`, y un ensayo que deje trazas visibles (ver [guion del directo](guion-directo-modelos.md)).

## 15 minutos antes

- [ ] Contenedor `thepower-s19-pgvector` sano en `127.0.0.1:54519`.
- [ ] `.env` con `S19_PERFIL=doble` y `S19_LANGFUSE=off`. Ninguna clave en pantalla.
- [ ] Índices A y B creados (`ingestar --config A` y `--config B`).
- [ ] `resultados/` sin carpetas `mi-*` de ensayos anteriores.
- [ ] Terminal con letra grande en `demo-evaluacion/`. Editor con `datos/test.jsonl`, `evaluacion/metricas.py`, `rag/observabilidad.py` y el CSV de revisión de ejemplo.
- [ ] Presentación abierta en la diapositiva 1. QR de la diapositiva 2 legible desde el móvil.
- [ ] Notificaciones silenciadas.

## Durante la clase

- [ ] Diapositiva 2: decir qué sesión se valora (S18 del 19/11 en M/J; S18 del 25/11 en L/X).
- [ ] Decir en voz alta, la primera vez, que el perfil doble **no mide ningún modelo**.
- [ ] Vivo 4: enseñar el código de salida 0 y el código de salida 1.
- [ ] No presentar ninguna cifra del ejemplo como medición de un modelo real ni de Ragas con juez real.
- [ ] Recordar que la práctica es opcional.

## Si algo falla

| Fallo | Qué hacer |
|---|---|
| Docker no arranca | Enseñar `resultados/ejemplo-doble/` y ejecutar `uv run pytest` (no necesita base de datos) |
| `preflight` no conecta | `docker compose down -v && docker compose up -d --wait` (después hay que volver a `ingestar` A y B) |
| El chat no abre | Necesita una terminal real; si falla, seguir con `preguntar` y el mismo número de pregunta |
| Puerto 54519 ocupado | Cambiar el puerto en `compose.yaml` y en `S19_DATABASE_URL` |
| El evaluador tarda en arrancar | La primera importación de Ragas compila; ejecutarlo una vez antes de clase |

## Al terminar

- [ ] `docker compose down -v`.
- [ ] Anotar dudas de los alumnos para la siguiente fecha.
