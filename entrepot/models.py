from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import F


class Fournisseur(models.Model):
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=15)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prix_total_depense_chez_fournisseur = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Ajout de l'attribut nombre_achat pour les fournisseurs

    def __str__(self):
        return self.nom

class Produit(models.Model):
    code = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
    nombre_vente = models.IntegerField(default=0)  # Ajout de l'attribut nombre_vente pour les produits

    def __str__(self):
        return self.designation
    
class Achat(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire_HT = models.DecimalField(max_digits=10, decimal_places=2)
    date_achat = models.DateField(auto_now_add=True)
    paiement_partiel = models.BooleanField(default=False)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    
    def __str__(self):
        return f"Achat de {self.produit} chez {self.fournisseur} le {self.date_achat}"

class Transfert(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite = models.IntegerField()
    centre_destination = models.ForeignKey('gestionCentre.Centre', on_delete=models.CASCADE)
    date_transfert = models.DateField(auto_now_add=True)
    # Add other fields as needed

    def __str__(self):
        return f"Transfert de {self.produit} vers {self.centre_destination} le {self.date_transfert}"

class Vente(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    client = models.ForeignKey('utilisateur.Client', on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    montant_encaisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_vente = models.DateField(auto_now_add=True)
    paiement_partiel = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        etat_stock, _ = EtatStock.objects.get_or_create(produit=self.produit)

        total_vente = self.quantite * self.prix_unitaire
        difference = total_vente - self.montant_encaisse

        if self.paiement_partiel:
            difference = self.montant_encaisse

        if self.pk:  # Si c'est une mise à jour
            ancienne_vente = Vente.objects.get(pk=self.pk)

            # Vérifier la quantité seulement si elle a été modifiée
            if self.quantite != ancienne_vente.quantite:
                difference_quantite = self.quantite - ancienne_vente.quantite

                if self.quantite > etat_stock.quantite + difference_quantite:
                    raise ValidationError("Quantité de vente supérieure à la quantité en stock.")

                etat_stock.quantite -= difference_quantite
                etat_stock.save()

            # Ajuster le crédit du client
            ancien_montant_vente = ancienne_vente.quantite * ancienne_vente.prix_unitaire
            ancien_difference = ancien_montant_vente - ancienne_vente.montant_encaisse

            self.client.credit -= ancien_difference
            self.client.prix_total_depense_par_client -= ancien_difference
            self.produit.nombre_vente -= ancienne_vente.quantite
            self.client.save()
            self.produit.save()

        else:  # Pour un nouvel achat
            if self.quantite > etat_stock.quantite:
                raise ValidationError("Quantité de vente supérieure à la quantité en stock.")

            etat_stock.quantite -= self.quantite
            etat_stock.save()

        # Mettre à jour le crédit du client pour un nouvel achat ou une mise à jour
        self.client.credit += difference
        self.client.prix_total_depense_par_client += difference
        self.client.save()
        self.produit.nombre_vente += self.quantite
        self.produit.save()

    def delete(self, *args, **kwargs):
        etat_stock, _ = EtatStock.objects.get_or_create(produit=self.produit)
        total_vente = self.quantite * self.prix_unitaire
        difference = total_vente - self.montant_encaisse

        # Remettre la quantité en stock
        etat_stock.quantite += self.quantite
        etat_stock.save()

        # Ajuster le crédit du client
        self.client.credit -= difference
        self.client.prix_total_depense_par_client -= difference
        self.client.save()
        self.produit.nombre_vente -= self.quantite
        self.produit.save()
        

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Vente de {self.produit} à {self.client} le {self.date_vente}"

class EtatStock(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    quantite = models.IntegerField(default=0)
    date_achat = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"État du stock de {self.produit} : {self.quantite}"


class AnalyseAchats(models.Model):
    taux_evolution_achats = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top_fournisseurs = models.ManyToManyField('Fournisseur', blank=True)



