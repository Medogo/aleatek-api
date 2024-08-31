from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from Dashbord.models import Affaire
from .models import MissionActive, Mission, InterventionTechnique, Article, ArticleSelect, ArticleMission


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = ['id', 'code_mission', 'libelle', 'mission_parent']

""" def update(self, instance, validated_data):
        is_active = validated_data.get('is_active', instance.is_active)
        # Obtenez l'ID de l'affaire courante depuis le contexte du sérializer
        current_affaire_id = self.context.get('current_affaire_id')

        if is_active and not instance.is_active:
            # Créez une instance de MissionActive si `is_active` devient True
            if current_affaire_id:
                try:
                    current_affaire = Affaire.objects.get(id=current_affaire_id)
                    MissionActive.objects.get_or_create(id_mission=instance, id_affaire=current_affaire)
                except Affaire.DoesNotExist:
                    pass

        return super().update(instance, validated_data)"""


class MissionActiveSerializer(serializers.ModelSerializer):
    id_mission = MissionSerializer(many=True)

    class Meta:
        model = MissionActive
        fields = ['id', 'id_mission', 'id_affaire']


class InterventionTechniqueSerializer(ModelSerializer):
    class Meta:
        model = InterventionTechnique
        fields = '__all__'


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleSelectSerializer(ModelSerializer):
    class Meta:
        model = ArticleSelect
        fields = '__all__'


class ArticleMissionSerializer(ModelSerializer):
    class Meta:
        model = ArticleMission
        fields = '__all__'


class MissionSActiveSerializer(serializers.ModelSerializer):
    missions = serializers.PrimaryKeyRelatedField(many=True, queryset=Mission.objects.all(), source='id_mission')
    id_affaire = serializers.PrimaryKeyRelatedField(queryset=Affaire.objects.all())

    class Meta:
        model = MissionActive
        fields = ['id_affaire', 'missions']


"""
class MissionActiveDetailSerializer(serializers.ModelSerializer):
    missions = MissionSerializer(many=True, source='id_mission')

    class Meta:
        model = MissionActive
        fields = ['id_affaire', 'missions']
"""


class MissionActiveDetailSerializer(serializers.ModelSerializer):
    missions = MissionSerializer(many=True, source='id_mission')

    class Meta:
        model = MissionActive
        fields = ['id', 'id_affaire', 'missions']

        def get_missions(self, obj):
            active_missions = obj.get_active_missions()
            return MissionSerializer(active_missions, many=True).data


class SousMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['id', 'code_mission', 'libelle', 'mission_parent']
        read_only_fields = ['mission_parent']


class AffaireWithMissionsSerializer(serializers.ModelSerializer):
    missions = MissionSerializer(many=True, source='missionactive_set')

    class Meta:
        model = Affaire
        fields = ['id', 'libelle', 'statut', 'numero_offre', 'numero_contrat', 'missions']
