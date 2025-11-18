from django.urls import path
from .views import CartListView, CartDetailView, ClearCartView, CartListViewADMIN

urlpatterns = [
    path("admin/", CartListViewADMIN.as_view()),
    path("<str:user_id>/", CartListView.as_view()),  
    path("item/<int:pk>/", CartDetailView.as_view()), 
    path('<str:user_id>/clear/', ClearCartView.as_view(), name='cart-clear'),
]
