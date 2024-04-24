from django.shortcuts import render
from .permissions import IsAdminAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import RICTSerializer, DispositionSerializer, AvisArticleSerializer, CommentaireAvisArticleSerializer, DescriptionSommaireSerializer, MissionRICTSerializer
from .models import RICT, Disposition, AvisArticle, CommentaireAvisArticle, DescriptionSommaire, MissionRICT
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.db import transaction
from rest_framework import status
from mission.models import ArticleMission, MissionActive, Mission, ArticleSelect
from Dashbord.models import PlanAffaire
from utils.utils import getSubAffaireChild
from ouvrage.models import Documents
import datetime
# Create your views here.

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()



class RICTViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = RICTSerializer
    queryset = RICT.objects.all()
    permission_classes = [IsAdminAuthenticated]

class DispositionViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DispositionSerializer
    queryset = Disposition.objects.all()
    permission_classes = [IsAdminAuthenticated]

class AvisArticleViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AvisArticleSerializer
    queryset = AvisArticle.objects.all()
    permission_classes = [IsAdminAuthenticated]

class CommentaireAvisArticleViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentaireAvisArticleSerializer
    queryset = CommentaireAvisArticle.objects.all()
    permission_classes = [IsAdminAuthenticated]


class DescriptionSommaireViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DescriptionSommaireSerializer
    queryset = DescriptionSommaire.objects.all()
    permission_classes = [IsAdminAuthenticated]
    
class MissionRICTViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = MissionRICTSerializer
    queryset = MissionRICT.objects.all()
    permission_classes = [IsAdminAuthenticated]


class CheckRICTForAffaire(APIView):
    def get(self, request, id_affaire):
        try:
            data = []
            rict = RICT.objects.filter(affaire=id_affaire)
            for ri in rict:
                data.append(model_to_dict(ri))
            return Response(data)
        except:
            return Response(False)
        
class GetAllDispositionByRICTandMission(APIView):
    def get(self, request, id_rict, id_mission):
        dispositions = Disposition.objects.filter(rict=id_rict)
        data = []
        for disposition in dispositions:
            if disposition.article.mission.id == id_mission:
                data.append(model_to_dict(disposition))
        return Response(data)
        
class GetAllAvisByRICTandMission(APIView):
    def get(self, request, id_rict, id_mission):
        all_avis = AvisArticle.objects.filter(rict=id_rict)
        data = []
        for avis in all_avis:
            if avis.article.mission.id == id_mission:
                prepare = model_to_dict(avis)
                prepare['commentaires'] = []
                commentaires = CommentaireAvisArticle.objects.filter(id_avis=avis.id)
                for commentaire in commentaires:
                    prepare['commentaires'].append(model_to_dict(commentaire))
                data.append(prepare)
        return Response(data)
    
class GetDesriptionSommaireByRICT(APIView):
    def get(self, request, id_rict):
        descriptions = DescriptionSommaire.objects.filter(rict=id_rict)
        data = []

        for description in descriptions:
            data.append(model_to_dict(description))

        return Response(data)
    
