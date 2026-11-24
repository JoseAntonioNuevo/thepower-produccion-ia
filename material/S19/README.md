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
   20 diapositivas con notas del orador: 15 de recorrido (repaso del sistema y tres pruebas reales, cada una con
   pregunta y resultado) y 5 de anexo de consulta. Portada con fechas y grupos de los dos directos. Fuente editable
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
   El [repositorio público de S19](https://github.com/JoseAntonioNuevo/thepower-evaluacion) contiene la misma práctica.

## Estructura de la clase

| Hora | Bloque | Diapositivas | En vivo |
|---|---|---|---|
| 18:30 | Apertura: pregunta del día, QR y recorrido | 1–2 | — |
| 18:33 | Repaso del sistema: herramientas, RAG, grafo y Langfuse | 3–6 | `preflight`, `chat` (T17), sesión de Langfuse |
| 18:52 | Prueba 1 · Cambiar el generador (T01 y T12) | 7–10 | `chat` con Hydrogen y Terra |
| 19:16 | Prueba 2 · Cambiar el juez (V02 congelada) | 11–12 | `cmp` y puntuaciones de Sol y Opus |
| 19:32 | Prueba 3 · Regresión del evaluador (T09) | 13–14 | `cmp`, comprobación de T09, `pytest` |
| 19:50 | Cierre y práctica opcional | 15 | `estimar` |
| — | Anexo de consulta | 16–20 | Métricas, A/B 320 → 900, histórico Hydrogen–Sol, prompt NO_CONSTA, comandos |

## Estado real a 22/11/2026

| Qué | Estado |
|---|---|
| Demo con perfil doble (sin modelos) | **Ejecutada de principio a fin** contra PostgreSQL 17 + pgvector en Docker |
| Tests | **137** de la demo, **2** de pgvector y **19** del evaluador pasan; hay un fallo esperado en el ejercicio de fuentes contradictorias |
| Consulta como grafo LangGraph (`rag/grafo.py`) y CRAG como agente | **Hecho el 22/11**: salida del perfil doble idéntica antes y después (56 de 56 respuestas); tests de trayectoria y de `recursion_limit` |
| Chat en terminal (`s19.py chat`, OpenTUI de S5/S6) | **Probado** en pseudo-terminal con perfil doble y real, incluido `/perfil`; falta que José lo vea en su terminal |
| Evaluación de modelos (`MH` frente a `MS`, mismo juez) | **Ejecutada el 22/11**: Hydrogen 13/14, Sol 12/14 por criterio (dos fallos del criterio, no del contenido); Sol más rápido (p95 1,9 s frente a 3,6 s) y la mitad de caro por consulta |
| Métricas de producción en el informe | **Hechas**: p50/p95, tasas de error y rechazo, coste por consulta y por 1.000, peso del juez; el coste del sistema ya incluye los rechazos del modelo |
| Control de regresión | **Demostrado**: pasa con la referencia (código 0) y falla con tres copias degradadas (código 1) |
| API de Ragas 0.4.3 | **Comprobada** instalando las versiones fijadas; dos discrepancias documentadas |
| Presentación | **Generada y revisada** diapositiva a diapositiva sobre el render |
| Perfil real (OpenRouter: generación, embeddings y juez configurables en `.env`) | **Ejecutado el 22/11/2026** con Gemini 4 Hydrogen y juez Claude Opus 5.5: test A 13/14 aciertos y 6/6 rechazos; 1,29 USD medidos por pasada completa. Resultados en `demo-evaluacion/resultados/ejemplo-real/` |
| Envío a un servidor Langfuse | **Ejecutado el 22/11/2026** en Langfuse Cloud (UE): sesiones `langfuse-prueba-hydrogen` y `chat-20261122-155649` comprobadas en Brave; detalle en [verificacion.md](verificacion.md) |
| Revisión manual humana | **Pendiente** de José: plantilla real en `demo-evaluacion/resultados/ejemplo-real/test-A/revision-manual.csv`; hay un ejemplo hecho por el agente con el perfil doble |

Los resultados de T01, T12, V02 y T09 proceden de ensayos con modelos reales. El perfil
doble usa generación y embeddings locales para practicar el recorrido sin consumir la API.

## Antes del directo

1. [Lista previa](checklist.md).
2. Decidir si se quiere enseñar el perfil real. Previsión de `python s19.py estimar`:
   566 llamadas como máximo, 2,91 USD estimados, cota superior 24,90 USD con los modelos por
   defecto: Gemini 4 Hydrogen genera y Claude Opus 5.5 juzga (precios de OpenRouter del
   22/11/2026; `python s19.py catalogo` los actualiza).
