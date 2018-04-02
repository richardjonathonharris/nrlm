from test_plus.test import TestCase
from nrlm.league.models import *

class PlayerModelTest(TestCase):
    def test_string_representation(self):
        player = Player(name='Test User')
        self.assertEqual(str(player), player.name)

class EventModelTest(TestCase):
    def test_string_representation(self):
        event = Event(name='Test Event')
        self.assertEqual(str(event), event.name)

class IdentityModelTest(TestCase):
    def test_string_representation(self):
        identity = Identity(name='Test Identity')
        self.assertEqual(str(identity), identity.name)

class GameModelTest(TestCase):
    game = Game(
                player=Player(name='Test User'),
                identity=Identity(name='Test Identity'),
                is_corp=0,
                played_against_player=Player(name='Other User'),
                played_against_identity=Identity(name='Another Ident'),
                points=0,
                event=Event(name='Cool event'))
