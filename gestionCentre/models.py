from django.db import models
from django.utils import timezone

class Centre(models.Model):
    code = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
    total_stock_value = 0 
    # Ajoutez d'autres champs pour les détails du centre

    

    def __str__(self):
        return self.designation

class Employe(models.Model):
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=15)
    salaire_jour = models.DecimalField(max_digits=10, decimal_places=2)
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.nom
    

class GestionDesEmployes(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)  # Lien vers le modèle Employé
    salaires_journaliers = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    absences = models.IntegerField(default=0)  # Nombre de jours d'absence
    avances_salaire = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, null=True)  # Make this field optional
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Gestion de {self.employe.nom}"

class ActiviteDuCentre(models.Model):
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE)  # Lien vers le modèle Centre
    date = models.DateField
    description = models.TextField()
    employe_responsable = models.ForeignKey('Employe', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Activité du {self.date} au {self.centre.designation}"
    
class PV(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    montant_verse = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    centre_responsable = models.ForeignKey(Centre, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"PV for {self.employe.nom} on {self.date}"

class CentreVente(models.Model):
    produit = models.ForeignKey('entrepot.Produit', on_delete=models.CASCADE)
    client = models.ForeignKey('utilisateur.Client', on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    montant_encaisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_vente = models.DateField(auto_now_add=True)
    paiement_partiel = models.BooleanField(default=False)
   



    def __str__(self):
        return f"Vente de {self.produit} à {self.client} le {self.date_vente}"

class CentreEtatStock(models.Model):
    produit = models.ForeignKey('entrepot.Produit', on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    date_achat = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"État du stock de {self.produit} : {self.quantite}"

