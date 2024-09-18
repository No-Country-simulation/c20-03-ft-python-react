from rest_framework import serializers
from django.contrib.auth.models import User  # This import is missing
from .models import Product, ProductVariant, Cart, PurchaseHistory

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['size', 'shoe_size', 'stock']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'color', 'gender', 'garment_type', 'price', 'imageURL', 'variants']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # The User model is now properly defined
        fields = ['username', 'email']

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
