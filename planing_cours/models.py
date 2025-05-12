from django.db import models
from gestion_inventaire.models import Salle, Equipement
from Gestion_utilisateur.models import Profil

class Enseignant(models.Model):
    profil = models.OneToOneField(Profil, on_delete=models.CASCADE, verbose_name='Profil')
    nom = models.CharField(max_length=100, verbose_name='Nom')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Enseignant'
        verbose_name_plural = 'Enseignants'

class GroupeEtudiants(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom')
    taille = models.PositiveIntegerField(verbose_name='Taille')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Groupe d\'étudiants'
        verbose_name_plural = 'Groupes d\'étudiants'

class Cours(models.Model):
    sujet = models.CharField(max_length=100, verbose_name='Sujet')
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, verbose_name='Enseignant')
    groupe = models.ForeignKey(GroupeEtudiants, on_delete=models.CASCADE, verbose_name='Groupe')
    duree = models.PositiveIntegerField(verbose_name='Durée (heures)')
    frequence = models.CharField(max_length=20, choices=[('HEBDOMADAIRE', 'Hebdomadaire'), ('UNIQUE', 'Unique')], verbose_name='Fréquence')
    equipements_requis = models.ManyToManyField(Equipement, blank=True, verbose_name='Équipements requis')

    def __str__(self):
        return f"{self.sujet} ({self.groupe.nom})"

    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

class EmploiDuTemps(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, verbose_name='Cours')
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, verbose_name='Salle')
    debut = models.DateTimeField(verbose_name='Début')
    fin = models.DateTimeField(verbose_name='Fin')

    def __str__(self):
        return f"{self.cours.sujet} dans {self.salle.nom} à {self.debut}"

    class Meta:
        verbose_name = 'Emploi du temps'
        verbose_name_plural = 'Emplois du temps'