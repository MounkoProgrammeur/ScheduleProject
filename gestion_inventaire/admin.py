from django.contrib import admin
from django.utils.html import format_html
from .models import Batiment, Salle, Equipement

@admin.register(Batiment)
class BatimentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'nombre_salles')
    search_fields = ('nom', 'adresse')
    list_per_page = 20

    def nombre_salles(self, obj):
        count = obj.salles.count()
        return format_html('<span class="badge bg-blue-500 text-white">{}</span>', count)
    nombre_salles.short_description = 'Nombre de salles'

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'batiment', 'type_salle', 'capacite', 'liste_equipements', 'etat_badge')
    list_filter = ('type_salle', 'batiment')
    search_fields = ('nom', 'batiment__nom')
    list_per_page = 20
    fieldsets = (
        ('Informations Générales', {
            'fields': ('nom', 'batiment', 'etage', 'type_salle', 'capacite')
        }),
        ('Détails', {
            'fields': ('notes',)
        }),
    )

    def liste_equipements(self, obj):
        equipements = obj.equipements.all()
        return ", ".join(eq.nom for eq in equipements) or "-"
    liste_equipements.short_description = 'Équipements'

    def etat_badge(self, obj):
        return format_html('<span class="badge bg-green-500 text-white">Disponible</span>')
    etat_badge.short_description = 'État'

@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'mobilite_badge', 'nombre_salles')
    list_filter = ('est_mobile',)
    search_fields = ('nom', 'description')
    list_per_page = 20
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'description', 'est_mobile')
        }),
        ('Assignation', {
            'fields': ('salles',)
        }),
    )

    def mobilite_badge(self, obj):
        color = 'bg-green-500' if obj.est_mobile else 'bg-red-500'
        texte = 'Mobile' if obj.est_mobile else 'Fixe'
        return format_html('<span class="badge {} text-white">{}</span>', color, texte)
    mobilite_badge.short_description = 'Mobilité'

    def nombre_salles(self, obj):
        count = obj.salles.count()
        return format_html('<span class="badge bg-blue-500 text-white">{}</span>', count)
    nombre_salles.short_description = 'Salles associées'