from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Mission, MissionActive, InterventionTechnique, Article, ArticleSelect, ArticleMission
from .permissions import IsAdminAuthenticated
from .serializers import MissionSerializer, MissionActiveSerializer, InterventionTechniqueSerializer, ArticleSerializer, \
    ArticleSelectSerializer, ArticleMissionSerializer, MissionActiveDetailSerializer, MissionSActiveSerializer, \
    SousMissionSerializer
from rest_framework.views import APIView
from Dashbord.models import Affaire, PlanAffaire
from collaborateurs.models import Collaborateurs
from django.forms.models import model_to_dict
from rest_framework import status, viewsets, generics
from django.db import transaction
from utils.utils import getllFirstParentOfArticle, getSubAffaireChild, getParentAffaire
from RICT.models import MissionRICT


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


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


"""
class MissionActiveAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = MissionActiveSerializer
    queryset = MissionActive.objects.all()
    permission_classes = [IsAdminAuthenticated]"""


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


class AddMissionActive(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                MissionActive.objects.filter(id_affaire=request.data['affaire']).delete()
                for mission in request.data['missions']:
                    MissionActive(id_affaire_id=request.data['affaire'], id_mission_id=mission).save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

                # article_obj = Article.objects.get(id=article)
                # ancestors, descendants = article_obj.get_ancestors_and_descendants()

                # article_lst = ancestors + [article_obj] + descendants

                # for article in article_lst:
                #     if check:
                #         if not ArticleSelect.objects.filter(affaire=id_affaire, article=article.id).exists():
                #             ArticleSelect(affaire_id=id_affaire, article_id=article.id).save()
                #     else:
                #         ArticleSelect.objects.filter(affaire=id_affaire, article=article.id).delete()
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


class MissionActiveDetailAPIView(APIView):
    def get(self, request, affaire_id, *args, **kwargs):
        try:
            mission_active = MissionActive.objects.get(id_affaire_id=affaire_id)
            serializer = MissionActiveDetailSerializer(mission_active)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MissionActive.DoesNotExist:
            return Response({'error': 'No missions found for this Affaire.'}, status=status.HTTP_404_NOT_FOUND)


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