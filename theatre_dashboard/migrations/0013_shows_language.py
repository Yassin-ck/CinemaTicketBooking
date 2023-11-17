# Generated by Django 4.2.6 on 2023-11-17 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("admin_dashboard", "0004_remove_moviesdetails_languages"),
        ("theatre_dashboard", "0012_remove_screendetails_shows_shows_screen"),
    ]

    operations = [
        migrations.AddField(
            model_name="shows",
            name="language",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="admin_dashboard.languages",
            ),
            preserve_default=False,
        ),
    ]
