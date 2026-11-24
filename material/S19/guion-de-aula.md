# S19 · Guion del directo

Lee la frase entre comillas. Copia cada bloque en la aplicación indicada. En la TUI, pulsa **Intro** y espera la respuesta antes de continuar.

## Arranque · Warp

«Vamos a preguntar a Hydrogen y a seguir cada consulta en Langfuse.»

**Para empezar hoy:** en Warp, comprueba que ves **Hydrogen · config A**, **corpus base** y **Aún no hay consultas**. Si es así, pasa al **paso 1** y pega la pregunta sobre TLS.

**Solo si necesitas arrancar de cero**, pega este bloque en una pestaña de Warp con terminal:

```bash
cd material/S19/demo-evaluacion &&
docker compose up -d --wait &&
uv run --frozen python s19.py preparar-corpus --config A --env .env.hydrogen-sol --execute &&
S19_PROMPT_VERSION=v1 S19_GEN_TEMPERATURE='' uv run --frozen python s19.py chat --config A --env .env.hydrogen-sol --execute
```

**Espera** la TUI con **Hydrogen · A · base** y **Langfuse on**. Tras la primera pregunta, abre [Sessions en Brave](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions) y busca el `chat-…` de **tu** pantalla. El chat usa la API de pago.

## 1. Mismo resultado con dos modelos

«¿Mantiene Terra la respuesta y la cita que da Hydrogen?»

**TUI**

```text
¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?
```

```text
/perfil terra-opus
```

```text
¿Qué versión de TLS exigen las pasarelas perimetrales de AetherCloud?
```

**Espera** **TLS 1.3** y la misma cita de arquitectura en ambos turnos. En Brave abre [Sessions](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions), busca el `chat-…` que muestra **tu TUI** y selecciona cada turno. En **Open trace → generacion** verás los segundos y el coste de esa llamada.

## 2. ¿Ha fallado el modelo o el test?

«¿Debería fallar una respuesta por escribir “ms” en vez de “milisegundos”?»

**TUI · Pregunta a Terra.**

```text
¿Qué percentil de latencia dispara el rollback automático y a partir de qué latencia se conserva siempre una traza?
```

**Cambia a Hydrogen y pega de nuevo la misma pregunta.**

```text
/perfil hydrogen-sol
```

```text
¿Qué percentil de latencia dispara el rollback automático y a partir de qué latencia se conserva siempre una traza?
```

**Espera** p95 superior a **800 ms durante tres minutos** y trazas de más de **1.500 ms**. Compara **generacion → Output** con **Scores → acierto_criterio**.

**Di según lo que salga:** si ambos pasan, «Los dos han dado los valores y el test los reconoce». Si uno escribe «ms» y falla, «¿Ha cambiado el dato o la forma de escribir la unidad?». En el último ensayo pasaron ambos.

## 3. Una regresión que sí nota el usuario

«Mismos documentos y mismo modelo. ¿Qué cambia si buscamos en fragmentos más largos?»

**TUI**

```text
/config A
```

```text
¿Qué plazo hay para pedir un crédito de servicio y qué hay que adjuntar a la solicitud?
```

```text
/config B
```

```text
¿Qué plazo hay para pedir un crédito de servicio y qué hay que adjuntar a la solicitud?
```

**Espera** que A responda **15 días hábiles desde el cierre del mes y los identificadores de incidencia**. Con B, **«No consta»**. En **recuperacion → Output**, la similitud pasó de **0,6219 a 0,4589**, por debajo del umbral **0,5223**. En B el grafo terminó antes de generar.

**TUI · Recupera los fragmentos cortos para el resto de la clase.**

```text
/config A
```

## 4. Cómo probar el RAG y el agente · Demo en Kiro

Abre en Kiro una copia de [la demo](demo-evaluacion/) para hacer aquí los cambios temporales del taller. **⌘P** abre un archivo en la línea indicada. Ejecuta los comandos en **Terminal → New Terminal** de esa carpeta.

### Comprueba las dos rutas

«¿Cuántas veces llamamos al generador cuando hay evidencia? ¿Y cuando falta?»

**Kiro · ⌘P:** `rag/grafo.py:88` para enseñar la decisión y `tests/test_grafo.py:48` para enseñar los dos tests.

```bash
uv run --frozen pytest -v tests/test_grafo.py -k 'con_evidencia_recorre or sin_evidencia_toma'
```

**Espera** **2 passed**. Señala los `assert`: con evidencia, una llamada; con rechazo previo, cero.

### Introduce un fallo que los tests actuales dejan pasar

«Voy a hacer que el agente abandone tras la primera búsqueda vacía. ¿Lo detectarán los cinco casos?»

**Kiro · ⌘P:** `ampliacion/crag.py:33`. En `decidir`, pega estas líneas antes del primer `if` y guarda.

```text
    if mejor_similitud is None:
        return "rechazar"
```

**Terminal de Kiro**

