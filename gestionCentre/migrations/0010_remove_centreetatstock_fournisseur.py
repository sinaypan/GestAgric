# Generated by Django 5.0 on 2024-01-05 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionCentre', '0009_centreetatstock_fournisseur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='centreetatstock',
            name='fournisseur',
        ),
    ]
