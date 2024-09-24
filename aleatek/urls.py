from django.contrib import admin
from django.urls import path, include
from ouvrage.views import AffaireOuvrageAdminViewset
from Dashbord.serializers import BatimentSerializer
from .views import get_csrf_token
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser.views import UserViewSet
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from Dashbord.views import AffaireListView, TutorialIDList, TutoratViewSet, PlanAffaireByAffaireIdView, \
    BatiementPlanAffaireViewset, ActiveAffaireView
from django.conf import settings
from django.conf.urls.static import static
from ouvrage.views import EntrepriseAffaireOuvrageViewsetAdministration
from mission.views import AddInterventionTechnique, AddMissionActive, DeleteArticleSelectForAffaire, \
    AddArticleSelectForAffaire, GetAllCritereForAffaire, ArticleSelectViewsetAdmin, GetAllArticleForMission, \
    GetAllMissionViewByChapitre, MissionAdminViewsetAdmin, ITAdminViewsetAdmin, \
    ArticleAdminViewsetAdmin, GetAllParentMission, \
    MissionActiveForCurrentAffaire, VerifyExistITForMissionSignAndCollab, VerifyExistMissionActive, \
    AllIntervenantForAffaire, AllMissionForAffaire, ArticleMissionViewsetAdmin, MissionActiveView, \
    MissionActiveCreateAPIView, AddSousMissionView, \
    AffaireDetailView

from collaborateurs.views import UtilisateurConnecteView, CollaborateursAdminViewsetAdmin, AllCollabAssignToMission
from entreprise.views import AddEntrepriseOnAffaire, CreateEntreprise, EditeDataEntreprise, \
    ResponsableAdminViewsetAdmin, EntrepriseAdminViewsetAdmin, GetEntrepriseWithCollaborateur
from Dashbord.views import AffaireAdminViewsetAdmin, PlanAffaireAdminViewsetAdmin, ProduitAdminViewsetAdmin, \
    EditPlanAffaire, \
    BatimentAdminViewsetAdmin, ChantierAdminViewsetAdmin, GetPlanAffaireDetail, EntrepriseAffaireViewsetAdmin, \
    GetAllEntrepriseForAffaire, GetAllEntrepriseDetailForAffaire, FindChargeAffaireForAffaire, \
    GetPlanAffaireDetailForPlanAffaire, DeleteEntrepriseAffaire, CreateAffaireAndPlanAffaire, GetAllPlansAffaire
from adresse.views import AdressdminViewsetAdmin
from ouvrage.views import DefineDiffusionForOuvrage, AddAffaireOuvrage, AsoViewsetAdmin, \
    AffaireOuvrageAdminViewsetAdmin, OuvrageAdminViewsetAdmin, CodificationASO, \
    EntrepriseAffaireOuvrageViewset, GetAllAffaireOuvrageByAffaire, VerifyEntrepriseCollabOnOuvrage, \
    CodificationASOInCurrent, \
    AllEntreprisebAssignToAffaireOuvrage, GetAllDetailAsoForAffaireOneVersion, AffaireOuvrageConcerneByAso, AddAvisOnDoc

from ouvrage.views import AddEntrepriseOnOuvrage, AttachDocOnAso, DocumentSerializerAdminViewsetAdmin, \
    AvisSerializerAdminViewsetAdmin, GetAllDetailDocumentForAffaireOuvrage, AllEntrepriseConcerneByAso, \
    FichierSerializerAdminViewsetAdmin, VerifyExistAffaireOuvrage, CheckAvisOnDocumentByCollaborateur, \
    GenerateDataForAso, CheckAsoCurrentForAffaireOuvrage

from commentaire.views import CommentaireAdminViewsetAdmin, GetAllCommentForAvis

from rapport_visite.views import AddAvisOnRv, CreateRv, AllAvisFromRV, RapportVisiteSerializerAdminViewsetAdmin, \
    AvisOuvrageViewsetAdmin, CommentaireAvisOuvrageViewsetAdmin, \
    GetAllRapportVisiteByAffaire, GetAllRapportVisiteOneVersions, AllEntrepriseConcerneByRV, GenerateDataForRV, \
    NextNumberRVForAffaire, EditAvisOuvrage

