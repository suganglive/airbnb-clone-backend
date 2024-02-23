from django.conf import settings
from django.db import models

from common.models import CommonModel


class ChatRoom(CommonModel):
    """Room Model Definition"""

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="chatrooms",
    )

    def __str__(self):
        return "Chat Room"


class Message(CommonModel):
    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )
    room = models.ForeignKey(
        "dms.ChatRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self):
        return f"{self.user} says: {self.text[:10]}..."


# Create your models here.
