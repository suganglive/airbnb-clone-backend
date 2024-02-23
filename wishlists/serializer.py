from rest_framework.serializers import ModelSerializer

from rooms.serializer import RoomListSerializer

from .models import Wishlist


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )


# class SmallWishlist(ModelSerializer):
#     rooms = RoomListSerializer(
#         many=True,
#         read_only=True,
#     )

#     class Meta:
#         model = Wishlist
#         fields = ("rooms",)
