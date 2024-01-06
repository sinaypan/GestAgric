from django import forms
from .models import Centre,Employe, GestionDesEmployes,PV,CentreVente

class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        fields = '__all__'

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = '__all__'
    
class GestionDesEmployesForm(forms.ModelForm):
    absence = forms.BooleanField(required=False, label='Absence')

    class Meta:
       
        model = GestionDesEmployes
        fields = ['employe', 'avances_salaire', 'absence', 'date']

class PVForm(forms.ModelForm):
    class Meta:
        model = PV
        fields = ['employe', 'montant_verse', 'centre_responsable', 'description']

class VenteForm(forms.ModelForm):
    class Meta:
        model = CentreVente
        fields = '__all__'

class MontantAjouteForm(forms.Form):  # Remarquez que c'est un forms.Form et non forms.ModelForm
    montant_ajoute = forms.DecimalField(max_digits=10, decimal_places=2, label="Montant Ajouté")

    def clean_montant_ajoute(self):
        montant_ajoute = self.cleaned_data['montant_ajoute']
        # Vous pouvez ajouter ici une validation supplémentaire si nécessaire
        return montant_ajoute