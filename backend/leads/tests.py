from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User
from .models import Lead
from .services import calculate_lead_score

class LeadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='u@test.local',password='StrongPass123',full_name='U',role='sales_rep',team_name='T')
        self.other = User.objects.create_user(email='o@test.local',password='StrongPass123',full_name='O',role='sales_rep',team_name='Other')
        self.client=APIClient(); self.client.force_authenticate(self.user)
    def test_deterministic_score(self):
        lead=Lead.objects.create(owner=self.user,name='A',email='a@x.com',company='X',job_title='HR Manager',industry='SaaS',company_size='201-500',hiring_signal=True,signal_description='Hiring 10 roles')
        result=calculate_lead_score(lead)
        self.assertEqual(result['total'],100)
        self.assertEqual(result['priority'],'high')
        self.assertEqual(result['breakdown']['growth_signal'],25)
    def test_ownership(self):
        Lead.objects.create(owner=self.other,name='B',email='b@x.com',company='Y',job_title='CEO',industry='SaaS',company_size='201-500')
        r=self.client.get('/api/leads/')
        self.assertEqual(r.status_code,200)
        self.assertEqual(len(r.data),0)
