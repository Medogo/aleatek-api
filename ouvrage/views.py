from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Aso, AffaireOuvrage, Avis, Ouvrage, Documents, FichierAttache, EntrepriseAffaireOuvrage, DocumentAffectation, RemarqueAso
from .permissions import IsAdminAuthenticated
from .serializers import AsoSerializer, OuvrageSerializer, DocumentSerializer, FichierAttacheSerializer, \
    AvisSerializer, AffaireOuvrageSerializer, EntrepriseAffaireOuvrageSerializer, DocumentAffectationSerializer, RemarqueAsoSerializer
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from entreprise.models import Entreprise, Responsable
from Dashbord.models import EntrepriseAffaire
from mission.models import  MissionActive
from commentaire.models import Commentaire
from django.db import transaction
from rest_framework import status
from datetime import date
from django.db.models import Q

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    
class DocumentAffectationViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DocumentAffectationSerializer
    queryset = DocumentAffectation.objects.all()
    permission_classes = [IsAdminAuthenticated]

class AsoViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AsoSerializer
    queryset = Aso.objects.all()
    permission_classes = [IsAdminAuthenticated]
    
class RemarqueAsoViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = RemarqueAsoSerializer
    queryset = RemarqueAso.objects.all()
    permission_classes = [IsAdminAuthenticated]

class AffaireOuvrageAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AffaireOuvrageSerializer
    queryset = AffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]

from rest_framework import generics
from ouvrage.serializers import AffaireOuvrageSerializerAdmin
class AffaireOuvrageAdminViewset(generics.ListAPIView):
    serializer_class = AffaireOuvrageSerializerAdmin
    queryset = AffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]

from ouvrage.serializers import EntrepriseAffaireOuvrageSerializerAdminisrator
from rest_framework import generics
class EntrepriseAffaireOuvrageViewsetAdministration(generics.ListAPIView):
    serializer_class = EntrepriseAffaireOuvrageSerializerAdminisrator
    queryset = EntrepriseAffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]





class OuvrageAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = OuvrageSerializer
    queryset = Ouvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class DocumentSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Documents.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AvisSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AvisSerializer
    queryset = Avis.objects.all()
    permission_classes = [IsAdminAuthenticated]


class FichierSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = FichierAttacheSerializer
    queryset = FichierAttache.objects.all()
    permission_classes = [IsAdminAuthenticated]


class EntrepriseAffaireOuvrageViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EntrepriseAffaireOuvrageSerializer
    queryset = EntrepriseAffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class VerifyExistAffaireOuvrage(APIView):
    def get(self, request, id_affaire, id_ouvrage):
        try:
            AffaireOuvrage.objects.get(id_affaire=id_affaire, id_ouvrage=id_ouvrage)
            return Response({'check': True})
        except:
            return Response({'check': False})


class GetAllAffaireOuvrageByAffaire(APIView):
    def get(self, request, id_affaire):
        all_affaire_ouvrage = AffaireOuvrage.objects.filter(id_affaire=id_affaire).values()
        data = []
        for ouvrage in all_affaire_ouvrage:
            final_data = dict(ouvrage)  # Convertir l'objet QueryDict en dictionnaire
            detail_ouvrage = Ouvrage.objects.get(id=ouvrage['id_ouvrage_id'])
            ouvrage_data = model_to_dict(detail_ouvrage)
            final_data['ouvrage'] = ouvrage_data
            data.append(final_data)
        return Response(data)


class VerifyEntrepriseCollabOnOuvrage(APIView):
    def get(self, request, id_entreprise_affaire, id_ouvrage_affaire):
        try:
            EntrepriseAffaireOuvrage.objects.get(affaire_ouvrage=id_ouvrage_affaire,
            affaire_entreprise=id_entreprise_affaire)
            return Response({'check': True})
        except:
            return Response({'check': False})


class AllEntreprisebAssignToAffaireOuvrage(APIView):
    def get(self, request, id_affaire_ouvrage):
        entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(
            affaire_ouvrage=id_affaire_ouvrage).values()
        data = []
        for e_a_o in entreprise_affaire_ouvrage:
            final = dict(e_a_o)
            detailEntrepriseAffaire = EntrepriseAffaire.objects.get(id=e_a_o['affaire_entreprise_id'])
            detailEntreprise = model_to_dict(detailEntrepriseAffaire.entreprise)
            final['entreprise'] = detailEntreprise
            data.append(final)

        return Response(data)