from ouvrage.views import EditRemarque, GetUserRemarqueGeneralOnAso, GetAllRemarqueGeneralOnAso, DocumentCreate, \
    NextNumberAsoForAffaire, RecupereLensembleDesAvisSurDocument, GetAllDetailDocument, GetAllDetailDocumentWithIdDoc, \
    GetAffaireOuvrageFromDocument, GetAllDetailAsoForAffaire, CreateOuvrageForAffaire

from RICT.views import ReviserRICT, GenerateDataForRICT, SaveDecriptionSommaire, ValidateRICT, \
    GetAllAvisByRICTandMission, GetAllDispositionByRICTandMission, CheckRICTForAffaire, RICTViewsetAdmin, \
    AvisArticleViewsetAdmin, DescriptionSommaireViewsetAdmin, \
    DispositionViewsetAdmin, CommentaireAvisArticleViewsetAdmin, GetDesriptionSommaireByRICT, SaveArticleDisposition, \
    GetDisposionAvisAndComment, MissionRICTViewsetAdmin, ValidateDevalidateMissionRict
from Dashbord.views import ActiveAffaireViewMission
from ouvrage.views import GetOuvrageAffaireDetailEntreprise, AllOuvrageAvailableForAffaire, \
    DocumentAffectationViewsetAdmin, GetCollaborateurAffectOnDocument, RemoveCollaborateurOnDocument, \
    RemarqueAsoViewsetAdmin, SetRemarqueOnAso

from synthese.views import SyntheseAvisViewsetAdmin, CreateSyntheseAvis, AllSyntheseAvis, \
    SyntheseComentaireRVViewsetAdmin, SyntheseCommentaireArticleViewsetAdmin, SyntheseCommentaireDocumentViewsetAdmin, \
    GetAllCommentaireOnAffaire, LeverCommentaire, AnnulerLever, AllAvisOfAffaire, ValidateSyntheseAvis, \
    AllAvisOfSynthese, DevalidateSyntheseAvis

from mission.views import GetCritereAboutDescriptionBati, HandleSelectCritere, GetCritereAboutCodeTravail, ToggleMissionActiveView, AffaireMissionsView

# from ouvrage.views import CodificationplusBas

router = routers.SimpleRouter()

router.register('synthese_commentaire_document', SyntheseCommentaireDocumentViewsetAdmin,
                basename='synthese_commentaire_document')
router.register('synthese_commentaire_rv', SyntheseComentaireRVViewsetAdmin, basename='synthese_commentaire_rv')
router.register('synthese_commentaire_article', SyntheseCommentaireArticleViewsetAdmin,
                basename='synthese_commentaire_article')

router.register('synthese_avis', SyntheseAvisViewsetAdmin, basename='synthese avis')

router.register('document_affectation', DocumentAffectationViewsetAdmin, basename='document_affectation')
router.register('remarque_aso', RemarqueAsoViewsetAdmin, basename='remarque_aso')

router.register('rict', RICTViewsetAdmin, basename='rict')
router.register('mission_rict', MissionRICTViewsetAdmin, basename='mission_rict')
router.register('disposition', DispositionViewsetAdmin, basename='disposition')
router.register('avis_article', AvisArticleViewsetAdmin, basename='avis_article')
router.register('commentaire_avis_article', CommentaireAvisArticleViewsetAdmin, basename='commentaire_avis_article')
router.register('description_sommaire', DescriptionSommaireViewsetAdmin, basename='description_sommaire'),

router.register('avis_ouvrage', AvisOuvrageViewsetAdmin, basename='admin-avis_ouvrage')
router.register('article', ArticleAdminViewsetAdmin, basename='admin-article')
router.register('article_select', ArticleSelectViewsetAdmin, basename='admin-article-select')
router.register('avis_commentaire', CommentaireAvisOuvrageViewsetAdmin)
router.register('rapport/visite', RapportVisiteSerializerAdminViewsetAdmin, basename='admin-rapport')
router.register('commentaire', CommentaireAdminViewsetAdmin, basename='admin=commentaire')
router.register('fichierattacher', FichierSerializerAdminViewsetAdmin, basename='admin=avis')
router.register('avis', AvisSerializerAdminViewsetAdmin, basename='admin=avis')
router.register('documents', DocumentSerializerAdminViewsetAdmin, basename='admin=document')
router.register('ouvrage', OuvrageAdminViewsetAdmin, basename='admin=ouvrage')
router.register('affaireouvrage', AffaireOuvrageAdminViewsetAdmin, basename='admin=aafffaireouvrage')
router.register('aso', AsoViewsetAdmin, basename='admin=aso')
router.register('mission', MissionAdminViewsetAdmin, basename='admin-mission')
#router.register('missions/active', MissionActiveAdminViewsetAdmin, basename='admin-mission-active')
router.register('article_mission', ArticleMissionViewsetAdmin, basename='admin-article-mission')
router.register('intervention/technique', ITAdminViewsetAdmin, basename='admin-it')

