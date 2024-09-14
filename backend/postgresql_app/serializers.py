from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer, TokenRefreshSerializer as BaseTokenRefreshSerializer
from .models import Product, ProductVariant

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'shoe_size', 'stock']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'color',
            'gender', 'garment_type', 'price', 'imageURL', 'created_at', 'updated_at', 'variants'
        ]

    def create(self, validated_data):
        # Extrae las variantes del producto de los datos validados
        variants_data = validated_data.pop('variants', [])

        # Crea el producto
        product = Product.objects.create(**validated_data)

        # Crea las variantes asociadas al producto
        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)

        return product

    def to_representation(self, instance):
        # Sobreescribir el método para agregar las variantes al serializer
        representation = super().to_representation(instance)
        representation['variants'] = ProductVariantSerializer(instance.variants.all(), many=True).data
        return representation

    def validate(self, data):
        # Validación personalizada para asegurar que haya al menos una variante con stock
        if 'variants' in data and not data['variants']:
            raise serializers.ValidationError({"variants": "Debe proporcionar al menos una variante con stock."})
        return data
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data

class TokenRefreshSerializer(BaseTokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data
