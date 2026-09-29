from rest_framework import serializers
from .models import Lead
from .services import score_breakdown_for_lead

class LeadSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    priority_label = serializers.CharField(source='get_priority_display', read_only=True)
    score_breakdown = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    def get_score_breakdown(self, obj):
        return score_breakdown_for_lead(obj)

    def get_activities(self, obj):
        return list(obj.activities.all().values('id', 'activity_type', 'metadata', 'created_at')[:10])
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ('owner','score','priority','why_now','recommended_action','message_angle','created_at','updated_at')
