from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Commentaire
from .permissions import IsAdminAuthenticated
from .serializers import CommentaireSerializer
from rest_framework.views import APIView
from django.forms.models import model_to_dict


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CommentaireAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentaireSerializer
    queryset = Commentaire.objects.all()
    permission_classes = [IsAdminAuthenticated]

class GetAllCommentForAvis(APIView):
    def get(self, request, id_avis):
        all_comment = Commentaire.objects.all()
        data = []
        for comment in all_comment:
            avis = comment.id_avis
            if avis.id == id_avis:
                data.append(model_to_dict(comment))
        
        return Response(data)