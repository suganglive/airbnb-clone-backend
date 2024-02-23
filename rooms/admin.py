from django.contrib import admin

from .models import Amenity, Room


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):  # Takes three parameters
    for room in rooms:
        room.price = 0
        room.save()


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "rating",  # takse function(method) as well.
        "total_amenities",
        "owner",
    )

    list_filter = (
        "name",
        "country",
        "city",
        "created_at",
        "amenities",
    )
    search_fields = (
        # ^ -> startswith, = -> exact, none -> contain. ex) "name" -> contain, "^name" -> startswith
        "owner__username",
        "name",
    )
    # def total_amenities(self, room):
    #     return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
