from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User
from leads.models import Lead
from .models import Campaign, CampaignLead
from .services import ensure_default_sequence

class CampaignTests(TestCase):
    def test_default_sequence_and_duplicate(self):
        u=User.objects.create_user(email='u@test.local',password='StrongPass123',full_name='U',role='sales_rep',team_name='T')
        lead=Lead.objects.create(owner=u,name='A',email='a@x.com',company='X',job_title='CEO',industry='SaaS',company_size='201-500')
        c=Campaign.objects.create(owner=u,name='C')
        ensure_default_sequence(c)
        self.assertEqual(c.sequence_steps.count(),3)
        CampaignLead.objects.create(campaign=c,lead=lead)
        self.assertEqual(CampaignLead.objects.count(),1)
