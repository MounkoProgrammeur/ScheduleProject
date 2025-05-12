from django.urls import path
from . import views

app_name = 'visualisation_emploi'

urlpatterns = [
    path('', views.tableau_bord, name='tableau_bord'),
    path('calendrier/', views.calendrier, name='calendrier'),
    path('disponibilite/', views.disponibilite_salles, name='disponibilite_salles'),
]