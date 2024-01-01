from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.models import Sum


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



    def __str__(self):
        return f"Vente de {self.produit} à {self.client} le {self.date_vente}"

class EtatStock(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    quantite = models.IntegerField(default=0)
    date_achat = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"État du stock de {self.produit} : {self.quantite}"

class StockManager(models.Model):
    total_stock_value = 0  # Initial total stock value

    @classmethod
    def update_total_stock_value(cls):
        all_purchases = Achat.objects.all()
        total_value = sum(purchase.quantite * purchase.prix_unitaire_HT for purchase in all_purchases)
        cls.total_stock_value = total_value

    @classmethod
    def update_total_value_minus(cls, instance):
        quantite_vendue = instance.quantite  # Obtenez la quantité vendue dans l'instance de vente

        # Récupérez le prix total d'achat du produit depuis la table Achat
        prix_total_achat_produit = Achat.objects.filter(produit=instance.produit).aggregate(total_achat=Sum('prix_unitaire_HT'))['total_achat']

        if prix_total_achat_produit is not None:
            # Mettez à jour la valeur totale du stock en déduisant le coût total d'achat de la quantité vendue
            cls.total_stock_value -= quantite_vendue * prix_total_achat_produit

    @classmethod
    def update_total_value_plus(cls, instance):
        quantite_vendue = instance.quantite  # Obtenez la quantité vendue dans l'instance de vente

        # Récupérez le prix total d'achat du produit depuis la table Achat
        prix_total_achat_produit = Achat.objects.filter(produit=instance.produit).aggregate(total_achat=Sum('prix_unitaire_HT'))['total_achat']

        if prix_total_achat_produit is not None:
            # Mettez à jour la valeur totale du stock en déduisant le coût total d'achat de la quantité vendue
            cls.total_stock_value += quantite_vendue * prix_total_achat_produit


class AnalyseAchats(models.Model):
    taux_evolution_achats = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top_fournisseurs = models.ManyToManyField('Fournisseur', blank=True)