class SaveDecriptionSommaire(APIView):
    def put(self, request):
        try:
            with transaction.atomic():
                descriptions = request.data['descriptions']
                
                for description in descriptions:
                    if 'id' in description:
                        description['rict_id'] = description.pop('rict')
                        DescriptionSommaire.objects.filter(id=description['id']).update(**description)
                    else:
                        DescriptionSommaire(**description).save()
            
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    
class SaveArticleDisposition(APIView):
    def post(self, request, rict, article, mission):
        try:
            with transaction.atomic():
                commentaire = request.data['commentaire']
                avis = request.data['avis']
                commentsAvis = request.data['commentAvis']
                
                id_avis = None
                
                article_mission = ArticleMission.objects.get(article=article, mission=mission)
                
                if Disposition.objects.filter(rict=rict, article=article_mission).exists():
                    Disposition.objects.filter(rict=rict, article=article_mission).update(commentaire=commentaire)
                else:
                    Disposition(rict_id=rict, article=article_mission, commentaire=commentaire).save()
                    
                if avis != 'false':
                    if AvisArticle.objects.filter(rict=rict, article=article_mission).exists():
                        AvisArticle.objects.filter(rict=rict, article=article_mission).update(codification=avis)
                    else:
                        AvisArticle(rict_id=rict, article=article_mission, codification=avis).save()
        
                    id_avis = AvisArticle.objects.get(rict=rict, article=article_mission).id
                else:
                    AvisArticle.objects.filter(rict=rict, article=article_mission).delete()
                    
                if id_avis:
                    CommentaireAvisArticle.objects.filter(id_avis=id_avis).delete()
                    for comment in commentsAvis:
                        CommentaireAvisArticle(id_avis_id=id_avis, commentaire=comment['commentaire'], a_suivre=comment['a_suivre']).save()
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    
class GetDisposionAvisAndComment(APIView):
    def get(self, request, rict, article, mission):
        try:
            data = {}
            
            article_mission = ArticleMission.objects.get(article=article, mission=mission)
            
            if Disposition.objects.filter(rict=rict, article=article_mission).exists():
                dispo = Disposition.objects.get(rict=rict, article=article_mission)
                data['disposition'] = model_to_dict(dispo)
                
            if AvisArticle.objects.filter(rict=rict, article=article_mission).exists():
                avis = AvisArticle.objects.get(rict=rict, article=article_mission)
                data['avis'] = model_to_dict(avis)
                data['avis']['commentaires'] = []
                for comment in CommentaireAvisArticle.objects.filter(id_avis=avis.id):
                    data['avis']['commentaires'].append(model_to_dict(comment))
                

        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data, status=status.HTTP_200_OK)
    
class ValidateDevalidateMissionRict(APIView):
    def post(self, request, id_rict, id_mission):
        try:
            with transaction.atomic():
                validate = request.data['validate']
                rict = RICT.objects.get(id=id_rict)
                mission_active = MissionActive.objects.get(id_mission=id_mission, id_affaire=rict.affaire)
                if validate:
                    MissionRICT(rict=rict, mission=mission_active).save()
                else:
                    MissionRICT.objects.filter(rict=rict, mission=mission_active).delete()
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    
class ValidateRICT(APIView):
    def put(self, request, id_rict):
        try:
            data = {}
            with transaction.atomic():
                exist = MissionRICT.objects.filter(rict=id_rict).exists()
                if exist:
                    RICT.objects.filter(id=id_rict).update(statut=1)
                    data['validate'] = True
                else:
                    data['validate'] = False
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK, data=data)

class GenerateDataForRICT(APIView):
    def get(self, request, id_rict, plan_affaire):
        # try:
            rict = RICT.objects.get(id=id_rict)

            data = {}

            # # Donne du rict

            data['rict'] = model_to_dict(rict)

            # # Donne de l'affaire

            data['affaire'] = model_to_dict(rict.affaire)

            # # Donne du charge d'affaire

            charge = rict.affaire.charge

            data['charge'] = model_to_dict(charge)
            if charge.address:
                data['charge']['adresse'] = model_to_dict(charge.address)

            # Donne de l'entreprise cliente

            entreprise = rict.affaire.client

            data['client'] = model_to_dict(entreprise)
            data['client']['adresse'] = model_to_dict(entreprise.adresse)

            # # All mission

            data['mission'] = []
            id_affaire = rict.affaire

            all_mission = MissionActive.objects.filter(id_affaire=id_affaire)

            for mission in all_mission:
                data['mission'].append(model_to_dict(mission.id_mission))

            # # Data plan affaire
            
            data['plan'] = model_to_dict(PlanAffaire.objects.get(id=plan_affaire))
            
            # # Data about description sommaire
            
            descriptions = DescriptionSommaire.objects.filter(rict=id_rict)
            data['descriptions'] = []

            for description in descriptions:
                data['descriptions'].append(model_to_dict(description))
                
            # # Data about mission and all
            
            missionsActive = MissionActive.objects.filter(id_affaire=rict.affaire)
            data_missions = []
            for missionActive in missionsActive:

                mission = missionActive.id_mission
                if mission.mission_parent == None:
                    childs = Mission.objects.filter(mission_parent=mission.id)
                    if len(childs) == 0:
                        result = {}
                        result['mission'] = model_to_dict(mission)
                        result['chapitre'] = model_to_dict(mission)
                        result = getAllArticle(result, rict.affaire)
                        
                        # inject avis and disposition
                        result = getAvisAndDisposition(result, rict)
                        data_missions.append(result)
                    else:
                        for child in childs:
                            result = {}
                            result['mission'] = model_to_dict(mission)
                            result['chapitre'] = model_to_dict(child)
                            result = getAllArticle(result, rict.affaire)
                            
                            # inject avis and disposition
                            result = getAvisAndDisposition(result, rict)
                            data_missions.append(result)
                            
            data['missions'] = data_missions

            return Response(data)

        # except:
        #     return Response({})

