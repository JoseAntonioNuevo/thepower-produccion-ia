#!/usr/bin/env bash
# Comprobación funcional mínima de una API en marcha: salud, versión y una clasificación.
# La usan el workflow (contra el contenedor recién construido y contra staging) y tú en local.
#   bash scripts/smoke.sh http://127.0.0.1:8000 [version-esperada]
set -euo pipefail

BASE="${1:?Uso: bash scripts/smoke.sh http://host:puerto [version-esperada]}"
ESPERADA="${2:-}"

# 1. Salud: el proceso responde. Reintenta mientras el contenedor termina de arrancar.
# --retry-all-errors cubre también el instante en que el puerto existe y el proceso aún no.
salud="$(curl --fail-with-body -sS --retry 20 --retry-all-errors --retry-delay 2 \
  --connect-timeout 5 --max-time 10 "$BASE/health")"
echo "GET /health -> $salud"
[[ "$(jq -r '.estado' <<<"$salud")" == "ok" ]] || { echo "ERROR: salud incorrecta" >&2; exit 1; }

# 2. Identidad: lo que responde es la versión que queríamos desplegar.
version="$(jq -r '.version' <<<"$salud")"
if [[ -n "$ESPERADA" && "$version" != "$ESPERADA" ]]; then
  echo "ERROR: responde la versión $version y se esperaba $ESPERADA" >&2
  exit 1
fi

# 3. Petición funcional: una incidencia ficticia devuelve una clasificación válida.
resultado="$(curl --fail-with-body -sS --connect-timeout 5 --max-time 40 \
  -X POST "$BASE/clasificar" -H 'Content-Type: application/json' \
  -d '{"texto":"No puedo entrar en mi cuenta ficticia"}')"
echo "POST /clasificar -> $resultado"
jq -e '
  (.resultado.categoria | IN("acceso", "facturacion", "tecnico", "consulta")) and
  (.resultado.prioridad | IN("alta", "media", "baja")) and
  (.resultado.respuesta | type == "string" and length > 0) and
  (.request_id | type == "string" and length > 0)
' <<<"$resultado" >/dev/null || { echo "ERROR: la clasificación no cumple el contrato" >&2; exit 1; }

# 4. Entrada inválida: la API la rechaza con 422 en vez de procesarla.
estado="$(curl -sS -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 \
  -X POST "$BASE/clasificar" -H 'Content-Type: application/json' -d '{"texto":""}')"
echo "POST /clasificar con texto vacío -> $estado"
[[ "$estado" == "422" ]] || { echo "ERROR: se esperaba 422" >&2; exit 1; }

echo "SMOKE CORRECTO: versión $version, modo $(jq -r '.modo' <<<"$salud")"
