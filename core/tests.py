from django.core.management import call_command
from django.utils.http import urlencode
from rest_framework.test import APITestCase
from django.urls import reverse

from core.models import UserRole


class TestBasketBall(APITestCase):
    multi_db = True

    def test_get_score_board(self):
        call_command('init_basketball_data')
        response = self.client.get(reverse('scoreboard'))
        self.assertEqual(response.json()['success'], True)
        self.assertIsInstance(response.json()['score_board'], list)

    def test_coach(self):
        call_command('init_basketball_data')
        user_role = UserRole.objects.filter(role_id=2)
        user_role_coach = UserRole.objects.filter(role_id=1)
        player_id = user_role[0].user_id
        coach_id = user_role_coach[0].user_id
        response = self.client.get(reverse('coach', kwargs={'user_id': player_id}), format='json')
        self.assertEqual(response.json()['success'], False)
        response = self.client.get(reverse('coach', kwargs={'user_id': coach_id}), format='json')
        self.assertEqual(response.json()['success'], True)
