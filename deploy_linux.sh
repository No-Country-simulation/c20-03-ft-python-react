#!/bin/bash

# Función para mostrar el manual de uso
mostrar_manual() {
  echo "Uso del script:"
  echo "  $0"
  echo "Este script no requiere argumentos. Utiliza el commit short como tag para Docker."
}

# Variables genéricas
REPO_DIR="/u/docker/c20-03-ft-python-react"  # Actualiza esta variable con la ruta a tu repositorio
COMPOSE_FILE="docker-compose.yml"

# Lista de servicios para construir imágenes
SERVICES=("backend" "frontend")

# 0. Nos movemos al directorio del repositorio
cd $REPO_DIR || { echo "Directorio no encontrado: $REPO_DIR"; exit 1; }

# 1. Guardar cambios locales si hay alguno
if [[ -n $(git status -s) ]]; then
  echo "Guardando cambios locales..."
  git stash push -m "Automated stash $(date +%F_%T)"
fi

# 2. Moverse a la rama main y actualizar
echo "Actualizando repositorio..."
git checkout main
git fetch --all
git pull origin main

# 3. Obtener el commit short para usarlo como tag
COMMIT_SHORT=$(git rev-parse --short HEAD)
IMAGE_TAG="${COMMIT_SHORT}"

# 4. Construir las imágenes y levantar los servicios
for SERVICE in "${SERVICES[@]}"; do
  IMAGE_NAME="${SERVICE}"

  # Verificar si la imagen con el tag específico ya existe
  if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "${IMAGE_NAME}:${IMAGE_TAG}"; then
    echo "La imagen Docker con el tag $IMAGE_TAG ya existe para $SERVICE. No es necesario construirla nuevamente."
  else
    echo "Construyendo la imagen Docker para $SERVICE con tag $IMAGE_TAG..."
    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ./${SERVICE}/

    # Actualizar el archivo docker-compose.yml para usar el nuevo tag
    echo "Actualizando docker-compose.yml para el servicio $SERVICE con el tag $IMAGE_TAG..."
    sed -i "s|image: ${IMAGE_NAME}:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g" $COMPOSE_FILE
  fi
done

# 5. Mostrar logs (opcional)
#docker-compose logs -f

# 6. Levantar los nuevos contenedores
echo "Actualizando contenedores..."
docker-compose up -d

# 7. Limpiar stashes antiguos si hay más de 5
MAX_STASHES=2
STASH_COUNT=$(git stash list | wc -l)
if [ "$STASH_COUNT" -gt "$MAX_STASHES" ]; then
  echo "Limpiando stashes antiguos..."
  git stash list | tail -n +$(($MAX_STASHES + 1)) | while read -r stash; do
    stash_ref=$(echo "$stash" | awk '{print $1}')
    echo "Eliminando stash $stash_ref"
    git stash drop "$stash_ref"
  done
fi

