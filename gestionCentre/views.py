from django.shortcuts import render, get_object_or_404, redirect
from .models import Centre, Employe
from .forms import CentreForm, EmployeForm


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
    return render(request, 'Employe/employe_detail.html', {'employe': employe})

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





