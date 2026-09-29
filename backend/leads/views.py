from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Lead
from .serializers import LeadSerializer
from .services import calculate_lead_score
from outreach.services import generate_outreach_draft

class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Lead.objects.select_related('owner')
        if self.request.user.role == 'sales_rep':
            qs = qs.filter(owner=self.request.user)
        else:
            qs = qs.filter(owner__team_name=self.request.user.team_name)
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q)|Q(email__icontains=q)|Q(company__icontains=q)|Q(job_title__icontains=q))
        mapping = ('industry','company_size','job_title','status','priority','signal_type')
        for key in mapping:
            if self.request.query_params.get(key):
                qs = qs.filter(**{f'{key}__icontains' if key=='job_title' else key: self.request.query_params.get(key)})
        if self.request.query_params.get('min_score'):
            qs = qs.filter(score__gte=int(self.request.query_params['min_score']))
        if self.request.query_params.get('max_score'):
            qs = qs.filter(score__lte=int(self.request.query_params['max_score']))
        return qs

    def perform_create(self, serializer):
        lead = serializer.save(owner=self.request.user)
        calculate_lead_score(lead)

    @action(detail=True, methods=['post'])
    def score(self, request, pk=None):
        lead = self.get_object()
        result = calculate_lead_score(lead)
        return Response({'lead': LeadSerializer(lead).data, 'scoring': result})

    @action(detail=True, methods=['post'], url_path='generate-email')
    def generate_email(self, request, pk=None):
        lead = self.get_object()
        tone = request.data.get('tone', 'professional')
        draft = generate_outreach_draft(request.user, lead, tone)
        return Response(draft, status=status.HTTP_200_OK)
