from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, ProductVariant, Cart, PurchaseHistory

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['size', 'shoe_size', 'stock']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'color', 'gender', 'garment_type', 'price', 'imageURL', 'variants']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['product', 'quantity']

class PurchaseHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PurchaseHistory
        fields = ['product', 'quantity', 'price_at_purchase', 'purchase_date']
