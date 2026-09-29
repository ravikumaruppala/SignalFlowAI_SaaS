from rest_framework import serializers
from .models import Payment, Subscription


class PaymentSerializer(serializers.ModelSerializer):
    amount_rupees = serializers.FloatField(read_only=True)
    plan_label = serializers.CharField(source='get_plan_code_display', read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 'plan_code', 'plan_label', 'amount', 'amount_rupees', 'currency',
            'razorpay_order_id', 'razorpay_payment_id', 'status', 'provider_status',
            'created_at', 'updated_at'
        )
        read_only_fields = fields


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_label = serializers.CharField(source='get_plan_code_display', read_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'plan_code', 'plan_label', 'status', 'starts_at', 'ends_at', 'created_at')
        read_only_fields = fields
