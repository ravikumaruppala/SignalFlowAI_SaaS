from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SequenceStep
from .serializers import SequenceStepSerializer

class SequenceViewSet(viewsets.ModelViewSet):
    serializer_class = SequenceStepSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','patch','head','options']
    def get_queryset(self):
        qs = SequenceStep.objects.select_related('campaign__owner')
        if self.request.user.role == 'sales_rep':
            return qs.filter(campaign__owner=self.request.user)
        return qs.filter(campaign__owner__team_name=self.request.user.team_name)
