from django import forms
from .models import Centre,Employe

class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        fields = '__all__'

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = '__all__'