from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Produit, PlanAffaire, Affaire, Batiment, Chantier, EntrepriseAffaire
from .permissions import IsAdminAuthenticated
from .serializers import AffaireSerializer, ProduitSerializer, PlanAffaireSerializer, BatimentSerializer, \
    ChantierSerializer, EntrepriseAffaireSerializer
from rest_framework.views import APIView
from adresse.models import Adress
from collaborateurs.models import Collaborateurs
from entreprise.models import Entreprise
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Affaire
from django.forms.models import model_to_dict
from mission.models import MissionActive
from django.db import transaction


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AffaireAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AffaireSerializer
    queryset = Affaire.objects.all()
    permission_classes = [IsAdminAuthenticated]


class PlanAffaireAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = PlanAffaireSerializer
    queryset = PlanAffaire.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ProduitAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProduitSerializer
    queryset = Produit.objects.all()
    permission_classes = [IsAdminAuthenticated]


class BatimentAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = BatimentSerializer
    queryset = Batiment.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ChantierAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ChantierSerializer
    queryset = Chantier.objects.all()
    permission_classes = [IsAdminAuthenticated]


class EntrepriseAffaireViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EntrepriseAffaireSerializer
    queryset = EntrepriseAffaire.objects.all()
    permission_classes = [IsAdminAuthenticated]


class GetPlanAffaireDetail(APIView):
    def get(self, request):
        planAffaires = PlanAffaire.objects.all().values()
        data = []
        for planAffaire in planAffaires:
            planAffaire_data = dict(planAffaire)
            # On cherche l'affaire
            affaire = Affaire.objects.get(id=planAffaire['affaire_id'])
            planAffaire_data['affaire'] = model_to_dict(affaire)
            # On cherche la ville
            chantier = model_to_dict(Chantier.objects.get(plan_affaire=planAffaire['id']))
            adresse = Adress.objects.get(id=chantier['id'])
            planAffaire_data['ville'] = adresse.ville
            # On cherche le charger
            charger_affaire = Collaborateurs.objects.get(id=model_to_dict(affaire)['charge'])
            planAffaire_data['charge_affaire'] = {
                'nom': charger_affaire.last_name,
                'prenom': charger_affaire.first_name,
            }
            # On cherche le client
            client = Entreprise.objects.get(id=model_to_dict(affaire)['client'])
            planAffaire_data['client'] = client.raison_sociale
            # On cherche le batiment
            batiment = Batiment.objects.get(id=chantier['batiment'])
            planAffaire_data['batiment'] = batiment.libelle
            data.append(planAffaire_data)
        return Response(data)


class GetPlanAffaireDetailForPlanAffaire(APIView):
    def get(self, request, id_plan_affaire):
        try:
            planAffaire = PlanAffaire.objects.get(id=id_plan_affaire)

            planAffaire_data = model_to_dict(planAffaire)
            # On cherche l'affaire
            affaire = Affaire.objects.get(id=planAffaire_data['affaire'])
            planAffaire_data['affaire'] = model_to_dict(affaire)
            # On cherche la ville
            chantier = model_to_dict(Chantier.objects.get(plan_affaire=planAffaire_data['id']))
            adresse = Adress.objects.get(id=chantier['id'])
            planAffaire_data['adresse'] = model_to_dict(adresse)
            # On cherche le charger
            charger_affaire = Collaborateurs.objects.get(id=model_to_dict(affaire)['charge'])
            planAffaire_data['charge_affaire'] = model_to_dict(charger_affaire)
            # On cherche le client
            client = Entreprise.objects.get(id=model_to_dict(affaire)['client'])
            adresse_client = client.adresse
            planAffaire_data['client'] = model_to_dict(client)
            planAffaire_data['client']['adresse_detail'] = model_to_dict(adresse_client)
            # On cherche le batiment
            batiment = Batiment.objects.get(id=chantier['batiment'])
            planAffaire_data['batiment'] = model_to_dict(batiment)
            # On ajoute le chantier
            planAffaire_data['chantier'] = chantier

            return Response(planAffaire_data)
        except:
            return Response({})


class GetAllEntrepriseForAffaire(APIView):
    def get(self, request, id_affaire):
        entreprises = EntrepriseAffaire.objects.filter(affaire=id_affaire)
        data = []
        for entreprise in entreprises:
            data.append(model_to_dict(entreprise.entreprise)['id'])

        return Response(data)


class GetAllEntrepriseDetailForAffaire(APIView):
    def get(self, request, id_affaire):
        entreprises = EntrepriseAffaire.objects.filter(affaire=id_affaire).values()
        data = []
        for entreprise in entreprises:
            final = dict(entreprise)
            detailEntreprise = Entreprise.objects.get(id=entreprise['entreprise_id'])
            final['entreprise'] = model_to_dict(detailEntreprise)
            data.append(final)

        return Response(data)


class FindChargeAffaireForAffaire(APIView):
    def get(self, requet, id_affaire):
        try:
            affaire = Affaire.objects.get(id=id_affaire)
            charge = {
                'id': affaire.charge.id,
                'prenom': affaire.charge.first_name,
                'nom': affaire.charge.last_name
            }
            return Response(charge)
        except:
            return Response({"not found": True})


class DeleteEntrepriseAffaire(APIView):
    def get(self, request, id_affaire, id_entreprise):
        try:
            result = EntrepriseAffaire.objects.get(entreprise=id_entreprise, affaire=id_affaire).delete()
            return Response(result)
        except:
            return Response({})


