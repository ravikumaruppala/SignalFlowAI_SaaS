from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import InboxReply, Activity
from .serializers import InboxReplySerializer
from leads.models import Lead

class InboxReplyViewSet(viewsets.ModelViewSet):
    serializer_class = InboxReplySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','patch','head','options']
    def get_queryset(self):
        qs = InboxReply.objects.select_related('lead','campaign')
        if self.request.user.role == 'sales_rep':
            return qs.filter(lead__owner=self.request.user)
        return qs.filter(lead__owner__team_name=self.request.user.team_name)
    def partial_update(self, request, *args, **kwargs):
        reply = self.get_object()
        category = request.data.get('category')
        if category:
            reply.category = category
            reply.save(update_fields=['category'])
            status_map = {'interested':'interested','not_interested':'not_interested','follow_up':'follow_up'}
            if category in status_map:
                lead = reply.lead
                lead.status = status_map[category]
                lead.save(update_fields=['status','updated_at'])
                Activity.objects.create(user=request.user, lead=lead, campaign=reply.campaign, activity_type='reply_status_updated', metadata={'category':category})
        return super().partial_update(request, *args, **kwargs)
