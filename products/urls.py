from django.urls import path
from . import views
urlpatterns = [
    path('admin/', views.admin_all_products.as_view(), name='admin_products'),
    path('admin/<int:pk>/', views.admin_product_detail.as_view(), name='admin_detial_products'),
    path('PC/', views.pc_products.as_view(), name='pc_products'),
    path('Laptops/', views.laptop_products.as_view(), name='laptop_products'),
    path('Parts/', views.parts_products.as_view(), name='parts_products'),
    path('<int:pk>/', views.product_detail.as_view(), name='product_detail'),
]