from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .serializers import UserSerializer, UserListSerializer, ProductSerializer
from .models import Product
from django.views.decorators.csrf import csrf_protect  # Importar csrf_protect desde Django

# Vista para listar productos
@swagger_auto_schema(method='get', responses={200: ProductSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para crear un producto
@swagger_auto_schema(method='post', request_body=ProductSerializer, responses={201: ProductSerializer})
@csrf_protect
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    if not request.user.groups.filter(name='admin').exists():
        return Response({'error': 'No tienes permisos para crear productos'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para obtener, actualizar o eliminar un producto
@swagger_auto_schema(
    method='get', 
    responses={200: ProductSerializer}
)
@swagger_auto_schema(
    method='put', 
    request_body=ProductSerializer, 
    responses={200: ProductSerializer}
)
@swagger_auto_schema(
    method='delete', 
    responses={204: 'No Content'}
)
@csrf_protect
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == 'PUT':
        if not request.user.groups.filter(name='admin').exists():
            return Response({'error': 'No tienes permisos para actualizar productos'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not request.user.groups.filter(name='admin').exists():
            return Response({'error': 'No tienes permisos para eliminar productos'}, status=status.HTTP_403_FORBIDDEN)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Vista para listar usuarios
@swagger_auto_schema(method='get', responses={200: UserListSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    try:
        users = User.objects.filter(is_superuser=False)
        serializer = UserListSerializer(users, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para registrar un usuario básico
@csrf_protect
@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer})
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso a cualquiera
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, password=password, email=email)
            
            # Asignar al grupo 'user'
            group = Group.objects.get(name='user')
            user.groups.add(group)
            
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para registrar un usuario con rol de admin
@csrf_protect
@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_admin(request):
    try:
        if not request.user.is_superuser:
            return Response({'error': 'No tienes permisos para crear administradores'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, password=password, email=email)
            
            # Asignar al grupo 'admin'
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            
            return Response({'message': 'Admin user created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_protect
@swagger_auto_schema(method='post', request_body=TokenObtainPairSerializer, responses={200: TokenObtainPairSerializer})
@api_view(['POST'])
def token_obtain_pair(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_protect
@swagger_auto_schema(method='post', request_body=TokenRefreshSerializer, responses={200: TokenRefreshSerializer})
@api_view(['POST'])
def token_refresh(request):
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
