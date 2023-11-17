# Generated by Django 4.2.6 on 2023-11-17 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("admin_dashboard", "0004_remove_moviesdetails_languages"),
        ("theatre_dashboard", "0013_shows_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shows",
            name="movies",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="show_movie",
                to="admin_dashboard.moviesdetails",
            ),
        ),
    ]
