# Generated by Django 5.0.2 on 2024-02-23 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0003_alter_experience_category_alter_experience_perks"),
    ]

    operations = [
        migrations.RenameField(
            model_name="experience",
            old_name="end",
            new_name="duration",
        ),
        migrations.RemoveField(
            model_name="experience",
            name="start",
        ),
    ]
