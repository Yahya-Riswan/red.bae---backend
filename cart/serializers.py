from .models import Cart
from rest_framework import serializers
from users.serializers import UserSerializer
from products.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']
