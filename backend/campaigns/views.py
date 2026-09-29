from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Campaign, CampaignLead
from .serializers import CampaignSerializer
from .services import ensure_default_sequence
from leads.models import Lead
from inbox.models import Activity

class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = Campaign.objects.prefetch_related('sequence_steps','campaign_leads__lead')
        if self.request.user.role == 'sales_rep':
            return qs.filter(owner=self.request.user)
        return qs.filter(owner__team_name=self.request.user.team_name)
    def perform_create(self, serializer):
        campaign = serializer.save(owner=self.request.user)
        ensure_default_sequence(campaign)
    @action(detail=True, methods=['post'], url_path='leads')
    def assign_leads(self, request, pk=None):
        campaign = self.get_object()
        ids = request.data.get('lead_ids', [])
        created, skipped = 0, 0
        for lead_id in ids:
            try:
                lead = Lead.objects.get(id=lead_id)
                if request.user.role == 'sales_rep' and lead.owner_id != request.user.id:
                    skipped += 1; continue
                if request.user.role != 'sales_rep' and lead.owner.team_name != request.user.team_name:
                    skipped += 1; continue
                CampaignLead.objects.create(campaign=campaign, lead=lead)
                created += 1
            except (Lead.DoesNotExist, IntegrityError):
                skipped += 1
        return Response({'created': created, 'skipped': skipped}, status=status.HTTP_200_OK)
    @action(detail=True, methods=['post'], url_path='simulate')
    def simulate(self, request, pk=None):
        campaign = self.get_object()
        event = request.data.get('event', 'send')
        allowed = {'send':'simulated_send','open':'simulated_open','reply':'simulated_reply','meeting':'meeting'}
        if event not in allowed:
            return Response({'detail': 'Unsupported simulation event.'}, status=400)
        ids = request.data.get('lead_ids') or list(campaign.campaign_leads.values_list('lead_id', flat=True)[:1])
        created = 0
        for lead_id in ids:
            member = CampaignLead.objects.filter(campaign=campaign, lead_id=lead_id).select_related('lead').first()
            if not member: continue
            if Activity.objects.filter(campaign=campaign, lead_id=lead_id, activity_type=allowed[event]).exists():
                continue
            Activity.objects.create(user=request.user, lead=member.lead, campaign=campaign, activity_type=allowed[event], metadata={'simulated': True})
            if event == 'reply':
                from inbox.models import InboxReply
                InboxReply.objects.create(lead=member.lead, campaign=campaign, body=f'Hi, thanks for the outreach. Please share a little more context about the next step.', category='needs_reply', simulated=True)
            elif event == 'meeting':
                member.lead.status = 'meeting'
                member.lead.save(update_fields=['status','updated_at'])
            elif event == 'send':
                member.lead.status = 'contacted'
                member.lead.save(update_fields=['status','updated_at'])
            created += 1
        return Response({'event': event, 'created': created})
