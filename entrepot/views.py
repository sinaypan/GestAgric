
from django.shortcuts import render, get_object_or_404, redirect
from .models import Fournisseur, Produit, Achat, Transfert, Vente ,EtatStock
from .forms import FournisseurForm, ProduitForm, AchatForm, TransfertForm,VenteForm,MontantAjouteForm
from django.utils.dateparse import parse_date
from utilisateur.models import Client
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, DecimalField
import matplotlib.pyplot as plt


def fournisseur_list(request):
    query = request.GET.get('q')
    fournisseurs = Fournisseur.objects.all()

    if query:
        fournisseurs = fournisseurs.filter(nom__icontains=query)  # Filtrer par le champ 'nom'

    return render(request, 'Fournisseur/fournisseur_list.html', {'fournisseurs': fournisseurs})


def fournisseur_detail(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    return render(request, 'Fournisseur/fournisseur_detail.html', {'fournisseur': fournisseur})

def fournisseur_new(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST)
        if form.is_valid():
            fournisseur = form.save(commit=False)
            fournisseur.save()
            return redirect('fournisseur_detail', pk=fournisseur.pk)
    else:
        form = FournisseurForm()
    return render(request, 'Fournisseur/fournisseur_edit.html', {'form': form})

def fournisseur_edit(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == "POST":
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            fournisseur = form.save(commit=False)
            fournisseur.save()
            return redirect('fournisseur_detail', pk=fournisseur.pk)
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'Fournisseur/fournisseur_edit.html', {'form': form})

def fournisseur_delete(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    fournisseur.delete()
    return redirect('fournisseur_list')

# Vues similaires pour les autres entités (Produit, Client) avec les opérations CRUD


def produit_list(request):
    query = request.GET.get('q')
    produits = Produit.objects.all()

    if query:
        produits = produits.filter(designation__icontains=query)  # Filtrer par le champ 'designation'

    return render(request, 'Produit/produit_list.html', {'produits': produits})

def produit_detail(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    return render(request, 'Produit/produit_detail.html', {'produit': produit})

def produit_new(request):
    if request.method == "POST":
        form = ProduitForm(request.POST)
        if form.is_valid():
            produit = form.save()  # Sauvegarder le produit en premier

            nom_produit = produit.designation  # Utilisation du champ 'designation'

            # Vérifier si le produit existe déjà dans l'état du stock
            produit_existant = EtatStock.objects.filter(produit__designation=nom_produit).first()

            if produit_existant:
                # Le produit existe déjà dans l'état du stock, augmenter la quantité de 1
                produit_existant.quantite += 1
                produit_existant.save()
            else:
                # Le produit n'existe pas dans l'état du stock, créer un nouvel enregistrement
                # dans l'état du stock avec une quantité de 1
                nouvel_etat_stock = EtatStock.objects.create(produit=produit, quantite=1)

            return redirect('produit_detail', pk=produit.pk)
    else:
        form = ProduitForm()
    return render(request, 'Produit/produit_edit.html', {'form': form})

def produit_edit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == "POST":
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.save()
            return redirect('produit_detail', pk=produit.pk)
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'Produit/produit_edit.html', {'form': form})

def produit_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    produit.delete()
    return redirect('produit_list')


def Achat_list(request):
    query = request.GET.get('q')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    fournisseur_id = request.GET.get('fournisseur')

    Achats = Achat.objects.all()

    if date_debut and date_fin:
        # Conversion des chaînes de date en objets date
        start_date = parse_date(date_debut)
        end_date = parse_date(date_fin)
        if start_date and end_date:
            # Filtrer les achats dans la plage de dates
            Achats = Achats.filter(date_achat__range=[start_date, end_date])

    if query:
        Achats = Achats.filter(produit__designation__icontains=query)

    if fournisseur_id:
        Achats = Achats.filter(fournisseur__id=fournisseur_id)

    fournisseurs = Fournisseur.objects.all()

    # Calcul du montant total des achats
    total_montant_achats = Achats.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0

    return render(request, 'Achat/Achat_list.html', {
        'Achats': Achats,
        'fournisseurs': fournisseurs,
        'total_montant_achats': total_montant_achats
    })



def Achat_detail(request, pk):
    achat_instance = get_object_or_404(Achat, pk=pk)
    return render(request, 'Achat/Achat_detail.html', {'Achat': achat_instance})


def Achat_new(request):
    if request.method == "POST":
        form = AchatForm(request.POST)
        if form.is_valid():
            achat = form.save()  # Sauvegarde de l'objet Achat
            return redirect('achat_detail', pk=achat.pk)
    else:
        form = AchatForm()

    
    return render(request, 'Achat/achat_edit.html', {'form': form})

def fournisseur_new1(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST)
        if form.is_valid():
            fournisseur = form.save(commit=False)
            fournisseur.save()
            return redirect('achat_new')
    else:
        form = FournisseurForm()
    return render(request, 'Fournisseur/fournisseur_edit1.html', {'form': form})

def produit_new1(request):
    if request.method == "POST":
        form = ProduitForm(request.POST)
        if form.is_valid():
            new_produit = form.save(commit=False)
            new_produit.save()
            return redirect('achat_new')
    else:
        form = ProduitForm()
    return render(request, 'Produit/produit_edit1.html', {'form': form})


def Achat_edit(request, pk):
    achat_instance = get_object_or_404(Achat, pk=pk)
    if request.method == "POST":
        form = AchatForm(request.POST, instance=achat_instance)
        if form.is_valid():
            achat_instance = form.save(commit=False)
            achat_instance.save()
            return redirect('achat_detail', pk=achat_instance.pk)
    else:
        form = AchatForm(instance=achat_instance)
    return render(request, 'Achat/achat_edit.html', {'form': form})

def Achat_delete(request, pk):
    achat_instance = get_object_or_404(Achat, pk=pk)
    achat_instance.delete()
    return redirect('achat_list')

    


def Transfert_list(request):
    query = request.GET.get('q')
    
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    transferts = Transfert.objects.all()

    if date_debut and date_fin:
        # Conversion des chaînes de date en objets date
        start_date = parse_date(date_debut)
        end_date = parse_date(date_fin)
        if start_date and end_date:
            # Filtrer les transferts dans la plage de dates
            transferts = transferts.filter(date_transfert__range=[start_date, end_date])

    if query:
        transferts = transferts.filter(produit__designation__icontains=query)  # Filtrez par le nom du produit si nécessaire

    return render(request, 'Transfert/transfert_list.html', {'transferts': transferts})


def Transfert_detail(request, pk):
    transfert_instance = get_object_or_404(Transfert, pk=pk)
    return render(request, 'Transfert/transfert_detail.html', {'transfert': transfert_instance})

def Transfert_new(request):
    if request.method == "POST":
        form = TransfertForm(request.POST)
        if form.is_valid():
            transfert = form.save(commit=False)
            transfert.save()
            return redirect('transfert_detail', pk=transfert.pk)
    else:
        form = TransfertForm()
    return render(request, 'Transfert/transfert_edit.html', {'form': form})

def Transfert_edit(request, pk):
    transfert_instance = get_object_or_404(Transfert, pk=pk)
    if request.method == "POST":
        form = TransfertForm(request.POST, instance=transfert_instance)
        if form.is_valid():
            transfert_instance = form.save(commit=False)
            transfert_instance.save()
            return redirect('transfert_detail', pk=transfert_instance.pk)
    else:
        form = TransfertForm(instance=transfert_instance)
    return render(request, 'Transfert/transfert_edit.html', {'form': form})

def Transfert_delete(request, pk):
    transfert_instance = get_object_or_404(Transfert, pk=pk)
    transfert_instance.delete()
    return redirect('transfert_list')



def Vente_list(request):
    query = request.GET.get('q')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    client_id = request.GET.get('client')

    ventes = Vente.objects.all()

    if date_debut and date_fin:
        # Conversion des chaînes de date en objets date
        start_date = parse_date(date_debut)
        end_date = parse_date(date_fin)
        if start_date and end_date:
            # Filtrer les achats dans la plage de dates
            ventes = ventes.filter(date_vente__range=[start_date, end_date])

    if query:
        ventes = ventes.filter(produit__nom__icontains=query)  # Filtrez par le nom du produit si nécessaire

    if client_id:
        ventes = ventes.filter(client__id=client_id)
    
    # Calcul du montant total des achats
    total_montant_ventes = ventes.aggregate(Sum('montant_encaisse'))['montant_encaisse__sum'] or 0

    clients = Client.objects.all()
    return render(request, 'Vente/vente_list.html', {'ventes': ventes, 'clients': clients, 'total_montant_ventes':total_montant_ventes})


def Vente_detail(request, pk):
    vente_instance = get_object_or_404(Vente, pk=pk)
    return render(request, 'Vente/vente_detail.html', {'vente': vente_instance})

def Vente_new(request):
    if request.method == "POST":
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)
            vente.save()
            return redirect('vente_detail', pk=vente.pk)
    else:
        form = VenteForm()
    return render(request, 'Vente/vente_edit.html', {'form': form})

def Vente_edit(request, pk):
    vente_instance = get_object_or_404(Vente, pk=pk)
    if request.method == "POST":
        form = VenteForm(request.POST, instance=vente_instance)
        if form.is_valid():
            vente_instance = form.save(commit=False)
            vente_instance.save()
            return redirect('vente_detail', pk=vente_instance.pk)
    else:
        form = VenteForm(instance=vente_instance)
    return render(request, 'Vente/vente_edit.html', {'form': form})

def Vente_delete(request, pk):
    vente_instance = get_object_or_404(Vente, pk=pk)
    vente_instance.delete()
    return redirect('vente_list')

def vente_completer(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    if request.method == "POST":
        form = MontantAjouteForm(request.POST)
        if form.is_valid():
            montant_ajoute = form.cleaned_data['montant_ajoute']
            vente.montant_encaisse += montant_ajoute
            vente.save()  # La méthode save du modèle Vente ajuste le crédit du client
            return redirect('vente_detail', pk=vente.pk)
    else:
        form = MontantAjouteForm()

    return render(request, 'Vente/vente_completer.html', {'form': form, 'vente': vente, 'client': vente.client})


def etat_stock(request):
    query = request.GET.get('q')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    fournisseur_id = request.GET.get('fournisseur')

    etat_stock_query = EtatStock.objects.all()

    if date_debut and date_fin:
        start_date = parse_date(date_debut)
        end_date = parse_date(date_fin)
        if start_date and end_date:
            etat_stock_query = etat_stock_query.filter(date_achat__range=[start_date, end_date])

    if query:
        etat_stock_query = etat_stock_query.filter(produit__designation__icontains=query)

    if fournisseur_id:
        etat_stock_query = etat_stock_query.filter(fournisseur__id=fournisseur_id)

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

    graphique_filename = 'etat_stock_graph.png'
    graphique_path = f'entrepot/static/media/{graphique_filename}'
    plt.savefig(graphique_path)

    fournisseurs = Fournisseur.objects.all()

    for stock in etat_stock_global:
        produit_designation = stock['produit__designation']
    
        # Retrieve all purchases for this product
        purchases = Achat.objects.filter(produit__designation=produit_designation)
        
        # Calculate total quantity for this product
        total_quantite = stock['total_quantite']
        
        # Calculate total value for this product based on purchases
        total_value = sum(purchase.quantite * purchase.prix_unitaire_HT for purchase in purchases)
        stock['total_value'] = total_value

# Retrieve the total value of the entire stock
    total_stock_value = sum(stock['total_value'] for stock in etat_stock_global)

# ... (existing code remains unchanged)

# Rendu de la vue avec la valeur totale du stock
    return render(request, 'EtatStock/etat_stock.html', {
        'etat_stock_global': etat_stock_global,
        'graphique_filename': graphique_filename,
        'fournisseurs': fournisseurs,
        'total_stock_value': total_stock_value,  # Pass total stock value to the template
    })