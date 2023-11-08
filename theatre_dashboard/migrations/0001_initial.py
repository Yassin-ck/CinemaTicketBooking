# Generated by Django 4.2.6 on 2023-11-07 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("authentications", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TheareOwnerDetails",
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
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone", models.CharField(max_length=13, unique=True)),
                (
                    "alternative_contact",
                    models.CharField(blank=True, max_length=13, null=True, unique=True),
                ),
                ("id_number", models.CharField(max_length=100)),
                ("id_proof", models.ImageField(upload_to="owner_id_proof/")),
                ("address", models.TextField()),
                ("is_verified", models.BooleanField(default=False)),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="theatreownerdetails",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TheatreDetails",
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
                ("theatre_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone", models.CharField(max_length=13, unique=True)),
                (
                    "alternative_contact",
                    models.CharField(blank=True, max_length=13, null=True, unique=True),
                ),
                ("num_of_screens", models.CharField(max_length=2)),
                ("certification", models.ImageField(upload_to="TheatreCertification/")),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "location",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="authentications.location",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="theatreowner",
                        to="theatre_dashboard.theareownerdetails",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ScreenDetails",
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
                ("screen_number", models.IntegerField(blank=True, null=True)),
                ("number_of_seats", models.IntegerField(blank=True, null=True)),
                ("row_count", models.IntegerField(blank=True, null=True)),
                ("column_count", models.IntegerField(blank=True, null=True)),
                ("seat_arrangement", models.JSONField(blank=True, null=True)),
                (
                    "theatre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="theatre_dashboard.theatredetails",
                    ),
                ),
            ],
        ),
    ]
