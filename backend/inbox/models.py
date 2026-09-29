from django.conf import settings
from django.db import models
from leads.models import Lead
from campaigns.models import Campaign

class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    activity_type = models.CharField(max_length=50)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [models.Index(fields=['created_at']), models.Index(fields=['activity_type'])]
        ordering = ['-created_at']

class InboxReply(models.Model):
    CATEGORY_CHOICES = [('needs_reply','Needs reply'),('interested','Interested'),('not_interested','Not interested'),('follow_up','Follow-up')]
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='inbox_replies')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='inbox_replies')
    body = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='needs_reply')
    simulated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
