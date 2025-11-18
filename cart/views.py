from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer
from users.models import CustomUser
from products.models import Product
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class CartListViewADMIN(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        cart_items = Cart.objects.all()
        serializer = CartSerializer(cart_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CartListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response(
                {"error": "Unauthorized access"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, user_id):

        # if request.user.id != user_id:
        #     return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Invalid product"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    
class CartDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, user, pk):
        try:
            return Cart.objects.get(user=user, product__id=pk)
        except Cart.DoesNotExist:
            return None

    def put(self, request, pk):
        cart_item = self.get_object(request.user, pk)
        if not cart_item:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()

        return Response(CartSerializer(cart_item).data)

    def delete(self, request, pk):
        cart_item = self.get_object(request.user, pk)
        if not cart_item:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClearCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        # # Ensure user can clear only their own cart
        # if request.user.id != user_id:
        #     return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

       
        deleted_count, _ = Cart.objects.filter(user=request.user).delete()

        return Response(
            {"message": "Cart cleared", "items_deleted": deleted_count},
            status=status.HTTP_200_OK
        )