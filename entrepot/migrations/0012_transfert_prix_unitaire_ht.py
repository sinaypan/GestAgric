# Generated by Django 5.0 on 2024-01-06 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrepot', '0011_remove_produit_nombre_vente_produit_nombre_vente0_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfert',
            name='prix_unitaire_HT',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
