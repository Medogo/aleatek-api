from django.db import models
from Dashbord.models import Affaire, EntrepriseAffaire
from collaborateurs.models import Collaborateurs
from django.db.models import UniqueConstraint

from entreprise.models import Entreprise
class Ouvrage(models.Model):
    libelle = models.CharField(max_length=200)
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE, null=True)


class AffaireOuvrage(models.Model):
    id_affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    id_ouvrage = models.ForeignKey(Ouvrage, on_delete=models.CASCADE)
    diffusion = models.BooleanField(default=False)
    rename = models.CharField(max_length=200, default='', blank=True)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_affaire', 'id_ouvrage'], name='unique_affaire_document')
        ]

class Aso(models.Model):
    ETAPES = [
        (0, 'En cours'),
        (1, 'Accepté'),
        (2, 'Classé'),
        (3, 'Diffuse'),
    ]
    date = models.DateField()
    statut = models.CharField(max_length=10, choices=ETAPES, default=0, null=True, blank=True)
    redacteur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, null=True)
    order_in_affaire = models.IntegerField()
    affaireouvrage = models.ForeignKey(AffaireOuvrage, on_delete=models.CASCADE)
    
class RemarqueAso(models.Model):
    aso = models.ForeignKey(Aso, on_delete=models.CASCADE)
    redacteur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE)
    content = models.TextField()



class EntrepriseOuvrage(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    ouvrage = models.ForeignKey(Ouvrage, on_delete=models.CASCADE)



class EntrepriseAffaireOuvrage(models.Model):
    affaire_ouvrage = models.ForeignKey(AffaireOuvrage, on_delete=models.CASCADE)
    affaire_entreprise = models.ForeignKey(EntrepriseAffaire, on_delete=models.CASCADE)
    diffusion = models.BooleanField(default=False)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['affaire_ouvrage', 'affaire_entreprise'], name='unique_entreprise_ouvrage')
        ]

class Documents(models.Model):
    Nature = [
        ('TOUS', 'TOUS'),
        ('Descriptif', 'Descriptif'),
        ('AT/DTA', 'AT/DTA'),
        ('Attestation Incendie', 'Attestation Incendie'),
        ('Carnet', 'Carnet'),
        ('Certificat', 'Certificat'),
        ('Certificat incendie', 'Certificat incendie'),
        ('Compte rendue', 'Compte rendu'),
        ('Courrier', 'Courrier'),
        ('fiche techinique', 'Fiche Technique'),
        ('Note', 'Note'),
        ('Note de calcule', 'Note de calcule'),
        ('Notice', 'Notice'),
        ('Plan', 'Plan'),
        ('PV', 'PV'),
        ('PV Incendie', 'PV Incendie'),
        ('Rapport', 'Rapport'),
        ('Schéma', 'Schéma')
    ]
    order = models.IntegerField()
    dossier = models.CharField(max_length=200, default='Execution', choices=(('Execution', 'Execution'),
                                                                            ('Conception', 'Conception')))
    nature = models.CharField(choices=Nature, max_length=30)
    indice = models.CharField(max_length=5, blank=True, null=True)
    date_indice = models.DateField(blank=True, null=True)
    date_reception = models.DateField(blank=True, null=True)
    titre = models.CharField(max_length=500, blank=True, null=True)
    numero_externe = models.IntegerField(blank=True, null=True)
    emetteur = models.ForeignKey(EntrepriseAffaireOuvrage, on_delete=models.CASCADE)
    aso = models.ForeignKey(Aso, on_delete=models.SET_NULL, null=True)
    validateur = models.ForeignKey(Collaborateurs, on_delete=models.SET_NULL, null=True, blank=True, related_name='ouvrageDocumentsvalidateur')
    createur = models.ForeignKey(Collaborateurs, on_delete=models.SET_NULL, null=True, blank=True, related_name='ouvrageDocumentscreateur')

class DocumentAffectation(models.Model):
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    collaborateur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['document', 'collaborateur'], name='unique_document_affectation')
        ]

class FichierAttache(models.Model):
    nom = models.CharField(max_length=250)
    fichier = models.FileField(upload_to='fichierattachedocument')
    date = models.DateField()
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_fichier


class Avis(models.Model):
    AVIS = [
        ('F', 'F'),
        ('RMQ', 'RMQ'),
        ('HM', 'HM'),
        ('VI', 'VI')]
    id_document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    codification = models.CharField(max_length=23, choices=AVIS)
    collaborateurs = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_document', 'collaborateurs'], name='unique_avis_collaborateur')
        ]

