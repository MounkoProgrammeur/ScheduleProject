from django.contrib import admin
from django.utils.html import format_html
from .models import Enseignant, GroupeEtudiants, Cours, EmploiDuTemps

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'profil', 'nombre_cours')
    search_fields = ('nom', 'profil__utilisateur__username')
    list_per_page = 20
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'profil')
        }),
    )

    def nombre_cours(self, obj):
        count = obj.cours_set.count()
        return format_html('<span class="badge bg-blue-500 text-white">{}</span>', count)
    nombre_cours.short_description = 'Cours assignés'

@admin.register(GroupeEtudiants)
class GroupeEtudiantsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'taille', 'nombre_cours')
    search_fields = ('nom',)
    list_per_page = 20
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'taille')
        }),
    )

    def nombre_cours(self, obj):
        count = obj.cours_set.count()
        return format_html('<span class="badge bg-blue-500 text-white">{}</span>', count)
    nombre_cours.short_description = 'Cours assignés'

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('sujet', 'enseignant', 'groupe', 'duree', 'frequence_badge', 'liste_equipements')
    list_filter = ('frequence', 'enseignant')
    search_fields = ('sujet', 'enseignant__nom', 'groupe__nom')
    list_per_page = 20
    fieldsets = (
        ('Informations Générales', {
            'fields': ('sujet', 'enseignant', 'groupe', 'duree', 'frequence')
        }),
        ('Équipements', {
            'fields': ('equipements_requis',)
        }),
    )

    def frequence_badge(self, obj):
        color = 'bg-green-500' if obj.frequence == 'HEBDOMADAIRE' else 'bg-blue-500'
        return format_html('<span class="badge {} text-white">{}</span>', color, obj.frequence)
    frequence_badge.short_description = 'Fréquence'

    def liste_equipements(self, obj):
        equipements = obj.equipements_requis.all()
        return ", ".join(eq.nom for eq in equipements) or "-"
    liste_equipements.short_description = 'Équipements'

@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ('cours', 'salle', 'debut', 'fin', 'duree_badge')
    list_filter = ('salle', 'debut')
    search_fields = ('cours__sujet', 'salle__nom')
    list_per_page = 20
    fieldsets = (
        ('Détails du Cours', {
            'fields': ('cours', 'salle')
        }),
        ('Horaires', {
            'fields': ('debut', 'fin')
        }),
    )

    def duree_badge(self, obj):
        return format_html('<span class="badge bg-blue-500 text-white">{}h</span>', obj.cours.duree)
    duree_badge.short_description = 'Durée'