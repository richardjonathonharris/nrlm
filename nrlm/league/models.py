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
    faction = models.CharField(max_length=500, null=True)
    is_corp = models.NullBooleanField()
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='identities', 
        on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    runner = models.ForeignKey(Player, 
        on_delete=models.CASCADE, 
        related_name='main_player')
    r_identity = models.ForeignKey(Identity, 
        on_delete=models.CASCADE,
        related_name='main_player_identity')
    corp= models.ForeignKey(Player, 
        on_delete=models.CASCADE,
        related_name='opponent_player')
    c_identity = models.ForeignKey(Identity, 
        on_delete=models.CASCADE,
        related_name='opponent_player_id')
    r_points = models.IntegerField(default=0)
    c_points = models.IntegerField(default=0)
    round_num = models.IntegerField(null=True, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='games',
        on_delete=models.CASCADE, default=None, null=True)

    def save(self, *args, **kwargs):
        if self.runner == self.corp:
            raise Exception('Attempted to have same two players play each other')
        elif self.r_identity == self.c_identity:
            raise Exception('Attempted to have the same identities play each other')
        super(Game, self).save(*args, **kwargs)