class CodificationASOInCurrent(APIView):
    def get(self, request, id_aso):
        aviss = Avis.objects.all()
        ouvrage = Aso.objects.get(id=id_aso).affaireouvrage
        TabCodifications = []
        for avis in aviss:
            document = avis.id_document
            if document.emetteur.affaire_ouvrage.id == ouvrage.id:
                TabCodifications.append(avis.codification)

        if len(TabCodifications) == 0:
            return Response({'codification': False})

        liste = ['RMQ', 'F', 'HM', 'VI']
        unique_liste = list(set(TabCodifications))
        codification = unique_liste[0]

        for tu in unique_liste:
            if liste.index(tu) < liste.index(codification):
                codification = tu

        return Response({'codification': codification})


class CodificationASO(APIView):
    def get(self, request, id_aso):
        # aviss = Avis.objects.all()
        TabCodifications = []
        documents = Documents.objects.filter(aso=id_aso)
        for document in documents:
            aviss = Avis.objects.filter(id_document=document.id)
            for avis in aviss:
                TabCodifications.append(avis.codification)

        if len(TabCodifications) == 0:
            return Response({'codification': False})

        liste = ['RMQ', 'F', 'HM', 'VI']
        unique_liste = list(set(TabCodifications))
        codification = unique_liste[0]

        for tu in unique_liste:
            if liste.index(tu) < liste.index(codification):
                codification = tu

        return Response({'codification': codification})

class GetAllDetailDocument(APIView):
    def get(self, request, id_affaire):
        all_document = Documents.objects.all()

        data = []

        for document in all_document:
            emetteur = document.emetteur
            if emetteur != None:
                affaireOuvrage = emetteur.affaire_ouvrage
                affaireEntreprise = emetteur.affaire_entreprise

                id = affaireOuvrage.id_affaire.id
                if id == id_affaire:
                    prepare = model_to_dict(document)
                    ouvrage = affaireOuvrage.id_ouvrage
                    entreprise = affaireEntreprise.entreprise

                    prepare['ouvrage'] = model_to_dict(ouvrage)
                    prepare['entreprise'] = model_to_dict(entreprise)

                    data.append(prepare)

        return Response(data)
    
class GetAllDetailDocumentWithIdDoc(APIView):
    def get(self, request, id_affaire, id_doc):
        all_document = Documents.objects.all()
        data = []

        for document in all_document:
            emetteur = document.emetteur
            if emetteur is not None:
                affaireOuvrage = emetteur.affaire_ouvrage
                affaireEntreprise = emetteur.affaire_entreprise

                id = affaireOuvrage.id_affaire.id
                if id == id_affaire:
                    prepare = model_to_dict(document)
                    ouvrage = affaireOuvrage.id_ouvrage
                    entreprise = affaireEntreprise.entreprise

                    prepare['ouvrage'] = model_to_dict(ouvrage)
                    prepare['entreprise'] = model_to_dict(entreprise)

                    if document.validateur:
                        prepare['validateur'] = model_to_dict(document.validateur)

                    data.append(prepare)

        if id_doc is not None:
            filtered_data = [doc for doc in data if doc['id'] == id_doc]
            if len(filtered_data) == 0:
                return Response({'error': 'Document not found'}, status=404)
            return Response(filtered_data[0])
        
        return Response(data)


class CheckAvisOnDocumentByCollaborateur(APIView):
    def get(self, request, id_document, id_collaborateur):
        all_avis = Avis.objects.all()
        find = None
        for avis in all_avis:
            document = avis.id_document
            collab = avis.collaborateurs
            if document.id == id_document and collab.id == id_collaborateur:
                find = avis
                break

        if find == None:
            return Response({'avis' : False})
        else:
            return Response({'avis' : model_to_dict(find)})


class RecupereLensembleDesAvisSurDocument(APIView):
    def get(self, request, id_document):
        aviss = Avis.objects.all()
        TabCodifications = []
        for avis in aviss:
            document = avis.id_document
            if id_document == document.id:
                TabCodifications.append(avis.codification)
        if len(TabCodifications) == 0:
            return Response({'codification': False})
        liste = ['RMQ', 'F', 'HM', 'VI']
        unique_liste = list(set(TabCodifications))
        codification = unique_liste[0]

        for tu in unique_liste:
            if liste.index(tu) < liste.index(codification):
                codification = tu

        return Response({'codification': codification})


