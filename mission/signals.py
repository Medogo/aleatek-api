from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mission, MissionActive
from Dashbord.models import Affaire

@receiver(post_save, sender=Mission)
def create_mission_active(sender, instance, created, **kwargs):
    if created:
        affaires = Affaire.objects.all()
        for affaire in affaires:
            MissionActive.objects.create(id_mission=instance, id_affaire=affaire, is_active=False)
