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
    faction = serializers.CharField(required=True, max_length=500)
    is_corp = serializers.NullBooleanField()
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Identity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.faction = validated_data.get('faction', instance.faction)
        instance.is_corp = validated_data.get('is_corp', instance.is_corp)
        instance.save()
        return instance

    class Meta:
        model = Identity
        fields = ('id', 'name', 'faction', 'is_corp')

class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    runner = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all()) # can change this to id or slug if we want different values
    r_identity = serializers.PrimaryKeyRelatedField(queryset=Identity.objects.all())
    corp = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())
    c_identity = serializers.PrimaryKeyRelatedField(queryset=Identity.objects.all())
    r_points = serializers.IntegerField()
    c_points = serializers.IntegerField()
    round_num = serializers.IntegerField()
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    created_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.runner = validated_data.get('runner', instance.runner)
        instance.r_identity = validated_data.get('r_identity', instance.r_identity)
        instance.corp = validated_data.get('corp', instance.corp)
        instance.c_identity= validated_data.get('c_identity', instance.c_identity)
        instance.r_points = validated_data.get('r_points', instance.r_points)
        instance.c_points = validated_data.get('c_points', instance.c_points)
        instance.round_num = validated_data.get('round_num', instance.round_num)
        instance.event = validated_data.get('event', instance.event)
        instance.save()
        return instance

    class Meta:
        model = Game
        fields = ('id', 'runner', 'r_identity', 
            'corp', 'c_identity',
            'r_points', 'c_points',
            'round_num', 'event'
        )

class UserSerializer(serializers.ModelSerializer):
    players = serializers.HyperlinkedRelatedField(many=True, 
        view_name='player-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'players')
