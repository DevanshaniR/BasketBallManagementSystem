from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase
from django.urls import reverse

from core.models import UserRole


class TestBasketBall(APITestCase):

    def create_test_data_and_authenticate(self):
        call_command('init_basketball_data')
        user = User.objects.create_user(username="test_user", email="test@gmail.com", password="mydemo",
                                        first_name="test_user", last_name="test_lastname")
        user.save()
        p = UserRole(user_id=user.id, role_id=3, is_logged_in=0)
        p.save()
        self.assertTrue(self.client.login(username='test_user', password='mydemo'))

    def test_get_score_board(self):
        self.create_test_data_and_authenticate()
        response = self.client.get(reverse('scoreboard'))
        self.assertEqual(response.json()['success'], True)
        self.assertIsInstance(response.json()['score_board'], list)

    def test_coach(self):
        self.create_test_data_and_authenticate()
        user_role = UserRole.objects.filter(role_id=2)
        user_role_coach = UserRole.objects.filter(role_id=1)
        player_id = user_role[0].user_id
        coach_id = user_role_coach[0].user_id
        response = self.client.get(reverse('coach', kwargs={'user_id': player_id}), format='json')
        self.assertEqual(response.json()['success'], False)
        response = self.client.get(reverse('coach', kwargs={'user_id': coach_id}), format='json')
        self.assertEqual(response.json()['success'], True)

    def test_player_score(self):
        self.create_test_data_and_authenticate()
        user_role = UserRole.objects.filter(role_id=2)
        user_role_coach = UserRole.objects.filter(role_id=1)
        player_id = user_role[0].user_id
        coach_id = user_role_coach[0].user_id
        response = self.client.get(reverse('player_score', kwargs={'user_id': player_id}), {'filter_score': 90},
                                   format='json')
        self.assertEqual(response.json()['success'], False)
        response = self.client.get(reverse('player_score', kwargs={'user_id': coach_id}), {'filter_score': 90},
                                   format='json')
        self.assertEqual(response.json()['success'], True)

    def test_team_details(self):
        self.create_test_data_and_authenticate()
        user_role = UserRole.objects.filter(role_id=2)
        user_role_coach = UserRole.objects.filter(role_id=1)
        admin = UserRole.objects.filter(role_id=3)
        player_id = user_role[0].user_id
        coach_id = user_role_coach[0].user_id
        admin_id = admin[0].user_id
        response = self.client.get(reverse('team_details', kwargs={'user_id': player_id}),
                                   format='json')
        self.assertEqual(response.json()['success'], False)
        response = self.client.get(reverse('team_details', kwargs={'user_id': coach_id}),
                                   format='json')
        self.assertEqual(response.json()['success'], False)
        response = self.client.get(reverse('team_details', kwargs={'user_id': admin_id}),
                                   format='json')
        self.assertEqual(response.json()['success'], True)

    def test_team_details(self):
        self.create_test_data_and_authenticate()
        user_role = UserRole.objects.filter(role_id=2)
        user_role_coach = UserRole.objects.filter(role_id=1)
        admin = UserRole.objects.filter(role_id=3)
        player_id = user_role[0].user_id
        coach_id = user_role_coach[0].user_id
        admin_id = admin[0].user_id
        response = self.client.get(reverse('login_details', kwargs={'user_id': player_id}),
                                   format='json')
        self.assertEqual(response.json()['success'], False)
        response = self.client.get(reverse('login_details', kwargs={'user_id': coach_id}),
                                   format='json')
        self.assertEqual(response.json()['success'], False)
        response = self.client.get(reverse('login_details', kwargs={'user_id': admin_id}),
                                   format='json')
        self.assertEqual(response.json()['success'], True)
