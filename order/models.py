from django.db import models
from users.models import CustomUser as User
from products.models import Product    # change to your product app

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=200)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, default="Processing")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
