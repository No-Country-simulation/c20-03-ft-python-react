# Definir variables
$REPO_DIR = "C:\ruta\a\tu\repositorio"
$COMPOSE_FILE = "docker-compose.yml"
$SERVICES = @("backend", "frontend")

# Cambiar al directorio del repositorio
Set-Location -Path $REPO_DIR

# Obtener el commit short para usarlo como tag
$COMMIT_SHORT = & git rev-parse --short HEAD
$IMAGE_TAG = $COMMIT_SHORT

# Construir imágenes y levantar servicios
foreach ($SERVICE in $SERVICES) {
    $IMAGE_NAME = $SERVICE

    # Verificar si la imagen con el tag específico ya existe
    $imageExists = docker images --format "{{.Repository}}:{{.Tag}}" | Select-String -Pattern "$IMAGE_NAME:$IMAGE_TAG"
    if ($imageExists) {
        Write-Output "La imagen Docker con el tag $IMAGE_TAG ya existe para $SERVICE. No es necesario construirla nuevamente."
    } else {
        Write-Output "Construyendo la imagen Docker para $SERVICE con tag $IMAGE_TAG..."
        docker build -t "$IMAGE_NAME:$IMAGE_TAG" .\$SERVICE

        # Actualizar el archivo docker-compose.yml para usar el nuevo tag
        Write-Output "Actualizando docker-compose.yml para el servicio $SERVICE con el tag $IMAGE_TAG..."
        (Get-Content $COMPOSE_FILE) -replace "image: $IMAGE_NAME:.*", "image: $IMAGE_NAME:$IMAGE_TAG" | Set-Content $COMPOSE_FILE
    }
}

# Levantar los nuevos contenedores
Write-Output "Actualizando contenedores..."
docker-compose up -d

