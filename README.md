# thePower Producción de IA

## Material vigente para clase · noviembre de 2026

- **S16:** [API pequeña con OpenRouter, Docker y Fargate](material/S16/demo-openrouter/README.md).
- **S17:** [API pequeña con Lambda, HTTP API IAM y Bedrock en eu-north-1](material/S17/demo-bedrock/README.md).
- [Power y materiales actuales de S17](material/S17/README.md).

La S17 pequeña tiene despliegue y limpieza ensayados. La clasificación real
sigue bloqueada por cuota cero de Bedrock en el proyecto Free; el README
explica la comprobación y la revisión pendiente con AWS. No se sustituyen
inferencias por simulaciones. Se mantiene el plan Free.

**Base histórica del monorepo.** Los comandos que siguen corresponden al
laboratorio original de octubre (Anthropic, eu-west-1 y ZIP avanzado de S17).
Para las clases actuales, comienza por los enlaces anteriores.

Base común de las sesiones S16–S20 de AI Engineer y laboratorio de **S16: Cloud deployment, AWS y Docker**, con una misma versión para el 12 y el 18 de noviembre de 2026, de 18:30 a 20:00 en Madrid. La práctica de S16 es opcional.

**S17 preparada localmente:** [código y paquete docente de Serverless AI](material/S17/README.md), para el 17/11 M/J y 23/11 L/X. Incluye handler Lambda, Bedrock, firma IAM, infraestructura, mediciones, costes y materiales. El ensayo AWS real sigue separado de la verificación local.

El proyecto implementa la misma clasificación de soporte mediante FastAPI en S16 y mediante Lambda/Bedrock en S17. Reutiliza la taxonomía de S7/S8 sin requerir los otros repositorios, pesos ni GPU. Evaluación, CI/CD y agente final siguen planificados.

## Empezar por S17 sin llamadas de pago

```bash
uv sync --frozen --all-extras
uv run python scripts/demo_s17.py
uv run python -m scripts.aws_s17 plan
uv run python scripts/costes_s17.py
```

La [guía de S17](material/S17/guia-alumno.md) desarrolla ZIP Linux, emulador, acceso, perfil europeo, despliegue, firma, cold/warm y limpieza. La [arquitectura](docs/arquitectura-s17.md) explica la reutilización y los límites. El modo demo no acredita IAM ni Bedrock real.

## Empezar por S16

- [Índice del paquete docente](material/S16/README.md).
- [Guía completa del alumno](material/S16/guia-alumno.md): instalación, API, Docker, AWS, verificación, coste y retirada.
- [Guion del profesor](material/S16/guion-profesor.md): explicación y preguntas, comandos, tiempos y alternativas.
- [Matriz de cobertura](material/S16/cobertura.md): todos los puntos del temario y del ejercicio, con ubicación y estado de verificación.
- [Decisiones y reutilización](docs/arquitectura.md).
- [Estado de preparación de S16–S20](docs/cobertura-S16-S20.md).

## Arranque local sin claves ni gasto

Requisitos: Python 3.12 y uv. Docker Desktop se necesita para el bloque de contenedores, no para ejecutar la API directamente.

```bash
uv sync --frozen --all-extras
uv run python scripts/preflight.py
uv run uvicorn curso_ia.api:create_app --factory --host 127.0.0.1 --port 8016 --no-access-log
```

En otra terminal:

```bash
curl --fail http://127.0.0.1:8016/health
curl --fail -H 'Content-Type: application/json' \
  --data-binary @datos/peticion.json http://127.0.0.1:8016/clasificar
uv run python scripts/ensayo_local.py
```

Documentación interactiva: `http://127.0.0.1:8016/docs`. `execution: demo` significa reglas locales, no un modelo. Los tokens y el coste desconocidos aparecen como `null`; `metodo_coste: sin_llamada` identifica que no hubo inferencia.

## Ejecutar el mismo código en Docker

Detener primero la API local para liberar el puerto 8016.

```bash
docker compose up --build -d
uv run python scripts/ensayo_local.py
docker compose logs --tail 10 api
docker compose down
```

Compose publica solo en loopback. Para preparar una imagen compatible con la tarea Fargate X86_64:

```bash
docker build --platform linux/amd64 --provenance=false \
  --build-arg APP_VERSION=s16-ensayo-01 -t thepower-s16:ensayo .
```

