from django.conf import settings
from django.db import models
from leads.models import Lead

class Campaign(models.Model):
    STATUS_CHOICES = [('draft','Draft'),('active','Active'),('paused','Paused'),('completed','Completed')]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [models.Index(fields=['status'])]
        ordering = ['-created_at']
    def __str__(self): return self.name

class SequenceStep(models.Model):
    CHANNEL_CHOICES = [('email','Email'),('linkedin','LinkedIn'),('whatsapp','WhatsApp')]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='sequence_steps')
    step_number = models.PositiveSmallIntegerField()
    day_offset = models.PositiveSmallIntegerField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='email')
    subject_template = models.CharField(max_length=200)
    body_template = models.TextField()
    class Meta:
        ordering = ['step_number']
        constraints = [models.UniqueConstraint(fields=['campaign','step_number'], name='unique_campaign_step')]

class CampaignLead(models.Model):
    STATUS_CHOICES = [('enrolled','Enrolled'),('active','Active'),('completed','Completed'),('paused','Paused')]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_leads')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='campaign_memberships')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['campaign','lead'], name='unique_campaign_lead')]
