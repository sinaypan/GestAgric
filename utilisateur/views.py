from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, UserProfile
from .forms import ClientForm, VerificationCodeForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
import matplotlib.pyplot as plt
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages
from django.core.mail import send_mail

from django.urls import reverse
import random



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
            if user.is_active:
                login(request, user)
                return redirect(reverse('entrepot:home'))  # Change this to the correct URL after login
            else:
                messages.warning(request, "Votre compte n'est pas encore vérifié. Veuillez vérifier votre email.")
                return redirect(reverse('verify_user'))
        else:
            messages.error(request, "There was an error logging in. Please try again.")
            return redirect('logout')
    else:
        return render(request, 'authentification/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out!")
    return redirect('home')  # Change this to the correct URL after logout

def register_user(request):
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.adresse = form.cleaned_data['adresse']
            user.telephone = form.cleaned_data['telephone']
            user.is_active = False  # User is not active until email is verified
            user.save()

            # Create a user profile with a verification code
            user_profile = UserProfile.objects.create(user=user, adresse=form.cleaned_data['adresse'], telephone=form.cleaned_data['telephone'])
            verification_code = generate_verification_code()
            user_profile.verification_code = verification_code
            user_profile.save()

            # Send the verification email
            send_verification_email(user.email, verification_code)

            messages.success(request, "Inscription réussie ! Un email de confirmation a été envoyé.")
            return redirect('verify_user', user_profile_id=user_profile.pk)

    return render(request, 'authentification/register_user.html', {'form': form})

def generate_verification_code():
    # Generate a random 4-digit verification code
    return str(random.randint(1000, 9999))

def send_verification_email(email, verification_code):
    # Implement a function to send the verification code via email
    subject = 'Confirmation de compte'
    message = f'Votre code de vérification est : {verification_code}'
    from_email = 'projetyanrah@gmail.com'  # Set your email address
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def verify_user(request, user_profile_id):
    user_profile = get_object_or_404(UserProfile, pk=user_profile_id)

    if request.method == "POST":
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']

            if verification_code == user_profile.verification_code:
                user_profile.user.is_active = True
                user_profile.user.save()
                login(request, user_profile.user)
                messages.success(request, "Votre compte a été vérifié avec succès.")
                return redirect('login')  # Redirect to home or profile page
            else:
                messages.error(request, "Code de vérification incorrect. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez fournir un code de vérification valide.")
    else:
        form = VerificationCodeForm()

    return render(request, 'authentification/verify_user.html', {'form': form})

def home(request):
    return render(request, 'homeU.html')