#!/bin/bash

# Función para mostrar el manual de uso
mostrar_manual() {
  echo "Uso del script:"
  echo "  $0 [rama] [archivo-compose] [directorio-repo]"
  echo "Este script acepta tres argumentos opcionales:"
  echo "  1. Rama de Git (por defecto 'main')."
  echo "  2. Archivo docker-compose (por defecto 'docker-compose.yml')."
  echo "  3. Directorio del repositorio (por defecto '/u/docker/examples/c20-03-ft-python-react')."
}

# Obtener la rama, el archivo compose y el directorio del repositorio como argumentos o usar valores por defecto
BRANCH=${1:-main}
COMPOSE_FILE=${2:-docker-compose.yml}
REPO_DIR=${3:-/u/docker/examples}

# 0. Nos movemos al directorio del repositorio
cd "$REPO_DIR" || { echo "Directorio no encontrado: $REPO_DIR"; exit 1; }

# 1. Guardar cambios locales si hay alguno
if [[ -n $(git status -s) ]]; then
  echo "Guardando cambios locales..."
  git stash push -m "Automated stash $(date +%F_%T)"
fi

# 2. Moverse a la rama especificada y actualizar
echo "Actualizando repositorio en la rama $BRANCH..."
git checkout $BRANCH
git fetch --all
git pull origin $BRANCH

# 3. Obtener el commit short para usarlo como tag
COMMIT_SHORT=$(git rev-parse --short HEAD)
IMAGE_TAG="${BRANCH}-${COMMIT_SHORT}"

# 4. Lista de servicios para construir imágenes
SERVICES=("backend" "frontend")

# 5. Construir las imágenes y levantar los servicios
for SERVICE in "${SERVICES[@]}"; do
  IMAGE_NAME="${SERVICE}-${BRANCH}"

  # Verificar si la imagen con el tag específico ya existe
  if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "${IMAGE_NAME}:${IMAGE_TAG}"; then
    echo "La imagen Docker con el tag $IMAGE_TAG ya existe para $SERVICE. No es necesario construirla nuevamente."
  else
    echo "Construyendo la imagen Docker para $SERVICE con tag $IMAGE_TAG..."
    docker build --no-cache -t "${IMAGE_NAME}:${IMAGE_TAG}" "./${SERVICE}/"
    sleep 10

    # Actualizar el archivo docker-compose.yml para usar el nuevo tag
    echo "Actualizando $COMPOSE_FILE para el servicio $SERVICE con el tag $IMAGE_TAG..."
    sed -i "s|image: ${IMAGE_NAME}:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g" "$COMPOSE_FILE"
    sleep 10
  fi
done

# 6. Bajar los contenedores existentes y eliminar volúmenes
echo "Deteniendo contenedores y eliminando volúmenes..."
docker-compose -f "$COMPOSE_FILE" down -v

# 7. Reconstruir los contenedores y levantar los nuevos contenedores
echo "Reconstruyendo y actualizando contenedores..."
docker-compose -f "$COMPOSE_FILE" build --no-cache
docker-compose -f "$COMPOSE_FILE" up -d

# 8. Limpiar stashes antiguos si hay más de 2
MAX_STASHES=2
STASH_COUNT=$(git stash list | wc -l)
if [ "$STASH_COUNT" -gt "$MAX_STASHES" ]; then
  echo "Limpiando stashes antiguos..."
  git stash list | tail -n +$(($MAX_STASHES + 1)) | while read -r stash; do
    stash_ref=$(echo "$stash" | awk '{print $1}' | sed 's/://')
    if [[ "$stash_ref" =~ ^stash@{[0-9]+}$ ]]; then
      echo "Eliminando stash $stash_ref"
      git stash drop "$stash_ref" || echo "No se pudo eliminar el stash $stash_ref"
    else
      echo "Referencia de stash inválida: $stash_ref"
    fi
  done
fi

