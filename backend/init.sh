#!/bin/bash
set -euo pipefail

# Imprimir información de conexión de la base de datos
echo "Conectando a la base de datos:"
echo "  HOST: ${DATABASE_HOST}"
echo "  PUERTO: ${DATABASE_PORT}"
echo "  NOMBRE: ${DATABASE_NAME}"
echo "  USUARIO: ${DATABASE_USER}"

# Instalar dependencias de Python (con caché)
pip install -r requirements.txt

# Verificar la conexión a la base de datos
echo "Verificando conexión a la base de datos..."

DB_CHECK=$(python manage.py shell -c "
from django.db import connections;
try:
    connections['default'].cursor()
    print('Conexión a la base de datos exitosa.')
except Exception as e:
    print(f'Error de conexión a la base de datos: {e}')
")

echo "$DB_CHECK"

if [[ "$DB_CHECK" == *"Error de conexión a la base de datos"* ]]; then
  echo "Fallo al conectar con la base de datos. Abortando..."
  exit 1
fi

echo "Conexión a la base de datos verificada correctamente."

# Limpiar todas las entradas de migraciones en la base de datos para todas las aplicaciones
echo "Eliminando entradas de migraciones antiguas para todas las aplicaciones..."
python manage.py dbshell <<EOF
DELETE FROM django_migrations WHERE app != 'auth' AND app != 'contenttypes' AND app != 'sessions' AND app != 'admin';
EOF

# Eliminar las tablas de las aplicaciones para evitar conflictos de "relation already exists"
echo "Eliminando tablas de aplicaciones de usuario para evitar conflictos..."
python manage.py shell -c "
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')
"

# Generar y aplicar migraciones
python manage.py createcachetable
python manage.py collectstatic --noinput --verbosity 2
python manage.py makemigrations
python manage.py migrate --noinput

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
    --log-level 'log'

