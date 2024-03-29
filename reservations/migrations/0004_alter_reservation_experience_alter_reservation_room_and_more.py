# Generated by Django 5.0.2 on 2024-02-15 05:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0003_alter_experience_category_alter_experience_perks"),
        ("reservations", "0003_alter_reservation_kind"),
        ("rooms", "0006_alter_room_amenities_alter_room_category_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="experience",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reservations",
                to="experiences.experience",
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="room",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reservations",
                to="rooms.room",
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
