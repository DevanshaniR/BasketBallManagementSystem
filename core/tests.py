from django.core.management import call_command
from rest_framework.test import APITestCase
from django.urls import reverse


class TestBasketBall(APITestCase):
    def test_get_score_board(self):
        call_command('init_basketball_data')
        response = self.client.get(reverse('scoreboard'))
        self.assertEqual(response.json()['success'], True)
        self.assertIsInstance(response.json()['score_board'], list)
