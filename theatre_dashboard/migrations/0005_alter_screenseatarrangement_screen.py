# Generated by Django 4.2.6 on 2023-11-14 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("theatre_dashboard", "0004_screenseatarrangement_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="screenseatarrangement",
            name="screen",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to="theatre_dashboard.screendetails",
            ),
        ),
    ]
