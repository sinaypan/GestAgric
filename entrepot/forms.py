from django import forms
from .models import Fournisseur, Produit, Achat, Transfert, Vente



class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'
        exclude=['solde', 'prix_total_depense_chez_fournisseur']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'
        exclude=['nombre_vente0','nombre_vente1','nombre_vente2','nombre_vente3']


class AchatForm(forms.ModelForm):

    class Meta:
        model = Achat
        fields = '__all__'


class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = '__all__'
        exclude=['prix_unitaire_HT']
        
class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = '__all__'


class MontantAjouteForm(forms.Form):  # Remarquez que c'est un forms.Form et non forms.ModelForm
    montant_ajoute = forms.DecimalField(max_digits=10, decimal_places=2, label="Montant Ajouté")

    def clean_montant_ajoute(self):
        montant_ajoute = self.cleaned_data['montant_ajoute']
        # Vous pouvez ajouter ici une validation supplémentaire si nécessaire
        return montant_ajoute
