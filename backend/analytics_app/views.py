from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from leads.models import Lead
from campaigns.models import Campaign
from inbox.models import Activity, InboxReply

def scoped(user):
    if user.role == 'sales_rep':
        return Lead.objects.filter(owner=user), Campaign.objects.filter(owner=user)
    return Lead.objects.filter(owner__team_name=user.team_name), Campaign.objects.filter(owner__team_name=user.team_name)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_view(request):
    leads, campaigns = scoped(request.user)
    lead_ids = list(leads.values_list('id', flat=True))
    campaign_ids = list(campaigns.values_list('id', flat=True))
    acts = Activity.objects.filter(lead_id__in=lead_ids)
    counts = {k: acts.filter(activity_type=k).count() for k in ['simulated_send','simulated_open','simulated_reply','meeting']}
    real_sends = acts.filter(activity_type='email_sent').count()
    status_counts = dict(leads.values('status').annotate(c=Count('id')).values_list('status','c'))
    priority_counts = dict(leads.values('priority').annotate(c=Count('id')).values_list('priority','c'))
    reply_counts = dict(InboxReply.objects.filter(lead_id__in=lead_ids).values('category').annotate(c=Count('id')).values_list('category','c'))
    total = leads.count()
    conversion = round((status_counts.get('meeting',0)/total)*100, 2) if total else 0
    return Response({'totals': {'leads': total, 'campaigns': campaigns.count(), 'sends': counts['simulated_send'] + real_sends, 'opens': counts['simulated_open'], 'replies': counts['simulated_reply'], 'interested': status_counts.get('interested',0), 'meetings': counts['meeting'], 'conversion_rate': conversion}, 'by_status': status_counts, 'by_priority': priority_counts, 'reply_categories': reply_counts, 'simulated': {'opens': True, 'replies': True, 'meetings': True}, 'real_email_sends': real_sends})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    leads, campaigns = scoped(request.user)
    lead_ids = list(leads.values_list('id', flat=True))
    campaign_ids = list(campaigns.values_list('id', flat=True))
    acts = Activity.objects.filter(lead_id__in=lead_ids)
    high = leads.filter(priority='high').count()
    data = {
        'metrics': {
            'total_leads': leads.count(), 'high_priority': high, 'active_campaigns': campaigns.filter(status='active').count(),
            'sends': acts.filter(activity_type__in=['simulated_send', 'email_sent']).count(), 'replies': acts.filter(activity_type='simulated_reply').count(),
            'interested': leads.filter(status='interested').count(), 'meetings': acts.filter(activity_type='meeting').count(),
        },
        'priority_leads': list(leads.filter(priority='high')[:5].values('id','name','company','score','priority','signal_type','why_now')),
        'recent_activity': list(acts.select_related('lead').values('id','activity_type','lead__name','lead__company','created_at')[:8]),
    }
    return Response(data)
