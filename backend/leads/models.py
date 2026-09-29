from django.conf import settings
from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'), ('contacted', 'Contacted'), ('follow_up', 'Follow-up'),
        ('interested', 'Interested'), ('not_interested', 'Not Interested'), ('meeting', 'Meeting'),
    ]
    PRIORITY_CHOICES = [('high','High'),('medium','Medium'),('low','Low')]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=160)
    job_title = models.CharField(max_length=120)
    industry = models.CharField(max_length=120)
    company_size = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    score = models.PositiveIntegerField(default=0)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    signal_type = models.CharField(max_length=80, default='Growth signal')
    signal_description = models.TextField(default='')
    why_now = models.TextField(default='')
    recommended_action = models.TextField(default='')
    message_angle = models.TextField(default='')
    contact_available = models.BooleanField(default=True)
    company_growth = models.BooleanField(default=False)
    hiring_signal = models.BooleanField(default=False)
    leadership_change = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']), models.Index(fields=['status']), models.Index(fields=['score']),
            models.Index(fields=['industry']), models.Index(fields=['company_size']),
        ]
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f'{self.name} - {self.company}'
