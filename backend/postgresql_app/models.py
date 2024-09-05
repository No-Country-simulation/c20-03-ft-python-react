from django.db import models


# Create your models here.
class Joke(models.Model):
  content = models.CharField(max_length=500)
  added_at = models.DateTimeField('time published')

  # ...
  def __str__(self):
    added_at = self.added_at.strftime("%m/%d/%Y, %H:%M:%S")
    return self.content + " | " + added_at

# New Product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name