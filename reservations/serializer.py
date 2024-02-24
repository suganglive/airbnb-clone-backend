from django.utils import timezone
from rest_framework import serializers

# from datetime import timedelta
from .models import Reservation


class PublicReservationSerializer(serializers.ModelSerializer):  # public booking
    guests = serializers.IntegerField()

    class Meta:
        model = Reservation
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "kind",
            "guests",
        )


class CreateRoomReservationSerializer(
    serializers.ModelSerializer
):  # only for create reservation
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Reservation
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localdate(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't reservate in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localdate(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't reservate in the past!")
        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "check_out should be later then check_in!"
            )
        if Reservation.objects.filter(
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        ).exists():
            raise serializers.ValidationError("Reservation occupied.")
        else:
            return data


class CreateExpereinceReservation(serializers.ModelSerializer):

    experience_time = serializers.DateTimeField()

    class Meta:
        model = Reservation
        fields = (
            "experience_time",
            "kind",
            "guests",
        )

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't reservate in the past!")
        return value

    def validate(self, data):
        duration = self.context["duration"]
        start = data["experience_time"]
        startminus = start - duration
        startplus = start + duration
        # print(startminus)
        # print(startplus)

        if Reservation.objects.filter(
            experience_time__gt=startminus,
            experience_time__lt=startplus,
        ).exists():
            raise serializers.ValidationError("Reservation occupied.")
        else:
            return data
