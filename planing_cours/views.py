from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cours, EmploiDuTemps, Enseignant, GroupeEtudiants
from .forms import FormulaireCours
from .scheduler import generer_emploi_du_temps
from datetime import datetime

def est_planificateur_ou_admin(user):
    return user.is_authenticated and user.profil.role in ['ADMIN', 'PLANIFICATEUR']

@login_required
@user_passes_test(est_planificateur_ou_admin)
def liste_cours(request):
    cours = Cours.objects.all()
    return render(request, 'planning_cours/liste_cours.html', {'cours': cours})

@login_required
@user_passes_test(est_planificateur_ou_admin)
def creer_cours(request):
    if request.method == 'POST':
        formulaire = FormulaireCours(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            return redirect('planning_cours:liste_cours')
    else:
        formulaire = FormulaireCours()
    return render(request, 'planning_cours/formulaire_cours.html', {'formulaire': formulaire})

@login_required
@user_passes_test(est_planificateur_ou_admin)
def generer_emplois(request):
    if request.method == 'POST':
        date_debut = datetime.strptime(request.POST['date_debut'], '%Y-%m-%d')
        date_fin = datetime.strptime(request.POST['date_fin'], '%Y-%m-%d')
        cours = Cours.objects.all()
        succes = generer_emploi_du_temps(cours, date_debut, date_fin)
        if succes:
            return redirect('visualisation_emploi:tableau_bord')
        return render(request, 'planning_cours/erreur_planification.html')
    return render(request, 'planning_cours/formulaire_planification.html')