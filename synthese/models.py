from django.db import models
from Dashbord.models import Affaire
from collaborateurs.models import Collaborateurs
from commentaire.models import Commentaire
from rapport_visite.models import CommentaireAvisOuvrage
from RICT.models import CommentaireAvisArticle
from django.db.models import UniqueConstraint

import datetime
# Create your models here.

class SyntheseAvis(models.Model):
    ETAPES = [
        (0, 'En cours'),
        (1, 'Accepté'),
        (2, 'Classé'),
        (3, 'Diffuse'),
    ]
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    createur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE)
    date = models.DateField(blank=True, default=datetime.date.today)
    statut = models.IntegerField(choices=ETAPES, default=0)
    order = models.IntegerField(default=0)

class SyntheseCommentaireDocument(models.Model):
    synthese = models.ForeignKey(SyntheseAvis, on_delete=models.CASCADE)
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['synthese', 'commentaire'], name='unique_synthese_commentaire_document')
        ]
    
class SyntheseComentaireRV(models.Model):
    synthese = models.ForeignKey(SyntheseAvis, on_delete=models.CASCADE)
    commentaire = models.ForeignKey(CommentaireAvisOuvrage, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['synthese', 'commentaire'], name='unique_synthese_commentaire_rv')
        ]

class SyntheseCommentaireArticle(models.Model):
    synthese = models.ForeignKey(SyntheseAvis, on_delete=models.CASCADE)
    commentaire = models.ForeignKey(CommentaireAvisArticle, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['synthese', 'commentaire'], name='unique_synthese_commentaire_article')
        ]