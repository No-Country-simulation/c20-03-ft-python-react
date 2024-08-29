#!/bin/bash

# Verifica si se proporcionó un argumento
if [ $# -eq 0 ]; then
  echo "No se proporcionó nombre de la rama. Uso: $0 <nombre-de-la-rama>"
  exit 1
fi

BRANCH_NAME=$1
COMPOSE_FILE=$2

echo "Nombre de la rama: $BRANCH_NAME"
echo "Nombre del compose a usar: $COMPOSE_FILE"
