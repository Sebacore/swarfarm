from django.contrib.auth.models import User
from rest_framework import serializers

from herders.models import Summoner
from news.models import *


class UserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    summoner_name = serializers.CharField(source='summoner.summoner_name', allow_blank=True)
    server = serializers.ChoiceField(source='summoner.server', choices=Summoner.SERVER_CHOICES, allow_blank=True)
    public = serializers.BooleanField(source='summoner.public')
    timezone = serializers.CharField(source='summoner.timezone')

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'summoner_name', 'server', 'public', 'timezone')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ('url', 'pk', 'title', 'body', 'created', 'sticky')
