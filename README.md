# C20-03-FT-Python-React

## Industria: E-commerce

### Descripción
Este proyecto es una aplicación web de e-commerce que combina un backend desarrollado en Django y un frontend en Next.js. La arquitectura está basada en contenedores Docker, lo que permite una fácil configuración y despliegue tanto en entornos de desarrollo como de producción.

### Colaboradores
- **Lucas Catriel Ballesteros** - [LinkedIn](https://www.linkedin.com/) - **Backend Developer**
- **Maira Zamer** - [LinkedIn](https://www.linkedin.com/in/maira-zamer/) - **Frontend Developer**
- **Alejo Colazurda** - [LinkedIn](https://www.linkedin.com/in/alejo-colazurda/) - **Frontend Developer**
- **Vicente Soto** - [LinkedIn](https://www.linkedin.com/in/vicentesotoarriagada/) - **Frontend Developer**
- **Alejandro Villalba** - [LinkedIn](https://www.linkedin.com/in/avillalba96/) - **DevOps Engineer**

### Tecnologías Utilizadas
- **Backend**: Django
- **Frontend**: Next.js
- **Base de Datos**: PostgreSQL
- **Contenedorización**: Docker, Docker Compose
- **Despliegue**: Script de despliegue en el proceso de automatizacion (`deploy_linux.sh`)

### Estructura del Proyecto

La estructura principal del proyecto es la siguiente:

```
c20-03-ft-python-react/
│
├── backend/                # Código fuente del backend en Django
├── db/                     # Datos de la base de datos PostgreSQL
├── frontend/               # Código fuente del frontend en Next.js
├── deploy_linux.sh         # Script de despliegue
├── docker-compose_dev.yml      # Configuración general de Docker Compose para la aplicación completa de Develop
├── docker-compose_prod.yml      # Configuración general de Docker Compose para la aplicación completa de Produccion
├── docker-compose_backend.yml  # Configuración específica para el backend y base de datos
├── docker-compose_frontend.yml  # Configuración específica para el frontend
└── README.md               # Este archivo
```

### Servicios

El proyecto se compone de los siguientes servicios Docker:

- **db-back**: Servicio de base de datos PostgreSQL.
- **django-back**: Servicio del backend en Django.
- **nextjs-front**: Servicio del frontend en Next.js.

### Endpoints Públicos

#### Entorno de Producción (main)
- **Frontend**: [https://front.avillalba.com.ar/](https://front.avillalba.com.ar/)
- **Backend**: [https://back.avillalba.com.ar/](https://back.avillalba.com.ar/)

#### Entorno de Desarrollo (develop)
- **Frontend**: [https://front-dev.avillalba.com.ar/](https://front-dev.avillalba.com.ar/)
- **Backend**: [https://back-dev.avillalba.com.ar/](https://back-dev.avillalba.com.ar/)

### Endpoints Locales

Para probar localmente, utiliza los siguientes endpoints:

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend**: [http://localhost:8000](http://localhost:8000)

### Instrucciones de Uso

#### Despliegue Local

Para desplegar la aplicación localmente, ejecuta:

```bash
docker-compose up --build
```

Esto iniciará todos los servicios: base de datos, backend y frontend.

#### Despliegue de Backend

Para desplegar solo el backend y la base de datos:

```bash
docker-compose -f docker-compose_backend.yml up --build
```

#### Despliegue de Frontend

Para desplegar solo el frontend:

```bash
docker-compose -f docker-compose_frontend.yml up --build
```

### Variables de Entorno

El proyecto utiliza las siguientes variables de entorno, que deben configurarse antes de ejecutar los servicios:

- `DATABASE_HOST`: Dirección del servidor de base de datos.
- `DATABASE_PORT`: Puerto del servidor de base de datos.
- `DATABASE_NAME`: Nombre de la base de datos.
- `DATABASE_USER`: Usuario de la base de datos.
- `DATABASE_PASSWORD`: Contraseña del usuario de la base de datos.
