# Tarea: configurar Langfuse Cloud para la demo de S19 y comprobar que llegan las trazas

Trabajas en el Mac de José. Usa **computer use en el navegador Brave** para la parte web
(Langfuse) y la terminal para los comandos. Hazlo todo tú, de principio a fin, salvo los pasos
que este texto reserva a José.

## Contexto: qué es esto y por qué hace falta

- Repositorio: `/Users/jose/Documents/the-power/4-produccion-ia` (curso AI Engineer de thePower).
  Lee antes su `AGENTS.md`. La demo está en `material/S19/demo-evaluacion/`.
- S19 es la clase «Evaluación y testing de sistemas de IA», el martes 24/11/2026. Uno de sus
  cuatro bloques es **«Integración de la evaluación con las herramientas de observabilidad»**, y
  el enunciado pide registrar en **Langfuse** respuesta, fuentes, métricas, latencia, tokens y
  coste por consulta, con el consumo del evaluador (juez de Ragas) en trazas aparte.
- El código ya lo hace. `rag/observabilidad.py` usa `langfuse==5.2.0`. Cada consulta es una
  traza `consulta-rag` con dos observaciones: `recuperacion` (tipo retriever) y `generacion`
  (tipo generation, con modelo, tokens y coste). Las métricas del caso son puntuaciones de la
  traza. El juez va en trazas `evaluador-ragas` con la etiqueta `evaluador`.
- **Nunca se ha enviado nada a un servidor Langfuse real.** Solo se ha probado sin red. Tu
  trabajo es crear el proyecto, poner las claves y demostrar que las trazas llegan bien, antes
  de la clase.
- La consulta del RAG es un grafo de LangGraph (`rag/grafo.py`). Hay un chat de terminal
  (`python s19.py chat`, OpenTUI) que deja una traza por pregunta.
- Hay dos archivos de entorno de clase en la carpeta de la demo. Git los ignora y ya contienen
  la clave de OpenRouter:
  - `.env.hydrogen-sol`: genera `google/gemini-4-hydrogen` y juzga `openai/gpt-6.2-sol`.
  - `.env.sol-opus`: genera `openai/gpt-6.2-sol` y juzga `anthropic/claude-opus-5.5`.

  Los dos tienen ya este bloque, con los valores vacíos:
  ```
  S19_LANGFUSE=off
  LANGFUSE_PUBLIC_KEY=
  LANGFUSE_SECRET_KEY=
  LANGFUSE_BASE_URL=https://cloud.langfuse.com
  ```
  El `.env` activo es otro archivo: está en perfil doble y **no se toca**. Los comandos eligen
  el archivo de clase con `--env`.
- PostgreSQL + pgvector corre en Docker (`thepower-s19-pgvector`, `127.0.0.1:54519`) y tiene
  cargado el índice real de la configuración A.

## Reglas (no negociables)

1. **Secretos.** No escribas las claves de Langfuse ni la de OpenRouter en el chat, en los logs,
   en archivos versionados, en el informe final ni en ningún comando que las imprima. Pásalas
   del navegador al archivo con el portapapeles y el script de abajo. Después vacía el
   portapapeles. Comprueba que están escritas sin mostrar su valor.
2. **Cuenta.** Usa la sesión de Langfuse que José ya tenga abierta en Brave. Si Langfuse pide
   iniciar sesión o crear una cuenta, **para y pídeselo a José**: no escribas contraseñas ni
   aceptes términos en su nombre. Elige siempre el plan gratuito (Hobby). No añadas métodos de
   pago, no invites a miembros y no actives funciones de pago.
3. **Región.** La UE: `https://cloud.langfuse.com`. Si la organización de José ya existe en otra
   región, úsala y pon esa URL en `LANGFUSE_BASE_URL`.
4. **Código.** No cambies código, tests ni dependencias, no hagas commit ni push y no uses
   LangSmith. No ejecutes `docker compose down -v`, porque borra el índice. Si algo falla en el
   código, para e informa con el error exacto.
5. **Gasto.** Tienes autorizado gastar en OpenRouter **0,50 USD como máximo** en total. Las
   cifras previstas están en cada paso. Ningún comando de pago se ejecuta sin `--execute`.
6. **Datos.** Las preguntas y documentos son ficticios (empresa «AetherCloud»). No envíes a
   Langfuse ningún otro dato.

## Paso 1 · Proyecto y claves en Langfuse (Brave, computer use)

