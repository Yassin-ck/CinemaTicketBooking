# Generated by Django 4.2.6 on 2023-10-24 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theatre_dashboard', '0003_alter_theareownerdetails_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theareownerdetails',
            name='password',
        ),
    ]
