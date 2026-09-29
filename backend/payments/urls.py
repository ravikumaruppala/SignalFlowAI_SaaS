from django.urls import path
from .views import create_order_view, current_subscription_view, payment_history_view, verify_payment_view

urlpatterns = [
    path('create-order/', create_order_view),
    path('verify/', verify_payment_view),
    path('subscription/', current_subscription_view),
    path('history/', payment_history_view),
]
