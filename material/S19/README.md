# S19 · Evaluación y testing de sistemas de IA

**AI Engineer · M/J: martes 24/11/2026 · L/X: lunes 30/11/2026 · 18:30–20:00 Europe/Madrid.**
Profesor: José Antonio Nuevo. El mismo material sirve para las dos fechas.

Objetivo del temario: *cerrar el ciclo de calidad: medir de forma rigurosa si un sistema de
IA funciona bien antes y después de cada cambio*. La clase construye un RAG pequeño, mide
recuperación y generación por separado, lo cubre con tests y demuestra un control de
regresión que falla cuando debe.

**S19 no depende de la demo de S18.** El directo de M/J (24/11) es anterior a la S18 de José
(25/11, L/X), así que todo corre en local con su propio proyecto.

## Qué evalúa el QR en cada fecha

| Directo | Grupo | El QR de la diapositiva 2 valora |
|---|---|---|
| Martes 24/11/2026 | M/J | S18 del jueves 19/11/2026 |
| Lunes 30/11/2026 | L/X | S18 del miércoles 25/11/2026 |

QR vigente de AI Engineer: [assets/qr-ai-engineer.jpg](assets/qr-ai-engineer.jpg), copia byte a
byte de `material/S16/assets/`.

## Piezas

1. **[Presentación](presentaciones/S19-evaluacion-testing.pptx)** y [PDF](presentaciones/S19-evaluacion-testing.pdf):
   32 diapositivas con notas del orador (portada con fechas y grupos de los dos directos). Mismo diseño que el ejemplo de S17. Fuente editable
   en [fuentes/presentacion/](fuentes/presentacion/README.md).
2. **[Demo `demo-evaluacion`](demo-evaluacion/README.md)**: proyecto Python autónomo, paso a paso.
3. [Guion de 90 minutos](demo-evaluacion/docs/guion-clase.md),
   [comandos en el orden de la presentación](demo-evaluacion/docs/comandos.md) y
   [guion del directo con dos modelos y Langfuse](guion-directo-modelos.md) (solo profesor, fuera del ZIP).
4. [Práctica opcional paso a paso](demo-evaluacion/docs/ejercicio.md) y [enunciado original](enunciado.md).
5. [Evaluador aislado con Ragas 0.4.3](demo-evaluacion/evaluador/README.md) y lo que se encontró en su API.
6. [Resultados de ejemplo del perfil doble](demo-evaluacion/resultados/README.md).
7. [Cobertura](cobertura.md) del temario y del enunciado, [verificación](verificacion.md),
   [fuentes](fuentes.md) y [lista previa al directo](checklist.md).
8. Fuentes de la escuela: [temario](fuentes/temario-S19-original.txt),
   [ejercicio](fuentes/ejercicio-S19-original.txt) e [indicaciones de Laura](fuentes/indicaciones-laura.md).
9. **[Paquete para los alumnos](paquetes/S19-demo-evaluacion.zip)** ([manifiesto](paquetes/manifiesto.json)):
   la demo autocontenida con `ENUNCIADO.md`, sin el guion del profesor. Se regenera con
   `uv run python -m scripts.empaquetar_s19` desde la raíz del repositorio.

## Estructura de la clase

| Hora | Bloque | Diapositivas | En vivo |
|---|---|---|---|
| 18:30 | Apertura: QR, plan, punto de partida (qué es evaluar, tests frente a evaluación, casos de uso) y caso | 1–6 | — |
| 18:41 | 1 · Qué medir | 7–10 | `preflight`, `ingestar`, `preguntar`, `chat` (grafo paso a paso) |
| 18:51 | 2 · Recuperación | 11–14 | `calibrar`, `lote`, `informe` |
| 19:06 | 3 · Generación | 15–21 | `evaluar.py`, revisión manual |
| 19:24 | 4 · Testing automatizado | 22–26 | `pytest`, `umbrales`, `regresion`, `degradar` |
| 19:38 | 5 · Producción y observabilidad | 27–30 | `comparar` |
| 19:51 | Práctica opcional y cierre | 31–32 | `estimar` |

## Estado real a 22/11/2026

| Qué | Estado |
|---|---|
| Demo con perfil doble (sin modelos) | **Ejecutada de principio a fin** contra PostgreSQL 17 + pgvector en Docker |
| Tests | **131** de la demo, **2** de pgvector y **19** del evaluador pasan; `ruff` limpio |
| Consulta como grafo LangGraph (`rag/grafo.py`) y CRAG como agente | **Hecho el 22/11**: salida del perfil doble idéntica antes y después (56 de 56 respuestas); tests de trayectoria y de `recursion_limit` |
| Chat en terminal (`s19.py chat`, OpenTUI de S5/S6) | **Probado** en pseudo-terminal con perfil doble y real, incluido `/perfil`; falta que José lo vea en su terminal |
| Evaluación de modelos (`MH` frente a `MS`, mismo juez) | **Ejecutada el 22/11**: Hydrogen 13/14, Sol 12/14 por criterio (dos fallos del criterio, no del contenido); Sol más rápido (p95 1,9 s frente a 3,6 s) y la mitad de caro por consulta |
| Métricas de producción en el informe | **Hechas**: p50/p95, tasas de error y rechazo, coste por consulta y por 1.000, peso del juez; el coste del sistema ya incluye los rechazos del modelo |
| Control de regresión | **Demostrado**: pasa con la referencia (código 0) y falla con tres copias degradadas (código 1) |
| API de Ragas 0.4.3 | **Comprobada** instalando las versiones fijadas; dos discrepancias documentadas |
| Presentación | **Generada y revisada** diapositiva a diapositiva sobre el render |
| Perfil real (OpenRouter: generación, embeddings y juez configurables en `.env`) | **Ejecutado el 22/11/2026** con Gemini 4 Hydrogen y juez Claude Opus 5.5: test A 13/14 aciertos y 6/6 rechazos; 1,29 USD medidos por pasada completa. Resultados en `demo-evaluacion/resultados/ejemplo-real/` |
| Envío a un servidor Langfuse | **No ejecutado**; llamadas al SDK probadas sin red |
| Revisión manual humana | **Pendiente** de José: plantilla real en `demo-evaluacion/resultados/ejemplo-real/test-A/revision-manual.csv`; hay un ejemplo hecho por el agente con el perfil doble |

Todas las cifras que aparecen en la presentación y en la demo son del **perfil doble** o
ejemplos ilustrativos, y van rotuladas. Ninguna mide un modelo.

## Antes del directo

1. [Lista previa](checklist.md).
2. Decidir si se quiere enseñar el perfil real. Previsión de `python s19.py estimar`:
   566 llamadas como máximo, 2,91 USD estimados, cota superior 24,90 USD con los modelos por
   defecto: Gemini 4 Hydrogen genera y Claude Opus 5.5 juzga (precios de OpenRouter del
   22/11/2026; `python s19.py catalogo` los actualiza).