def getAllArticle(data_mission, affaire):
    articlesSelect = ArticleSelect.objects.filter(affaire=affaire)

    articles = []
    
    unique_parents = []
    
    for articleSelect in articlesSelect:
        if ArticleMission.objects.filter(mission=data_mission['chapitre']['id'], article=articleSelect.article.id).exists():
            articles.append(articleSelect.article)
            if articleSelect.article.article_parent != None and articleSelect.article.article_parent not in unique_parents:
                unique_parents.append(articleSelect.article.article_parent)

    pre_data = []
    data = []

    for article in articles:
        pre_data.append(getSubAffaireChild(article, data_mission['chapitre']['id']))
        
    for parent in unique_parents:
        final_parent = {
            'parent' : model_to_dict(parent),
            'childs' : []
        }
        for article in pre_data:
            if article['parent']['article_parent'] == parent.id:
                final_parent['childs'].append(article)
        data.append(final_parent)
        
    data_mission['articles'] = data

    return data_mission;

def getAvisAndDisposition(data_mission, rict):
    for index, article in enumerate(data_mission['articles']):
        data_mission['articles'][index] = recursInsertData(data_mission['articles'][index], rict, data_mission['chapitre']['id'])
    return data_mission;
    

def recursInsertData(article, rict, mission):
    
    # Insert here disposition and avis
    data = {}
    # print(article)
    # print(rict)
    # print(mission)
    article_mission = ArticleMission.objects.get(article=article['parent']['id'], mission=mission)
    
    if Disposition.objects.filter(rict=rict, article=article_mission).exists():
        dispo = Disposition.objects.get(rict=rict, article=article_mission)
        data['disposition'] = model_to_dict(dispo)
        
    if AvisArticle.objects.filter(rict=rict, article=article_mission).exists():
        avis = AvisArticle.objects.get(rict=rict, article=article_mission)
        data['avis'] = model_to_dict(avis)
        data['avis']['commentaires'] = []
        for comment in CommentaireAvisArticle.objects.filter(id_avis=avis.id):
            data['avis']['commentaires'].append(model_to_dict(comment))

    article['data'] = data
    
    for child in article['childs']:
        child = recursInsertData(child, rict, mission)
        
    return article;

class ReviserRICT(APIView):
    def get(self, request, id_rict):
        try:
            with transaction.atomic():
                old_rict = RICT.objects.get(id=id_rict)
                old_rict.statut = 2
                old_rict.save()
                new_rict = RICT.objects.create(
                    affaire=old_rict.affaire,
                    statut=0,
                    date=datetime.datetime.now()
                )
                new_rict.save()
                
                old_dipositions = Disposition.objects.filter(rict=old_rict)
                for old_disposition in old_dipositions:
                    Disposition.objects.create(
                        rict=new_rict,
                        article=old_disposition.article,
                        commentaire=old_disposition.commentaire
                    ).save()
                    
                old_avis = AvisArticle.objects.filter(rict=old_rict)
                for old_avi in old_avis:
                    new_avis = AvisArticle.objects.create(
                        rict=new_rict,
                        article=old_avi.article,
                        codification=old_avi.codification
                    )
                    new_avis.save()
                    
                    old_comments = CommentaireAvisArticle.objects.filter(id_avis=old_avi.id)
                    for old_comment in old_comments:
                        CommentaireAvisArticle.objects.create(
                            id_avis=new_avis,
                            commentaire=old_comment.commentaire,
                            a_suivre=old_comment.a_suivre,
                            lever=old_comment.lever
                        ).save()

                old_descriptions = DescriptionSommaire.objects.filter(rict=old_rict)
                for old_description in old_descriptions:
                    DescriptionSommaire.objects.create(
                        rict=new_rict,
                        type=old_description.type,
                        content=old_description.content
                    ).save()
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)