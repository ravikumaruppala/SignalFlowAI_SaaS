from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment, Subscription
from .serializers import PaymentSerializer, SubscriptionSerializer
from .services import PLANS, activate_subscription, create_razorpay_order, verify_razorpay_payment


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_view(request):
    plan_code = str(request.data.get('plan_code', '')).lower().strip()
    payment, key_id = create_razorpay_order(request.user, plan_code)
    return Response({
        'payment': PaymentSerializer(payment).data,
        'key_id': key_id,
        'name': 'SignalFlow AI',
        'description': f'{PLANS[plan_code]["name"]} plan - 30 days',
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment_view(request):
    payment, provider_status = verify_razorpay_payment(
        request.user,
        request.data.get('razorpay_order_id'),
        request.data.get('razorpay_payment_id'),
        request.data.get('razorpay_signature'),
    )
    subscription = Subscription.objects.filter(user=request.user, status='active').first()
    return Response({
        'detail': 'Payment verified successfully and plan activated.',
        'payment': PaymentSerializer(payment).data,
        'subscription': SubscriptionSerializer(subscription).data if subscription else None,
        'provider_status': provider_status,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_subscription_view(request):
    subscription = Subscription.objects.filter(user=request.user, status='active').first()
    if subscription and subscription.ends_at and subscription.ends_at <= timezone.now():
        subscription.status = 'expired'
        subscription.save(update_fields=['status', 'updated_at'])
        subscription = None

    if not subscription:
        # Free is the default plan when no paid subscription exists.
        payload = {
            'plan_code': 'free',
            'plan_label': 'Free',
            'status': 'active',
            'starts_at': None,
            'ends_at': None,
        }
        return Response(payload)
    return Response(SubscriptionSerializer(subscription).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history_view(request):
    payments = Payment.objects.filter(user=request.user)[:20]
    return Response(PaymentSerializer(payments, many=True).data)
