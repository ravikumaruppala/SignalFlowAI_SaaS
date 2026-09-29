from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from campaigns.models import Campaign, CampaignLead
from campaigns.services import ensure_default_sequence
from leads.models import Lead
from leads.services import calculate_lead_score
from inbox.models import Activity, InboxReply

User = get_user_model()

LEADS = [
    ('Aarav Mehta','aarav@novaforge.test','NovaForge','Head of Sales','SaaS','201-500','hiring','Hiring 18 roles across sales and customer success',True,True,False),
    ('Maya Shah','maya@cloudharbor.test','CloudHarbor','HR Director','HRTech','51-200','growth','Regional expansion is recorded in the sample signal set',True,True,False),
    ('Rohan Iyer','rohan@paygrid.test','PayGrid','COO','FinTech','501-1000','leadership','New operations leadership recorded in sample data',True,False,True),
    ('Ananya Rao','ananya@edulink.test','EduLink','Revenue Operations Manager','EdTech','201-500','growth','Expansion into two new markets in sample data',True,True,False),
    ('Vikram Nair','vikram@logiwave.test','LogiWave','VP Operations','Logistics','501-1000','hiring','Warehouse and operations hiring signal',True,True,False),
    ('Sara Thomas','sara@healthnest.test','HealthNest','People Operations Lead','HealthTech','51-200','growth','Growth signal in sample company profile',True,True,False),
    ('Karan Verma','karan@securemesh.test','SecureMesh','Founder','Cybersecurity','51-200','hiring','Engineering and GTM hiring signal',True,True,False),
    ('Ishita Sen','ishita@brightpath.test','BrightPath','Sales Manager','SaaS','201-500','growth','New vertical launch signal',True,True,False),
    ('Aditya Rao','aditya@finspire.test','FinSpire','Finance Operations Lead','FinTech','51-200','none','No strong growth trigger recorded',True,False,False),
    ('Neha Kulkarni','neha@learnsphere.test','LearnSphere','CEO','EdTech','11-50','none','No strong growth trigger recorded',True,False,False),
    ('Dev Malhotra','dev@fleetpilot.test','FleetPilot','COO','Logistics','51-200','growth','Customer expansion signal in sample data',True,True,False),
    ('Priya Menon','priya@carestack.test','CareStack','HR Manager','HealthTech','201-500','hiring','Hiring signal in operations team',True,True,False),
    ('Rahul Jain','rahul@peoplepulse.test','PeoplePulse','Head of People','HRTech','51-200','leadership','Leadership transition signal',True,False,True),
    ('Meera Gupta','meera@retailops.test','RetailOps','Operations Manager','Retail','201-500','none','No strong growth trigger recorded',True,False,False),
    ('Kabir Das','kabir@marketmint.test','MarketMint','Head of Revenue','SaaS','501-1000','growth','New enterprise segment signal',True,True,False),
    ('Pooja Reddy','pooja@insureflow.test','InsureFlow','HR Director','FinTech','201-500','hiring','Sample signal records hiring',True,True,False),
    ('Arjun Singh','arjun@dataorbit.test','DataOrbit','Founder','Cybersecurity','11-50','none','No strong growth trigger recorded',True,False,False),
    ('Nisha Kapoor','nisha@talentgrid.test','TalentGrid','VP People','HRTech','501-1000','growth','Scale-up signal in sample data',True,True,False),
    ('Sameer Bhat','sameer@routezen.test','RouteZen','COO','Logistics','51-200','none','No strong growth trigger recorded',True,False,False),
    ('Riya Joshi','riya@skillstack.test','SkillStack','Revenue Operations','EdTech','201-500','hiring','New sales hiring signal',True,True,False),
    ('Sahil Kumar','sahil@cyberlane.test','CyberLane','Sales Director','Cybersecurity','201-500','growth','Expansion signal in sample data',True,True,False),
    ('Aditi Bose','aditi@mediflow.test','MediFlow','HR Lead','HealthTech','51-200','none','No strong growth trigger recorded',True,False,False),
    ('Manav Shah','manav@finbase.test','FinBase','CEO','FinTech','201-500','growth','New regional team signal',True,True,False),
    ('Tanvi Rao','tanvi@hirestack.test','HireStack','People Operations','HRTech','11-50','hiring','Hiring signal in sample data',True,True,False),
]

@transaction.atomic
def seed():
    sales, _ = User.objects.get_or_create(email='sales@signalflow.local', defaults={'full_name':'Demo Sales Rep','role':'sales_rep','team_name':'Demo Sales Team'})
    sales.set_password('Demo@12345'); sales.save()
    manager, _ = User.objects.get_or_create(email='manager@signalflow.local', defaults={'full_name':'Demo Sales Manager','role':'manager','team_name':'Demo Sales Team'})
    manager.set_password('Demo@12345'); manager.save()
    admin, _ = User.objects.get_or_create(email='admin@signalflow.local', defaults={'full_name':'Demo Admin','role':'admin','team_name':'Demo Sales Team','is_staff':True,'is_superuser':True})
    admin.set_password('Admin@12345'); admin.is_staff=True; admin.is_superuser=True; admin.save()
    Lead.objects.filter(owner__in=[sales, manager]).delete()
    for i, row in enumerate(LEADS):
        name,email,company,title,industry,size,stype,sdesc,available,growth,leadership = row
        lead = Lead.objects.create(owner=sales, name=name,email=email,company=company,job_title=title,industry=industry,company_size=size,status='new',signal_type=stype.title()+' signal',signal_description=sdesc,contact_available=available,company_growth=growth,hiring_signal=stype=='hiring',leadership_change=leadership)
        calculate_lead_score(lead)
    Campaign.objects.filter(owner=sales).delete()
    campaigns = [
        ('Q4 High-Intent Outreach','Focus on high-priority leads with verified sample signals.','active'),
        ('Growth Signal Follow-up','Use growth and hiring context in concise outreach.','draft'),
        ('Ops Leaders Pilot','Pilot sequence for operations leadership titles.','active'),
    ]
    leads = list(Lead.objects.filter(owner=sales).order_by('-score'))
    for idx,(name,desc,status) in enumerate(campaigns):
        camp = Campaign.objects.create(owner=sales,name=name,description=desc,status=status)
        ensure_default_sequence(camp)
        for lead in leads[idx*4:idx*4+5]:
            CampaignLead.objects.get_or_create(campaign=camp,lead=lead)
        for member in camp.campaign_leads.all()[:3]:
            Activity.objects.get_or_create(user=sales,lead=member.lead,campaign=camp,activity_type='simulated_send',defaults={'metadata':{'simulated':True,'seeded':True}})
        member = camp.campaign_leads.all().first()
        if member:
            Activity.objects.get_or_create(user=sales,lead=member.lead,campaign=camp,activity_type='simulated_reply',defaults={'metadata':{'simulated':True,'seeded':True}})
            InboxReply.objects.create(lead=member.lead,campaign=camp,body=f'Thanks for reaching out. Could you share a bit more context for {member.lead.company}?',category='needs_reply',simulated=True)
    return len(leads)

class Command(BaseCommand):
    help='Create/reset realistic demo data for SignalFlow AI.'
    def handle(self, *args, **kwargs):
        n = seed()
        self.stdout.write(self.style.SUCCESS(f'Seeded {n} leads and demo campaigns.'))
        self.stdout.write('Sales Rep: sales@signalflow.local / Demo@12345')
        self.stdout.write('Manager: manager@signalflow.local / Demo@12345')
        self.stdout.write('Admin: admin@signalflow.local / Admin@12345')
