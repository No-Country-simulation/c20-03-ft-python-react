#!/bin/bash

# Función para mostrar el manual de uso
mostrar_manual() {
  echo "Uso del script:"
  echo "  $0 [rama] [archivo-compose] [directorio-repo] [credenciales-git]"
  echo "Este script acepta cuatro argumentos opcionales:"
  echo "  1. Rama de Git (por defecto 'main')."
  echo "  2. Archivo docker-compose (por defecto 'docker-compose.yml')."
  echo "  3. Directorio del repositorio (por defecto '/u/docker/examples/c20-03-ft-python-react')."
  echo "  4. Clave SSH de Git (opcional)."
}

# Obtener la rama, el archivo compose, el directorio del repositorio y las credenciales como argumentos o usar valores por defecto
BRANCH=${1:-main}
COMPOSE_FILE=${2:-docker-compose.yml}
REPO_DIR=${3:-/u/docker/examples}
GIT_CREDENTIALS=${4:-}

# Si se pasa la clave SSH, usarla
if [[ -n "$GIT_CREDENTIALS" ]]; then
  echo "Usando credenciales SSH: $GIT_CREDENTIALS"
  export GIT_SSH_COMMAND="ssh -i $HOME/.ssh/$GIT_CREDENTIALS -o StrictHostKeyChecking=no"
fi

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
docker-compose -f "$COMPOSE_FILE" up -d

# 8. Limpiar stashes antiguos si hay más de 2
echo "Eliminando todos los stashes existentes..."
git stash clear
echo "Todos los stashes han sido eliminados."
