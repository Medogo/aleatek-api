"""from django.db.models.signals import post_save
from django.dispatch import receiver

# Importez vos modèles
from .models import Mission, MissionActive


@receiver(post_save, sender=Mission)
def create_or_update_mission_active(sender, instance, created, **kwargs):
    # Vérifiez si is_active est True
    if instance.is_active:
        # Recherchez ou créez une instance MissionActive pour l'affaire correspondante
        mission_active, _ = MissionActive.objects.get_or_create(id_affaire=instance.mission_parent.id_affaire)

        # Ajoutez la mission à cette instance MissionActive
        mission_active.id_mission.add(instance)

        # Sauvegardez la relation
        mission_active.save()
"""