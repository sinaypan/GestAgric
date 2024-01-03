from django.db.models import Sum
from .models import Employe, GestionDesEmployes


def calculer_salaire_mensuel(employe):
    total_absences = employe.gestiondesemployes_set.aggregate(Sum('absences'))['absences__sum'] or 0
    total_avances = employe.gestiondesemployes_set.aggregate(Sum('avances_salaire'))['avances_salaire__sum'] or 0
    salaire_mensuel = employe.salaire_jour * (24 - total_absences) - total_avances
    return max(salaire_mensuel, 0)
