"""from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Affaire, PlanAffaire


@receiver(post_save, sender=Affaire)
def create_initial_plan_affaire(sender, instance, created, **kwargs):
    if created:
        # Création automatique du premier PlanAffaire avec le numéro 1
        PlanAffaire.objects.create(
            affaire=instance,
            numero=1,
            risque='Normal',
            devise='€',
            type='CTC'
        )


@receiver(post_save, sender=PlanAffaire)
def set_plan_affaire_numero(sender, instance, created, **kwargs):
    if created and instance.numero == 1:
        # Incrémenter automatiquement le numéro pour les futurs PlanAffaire de la même Affaire
        dernier_numero = PlanAffaire.objects.filter(affaire=instance.affaire).order_by('-numero').first()
        if dernier_numero:
            instance.numero = dernier_numero.numero + 1
            instance.save()
"""

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

