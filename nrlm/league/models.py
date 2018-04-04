from django.db import models
from config.settings.base import AUTH_USER_MODEL

class Player(models.Model):
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='players',
        on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    occured_at = models.DateField(default=None, null=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='events', 
        on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name

class Identity(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Game(models.Model):
    player = models.ForeignKey(Player, 
        on_delete=models.CASCADE, 
        related_name='main_player')
    identity = models.ForeignKey(Identity, 
        on_delete=models.CASCADE,
        related_name='main_player_identity')
    is_corp = models.BooleanField()
    played_against_player = models.ForeignKey(Player, 
        on_delete=models.CASCADE,
        related_name='opponent_player')
    played_against_identity = models.ForeignKey(Identity, 
        on_delete=models.CASCADE,
        related_name='opponent_player_id')
    points = models.IntegerField(default=0)
    round_num = models.IntegerField(null=True, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='games',
        on_delete=models.CASCADE, default=None, null=True)

    def save(self, *args, **kwargs):
        if self.player == self.played_against_player:
            raise Exception('Attempted to have same two players play each other')
        elif self.identity == self.played_against_identity:
            raise Exception('Attempted to have the same identities play each other')
        super(Game, self).save(*args, **kwargs)
