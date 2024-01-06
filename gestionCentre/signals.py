from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import CentreVente, CentreEtatStock,Centre
from django.db.models.signals import post_save

@receiver(pre_save, sender=CentreVente)
def validate_stock_before_sale(sender, instance, **kwargs):
    try:
        centre_stock = CentreEtatStock.objects.get(produit=instance.produit, centre=instance.centre)
        if instance.quantite > centre_stock.quantite:
            raise ValueError('La quantité à vendre est supérieure à celle en stock')
    except CentreEtatStock.DoesNotExist:
       raise ValueError('État du stock pour ce produit introuvable')

@receiver(post_save, sender=CentreVente)
def update_centre_total_stock_value_on_sale(sender, instance, created, **kwargs):
    produit = instance.produit
    quantite_vendue = instance.quantite

    if created:
        # Mise à jour du stock
        centre_stock = CentreEtatStock.objects.get(produit=produit, centre=instance.centre)
        centre_stock.quantite -= quantite_vendue
        centre_stock.save()

        # Utiliser directement instance.centre
        designation_centre = instance.centre.designation

        # Mise à jour du compteur de ventes pour le centre spécifique
        if designation_centre == 'centre1':
            produit.nombre_vente1 += quantite_vendue
        elif designation_centre == 'centre2':
            produit.nombre_vente2 += quantite_vendue
        elif designation_centre == 'centre3':
            produit.nombre_vente3 += quantite_vendue
        produit.save()

        # Mise à jour du crédit du client et du total dépensé
        difference_prix = (quantite_vendue * instance.prix_unitaire) - instance.montant_encaisse
        if instance.paiement_partiel or difference_prix != 0:
            instance.client.credit += difference_prix
            instance.client.save()
        instance.client.prix_total_depense_par_client += (quantite_vendue * instance.prix_unitaire)
        instance.client.save()




@receiver(pre_delete, sender=CentreVente)
def update_stock_on_delete(sender, instance, **kwargs):
    produit = instance.produit
    quantite_vendue = instance.quantite

    # Mise à jour du stock
    centre_stock = CentreEtatStock.objects.get(produit=produit, centre=instance.centre)
    centre_stock.quantite += quantite_vendue
    centre_stock.save()

    # Utiliser directement instance.centre au lieu de le récupérer de nouveau
    designation_centre = instance.centre.designation

    # Mise à jour du compteur de ventes pour le centre spécifique
    if designation_centre == 'centre1':
        produit.nombre_vente1 -= quantite_vendue
    elif designation_centre == 'centre2':
        produit.nombre_vente2 -= quantite_vendue
    elif designation_centre == 'centre3':
        produit.nombre_vente3 -= quantite_vendue
    produit.save()

    # Mise à jour du crédit du client et du total dépensé
    difference_prix = (quantite_vendue * instance.prix_unitaire) - instance.montant_encaisse
    if instance.paiement_partiel or difference_prix != 0:
        instance.client.credit -= difference_prix
        instance.client.save()
    instance.client.prix_total_depense_par_client -= (quantite_vendue * instance.prix_unitaire)
    instance.client.save()


#tae stockmanager /vente mzl