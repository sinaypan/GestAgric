from django.shortcuts import render, get_object_or_404, redirect
from .models import Centre, Employe,GestionDesEmployes,PV,CentreVente,CentreEtatStock
from .forms import CentreForm, EmployeForm,GestionDesEmployesForm,PVForm,VenteForm,MontantAjouteForm
from .utilities import calculer_salaire_mensuel
import matplotlib.pyplot as plt
from django.db.models import Sum, FloatField
from django.utils.dateparse import parse_date
from utilisateur.models import Client
from entrepot.models import Produit,Fournisseur
from django.core.exceptions import ValidationError
from entrepot.models import Transfert



def centre_list(request):
    query = request.GET.get('q')
    centres = Centre.objects.all()

    if query:
        centres = centres.filter(designation__icontains=query)  # Filtrer par le champ 'designation'

    return render(request, 'Centre/centre_list.html', {'centres': centres})

# Vues pour le détail, l'ajout, la modification et la suppression similaires à celles des autres modèles
# centre_detail, centre_new, centre_edit, centre_delete
def centre_detail(request, pk):
    centre = get_object_or_404(Centre, pk=pk)

    # Calcul du montant total des ventes pour ce centre
    ventes = CentreVente.objects.filter(centre=centre)
    montant_total_ventes = sum(vente.quantite * vente.prix_unitaire for vente in ventes)

    # Calcul du montant total des transferts pour ce centre
    transferts = Transfert.objects.filter(centre_destination=centre)
    montant_total_transferts = sum(transfert.quantite * transfert.prix_unitaire_HT for transfert in transferts)

    # Calcul du bénéfice en soustrayant le montant des transferts du montant des ventes
    benefice = montant_total_ventes - montant_total_transferts

    return render(request, 'Centre/centre_detail.html', {
        'centre': centre,
        'montant_total_ventes': montant_total_ventes,
        'montant_total_transferts': montant_total_transferts,
        'benefice': benefice,
    })

def centre_new(request):
    if request.method == "POST":
        form = CentreForm(request.POST)
        if form.is_valid():
            centre = form.save(commit=False)
            centre.save()
            return redirect('centre_detail', pk=centre.pk)
    else:
        form = CentreForm()
    return render(request, 'Centre/centre_edit.html', {'form': form})

def centre_edit(request, pk):
    centre = get_object_or_404(Centre, pk=pk)
    if request.method == "POST":
        form = CentreForm(request.POST, instance=centre)
        if form.is_valid():
            centre = form.save(commit=False)
            centre.save()
            return redirect('centre_detail', pk=centre.pk)
    else:
        form = CentreForm(instance=centre)
    return render(request, 'Centre/centre_edit.html', {'form': form})

def centre_delete(request, pk):
    centre = get_object_or_404(Centre, pk=pk)
    centre.delete()
    return redirect('centre_list')

def employe_list(request):
    query = request.GET.get('q')
    employes = Employe.objects.all()

    if query:
        employes = employes.filter(nom__icontains=query)

    return render(request, 'Employe/employe_list.html', {'employes': employes})

