from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('v1/register/', views.register_user, name='register_user'),
    path('v1/register/admin/', views.register_admin, name='register_admin'),
    path('v1/users/', views.list_users, name='list_users'),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/products/', views.list_products, name='list_products'),
    path('v1/products/add/', views.create_product, name='create_product'),
    path('v1/products/<int:pk>/', views.product_detail, name='product_detail'),
    path('v1/products/<int:product_id>/variants/<str:size>/', views.product_variant_detail, name='product_variant_detail'),  # Nueva ruta
]
