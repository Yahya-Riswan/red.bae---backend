from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    avgreview= models.FloatField(default=0.0)
    status = models.CharField(max_length=50, default='active')
    def __str__(self):
        return self.title