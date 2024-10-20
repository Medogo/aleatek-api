import logging
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Mission, MissionActive, InterventionTechnique, Article, ArticleSelect, ArticleMission
from .permissions import IsAdminAuthenticated
from .serializers import MissionSerializer, MissionActiveSerializer, InterventionTechniqueSerializer, ArticleSerializer, \
    ArticleSelectSerializer, ArticleMissionSerializer, MissionActiveDetailSerializer, MissionSActiveSerializer, \
    SousMissionSerializer, AffaireWithMissionsSerializer
from rest_framework.views import APIView
from Dashbord.models import Affaire, PlanAffaire
from collaborateurs.models import Collaborateurs
from django.forms.models import model_to_dict
from rest_framework import status, viewsets, generics
from django.db import transaction
from utils.utils import getllFirstParentOfArticle, getSubAffaireChild, getParentAffaire
from RICT.models import MissionRICT  
from rest_framework import serializers, views, status
from rest_framework.response import Response
from .models import Mission, MissionActive
from .serializers import MissionSerializer, MissionActiveSerializer, SousMissionActivationSerializer, MissionActiveSerializerMission
from Dashbord.views import ActiveAffaireView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Mission, MissionActive, Affaire, DocumentAffectationIT
from .serializers import MissionActiveSerializerMission
from .serializers import DocumentAffectationITSerializers


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()



