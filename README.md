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
- **Despliegue**: Script de despliegue en el proceso de automatización (`deploy_linux.sh`)

### Estructura del Proyecto

La estructura principal del proyecto es la siguiente:

```bash
c20-03-ft-python-react/
│
├── backend/                # Código fuente del backend en Django
├── db/                     # Datos de la base de datos PostgreSQL
├── frontend/               # Código fuente del frontend en Next.js
├── deploy_linux.sh         # Script de despliegue
├── docker-compose_dev.yml  # Configuración general de Docker Compose para la aplicación completa de Desarrollo
├── docker-compose_prod.yml # Configuración general de Docker Compose para la aplicación completa de Producción
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

### Documentación de la API

Para consultar la documentación de la API, puedes utilizar las siguientes herramientas:

- **Swagger UI**: [https://back.avillalba.com.ar/swagger/](https://back.avillalba.com.ar/swagger/)
- **Redoc**: [https://back.avillalba.com.ar/redoc/](https://back.avillalba.com.ar/redoc/)

Estas herramientas te permitirán explorar los endpoints de la API y probar las solicitudes directamente desde tu navegador.

### Generar y Refrescar el Token JWT

Para obtener un token JWT, utiliza el siguiente comando cURL:

```bash
curl -X POST https://back.avillalba.com.ar/api/v1/token/ \
-H "Content-Type: application/json" \
-d '{
    "username": "superadmin",
    "password": "superadminsecret"
}'
```

Esto generará un `access token` que puedes usar para autenticarte en las solicitudes a la API. Incluye este token en la cabecera `Authorization` en el formato `Bearer <access_token>`.

Para refrescar el token, utiliza el siguiente comando cURL:

```bash
curl -X POST https://back.avillalba.com.ar/api/v1/token/refresh/ \
-H "Content-Type: application/json" \
-d '{
    "refresh": "<refresh_token>"
}'
```

Esto generará un nuevo `access token`. Sustituye `<refresh_token>` con el token de refresco que obtuviste al generar el token inicial.

### Crear Superusuario

Para crear un superusuario de Django, sigue estos pasos:

1. **Accede al Contenedor Backend**:

   Si estás utilizando Docker, primero accede al contenedor del backend:

   ```bash
   docker-compose -f docker-compose_backend.yml exec django-back bash -c "python manage.py createsuperuser"
   ```

2. **Introduce la Información del Superusuario**:

   Se te pedirá que introduzcas un nombre de usuario, un correo electrónico y una contraseña para el superusuario. Introduce la información según se te solicite. Por ejemplo:

    ```bash
   Username (leave blank to use 'admin'): admin
   Email address: admin@example.com
   Password: ********
   Password (again): ********
   ```
