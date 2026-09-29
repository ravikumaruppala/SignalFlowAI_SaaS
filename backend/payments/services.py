import hashlib
import hmac
import os
import uuid
from datetime import timedelta

import requests
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError

from .models import Payment, Subscription

# Prices are deliberately illustrative for the BusinessLabs assessment/demo.
PLANS = {
    'starter': {
        'name': 'Starter',
        'amount_rupees': 999,
        'currency': 'INR',
    },
    'professional': {
        'name': 'Professional',
        'amount_rupees': 2499,
        'currency': 'INR',
    },
}


def _config():
    key_id = os.getenv('RAZORPAY_KEY_ID', '').strip()
    key_secret = os.getenv('RAZORPAY_KEY_SECRET', '').strip()
    currency = os.getenv('RAZORPAY_CURRENCY', 'INR').strip().upper() or 'INR'
    return key_id, key_secret, currency


def ensure_configured():
    key_id, key_secret, currency = _config()
    if not key_id or not key_secret:
        raise ValidationError('Razorpay is not configured. Add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET to backend/.env.')
    return key_id, key_secret, currency


def create_razorpay_order(user, plan_code):
    plan = PLANS.get(plan_code)
    if not plan:
        raise ValidationError('Select a paid plan: Starter or Professional.')

    key_id, key_secret, env_currency = ensure_configured()
    currency = plan['currency'] or env_currency
    amount = plan['amount_rupees'] * 100
    receipt = f'sf_{user.id}_{uuid.uuid4().hex[:20]}'

    payload = {
        'amount': amount,
        'currency': currency,
        'receipt': receipt,
        'notes': {
            'user_id': str(user.id),
            'email': user.email,
            'plan_code': plan_code,
        },
    }

    try:
        response = requests.post(
            'https://api.razorpay.com/v1/orders',
            auth=(key_id, key_secret),
            json=payload,
            timeout=20,
        )
    except requests.RequestException as exc:
        raise APIException(f'Unable to reach Razorpay: {exc}') from exc

    if response.status_code >= 400:
        detail = response.text[:500]
        raise APIException(f'Razorpay order creation failed: {detail}')

    try:
        data = response.json()
    except ValueError as exc:
        raise APIException('Razorpay returned an invalid response.') from exc

    payment = Payment.objects.create(
        user=user,
        plan_code=plan_code,
        amount=amount,
        currency=currency,
        razorpay_order_id=data['id'],
        status='created',
    )
    return payment, key_id


def verify_razorpay_payment(user, order_id, payment_id, signature):
    if not all([order_id, payment_id, signature]):
        raise ValidationError('razorpay_order_id, razorpay_payment_id and razorpay_signature are required.')

    key_id, key_secret, _ = ensure_configured()
    try:
        payment = Payment.objects.get(razorpay_order_id=order_id, user=user)
    except Payment.DoesNotExist as exc:
        raise ValidationError('Payment order was not found for the current user.') from exc

    if payment.status == 'verified':
        return payment, None

    message = f'{payment.razorpay_order_id}|{payment_id}'
    expected = hmac.new(key_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        payment.status = 'failed'
        payment.provider_status = 'signature_mismatch'
        payment.save(update_fields=['status', 'provider_status', 'updated_at'])
        raise ValidationError('Payment signature verification failed.')

    provider_status = ''
    try:
        response = requests.get(
            f'https://api.razorpay.com/v1/payments/{payment_id}',
            auth=(key_id, key_secret),
            timeout=20,
        )
        if response.status_code < 400:
            info = response.json()
            provider_status = info.get('status', '')
            if info.get('order_id') and info.get('order_id') != payment.razorpay_order_id:
                raise ValidationError('Payment order does not match the stored order.')
            provider_amount = info.get('amount')
            if provider_amount is not None and int(provider_amount) != payment.amount:
                raise ValidationError('Payment amount does not match the selected plan.')
            if provider_status and provider_status not in ('captured', 'authorized'):
                payment.status = 'failed'
                payment.provider_status = provider_status
                payment.save(update_fields=['status', 'provider_status', 'updated_at'])
                raise ValidationError(f'Razorpay payment status is {provider_status}; the plan was not activated.')
    except requests.RequestException:
        # The checkout signature is still verified. Provider status is left blank if the details endpoint is unavailable.
        provider_status = 'signature_verified'
    except ValueError:
        provider_status = 'signature_verified'

    payment.razorpay_payment_id = payment_id
    payment.razorpay_signature = signature
    payment.provider_status = provider_status or 'signature_verified'
    payment.status = 'verified'
    payment.save(update_fields=[
        'razorpay_payment_id', 'razorpay_signature', 'provider_status', 'status', 'updated_at'
    ])

    activate_subscription(payment)
    return payment, provider_status


@transaction.atomic
def activate_subscription(payment):
    now = timezone.now()
    Subscription.objects.filter(user=payment.user, status='active').update(status='expired', ends_at=now)
    Subscription.objects.create(
        user=payment.user,
        plan_code=payment.plan_code,
        status='active',
        starts_at=now,
        ends_at=now + timedelta(days=30),
        source_payment=payment,
    )
