from django.conf import settings
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    PLAN_CHOICES = [
        ('starter', 'Starter'),
        ('professional', 'Professional'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    plan_code = models.CharField(max_length=30, choices=PLAN_CHOICES)
    amount = models.PositiveIntegerField(help_text='Amount in paise.')
    currency = models.CharField(max_length=3, default='INR')
    razorpay_order_id = models.CharField(max_length=80, unique=True)
    razorpay_payment_id = models.CharField(max_length=80, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    provider_status = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    @property
    def amount_rupees(self):
        return self.amount / 100

    def __str__(self):
        return f'{self.user.email} - {self.plan_code} - {self.status}'


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('business', 'Business'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan_code = models.CharField(max_length=30, choices=PLAN_CHOICES, default='free')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(null=True, blank=True)
    source_payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['plan_code']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.plan_code}'
