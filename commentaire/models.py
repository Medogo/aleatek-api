from django.db import models

from ouvrage.models import Avis

# Create your models here.

class Commentaire(models.Model):
    id_avis = models.ForeignKey(Avis, on_delete=models.CASCADE)
    commentaire = models.CharField(max_length=200)
    a_suivre = models.BooleanField(default=True)
    lever = models.BooleanField(default=False)
