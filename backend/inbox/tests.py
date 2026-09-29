from django.test import TestCase
from accounts.models import User
from leads.models import Lead
from .models import InboxReply

class InboxTests(TestCase):
    def test_reply_category_updates_status(self):
        u=User.objects.create_user(email='u@test.local',password='StrongPass123',full_name='U',role='sales_rep',team_name='T')
        lead=Lead.objects.create(owner=u,name='A',email='a@x.com',company='X',job_title='CEO',industry='SaaS',company_size='201-500')
        reply=InboxReply.objects.create(lead=lead,body='Interested')
        self.client.force_login(u)
        r=self.client.patch(f'/api/inbox/{reply.id}/',{'category':'interested'},content_type='application/json')
        self.assertEqual(r.status_code,200)
        lead.refresh_from_db(); self.assertEqual(lead.status,'interested')
