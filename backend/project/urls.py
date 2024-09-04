from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Define the schema view with custom security definitions
schema_view = get_schema_view(
    openapi.Info(
        title="eCommerce NoCountry",
        default_version='v1',
        description="Swagger Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="avillalba96@outlook.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # Make Swagger public
    permission_classes=[permissions.AllowAny],  # Allow any access to Swagger
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('postgresql_app.urls')),  # Includes URLs from postgresql_app
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
