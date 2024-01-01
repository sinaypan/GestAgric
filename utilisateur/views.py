from django.shortcuts import render, get_object_or_404, redirect
from .models import Client
from .forms import ClientForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
import matplotlib.pyplot as plt
from django.db.models import Sum


def client_list(request):
    query = request.GET.get('q')
    clients = Client.objects.all()
    if query:
        clients = clients.filter(nom__icontains=query)

     # Récupérer les 10 clients ayant dépensé le plus
    clients_top_depense = Client.objects.order_by('-prix_total_depense_par_client')[:10]

    # Extraire les noms des clients et leurs dépenses totales
    noms_clients = [client.nom for client in clients_top_depense]
    depenses = [client.prix_total_depense_par_client for client in clients_top_depense]

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.bar(noms_clients, depenses)
    plt.xlabel('Clients')
    plt.ylabel('Dépenses totales')
    plt.title('Top 10 des clients ayant dépensé le plus')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Sauvegarder le graphique
    graphique_filename = 'top10_clients_depense.png'
    graphique_path = f'utilisateur/static/media/{graphique_filename}'
    plt.savefig(graphique_path)

    # Rendre le graphique accessible dans le contexte du template
    graphique_url = f'/static/media/{graphique_filename}'

    return render(request, 'Client/client_list.html', {
        'clients': clients,
        'graphique_url': graphique_url,  # Envoyer l'URL du graphique au template
    })

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'Client/client_detail.html', {'client': client})

def client_new(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()
    return render(request, 'Client/client_edit.html', {'form': form})

def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'Client/client_edit.html', {'form': form})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('client_list')



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('register_user')  # Change this to the correct URL after login
        else:
            messages.error(request, "There was an error logging in. Please try again.")
            return redirect('login')
    else:
        return render(request, 'authentification/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out!")
    return redirect('produit_list')  # Change this to the correct URL after logout

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.adresse = form.cleaned_data['adresse']
            user.telephone = form.cleaned_data['telephone']
            user.credit = form.cleaned_data['credit']
            user.save()

            # Création du client associé à l'utilisateur
            Client.objects.create(
                user=user,
                code=f"Code-{user.username}",  # Vous pouvez adapter la génération du code
                nom=user.get_full_name(),
                adresse=user.adresse,
                telephone=user.telephone,
                credit=user.credit
            )

            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect('login')  # Redirection vers la page de connexion après l'inscription
    else:
        form = RegisterUserForm()

    return render(request, 'authentification/register_user.html', {'form': form})