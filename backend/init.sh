#!/bin/bash
set -euo pipefail

# Instalar dependencias de Python (con caché)
pip install -r requirements.txt

# Realizar migraciones y recopilar archivos estáticos
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Crear grupos 'admin' y 'user' si no existen
python manage.py shell -c "
from django.contrib.auth.models import Group;
Group.objects.get_or_create(name='admin');
Group.objects.get_or_create(name='user');
"

# Iniciar Nginx en segundo plano
nginx &

# Iniciar Gunicorn con variables de entorno
exec gunicorn --bind 0.0.0.0:8000 project.wsgi:application \
    --workers ${GUNICORN_WORKERS:-4} \
    --threads ${GUNICORN_THREADS:-2} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --keep-alive ${GUNICORN_KEEP_ALIVE:-5} \
    --max-requests ${GUNICORN_MAX_REQUESTS:-1000} \
    --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER:-50} \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level 'info'
