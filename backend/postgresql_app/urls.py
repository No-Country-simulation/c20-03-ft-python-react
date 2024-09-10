# backend/postgresql_app/urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('v1/register/', views.register, name='register'),
    path('v1/users/', views.list_users, name='list_users'),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
