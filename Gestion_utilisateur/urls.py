from django.urls import path
from . import views

app_name = 'gestion_utilisateur'

urlpatterns = [
    path('profil/', views.profil, name='profil'),
    path('liste/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('modifier/<int:pk>/', views.modifier_utilisateur, name='modifier_utilisateur'),
]