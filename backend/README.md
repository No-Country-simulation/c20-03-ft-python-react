# README.md

## Tutorial

1. Solo es machete de ejemplo

```bash
rm -r backend/postgresql_app/migrations

docker exec -it db-back bash
psql -h localhost -p 5432 -U user_nocountry -d db_nocountry
DELETE FROM django_migrations WHERE app = 'postgresql_app';
\dt

docker exec -it django-back bash
python manage.py makemigrations postgresql_app
python manage.py migrate
```
