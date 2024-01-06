from django.db.models.signals import post_save, pre_delete,post_delete,pre_save
from django.dispatch import receiver
from .models import Achat, EtatStock,Vente ,StockManager,Transfert
from utilisateur.models import Client
from gestionCentre.models import CentreEtatStock

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
        
    else:#modif
        fournisseur = instance.fournisseur
        ancien_achat = Achat.objects.get(pk=instance.pk)
        ancien_montant = (ancien_achat.prix_unitaire_HT * ancien_achat.quantite) - ancien_achat.montant_paye
        nouveau_montant = (instance.prix_unitaire_HT * instance.quantite) - instance.montant_paye
        difference = nouveau_montant - ancien_montant
        fournisseur.solde += difference
        if instance.prix_unitaire_HT != ancien_achat.prix_unitaire_HT or instance.quantite != ancien_achat.quantite:
            fournisseur.prix_total_depense_chez_fournisseur += difference

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

        produit.nombre_vente0 += quantite_vendue
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

    produit.nombre_vente0 -= quantite_vendue
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

#transfert et etat stock

@receiver(pre_save, sender=Transfert)
def check_stock_before_transfer(sender, instance, **kwargs):
    produit = instance.produit
    quantite_transferee = instance.quantite

    # Vérifier si la quantité à transférer est disponible en stock
    try:
        etat_stock_produit = EtatStock.objects.get(produit=produit)
        if quantite_transferee > etat_stock_produit.quantite:
            raise ValueError('La quantité à transférer est supérieure à celle en stock')
    except EtatStock.DoesNotExist:
        raise ValueError('État du stock pour ce produit introuvable')

@receiver(post_save, sender=Transfert)
def update_stock_after_transfer(sender, instance, created, **kwargs):
    if created:
        produit = instance.produit
        quantite_transferee = instance.quantite

        # Mettre à jour l'état du stock
        etat_stock_produit = EtatStock.objects.get(produit=produit)
        etat_stock_produit.quantite -= quantite_transferee
        etat_stock_produit.save()

        # Optionnel: Mettre à jour un champ dans le produit ou ailleurs pour suivre le nombre de transferts

@receiver(pre_delete, sender=Transfert)
def update_stock_on_cancel_transfer(sender, instance, **kwargs):
    produit = instance.produit
    quantite_transferee = instance.quantite

    # Annuler la mise à jour de stock si un transfert est supprimé
    etat_stock_produit = EtatStock.objects.get(produit=produit)
    etat_stock_produit.quantite += quantite_transferee
    etat_stock_produit.save()

#changer etat stock du centre a cause du transfert
@receiver(post_save, sender=Transfert)
def update_centre_stock_on_transfert_creation_or_update(sender, instance, created, **kwargs):
    centre_stock, _ = CentreEtatStock.objects.get_or_create(produit=instance.produit, centre=instance.centre_destination)

    if created:
        # Increase stock quantity for the destination centre when a new transfer is created
        centre_stock.quantite += instance.quantite
    else:
        # Adjust stock quantity for the destination centre if the transfer is updated
        old_transfert = Transfert.objects.get(pk=instance.pk)
        difference_quantite = instance.quantite - old_transfert.quantite
        centre_stock.quantite += difference_quantite

    centre_stock.save()


@receiver(pre_delete, sender=Transfert)
def update_centre_stock_on_transfert_deletion(sender, instance, **kwargs):
    centre_stock = CentreEtatStock.objects.filter(produit=instance.produit, centre=instance.centre_destination).first()
    if centre_stock and instance.quantite <= centre_stock.quantite:
        # Decrease stock quantity for the destination centre when a transfer is deleted
        centre_stock.quantite -= instance.quantite
        centre_stock.save()