class DocumentAffectationITSerializersView(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DocumentAffectationITSerializers
    queryset = DocumentAffectationIT.objects.all()
    permission_classes = [IsAdminAuthenticated]



class ArticleMissionViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleMissionSerializer
    queryset = ArticleMission.objects.all()
    permission_classes = [IsAdminAuthenticated]


class MissionAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = MissionSerializer
    queryset = Mission.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ArticleAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ArticleSelectViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleSelectSerializer
    queryset = ArticleSelect.objects.all()
    permission_classes = [IsAdminAuthenticated]



class ITAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = InterventionTechniqueSerializer
    queryset = InterventionTechnique.objects.all()
    permission_classes = [IsAdminAuthenticated]


class MissionActiveForCurrentAffaire(APIView):
    def get(self, request, id_affaire):
        all_mission_active = MissionActive.objects.filter(id_affaire=id_affaire).values()

        return Response(list(all_mission_active))


class VerifyExistITForMissionSignAndCollab(APIView):
    def get(self, request, id_collab, id_mission_sign):
        try:
            InterventionTechnique.objects.get(id_mission_active=id_mission_sign, id_collaborateur=id_collab)
            return Response({'check': True})
        except:
            return Response({'check': False})


class VerifyExistMissionActive(APIView):
    def get(self, request, id_affaire, id_mission):
        try:
            mission = MissionActive.objects.get(id_mission=id_mission, id_affaire=id_affaire)
            return Response({'check': mission.id})
        except:
            return Response({'check': False})


class AllIntervenantForAffaire(APIView):
    def get(self, request, id_affaire):
        all_collab = Collaborateurs.objects.all()
        all_IT = InterventionTechnique.objects.all()

        data = []

        for collab in all_collab:
            for IT in all_IT:
                if collab.id == IT.id_collaborateur.id:
                    missionActive = IT.id_mission_active
                    affaire = missionActive.id_affaire
                    if affaire.id == id_affaire:
                        data.append({
                            "id": collab.id,
                            "nom": collab.first_name,
                            "prenom": collab.last_name,
                            "email": collab.email
                        })

        return Response(data)


class AllMissionForAffaire(APIView):
    def get(self, request, id_affaire):
        mission_actives = MissionActive.objects.all()

        data = []
        for mission_active in mission_actives:
            affaire = mission_active.id_affaire
            if id_affaire == affaire.id:
                data_mission = mission_active.id_mission
                transform = model_to_dict(data_mission)
                data.append(transform)

        return Response(data)


class GetAllParentMission(APIView):
    def get(self, request):
        data = Mission.objects.filter(mission_parent=None).values()

        return Response(list(data))


class GetAllMissionViewByChapitre(APIView):
    def get(self, request, id_affaire, id_rict):
        missionsActive = MissionActive.objects.filter(id_affaire=id_affaire)
        data = []
        for missionActive in missionsActive:

            mission = missionActive.id_mission
            if mission.mission_parent == None:

                childs = Mission.objects.filter(mission_parent=mission.id)
                if len(childs) == 0:
                    result = {}
                    result['mission'] = model_to_dict(mission)
                    result['chapitre'] = model_to_dict(mission)
                    check = MissionRICT.objects.filter(rict=id_rict, mission=missionActive.id).exists()
                    result['chapitre']['check'] = check
                    data.append(result)
                else:
                    for child in childs:
                        result = {}
                        result['mission'] = model_to_dict(mission)
                        result['chapitre'] = model_to_dict(child)
                        active_mission = MissionActive.objects.filter(id_affaire=id_affaire, id_mission=mission.id)
                        check = MissionRICT.objects.filter(rict=id_rict, mission=active_mission[0].id).exists()
                        result['chapitre']['check'] = check
                        data.append(result)

        return Response(data)


class GetAllArticleForMission(APIView):
    def get(self, request, id_mission, id_affaire):
        articlesSelect = ArticleSelect.objects.filter(affaire=id_affaire)

        articles = []

        unique_parents = []

        for articleSelect in articlesSelect:
            if ArticleMission.objects.filter(mission=id_mission, article=articleSelect.article.id).exists():
                articles.append(articleSelect.article)
                if articleSelect.article.article_parent != None and articleSelect.article.article_parent not in unique_parents:
                    unique_parents.append(articleSelect.article.article_parent)

        pre_data = []
        data = []

        for article in articles:
            pre_data.append(getSubAffaireChild(article, id_mission))

        for parent in unique_parents:
            final_parent = {
                'parent': model_to_dict(parent),
                'childs': []
            }
            for article in pre_data:
                if article['parent']['article_parent'] == parent.id:
                    final_parent['childs'].append(article)
            data.append(final_parent)

        return Response(data)


class GetAllCritereForAffaire(APIView):
    def get(self, request, id_affaire):
        articles_mission_active = Article.objects.filter(
            mission__missionactive__id_affaire=id_affaire,
            article_parent__article_parent__isnull=True
        )

        result = []

        for article_mission_active in articles_mission_active:
            if article_mission_active.article_parent != None:
                toAppend = model_to_dict(article_mission_active)
                toAppend['parent'] = model_to_dict(article_mission_active.article_parent)
                check_exist = ArticleSelect.objects.filter(affaire=id_affaire,
                                                           article=article_mission_active.id).exists()
                toAppend['select'] = check_exist
                result.append(toAppend)

        return Response(result)


class AddArticleSelectForAffaire(APIView):
    def get(self, request, id_affaire, id_article):
        exist = ArticleSelect.objects.filter(affaire=id_affaire, article=id_article).exists()

        if not exist:
            new = ArticleSelect(affaire_id=id_affaire, article_id=id_article)
            new.save()
            return Response({'id': new.id})

        return Response({'id': None})


class DeleteArticleSelectForAffaire(APIView):
    def get(self, request, id_affaire, id_article):
        try:
            ArticleSelect.objects.filter(affaire=id_affaire, article=id_article).delete()
            return Response({'delete': True})
        except:
            return Response({'delete': False})


logger = logging.getLogger(__name__)


class AddMissionActive(APIView):
    def post(self, request):
        try:
            affaire_id = request.data.get('affaire')
            missions = request.data.get('missions')

            if not affaire_id or not missions:
                return Response({"error": "Affaire or missions data is missing"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                MissionActive.objects.filter(id_affaire=affaire_id).delete()

                for mission_id in missions:
                    MissionActive(id_affaire_id=affaire_id, id_mission_id=mission_id).save()

        except KeyError as e:
            logger.error(f"Missing data: {e}")
            return Response({"error": f"Missing data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)


class AddInterventionTechnique(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                mission = request.data['mission_sign']
                for collab in request.data['collaborateurs']:
                    if not InterventionTechnique.objects.filter(id_mission_active=mission,
                                                                id_collaborateur=collab).exists():
                        InterventionTechnique(id_mission_active_id=mission, id_collaborateur_id=collab,
                                              affecteur=request.user).save()
        except Exception as ex:
            print(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)


class GetCritereAboutDescriptionBati(APIView):
    def get(self, request, id_affaire):
        data = []
        try:
            articles = Article.objects.filter(article_parent__article_parent__isnull=True,
                                              article__mission__in=[1, 2, 3, 4])
            for article in articles:
                if article.article_parent != None:
                    result = model_to_dict(article)

                    if ArticleSelect.objects.filter(article=article.id, affaire=id_affaire).exists():
                        result['select'] = True
                    else:
                        result['select'] = False

                    result['parent'] = model_to_dict(article.article_parent)
                    data.append(result)
        except Exception as ex:
            print(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data)


class GetCritereAboutCodeTravail(APIView):
    def get(self, request, id_affaire):
        data = []
        try:
            articles = Article.objects.filter(article_parent__article_parent__isnull=True,
                                              article__mission__in=[31, 32, 29, 30, 24, 25, 26])
            for article in articles:
                if article.article_parent != None:
                    result = model_to_dict(article)

                    if ArticleSelect.objects.filter(article=article.id, affaire=id_affaire).exists():
                        result['select'] = True
                    else:
                        result['select'] = False

                    result['parent'] = model_to_dict(article.article_parent)
                    data.append(result)
        except Exception as ex:
            print(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data)


class HandleSelectCritere(APIView):
    def post(self, request, id_affaire, article):
        try:
            with transaction.atomic():
                check = request.data['check']

                if check:
                    if not ArticleSelect.objects.filter(affaire=id_affaire, article=article).exists():
                        ArticleSelect(affaire_id=id_affaire, article_id=article).save()
                else:
                    ArticleSelect.objects.filter(affaire=id_affaire, article=article).delete()

        except Exception as ex:
            print(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)


class MissionActiveViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            mission_active = MissionActive.objects.get(pk=pk)
        except MissionActive.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = MissionActiveSerializer(mission_active)
        return Response(serializer.data)


class MissionActiveView(viewsets.ModelViewSet):
    queryset = MissionActive.objects.all()
    serializer_class = MissionActiveSerializer
    permission_classes = [IsAdminAuthenticated]


class MissionActiveCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MissionSActiveSerializer(data=request.data)
        if serializer.is_valid():
            mission_active = serializer.save()
            return Response({'message': 'Missions successfully assigned to the Affaire.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MissionActiveDetailView(generics.RetrieveAPIView):
    queryset = MissionActive.objects.all()
    serializer_class = MissionActiveDetailSerializer
    lookup_field = 'id_affaire'


class AddSousMissionView(generics.CreateAPIView):
    serializer_class = SousMissionSerializer

    def post(self, request, *args, **kwargs):
        mission_parent_id = kwargs.get('mission_parent_id')
        mission_parent = Mission.objects.get(id=mission_parent_id)

        # Créer une nouvelle sous-mission en assignant la mission parent
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(mission_parent=mission_parent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AffaireDetailView(generics.RetrieveAPIView):
    queryset = Affaire.objects.all()
    serializer_class = AffaireWithMissionsSerializer
    lookup_field = 'id'


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticated]  # Notez que c'est une liste

    def list(self, request, *args, **kwargs):
        # Assurez-vous que `self.queryset` est un QuerySet et pas un seul objet
        missions = self.queryset  # C'est généralement correct
        return Response(MissionSerializer(missions, many=True).data)


class MissionActiveViewSet(viewsets.ModelViewSet):
    queryset = MissionActive.objects.all()
    serializer_class = MissionActiveSerializer
    permission_classes = [IsAuthenticated]  # Notez que c'est une liste

    def get_queryset(self):
        affaire_id = self.kwargs.get('affaire_id')
        queryset = MissionActive.objects.filter(id_affaire=affaire_id)
        print(f"Queryset: {queryset}")  # Affichez le QuerySet pour vérifier les objets
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'detail': 'Aucune mission active trouvée.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def get_active_missions_for_affaire(request, affaire_id):
    # Récupérer l'Affaire courante
    affaire = get_object_or_404(Affaire, id=affaire_id)

    # Filtrer les missions actives pour l'Affaire courante
    missions_actives = MissionActive.objects.filter(id_affaire=affaire, id_mission__is_active=True)

    # Sérialiser les données
    serializer = MissionActiveSerializer(missions_actives, many=True)
    
    return Response(serializer.data)



class AffaireMissionsView(APIView):
    def get(self, request):
        try:
            active_affaire = Affaire.objects.get(is_active=True)
            
            # Utilisez values() pour obtenir un dictionnaire et éviter tout filtrage potentiel
            all_missions = MissionActive.objects.filter(id_affaire=active_affaire).values(
                'id',
                'is_active',
                'id_mission__id',
                'id_mission__code_mission',
                'id_mission__libelle'
            )
            
            serialized_missions = [
                {
                    'id': mission['id_mission__id'],
                    'code_mission': mission['id_mission__code_mission'],
                    'libelle': mission['id_mission__libelle'],
                    'is_active': mission['is_active']
                } for mission in all_missions
            ]
            
            print(f"Nombre de missions trouvées : {len(serialized_missions)}")
            
            return Response({
                'active_affaire_id': active_affaire.id,
                'missions': serialized_missions
            }, status=status.HTTP_200_OK)
        except Affaire.DoesNotExist:
            return Response({'detail': "Aucune affaire active trouvée."}, status=status.HTTP_404_NOT_FOUND)

class ToggleMissionActiveView(APIView):
    def post(self, request):
        try:
            active_affaire = Affaire.objects.get(is_active=True)
            mission_ids = request.data.get('mission_ids', [])
            
            if not mission_ids:
                return Response({'detail': "Aucun ID de mission fourni."}, status=status.HTTP_400_BAD_REQUEST)
            
            updated_missions = []
            for mission_id in mission_ids:
                mission_active, created = MissionActive.objects.get_or_create(
                    id_affaire=active_affaire,
                    id_mission_id=mission_id,
                    defaults={'is_active': False}
                )
                
                # Basculer l'état actif
                mission_active.is_active = not mission_active.is_active
                mission_active.save()
                
                updated_missions.append({
                    'mission_id': mission_id,
                    'is_active': mission_active.is_active
                })
            
            return Response({
                'updated_missions': updated_missions
            }, status=status.HTTP_200_OK)
        except Affaire.DoesNotExist:
            return Response({'detail': "Aucune affaire active trouvée."}, status=status.HTTP_404_NOT_FOUND)
 
# View
class SousMissionsActivationView(views.APIView):
    def get(self, request, mission_id):
        try:
            mission = Mission.objects.get(id=mission_id, mission_parent__isnull=True)
            sous_missions = mission.sous_missions.all()
            serializer = MissionSerializer(sous_missions, many=True)
            return Response(serializer.data)
        except Mission.DoesNotExist:
            return Response({"error": "Mission parente non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def post(self, request, mission_id):
        serializer = SousMissionActivationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            mission_parente = Mission.objects.get(id=mission_id, mission_parent__isnull=True)
            sous_missions = serializer.validated_data['sous_missions']
            affaire_id = serializer.validated_data['affaire_id']

            def update_missions():
                for sous_mission_id, is_active in sous_missions.items():
                    try:
                        sous_mission = Mission.objects.get(id=int(sous_mission_id), mission_parent=mission_parente)
                        mission_active, created = MissionActive.objects.get_or_create(
                            id_mission=sous_mission,
                            id_affaire_id=affaire_id,
                            defaults={'is_active': is_active}
                        )
                        if not created:
                            mission_active.is_active = is_active
                            mission_active.save()
                        yield mission_active
                    except Mission.DoesNotExist:
                        raise ValueError(f"Sous-mission {sous_mission_id} non trouvée ou n'appartient pas à la mission parente")

            updated_missions = list(update_missions())
            serializer = MissionActiveSerializer(updated_missions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Mission.DoesNotExist:
            return Response({"error": "Mission parente non trouvée"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class MissionAddParentesSousMissionAffaireViewSet(viewsets.ModelViewSet):
    serializer_class = MissionSerializer
    queryset = Mission.objects.all()

    def get_active_affaire(self):
        view = ActiveAffaireView()
        response = view.get(self.request)
        if response.status_code == status.HTTP_200_OK:
            return Affaire.objects.get(id=response.data['active_affaire_id'])
        return None

    @action(detail=False, methods=['GET'])
    def active_parent_missions(self, request):
        active_affaire = self.get_active_affaire()
        if not active_affaire:
            return Response({"error": "Aucune affaire active trouvée"}, status=status.HTTP_404_NOT_FOUND)

        parent_missions = Mission.objects.filter(mission_parent__isnull=True)
        serializer = self.get_serializer(parent_missions, many=True)
        
        # Ajouter l'état d'activation pour chaque mission parente
        for mission_data in serializer.data:
            mission_data['is_active'] = MissionActive.objects.filter(
                id_mission_id=mission_data['id'],
                id_affaire=active_affaire,
                is_active=True
            ).exists()

        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def child_missions(self, request, pk=None):
        parent_mission = self.get_object()
        active_affaire = self.get_active_affaire()
        if not active_affaire:
            return Response({"error": "Aucune affaire active trouvée"}, status=status.HTTP_404_NOT_FOUND)

        child_missions = Mission.objects.filter(mission_parent=parent_mission)
        serializer = self.get_serializer(child_missions, many=True)

        # Ajouter l'état d'activation pour chaque mission fille
        for mission_data in serializer.data:
            mission_data['is_active'] = MissionActive.objects.filter(
                id_mission_id=mission_data['id'],
                id_affaire=active_affaire,
                is_active=True
            ).exists()

        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def toggle_mission_activation(self, request, pk=None):
        mission = self.get_object()
        active_affaire = self.get_active_affaire()
        if not active_affaire:
            return Response({"error": "Aucune affaire active trouvée"}, status=status.HTTP_404_NOT_FOUND)

        mission_active, created = MissionActive.objects.get_or_create(
            id_mission=mission,
            id_affaire=active_affaire,
            defaults={'is_active': True}
        )

        if not created:
            mission_active.is_active = not mission_active.is_active
            mission_active.save()

        status_message = "activée" if mission_active.is_active else "désactivée"
        logger.info(f"Mission {mission.id} {status_message} pour l'affaire {active_affaire.id}")

        return Response({
            "mission_id": mission.id,
            "is_active": mission_active.is_active,
            "message": f"Mission {status_message} avec succès"
        })

    @action(detail=True, methods=['POST'])
    def activate_child_missions(self, request, pk=None):
        parent_mission = self.get_object()
        active_affaire = self.get_active_affaire()
        if not active_affaire:
            return Response({"error": "Aucune affaire active trouvée"}, status=status.HTTP_404_NOT_FOUND)

        mission_ids = request.data.get('mission_ids', [])
        if not mission_ids:
            return Response({"error": "mission_ids est requis"}, status=status.HTTP_400_BAD_REQUEST)

        activated_missions = []
        for mission_id in mission_ids:
            try:
                child_mission = Mission.objects.get(pk=mission_id, mission_parent=parent_mission)
                mission_active, created = MissionActive.objects.get_or_create(
                    id_mission=child_mission,
                    id_affaire=active_affaire,
                    defaults={'is_active': True}
                )
                if not created:
                    mission_active.is_active = True
                    mission_active.save()
                activated_missions.append(child_mission)
                logger.info(f"Sous-mission {child_mission.id} activée pour l'affaire {active_affaire.id}")
            except Mission.DoesNotExist:
                logger.warning(f"Sous-mission {mission_id} non trouvée ou n'est pas une sous-mission valide de {parent_mission.id}")

        serializer = self.get_serializer(activated_missions, many=True)
        return Response(serializer.data)
     
    @action(detail=True, methods=['get'])
    def count_active_child_missions(self, request, pk=None):
        """
        Compte le nombre de sous-missions actives pour une mission parente spécifique.
        """
        parent_mission = get_object_or_404(Mission, pk=pk)
        affaire = self.get_active_affaire()
        
        if not affaire:
            return Response({"error": "Aucune affaire active trouvée"}, status=status.HTTP_404_NOT_FOUND)

        # Assurez-vous que affaire est bien un objet Affaire
        if isinstance(affaire, int):
            affaire = get_object_or_404(Affaire, pk=affaire)

        active_child_count = MissionActive.objects.filter(
            id_mission__mission_parent=parent_mission,
            id_affaire=affaire,
            is_active=True
        ).count()

        total_child_count = Mission.objects.filter(mission_parent=parent_mission).count()

        return Response({
            "parent_mission_id": parent_mission.id,
            "parent_mission_code": parent_mission.code_mission,
            "active_child_missions_count": active_child_count,
            "total_child_missions_count": total_child_count,
            "affaire_id": affaire.id
        })
    
 
from django.http import HttpRequest
class SousMisToggleChildMissionView(viewsets.ViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def get_object(self, pk):
        """
        Récupère l'objet basé sur la clé primaire (pk).
        """
        try:
            return Mission.objects.get(pk=pk)
        except Mission.DoesNotExist:
            raise Response({"error": "Mission non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    def get_active_affaire(self):
        """
        Utilise la logique de ActiveAffaireView pour obtenir l'affaire active.
        """
        view = ActiveAffaireView()
        request = HttpRequest()  # Créez un objet de requête vide
        response = view.get(request)  # Appelez la méthode get
        if response.status_code == status.HTTP_200_OK:
            return response.data['active_affaire_id']
        else:
            return None

    @action(detail=True, methods=['put'])
    def toggle_child_mission(self, request, pk=None):
        parent_mission = self.get_object(pk)
        
        # Vérifiez à la fois dans request.data et request.query_params
        child_mission_id = request.data.get('child_mission_id') or request.query_params.get('child_mission_id')

        if not child_mission_id:
            return Response({"error": "child_mission_id est requis"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtenez l'affaire active
        affaire_id = self.get_active_affaire()
        if not affaire_id:
            return Response({"error": "Aucune affaire active trouvée"}, status=status.HTTP_404_NOT_FOUND)

        try:
            child_mission = Mission.objects.get(id=child_mission_id, mission_parent=parent_mission)
            affaire = Affaire.objects.get(id=affaire_id)
        except (Mission.DoesNotExist, Affaire.DoesNotExist):
            return Response({"error": "child_mission_id ou affaire_id invalide"}, status=status.HTTP_404_NOT_FOUND)

        mission_active, created = MissionActive.objects.get_or_create(
            id_mission=child_mission,
            id_affaire=affaire
        )

        # Basculer la valeur de is_active
        mission_active.is_active = not mission_active.is_active
        mission_active.save()

        serializer = MissionActiveSerializerMission(mission_active)
        return Response(serializer.data)

class SousMissionToggleChildMissionView(viewsets.ViewSet):
    queryset = Mission.objects.all()

    def get_active_affaire(self):
        """
        Utilise la logique de ActiveAffaireView pour obtenir l'affaire active.
        """
        view = ActiveAffaireView()
        request = HttpRequest()  # Créez un objet de requête vide
        response = view.get(request)  # Appelez la méthode get
        if response.status_code == status.HTTP_200_OK:
            return response.data['active_affaire_id']
        else:
            return None

    @action(detail=True, methods=['put'])
    def toggle_child_mission(self, request, pk=None):
        """
        Bascule l'état actif d'une sous-mission spécifique.
        """
        # 'pk' est l'ID de la sous-mission qu'on veut basculer
        child_mission = get_object_or_404(Mission, pk=pk)

        # Obtenir l'affaire active
        affaire = self.get_active_affaire()
        if not affaire:
            return Response({"error": "Aucune affaire active trouvée"}, status=status.HTTP_404_NOT_FOUND)

        mission_active, created = MissionActive.objects.get_or_create(
            id_mission=child_mission,
            id_affaire=affaire
        )

        # Basculer la valeur de is_active
        mission_active.is_active = not mission_active.is_active
        mission_active.save()

        serializer = MissionActiveSerializerMission(mission_active)
        return Response(serializer.data)
    