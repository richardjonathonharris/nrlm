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
    def test_cannot_save_same_players(self):
        player = Player.objects.create(name='Test User 1')
        identity1 = Identity.objects.create(name='Identity 1')
        identity2 = Identity.objects.create(name='Identity 2')
        event = Event.objects.create(name='Test Event 1')
        with self.assertRaises(Exception) as cm:
            Game.objects.create(
                player = Player.objects.get(name='Test User 1'),
                identity = Identity.objects.get(name='Identity 1'),
                is_corp = False,
                played_against_player = Player.objects.get(name='Test User 1'),
                played_against_identity = Identity.objects.get(name='Identity 2'),
                points = 0,
                round_num = 1,
                event = Event.objects.get(name='Test Event 1')
            )

        self.assertEqual(str(cm.exception), 
                'Attempted to have same two players play each other')

    def test_cannot_save_same_identities(self):
        player1 = Player.objects.create(name='Test User 1')
        player2 = Player.objects.create(name='Test User 2')
        identity = Identity.objects.create(name='Problem')
        event = Event.objects.create(name='Test Event 1')
        with self.assertRaises(Exception) as cm:
            Game.objects.create(
                player = Player.objects.get(name='Test User 1'),
                identity = Identity.objects.get(name='Problem'),
                is_corp=False,
                played_against_player = Player.objects.get(name='Test User 2'),
                played_against_identity = Identity.objects.get(name='Problem'),
                points=0,
                round_num=1,
                event=Event.objects.get(name='Test Event 1')
            )

        self.assertEqual(str(cm.exception),
            'Attempted to have the same identities play each other')
