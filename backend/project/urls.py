from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from django.conf import settings
import os

# Define a custom schema generator class to allow both HTTP and HTTPS
class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # Allow both HTTP and HTTPS
        schema.schemes = ["http", "https"]
        return schema

# Define the base URL for Swagger based on the environment
swagger_base_url = os.environ.get('SWAGGER_BASE_URL', 'http://localhost:8000')

# Define the schema with the specified scheme and host
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
    generator_class=BothHttpAndHttpsSchemaGenerator,  # Use the custom generator class
    url=swagger_base_url,  # Set URL based on the environment
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('postgresql_app.urls')),  # Include URLs from postgresql_app
    path('swagger/', schema_view.with_ui(
        'swagger',
        cache_timeout=0
    ), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc',
        cache_timeout=0
    ), name='schema-redoc'),
]
