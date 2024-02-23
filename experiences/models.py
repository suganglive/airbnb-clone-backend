from django.conf import settings
from django.db import models

from common.models import CommonModel


class Experience(CommonModel):
    """Experience Definiton"""

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="Korea",
    )
    city = models.CharField(
        max_length=50,
        default="Seoul",
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
        blank=True,
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="experiences",
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    """What is included on an Experience"""

    name = models.CharField(
        max_length=150,
    )
    detail = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    description = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self):
        return self.name
