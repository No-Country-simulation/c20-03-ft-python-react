#!/bin/bash
set -euo pipefail

# Instala los paquetes de Python y actualiza los existentes según requirements.txt
pip install --upgrade -r requirements.txt

# Ejecuta las migraciones de la base de datos
python manage.py makemigrations
python manage.py migrate

# Inicia el servidor de desarrollo de Django
exec python manage.py runserver 0.0.0.0:8000
