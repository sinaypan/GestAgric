
from django.shortcuts import render, get_object_or_404, redirect
from .models import Fournisseur, Produit, Achat, Transfert, Vente ,EtatStock,StockManager
from .forms import FournisseurForm, ProduitForm, AchatForm, TransfertForm,VenteForm,MontantAjouteForm
from django.utils.dateparse import parse_date
from utilisateur.models import Client
from django.db.models import Sum, FloatField
from django.db.models import F, ExpressionWrapper, DecimalField
import matplotlib.pyplot as plt


def fournisseur_list(request):
    query = request.GET.get('q')
    fournisseurs = Fournisseur.objects.all()

    # Filtrer les fournisseurs par nom s'il y a une requête
    if query:
        fournisseurs = fournisseurs.filter(nom__icontains=query)

    # Récupérer les 10 fournisseurs avec le plus grand total de dépenses
    fournisseurs_top_depense = fournisseurs.order_by('-prix_total_depense_chez_fournisseur')[:10]

    # Extraire les noms des fournisseurs et leurs dépenses totales
    noms_fournisseurs = [fournisseur.nom for fournisseur in fournisseurs_top_depense]
    depenses = [fournisseur.prix_total_depense_chez_fournisseur for fournisseur in fournisseurs_top_depense]

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.bar(noms_fournisseurs, depenses)
    plt.xlabel('Fournisseurs')
    plt.ylabel('Total des dépenses')
    plt.title('Top 10 des fournisseurs ayant le plus de dépenses')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Sauvegarder le graphique
    graphique_filename = 'top10_fournisseurs_depense.png'
    graphique_path = f'entrepot/static/media/{graphique_filename}'
    plt.savefig(graphique_path)

    # Rendre le graphique accessible dans le contexte du template
    graphique_url = f'/static/media/{graphique_filename}'

    return render(request, 'Fournisseur/fournisseur_list.html', {
        'fournisseurs': fournisseurs,
        'graphique_url': graphique_url,  # Envoyer l'URL du graphique au template
    })

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
    total_montant_achats_payer = Achats.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
    total_montant_achats = Achat.objects.aggregate(
    total=Sum(F('prix_unitaire_HT') * F('quantite'), output_field=FloatField())
)['total'] or 0

    return render(request, 'Achat/Achat_list.html', {
        'Achats': Achats,
        'fournisseurs': fournisseurs,
        'total_montant_achats_payer': total_montant_achats_payer,
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
    achats=Achat.objects.all()

    if date_debut and date_fin:
        start_date = parse_date(date_debut)
        end_date = parse_date(date_fin)
        if start_date and end_date:
            ventes = ventes.filter(date_vente__range=[start_date, end_date])
            achats = achats.filter(date_achat__range=[start_date, end_date])


    if query:
        ventes = ventes.filter(produit__designation__icontains=query)
        achats = achats.filter(produit__designation__icontains=query)

    if client_id:
        ventes = ventes.filter(client__id=client_id)
        achats = achats.filter(produit__designation__icontains=query)
    
    total_montant_ventes = ventes.aggregate(Sum('montant_encaisse'))['montant_encaisse__sum'] or 0

    clients = Client.objects.all()

    # Récupérer les 10 produits les plus vendus
    produits_best_seller = Produit.objects.order_by('-nombre_vente')[:10]

    # Extraire les noms des produits et les quantités vendues
    noms_produits = [produit.designation for produit in produits_best_seller]
    quantites = [produit.nombre_vente for produit in produits_best_seller]

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.bar(noms_produits, quantites)
    plt.xlabel('Produits')
    plt.ylabel('Nombre de ventes')
    plt.title('Top 10 des produits best-sellers ')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Sauvegarder le graphique
    graphique_filename = 'top10best-sellers.png'
    graphique_path = f'entrepot/static/media/{graphique_filename}'
    plt.savefig(graphique_path)

    # Rendre le graphique accessible dans le contexte du template
    graphique_url = f'/static/media/{graphique_filename}'

    total_stock_value=StockManager.total_stock_value
    total_montant_ventes = ventes.aggregate(Sum('montant_encaisse'))['montant_encaisse__sum'] or 0
    total_montant_achats_payer = achats.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0

    total_benefice = total_montant_ventes - total_montant_achats_payer

    return render(request, 'Vente/vente_list.html', {
        'ventes': ventes,
        'clients': clients,
        'total_stock_value': total_stock_value,
        'total_montant_ventes': total_montant_ventes,
        'total_benefice': total_benefice,
        'graphique_url': graphique_url, 
    })

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
        
    total_stock_value = StockManager.total_stock_value  # Récupérez la valeur totale mise à jour

    # Rendu de la vue avec la valeur totale du stock
    return render(request, 'EtatStock/etat_stock.html', {
        'etat_stock_global': etat_stock_global,
        'graphique_filename': graphique_filename,
        'fournisseurs': fournisseurs,
        'total_stock_value': total_stock_value,  # Pass total stock value to the template
    })