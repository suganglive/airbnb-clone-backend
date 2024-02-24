from rest_framework.serializers import ModelSerializer

from categories.serializers import CategorySerializer
from media.serializer import PhotoSerializer
from users.serializer import TinyUserSerializer

from .models import Experience, Perk


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceListSerailzer(ModelSerializer):
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Experience
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "photos",
            "duration",
        )


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(
        read_only=True,
    )
    perks = PerkSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "description",
            "host",
            "address",
            "start",
            "end",
            "duration",
            "perks",
            "category",
            "photos",
        )
