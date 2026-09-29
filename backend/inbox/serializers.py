from rest_framework import serializers
from .models import Activity, InboxReply
class InboxReplySerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    lead_company = serializers.CharField(source='lead.company', read_only=True)
    class Meta:
        model = InboxReply
        fields = '__all__'
        read_only_fields = ('created_at','simulated')
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
