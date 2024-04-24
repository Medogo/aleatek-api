from django.db import models

# Create your models here.

class Adress(models.Model):
    cplt_geo = models.CharField(max_length=250, blank=True)
    numero_voie = models.CharField(max_length=500, blank=True)
    lieu_dit = models.CharField(max_length=250, blank=True)
    code_postal = models.CharField(max_length=5, blank=True)
    ville = models.CharField(max_length=500, blank=True)
    pays = models.CharField(max_length=500, default='France', blank=True)

