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
    statut = models.CharField(max_length=20, choices=STATUS)
    numero_offre = models.IntegerField(blank=True, null=True)
    numero_contrat = models.IntegerField(blank=True, null=True)
    libelle_contrat = models.CharField(max_length=100, default='', blank=True)
    date_contrat = models.DateField(blank=True, null=True)
    client = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True)  # Retirer null
    charge = models.ForeignKey(Collaborateurs, on_delete=models.SET_NULL, related_name='DashbordAffairecharge', null=True)
    assistant = models.ForeignKey(Collaborateurs, on_delete=models.SET_NULL, related_name='DashbordAffaireassistant', null=True)
    chef = models.ForeignKey(Collaborateurs, on_delete=models.SET_NULL, related_name='DashbordAffairechef', null=True)


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
    libelle = models.CharField(max_length=50, null=True, blank=True)
    devise = models.CharField(max_length=10, choices=DEVISE)
    type = models.CharField(max_length=10, choices=TYPES_AFFAIRES)
    type_montant = models.CharField(max_length=10, choices=TYPES_MONTANT, default='HT')
    prix = models.IntegerField(blank=True, null=True)
    debut_prestation = models.DateField(blank=True, null=True)
    debut_chantier = models.DateField(blank=True, null=True)
    fin_chantier = models.DateField(blank=True, null=True)
    visite = models.IntegerField(blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)


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
