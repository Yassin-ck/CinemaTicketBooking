# Generated by Django 4.2.6 on 2023-10-26 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theatre_dashboard', '0008_theareownerdetails_id_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='theareownerdetails',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='theareownerdetails',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='theatredetails',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='theatredetails',
            name='is_loginned',
            field=models.BooleanField(default=False),
        ),
    ]