1. Abre `https://cloud.langfuse.com` en Brave.
2. **Organización:** si ya existe una para thePower, úsala. Si no, crea `thePower`.
3. **Proyecto:** crea `s19-evaluacion`, o reutilízalo si ya existe.
4. En el proyecto, entra en **Settings → API Keys → Create new API keys**. Langfuse muestra la
   *Public Key* (`pk-lf-…`), la *Secret Key* (`sk-lf-…`, solo se ve una vez) y el *Host*.
   Si la interfaz ha cambiado, busca el equivalente; el resultado debe ser ese mismo par de claves.
5. **No cierres ese diálogo** hasta haber copiado las dos claves con el paso 2.

## Paso 2 · Escribir las claves sin mostrarlas (terminal)

Usa siempre el botón de copiar de Langfuse. Luego, desde la carpeta de la demo:

```bash
cd /Users/jose/Documents/the-power/4-produccion-ia/material/S19/demo-evaluacion
```

Copia primero la **Public Key** y ejecuta este script con `CLAVE=LANGFUSE_PUBLIC_KEY` y
`PREFIJO=pk-lf-`. Después copia la **Secret Key** y ejecútalo otra vez con
`CLAVE=LANGFUSE_SECRET_KEY` y `PREFIJO=sk-lf-`:

```bash
CLAVE=LANGFUSE_PUBLIC_KEY PREFIJO=pk-lf- python3 - <<'EOF'
import os, re, subprocess, pathlib
clave, prefijo = os.environ["CLAVE"], os.environ["PREFIJO"]
valor = subprocess.run(["pbpaste"], capture_output=True, text=True).stdout.strip()
if not valor.startswith(prefijo) or "\n" in valor:
    raise SystemExit(f"El portapapeles no contiene una clave que empiece por {prefijo}")
for nombre in (".env.hydrogen-sol", ".env.sol-opus"):
    p = pathlib.Path(nombre)
    texto, n = re.subn(rf"^{clave}=.*$", lambda _m: f"{clave}={valor}", p.read_text(encoding="utf-8"), flags=re.M)
    if n != 1:
        raise SystemExit(f"{nombre}: esperaba una línea {clave}=, hay {n}")
    p.write_text(texto, encoding="utf-8")
print(f"{clave} escrita en los dos archivos ({len(valor)} caracteres)")
EOF
```

Después de las dos claves:

```bash
printf '' | pbcopy                                            # vacía el portapapeles
sed -i '' 's/^S19_LANGFUSE=off$/S19_LANGFUSE=on/' .env.hydrogen-sol .env.sol-opus
# Solo si el Host de Langfuse no es https://cloud.langfuse.com, cambia LANGFUSE_BASE_URL igual.
grep -c '^LANGFUSE_PUBLIC_KEY=pk-lf-' .env.hydrogen-sol .env.sol-opus   # 1 y 1
grep -c '^LANGFUSE_SECRET_KEY=sk-lf-' .env.hydrogen-sol .env.sol-opus   # 1 y 1
grep -c '^S19_LANGFUSE=on$' .env.hydrogen-sol .env.sol-opus             # 1 y 1
grep '^S19_LANGFUSE' .env                                               # sigue en off (no se toca)
git status --short --ignored | grep '\.env'                             # solo !! (ignorados) y .env.example
```

Ya puedes cerrar el diálogo de Langfuse.

## Paso 3 · Comprobar sin gastar

```bash
uv run python s19.py preflight --env .env.hydrogen-sol   # debe decir «Langfuse: activado» y «Preflight correcto»
uv run python s19.py preflight --env .env.sol-opus
```

Si dice «índice de esta configuración todavía vacío», reconstrúyelo (menos de 0,001 USD):
`uv run python s19.py ingestar --config A --env .env.hydrogen-sol --execute`.

## Paso 4 · Primeras trazas reales: un lote de validación (unos 0,02 USD)

```bash
uv run python s19.py lote --env .env.hydrogen-sol --conjunto validacion --config A \
  --run langfuse-prueba-hydrogen --salida resultados/langfuse-prueba-hydrogen --execute
uv run python s19.py informe resultados/langfuse-prueba-hydrogen
```

En Brave, dentro del proyecto `s19-evaluacion`, comprueba en **Tracing** (Sessions y Traces):

- Hay una sesión `langfuse-prueba-hydrogen` con **8 trazas** `consulta-rag`, etiquetadas
  `s19`, `config:A` y `perfil:real`.
