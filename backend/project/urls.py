from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions

# Define una clase generadora de esquema personalizada para permitir ambos esquemas
class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # Permitir tanto http como https
        schema.schemes = ["http", "https"]
        return schema

# Define el esquema con el esquema y el host especificados
schema_view = get_schema_view(
    openapi.Info(
        title="eCommerce NoCountry",
        default_version='v1',
        description="Swagger Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="avillalba96@outlook.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=BothHttpAndHttpsSchemaGenerator,  # Usa la clase generadora personalizada
    # url='https://dev.avillalba.com.ar/',  # Forzar el esquema HTTPS
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('postgresql_app.urls')),  # Incluye URLs de postgresql_app
    path('swagger/', schema_view.with_ui(
        'swagger',
        cache_timeout=0
    ), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc',
        cache_timeout=0
    ), name='schema-redoc'),
]
