from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from categories.serializers import CategorySerializer
from media.serializer import PhotoSerializer
from reviews.serializer import ReviewSerializer
from users.serializer import TinyUserSerializer
from wishlists.models import Wishlist

from .models import Amenity, Room


class AmenitiySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    def get_rating(self, room):  # mandatory naming
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]  # context from serializer context
        return room.owner == request.user

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )
        # depth = 1


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    # amenities = AmenitiySerializer(
    #     many=True,
    #     read_only=True,
    # )  # many=True because amenities is list
    category = CategorySerializer(read_only=True)

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        # fields = "__all__"
        exclude = ("amenities",)

    def get_rating(self, room):  # mandatory
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]  # context from serializer context
        return room.owner == request.user

    def get_is_liked(self, room):  # room = serializer content.
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()