- En un caso respondido (por ejemplo V02), la traza tiene dos hijas, `recuperacion` y
  `generacion`. La generación lleva el modelo `google/gemini-4-hydrogen`, el prompt, la
  respuesta, los tokens de entrada y salida y un **coste** distinto de 0 (unas milésimas de USD).
  Las puntuaciones son `precision_at_5`, `recall_at_5`, `rechazo` y `acierto_criterio`.
- En un caso de **rechazo previo** solo está `recuperacion`, sin generación, tokens ni coste. Para
  encontrarlo, busca en `resultados/langfuse-prueba-hydrogen/respuestas.jsonl` una fila con
  `"motivo_rechazo": "evidencia_insuficiente"`.
- El coste lo envía el programa (`cost_details`), así que Langfuse no necesita conocer el precio
  del modelo. Si aparece sin coste, anótalo con el caso y el modelo.

## Paso 5 · Puntuaciones de Ragas y juez separado (unos 0,10–0,20 USD)

```bash
(cd evaluador && uv run python evaluar.py ../resultados/langfuse-prueba-hydrogen \
   --env ../.env.hydrogen-sol --modo real --execute)
uv run python s19.py informe resultados/langfuse-prueba-hydrogen
uv run python s19.py publicar-evaluador resultados/langfuse-prueba-hydrogen --env .env.hydrogen-sol
```

En Langfuse, comprueba que:

- las trazas `consulta-rag` de esa sesión tienen además `faithfulness` y `answer_relevancy`,
  solo en los casos respondidos; los rechazos no se puntúan y eso es correcto;
- existen trazas `evaluador-ragas` (etiqueta `evaluador`), una por caso, con el modelo del juez
  (`openai/gpt-6.2-sol`), sus tokens y su coste. El coste de juzgar va separado del de responder.

Este juez (GPT-6.2 Sol) no se ha usado nunca en una evaluación completa. Si falla, no toques el
código: anota el error exacto y repite **solo este paso** con `.env.sol-opus` (juez Opus, ya
probado; unos 0,18 USD). Usa la carpeta y el run `langfuse-prueba-opus` y empieza desde el lote
del paso 4 con ese archivo.

## Paso 6 · Trazas desde el chat (opcional, menos de 0,01 USD; computer use en Terminal)

El chat necesita una terminal interactiva real. No funciona en una salida sin TTY. Abre la app
Terminal de macOS:

```bash
cd /Users/jose/Documents/the-power/4-produccion-ia/material/S19/demo-evaluacion
uv run python s19.py chat --env .env.hydrogen-sol --execute
```

Escribe `3` y Enter (T12). Espera la respuesta. Luego escribe `/perfil sol-opus`, Enter, y
otra vez `3`. Sal con Esc. En Langfuse debe aparecer una sesión `chat-AAAAMMDD-HHMMSS` con 2
trazas: una con `gemini-4-hydrogen` y otra con `gpt-6.2-sol`, con `caso_test = T12` en los metadatos.

## Paso 7 · Dejarlo listo y documentarlo

- Los dos archivos de clase quedan con `S19_LANGFUSE=on` y las claves. El `.env` activo no cambia.
- Las carpetas `resultados/langfuse-prueba-*` están ignoradas por Git y se pueden quedar.
- Añade al final de `material/S19/verificacion.md` una sección «Langfuse Cloud · <fecha>» con:
  región, organización y proyecto (sin claves); qué comandos ejecutaste; qué comprobaste en la
  interfaz, caso por caso, y si coincide con lo esperado; las diferencias encontradas; y el
  gasto. Lee el saldo de OpenRouter sin imprimir la clave:
  ```bash
  K=$(grep '^OPENROUTER_API_KEY=' .env | cut -d= -f2-); curl -s https://openrouter.ai/api/v1/key -H "Authorization: Bearer $K" \
    | python3 -c "import json,sys;print(round(json.load(sys.stdin)['data']['limit_remaining'],2))"; unset K
  ```
  Escribe solo lo que hayas visto y verificado.
- No toques la presentación ni el resto de la documentación: José lo actualizará después con
  tu informe.

## Qué devuelves a José

Un resumen breve en español con:

1. El enlace al proyecto de Langfuse (sin claves).
2. Una tabla de comprobaciones de los pasos 3 a 6, cada una con «correcto», «falla» o «no
   hecho» y lo observado.
3. Las diferencias entre la interfaz de Langfuse y lo descrito aquí.
4. El gasto en OpenRouter (saldo antes y después).
5. Lo que quede pendiente.

No incluyas capturas que muestren claves.
