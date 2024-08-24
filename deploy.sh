#!/bin/bash

# Variables genéricas
REPO_DIR="/u/docker/c20-03-ft-python-react"

# 0. Nos movemos al directorio del repositorio
cd $REPO_DIR || { echo "Directorio no encontrado: $REPO_DIR"; exit 1; }

# 1. Moverse a la rama main/deploy y actualizar
echo "Actualizando repositorio..."
git checkout deploy
git fetch --all
git pull origin deploy

# 2. Construir la imagen Docker (sin tag)
echo "Construyendo la imagen Docker..."
docker-compose build

# 3. Detener y eliminar contenedores
echo "Deteniendo y eliminando contenedores..."
docker-compose down -v

# 4. Levantar los contenedores
echo "Levantando contenedores..."
docker-compose up -d

# 5. Mostrar logs (opcional)
#docker-compose logs -f