```bash
uv run --frozen pytest -q --tb=short tests/test_enrutado.py::test_tabla_de_decisiones
```

**Espera** **5 passed**. La tabla contempla una búsqueda vacía en el último intento. Le falta el primero.

### Escribe el caso que falta

«Si la primera búsqueda vuelve vacía y queda otro intento, esperamos que reformule.»

**Kiro · ⌘P:** `tests/test_enrutado.py:10`. Inserta esta fila encima de `(None, 2, "rechazar")`, guarda y repite el comando con **↑ Intro**.

```text
        (None, 1, "reformular"),
```

**Espera** **1 failed, 5 passed**: esperábamos `reformular` y obtuvimos `rechazar`. Quita las dos líneas añadidas en `decidir`, conserva el test, guarda y repite: **6 passed**.

### Opcional · Detecta un lote degradado

«¿Saltaría la alarma si el buscador perdiera el primer documento de cada consulta?»

**Terminal de Kiro**

```bash
uv run --frozen python s19.py regresion resultados/ejemplo-doble/validacion-A
echo "Salida: $?"
```

```bash
uv run --frozen python s19.py regresion resultados/ejemplo-doble/degradado-recuperacion
echo "Salida: $?"
```

**Espera** **PASA · 0** en la referencia y **FALLA · 1** en la copia degradada. El recall cae a **0,10** y el mínimo es **0,90**.

## 5. Qué pasa cuando cambian los documentos · Demo en Kiro

En cada caso ejecuta el test local en **Kiro**, pregunta en la **TUI** y refresca **tu sesión** en Brave. Abre las dos últimas trazas. **Metadata → corpus** identifica la versión de cada una.

### Alta

«¿Aprende el sistema un dato al añadir su primera fuente?»

**Terminal de Kiro**

```bash
uv run --frozen pytest -q -s tests/test_cambios_corpus.py::test_alta
```

**TUI · Antes y después. Copia un bloque cada vez.**

```text
/corpus base
```

```text
¿Cuántos minutos dura la reserva del telescopio Nébula?
```

```text
/corpus alta
```

```text
¿Cuántos minutos dura la reserva del telescopio Nébula?
```

**Espera** **1 passed**. En la TUI, «No consta» → **30 minutos**. En la segunda traza, busca el reglamento nuevo en **generacion → Input**.

### Baja

«Si retiramos la política, ¿sigue dando el plazo antiguo?»

**Terminal de Kiro**

```bash
uv run --frozen pytest -q -s tests/test_cambios_corpus.py::test_baja
```

**TUI · Antes y después. Copia un bloque cada vez.**

```text
/corpus base
```

```text
¿Cuánto dura el periodo de enfriamiento de una CMK antes de su borrado irreversible?
```

```text
/corpus baja
```

```text
¿Cuánto dura el periodo de enfriamiento de una CMK antes de su borrado irreversible?
```

**Espera** **1 passed**. En la TUI, **72 horas** → **«No consta»**. En **recuperacion → Output** desaparece la fuente de claves; el segundo turno termina ahí.

### Actualización

«Si cambia el plazo dentro del mismo archivo, ¿qué versión lee el modelo?»

**Terminal de Kiro**

```bash
uv run --frozen pytest -q -s tests/test_cambios_corpus.py::test_actualizacion
```

**TUI · Antes y después. Copia un bloque cada vez.**

```text
/corpus alta
```

```text
¿Cuántos minutos dura la reserva del telescopio Nébula?
```

```text
/corpus actualizacion
```

```text
¿Cuántos minutos dura la reserva del telescopio Nébula?
```

**Espera** **1 passed**. Misma cita, **30 → 45 minutos**. Abre **generacion → Input** para leer el texto antiguo y el actualizado.

### Contradicción

«Si el reglamento dice 30 y el manual dice 90, ¿qué duración le prometemos al usuario?»

**Terminal de Kiro**

```bash
uv run --frozen pytest -q -s --runxfail --tb=short tests/test_cambios_corpus.py -k conflicto
```

**TUI · Antes y después. Copia un bloque cada vez.**

```text
/corpus alta
```

```text
¿Cuántos minutos dura la reserva del telescopio Nébula?
```

```text
/corpus conflicto
```

```text
¿Cuántos minutos dura la reserva del telescopio Nébula?
```

**Espera** **1 passed y 1 failed** en el test local: ambas fuentes llegan, pero se incumple la regla de abstenerse. En el ensayo real, Hydrogen explicó la discrepancia y citó **30 y 90**. En **generacion → Input / Output**, compara las dos fuentes con lo que conteste hoy.

**TUI · Al terminar, vuelve a los documentos habituales.**

```text
/corpus base
```

**Respaldo si falla el directo:** [ensayo general con las 14 trazas, en el orden de este guion](https://cloud.langfuse.com/project/cmwrx9lak007pad0e19vlgk2l/sessions/chat-20261124-175938).
