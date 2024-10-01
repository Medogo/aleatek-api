from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Aso, AffaireOuvrage, Avis, Ouvrage, Documents, FichierAttache, EntrepriseAffaireOuvrage, DocumentAffectation, RemarqueAso
from Dashbord.serializers import AffaireSerializer
from Dashbord.models import EntrepriseAffaire

class AsoSerializer(ModelSerializer):
    class Meta:
        model = Aso
        fields = '__all__'
        
class RemarqueAsoSerializer(ModelSerializer):
    class Meta:
        model = RemarqueAso
        fields = '__all__'

class AffaireOuvrageSerializer(ModelSerializer):
    class Meta:
        model = AffaireOuvrage
        fields = '__all__'


class AvisSerializer(ModelSerializer):
    class Meta:
        model = Avis
        fields = '__all__'


class OuvrageSerializer(ModelSerializer):
    class Meta:
        model = Ouvrage
        fields = '__all__'


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'

class DocumentAffectationSerializer(ModelSerializer):
    class Meta:
        model = DocumentAffectation
        fields = '__all__'

class FichierAttacheSerializer(ModelSerializer):
    class Meta:
        model = FichierAttache
        fields = '__all__'


class EntrepriseAffaireOuvrageSerializer(ModelSerializer):
    class Meta:
        model = EntrepriseAffaireOuvrage
        fields = '__all__'
        


class AffaireOuvrageSerializerAdmin(serializers.ModelSerializer):
    affaire = AffaireSerializer(source='id_affaire', read_only=True)
    ouvrage = OuvrageSerializer(source='id_ouvrage', read_only=True)

    class Meta:
        model = AffaireOuvrage
        fields = ['id', 'diffusion', 'rename', 'id_affaire', 'id_ouvrage', 'affaire', 'ouvrage']

from Dashbord.serializers import EntrepriseAffaireSerializer
class EntrepriseAffaireOuvrageSerializerAdminisrator(serializers.ModelSerializer):
    affaire_ouvrage = AffaireOuvrageSerializer(read_only=True)
    affaire_entreprise = EntrepriseAffaireSerializer(read_only=True)

    class Meta:
        model = EntrepriseAffaireOuvrage
        fields = ['id', 'diffusion', 'affaire_ouvrage', 'affaire_entreprise']



from entreprise.serializers import EntrepriseSerializer
class EntrepriseAffaireOuvrageSerializerAddline(serializers.ModelSerializer):
    affaire_entreprise = EntrepriseSerializer()  # Utilise le serializer d'entreprise

    class Meta:
        model = EntrepriseAffaireOuvrage
        fields = ['affaire_entreprise', 'diffusion']



from collaborateurs.models import Collaborateurs

class CollaborateurSerializersss(serializers.ModelSerializer):
    class Meta:
        model = Collaborateurs
        fields = ['id', 'username', 'last_name', 'first_name']



class AsoDetailSerializers(serializers.ModelSerializer):
    statut = serializers.SerializerMethodField()
    redacteur = serializers.CharField(source='redacteur.last_name')
    ouvrage = serializers.SerializerMethodField()

    class Meta:
        model = Aso
        fields = ['id', 'date', 'statut', 'redacteur', 'order_in_affaire', 'affaireouvrage', 'ouvrage']

    def get_statut(self, obj):
        statut_dict = dict(Aso.ETAPES)
        statut_value = obj.statut
        if isinstance(statut_value, int):
            return statut_dict.get(statut_value, "Inconnu")
        elif isinstance(statut_value, str):
            try:
                return statut_dict.get(int(statut_value), statut_value)
            except ValueError:
                return statut_value
        return "Inconnu"

    def get_ouvrage(self, obj):
        ouvrage = obj.affaireouvrage.id_ouvrage
        return OuvrageSerializer(ouvrage).data

class RemarqueAsoSerializers(serializers.ModelSerializer):
    redacteur = CollaborateurSerializersss()
    aso = AsoDetailSerializers()

    class Meta:
        model = RemarqueAso
        fields = ['id', 'aso', 'redacteur', 'content']







class AffaireOuvrageSerializerss(serializers.ModelSerializer):
    id_affaire = AffaireSerializer()
    id_ouvrage = OuvrageSerializer()

    class Meta:
        model = AffaireOuvrage
        fields = '__all__'

class EntrepriseAffaireSerializerzerr(serializers.ModelSerializer):
    entreprise = EntrepriseSerializer()
    affaire = AffaireSerializer()

    class Meta:
        model = EntrepriseAffaire
        fields = '__all__'

class EntrepriseAffaireOuvrageSerializerss(serializers.ModelSerializer):
    affaire_ouvrage = AffaireOuvrageSerializerss()
    affaire_entreprise = EntrepriseAffaireSerializerzerr()

    class Meta:
        model = EntrepriseAffaireOuvrage
        fields = '__all__'
