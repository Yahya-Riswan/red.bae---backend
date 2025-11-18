from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Whishlist
from .serializers import WishlistSerializer
from users.models import CustomUser
from products.models import Product


class WhishlistListViewADMIN(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        items = Whishlist.objects.all()
        serializer = WishlistSerializer(items, many=True)
        print("ADMIN WISHLIST DATA:", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)



class WishlistView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):

  
        # if request.user.id != user_id:
        #     return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        items = Whishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):


        # if request.user.id != user_id:
        #     return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        product_id = request.data.get("product")

        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Invalid product"}, status=status.HTTP_400_BAD_REQUEST)

 
        existing = Whishlist.objects.filter(user=request.user, product=product).first()


        if existing:
            existing.delete()
            return Response(
                {"message": "Product removed from wishlist"},
                status=status.HTTP_200_OK
            )

 
        new_item = Whishlist.objects.create(user=request.user, product=product)
        serializer = WishlistSerializer(new_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
