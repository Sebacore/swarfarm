from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly

from news.models import *
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
