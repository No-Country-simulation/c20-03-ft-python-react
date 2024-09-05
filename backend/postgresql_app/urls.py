from django.urls import path
from . import views
from .views import upload_product

urlpatterns = [
    path('api/v1/register/', views.register, name='register'),
    path('api/v1/users/', views.list_users, name='list_users'),
    path('upload-product/', upload_product, name='upload_product'),
]

