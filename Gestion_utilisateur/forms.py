from django import forms
from .models import Profil

class FormulaireProfil(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['role']
        labels = {
            'role': 'Rôle',
        }