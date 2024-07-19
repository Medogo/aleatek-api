from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PlanAffaire, Produit, Affaire, Chantier, Batiment, EntrepriseAffaire


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
