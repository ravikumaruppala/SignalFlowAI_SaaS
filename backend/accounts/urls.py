from django.urls import path
from .views import (
    confirm_password_reset_view,
    csrf_view,
    login_view,
    logout_view,
    me_view,
    profile_view,
    register_view,
    request_password_otp_view,
)

urlpatterns = [
    path('csrf/', csrf_view),
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('me/', me_view),
    path('profile/', profile_view),
    path('password/request-otp/', request_password_otp_view),
    path('password/reset/', confirm_password_reset_view),
]