router.register('admin/adresse', AdressdminViewsetAdmin, basename='admin-adresse')

router.register('batiment', BatimentAdminViewsetAdmin, basename='admin-batiment')
router.register('entreprise_affaire', EntrepriseAffaireViewsetAdmin, basename='admin-entrepriseaffaire')
router.register('entreprise_affaire_ouvrage', EntrepriseAffaireOuvrageViewset,
                basename='admin-entrepriseaffaireouvrage')
router.register('chantier', ChantierAdminViewsetAdmin, basename='admin-chantier')
router.register('affaire', AffaireAdminViewsetAdmin, basename='admin-affaoire')
router.register('planaffaire', PlanAffaireAdminViewsetAdmin, basename='admin-paffaire')
router.register('produit', ProduitAdminViewsetAdmin, basename='admin-collab')
router.register('responsable', ResponsableAdminViewsetAdmin, basename='admin-collab')
router.register('entreprise', EntrepriseAdminViewsetAdmin, basename='admin-entreprise')
router.register('collaborateurs', CollaborateursAdminViewsetAdmin, basename='admin-collab')
router.register('tutorats', TutoratViewSet, basename='admin-tutorat')
router.register('users', UserViewSet, basename='users')
#router.register('active', MissionActiveView, basename='mission_active')
from mission.views import MissionViewSet, MissionActiveViewSet, SousMissionsActivationView
from mission.views import MissionAddParentesSousMissionAffaireViewSet, SousMissionToggleChildMissionView

router.register('batiement_planaffaire', BatiementPlanAffaireViewset, basename='admin-plan-affaire-batiement')
router.register('news_missions', MissionViewSet, basename="missions_actives_news")
router.register('news_missions-active', MissionActiveViewSet, basename='mission_actives_active')
#router.register('mission-state-management', SousMissionActiveViewSet, basename='mission_state_management')
router.register('missions-parents-sous-mission', MissionAddParentesSousMissionAffaireViewSet, basename='missions-parents-sous-mission') 
router.register('toggle-child-mission', SousMissionToggleChildMissionView, basename='toggle-child-mission')




schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
from mission.views import get_active_missions_for_affaire

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #    path('codification/plusbas/', CodificationplusBas.as_view(), name='codification_plus_bas'),

    # sythese avis service

    path('api/create_synthese_avis/<int:id_affaire>/', CreateSyntheseAvis.as_view()),
    path('api/all_synthese_avis/<int:id_affaire>/', AllSyntheseAvis.as_view()),
    path('api/all_avis_of_affaire/<int:id_affaire>/', AllAvisOfAffaire.as_view()),
    path('api/all_avis_of_synthese/<int:id_synthese>/', AllAvisOfSynthese.as_view()),
    path('api/validate_synthese_avis/<int:id_synthese>/<int:id_affaire>/', ValidateSyntheseAvis.as_view()),
    path('api/devalidate_synthese_avis/<int:id_synthese>/', DevalidateSyntheseAvis.as_view()),

    # entreprise service
    path('api/all_entreprise_concerne_by_aso/<int:id_aso>/', AllEntrepriseConcerneByAso.as_view()),
    path('api/all_entreprise_concerne_by_rv/<int:id_rv>/', AllEntrepriseConcerneByRV.as_view()),
    path('api/entreprise_and_responsable/', GetEntrepriseWithCollaborateur.as_view()),
    path('api/entreprise_and_responsable/<int:id_entreprise>/', GetEntrepriseWithCollaborateur.as_view()),
    path('api/verify_entreprise_collab_on_ouvrage/<int:id_entreprise_affaire>/<int:id_ouvrage_affaire>/',
         VerifyEntrepriseCollabOnOuvrage.as_view()),
    path('api/entreprise_for_affaire_ouvrage/<int:id_affaire_ouvrage>/',
         AllEntreprisebAssignToAffaireOuvrage.as_view()),
    path('api/entreprise_collab_affaire/<int:id_affaire>/', GetAllEntrepriseForAffaire.as_view()),
    path('api/entreprise_collab_affaire_detail/<int:id_affaire>/', GetAllEntrepriseDetailForAffaire.as_view()),
    path('api/delete/entreprise_affaire/<int:id_affaire>/<int:id_entreprise>/', DeleteEntrepriseAffaire.as_view()),
    path('api/add_entreprise_on_ouvrage/', AddEntrepriseOnOuvrage.as_view()),
    path('api/edite_data_entreprise/', EditeDataEntreprise.as_view()),
    path('api/create_entreprise/', CreateEntreprise.as_view()),
    path('api/add_entreprise_on_affaire/', AddEntrepriseOnAffaire.as_view()),

    # affaire ouvrage service
    path('api/affaire_ouvrage_concerne_by_aso/<int:id_aso>/', AffaireOuvrageConcerneByAso.as_view()),
    path('api/get_affaire_ouvrage_from_document/<int:id_doc>/', GetAffaireOuvrageFromDocument.as_view()),
    path('api/get_ouvrage_affaire/<int:id_affaire>/', GetAllAffaireOuvrageByAffaire.as_view()),
    path('api/ouvrage_affaire/<int:id_affaire>/<int:id_ouvrage>/', VerifyExistAffaireOuvrage.as_view()),
    path('api/add_affaire_ouvrage/', AddAffaireOuvrage.as_view()),
    path('api/define_diffusion_for_ouvrage/', DefineDiffusionForOuvrage.as_view()),
    path('api/create_ouvrage_for_affaire/', CreateOuvrageForAffaire.as_view()),
    path('api/all_ouvrage_available_for_affaire/<int:id_affaire>/', AllOuvrageAvailableForAffaire.as_view()),
    path('api/get_ouvrage_affaire_detail_entreprise/<int:id_affaire>/', GetOuvrageAffaireDetailEntreprise.as_view()),

    # aso service
    path('api/get_all_detail_aso_for_affaire_one_version/<int:id_aso>/', GetAllDetailAsoForAffaireOneVersion.as_view()),
    path('api/get_all_detail_aso_for_affaire/<int:id_affaire>/', GetAllDetailAsoForAffaire.as_view()),
    path('api/check_aso_current_for_affaire_ouvrage/<int:id_affaire_ouvrage>/',
         CheckAsoCurrentForAffaireOuvrage.as_view()),
    path('api/next_number_aso_for_affaire/<int:id_affaire>/', NextNumberAsoForAffaire.as_view()),

    # RV service
    path('api/get_all_rapport_visite_by_affaire/<int:affaire>/', GetAllRapportVisiteByAffaire.as_view()),
    path('api/get_all_rapport_visite_by_affaire_one_version/<int:rv>/', GetAllRapportVisiteOneVersions.as_view()),
    path('api/next_number_rv_for_affaire/<int:id_affaire>/', NextNumberRVForAffaire.as_view()),
    path('api/create_rv/', CreateRv.as_view()),
    path('api/add_avis_on_rv/<int:id_rv>', AddAvisOnRv.as_view()),
    path('api/edit_avis_ouvrage/', EditAvisOuvrage.as_view()),

    # Codification service
    path('api/codification_aso/<int:id_aso>/', CodificationASO.as_view()),
    path('api/codification_aso_in_current/<int:id_aso>/', CodificationASOInCurrent.as_view()),
    path('api/documents/avis/<int:id_document>/', RecupereLensembleDesAvisSurDocument.as_view(),
         name='recuperer_avis_document'),

    # Affaire and plan affaire service
    path('affaire/api/detail_plan_affaire/', GetPlanAffaireDetail.as_view()),
    path('affaire/api/detail_plan_affaire_for_plan_affaire/<int:id_plan_affaire>/',
         GetPlanAffaireDetailForPlanAffaire.as_view()),
    path('affaire/api/create_affaire_and_plan_affaire/', CreateAffaireAndPlanAffaire.as_view()),
    path('affaire/api/edit_plan_affaire/<int:id_plan>/', EditPlanAffaire.as_view()),
    path('affaire/<int:affaire_id>/plans/', PlanAffaireByAffaireIdView.as_view(), name='plans-by-affaire-id'),

    # Mission service
    path('mission_sign/<int:id_affaire>/', MissionActiveForCurrentAffaire.as_view()),
    path('mission_collab/<int:id_collab>/<int:id_mission_sign>/',
         VerifyExistITForMissionSignAndCollab.as_view()),
    path('mission_affaire/<int:id_affaire>/<int:id_mission>/', VerifyExistMissionActive.as_view()),
    path('api/mission_all/<int:id_affaire>/', AllMissionForAffaire.as_view()),
    path('mission_get_all_parent_/', GetAllParentMission.as_view()),
    path('mission_get_all_view_by_chapitre/<int:id_affaire>/<int:id_rict>/', GetAllMissionViewByChapitre.as_view()),
    path('mission_add_mission_active/', AddMissionActive.as_view()),

    # Collaborateur service
    path('api/find_charge_affaire_for_affaire/<int:id_affaire>/', FindChargeAffaireForAffaire.as_view()),
    path('api/collab_for_mission_sign/<int:id_mission_sign>/', AllCollabAssignToMission.as_view()),
    path('api/all_intervenant/<int:id_affaire>/', AllIntervenantForAffaire.as_view()),
    path('api/get_collaborateur_affect_on_document/<int:id_document>/', GetCollaborateurAffectOnDocument.as_view()),

    # Document service
    path('api/get_all_detail_document/<int:id_affaire>/', GetAllDetailDocument.as_view()),
    path('api/get_all_detail_document/<int:id_affaire>/<int:id_doc>/', GetAllDetailDocumentWithIdDoc.as_view()),
    path('api/get_all_detail_document_for_affaire_ouvrage/<int:id_affaire_ouvrage>/',
         GetAllDetailDocumentForAffaireOuvrage.as_view()),
    path('api/remove_collaborateur_on_document/<int:id_collab>/<int:id_doc>/', RemoveCollaborateurOnDocument.as_view()),
    path('api/document_create/', DocumentCreate.as_view()),
    path('api/attach_doc_on_aso/', AttachDocOnAso.as_view()),

    # Avis service
    path('api/check_avis_on_document_by_collaborateur/<int:id_document>/<int:id_collaborateur>/',
         CheckAvisOnDocumentByCollaborateur.as_view()),
    path('api/get_all_comment_for_avis/<int:id_avis>/', GetAllCommentForAvis.as_view()),
    path('api/add_avis_on_doc/', AddAvisOnDoc.as_view()),

    # Article Service
    path('api/get_all_article_for_mission/<int:id_mission>/<int:id_affaire>/', GetAllArticleForMission.as_view()),
    path('api/get_all_critere_for_affaire/<int:id_affaire>/', GetAllCritereForAffaire.as_view()),
    path('api/add_article_select_for_affaire/<int:id_affaire>/<int:id_article>/', AddArticleSelectForAffaire.as_view()),
    path('api/delete_article_select_for_affaire/<int:id_affaire>/<int:id_article>/',
         DeleteArticleSelectForAffaire.as_view()),
    path('api/all_avis_from_RV/<int:id_rv>/', AllAvisFromRV.as_view()),

    path('api/handle_select_critere/<int:id_affaire>/<int:article>/', HandleSelectCritere.as_view()),
    path('api/get_critere_about_description_bati/<int:id_affaire>/', GetCritereAboutDescriptionBati.as_view()),
    path('api/get_critere_about_code_travail/<int:id_affaire>/', GetCritereAboutCodeTravail.as_view()),

    # RICT Service
    path('api/check_RICT_for_affaire/<int:id_affaire>/', CheckRICTForAffaire.as_view()),
    path('api/get_disposion_avis_and_comment/<int:rict>/<int:article>/<int:mission>/',
         GetDisposionAvisAndComment.as_view()),
    path('api/validate_devalidate_mission_rict/<int:id_mission>/<int:id_rict>/',
         ValidateDevalidateMissionRict.as_view()),
    path('api/valider_rict/<int:id_rict>/', ValidateRICT.as_view()),
    path('api/reviser_rict/<int:id_rict>/', ReviserRICT.as_view()),

    # Livrable service
    path('api/data_for_aso/<int:id_aso>/', GenerateDataForAso.as_view()),
    path('api/data_for_rv/<int:id_rv>/', GenerateDataForRV.as_view()),
    path('api/data_for_rict/<int:id_rict>/<int:plan_affaire>/', GenerateDataForRICT.as_view()),

    # Disposition service
    path('api/get_all_disposition_by_RICT_and_mission/<int:id_rict>/<int:id_mission>/',
         GetAllDispositionByRICTandMission.as_view()),
    path('api/save_article_disposition/<int:rict>/<int:article>/<int:mission>/', SaveArticleDisposition.as_view()),

    # AvisArticle service
    path('api/get_all_avis_by_RICT_and_mission/<int:id_rict>/<int:id_mission>/', GetAllAvisByRICTandMission.as_view()),

    # Description Sommaire service
    path('api/get_desription_sommaire_by_RICT/<int:id_rict>/', GetDesriptionSommaireByRICT.as_view()),
    path('api/save_decription_sommaire/', SaveDecriptionSommaire.as_view()),

    # IT service
    path('api/add_intervention_technique/', AddInterventionTechnique.as_view()),

    # Remarque aso service
    path('api/set_remarque_on_aso/<int:id_aso>/', SetRemarqueOnAso.as_view()),
    path('api/get_all_remarque_general_on_aso/<int:id_aso>/', GetAllRemarqueGeneralOnAso.as_view()),
    path('api/get_user_remarque_general_on_aso/<int:id_aso>/', GetUserRemarqueGeneralOnAso.as_view()),
    path('api/edit_remarque/', EditRemarque.as_view()),

    # Commentaire service
    path('api/get_all_commentaire_on_affaire/<int:id_affaire>/', GetAllCommentaireOnAffaire.as_view()),
    path('api/lever_commentaire/', LeverCommentaire.as_view()),
    path('api/annuler_lever_commentaire/', AnnulerLever.as_view()),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('api/utilisateur-connecte/', UtilisateurConnecteView.as_view(), name='utilisateur_connecte'),

    path('docs/', include('drf_autodocs.urls')),
    path('admin/', admin.site.urls),

    path('plans-affaire/', GetAllPlansAffaire.as_view(), name='all-plans-affaire'),
    path('api/affaires-list/', AffaireListView.as_view(), name='affaire-list'),
    path('api/tutore/', TutorialIDList.as_view(), name='tutorial_ids'),
    path('batimentss/', BatimentAdminViewsetAdmin.as_view({'get': 'list'}), name='batiment-list'),
   
    path('add_sous_missions/<int:mission_parent_id>/add_sous_mission/', AddSousMissionView.as_view(), name='add-sous-mission'),
    path('get_missions_affaires/<int:id>/', AffaireDetailView.as_view(), name='affaire-detail'),

    path('active-cuurent-affaire/', ActiveAffaireView.as_view(), name='active-affaire'),
    #path('activate-missions/', ActivateMissionsView.as_view(), name='activate-missions'),
    path('active-affaire-mission/', ActiveAffaireViewMission.as_view(), name='active-affaire'),
    path('recuperer_toutes_missions_actives_affaire/', AffaireMissionsView.as_view(), name='affaire-missions'),
    path('selected-mission-active/', ToggleMissionActiveView.as_view(), name='toggle-mission'),
    path('missions-state-management/<int:mission_id>/sous-missions/', SousMissionsActivationView.as_view(), name='sous-missions-activation'),
    path('les-affaire-ouvrages/', AffaireOuvrageAdminViewset.as_view(), name='affaire-ouvrage-lis-api'),
    path('les-entreprises-affaire-ouvrage/', EntrepriseAffaireOuvrageViewsetAdministration.as_view(), name='entreprise-affaire-ouvrage-lis-api'),
    


    


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
