# c20-03-ft-python-react

Este proyecto es una aplicación web que combina un backend desarrollado en Django y un frontend desarrollado en Next.js. La arquitectura está basada en contenedores Docker, lo que permite una fácil configuración y despliegue del entorno de desarrollo y producción.

## Estructura del Proyecto

La estructura principal del proyecto es la siguiente :

```
c20-03-ft-python-react/
│
├── backend/                # Código fuente del backend en Django
├── db/                     # Datos de la base de datos PostgreSQL
├── frontend/               # Código fuente del frontend en Next.js
├── deploy_linux.sh         # Script de despliegue
├── docker-compose.yml      # Configuración general de Docker Compose para la aplicación completa
├── docker-compose_backend.yml  # Configuración específica para el backend y base de datos
├── docker-compose_frontend.yml  # Configuración específica para el frontend
└── README.md               # Este archivo
```

## Servicios

El proyecto se compone de los siguientes servicios Docker:

- **db-back**: Servicio de base de datos PostgreSQL.
- **django-back**: Servicio del backend en Django.
- **nextjs-front**: Servicio del frontend en Next.js.

### `docker-compose.yml`

Este archivo define los servicios completos de la aplicación, incluyendo la base de datos, el backend, y el frontend.

### `docker-compose_backend.yml`

Este archivo está enfocado en el backend y la base de datos, permitiendo la construcción de la imagen del backend desde el contexto `./backend` y utilizando un Dockerfile personalizado.

### `docker-compose_frontend.yml`

Este archivo está enfocado en el frontend, permitiendo la construcción de la imagen del frontend desde el contexto `./frontend` y utilizando un Dockerfile personalizado.

## Uso

### Despliegue Local

Para desplegar la aplicación localmente, puedes usar el siguiente comando con el archivo `docker-compose.yml`:

```bash
docker-compose up --build
```

Esto iniciará todos los servicios: base de datos, backend y frontend.

### Despliegue de Backend

Para desplegar solo el backend y la base de datos, puedes utilizar el archivo `docker-compose_backend.yml`:

```bash
docker-compose -f docker-compose_backend.yml up --build
```

### Despliegue de Frontend

Para desplegar solo el frontend, puedes utilizar el archivo `docker-compose_frontend.yml`:

```bash
docker-compose -f docker-compose_frontend.yml up --build
```

### Script de Despliegue

El proyecto incluye un script de despliegue (`deploy_linux.sh`) que puede ser utilizado para automatizar el proceso de despliegue en entornos Linux.

## Variables de Entorno

El proyecto utiliza las siguientes variables de entorno, que deben ser configuradas antes de ejecutar los servicios:

- `DATABASE_HOST`: Dirección del servidor de base de datos.
- `DATABASE_PORT`: Puerto del servidor de base de datos.
- `DATABASE_NAME`: Nombre de la base de datos.
- `DATABASE_USER`: Usuario de la base de datos.
- `DATABASE_PASSWORD`: Contraseña del usuario de la base de datos.

## Requisitos

- Docker
- Docker Compose

## Contribuciones

Si deseas contribuir al proyecto, por favor, abre un Pull Request o una Issue en este repositorio.
