from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_order, name='create-order'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
    path("orders/", views.UserOrdersView.as_view(), name="user-orders"),
    path("orders/<int:order_id>/", views.UpdateOrderStatusView.as_view(), name="update-order-status"),
    path("admin/orders/", views.OrdersListView.as_view(), name="admin-user-orders"),
]
