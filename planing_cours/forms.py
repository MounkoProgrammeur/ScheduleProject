from django import forms
from .models import Cours

class FormulaireCours(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['sujet', 'enseignant', 'groupe', 'duree', 'frequence', 'equipements_requis']
        labels = {
            'sujet': 'Sujet du cours',
            'enseignant': 'Enseignant',
            'groupe': 'Groupe d\'étudiants',
            'duree': 'Durée (heures)',
            'frequence': 'Fréquence',
            'equipements_requis': 'Équipements requis',
        }
        widgets = {
            'equipements_requis': forms.CheckboxSelectMultiple,
        }