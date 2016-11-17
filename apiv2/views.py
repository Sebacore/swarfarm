from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission, AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly

from news.models import *
from .serializers import *


# Permissions
class IsStaffOrTargetUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


# User / Auth
class UserPagination(LimitOffsetPagination):
    default_limit = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def get_permissions(self):
        # Allow non-authed user to create via POST
        return (AllowAny(), ) if self.request.method == 'POST' else (IsStaffOrTargetUser(), )


# News
class ArticlePagination(LimitOffsetPagination):
    default_limit = 10


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
