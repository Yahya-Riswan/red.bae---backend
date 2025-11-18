from .models import Whishlist
from rest_framework import serializers
from users.serializers import UserSerializer
from products.serializers import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Whishlist
        fields = ['id', 'user', 'product']
