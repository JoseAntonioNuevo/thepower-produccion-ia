#!/usr/bin/env bash
# Muestra la IP pública de la tarea de staging en marcha. Solo lee; no cambia nada.
# La IP cambia en cada despliegue porque ECS arranca una tarea nueva.
#   bash scripts/ip-staging.sh s18-tu-nombre
set -euo pipefail

LAB="${1:?Uso: bash scripts/ip-staging.sh nombre-del-laboratorio}"

TAREA="$(aws ecs list-tasks --cluster "$LAB" --service-name "$LAB" \
  --desired-status RUNNING --query 'taskArns[0]' --output text)"
[[ "$TAREA" == arn:* ]] || { echo "ERROR: el servicio $LAB no tiene tareas en marcha" >&2; exit 1; }

INTERFAZ="$(aws ecs describe-tasks --cluster "$LAB" --tasks "$TAREA" --output json \
  | jq -r '[.tasks[0].attachments[].details[] | select(.name == "networkInterfaceId") | .value] | first')"

aws ec2 describe-network-interfaces --network-interface-ids "$INTERFAZ" \
  --query 'NetworkInterfaces[0].Association.PublicIp' --output text