class CreateAffaireAndPlanAffaire(APIView):
    def post(self, request):

        try:
            with transaction.atomic():
                affaire = Affaire(**request.data['dataAffaire'])
                affaire.save()

                plan_affaire = PlanAffaire(**request.data['dataPlanAffaire'], affaire_id=affaire.id)
                plan_affaire.save()

                adress = Adress(**request.data['dataAdresseChantier'])
                adress.save()

                chantier = Chantier(batiment_id=request.data['dataBatiment'], plan_affaire_id=plan_affaire.id,
                                    adresse_id=adress.id)
                chantier.save()

                for mission in request.data['dataMissions']:
                    mission_active = MissionActive(id_mission_id=mission, id_affaire_id=affaire.id)
                    mission_active.save()

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)


class EditPlanAffaire(APIView):
    def put(self, request, id_plan):
        try:
            with transaction.atomic():
                data = request.data
                PlanAffaire.objects.filter(id=id_plan).update(
                    risque=data['risque'],
                    libelle=data['libelle'],
                    devise=data['devise'],
                    type=data['type'],
                    type_montant=data['type_montant'],
                    prix=data['prix'],
                    debut_prestation=data['debut_prestation'],
                    fin_chantier=data['fin_chantier'],
                    visite=data['visite'],
                    doc=data['doc'],
                    debut_chantier=data['debut_chantier'],
                )
                Affaire.objects.filter(id=data['affaire']['id']).update(charge_id=data['affaire']['charge'])
                Chantier.objects.filter(id=data['chantier']['id']).update(batiment_id=data['destinationSelect'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)


"""
class GetAllPlansAffaire(APIView):
    def get(self, request):
        try:
            plans_affaire = PlanAffaire.objects.all()
            data = []

            for plan_affaire in plans_affaire:
                plan_affaire_data = model_to_dict(plan_affaire)

                # On cherche l'affaire
                affaire = Affaire.objects.get(id=plan_affaire.affaire_id)
                plan_affaire_data['affaire'] = model_to_dict(affaire)

                # On cherche la ville
                chantier = model_to_dict(Chantier.objects.get(plan_affaire=plan_affaire.id))
                adresse = Adress.objects.get(id=chantier['adresse_id'])
                plan_affaire_data['adresse'] = model_to_dict(adresse)

                # On cherche le charge
                charge_affaire = Collaborateurs.objects.get(id=affaire.charge_id)
                plan_affaire_data['charge_affaire'] = {
                    'nom': charge_affaire.last_name,
                    'prenom': charge_affaire.first_name,
                }

                # On cherche le client
                client = Entreprise.objects.get(id=affaire.client_id)
                adresse_client = model_to_dict(client.adresse)
                client_data = model_to_dict(client)
                client_data['adresse'] = adresse_client
                plan_affaire_data['client'] = client_data

                # On cherche le batiment
                batiment = Batiment.objects.get(id=chantier['batiment_id'])
                plan_affaire_data['batiment'] = model_to_dict(batiment)

                # On ajoute le chantier
                plan_affaire_data['chantier'] = chantier

                data.append(plan_affaire_data)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""


class GetAllPlansAffaire(APIView):
    def get(self, request):
        try:
            plans_affaire = PlanAffaire.objects.all()
            data = []

            for plan_affaire in plans_affaire:
                plan_affaire_data = model_to_dict(plan_affaire)

                # On cherche l'affaire
                affaire = Affaire.objects.get(id=plan_affaire.affaire_id)
                plan_affaire_data['affaire'] = model_to_dict(affaire)

                # On cherche la ville
                try:
                    chantier = Chantier.objects.get(plan_affaire=plan_affaire.id)
                    chantier_data = model_to_dict(chantier)
                    adresse = Adress.objects.get(id=chantier.adresse_id)
                    chantier_data['adresse'] = model_to_dict(adresse)
                    plan_affaire_data['chantier'] = chantier_data

                    # On cherche le batiment
                    batiment = Batiment.objects.get(id=chantier.batiment_id)
                    plan_affaire_data['batiment'] = model_to_dict(batiment)
                except Chantier.DoesNotExist:
                    plan_affaire_data['chantier'] = None
                    plan_affaire_data['batiment'] = None
                    plan_affaire_data['adresse'] = None

                # On cherche lte charge
                charge_affaire = Collaborateurs.objects.get(id=affaire.charge_id)
                plan_affaire_data['charge_affaire'] = {
                    'nom': charge_affaire.last_name,
                    'prenom': charge_affaire.first_name,
                }
                # On cherche le client
                client = Entreprise.objects.get(id=affaire.client_id)
                adresse_client = model_to_dict(client.adresse)
                client_data = model_to_dict(client)
                client_data['adresse'] = adresse_client
                plan_affaire_data['client'] = client_data
                data.append(plan_affaire_data)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AffaireListView(APIView):
    def get(self, request, *args, **kwargs):
        affaires = Affaire.objects.all()
        data = []
        for affaire in affaires:
            data.append({
                'id': affaire.id,
                'libelle': affaire.libelle,
                'statut': affaire.statut,
                'numero_offre': affaire.numero_offre,
                'numero_contrat': affaire.numero_contrat,
                'libelle_contrat': affaire.libelle_contrat,
                'date_contrat': affaire.date_contrat,
                'client': affaire.client.id if affaire.client else None,
                'charge': affaire.charge.id if affaire.charge else None,
                'assistant': affaire.assistant.id if affaire.assistant else None,
                'chef': affaire.chef.id if affaire.chef else None,
                'produit':affaire.produit.libelle if affaire.produit else None,
            })
        return Response(data, status=status.HTTP_200_OK)


from .models import Tutorial
from .serializers import TutorialSerializer


class TutorialIDList(APIView):
    def get(self, request):
        tutorials = Tutorial.objects.all()
        serializer = TutorialSerializer(tutorials, many=True)
        return Response(serializer.data)


class TutoratViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [IsAuthenticated]