class GetAffaireOuvrageFromDocument(APIView):
    def get(self, request, id_doc):
        try:
            doc = Documents.objects.get(id=id_doc)
            entreprise_affaire_ouvrage = doc.emetteur

            affaire_ouvrage = entreprise_affaire_ouvrage.affaire_ouvrage
            result = model_to_dict(affaire_ouvrage)
            return Response(result)
        except:
            return Response({'not found' : True})

class GetAllDetailAsoForAffaire(APIView):
    def get(self, request, id_affaire):
        all_aso = Aso.objects.all()

        data = []

        for aso in all_aso:
            affaire = aso.affaireouvrage.id_affaire
            if affaire.id == id_affaire:
                prepare = model_to_dict(aso)
                prepare['ouvrage'] = model_to_dict(aso.affaireouvrage.id_ouvrage)
                data.append(prepare)
        
        return Response(data)
    
class GetAllDetailAsoForAffaireOneVersion(APIView):
    def get(self, request, id_aso):
        try:
            aso = Aso.objects.get(id=id_aso)
            data = model_to_dict(aso)
            data['ouvrage'] = model_to_dict(aso.affaireouvrage.id_ouvrage)
            return Response(data)
        except:
            return Response({'not found' : True})

class GetAllDetailDocumentForAffaireOuvrage(APIView):
    def get(self, request, id_affaire_ouvrage):
        all_doc = Documents.objects.all()

        data = []
        for doc in all_doc:
            affaire_ouvrage = doc.emetteur.affaire_ouvrage
            if affaire_ouvrage.id == id_affaire_ouvrage and doc.validateur != None:
                prepare = model_to_dict(doc)
                prepare['ouvrage'] = model_to_dict(doc.emetteur.affaire_ouvrage.id_ouvrage)
                prepare['entreprise'] = model_to_dict(doc.emetteur.affaire_entreprise.entreprise)
                data.append(prepare)
        return Response(data)
    
class GenerateDataForAso(APIView):
    def get(self, request, id_aso):
        # try:
            aso = Aso.objects.get(id=id_aso)

            data = {}

            # Donne de l'aso

            data['aso'] = model_to_dict(aso)

            # Donne de l'affaire

            data['affaire'] = model_to_dict(aso.affaireouvrage.id_affaire)

            # Donne ouvrage et entreprise en diffusion

            data['ouvrage'] = model_to_dict(aso.affaireouvrage.id_ouvrage)
            data['collaborateurs'] = []

            entreprise_affaire = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=aso.affaireouvrage.id, diffusion=True)
            for ea in entreprise_affaire:
                data['collaborateurs'].append(model_to_dict(ea.affaire_entreprise.entreprise))
            # Donne du charge d'affaire

            charge = aso.affaireouvrage.id_affaire.charge

            data['charge'] = model_to_dict(charge)
            if charge.address:
                data['charge']['adresse'] = model_to_dict(charge.address)

            # Donne de l'entreprise cliente

            entreprise = aso.affaireouvrage.id_affaire.client

            data['client'] = model_to_dict(entreprise)
            data['client']['adresse'] = model_to_dict(entreprise.adresse)

            # All mission

            data['mission'] = []
            id_affaire = aso.affaireouvrage.id_affaire.id

            all_mission = MissionActive.objects.filter(id_affaire=id_affaire)

            for mission in all_mission:
                data['mission'].append(model_to_dict(mission.id_mission))

            # Data about document

            data['documents'] = []
            
            all_entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=aso.affaireouvrage)
            all_document = Documents.objects.filter(aso=id_aso)
            all_commentaire = Commentaire.objects.all()
            aviss = Avis.objects.all()
            liste = ['RMQ', 'F', 'HM', 'VI']


            for document in all_document:
                for e_a_o in all_entreprise_affaire_ouvrage:
                    if document.emetteur != None and document.emetteur.id == e_a_o.id:
                        prepare = {}
                        prepare['document'] = model_to_dict(document)
                        prepare['avis'] = []
                        for commentaire in all_commentaire:
                            if commentaire.id_avis.id_document.id == document.id:
                                prepare['avis'].append(model_to_dict(commentaire))

                        TabCodifications = []
                        for avis in aviss:
                            document_o = avis.id_document
                            if document.id == document_o.id:
                                TabCodifications.append(avis.codification)
                        if len(TabCodifications) != 0:
                            unique_liste = list(set(TabCodifications))
                            codification = unique_liste[0]

                            for tu in unique_liste:
                                if liste.index(tu) < liste.index(codification):
                                    codification = tu
                            prepare['codification'] = codification
                        
                        data['documents'].append(prepare)

            aviss = Avis.objects.all()
            TabCodifications = []
            for avis in aviss:
                document = avis.id_document
                if document.aso and (document.aso.id == id_aso):
                    TabCodifications.append(avis.codification)

            liste = ['RMQ', 'F', 'HM', 'VI']
            unique_liste = list(set(TabCodifications))

            codification = ''

            if len(unique_liste) != 0:
                codification = unique_liste[0]

            for tu in unique_liste:
                if liste.index(tu) < liste.index(codification):
                    codification = tu

            data['codification'] = codification
        
            return Response(data)
        
        # except:
        #     return Response({})


