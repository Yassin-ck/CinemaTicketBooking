# Generated by Django 4.2.6 on 2023-12-06 06:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("admin_dashboard", "0001_initial"),
        ("theatre_dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="shows",
            unique_together={("language", "screen", "movies")},
        ),
    ]
