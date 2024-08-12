from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PlanAffaire, Produit, Affaire, Chantier, Batiment, EntrepriseAffaire, Tutorial
from collaborateurs.serializers import ColaboratteursSerializer
from entreprise.serializers import EntrepriseSerializer


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'  # On ne retourne que l'ID


class ProduitSerializer(ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'


class PlanAffaireSerializer(ModelSerializer):
    tutored = serializers.SerializerMethodField()

    class Meta:
        model = PlanAffaire
        fields = '__all__'

    def get_tutored(self, obj):
        try:
            tutorat = Tutorial.objects.get(plan_affaire=obj)
            return {
                'nom': tutorat.tutored.last_name,
                'prenom': tutorat.tutored.first_name,
            }
        except Tutorial.DoesNotExist:
            return None


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


# serializers.py
from .models import Tutorial


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'  # On ne retourne que l'ID
