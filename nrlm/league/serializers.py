from rest_framework import serializers
from nrlm.league.models import Game, Player, Event, Identity
from nrlm.users.models import User

class PlayerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=500)
    created_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False)
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    class Meta:
        model = Player
        fields = ('id', 'name', 'created_at', 'modified_at', 'owner')

class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=500)
    created_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False)
    occured_at = serializers.DateField(required=False)
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    class Meta:
        model = Event
        fields = ('id', 'name', 'occured_at', 'owner')

class IdentitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=500)

    def create(self, validated_data):
        return Identity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    class Meta:
        model = Identity
        fields = ('id', 'name')

class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all()) # can change this to id or slug if we want different values
    identity = serializers.PrimaryKeyRelatedField(queryset=Identity.objects.all())
    is_corp = serializers.BooleanField()
    played_against_player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())
    played_against_identity = serializers.PrimaryKeyRelatedField(queryset=Identity.objects.all())
    points = serializers.IntegerField()
    round_num = serializers.IntegerField()
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    created_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.player = validated_data.get('player', instance.player)
        instance.identity = validated_data.get('identity', instance.identity)
        instance.is_corp = validated_data.get('is_corp', instance.is_corp)
        instance.played_against_player = validated_data.get('played_against_player', instance.played_against_player)
        instance.played_against_identity = validated_data.get('played_against_identity', instance.played_against_identity)
        instance.points = validated_data.get('points', instance.points)
        instance.round_num = validated_data.get('round_num', instance.round_num)
        instance.event = validated_data.get('event', instance.event)

    class Meta:
        model = Game
        fields = ('id', 'player', 'identity', 'is_corp', 
            'played_against_player', 'played_against_identity',
            'points', 'round_num', 'event'
        )

class UserSerializer(serializers.ModelSerializer):
    players = serializers.HyperlinkedRelatedField(many=True, 
        view_name='player-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'players')
