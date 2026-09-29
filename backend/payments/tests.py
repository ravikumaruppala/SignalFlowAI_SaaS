import hashlib
import hmac
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Payment, Subscription


class PaymentFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='payer@example.com',
            password='StrongPass123!',
            full_name='Payment Tester',
            role='sales_rep',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @patch('payments.services.requests.post')
    def test_create_order_uses_server_price(self, mocked_post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {'id': 'order_test_123'}
        mocked_post.return_value = response

        with self.settings(SECRET_KEY='test-secret'):
            with patch.dict('os.environ', {
                'RAZORPAY_KEY_ID': 'rzp_test_key',
                'RAZORPAY_KEY_SECRET': 'test_secret',
                'RAZORPAY_CURRENCY': 'INR',
            }, clear=False):
                api_response = self.client.post('/api/payments/create-order/', {'plan_code': 'starter'}, format='json')

        self.assertEqual(api_response.status_code, 201)
        payment = Payment.objects.get(razorpay_order_id='order_test_123')
        self.assertEqual(payment.amount, 99900)

    def test_signature_verification_activates_subscription(self):
        secret = 'test_secret'
        payment = Payment.objects.create(
            user=self.user,
            plan_code='starter',
            amount=99900,
            currency='INR',
            razorpay_order_id='order_test_456',
        )
        payment_id = 'pay_test_456'
        signature = hmac.new(
            secret.encode(),
            f'{payment.razorpay_order_id}|{payment_id}'.encode(),
            hashlib.sha256,
        ).hexdigest()

        with patch.dict('os.environ', {
            'RAZORPAY_KEY_ID': 'rzp_test_key',
            'RAZORPAY_KEY_SECRET': secret,
            'RAZORPAY_CURRENCY': 'INR',
        }, clear=False), patch('payments.services.requests.get') as mocked_get:
            provider_response = Mock()
            provider_response.status_code = 200
            provider_response.json.return_value = {
                'id': payment_id,
                'order_id': payment.razorpay_order_id,
                'amount': payment.amount,
                'status': 'captured',
            }
            mocked_get.return_value = provider_response
            response = self.client.post('/api/payments/verify/', {
                'razorpay_order_id': payment.razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            }, format='json')

        self.assertEqual(response.status_code, 200)
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'verified')
        self.assertTrue(Subscription.objects.filter(user=self.user, plan_code='starter', status='active').exists())
