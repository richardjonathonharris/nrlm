from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

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
    points = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
