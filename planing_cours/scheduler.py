from ortools.sat.python import cp_model
from datetime import datetime, timedelta
from .models import Cours, Salle, EmploiDuTemps, Enseignant, GroupeEtudiants
from gestion_inventaire.models import Equipement

def generer_emploi_du_temps(cours, date_debut, date_fin):
    modele = cp_model.CpModel()
    solveur = cp_model.CpSolver()

    # Définir les créneaux horaires (8h à 18h, créneaux d'1h, lundi à vendredi)
    creneaux = []
    date_actuelle = date_debut
    while date_actuelle <= date_fin:
        if date_actuelle.weekday() < 5:  # Lundi à vendredi
            heure_actuelle = date_actuelle.replace(hour=8, minute=0)
            while heure_actuelle <= date_actuelle.replace(hour=18, minute=0):
                creneaux.append(heure_actuelle)
                heure_actuelle += timedelta(hours=1)
        date_actuelle += timedelta(days=1)
    
    salles = Salle.objects.all()
    emplois = {}

    # Créer des variables pour chaque cours
    for cours_item in cours:
        emplois[cours_item.id] = {}
        for salle in salles:
            for creneau in creneaux:
                nom_var = f"cours_{cours_item.id}_salle_{salle.id}_creneau_{creneau.isoformat()}"
                emplois[cours_item.id][(salle.id, creneau)] = modele.NewBoolVar(nom_var)

    # Contraintes
    for cours_item in cours:
        # Chaque cours doit être planifié selon sa fréquence
        if cours_item.frequence == 'HEBDOMADAIRE':
            # Planifier une fois par semaine pour le semestre
            nombre_semaines = (date_fin - date_debut).days // 7 + 1
            modele.Add(sum(emplois[cours_item.id][(salle.id, creneau)] 
                          for salle in salles for creneau in creneaux) == nombre_semaines)
        else:
            modele.Add(sum(emplois[cours_item.id][(salle.id, creneau)] 
                          for salle in salles for creneau in creneaux) == 1)
        
        # Capacité de la salle
        for salle in salles:
            if salle.capacite < cours_item.groupe.taille:
                for creneau in creneaux:
                    modele.Add(emplois[cours_item.id][(salle.id, creneau)] == 0)
        
        # Exigences d'équipement
        for eq in cours_item.equipements_requis.all():
            for salle in salles:
                if eq not in salle.equipements.all():
                    for creneau in creneaux:
                        modele.Add(emplois[cours_item.id][(salle.id, creneau)] == 0)
        
        # Disponibilité de l'enseignant
        for autre_cours in cours:
            if autre_cours != cours_item and autre_cours.enseignant == cours_item.enseignant:
                for salle in salles:
                    for autre_salle in salles:
                        for creneau in creneaux:
                            modele.Add(emplois[cours_item.id][(salle.id, creneau)] + 
                                      emplois[autre_cours.id][(autre_salle.id, creneau)] <= 1)

    # Occupation des salles
    for salle in salles:
        for creneau in creneaux:
            modele.Add(sum(emplois[cours_item.id][(salle.id, creneau)] for cours_item in cours) <= 1)

    # Résoudre
    statut = solveur.Solve(modele)
    if statut == cp_model.FEASIBLE or statut == cp_model.OPTIMAL:
        EmploiDuTemps.objects.all().delete()  # Supprimer les emplois existants
        for cours_item in cours:
            for salle in salles:
                for creneau in creneaux:
                    if solveur.Value(emplois[cours_item.id][(salle.id, creneau)]):
                        EmploiDuTemps.objects.create(
                            cours=cours_item,
                            salle=salle,
                            debut=creneau,
                            fin=creneau + timedelta(hours=cours_item.duree)
                        )
        return True
    return False