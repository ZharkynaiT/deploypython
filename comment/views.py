from rest_framework.viewsets import  ModelViewSet


from .models import Comment
from .serializers import CommentSerializer

from problem.views import PermissionMixin


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
