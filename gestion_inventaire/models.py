from django.db import models

class Batiment(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom')
    adresse = models.TextField(verbose_name='Adresse')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Bâtiment'
        verbose_name_plural = 'Bâtiments'

class Salle(models.Model):
    TYPES_SALLE = (
        ('COURS', 'Salle de cours'),
        ('AMPHI', 'Amphithéâtre'),
        ('LABO', 'Laboratoire'),
        ('BUREAU', 'Bureau'),
        ('REUNION', 'Salle de réunion'),
    )
    
    nom = models.CharField(max_length=100, verbose_name='Nom')
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='salles', verbose_name='Bâtiment')
    etage = models.IntegerField(verbose_name='Étage')
    type_salle = models.CharField(max_length=20, choices=TYPES_SALLE, verbose_name='Type de salle')
    capacite = models.PositiveIntegerField(verbose_name='Capacité')
    notes = models.TextField(blank=True, verbose_name='Notes')

    def __str__(self):
        return f"{self.nom} ({self.batiment.nom})"

    class Meta:
        verbose_name = 'Salle'
        verbose_name_plural = 'Salles'

class Equipement(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom')
    description = models.TextField(blank=True, verbose_name='Description')
    est_mobile = models.BooleanField(default=False, verbose_name='Est mobile')
    salles = models.ManyToManyField(Salle, related_name='equipements', blank=True, verbose_name='Salles')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Équipement'
        verbose_name_plural = 'Équipements'