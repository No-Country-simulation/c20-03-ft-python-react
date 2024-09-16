from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from .serializers import UserSerializer, UserListSerializer, ProductSerializer, ProductVariantSerializer
from .models import Product

# Vista para crear un producto
@swagger_auto_schema(method='post', request_body=ProductSerializer, responses={201: ProductSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    try:
        if not request.user.groups.filter(name='admin').exists():
            raise PermissionDenied('No tienes permisos para crear productos.')
        
        # Asegúrate de que todos los campos necesarios estén presentes y sean válidos
        product_serializer = ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)  # Lanzará un error si los datos no son válidos
        
        # Guarda el producto
        product = product_serializer.save()
        
        # Crea variantes para el producto si existen en la solicitud
        variants_data = request.data.get('variants', [])
        for variant_data in variants_data:
            variant_serializer = ProductVariantSerializer(data=variant_data)
            variant_serializer.is_valid(raise_exception=True)  # Verifica cada variante
            variant_serializer.save(product=product)  # Asocia cada variante al producto creado

        return Response(product_serializer.data, status=status.HTTP_201_CREATED)
    
    except PermissionDenied as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    except ValidationError as e:
        return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Nueva vista para obtener el stock de una variante de producto específica
@swagger_auto_schema(method='get', responses={200: ProductVariantSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_variant_detail(request, product_id, size):
    try:
        # Obtiene el producto por ID
        product = Product.objects.get(pk=product_id)
        
        # Filtra las variantes del producto por el tamaño especificado
        variant = product.variants.filter(size=size).first()

        if not variant:
            return Response({'error': 'No se encontró una variante con el tamaño especificado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serializa la variante encontrada
        serializer = ProductVariantSerializer(variant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    try:
        if not request.user.is_authenticated:
            raise NotAuthenticated('Authentication credentials were not provided.')

        product = Product.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        if request.method == 'PUT':
            if not request.user.groups.filter(name='admin').exists():
                raise PermissionDenied('No tienes permisos para actualizar productos.')

            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            if not request.user.groups.filter(name='admin').exists():
                raise PermissionDenied('No tienes permisos para eliminar productos.')

            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except NotAuthenticated as e:
        return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except PermissionDenied as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para listar productos
@swagger_auto_schema(method='get', responses={200: ProductSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products(request):
    try:
        products = Product.objects.prefetch_related('variants').all()  # Prefetch de variantes
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Vista para registrar un usuario básico
@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer})
@api_view(['POST'])
@permission_classes([AllowAny])
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

# Vista para listar usuarios
@swagger_auto_schema(method='get', responses={200: UserListSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    try:
        if not request.user.is_superuser:
            raise PermissionDenied('No tienes permisos para ver la lista de usuarios.')
        
        users = User.objects.filter(is_superuser=False).exclude(groups__name='admin')
        serializer = UserListSerializer(users, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)
    except PermissionDenied as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Vista para registrar un usuario con rol de admin
@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_admin(request):
    try:
        if not request.user.is_superuser:
            raise PermissionDenied('No tienes permisos para crear administradores.')
        
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
    except PermissionDenied as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
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

