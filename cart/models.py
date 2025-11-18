from django.db import models
from users.models import CustomUser
from products.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart of {self.user.username} - {self.product.name} (x{self.quantity})"