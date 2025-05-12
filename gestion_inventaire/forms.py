from django import forms
from .models import Salle, Equipement

class FormulaireSalle(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'batiment', 'etage', 'type_salle', 'capacite', 'notes']
        labels = {
            'nom': 'Nom de la salle',
            'batiment': 'Bâtiment',
            'etage': 'Étage',
            'type_salle': 'Type de salle',
            'capacite': 'Capacité',
            'notes': 'Notes',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class FormulaireEquipement(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = ['nom', 'description', 'est_mobile', 'salles']
        labels = {
            'nom': 'Nom de l\'équipement',
            'description': 'Description',
            'est_mobile': 'Équipement mobile',
            'salles': 'Salles associées',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'salles': forms.CheckboxSelectMultiple,
        }