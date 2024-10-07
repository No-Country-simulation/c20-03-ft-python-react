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
        fields = ['id', 'name', 'description', 'category', 'color', 'gender', 'garment_type', 'price', 'imageURL', 'variants']

    def create(self, validated_data):
        # Extract variants data
        variants_data = validated_data.pop('variants')
        
        # Create the product
        product = Product.objects.create(**validated_data)
        
        # Create each product variant
        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)
        
        return product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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

