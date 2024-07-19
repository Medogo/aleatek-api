from django.contrib import admin
from .models import Produit, Batiment, Affaire, PlanAffaire, Chantier, EntrepriseAffaire
from adresse.models import Adress
from entreprise.models import Entreprise

admin.site.register(Produit)
admin.site.register(Batiment)
admin.site.register(Affaire)
admin.site.register(PlanAffaire)
admin.site.register(Chantier)
admin.site.register(EntrepriseAffaire)
admin.site.register(Adress)
admin.site.register(Entreprise)
