from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import RapportVisite, AvisOuvrage, CommentaireAvisOuvrage

class RapportVisiteSerializer(ModelSerializer):
    class Meta:
        model = RapportVisite
        fields = '__all__'

class AvisOuvrageSerializer(ModelSerializer):
    class Meta:
        model = AvisOuvrage
        fields = '__all__'
        depth = 2 


class CommentaireAvisOuvrageSerializer(ModelSerializer):
    class Meta:
        model = CommentaireAvisOuvrage
        fields = '__all__'
        depth = 2 

