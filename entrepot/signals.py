from django.db.models.signals import post_save, pre_delete,post_delete
from django.dispatch import receiver
from .models import Achat, EtatStock

@receiver(post_save, sender=Achat)
def update_stock_on_product_creation_or_update(sender, instance, created, **kwargs):
    etat_stock_global, _ = EtatStock.objects.get_or_create(produit=instance.produit)

    if created:
        # Lors de la création d'un nouvel achat, augmenter la quantité en stock
        etat_stock_global.quantite += instance.quantite
        etat_stock_global.fournisseur = instance.fournisseur

    else:
        # Si l'achat existait déjà et a été mis à jour, ajuster la quantité en conséquence
        ancien_achat = Achat.objects.get(pk=instance.pk)
        difference_quantite = instance.quantite - ancien_achat.quantite
        etat_stock_global.quantite += difference_quantite

    etat_stock_global.save()
    

@receiver(pre_delete, sender=Achat)
def update_stock_on_product_deletion(sender, instance, **kwargs):
    etat_stock_global = EtatStock.objects.filter(produit=instance.produit).first()
    if etat_stock_global and instance.quantite <= etat_stock_global.quantite:
        # Si la quantité de l'achat à supprimer est inférieure ou égale à la quantité en stock,
        # diminuer la quantité en stock
        etat_stock_global.quantite -= instance.quantite
        etat_stock_global.save()


@receiver(post_save, sender=Achat)
def update_total_spent_by_supplier_on_create(sender, instance, created, **kwargs):
    if created:
        montant_achat = instance.prix_unitaire_HT * instance.quantite
        fournisseur = instance.fournisseur
        fournisseur.solde += montant_achat
        fournisseur.prix_total_depense_chez_fournisseur += montant_achat
        fournisseur.save()

@receiver(post_delete, sender=Achat)
def update_total_spent_by_supplier_on_delete(sender, instance, **kwargs):
    montant_achat = instance.prix_unitaire_HT * instance.quantite
    fournisseur = instance.fournisseur
    fournisseur.solde -= montant_achat
    fournisseur.prix_total_depense_chez_fournisseur -= montant_achat
    fournisseur.save()
