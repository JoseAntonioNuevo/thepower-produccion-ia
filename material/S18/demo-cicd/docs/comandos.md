# S18 · Comandos en el orden de la presentación

Bash (macOS, Linux o Git Bash). Cada momento de demo tiene dos versiones:

- **GitHub/AWS**: requiere el repositorio publicado y los stacks de [README.md](../README.md),
  pasos 4–7. **Pendiente de ensayo real** a 17/11/2026.
- **Local**: no necesita cuentas; se ejecutó de verdad el 17/11/2026 (Docker 29.9.3, uv 0.13.7).

Variables usadas en la versión GitHub/AWS (valores de ejemplo):

```bash
export AWS_PROFILE=tu-perfil AWS_REGION=eu-north-1 LAB=s18-tu-nombre
export GH_REPO=tu-usuario/thepower-cicd
salida() { aws cloudformation describe-stacks --stack-name "$1" \
  --query "Stacks[0].Outputs[?OutputKey=='$2'].OutputValue" --output text; }
```

## 0. Antes de conectar (no se proyecta)

```bash
cp -R demo-cicd ~/thepower-cicd && cd ~/thepower-cicd   # fuera de cualquier otro repositorio
git init -q -b main && git add -A && git commit -qm "Versión A"
uv sync --locked
docker build -q --provenance=false --build-arg APP_VERSION=version-A -t s18:A .
git switch -qc version-b && git apply cambios/02-version-b.patch && git commit -qam "Versión B"
docker build -q --provenance=false --build-arg APP_VERSION=version-B -t s18:B .
git switch -q main
```

## Diapositiva 9 · El repositorio

```bash
git ls-files
sed -n '1,40p' .github/workflows/comprobaciones.yml
```

## Diapositivas 13–14 · Las comprobaciones, en local

```bash
uv sync --locked
uv export --locked --no-dev --no-emit-project --no-header --format requirements-txt | diff -u requirements.lock -
uv run ruff check . && uv run ruff format --check .
uv run cfn-lint infra/*.yaml
uv run pytest -q                       # 23 passed
```

## Diapositiva 15 · Demo: una PR con un fallo queda bloqueada

GitHub:

```bash
git switch -c respuesta-por-defecto
git apply cambios/01-pr-con-fallo.patch
git commit -qam "Responder algo por defecto si falla el proveedor"
git push -u origin HEAD
gh pr create --fill
gh pr checks --watch                   # termina en rojo
gh pr view --json mergeStateStatus     # BLOCKED
gh pr close --delete-branch && git switch main
```

Local (mismo resultado de tests):

```bash
git switch -c respuesta-por-defecto && git apply cambios/01-pr-con-fallo.patch
uv run pytest -q                       # 2 failed, 21 passed
git checkout -- . && git switch main && git branch -D respuesta-por-defecto
```

## Diapositiva 22 · El `sub` real del token

```bash
gh workflow run diagnostico-oidc.yml --ref main
gh run view "$(gh run list --workflow diagnostico-oidc.yml --limit 1 --json databaseId --jq '.[0].databaseId')" --log | grep -E 'sub:|aud:'
aws iam get-role --role-name "$(salida "$LAB-staging" RolDesplegarArn | cut -d/ -f2)" \
  --query 'Role.AssumeRolePolicyDocument.Statement[0].Condition' --output json
```

## Diapositiva 23 · Demo: publicar desde main y anotar el digest

```bash
gh pr merge NUMERO --squash --delete-branch      # o un push directo en el ensayo
gh run watch "$(gh run list --workflow publicar-main.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
aws ecr describe-images --repository-name "$LAB" \
  --query 'sort_by(imageDetails,&imagePushedAt)[].{commit:imageTags[0],digest:imageDigest,subida:imagePushedAt}' \
  --output table
```

Local (la idea de identidad por contenido):

```bash
docker image inspect --format '{{.Id}}' s18:A s18:B   # dos contenidos, dos identificadores
```

## Diapositiva 28 · Cómo se demuestra un despliegue sin corte

