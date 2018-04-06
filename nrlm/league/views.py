from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from nrlm.league.models import Player, Event, Identity, Game
from nrlm.league.serializers import PlayerSerializer, \
    UserSerializer, EventSerializer, IdentitySerializer, \
    GameSerializer
from nrlm.users.models import User
from nrlm.league.permissions import IsOwnerOrReadOnly

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = (permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )
    authentication_class = (JSONWebTokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )
    authentication_class = (JSONWebTokenAuthentication,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class IdentityViewSet(viewsets.ModelViewSet):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    )
    authentication_class = (JSONWebTokenAuthentication,
    )

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
        )
    authentication_class = (JSONWebTokenAuthentication, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
