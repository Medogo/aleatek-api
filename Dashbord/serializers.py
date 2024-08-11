from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PlanAffaire, Produit, Affaire, Chantier, Batiment, EntrepriseAffaire
from collaborateurs.serializers import ColaboratteursSerializer
from entreprise.serializers import EntrepriseSerializer

class ProduitSerializer(ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'


class PlanAffaireSerializer(ModelSerializer):
    class Meta:
        model = PlanAffaire
        fields = '__all__'


class AffaireSerializer(ModelSerializer):
    plans = PlanAffaireSerializer(many=True, read_only=True)
    client = EntrepriseSerializer()  # Afficher toutes les infos de l'entreprise
    charge = ColaboratteursSerializer()  # Afficher toutes les infos du collaborateur chargé
    assistant = ColaboratteursSerializer()  # Afficher toutes les infos de l'assistant
    chef = ColaboratteursSerializer()  # Afficher toutes les infos du chef


    class Meta:
        model = Affaire
        fields = '__all__'


class ChantierSerializer(ModelSerializer):
    class Meta:
        model = Chantier
        fields = '__all__'


class BatimentSerializer(ModelSerializer):
    class Meta:
        model = Batiment
        fields = '__all__'

class EntrepriseAffaireSerializer(ModelSerializer):
    class Meta:
        model = EntrepriseAffaire
        fields = '__all__'
