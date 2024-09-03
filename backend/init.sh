#!/bin/bash
set -euo pipefail

# Instalar dependencias de Python (con caché)
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate


# Crear superusuario
python manage.py shell <<EOF
from django.contrib.auth.models import User
User.objects.create_superuser('avillalba', 'avillalba96@outlook.com', 'SecurePass123')
EOF

# Inicia el servidor de desarrollo de Django
exec python manage.py runserver 0.0.0.0:8000
