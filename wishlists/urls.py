from django.urls import path

from .views import WishlistDetail, WishlistRooms, Wishlists

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", WishlistRooms.as_view()),
]
