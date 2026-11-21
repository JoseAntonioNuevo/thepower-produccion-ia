# S18 · CI/CD y monitorización de una API de IA

Demo de la sesión 18 de AI Engineer (thePower). Una API pequeña de soporte —la de la
sesión 16— con todo lo necesario para entregarla con garantías:

- un cambio con errores **queda bloqueado** en la pull request;
- lo que se despliega es **exactamente la imagen que se probó**, identificada por su digest;
- nadie guarda claves de AWS: GitHub obtiene **credenciales temporales con OIDC**;
- cada petición deja un **log estructurado** con el que se localiza un fallo;
- si la versión nueva falla, se **vuelve a la anterior** reutilizando su digest.

> **Estado de la comprobación (17/11/2026).** Tests, análisis, lock, plantillas, workflows
> (`actionlint`), build de Docker y el recorrido A → B → A están comprobados **en local**.
> La ejecución real en GitHub Actions, ECR y ECS **no se ha ensayado todavía**: los pasos 4 a 9
> están escritos a partir de la documentación oficial y pendientes de ese ensayo.
> Detalle en [`../verificacion.md`](../verificacion.md).

## Qué hay en la carpeta

| Ruta | Qué es |
|---|---|
| `app.py` | La API completa en un archivo: contrato, proveedores, logs y endpoints |
| `tests/test_api.py` | 23 pruebas sin red ni claves (entrada inválida, respuesta válida, fallo del proveedor…) |
| `Dockerfile` · `requirements.lock` | Imagen con base y dependencias fijadas por hash |
| `pyproject.toml` · `uv.lock` | Dependencias exactas y configuración de ruff y pytest |
| `.github/workflows/` | Cinco workflows cortos (tabla siguiente) |
| `infra/` | Dos plantillas de CloudFormation: registro + publicación, y staging |
| `scripts/smoke.sh` | Comprobación funcional: salud, versión, una clasificación y un 422 |
| `scripts/ip-staging.sh` | Lee la IP pública de la tarea de staging |
| `cambios/` | Tres parches para la demo: PR con fallo, versión B y el test que faltaba |
| `extras/` | Ampliación opcional: migración compatible y prueba de restauración con SQLite; demostración local de un despliegue sin corte |
| `docs/` | Guion de clase, comandos en orden y práctica del alumno |

### Los workflows

| Archivo | Cuándo se ejecuta | Qué hace | ¿Credenciales de AWS? |
|---|---|---|---|
| `comprobaciones.yml` | Lo llaman los dos siguientes | Lock, ruff, cfn-lint, pytest, build y smoke del contenedor | No |
| `ci-pr.yml` | Cada pull request hacia `main` | Llama a `comprobaciones.yml` | **No, y no puede pedirlas** |
| `publicar-main.yml` | Cada integración en `main` | Repite las comprobaciones; construye **una** imagen, la publica en ECR y anota el digest | Rol *publicar* (solo ECR) |
| `desplegar-staging.yml` | A mano (`workflow_dispatch`) desde `main` | Despliega un digest ya publicado, sin reconstruir; comprueba salud y petición funcional | Rol *desplegar* (solo este servicio) |
| `diagnostico-oidc.yml` | A mano | Muestra el `sub` y el `aud` reales del token; no toca AWS | No |

Todas las acciones externas están fijadas al SHA completo de 40 caracteres (comprobado con
`gh api` el 17/11/2026):

| Acción | Versión | SHA |
|---|---|---|
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `astral-sh/setup-uv` | v10.3.3 | `68559e99cc807c1eb7e9238fd43a15bba460eec2` |
| `aws-actions/configure-aws-credentials` | v6.3.0 | `e1253824e5c10ff9df46874f81ed3ec929e19cfd` |
| `actions/github-script` | v9.0.0 | `3a2844b7e9c422d3c10d287c895573f7108da1b3` |

## 1. Requisitos

