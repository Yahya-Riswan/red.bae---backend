import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import OrderSerializer

client = razorpay.Client(auth=("rzp_test_RgjsRtwJcR5YW8", "AiSySpQfsmQUX5pmtxrEe9Qs"))


@api_view(["POST"])
def create_order(request):
    amount = int(request.data["amount"])
    cart_items = request.data["cart"]
    user = request.user

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # Create Order in Django
    order = Order.objects.create(
        user=user,
        razorpay_order_id=razorpay_order["id"],
        total_amount=request.data["amount"]
    )

    # Add Order Items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product_id=item["id"],
            quantity=item["quantity"]
        )

    return Response({
        "order_id": razorpay_order["id"],
        "amount": razorpay_order["amount"],
        "currency": razorpay_order["currency"],
    })


@api_view(["POST"])
def verify_payment(request):
    data = request.data

    # verify payment
    client.utility.verify_payment_signature({
        "razorpay_order_id": data["order_id"],
        "razorpay_payment_id": data["razorpay_payment_id"],
        "razorpay_signature": data["razorpay_signature"],
    })

    # Fetch payment details (to get payment method)
    payment = client.payment.fetch(data["razorpay_payment_id"])

    # Update Order
    order = Order.objects.get(razorpay_order_id=data["order_id"])
    order.razorpay_payment_id = data["razorpay_payment_id"]
    order.razorpay_signature = data["razorpay_signature"]
    order.payment_method = payment["method"]
    order.status = "Paid"
    order.save()

    return Response({"status": "success"})



class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class OrdersListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

    
    
class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        new_status = request.data.get("status")

        if new_status not in ["Processing", "Packed", "Shipped", "Delivered", "Cancelled"]:
            return Response({"error": "Invalid status"}, status=400)

        order.status = new_status
        order.save()

        return Response({"message": "Order status updated", "status": new_status})