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
- **Despliegue**: Script de despliegue en Linux (`deploy_linux.sh`)

### Estructura del Proyecto

La estructura principal del proyecto es la siguiente:

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

### Servicios

El proyecto se compone de los siguientes servicios Docker:

- **db-back**: Servicio de base de datos PostgreSQL.
- **django-back**: Servicio del backend en Django.
- **nextjs-front**: Servicio del frontend en Next.js.

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

### Script de Despliegue

El proyecto incluye un script de despliegue (`deploy_linux.sh`) que automatiza el proceso de despliegue en entornos Linux.

### Variables de Entorno

El proyecto utiliza las siguientes variables de entorno, que deben configurarse antes de ejecutar los servicios:

- `DATABASE_HOST`: Dirección del servidor de base de datos.
- `DATABASE_PORT`: Puerto del servidor de base de datos.
- `DATABASE_NAME`: Nombre de la base de datos.
- `DATABASE_USER`: Usuario de la base de datos.
- `DATABASE_PASSWORD`: Contraseña del usuario de la base de datos.

### Enlaces del Proyecto
- **Repositorio GitHub**: [C20-03-FT-Python-React](https://github.com/No-Country-simulation/c20-03-ft-python-react)
- **Sitio Web**: (pendiente si corresponde)

### Contribuciones

Si deseas contribuir al proyecto, por favor, abre un Pull Request o una Issue en este repositorio.
