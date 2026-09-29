from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=False)
    def test_register_login_logout(self):
        r = self.client.post('/api/auth/register/', {'email':'new@test.local','full_name':'New User','password':'StrongPass123','role':'sales_rep','team_name':'Demo Sales Team'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 200)
        self.assertEqual(self.client.post('/api/auth/logout/').status_code, 200)

    def test_login_accepts_csrf_token_from_bootstrap_endpoint(self):
        user = User.objects.create_user(email='login@test.local', password='StrongPass123')
        client = APIClient(enforce_csrf_checks=True)

        csrf_response = client.get('/api/auth/csrf/')
        response = client.post(
            '/api/auth/login/',
            {'email': user.email, 'password': 'StrongPass123'},
            format='json',
            HTTP_ORIGIN='http://127.0.0.1:5173',
            HTTP_X_CSRFTOKEN=csrf_response.data['csrfToken'],
        )

        self.assertEqual(response.status_code, 200)