class CheckAsoCurrentForAffaireOuvrage(APIView):
    def get(self, request, id_affaire_ouvrage):
        try:
            affaire_ouvrage = AffaireOuvrage.objects.get(id=id_affaire_ouvrage)
            aso_exists = Aso.objects.get(affaireouvrage=affaire_ouvrage, statut=0)

            if aso_exists:
                return Response(model_to_dict(aso_exists))
        except:
            return Response(False)

class AllEntrepriseConcerneByAso(APIView):
    def get(self, request, id_aso):
        aso = Aso.objects.get(id=id_aso)

        affaire_ouvrage = aso.affaireouvrage

        entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=affaire_ouvrage.id)

        data = []

        for eao in entreprise_affaire_ouvrage:
            result = model_to_dict(eao)
            result['detail_entreprise'] = model_to_dict(eao.affaire_entreprise.entreprise)
            result['responsables'] = []
            responsables = Responsable.objects.filter(entreprise=eao.affaire_entreprise.entreprise.id)
            for responsable in responsables:
                result['responsables'].append(model_to_dict(responsable))
            data.append(result)

        return Response(data)
    

class AffaireOuvrageConcerneByAso(APIView):
    def get(self, request, id_aso):
        aso = Aso.objects.get(id=id_aso)

        return Response(model_to_dict(aso.affaireouvrage))
    
class GetCollaborateurAffectOnDocument(APIView):
    def get(self, request, id_document):
        affectations = DocumentAffectation.objects.filter(document=id_document)
        data = []

        for affectation in affectations:
            data.append(affectation.collaborateur.id)

        return Response(data)

class RemoveCollaborateurOnDocument(APIView):
    def get(self, request, id_collab, id_doc):
        try:
            DocumentAffectation.objects.get(document=id_doc, collaborateur=id_collab).delete()
            return Response({'remove' : True})
        except:
            return Response({'remove' : False})
        
class NextNumberAsoForAffaire(APIView):
    def get(self, request, id_affaire):
        asos = Aso.objects.filter(affaireouvrage__id_affaire_id=id_affaire)
        return Response({'position' : len(asos) + 1})
    
class DocumentCreate(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                affaire  = request.data['affaire']
                del request.data['affaire']
                number = len(Documents.objects.filter(emetteur__affaire_ouvrage__id_affaire_id=affaire))
                doc = Documents(**request.data, createur=request.user, order=number+1)
                doc.save()
                doc_affec = DocumentAffectation(document=doc, collaborateur=request.user)
                doc_affec.save()
        except Exception as ex:
            print(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        return Response(status=status.HTTP_201_CREATED)

class AddAffaireOuvrage(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                for ouvrage in request.data['ouvrages']:
                    AffaireOuvrage(id_affaire_id=request.data['affaire'], id_ouvrage_id=ouvrage).save()
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_201_CREATED)

class DefineDiffusionForOuvrage(APIView):
    def put(self, request):
        try:
            with transaction.atomic():
                id_affaire_ouvrage = request.data['affaire_ouvrage']
                entreprise_affaire_ouvrages = request.data['eao']
                diffusion = request.data['diffusion']
                AffaireOuvrage.objects.filter(id=id_affaire_ouvrage).update(diffusion=diffusion)
                
                for eao in entreprise_affaire_ouvrages:
                    EntrepriseAffaireOuvrage.objects.filter(id=eao).update(diffusion=diffusion)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)

class AddAvisOnDoc(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                document = request.data['document']
                codification = request.data['codification']
                comments = request.data['comments']
                oldComments = request.data['oldComments']
                prevAvis = request.data['prevAvis']
                
                if prevAvis:
                    Avis.objects.filter(id=prevAvis).delete()
                
                avis = Avis(id_document_id=document, codification=codification, collaborateurs=request.user)
                avis.save()
                
                for comment in comments:
                    Commentaire(id_avis=avis, commentaire=comment['commentaire'], a_suivre=comment['a_suivre']).save()

                for oldComment in oldComments:
                    Commentaire(id_avis=avis, commentaire=oldComment['commentaire'], a_suivre=oldComment['a_suivre']).save()                    
            
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_201_CREATED)
    
class AttachDocOnAso(APIView):
    def put(self, request):
        try:
            with transaction.atomic():
                document = request.data['document']
                
                doc = Documents.objects.get(id=document)
                affaire_ouvrage = doc.emetteur.affaire_ouvrage
                
                result_aso = Aso.objects.filter(affaireouvrage=affaire_ouvrage, statut=0)
                
                if result_aso.exists():
                    if len(result_aso) > 1:
                        raise Exception("Plusieurs aso sont en cours pour l'ouvrage")
                    else:
                        aso = result_aso[0]
                        doc.aso = aso
                        doc.validateur = request.user
                        doc.save()
                else:
                    next_aso  = len(Aso.objects.filter(affaireouvrage__id_affaire_id=affaire_ouvrage.id_affaire.id))
                    aso = Aso(date=date.today(), redacteur=request.user, affaireouvrage=affaire_ouvrage, order_in_affaire=next_aso+1)
                    aso.save()
                    doc.aso = aso
                    doc.validateur = request.user
                    doc.save()
         
        except Exception as e:
            print(Exception)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_201_CREATED)
    
