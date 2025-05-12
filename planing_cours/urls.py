from django.urls import path
from . import views

app_name = 'planning_cours'

urlpatterns = [
    path('cours/', views.liste_cours, name='liste_cours'),
    path('cours/creer/', views.creer_cours, name='creer_cours'),
    path('generer/', views.generer_emplois, name='generer_emplois'),
]