def employe_detail(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    employe_salaire_mensuel = calculer_salaire_mensuel(employe)
    return render(request, 'Employe/employe_detail.html', {'employe': employe,'employe_salaire_mensuel':employe_salaire_mensuel})

def employe_new(request):
    if request.method == "POST":
        form = EmployeForm(request.POST)
        if form.is_valid():
            employe = form.save(commit=False)
            employe.save()
            return redirect('employe_detail', pk=employe.pk)
    else:
        form = EmployeForm()
    return render(request, 'Employe/employe_edit.html', {'form': form})

def employe_edit(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == "POST":
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            employe = form.save(commit=False)
            employe.save()
            return redirect('employe_detail', pk=employe.pk)
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'Employe/employe_edit.html', {'form': form})

def employe_delete(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    employe.delete()
    return redirect('employe_list')



def gestion_employe_list(request):
    query = request.GET.get('q')
    gestions = GestionDesEmployes.objects.all()

    if query:
        gestions = gestions.filter(employe__nom__icontains=query)  # Filtrer par le nom de l'employé

    return render(request, 'Gestion_Employe/gestion_employe_list.html', {'gestions': gestions})


def gerer_employe_new(request):
    form = GestionDesEmployesForm(request.POST or None)
    employe = None  # Initialize employe variable

    if request.method == 'POST' and form.is_valid():
        gestion = form.save(commit=False)
        employe = gestion.employe  # Set employe for context

        # Gérer les absences
        if form.cleaned_data['absence']:
            gestion.absences += 1
        # Gérer les avances sur salaire
        if gestion.avances_salaire is not None and  gestion.avances_salaire > 0:
            gestion.save()
            return redirect('pv_new')
        gestion.save()
        return redirect('gerer_employe_detail', employe_id=employe.id)


    return render(request, 'Gestion_Employe/Gestion_Employe_edit.html', {'form': form, 'employe': employe})


def gerer_employe_detail(request, employe_id):
    employe = get_object_or_404(Employe, pk=employe_id)
    gestions = GestionDesEmployes.objects.filter(employe=employe)
    return render(request, 'Gestion_Employe/Gestion_Employe_detail.html', {'employe': employe, 'gestions': gestions})


def gerer_employe_edit(request, gestion_id):
    gestion = get_object_or_404(GestionDesEmployes, pk=gestion_id)
    original_avances_salaire = gestion.avances_salaire  # Store the original value

    if request.method == "POST":
        form = GestionDesEmployesForm(request.POST, instance=gestion)
        if form.is_valid():
            updated_gestion = form.save(commit=False)

            if 'absence' in request.POST:
                updated_gestion.absences += 1

            # Check if avances_salaire value has changed
            if updated_gestion.avances_salaire != original_avances_salaire:
                updated_gestion.save()
                return redirect('pv_new')  # Redirect to pv_new if avances_salaire has changed

            updated_gestion.save()
            return redirect('gerer_employe_detail', employe_id=gestion.employe.id)

    else:
        form = GestionDesEmployesForm(instance=gestion)
    return render(request, 'Gestion_Employe/Gestion_Employe_edit.html', {'form': form})

def gerer_employe_delete(request, gestion_id):
    gestion = get_object_or_404(GestionDesEmployes, pk=gestion_id)
    employe_id = gestion.employe.id
    gestion.delete()
    return redirect('gestion_employe_list')


def pv_list(request):
    query = request.GET.get('q')
    pv = PV.objects.all()

    if query:
        pv = pv.filter(employe__nom__icontains=query)  # Filtrer par le nom de l'employé

    return render(request, 'PV/pv_list.html', {'pv': pv})


def pv_new(request):
    if request.method == 'POST':
        form = PVForm(request.POST)
        if form.is_valid():
            pv = form.save(commit=False)
            pv.save()
            return redirect('gestion_employe_list')
    else:
        form = PVForm()
    return render(request, 'PV/PV_new.html', {'form': form})


def Vente_centre_list(request):
    centre_id = request.GET.get('centre')
    noms_produits = []
    quantites = []

    if centre_id:
        ventes = CentreVente.objects.filter(centre__id=centre_id)
        centre = Centre.objects.get(id=centre_id)  # Récupérer l'instance du centre
        designation_centre = centre.designation
        if designation_centre == 'centre 1':
            produits_best_seller = Produit.objects.order_by('-nombre_vente1')[:10]
            noms_produits = [produit.designation for produit in produits_best_seller]
            quantites = [produit.nombre_vente1 for produit in produits_best_seller]
        elif designation_centre == 'centre 2':
            produits_best_seller = Produit.objects.order_by('-nombre_vente2')[:10]
            noms_produits = [produit.designation for produit in produits_best_seller]
            quantites = [produit.nombre_vente2 for produit in produits_best_seller]
        elif designation_centre == 'centre 3':
            produits_best_seller = Produit.objects.order_by('-nombre_vente3')[:10]
            noms_produits = [produit.designation for produit in produits_best_seller]
            quantites = [produit.nombre_vente3 for produit in produits_best_seller]
    else:#par defaut on affiche de centre1
        ventes = CentreVente.objects.all()
        produits_best_seller = Produit.objects.order_by('-nombre_vente1')[:10]
        noms_produits = [produit.designation for produit in produits_best_seller]
        quantites = [produit.nombre_vente1 for produit in produits_best_seller]

    total_montant_ventes = ventes.aggregate(Sum('montant_encaisse'))['montant_encaisse__sum'] or 0

    clients = Client.objects.all()
    centres = Centre.objects.all()

    

    
    plt.figure(figsize=(10, 6))
    plt.bar(noms_produits, quantites)
    plt.xlabel('Produits')
    plt.ylabel('Nombre de ventes')
    plt.title('Top 10 des produits best-sellers')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    graphique_filename = 'top10best_sellers_centre.png'
    graphique_path = f'gestionCentre/static/media/{graphique_filename}'
    plt.savefig(graphique_path)

    

    total_stock_value = {centre.designation: centre.total_stock_value for centre in centres}

    return render(request, 'Vente/Vente_centre_list.html', {
        'ventes': ventes,
        'clients': clients,
        'centres': centres,
        'total_stock_value': total_stock_value,
        'total_montant_ventes': total_montant_ventes,
        'graphique_filename': graphique_filename,
        'centre_id': centre_id  # Pass this to the template for preserving the selected center
    })

def Vente_centre_detail(request, pk):
    vente_instance = get_object_or_404(CentreVente, pk=pk)
    return render(request, 'Vente/vente_centre_detail.html', {'vente': vente_instance})

def Vente_centre_new(request):
    if request.method == "POST":
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)
            try:
                vente.full_clean()  # Validate the model (will trigger pre_save signal)
                vente.save()
                return redirect('vente_centre_detail', pk=vente.pk)
            except ValidationError as e:
                # Handle the validation error here
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
    else:
        form = VenteForm()

    return render(request, 'Vente/vente_centre_edit.html', {'form': form})

def Vente_centre_edit(request, pk):
    vente_instance = get_object_or_404(CentreVente, pk=pk)
    if request.method == "POST":
        form = VenteForm(request.POST, instance=vente_instance)
        if form.is_valid():
            vente_instance = form.save(commit=False)
            vente_instance.save()
            return redirect('vente_centre_detail', pk=vente_instance.pk)
    else:
        form = VenteForm(instance=vente_instance)
    return render(request, 'Vente/vente_centre_edit.html', {'form': form})

def Vente_centre_delete(request, pk):
    vente_instance = get_object_or_404(CentreVente, pk=pk)
    vente_instance.delete()
    return redirect('vente_centre_list')

def vente_centre_completer(request, pk):
    vente = get_object_or_404(CentreVente, pk=pk)
    if request.method == "POST":
        form = MontantAjouteForm(request.POST)
        if form.is_valid():
            montant_ajoute = form.cleaned_data['montant_ajoute']
            vente.montant_encaisse += montant_ajoute
            vente.save()  # La méthode save du modèle Vente ajuste le crédit du client
            return redirect('vente_centre_detail', pk=vente.pk)
    else:
        form = MontantAjouteForm()

    return render(request, 'Vente/vente_centre_completer.html', {'form': form, 'vente': vente, 'client': vente.client})


def etat_stock_centre(request):
    #query = request.GET.get('q')
    #date_debut = request.GET.get('date_debut')
    #date_fin = request.GET.get('date_fin')
    centre_id = request.GET.get('centre')

    if centre_id:
        try:
            centre_id = int(centre_id)  # Convert to integer, if possible
            etat_stock_query = CentreEtatStock.objects.filter(centre__id=centre_id)
        except ValueError:
            # Handle the case where centre_id is not a valid integer
            etat_stock_query = CentreEtatStock.objects.none()  # Or decide on another fallback
    else:
        etat_stock_query = CentreEtatStock.objects.all()  # Or handle this case as you see fit


    #if date_debut and date_fin:
        #start_date = parse_date(date_debut)
        #end_date = parse_date(date_fin)
        #if start_date and end_date:
            #etat_stock_query = etat_stock_query.filter(date_achat__range=[start_date, end_date])

    #if query:
        #etat_stock_query = etat_stock_query.filter(produit__designation__icontains=query)


    etat_stock_global = etat_stock_query.values('produit__designation').annotate(total_quantite=Sum('quantite'))

    noms_produits = [stock['produit__designation'] for stock in etat_stock_global]
    quantites = [stock['total_quantite'] for stock in etat_stock_global]

    plt.figure(figsize=(10, 6))
    plt.bar(noms_produits, quantites)
    plt.xlabel('Produits')
    plt.ylabel('Quantité')
    plt.title('État global du stock par produit')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    graphique_filename = 'etat_stock_centre_graph.png'
    graphique_path = f'gestionCentre/static/media/{graphique_filename}'
    plt.savefig(graphique_path)

    centres=Centre.objects.all()

    # Rendu de la vue avec la valeur totale du stock
    return render(request, 'EtatStock/etat_centre_stock.html', {
        'etat_stock_global': etat_stock_global,
        'graphique_filename': graphique_filename,
        'centres':centres,
         # Pass total stock value to the template
    })

def home(request):
    return render(request, 'homeG.html')