from django import forms
from .models import Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['code', 'nom', 'adresse', 'telephone']



class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'adresse', 'telephone')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(
        label="Code de vérification",
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Veuillez entrer le code de vérification.',
            'max_length': 'Le code de vérification doit contenir au maximum 4 caractères.',
            'min_length': 'Le code de vérification doit contenir au minimum 4 caractères.',
        }
    )