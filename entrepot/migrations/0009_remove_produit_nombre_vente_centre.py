# Generated by Django 5.0 on 2024-01-05 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrepot', '0008_produit_nombre_vente_centre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='nombre_vente_centre',
        ),
    ]