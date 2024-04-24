from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import SyntheseAvis, SyntheseCommentaireDocument, SyntheseComentaireRV, SyntheseCommentaireArticle

class SyntheseAvisSerializer(ModelSerializer):
    class Meta:
        model = SyntheseAvis
        fields = '__all__'

class SyntheseCommentaireDocumentSerializer(ModelSerializer):
    class Meta:
        model = SyntheseCommentaireDocument
        fields = '__all__'

class SyntheseComentaireRVSerializer(ModelSerializer):
    class Meta:
        model = SyntheseComentaireRV
        fields = '__all__'

class SyntheseCommentaireArticleSerializer(ModelSerializer):
    class Meta:
        model = SyntheseCommentaireArticle
        fields = '__all__'

