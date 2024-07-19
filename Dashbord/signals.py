from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Affaire, PlanAffaire

@receiver(post_save, sender=Affaire)
def create_plan_affaire(sender, instance, created, **kwargs):
    if created:
        PlanAffaire.objects.create(
            affaire=instance,
            numero=1,
            risque='Normal',  
            devise='€',       
            type='CTC'        
        )