# Generated by Django 5.0.2 on 2024-02-14 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="romms",
            new_name="rooms",
        ),
    ]