class AddEntrepriseOnOuvrage(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                entreprises = request.data['entreprises']
                ouvrage_affaire = request.data['ouvrage_affaire']
                
                for entreprise in entreprises:
                    if not EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=ouvrage_affaire, affaire_entreprise=entreprise).exists():
                        EntrepriseAffaireOuvrage(affaire_ouvrage_id=ouvrage_affaire, affaire_entreprise_id=entreprise).save()
         
        except Exception as e:
            print(Exception)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_201_CREATED)
    
class SetRemarqueOnAso(APIView):
    def post(self, request, id_aso):
        try:
            with transaction.atomic():
                RemarqueAso(aso_id=id_aso, redacteur=request.user, content=request.data['remarque']).save()
        except Exception as e:
            print(Exception)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_201_CREATED)
    
class GetAllRemarqueGeneralOnAso(APIView):
    def get(self, request, id_aso):
        remarques = RemarqueAso.objects.filter(aso=id_aso)
        
        data = []
        
        for remarque in remarques:
            prepare = model_to_dict(remarque)
            prepare['redacteur'] = model_to_dict(remarque.redacteur)
            data.append(prepare)
            
        return Response(data)

    
class GetUserRemarqueGeneralOnAso(APIView):
    def get(self, request, id_aso):
        remarques = RemarqueAso.objects.filter(aso=id_aso, redacteur=request.user.id)
        
        data = []
        
        for remarque in remarques:
            prepare = model_to_dict(remarque)
            prepare['redacteur'] = model_to_dict(remarque.redacteur)
            data.append(prepare)
            
        return Response(data)

class EditRemarque(APIView):
    def put(self, request):
        try:
            with transaction.atomic():
                remarques = request.data['remarques']
                for remarque in remarques:
                    RemarqueAso.objects.filter(id=remarque['id']).update(content=remarque['content'])
        except Exception as e:
            print(Exception)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)
    
class CreateOuvrageForAffaire(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                libelle = request.data['libelle']
                affaire = request.data['affaire']
                ouvrage = Ouvrage(libelle=libelle, affaire_id=affaire)
                ouvrage.save()
                AffaireOuvrage(id_affaire_id=affaire, id_ouvrage_id=ouvrage.id).save()
        except Exception as e:
            print(Exception)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)
    
class AllOuvrageAvailableForAffaire(APIView):
    def get(self, request, id_affaire):
        results = Ouvrage.objects.filter(Q(affaire=None) | Q(affaire_id=id_affaire))
        data = []
        for result in results:
            data.append(model_to_dict(result))
        return Response(data)

