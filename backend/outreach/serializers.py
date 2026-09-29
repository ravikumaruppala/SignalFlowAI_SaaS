from rest_framework import serializers
from .models import OutreachDraft
class OutreachDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutreachDraft
        fields = '__all__'
        read_only_fields = ('user', 'source', 'created_at')
