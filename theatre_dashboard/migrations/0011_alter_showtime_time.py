# Generated by Django 4.2.6 on 2023-11-17 01:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("theatre_dashboard", "0010_showtime_remove_screendetails_movies_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showtime",
            name="time",
            field=models.CharField(max_length=100),
        ),
    ]
