from django import forms
from .models import Centre,Employe, GestionDesEmployes,PV

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