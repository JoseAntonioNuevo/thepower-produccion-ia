# Taller S19 · Evalúa un cambio en un RAG

Trabaja desde la carpeta que contiene `s19.py`, después de la [instalación](../README.md#antes-de-empezar).
Abre dos terminales, una para el chat y otra para las pruebas.

## Pregunta, cambia el índice y repite

Con el perfil doble de `.env.example` puedes practicar sin claves. Prepara el índice B
y las cinco versiones del corpus A antes de abrir el chat.

```bash
uv run --frozen python s19.py ingestar --config B
uv run --frozen python s19.py preparar-corpus --config A
uv run --frozen python s19.py chat --config A
```

1. Pega **¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?**. Busca TLS 1.3 y la cita de arquitectura. Con el corpus base, pegar una pregunta exacta del test activa también su puntuación.
2. Pega **¿Qué plazo hay para pedir un crédito de servicio y qué hay que adjuntar a la solicitud?**. Escribe `/config B` y repite. Compara la mejor similitud, el umbral y la ruta del grafo. Vuelve con `/config A`.
3. Para comparar respuestas de modelos reales, prepara tus propios perfiles con el mismo índice, prompt y parámetros. Cambia de archivo con `/perfil <nombre>` y repite la misma pregunta. El [README](../README.md#cambiar-cualquier-modelo-desde-env) explica la configuración de OpenRouter. En perfil real, ingesta, preparación y chat requieren `--execute` y consumen API.

## Cambios en los documentos

Para Nébula, pregunta **¿Cuántos minutos dura la reserva del telescopio Nébula?**. Para las claves, pregunta **¿Cuánto dura el periodo de enfriamiento de una CMK antes de su borrado irreversible?**. Haz la misma pregunta tras cada cambio de corpus.

| Prueba | Órdenes en el chat | Qué comprobar |
|---|---|---|
| Alta · Nébula | `/corpus base` → `/corpus alta` | Aparece la fuente nueva y el plazo de 30 minutos. |
| Baja · claves | `/corpus base` → `/corpus baja` | Desaparece la política que respaldaba las 72 horas. Comprueba si el sistema se abstiene. |
| Actualización · Nébula | `/corpus alta` → `/corpus actualizacion` | La misma fuente cambia de 30 a 45 minutos. |
| Contradicción · Nébula | `/corpus alta` → `/corpus conflicto` | El reglamento dice 30 y el manual 90. Lee las dos citas y valora si la respuesta reconoce el conflicto. |

En tu propio proyecto de Langfuse, si activaste las trazas, busca el identificador del chat en **Sessions**. Dentro del turno, abre **Metadata** para ver `corpus` e `indice_id`, **recuperacion → Output** para ver qué encontró y **generacion → Input / Output** para ver qué leyó y qué contestó. Al terminar, escribe `/corpus base`.

## Prueba el comportamiento automáticamente

```bash
uv run --frozen pytest -v tests/test_grafo.py -k 'con_evidencia_recorre or sin_evidencia_toma'
uv run --frozen pytest -q --tb=short tests/test_enrutado.py::test_tabla_de_decisiones
uv run --frozen pytest -q -s tests/test_cambios_corpus.py
```

En `rag/grafo.py`, localiza `ruta_tras_recuperar`. En `tests/test_grafo.py`, observa cómo los tests comprueban tanto la ruta como el número de llamadas. Para el agente, compara `decidir` en `ampliacion/crag.py` con las filas de `test_tabla_de_decisiones`. Como ejercicio, añade la fila `(None, 1, "reformular")`: si aún queda otro intento, el agente puede volver a buscar.

Para proyectar el fallo esperado de la política de contradicciones:

```bash
uv run --frozen pytest -q -s --runxfail --tb=short tests/test_cambios_corpus.py -k conflicto
```

Una prueba pasa porque llegan ambos documentos. La otra falla porque el generador doble reproduce ambos plazos y el test exige abstención. Puedes comparar esos resultados con lo que haga tu modelo real.
