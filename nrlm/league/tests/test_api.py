import json
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import force_authenticate, APIClient
from django.test import Client
from test_plus.test import TestCase

from nrlm.league.models import Player, Event, Identity, Game
from nrlm.users.models import User
from nrlm.league.serializers import PlayerSerializer, EventSerializer, \
        IdentitySerializer, GameSerializer

client = Client()
apiclient = APIClient()

class TestGetPlayerRoute(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        User.objects.create(username='maude')
        all_owners = User.objects.all()
        Player.objects.create(
            name='Player 1', owner=all_owners[0]
        )
        Player.objects.create(
            name='Player 2', owner=User.objects.get(id=1)
        )
        Player.objects.create(
            name='Player 3 (Maude\'s Favorite)',
            owner=User.objects.get(id=2)
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def test_list_response(self):
        response = client.get(reverse('player-list'))
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_player(self):
        response = client.get(
            reverse('player-detail', kwargs={'pk': 2})
        )
        player_2 = Player.objects.get(id=2)
        serializer = PlayerSerializer(player_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_player(self):
        response = client.get(
            reverse('player-detail', kwargs={'pk': 200})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestGetEventRoute(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Event.objects.create(
            name='Event 1',
            owner=User.objects.get(username='richard')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.event_id = Event.objects.get(name='Event 1').id
        self.endpoint = '/events/' + str(self.event_id) + '/'

    def test_list_response(self):
        response = apiclient.get('/events/')
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_event(self):
        response = apiclient.get(self.endpoint)
        event = Event.objects.get(name='Event 1')
        serializer = EventSerializer(event)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_event(self):
        response = apiclient.get('/events/4000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestGetIdentityRoute(TestCase):

    @classmethod
    def setUpTestData(cls):
        Identity.objects.create(
            name='MaxX: Maximum Punk Rock'
        )
        User.objects.create(username='richard')

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.identity_id = Identity.objects.get(name='MaxX: Maximum Punk Rock').id
        self.endpoint = '/identities/' + str(self.identity_id) + '/'

    def test_list_response(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.get('/identities/')
        idents = Identity.objects.all()
        serializer = IdentitySerializer(idents, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_identity(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.get(self.endpoint)
        ident = Identity.objects.get(name='MaxX: Maximum Punk Rock')
        serializer = IdentitySerializer(ident)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_invalid_single_identity(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.get('/identities/4000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestGetGameRoute(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Player.objects.create(
            name='Player 1',
            owner=User.objects.get(username='richard')
        )
        Player.objects.create(
            name='Player 2',
            owner=User.objects.get(username='richard')
        )
        Identity.objects.create(
            name='Identity 1'
        )
        Identity.objects.create(
            name='Identity 2'
        )
        Event.objects.create(
            name='Event 1',
            owner=User.objects.get(username='richard')
        )
        Game.objects.create(
            player=Player.objects.get(name='Player 1'),
            identity=Identity.objects.get(name='Identity 1'),
            is_corp=True,
            played_against_player=Player.objects.get(name='Player 2'),
            played_against_identity=Identity.objects.get(name='Identity 2'),
            points=0,
            round_num=1,
            event=Event.objects.get(name='Event 1')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.game_id = Game.objects.get(id=1).id
        self.endpoint = '/games/' + str(self.game_id) + '/'

    def test_list_response(self):
        response = apiclient.get('/games/')
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_game(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.get(self.endpoint)
        game = Game.objects.get(id=1)
        serializer = GameSerializer(game)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_invalid_single_game(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.get('/games/4000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class TestCreateNewPlayer(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def test_create_valid_player(self):
        valid_payload = {
            'name': 'Test Player',
            'owner': 1
        }

        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.post('/players/', valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_player(self):
        payload = {
            'name': None,
            'owner': 1
        }
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.post('/players/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestCreateNewEvent(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def test_create_valid_event(self):
        payload = {
            'name': 'Event 1',
            'owner': 1
        }
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.post('/events/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event(self):
        payload = {
            'name': None,
            'owner': 1
        }
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.post('/events/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestCreateNewIdentity(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def test_create_valid_event(self):
        payload = {
            'name': 'NBN: Making News'
        }
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.post('/identities/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event(self):
        payload = {'name': None}
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.post('/identities/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestCreateNewIdentity(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Player.objects.create(
            name='Player 1',
            owner=User.objects.get(username='richard')
        )
        Player.objects.create(
            name='Player 2',
            owner=User.objects.get(username='richard')
        )
        Identity.objects.create(
            name='Identity 1'
        )
        Identity.objects.create(
            name='Identity 2'
        )
        Event.objects.create(
            name='Event 1',
            owner=User.objects.get(username='richard')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.player1id = Player.objects.get(name='Player 1').id
        self.player2id = Player.objects.get(name='Player 2').id
        self.identity1id = Identity.objects.get(name='Identity 1').id
        self.identity2id = Identity.objects.get(name='Identity 2').id
        self.eventid = Event.objects.get(name='Event 1').id

    def test_create_valid_game(self):
        payload = {
            'player': self.player1id,
            'identity': self.identity1id,
            'is_corp': True,
            'played_against_player': self.player2id,
            'played_against_identity': self.identity2id,
            'points': 0,
            'round_num': 1,
            'event': self.eventid,
        }
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.post('/games/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event(self):
        payload = {
            'player': self.player1id,
            'identity': self.identity1id,
            'is_corp': True,
            'played_against_player': self.player1id,
            'played_against_identity': self.identity2id,
            'points': 0,
            'round_num': 1,
            'event': self.eventid,
        }
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.post('/events/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSinglePlayer(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Player.objects.create(
            name='Player 1',
            owner=User.objects.get(username='richard')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.player_id = Player.objects.get(name='Player 1').id
        self.endpoint = '/players/' + str(self.player_id) + '/'

    def test_valid_update_player(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.put(self.endpoint, 
            {'name': 'New Player 1'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_player(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.put(self.endpoint,
            {'name': None},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleEvent(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Event.objects.create(
            name='Event 1',
            owner=User.objects.get(username='richard')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.event_id = Event.objects.get(name='Event 1').id
        self.endpoint = '/events/' + str(self.event_id) + '/'

    def test_valid_update_event(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.put(self.endpoint,
            {'name': 'New Event Here'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_event(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.put(self.endpoint,
            {'name': None},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleIdentity(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Identity.objects.create(
            name='NBN: Making News'
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self): 
        self.ident = Identity.objects.get(name='NBN: Making News').id
        self.endpoint = '/identities/' + str(self.ident) + '/'

    def test_valid_update_identity(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.put(self.endpoint,
            {'name': 'NBN: Controlling the Message'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_identity(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.put(self.endpoint,
            {'name': None},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleGame(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Player.objects.create(
            name='Player 1',
            owner=User.objects.get(username='richard')
        )
        Player.objects.create(
            name='Player 2',
            owner=User.objects.get(username='richard')
        )
        Identity.objects.create(
            name='Identity 1'
        )
        Identity.objects.create(
            name='Identity 2'
        )
        Event.objects.create(
            name='Event 1',
            owner=User.objects.get(username='richard')
        )
        Game.objects.create(
            player=Player.objects.get(name='Player 1'),
            identity=Identity.objects.get(name='Identity 1'),
            is_corp=True,
            played_against_player=Player.objects.get(name='Player 2'),
            played_against_identity=Identity.objects.get(name='Identity 2'),
            points=0,
            round_num=1,
            event=Event.objects.get(name='Event 1'),
            owner=User.objects.get(username='richard')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.game_id = Game.objects.all()[0].id
        self.endpoint = '/games/' + str(self.game_id) + '/'

    def test_valid_update_game(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        data = apiclient.get(self.endpoint).data
        response = apiclient.put(self.endpoint,
            {
                'player': data['player'],
                'identity': data['identity'],
                'is_corp': False,
                'played_against_player': data['played_against_player'],
                'played_against_identity': data['played_against_identity'],
                'points': data['points'],
                'round_num': data['round_num'],
                'event': data['event']
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_identity(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.put(self.endpoint,
            {'played_against_player': Player.objects.get(name='Player 1').id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSinglePlayer(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Player.objects.create(
            name='Player 1',
            owner=User.objects.get(username='richard')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.player_id = Player.objects.get(name='Player 1').id
        self.endpoint = '/players/' + str(self.player_id) + '/'

    def test_delete_valid_player(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_player(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.delete('/players/4000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class DeleteSingleEvent(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Event.objects.create(
            name='Event 1',
            owner=User.objects.get(username='richard')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.event_id = Event.objects.get(name='Event 1').id
        self.endpoint = '/events/' + str(self.event_id) + '/'

    def test_delete_valid_event(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_event(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.delete('/events/4000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class DeleteSingleIdentity(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Identity.objects.create(
            name='Jinteki'
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.ident = Identity.objects.get(name='Jinteki').id
        self.endpoint = '/identities/' + str(self.ident) + '/'

    def test_delete_valid_identity(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_identity(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.delete('/identities/4000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class DeleteSingleGame(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='richard')
        Player.objects.create(
            name='Player 1',
            owner=User.objects.get(username='richard')
        )
        Player.objects.create(
            name='Player 2',
            owner=User.objects.get(username='richard')
        )
        Identity.objects.create(
            name='Identity 1'
        )
        Identity.objects.create(
            name='Identity 2'
        )
        Event.objects.create(
            name='Event 1',
            owner=User.objects.get(username='richard')
        )
        Game.objects.create(
            player=Player.objects.get(name='Player 1'),
            identity=Identity.objects.get(name='Identity 1'),
            is_corp=True,
            played_against_player=Player.objects.get(name='Player 2'),
            played_against_identity=Identity.objects.get(name='Identity 2'),
            points=0,
            round_num=1,
            event=Event.objects.get(name='Event 1'),
            owner=User.objects.get(username='richard')
        )

    def tearDown(self):
        apiclient.force_authenticate(user=None)

    def setUp(self):
        self.game_id = Game.objects.all()[0].id
        self.endpoint = '/games/' + str(self.game_id) + '/'

    def test_delete_valid_game(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_game(self):
        apiclient.force_authenticate(user=User.objects.get(username='richard'))
        response = apiclient.delete('/identities/4000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

