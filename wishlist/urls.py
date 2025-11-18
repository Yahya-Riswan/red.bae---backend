from django.urls import path
from .views import WishlistView, WhishlistListViewADMIN

urlpatterns = [
    path("wishlist/<str:user_id>/", WishlistView.as_view()),
    path("admin/wishlist/", WhishlistListViewADMIN.as_view()),
]
