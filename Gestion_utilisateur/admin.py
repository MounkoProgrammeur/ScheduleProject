from django.contrib import admin
from django.utils.html import format_html
from .models import Profil

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'role_badge', 'email')
    list_filter = ('role',)
    search_fields = ('utilisateur__username', 'utilisateur__email')
    list_per_page = 20
    fieldsets = (
        ('Utilisateur', {
            'fields': ('utilisateur',)
        }),
        ('Rôle', {
            'fields': ('role',)
        }),
    )

    def role_badge(self, obj):
        couleurs = {
            'ADMIN': 'bg-blue-500',
            'PLANIFICATEUR': 'bg-green-500',
            'CONSULTANT': 'bg-yellow-500'
        }
        return format_html('<span class="badge {} text-white">{}</span>', couleurs.get(obj.role, 'bg-gray-500'), obj.role)
    role_badge.short_description = 'Rôle'

    def email(self, obj):
        return obj.utilisateur.email
    email.short_description = 'Email'