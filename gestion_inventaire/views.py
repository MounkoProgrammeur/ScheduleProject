from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Salle, Equipement
from .forms import FormulaireSalle, FormulaireEquipement

def est_admin_ou_planificateur(user):
    return user.is_authenticated and user.profile.role in ['ADMIN', 'PLANIFICATEUR']

@login_required
def liste_salles(request):
    salles = Salle.objects.all()
    return render(request, 'gestion_inventaire/liste_salles.html', {'salles': salles})

@login_required
@user_passes_test(est_admin_ou_planificateur)
def creer_salle(request):
    if request.method == 'POST':
        formulaire = FormulaireSalle(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            return redirect('gestion_inventaire:liste_salles')
    else:
        formulaire = FormulaireSalle()
    return render(request, 'gestion_inventaire/formulaire_salle.html', {'formulaire': formulaire})

@login_required
def liste_equipements(request):
    equipements = Equipement.objects.all()
    return render(request, 'gestion_inventaire/liste_equipements.html', {'equipements': equipements})

@login_required
@user_passes_test(est_admin_ou_planificateur)
def creer_equipement(request):
    if request.method == 'POST':
        formulaire = FormulaireEquipement(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            return redirect('gestion_inventaire:liste_equipements')
    else:
        formulaire = FormulaireEquipement()
    return render(request, 'gestion_inventaire/formulaire_equipement.html', {'formulaire': formulaire})