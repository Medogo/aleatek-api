from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from Dashbord.models import Affaire

from collaborateurs.models import Collaborateurs
from datetime import date
from django.db.models import UniqueConstraint


# Create your models here.
class Mission(models.Model):
    code_mission = models.CharField(max_length=10, unique=True)
    libelle = models.CharField(max_length=100)
    mission_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                       related_name='sous_missions', limit_choices_to={'mission_parent__isnull': True})

    def __str__(self):
        return self.code_mission


class MissionActive(models.Model):
    id_mission = models.ForeignKey(Mission, on_delete=models.CASCADE, default="")
    id_affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE, default="")
    is_active = models.BooleanField(default=False)


    def get_current_affaire(self):
        return self.id_affaire

    
   

class InterventionTechnique(models.Model):
    affecteur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, related_name='ITAffecteur')
    date = models.DateField(default=date.today, blank=True)
    id_mission_active = models.ForeignKey(MissionActive, on_delete=models.CASCADE)
    id_collaborateur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, related_name='ITAffecter')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_mission_active', 'id_collaborateur'], name='unique_IT')
        ]


class Article(models.Model):
    titre = models.CharField(max_length=500, unique=True)
    article_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                       related_name='sous_articles')
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return self.titre

    def get_ancestors_and_descendants(self):
        ancestors = self._get_ancestors(self)
        descendants = self._get_descendants(self)
        return ancestors, descendants

    def _get_ancestors(self, article):
        ancestors = []
        parent = article.article_parent
        while parent is not None:
            ancestors.insert(0, parent)
            parent = parent.article_parent
        return ancestors

    def _get_descendants(self, article):
        descendants = []
        children = article.sous_articles.all()
        for child in children:
            descendants.append(child)
            descendants.extend(self._get_descendants(child))
        return descendants

    class Meta:
        constraints = [
            UniqueConstraint(fields=['titre'], name='unique_titre')
        ]


class ArticleMission(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='mission')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['article', 'mission'], name='unique_article_mission')
        ]


class ArticleSelect(models.Model):
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE, related_name='affaire_article_select')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_article_select')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['article', 'affaire'], name='unique_affaire_article')
        ]
