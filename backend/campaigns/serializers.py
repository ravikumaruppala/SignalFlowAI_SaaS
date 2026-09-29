from rest_framework import serializers
from .models import Campaign, CampaignLead, SequenceStep

class SequenceStepSerializer(serializers.ModelSerializer):
    campaign_name = serializers.CharField(source="campaign.name", read_only=True)
    class Meta:
        model = SequenceStep
        fields = '__all__'

class CampaignLeadSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    lead_company = serializers.CharField(source='lead.company', read_only=True)
    class Meta:
        model = CampaignLead
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    sequence_steps = SequenceStepSerializer(many=True, read_only=True)
    campaign_leads = CampaignLeadSerializer(many=True, read_only=True)
    stats = serializers.SerializerMethodField()

    def get_stats(self, obj):
        from inbox.models import Activity
        return {
            'leads': obj.campaign_leads.count(),
            'sends': Activity.objects.filter(campaign=obj, activity_type='simulated_send').count(),
            'replies': Activity.objects.filter(campaign=obj, activity_type='simulated_reply').count(),
            'meetings': Activity.objects.filter(campaign=obj, activity_type='meeting').count(),
        }
    class Meta:
        model = Campaign
        fields = ('id','owner','name','description','status','created_at','updated_at','sequence_steps','campaign_leads','stats')
        read_only_fields = ('owner','created_at','updated_at','sequence_steps','campaign_leads','stats')
