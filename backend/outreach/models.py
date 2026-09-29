from django.conf import settings
from django.db import models
from leads.models import Lead

class OutreachDraft(models.Model):
    TONES = [('professional','Professional'),('friendly','Friendly'),('concise','Concise')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outreach_drafts')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='outreach_drafts')
    tone = models.CharField(max_length=20, choices=TONES, default='professional')
    subject = models.CharField(max_length=250)
    body = models.TextField()
    cta = models.CharField(max_length=250)
    source = models.CharField(max_length=30, default='fallback')
    created_at = models.DateTimeField(auto_now_add=True)
