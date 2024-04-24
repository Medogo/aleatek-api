from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Responsable, Entreprise
from .permissions import IsAdminAuthenticated
from .serializers import ResponsableSerializer
from rest_framework.views import APIView
from adresse.models import Adress
from django.forms.models import model_to_dict
from django.db import transaction
from rest_framework import status
from Dashbord.models import EntrepriseAffaire

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ResponsableAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ResponsableSerializer
    queryset = Responsable.objects.all()
    permission_classes = [IsAdminAuthenticated]


from .serializers import EntrepriseSerializer


class EntrepriseAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EntrepriseSerializer
    queryset = Entreprise.objects.all()
    permission_classes = [IsAdminAuthenticated]

class GetEntrepriseWithCollaborateur(APIView):
    def get(self, request, id_entreprise=None):
        if id_entreprise is not None:
            entreprise = Entreprise.objects.filter(id=id_entreprise).values().first()
            if entreprise is None:
                return Response({'message': 'Entreprise non trouvée'}, status=status.HTTP_404_NOT_FOUND)
            
            entreprise_data = {
                'id': entreprise['id'],
                'raison_sociale': entreprise['raison_sociale'],
                'siret': entreprise['siret'],
                'activite': entreprise['activite'],
                'adresse': {}
            }
            adresse = Adress.objects.get(id=entreprise['adresse_id'])
            entreprise_data['adresse'] = model_to_dict(adresse)
            responsables = Responsable.objects.filter(entreprise_id=entreprise['id'])
            entreprise_data['responsables'] = []
            for responsable in responsables:
                entreprise_data['responsables'].append(model_to_dict(responsable))
            
            return Response(entreprise_data)
        
        else:
            entreprises = Entreprise.objects.all().values()
            data = []
            for entreprise in entreprises:
                entreprise_data = {
                    'id': entreprise['id'],
                    'raison_sociale': entreprise['raison_sociale'],
                    'siret': entreprise['siret'],
                    'activite': entreprise['activite'],
                    'adresse': {}
                }
                adresse = Adress.objects.get(id=entreprise['adresse_id'])
                entreprise_data['adresse'] = model_to_dict(adresse)
                responsables = Responsable.objects.filter(entreprise_id=entreprise['id'])
                entreprise_data['responsables'] = []
                for responsable in responsables:
                    entreprise_data['responsables'].append(model_to_dict(responsable))
                data.append(entreprise_data)

            return Response(data)

class EditeDataEntreprise(APIView):
    def put(self, request):
        try:
            with transaction.atomic():
                adress = request.data['adress']
                id_entreprise = request.data['id_entreprise']
                entreprise = request.data['entreprise']
                responsables = request.data['responsables']
                
                Adress.objects.filter(id=adress['id']).update(**adress)
                Entreprise.objects.filter(id=id_entreprise).update(**entreprise, adresse_id=adress['id'])

                for responsable in responsables:
                    if not 'id' in responsable:
                        Responsable(**responsable, entreprise_id=id_entreprise).save()
            
        except Exception as e:
            print(Exception)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    
class CreateEntreprise(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                adress = request.data['adress']
                entreprise = request.data['entreprise']
                responsables = request.data['responsables']
                affaire = request.data['affaire'] if 'affaire' in request.data else None
                
                new_adresse = Adress(**adress)
                new_adresse.save()
                
                new_entreprise = Entreprise(**entreprise, adresse=new_adresse)
                new_entreprise.save()
                
                for responsable in responsables:
                    Responsable(**responsable, entreprise=new_entreprise).save()
                    
                if affaire:
                    EntrepriseAffaire(entreprise=new_entreprise, affaire_id=affaire).save()
                
        except Exception as e:
            print(Exception)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    
class AddEntrepriseOnAffaire(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                affaire = request.data['affaire']                
                entreprises = request.data['entreprises']
                
                for entreprise in entreprises:
                    EntrepriseAffaire(entreprise_id=entreprise, affaire_id=affaire).save()

        except Exception as e:
            print(Exception)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    