- Python 3.12 y [uv](https://docs.astral.sh/uv/) (la demo se probó con uv 0.13.7).
- Docker, `git`, `curl` y `jq`.
- Para los pasos 4 a 9: una cuenta de GitHub con la CLI `gh` y un proyecto de AWS con la
  CLI `aws`. La región de los ejemplos es **eu-north-1**; usa la de tu proyecto.

Los bloques son Bash (macOS, Linux o Git Bash en Windows).

## 2. Probar la API en local (sin cuenta de nada)

```bash
uv sync --locked            # instala exactamente lo que dice uv.lock
uv run ruff check .         # análisis de código
uv run ruff format --check .
uv run cfn-lint infra/*.yaml
uv run pytest               # 23 pruebas, sin red
```

Arranca la API en modo demo (reglas visibles, sin coste) y pruébala desde otra terminal:

```bash
uv run uvicorn app:crear_app --factory --port 8000 --no-access-log
bash scripts/smoke.sh http://127.0.0.1:8000
```

En la primera terminal aparece una línea JSON por petición. Fíjate en lo que **sí** hay
(`request_id`, `version`, `ruta`, `estado`, `duracion_ms`) y en lo que **no**: el texto de la
incidencia ni ninguna clave.

```json
{"ts": "2026-11-17T09:37:08.011+00:00", "nivel": "INFO", "evento": "peticion", "request_id": "05384e60-…", "version": "desarrollo-local", "metodo": "POST", "ruta": "/clasificar", "estado": 200, "duracion_ms": 1.0, "modo": "demo", "proveedor_ms": 0.0, "categoria": "acceso", "prioridad": "media"}
```

### Configuración local y de staging

La misma imagen sirve para los dos entornos; solo cambia la configuración, que nunca está
en el código:

| Variable | Local | Staging |
|---|---|---|
| `API_MODE` | `demo` (por defecto) o `.env` | Parámetro `ApiMode` de la plantilla |
| `OPENROUTER_MODEL` | `.env` (ver `.env.example`) | Parámetro `ModelId` de la plantilla |
| `OPENROUTER_API_KEY` | `.env`, fuera de Git | **Secrets Manager**; ECS la entrega al arrancar |
| `APP_VERSION` | `desarrollo-local` | Dentro de la imagen: el commit con el que se construyó |

Con `API_MODE=real` y sin clave, la API **no arranca**: es preferible un despliegue que
falla a una API que responde sin poder trabajar.

## 3. La misma comprobación que hará GitHub, con Docker

```bash
docker build --provenance=false --build-arg APP_VERSION=prueba-local -t api:local .
docker run --rm -d --name api --read-only --cap-drop ALL -p 127.0.0.1:8000:8000 api:local
bash scripts/smoke.sh http://127.0.0.1:8000 prueba-local
docker logs api
docker stop api
```

## 4. Tu repositorio en GitHub

Copia esta carpeta **fuera** de cualquier otro repositorio (dentro de otro, `git apply`
ignora los parches sin avisar) y créalo sin subir nada todavía. Un repositorio **público**
permite usar environments, reglas de rama y Actions sin plan de pago.

```bash
cp -R demo-cicd ~/thepower-cicd && cd ~/thepower-cicd
git init -b main && git add -A && git commit -m "Versión A"
gh repo create thepower-cicd --public --source . --remote origin   # todavía sin push
export GH_REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
```

Crea el environment `staging` y permite desplegar **solo desde `main`**. Hace falta porque un
`workflow_dispatch` puede lanzarse desde cualquier rama:

```bash
gh api -X PUT "repos/$GH_REPO/environments/staging" --input - <<'JSON'
{"deployment_branch_policy": {"protected_branches": false, "custom_branch_policies": true}}
JSON
gh api -X POST "repos/$GH_REPO/environments/staging/deployment-branch-policies" \
  -f name=main -f type=branch
```

## 5. AWS, primera parte: registro y rol para publicar

El rol confía en un único valor del `sub` del token de GitHub. Los repositorios creados desde
el 15/07/2026 emiten el formato con identificadores inmutables; calcula el tuyo:

```bash
export AWS_PROFILE=tu-perfil AWS_REGION=eu-north-1 LAB=s18-tu-nombre
PREFIJO="$(gh api "repos/$GH_REPO" --jq '"repo:\(.owner.login)@\(.owner.id)/\(.name)@\(.id)"')"
echo "$PREFIJO"   # p. ej. repo:tu-usuario@1111111/thepower-cicd@2222222 (valores ilustrativos)

aws cloudformation deploy --stack-name "$LAB-registro" \
  --template-file infra/01-registro-y-publicacion.yaml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "Lab=$LAB" "SubPublicar=$PREFIJO:ref:refs/heads/main"
```

Si en tu proyecto ya existe el proveedor `token.actions.githubusercontent.com`, añade
`CrearProveedorOidc=no`. Guarda en GitHub lo que necesitan los workflows; son **variables**,
no secretos: un ARN o un nombre no dan acceso a nada.

```bash
salida() { aws cloudformation describe-stacks --stack-name "$1" \
  --query "Stacks[0].Outputs[?OutputKey=='$2'].OutputValue" --output text; }
gh variable set AWS_REGION --body "$AWS_REGION"
gh variable set ECR_REPOSITORY --body "$LAB"
gh variable set AWS_ROLE_PUBLICAR --body "$(salida "$LAB-registro" RolPublicarArn)"
```

## 6. Primera publicación: la versión A

```bash
git push -u origin main
gh run watch "$(gh run list --workflow publicar-main.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
```

`Publicar · main` repite las comprobaciones, construye la imagen, la prueba, la sube y
escribe el **digest** en el resumen de la ejecución. También puedes leerlo en ECR:

```bash
DIGEST_A="$(aws ecr describe-images --repository-name "$LAB" \
  --image-ids "imageTag=$(git rev-parse HEAD)" --query 'imageDetails[0].imageDigest' --output text)"
echo "$DIGEST_A"
```

Si el paso de credenciales falla con *Not authorized to perform sts:AssumeRoleWithWebIdentity*,
el `sub` no coincide. Lanza `Diagnóstico · OIDC` (`gh workflow run diagnostico-oidc.yml`),
copia el prefijo `repo:…` real y actualiza el stack. No sustituyas la igualdad por un comodín.

## 7. AWS, segunda parte: staging

```bash
gh workflow run diagnostico-oidc.yml          # anota el «sub» real del environment
CUENTA="$(aws sts get-caller-identity --query Account --output text)"
MI_IP="$(curl -4fsS https://checkip.amazonaws.com)"

aws cloudformation deploy --stack-name "$LAB-staging" \
  --template-file infra/02-staging.yaml --capabilities CAPABILITY_IAM \
  --parameter-overrides "Lab=$LAB" "AllowedCidr=$MI_IP/32" \
    "ImageUri=$CUENTA.dkr.ecr.$AWS_REGION.amazonaws.com/$LAB@$DIGEST_A" \
    "SubDesplegar=$PREFIJO:environment:staging"

gh variable set ECS_CLUSTER --env staging --body "$(salida "$LAB-staging" Cluster)"
gh variable set ECS_SERVICE --env staging --body "$(salida "$LAB-staging" Service)"
gh variable set ECS_SECURITY_GROUP --env staging --body "$(salida "$LAB-staging" SecurityGroup)"
gh variable set AWS_ROLE_DESPLEGAR --env staging --body "$(salida "$LAB-staging" RolDesplegarArn)"

bash scripts/smoke.sh "http://$(bash scripts/ip-staging.sh "$LAB"):8000" "$(git rev-parse HEAD)"
```

La plantilla crea una red propia, un servicio Fargate de una tarea (0,25 vCPU y 0,5 GB), el
grupo de logs con 7 días de retención, tres métricas extraídas de los logs, un panel, una
alarma y el rol de despliegue. No hay balanceador, NAT ni base de datos. El puerto 8000 solo
admite tu IP; el workflow añade la del runner durante el smoke y la retira al terminar.

Por último, exige en GitHub que la PR pase las comprobaciones antes de integrarse:
**Settings → Rules → Rulesets → New branch ruleset**, rama `main`, activa *Require a pull
request before merging* y *Require status checks to pass* con el check
`comprobaciones / Lock, análisis, tests e imagen` (aparece en la lista después de la
primera PR).

## 8. El recorrido de la clase

### 8.1 Una PR con un fallo queda bloqueada

```bash
git switch -c respuesta-por-defecto
git apply cambios/01-pr-con-fallo.patch
git commit -am "Responder algo por defecto si falla el proveedor"
git push -u origin HEAD && gh pr create --fill && gh pr checks --watch
```

El cambio parece razonable, pero inventa una respuesta cuando el proveedor falla. Dos tests
lo detectan y la PR no se puede integrar. No ha recibido ninguna credencial de AWS.
Ciérrala: `gh pr close --delete-branch`.

### 8.2 La versión B se valida, se publica y se despliega

```bash
git switch main && git switch -c plazo-de-atencion
git apply cambios/02-version-b.patch
git commit -am "Añadir el plazo de atención (versión B)"
git push -u origin HEAD && gh pr create --fill && gh pr checks --watch
gh pr merge --squash --delete-branch && git switch main && git pull
```

Al integrar, `Publicar · main` deja el digest de B. Despliégalo **sin reconstruir**:

```bash
DIGEST_B="$(aws ecr describe-images --repository-name "$LAB" \
  --image-ids "imageTag=$(git rev-parse HEAD)" --query 'imageDetails[0].imageDigest' --output text)"
gh workflow run desplegar-staging.yml --ref main -f "digest=$DIGEST_B" -f motivo=despliegue
```

El workflow comprueba que el digest existe y lleva la etiqueta de un commit, registra una
definición de tarea idéntica salvo por la imagen, espera a que ECS sustituya la tarea sin
corte, confirma qué digest está en marcha y ejecuta el smoke contra la API real.

### 8.3 Un fallo que los tests no cubrían

Todo está en verde, y sin embargo:

```bash
IP="$(bash scripts/ip-staging.sh "$LAB")"
curl -sS -X POST "http://$IP:8000/clasificar" -H 'Content-Type: application/json' \
  -d '{"texto":"Tengo una duda sobre los horarios"}'
# {"error":"error_interno","request_id":"…"}
```

B calcula el plazo con un diccionario al que le falta la prioridad `baja`. El cliente solo
recibe un `request_id`; con él se encuentra la causa en CloudWatch:

```bash
aws logs filter-log-events --log-group-name "/thepower/$LAB" \
  --filter-pattern '{ $.request_id = "PEGA-AQUI-EL-REQUEST-ID" }' \
  --query 'events[].message' --output text
```

Aparecen dos líneas: `excepcion` (con `error_tipo: KeyError` y la traza) y `peticion` (con
`estado: 500` y la `version`, que es el commit de B). El panel (`Panel` en las salidas del
stack) muestra el error y la latencia, y la alarma `…-errores-5xx` cambia de estado.

Consulta de Logs Insights para comparar versiones:

```text
filter evento = "peticion" and ruta = "/clasificar"
| stats count() as peticiones, pct(duracion_ms, 95) as p95_ms by version, estado
```

### 8.4 Rollback: el mismo workflow con el digest anterior

```bash
gh workflow run desplegar-staging.yml --ref main -f "digest=$DIGEST_A" -f motivo=rollback
```

No se reconstruye ni se revierte ningún commit: se vuelve a ejecutar la imagen A que ya se
validó. Después se repite la petición que fallaba y debe responder 200.

### 8.5 Arreglar hacia delante

El rollback gana tiempo; el arreglo es otra PR con el test que faltaba:

```bash
git switch -c plazo-para-todas-las-prioridades
git apply cambios/03-test-que-faltaba.patch      # test + corrección
```

Para ver el test en rojo antes del arreglo: `git apply --include='tests/*' cambios/03-test-que-faltaba.patch`.

## 9. Retirar tus recursos

```bash
aws cloudformation delete-stack --stack-name "$LAB-staging"
aws cloudformation wait stack-delete-complete --stack-name "$LAB-staging"
# Las definiciones de tarea que registró el workflow no pertenecen al stack:
for d in $(aws ecs list-task-definitions --family-prefix "$LAB" --query 'taskDefinitionArns' --output text); do
  aws ecs deregister-task-definition --task-definition "$d" --query 'taskDefinition.status' --output text
done
# Un registro con imágenes no se puede borrar: primero se vacía.
aws ecr batch-delete-image --repository-name "$LAB" \
  --image-ids "$(aws ecr list-images --repository-name "$LAB" --query 'imageIds' --output json)"
aws cloudformation delete-stack --stack-name "$LAB-registro"
aws cloudformation wait stack-delete-complete --stack-name "$LAB-registro"
aws cloudformation describe-stacks --stack-name "$LAB-staging"   # debe decir que no existe
```

Si el proveedor OIDC lo creó este stack, se elimina con él; no lo borres si lo comparten
otros proyectos. En GitHub puedes borrar el environment o el repositorio cuando quieras.

## Plan para proteger los datos

La práctica no necesita base de datos. Si tu API la tuviera, este es el plan mínimo.

### Despliegue progresivo

| Estrategia | Qué hace | Cuándo usarla |
|---|---|---|
| **Rolling** (la de esta demo) | Arranca tareas nuevas, espera a que estén sanas y para las antiguas | Servicio pequeño; el *circuit breaker* de ECS deshace el cambio si la tarea no arranca |
| **Blue/green** | Dos entornos completos; se prueba el nuevo y se cambia el tráfico de una vez | Cuando hay que validar antes de recibir usuarios y volver atrás al instante |
| **Canary** | Un porcentaje pequeño de tráfico real va a la versión nueva; si va bien, el resto | Cambios de riesgo con métricas fiables de error y latencia |
| **Lineal** | El tráfico se mueve en incrementos iguales | Cuando se quiere observar cada escalón |

Blue/green, canary y lineal existen como estrategias nativas de ECS, pero necesitan un
balanceador (o Service Connect) que reparta el tráfico; esta demo no lo tiene. Plan para
producción: empezar con canary del 10 %, vigilar errores 5xx y p95 durante unos minutos,
continuar solo si no empeoran y volver al digest anterior en cuanto salte la alarma.

**Cómo se demuestra que no hay corte.** Con peticiones continuas por el mismo endpoint estable
(en producción, un balanceador como el ALB) antes, durante y después del cambio, y cero
respuestas fallidas en las tres fases. La IP pública de la tarea de este laboratorio cambia en
cada despliegue y el smoke se ejecuta al terminar: prueban que B funciona, no que el cambio no
cortó. `extras/despliegue_sin_corte.py` lo enseña en local, sin AWS ni cambios en la API: un
balanceador mínimo con readiness (B solo recibe tráfico tras responder `/health`) y drenaje (A
termina sus peticiones antes de pararse) frente a parar A y arrancar B.

```bash
uv run python extras/despliegue_sin_corte.py   # sin corte: 0 fallos · con corte: ~60 fallos
```

### Cambios de base de datos compatibles con la versión anterior

Durante un despliegue conviven la versión antigua y la nueva, y un rollback vuelve a poner
la antigua. Por eso cada cambio de esquema debe funcionar con **las dos**:

1. **Expand**: añadir lo nuevo sin quitar nada (columna opcional, tabla nueva).
2. **Migrar**: desplegar el código que escribe en lo nuevo y rellenar los datos antiguos.
3. **Contract**: retirar lo viejo solo cuando ninguna versión desplegable lo usa.

Renombrar o borrar una columna en un solo paso rompe a la versión anterior. Y **volver a
una imagen antigua no revierte una migración**: los datos escritos por B siguen ahí.

### Copias de seguridad con prueba de restauración

- Copias automáticas con retención definida (en RDS, entre 0 y 35 días; 0 las desactiva) y
  una copia manual antes de cada migración.
- Dos números acordados: cuántos datos se pueden perder (RPO) y cuánto se tarda en volver (RTO).
- **Restaurar de verdad**, de forma periódica, en una base nueva: comprobar integridad,
  número de filas y una consulta funcional. En RDS, restaurar a un punto en el tiempo crea
  una instancia nueva y no modifica la original.
- Anotar fecha, duración y resultado de cada prueba. Una copia nunca restaurada es una hipótesis.

`extras/migracion_y_restauracion.py` demuestra las tres ideas con SQLite y datos ficticios,
sin tocar la API ni AWS:

```bash
uv run python extras/migracion_y_restauracion.py
```

## Más documentación

- [Guion de la clase](docs/guion-clase.md) · [Comandos en orden](docs/comandos.md) ·
  [Práctica opcional](docs/ejercicio.md)
