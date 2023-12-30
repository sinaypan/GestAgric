from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=15)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prix_total_depense_par_client = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nom
