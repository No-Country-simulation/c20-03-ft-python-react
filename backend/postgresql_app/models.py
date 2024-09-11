# backend/postgresql_app/models.py

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
    size = models.CharField(max_length=5, blank=True, null=True, choices=SIZE_CHOICES)  # Talla (ropa)
    shoe_size = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)  # Talla (calzado)
    color = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    garment_type = models.CharField(max_length=50)  # Tipo de prenda
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.category} ({self.id})"

    def save(self, *args, **kwargs):
        # Validación personalizada: Ropa no puede tener talla de calzado, Calzado no puede tener talla de ropa
        if self.category == 'ropa' and self.shoe_size:
            raise ValueError('Un producto de ropa no puede tener talla de calzado.')
        if self.category == 'calzado' and self.size:
            raise ValueError('Un producto de calzado no puede tener talla de ropa.')
        super().save(*args, **kwargs)
