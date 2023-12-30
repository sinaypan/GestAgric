from django.shortcuts import render, get_object_or_404, redirect
from .models import Client
from .forms import ClientForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def client_list(request):
    query = request.GET.get('q')
    clients = Client.objects.all()
    if query:
        clients = clients.filter(nom__icontains=query)
    return render(request, 'Client/client_list.html', {'clients': clients})

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