Solo local (no hay balanceador en el laboratorio de AWS y no se crea ninguno). La API de la demo
arranca dos veces (A y B) en 127.0.0.1 detrás de un balanceador mínimo con readiness y drenaje;
peticiones continuas por ese mismo endpoint antes, durante y después. Unos 7 segundos.

```bash
uv run python extras/despliegue_sin_corte.py
# sin corte: 0 fallos → CUMPLE · con corte: ~60 fallos → NO CUMPLE
# la «IP» directa de A falla al pararse A; el smoke posterior contra B sale 200 en los dos
```

## Diapositiva 29 · Demo: desplegar B en staging

```bash
gh workflow run desplegar-staging.yml --ref main -f "digest=$DIGEST_B" -f motivo=despliegue
gh run watch "$(gh run list --workflow desplegar-staging.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
IP="$(bash scripts/ip-staging.sh "$LAB")"
curl -sS "http://$IP:8000/health"
```

Prueba de que la regla del environment bloquea otras ramas (debe fallar antes de pedir credenciales):

```bash
gh workflow run desplegar-staging.yml --ref respuesta-por-defecto -f "digest=$DIGEST_B" -f motivo=despliegue
```

Local:

```bash
docker run --rm -d --name api --read-only --cap-drop ALL -p 127.0.0.1:8000:8000 s18:B
bash scripts/smoke.sh http://127.0.0.1:8000 version-B   # SMOKE CORRECTO
```

## Diapositiva 33 · Demo: del `request_id` a la causa

```bash
BASE="http://$IP:8000"                 # local: BASE=http://127.0.0.1:8000
curl -sS -X POST "$BASE/clasificar" -H 'Content-Type: application/json' \
  -d '{"texto":"Tengo una duda sobre los horarios"}'
# {"error":"error_interno","request_id":"…"}
```

CloudWatch:

```bash
aws logs filter-log-events --log-group-name "/thepower/$LAB" --start-time "$(( ($(date +%s) - 900) * 1000 ))" \
  --filter-pattern '{ $.request_id = "PEGA-EL-REQUEST-ID" }' --query 'events[].message' --output text
```

Local:

```bash
docker logs api 2>&1 | grep PEGA-EL-REQUEST-ID
docker stop api
```

## Diapositiva 35 · Panel, métricas y alarma

Consulta de Logs Insights sobre `/thepower/$LAB`:

```text
filter evento = "peticion" and ruta = "/clasificar"
| stats count() as peticiones, pct(duracion_ms, 95) as p95_ms by version, estado
```

```bash
echo "$(salida "$LAB-staging" Panel)"
aws cloudwatch describe-alarms --alarm-names "$LAB-errores-5xx" \
  --query 'MetricAlarms[0].{estado:StateValue,motivo:StateReason}' --output table
```

## Diapositiva 36 · Demo: rollback al digest anterior

```bash
gh workflow run desplegar-staging.yml --ref main -f "digest=$DIGEST_A" -f motivo=rollback
gh run watch "$(gh run list --workflow desplegar-staging.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
IP="$(bash scripts/ip-staging.sh "$LAB")"
curl -sS -o /dev/null -w '%{http_code}\n' -X POST "http://$IP:8000/clasificar" \
  -H 'Content-Type: application/json' -d '{"texto":"Tengo una duda sobre los horarios"}'   # 200
```

Local (la misma imagen A, sin reconstruir):

```bash
docker run --rm -d --name api --read-only --cap-drop ALL -p 127.0.0.1:8000:8000 s18:A
bash scripts/smoke.sh http://127.0.0.1:8000 version-A
curl -sS -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8000/clasificar \
  -H 'Content-Type: application/json' -d '{"texto":"Tengo una duda sobre los horarios"}'   # 200
docker stop api
```

Arreglar hacia delante:

```bash
git switch version-b && git apply --include='tests/*' cambios/03-test-que-faltaba.patch
uv run pytest -q                       # 1 failed: el test que faltaba
git checkout -- . && git apply cambios/03-test-que-faltaba.patch && uv run pytest -q   # 27 passed
```

## Diapositiva 38 · Migración compatible y restauración

```bash
uv run python extras/migracion_y_restauracion.py
```

## Después de la clase · retirar

Ver [README.md](../README.md), paso 9. Local: `docker rmi s18:A s18:B`.
