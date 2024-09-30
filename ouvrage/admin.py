from django.contrib import admin

# Register your models here.
from .models import Ouvrage, Documents, Aso, AffaireOuvrage, EntrepriseOuvrage, RemarqueAso

admin.site.register(Ouvrage)
admin.site.register(Documents)
admin.site.register(Aso)
admin.site.register(AffaireOuvrage)
admin.site.register(EntrepriseOuvrage)
admin.site.register(RemarqueAso)