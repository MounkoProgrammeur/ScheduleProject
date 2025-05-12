from django.apps import AppConfig


class GestionUtilisateurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Gestion_utilisateur'

def ready(self):
    import Gestion_utilisateur.signals
