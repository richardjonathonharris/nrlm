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

