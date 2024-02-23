from django.contrib import admin

from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("god", "God"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class RatingFilter(admin.SimpleListFilter):
    title = "filter by ratings(more or less!)!"
    parameter_name = "rat"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        rating = self.value()
        if rating == "good":
            # print(reviews.filter(rating__gte=4))
            return reviews.filter(rating__gte=4)
        elif rating == "bad":
            return reviews.filter(rating__lte=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "room",
        "experience",
        "payload",
    )
    list_filter = (
        "rating",
        "user__is_host",
        "room__category",
        WordFilter,
        RatingFilter,
    )
    pass
