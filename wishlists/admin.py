from django.contrib import admin

from .models import Wishlist


@admin.register(Wishlist)
class Wishlist(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created_at",
        "updated_at",
    )
    pass


# Register your models here.
