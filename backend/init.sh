#!/bin/bash
set -euo pipefail

# Instalar dependencias de Python (con caché)
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

# Inicia el servidor de desarrollo de Django
exec python manage.py runserver 0.0.0.0:8000
