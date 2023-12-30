from django.db import models

class Centre(models.Model):
    code = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
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
    salaires_journaliers = models.DecimalField(max_digits=8, decimal_places=2)
    absences = models.IntegerField(default=0)  # Nombre de jours d'absence
    avances_salaire = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Gestion de {self.employe.nom}"

class ActiviteDuCentre(models.Model):
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE)  # Lien vers le modèle Centre
    date = models.DateField
    description = models.TextField()
    employe_responsable = models.ForeignKey('Employe', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Activité du {self.date} au {self.centre.designation}"
    
class AnalyseVentes(models.Model):
    taux_evolution_ventes = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    taux_evolution_benefice = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top_clients = models.ManyToManyField('utilisateur.Client', blank=True)
    produits_best_seller = models.ManyToManyField('entrepot.Produit', blank=True)

    def __str__(self):
        return "Analyse des Ventes pour la période spécifiée"