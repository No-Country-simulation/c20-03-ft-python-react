#!/bin/bash

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# Crear superusuario
echo "Creando superusuario..."
python /app/create_superuser.py

# Iniciar el servidor de desarrollo
echo "Iniciando el servidor Django..."
python manage.py runserver 0.0.0.0:8000

