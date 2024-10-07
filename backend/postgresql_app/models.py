from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('clothing', 'Clothing'),
        ('footwear', 'Footwear'),
        ('accessory', 'Accessory'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
    )

    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='clothing')
    color = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    garment_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imageURL = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.category} ({self.id})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.category == 'clothing' and self.variants.filter(shoe_size__isnull=False).exists():
            raise ValueError('A clothing product cannot have shoe size.')
        if self.category == 'footwear' and self.variants.filter(size__isnull=False).exists():
            raise ValueError('A footwear product cannot have clothing size.')

class ProductVariant(models.Model):
    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    SHOE_SIZE_CHOICES = [(str(x), str(x)) for x in range(35, 46)] 

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, blank=True, null=True)  # Clothing size
    shoe_size = models.CharField(max_length=2, choices=SHOE_SIZE_CHOICES, blank=True, null=True)  # Shoe size
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - Size: {self.size or self.shoe_size} ({self.id})"

    def save(self, *args, **kwargs):
        # Custom validation: Clothing cannot have shoe size, Footwear cannot have clothing size
        if self.product.category == 'clothing' and self.shoe_size:
            raise ValueError('A clothing product cannot have shoe size.')
        if self.product.category == 'footwear' and self.size:
            raise ValueError('A footwear product cannot have clothing size.')
        super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}'s Cart: {self.quantity} x {self.product.name}"

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase by {self.user.username}: {self.quantity} x {self.product.name} on {self.purchase_date}"
