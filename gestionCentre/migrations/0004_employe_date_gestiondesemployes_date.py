# Generated by Django 5.0 on 2024-01-03 01:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionCentre', '0003_activiteducentre_analyseventes_gestiondesemployes'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='gestiondesemployes',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
