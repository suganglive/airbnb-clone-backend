from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "room",
        "experience",
        "check_in",
        "check_out",
        "experience_time",
        "guests",
    )
    list_filter = ("kind",)
