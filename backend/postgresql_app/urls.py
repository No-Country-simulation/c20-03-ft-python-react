from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Rutas existentes
    path('v1/register/', views.register_user, name='register_user'),
    path('v1/register/admin/', views.register_admin, name='register_admin'),
    path('v1/users/', views.list_users, name='list_users'),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/products/', views.list_products, name='list_products'),
    path('v1/products/add/', views.create_product, name='create_product'),
    path('v1/products/<int:pk>/', views.product_detail, name='product_detail'),
    path('v1/products/<int:product_id>/variants/<str:size>/', views.product_variant_detail, name='product_variant_detail'),
    path('v1/cart/add/', views.add_to_cart, name='add_to_cart'),
    path('v1/cart/', views.view_cart, name='view_cart'),
    path('v1/cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('v1/purchase-history/', views.view_purchase_history, name='view_purchase_history'),
]