El Dockerfile fija el digest de la imagen base y usa `requirements.lock` con versiones y hashes. Solo entran dependencias y `src/` en el contexto permitido. La API corre como UID/GID 10001; no necesita escribir archivos. El Python del contenedor y el del Mac pueden tener diferente revisión de 3.12: registra ambas cuando compares.

## Modo real

El adaptador implementado usa Anthropic Messages. El identificador de modelo lo decide el operador y debe estar disponible en su cuenta. No se selecciona otro modelo cuando algo falla.

Copiar `.env.example` a `.env`, completar localmente `API_MODE=real`, `MODEL_ID` y `ANTHROPIC_API_KEY`, y arrancar con:

```bash
uv run --env-file .env python scripts/preflight.py
uv run --env-file .env uvicorn curso_ia.api:create_app --factory \
  --host 127.0.0.1 --port 8016 --no-access-log
```

El preflight es offline; la petición a `/clasificar` sí consume inferencia en modo real. No uses `ensayo_local.py` para esa operación: el script se niega a probar una API real. La guía del alumno explica una llamada sintética explícita y cómo conservar su evidencia. `GET /health` nunca comprueba el proveedor.

## AWS

```bash
uv run python scripts/aws_lab.py plan
uv run python scripts/aws_lab.py --help
```

El plan no lee credenciales ni abre conexiones. Las operaciones de cambio requieren perfil, región, cuenta esperada, laboratorio y `--execute`. `estado` es lectura; `verificar` hace una llamada real y también requiere `--execute`.

La secuencia es **registro ECR → imagen por digest → secreto → Fargate → salud y función → limpieza**. Las dos plantillas CloudFormation crean recursos propios, etiquetados. El contenedor tiene una IPv4 pública temporal, entrada 8000 limitada a una IP /32 y salida HTTPS. No hay NAT, balanceador ni base de datos. Este laboratorio usa contenido ficticio y no envía credenciales de cliente por HTTP; una publicación para usuarios necesita HTTPS y otro diseño de acceso.

El execution role obtiene imagen, logs y secreto para arrancar. El task role no tiene permisos adicionales porque la aplicación S16 no llama al SDK de AWS: usa una clave inyectada para Anthropic. KMS propia exige configurar su ARN, permitir el descifrado y tener una key policy compatible.

Los comandos completos están en [la guía](material/S16/guia-alumno.md). Los recibos van a `evidencias/aws/<lab>/`, excluidos de Git. Los recursos no están desplegados por el hecho de existir estas plantillas.

## Costes

```bash
uv run python scripts/costes.py
```

El ejemplo usa tarifas públicas leídas el 17/10/2026 para `eu-west-1` y cantidades declaradas: 0,25 vCPU, 0,5 GB, una IPv4, 0,25 GB de imagen, logs, un secreto y tráfico. Resultado: **13,78 USD/730 h sin inferencia**; **0,46 USD para 90 minutos conservando imagen y secreto un mes**. No son una factura ni un presupuesto autorizado. El archivo JSON permite cambiar cantidades y tarifas, y conserva sus fuentes. La salida facturable presupone que el tramo gratuito global ya se consumió.

## Verificación del proyecto

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run cfn-lint infra/s16/*.json
uv run python scripts/preflight.py
```

Los tests usan transportes simulados y no llaman a modelos ni AWS. Comprueban contratos, cuerpos acotados, errores, modo real sin fallback, destino/propiedad de operaciones y costes. La validación CloudFormation es estática; la creación real requiere permisos, cuota, cuenta y un ensayo propio.

## Navegación del código

| Archivo | Responsabilidad |
|---|---|
| `src/curso_ia/contratos.py` | Entrada, taxonomía, salida y consumo |
| `src/curso_ia/config.py` | Configuración y fallo de arranque si falta un dato real |
| `src/curso_ia/proveedores.py` | Demo y adaptador Anthropic con límite total, sin redirecciones ni reintentos |
| `src/curso_ia/api.py` | HTTP, errores saneados, límite de cuerpo, salud y clasificación |
| `scripts/aws_lab.py` | Operaciones explícitas del laboratorio y recibos |
| `scripts/costes.py` | Cálculo reproducible con cantidades y tarifas |
| `infra/s16/` | Registro y servicio/red/roles en CloudFormation |
| `material/S16/` | Presentación, guion, alumno y cobertura |

El historial se ha iniciado localmente, sin commit, remoto ni publicación. La evidencia de esta preparación y sus límites se conserva en `material/S16/verificacion.md`.

