from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Profil
from .forms import FormulaireProfil

def est_admin(user):
    return user.is_authenticated and user.profil.role == 'ADMIN'

@login_required
def profil(request):
    return render(request, 'gestion_utilisateur/profil.html', {'profil': request.user.profil})

@login_required
@user_passes_test(est_admin)
def liste_utilisateurs(request):
    utilisateurs = User.objects.all()
    return render(request, 'gestion_utilisateur/liste_utilisateurs.html', {'utilisateurs': utilisateurs})

@login_required
@user_passes_test(est_admin)
def modifier_utilisateur(request, pk):
    utilisateur = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        formulaire = FormulaireProfil(request.POST, instance=utilisateur.profil)
        if formulaire.is_valid():
            formulaire.save()
            return redirect('gestion_utilisateur:liste_utilisateurs')
    else:
        formulaire = FormulaireProfil(instance=utilisateur.profil)
    return render(request, 'gestion_utilisateur/formulaire_utilisateur.html', {'formulaire': formulaire, 'utilisateur': utilisateur})