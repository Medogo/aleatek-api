from datetime import datetime

from django.db import models
from django.db.models import UniqueConstraint

from adresse.models import Adress
from collaborateurs.models import Collaborateurs
from entreprise.models import Entreprise


# Create your models here.

class Produit(models.Model):
    code_produit = models.CharField(max_length=3)
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.code_produit


class Batiment(models.Model):
    libelle = models.CharField(max_length=50)


class Affaire(models.Model):
    STATUS = [
        ('En cours', 'En cours'),
        ('Achevé', 'Achevé'),
        ('Abandonné', 'Abandonné')
    ]

    libelle = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=STATUS, default='En cours')
    numero_offre = models.IntegerField(blank=True, null=True)
    numero_contrat = models.CharField(max_length=100, default='')
    libelle_contrat = models.CharField(max_length=100, default='', blank=True)
    date_contrat = models.DateField(blank=True, null=True)
    client = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True)  # Retirer null
    charge = models.ForeignKey(Collaborateurs, on_delete=models.SET_NULL, related_name='DashbordAffairecharge',
                               null=True)
    assistant = models.ForeignKey(Collaborateurs, on_delete=models.SET_NULL, related_name='DashbordAffaireassistant',
                                  null=True)
    chef = models.ForeignKey(Collaborateurs, on_delete=models.SET_NULL, related_name='DashbordAffairechef', null=True)

    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, related_name='DashbordProduit')

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.libelle)


class PlanAffaire(models.Model):
    RISQUES = [
        ('Normal', 'Normal'),
        ('Particulier', 'Particulier'),
        ('Complexe', 'Complexe')

    ]
    DEVISE = [
        ('$', '$'),
        ('€', '€')
    ]

    TYPES_AFFAIRES = [
        ('CTC', 'CTC'),
        ('VT', 'VT')
    ]

    TYPES_MONTANT = [
        ('HT', 'HT'),
        ('TTC', 'TTC')
    ]

    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    numero = models.IntegerField()
    risque = models.CharField(max_length=20, choices=RISQUES)
    libelle_planAffaire = models.CharField(max_length=50, null=True, blank=True)
    devise = models.CharField(max_length=10, choices=DEVISE)
    type = models.CharField(max_length=10, choices=TYPES_AFFAIRES)
    type_montant = models.CharField(max_length=10, choices=TYPES_MONTANT, default='HT')
    prix = models.IntegerField(blank=True, null=True)
    debut_prestation = models.DateField(blank=True, null=True)
    debut_chantier = models.DateField(blank=True, null=True)
    fin_chantier = models.DateField(blank=True, null=True)
    visite = models.IntegerField(blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)
    rapport_initiaux = models.IntegerField(blank=True, default=0, null=True)
    synthese = models.CharField(blank=True, max_length=100, default="", null=True)
    fiche_transfert = models.FileField(blank=True, null=True)
    point_risque_virgilence_associe = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.libelle_planAffaire)


class Chantier(models.Model):
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, null=True, blank=True)
    plan_affaire = models.OneToOneField(PlanAffaire, on_delete=models.CASCADE)
    adresse = models.OneToOneField(Adress, models.CASCADE)


class EntrepriseAffaire(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True)
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['entreprise', 'affaire'], name='unique_entreprise_affaire')
        ]


class Tutorial(models.Model):
    tutored = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='tutorals')
    plan_affaire = models.ForeignKey(PlanAffaire, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='tutorals')


class BatimentPlanAffaire(models.Model):
    batiment = models.ManyToManyField(Batiment)
    plan_affaire = models.ForeignKey(PlanAffaire, on_delete=models.CASCADE, null=True, blank=True,)