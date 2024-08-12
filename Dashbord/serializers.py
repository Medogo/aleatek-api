from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PlanAffaire, Produit, Affaire, Chantier, Batiment, EntrepriseAffaire, Tutorial
from collaborateurs.serializers import ColaboratteursSerializer
from entreprise.serializers import EntrepriseSerializer


class TutorialSerializer(serializers.ModelSerializer):
    tutored = serializers.SerializerMethodField()

    class Meta:
        model = Tutorial
        fields = ['tutored']

    def get_tutore(self, obj):
        return {
            'nom': obj.tutored.last_name,
            'prenom': obj.tutored.first_name,
        }


class ProduitSerializer(ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'


class PlanAffaireSerializer(serializers.ModelSerializer):
    tutorats = serializers.SerializerMethodField()

    class Meta:
        model = PlanAffaire
        fields = '__all__'  # Inclure tous les champs de PlanAffaire

    def get_tutorats(self, obj):
        # Utiliser filter() pour obtenir plusieurs Tutorats
        tutorats = Tutorial.objects.filter(plan_affaire=obj)
        tutorat_serializer = TutorialSerializer(tutorats, many=True)
        return tutorat_serializer.data


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
