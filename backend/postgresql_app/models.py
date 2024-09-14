from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('ropa', 'Ropa'),
        ('calzado', 'Calzado'),
        ('accesorio', 'Accesorio'),
    )

    GENDER_CHOICES = (
        ('hombre', 'Hombre'),
        ('mujer', 'Mujer'),
        ('unisex', 'Unisex'),
    )

    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    id = models.AutoField(primary_key=True)  # ID único
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ropa')
    color = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    garment_type = models.CharField(max_length=50)  # Tipo de prenda
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imageURL = models.CharField(max_length=200, blank=True, null=True)  # URL de imagen
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.category} ({self.id})"

    def save(self, *args, **kwargs):
        # Guarda el producto primero para asegurar que tiene un ID
        super().save(*args, **kwargs)

        # Luego realiza la validación personalizada
        if self.category == 'ropa' and self.variants.filter(shoe_size__isnull=False).exists():
            raise ValueError('Un producto de ropa no puede tener talla de calzado.')
        if self.category == 'calzado' and self.variants.filter(size__isnull=False).exists():
            raise ValueError('Un producto de calzado no puede tener talla de ropa.')

class ProductVariant(models.Model):
    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    SHOE_SIZE_CHOICES = [(str(x), str(x)) for x in range(35, 46)]  # Ejemplo de tallas de calzado (35-45)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, blank=True, null=True)  # Talla (ropa)
    shoe_size = models.CharField(max_length=2, choices=SHOE_SIZE_CHOICES, blank=True, null=True)  # Talla (calzado)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - Size: {self.size or self.shoe_size} ({self.id})"

    def save(self, *args, **kwargs):
        # Validación personalizada: Ropa no puede tener talla de calzado, Calzado no puede tener talla de ropa
        if self.product.category == 'ropa' and self.shoe_size:
            raise ValueError('Un producto de ropa no puede tener talla de calzado.')
        if self.product.category == 'calzado' and self.size:
            raise ValueError('Un producto de calzado no puede tener talla de ropa.')
        super().save(*args, **kwargs)
