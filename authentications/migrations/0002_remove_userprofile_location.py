# Generated by Django 4.2.6 on 2023-11-07 05:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("authentications", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="location",
        ),
    ]
