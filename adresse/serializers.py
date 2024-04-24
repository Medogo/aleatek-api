from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Adress


class AdresseSerializer(ModelSerializer):
    class Meta:
        model = Adress
        fields = '__all__'
