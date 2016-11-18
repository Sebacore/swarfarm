from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly

from news.models import *
from .serializers import *


# Permissions
class IsStaffOrUser(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class IsStaffOrOwner(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


# User / Auth
class UserPagination(LimitOffsetPagination):
    default_limit = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    permission_classes = (IsStaffOrOwner, )
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return (AllowAny(), )
        else:
            return (IsStaffOrUser(), )

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all().order_by('pk')
        elif self.request.user.is_authenticated():
            return User.objects.filter(pk=self.request.user.pk)
        else:
            return User.objects.none()


# News
class ArticlePagination(LimitOffsetPagination):
    default_limit = 10


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
