from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from planing_cours.models import EmploiDuTemps
from gestion_inventaire.models import Salle
from django.utils import timezone
from datetime import timedelta

@login_required
def tableau_bord(request):
    emplois = EmploiDuTemps.objects.filter(debut__gte=timezone.now())
    salles = Salle.objects.all()
    return render(request, 'visualisation_emploi/tableau_bord.html', {'emplois': emplois, 'salles': salles})

@login_required
def calendrier(request):
    emplois = EmploiDuTemps.objects.all()
    evenements = [
        {
            'titre': f"{emploi.cours.sujet} ({emploi.salle.nom})",
            'debut': emploi.debut.isoformat(),
            'fin': emploi.fin.isoformat(),
        } for emploi in emplois
    ]
    return render(request, 'visualisation_emploi/calendrier.html', {'evenements': evenements})

@login_required
def disponibilite_salles(request):
    if request.method == 'POST':
        date = request.POST['date']
        heure_debut = request.POST['heure_debut']
        capacite = int(request.POST.get('capacite', 0))
        salles = Salle.objects.filter(capacite__gte=capacite)
        salles_disponibles = []
        debut_datetime = timezone.datetime.strptime(f"{date} {heure_debut}", '%Y-%m-%d %H:%M')
        fin_datetime = debut_datetime + timedelta(hours=1)
        for salle in salles:
            if not EmploiDuTemps.objects.filter(
                salle=salle,
                debut__lt=fin_datetime,
                fin__gt=debut_datetime
            ).exists():
                salles_disponibles.append(salle)
        return render(request, 'visualisation_emploi/disponibilite_salles.html', {'salles': salles_disponibles})
    return render(request, 'visualisation_emploi/disponibilite_salles.html')