#!/bin/bash
set -euo pipefail

# Print database connection information
echo "Connecting to the database:"
echo "  HOST: ${DATABASE_HOST}"
echo "  PORT: ${DATABASE_PORT}"
echo "  NAME: ${DATABASE_NAME}"
echo "  USER: ${DATABASE_USER}"

# Install Python dependencies (with cache)
pip install -r requirements.txt

# Verify the database connection
echo "Verifying database connection..."

DB_CHECK=$(python manage.py shell -c "
from django.db import connections;
try:
    connections['default'].cursor()
    print('Database connection successful.')
except Exception as e:
    print(f'Database connection error: {e}')
")

echo "$DB_CHECK"

if [[ "$DB_CHECK" == *"Database connection error"* ]]; then
  echo "Failed to connect to the database. Aborting..."
  exit 1
fi

echo "Database connection verified successfully."

# Generate and apply migrations
python manage.py createcachetable
python manage.py collectstatic --noinput --verbosity 2
python manage.py makemigrations postgresql_app
python manage.py migrate --noinput

# Create 'admin' and 'user' groups if they don't exist
python manage.py shell -c "
from django.contrib.auth.models import Group;
Group.objects.get_or_create(name='admin');
Group.objects.get_or_create(name='user');
"

# Start Nginx in the background
nginx &

# Start Gunicorn with environment variables
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
