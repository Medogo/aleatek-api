from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import MissionActive, Mission, InterventionTechnique, Article, ArticleSelect, ArticleMission


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'


class MissionActiveSerializer(ModelSerializer):
    class Meta:
        model = MissionActive
        fields = '__all__'


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