# backend/postgresql_app/views.py

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .serializers import UserSerializer, UserListSerializer

@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Requiere autenticación
def register(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            User.objects.create_user(username=username, password=password, email=email)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='get', responses={200: UserListSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Requiere autenticación
def list_users(request):
    try:
        users = User.objects.filter(is_superuser=False)
        serializer = UserListSerializer(users, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='post', request_body=TokenObtainPairSerializer, responses={200: TokenObtainPairSerializer})
@api_view(['POST'])
def token_obtain_pair(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=TokenRefreshSerializer, responses={200: TokenRefreshSerializer})
@api_view(['POST'])
def token_refresh(request):
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
