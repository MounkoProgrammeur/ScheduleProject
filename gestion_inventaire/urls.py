from django.urls import path
from . import views

app_name = 'gestion_inventaire'

urlpatterns = [
    path('salles/', views.liste_salles, name='liste_salles'),
    path('salles/creer/', views.creer_salle, name='creer_salle'),
    path('equipements/', views.liste_equipements, name='liste_equipements'),
    path('equipements/creer/', views.creer_equipement, name='creer_equipement'),
]