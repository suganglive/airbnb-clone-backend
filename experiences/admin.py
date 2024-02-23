from django.contrib import admin

from .models import Experience, Perk


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start",
        "end",
        "price",
    )
    list_filter = ("category",)
    pass


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = ("name", "detail", "description")
    pass
