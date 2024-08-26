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

# 1. Moverse a la rama deploy y actualizar
echo "Actualizando repositorio..."
git checkout main
git fetch --all
git pull origin main

# 2. Obtener el commit short para usarlo como tag
COMMIT_SHORT=$(git rev-parse --short HEAD)
IMAGE_TAG="${COMMIT_SHORT}"

# 3. Construir las imágenes y levantar los servicios
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

# 4. Mostrar logs (opcional)
#docker-compose logs -f

# 5. Levantar los nuevos contenedores
echo "Actualizando contenedores..."
docker-compose up -d
