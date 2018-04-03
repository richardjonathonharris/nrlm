import json
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import force_authenticate, APIClient
from django.test import Client
from test_plus.test import TestCase

from nrlm.league.models import Player
from nrlm.users.models import User
from nrlm.league.serializers import PlayerSerializer

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
