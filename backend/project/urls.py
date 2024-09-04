from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.utils.deprecation import MiddlewareMixin

# Middleware para ajustar el esquema y host según la solicitud
class SchemaHostMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, 'scheme') and hasattr(request, 'get_host'):
            request.schema = request.scheme
            request.host = request.get_host()

# Define el esquema con configuración dinámica
def get_schema_view_func():
    return get_schema_view(
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
        url=None,  # Usa el esquema actual de la solicitud
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('postgresql_app.urls')),
    path('swagger/', get_schema_view_func().with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', get_schema_view_func().with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
