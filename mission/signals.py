from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mission, MissionActive  # Assurez-vous d'importer vos modèles
from Dashbord.models import Affaire

def get_current_affaire(request):
    affaire_id = request.session.get('current_affaire_id')
    if affaire_id:
        return Affaire.objects.get(id=affaire_id)
    return None


@receiver(post_save, sender=Mission)
def create_mission_active(sender, instance, **kwargs):
    if instance.is_active:
        # Récupérer l'affaire courante selon votre logique
        current_affaire = get_current_affaire()  # Implémentez la logique pour récupérer l'affaire courante
        if current_affaire:
            MissionActive.objects.get_or_create(id_mission=instance, id_affaire=current_affaire)
