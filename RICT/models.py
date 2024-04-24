from django.db import models
from django.db.models import UniqueConstraint
from Dashbord.models import Affaire
from mission.models import ArticleSelect, Article, ArticleMission
from collaborateurs.models import Collaborateurs
from mission.models import MissionActive

# Create your models here.

class RICT(models.Model):
    ETAPES = [
        (0, 'En cours'),
        (1, 'Accepté'),
        (2, 'Classé'),
        (3, 'Diffuse'),
    ]
    date = models.DateField()
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    statut = models.CharField(max_length=10, choices=ETAPES, default=0)


class Disposition(models.Model):
    rict = models.ForeignKey(RICT, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleMission, on_delete=models.CASCADE)
    commentaire = models.CharField(max_length=300)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['rict', 'article'], name='unique_rict_article')
        ]


class AvisArticle(models.Model):
    AVIS = [
        ('F', 'F'),
        ('RMQ', 'RMQ'),
        ('HM', 'HM'),
        ('SO', 'SO'),
        ('IM', 'IM')]
    rict = models.ForeignKey(RICT, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleMission, on_delete=models.CASCADE)
    codification = models.CharField(max_length=5, choices=AVIS)

class CommentaireAvisArticle(models.Model):
    id_avis = models.ForeignKey(AvisArticle, on_delete=models.CASCADE)
    commentaire = models.CharField(max_length=200)
    a_suivre = models.BooleanField(default=True)
    lever = models.BooleanField(default=False)

class DescriptionSommaire(models.Model):
    type = models.CharField(max_length=200)
    content = models.TextField()
    rict = models.ForeignKey(RICT, on_delete=models.CASCADE)

# Represente les missions valider pour un RICT
class MissionRICT(models.Model):
    mission = models.ForeignKey(MissionActive, on_delete=models.CASCADE)
    rict = models.ForeignKey(RICT, on_delete=models.CASCADE)
