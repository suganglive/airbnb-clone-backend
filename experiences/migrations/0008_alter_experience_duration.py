# Generated by Django 5.0.2 on 2024-02-23 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0007_alter_experience_duration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="duration",
            field=models.DurationField(blank=True, null=True),
        ),
    ]