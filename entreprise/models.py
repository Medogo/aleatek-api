from django.db import models

from adresse.models import Adress


class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=100)
    siret = models.IntegerField(blank=True, null=True)
    activite = models.CharField(max_length=200, blank=True, null=True)
    adresse = models.OneToOneField(Adress, on_delete=models.CASCADE)


class Responsable(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField()
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='Responsables')
