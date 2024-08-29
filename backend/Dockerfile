# Dockerfile para django-back
FROM python:3.12.5-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    musl-dev \
    bash \
    tzdata

# Actualizar pip
RUN pip install --upgrade pip

# Copiar los archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Hacer ejecutable el script init.sh
RUN chmod +x init.sh

# Comando por defecto para ejecutar el script init.sh
CMD ["./init.sh"]

