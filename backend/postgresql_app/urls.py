from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/register/', views.register, name='register'),
    path('api/v1/users/', views.list_users, name='list_users'),
]

