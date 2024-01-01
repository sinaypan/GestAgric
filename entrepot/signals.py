from django.db.models.signals import post_save, pre_delete,post_delete,pre_save
from django.dispatch import receiver
from .models import Achat, EtatStock,Vente ,StockManager
from utilisateur.models import Client

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
        montant_achat = (instance.prix_unitaire_HT * instance.quantite)-instance.montant_paye
        fournisseur = instance.fournisseur
        fournisseur.solde += montant_achat
        fournisseur.prix_total_depense_chez_fournisseur += instance.prix_unitaire_HT * instance.quantite
        fournisseur.save()

@receiver(post_delete, sender=Achat)
def update_total_spent_by_supplier_on_delete(sender, instance, **kwargs):
    montant_achat = (instance.prix_unitaire_HT * instance.quantite)-instance.montant_paye
    fournisseur = instance.fournisseur
    fournisseur.solde -= montant_achat
    fournisseur.prix_total_depense_chez_fournisseur -= instance.prix_unitaire_HT * instance.quantite
    fournisseur.save()










@receiver(pre_save, sender=Vente)
def check_stock_and_update(sender, instance, **kwargs):
    produit = instance.produit
    quantite_vendue = instance.quantite

    try:
        etat_stock_produit = EtatStock.objects.get(produit=produit)
        if quantite_vendue > etat_stock_produit.quantite:
            raise ValueError('La quantité à vendre est supérieure à celle en stock')
    except EtatStock.DoesNotExist:
        raise ValueError('État du stock pour ce produit introuvable')

@receiver(post_save, sender=Vente)
def update_stock_and_client_credit(sender, instance, created, **kwargs):
    produit = instance.produit
    quantite_vendue = instance.quantite

    if created:
        etat_stock_produit = EtatStock.objects.get(produit=produit)
        etat_stock_produit.quantite -= quantite_vendue
        etat_stock_produit.save()

        produit.nombre_vente += quantite_vendue
        produit.save()

        difference_prix = (quantite_vendue * instance.prix_unitaire) - instance.montant_encaisse

        if instance.paiement_partiel or difference_prix != 0:
            instance.client.credit += difference_prix
            instance.client.save()

        instance.client.prix_total_depense_par_client += (quantite_vendue * instance.prix_unitaire)
        instance.client.save()

@receiver(pre_delete, sender=Vente)
def update_stock_on_delete(sender, instance, **kwargs):
    produit = instance.produit
    quantite_vendue = instance.quantite

    etat_stock_produit = EtatStock.objects.get(produit=produit)
    etat_stock_produit.quantite += quantite_vendue
    etat_stock_produit.save()

    produit.nombre_vente -= quantite_vendue
    produit.save()

    difference_prix = (quantite_vendue * instance.prix_unitaire) - instance.montant_encaisse

    if instance.paiement_partiel or difference_prix != 0:
        
        instance.client.credit -= difference_prix
        instance.client.save()

    instance.client.prix_total_depense_par_client -= (quantite_vendue * instance.prix_unitaire)
    instance.client.save()

@receiver(post_save, sender=Vente)
def update_stock_and_client_credit(sender, instance, created, **kwargs):
    if created:
        StockManager.update_total_value_minus(instance)

@receiver(post_delete, sender=Vente)
def update_total_stock_value_after_delete(sender, instance, **kwargs):
    StockManager.update_total_value_plus(instance)

@receiver(post_save, sender=Achat)
def update_total_stock_value(sender, instance, created, **kwargs):
    if created:
        StockManager.update_total_stock_value()

@receiver(post_delete, sender=Achat)
def update_total_stock_value_after_delete(sender, instance, **kwargs):
    StockManager.update_total_stock_value()
