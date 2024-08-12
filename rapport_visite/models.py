from django.db import models
from Dashbord.models import Affaire
from collaborateurs.models import Collaborateurs
from ouvrage.models import AffaireOuvrage


# Create your models here.

class RapportVisite(models.Model):
    ETAPES = [
        (0, 'En cours'),
        (1, 'Accepté'),
        (2, 'Classé'),
        (3, 'Diffuse'),
    ]
    date = models.DateField()
    order_in_affaire = models.IntegerField()
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    objet = models.CharField(max_length=500, blank=True)
    statut = models.CharField(max_length=10, choices=ETAPES, default=0)


class AvisOuvrage(models.Model):
    redacteur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE)
    ouvrage = models.ForeignKey(AffaireOuvrage, on_delete=models.CASCADE)
    objet = models.CharField(max_length=200, null=True, blank=True)
    rv = models.ForeignKey(RapportVisite, on_delete=models.CASCADE)


class CommentaireAvisOuvrage(models.Model):
    asuivre = models.BooleanField(default=False)
    commentaire = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    avis = models.ForeignKey(AvisOuvrage, on_delete=models.CASCADE)
    lever = models.BooleanField(default=False)
