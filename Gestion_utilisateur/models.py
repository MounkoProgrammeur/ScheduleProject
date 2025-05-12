from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    ROLES = (
        ('ADMIN', 'Administrateur'),
        ('PLANIFICATEUR', 'Planificateur'),
        ('CONSULTANT', 'Consultant'),
    )
    
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Utilisateur')
    role = models.CharField(max_length=20, choices=ROLES, default='CONSULTANT', verbose_name='Rôle')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.role}"

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'