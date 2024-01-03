from django.shortcuts import render, get_object_or_404, redirect
from .models import Centre, Employe,GestionDesEmployes
from .forms import CentreForm, EmployeForm,GestionDesEmployesForm,PVForm
from .utilities import calculer_salaire_mensuel

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
    return render(request, 'Centre/centre_detail.html', {'centre': centre})

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
        if gestion.avances_salaire > 0:
            gestion.avances_salaire += gestion.avances_salaire
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
