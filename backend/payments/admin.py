from django.contrib import admin
from .models import Payment, Subscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan_code', 'amount', 'currency', 'status', 'razorpay_order_id', 'created_at')
    list_filter = ('status', 'plan_code', 'currency')
    search_fields = ('user__email', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan_code', 'status', 'starts_at', 'ends_at', 'created_at')
    list_filter = ('status', 'plan_code')
    search_fields = ('user__email',)