class GetOuvrageAffaireDetailEntreprise(APIView):
    def get(self, request, id_affaire):
        all_affaire_ouvrage = AffaireOuvrage.objects.filter(id_affaire=id_affaire)
        data = []
        for ouvrage in all_affaire_ouvrage:
            final_data = model_to_dict(ouvrage)  # Convertir l'objet QueryDict en dictionnaire
            detail_ouvrage = Ouvrage.objects.get(id=ouvrage.id_ouvrage.id)
            ouvrage_data = model_to_dict(detail_ouvrage)
            final_data['ouvrage'] = ouvrage_data
            
            entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(
            affaire_ouvrage=ouvrage.id).values()
            data_entreprise = []
            for e_a_o in entreprise_affaire_ouvrage:
                final = dict(e_a_o)
                detailEntrepriseAffaire = EntrepriseAffaire.objects.get(id=e_a_o['affaire_entreprise_id'])
                detailEntreprise = model_to_dict(detailEntrepriseAffaire.entreprise)
                final['entreprise'] = detailEntreprise
                data_entreprise.append(final)
                
            final_data['entreprises'] = data_entreprise
            data.append(final_data)
        return Response(data)

"""

class EntreprisesByOuvrageViewAddOnline(APIView):
    def get(self, request, ouvrage_id):
        try:
            # Récupérer toutes les entreprises associées à l'ouvrage donné
            entreprises = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage_id=ouvrage_id).select_related('affaire_entreprise')
            serializer = EntrepriseSerializer([entreprise.affaire_entreprise for entreprise in entreprises], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ouvrage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
"""

"""class EntreprisesByOuvrageViewAddOnline(APIView):
    def get(self, request, ouvrage_id):
        from entreprise.serializers import EntrepriseSerializer

        try:
            # Vérifie si l'ouvrage existe
            ouvrage = Ouvrage.objects.get(id=ouvrage_id)

            # Récupérer toutes les entreprises associées à l'ouvrage donné
            entreprises_affaire = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage_id=ouvrage_id).select_related('affaire_entreprise__entreprise')
            
            # Récupérer les instances d'Entreprise
            entreprises = [entreprise.affaire_entreprise.entreprise for entreprise in entreprises_affaire]
            
            # Sérialise les entreprises
            serializer = EntrepriseSerializer(entreprises, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ouvrage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)"""

"""from .serializers import EntrepriseAffaireOuvrageSerializerAddline
class EntreprisesByOuvrageViewAddOnline(generics.ListAPIView):
    serializer_class = EntrepriseAffaireOuvrageSerializerAddline

    def get_queryset(self):
        ouvrage_id = self.kwargs['ouvrage_id']  # Récupère l'ID de l'ouvrage à partir de l'URL
        return EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage__id_ouvrage=ouvrage_id)"""



from entreprise.serializers import EntrepriseSerializer
"""
class EntreprisesByOuvrageViewAddOnline(APIView):
    def get(self, request, ouvrage_id):
        try:
            entreprises = Entreprise.objects.filter(
                entrepriseaffaire__entrepreiseaffaireouvrage__affaire_ouvrage__id_ouvrage=ouvrage_id
            ).distinct()
            
            serializer = EntrepriseSerializer(entreprises, many=True)
            return Response(serializer.data)
        except Ouvrage.DoesNotExist:
            return Response({"error": "Ouvrage non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
"""






from Dashbord.serializers import EntrepriseAffairesNewsSerializerSecond
class EntreprisesByOuvrageViewAddOnline(APIView):
    """
    Récupérer toutes les entreprises liées à un ouvrage spécifique.
    """
    def get(self, request, ouvrage_id):
        try:
            affaire_ouvrage = AffaireOuvrage.objects.get(id=ouvrage_id)
        except AffaireOuvrage.DoesNotExist:
            return Response({"error": "L'ouvrage spécifié n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        entreprises_affaires_ouvrages = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=affaire_ouvrage)
        entreprises = [eao.affaire_entreprise for eao in entreprises_affaires_ouvrages]
        serializer = EntrepriseAffairesNewsSerializerSecond(entreprises, many=True)
        return Response(serializer.data)




from .serializers import RemarqueAsoSerializers
from .models import RemarqueAso
from .models import Affaire
from .models import Aso


class AffaireRemarquesView(APIView):
    def get(self, request, affaire_id):
        try:
            affaire = Affaire.objects.get(id=affaire_id)
        except Affaire.DoesNotExist:
            return Response({"error": "Affaire not found"}, status=status.HTTP_404_NOT_FOUND)

        remarques = RemarqueAso.objects.filter(aso__affaireouvrage__id_affaire=affaire)
        serializer = RemarqueAsoSerializers(remarques, many=True)
        return Response(serializer.data)