
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventaire/', include('gestion_inventaire.urls')),
    path('utilisateur/', include('Gestion_utilisateur.urls')),
    path('planing/', include('planing_cours.urls')),
    path('emploie/', include('visualisation_emploi.urls'))
   
   
]
