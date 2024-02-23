# Generated by Django 5.0.2 on 2024-02-14 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150)),
                (
                    "kind",
                    models.CharField(
                        choices=[("rooms", "Rooms"), ("expereince", "Experience")],
                        max_length=30,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
