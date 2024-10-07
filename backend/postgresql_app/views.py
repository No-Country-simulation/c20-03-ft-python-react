from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from .models import Product, ProductVariant, Cart, PurchaseHistory
from .serializers import ProductSerializer, UserSerializer, CartSerializer, PurchaseHistorySerializer
from django.db import DatabaseError
import traceback  # Para obtener información detallada del error

# View to create a product with error handling
@swagger_auto_schema(method='post', request_body=ProductSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    try:
        if not request.user.groups.filter(name='admin').exists():
            raise PermissionDenied('You do not have permissions to create products.')

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except PermissionDenied as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    except ValidationError as e:
        return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError as e:
        return Response({'error': 'Database error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        # Captura cualquier otro error inesperado
        error_trace = traceback.format_exc()  # Obtener el detalle completo del error
        return Response({
            'error': 'An unexpected error occurred.',
            'details': str(e),
            'trace': error_trace  # Enviar la traza del error para mayor detalle
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to get details of the product variant
@swagger_auto_schema(method='get', responses={200: ProductSerializer})
@api_view(['GET'])
@permission_classes([AllowAny])
def product_variant_detail(request, product_id, size):
    try:
        product = Product.objects.get(pk=product_id)
        variant = product.variants.filter(size=size).first()

        if not variant:
            return Response({'error': 'The specified size variant was not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to get, update, or delete a product
@swagger_auto_schema(method='get', responses={200: ProductSerializer})
@swagger_auto_schema(method='put', request_body=ProductSerializer)
@swagger_auto_schema(method='delete', responses={204: 'Product successfully deleted.'})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        elif request.method == 'PUT':
            if not request.user.is_authenticated or not request.user.groups.filter(name='admin').exists():
                raise PermissionDenied('You do not have permissions to update products.')

            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Product updated successfully.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if not request.user.is_authenticated or not request.user.groups.filter(name='admin').exists():
                raise PermissionDenied('You do not have permissions to delete products.')

            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to list products
@swagger_auto_schema(method='get', responses={200: ProductSerializer(many=True)})
@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    try:
        products = Product.objects.prefetch_related('variants').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to register a user
@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: 'User successfully created.'})
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            return Response({'message': 'User successfully registered.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to list users
@swagger_auto_schema(method='get', responses={200: UserSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='admin').exists()):
        raise PermissionDenied('You do not have permissions to view the user list.')

    users = User.objects.filter(is_superuser=False).exclude(groups__name='admin')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# View to register an admin
@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_admin(request):
    if not request.user.is_superuser:
        raise PermissionDenied('You do not have permissions to create administrators.')

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=request.data['password']
        )
        group = Group.objects.get(name='admin')
        user.groups.add(group)
        return Response({'message': 'Administrator successfully registered.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to obtain a JWT token
@swagger_auto_schema(method='post', request_body=TokenObtainPairSerializer)
@api_view(['POST'])
def token_obtain_pair(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to refresh a JWT token
@swagger_auto_schema(method='post', request_body=TokenRefreshSerializer)
@api_view(['POST'])
def token_refresh(request):
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to add a product to the cart
@swagger_auto_schema(method='post', request_body=CartSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to view cart content
@swagger_auto_schema(method='get', responses={200: CartSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    try:
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to remove a product from the cart
@swagger_auto_schema(method='delete', responses={204: 'Product removed from cart successfully.'})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, product_id):
    try:
        cart_item = Cart.objects.get(user=request.user, product_id=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Cart.DoesNotExist:
        return Response({'error': 'Product not found in cart.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to view purchase history
@swagger_auto_schema(method='get', responses={200: PurchaseHistorySerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_purchase_history(request):
    try:
        purchases = PurchaseHistory.objects.filter(user=request.user)
        serializer = PurchaseHistorySerializer(purchases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
