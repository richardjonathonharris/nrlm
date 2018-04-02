from rest_framework import serializers
from nrlm.league.models import Game, Player, Event, Identity

class PlayerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=500)
    created_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
