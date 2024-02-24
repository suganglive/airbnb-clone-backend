from rest_framework.serializers import ModelSerializer

from experiences.serializer import ExperienceListSerailzer
from rooms.serializer import RoomListSerializer

from .models import Wishlist


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

    experiences = ExperienceListSerailzer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = ("pk", "name", "rooms", "experiences")


# class SmallWishlist(ModelSerializer):
#     rooms = RoomListSerializer(
#         many=True,
#         read_only=True,
#     )

#     class Meta:
#         model = Wishlist
#         fields = ("rooms",)
