import secrets
from datetime import timedelta

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import PasswordResetOTP, User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_view(request):
    return JsonResponse({'detail': 'CSRF cookie set', 'csrfToken': get_token(request)})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    login(request, user)
    request.session.set_expiry(0)
    return Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    remember_me = bool(serializer.validated_data.get('remember_me', False))
    login(request, user)
    # Browser-session cookie when unchecked; 30-day persistent session when checked.
    request.session.set_expiry(60 * 60 * 24 * 30 if remember_me else 0)
    return Response({'user': UserSerializer(user).data, 'remember_me': remember_me})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'detail': 'Logged out successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response({'user': UserSerializer(request.user).data})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    if 'full_name' in request.data:
        user.full_name = request.data['full_name']
    if 'team_name' in request.data:
        user.team_name = request.data['team_name']
    user.save(update_fields=['full_name', 'team_name'])
    return Response({'user': UserSerializer(user).data})


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_otp_view(request):
    email = str(request.data.get('email', '')).strip().lower()
    if not email:
        return Response({'detail': 'Enter your email address.'}, status=400)

    generic_message = 'If an active account exists for this email, a 6-digit OTP has been sent.'
    user = User.objects.filter(email__iexact=email, is_active=True).first()
    if not user:
        return Response({'detail': generic_message})

    now = timezone.now()
    recent = PasswordResetOTP.objects.filter(
        email__iexact=email,
        created_at__gte=now - timedelta(seconds=60),
    ).exists()
    if recent:
        return Response({'detail': 'An OTP was already sent recently. Please wait a minute before requesting another.'})

    otp = f'{secrets.randbelow(1_000_000):06d}'
    PasswordResetOTP.objects.filter(
        email__iexact=email,
        used_at__isnull=True,
    ).update(used_at=now)

    reset = PasswordResetOTP.objects.create(
        email=email,
        code_hash=make_password(otp),
        expires_at=now + timedelta(minutes=10),
    )

    subject = 'Your SignalFlow AI password reset OTP'
    body = (
        f'Hi {user.full_name or "there"},\n\n'
        f'Your SignalFlow AI password reset OTP is: {otp}\n\n'
        'This OTP expires in 10 minutes. If you did not request a password reset, '
        'you can ignore this email.\n\n'
        'SignalFlow AI'
    )

    try:
        sent = send_mail(
            subject,
            body,
            None,
            [user.email],
            fail_silently=False,
        )
    except Exception as exc:
        reset.delete()
        return Response(
            {'detail': f'Unable to send OTP email. Check Gmail SMTP settings in backend/.env. ({exc})'},
            status=503,
        )

    if sent != 1:
        reset.delete()
        return Response({'detail': 'OTP email could not be sent. Check Gmail SMTP configuration.'}, status=503)

    return Response({'detail': generic_message, 'expires_in_seconds': 600})


@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def confirm_password_reset_view(request):
    email = str(request.data.get('email', '')).strip().lower()
    otp = str(request.data.get('otp', '')).strip()
    password = str(request.data.get('new_password', ''))

    if not email or not otp or not password:
        return Response({'detail': 'Email, OTP, and new password are required.'}, status=400)
    if not otp.isdigit() or len(otp) != 6:
        return Response({'detail': 'OTP must be a 6-digit code.'}, status=400)

    try:
        validate_password(password)
    except Exception as exc:
        messages = [str(error) for error in getattr(exc, 'error_list', [exc])]
        return Response({'detail': messages}, status=400)

    now = timezone.now()
    reset = PasswordResetOTP.objects.filter(
        email__iexact=email,
        used_at__isnull=True,
        expires_at__gt=now,
        attempts__lt=5,
    ).order_by('-created_at').first()
    if not reset:
        return Response({'detail': 'OTP is invalid or expired. Request a new OTP.'}, status=400)

    if not check_password(otp, reset.code_hash):
        reset.attempts += 1
        reset.save(update_fields=['attempts'])
        remaining = max(0, 5 - reset.attempts)
        return Response({'detail': f'Invalid OTP. {remaining} attempt(s) remaining.'}, status=400)

    user = User.objects.filter(email__iexact=email, is_active=True).first()
    if not user:
        return Response({'detail': 'Unable to reset this account.'}, status=400)

    user.set_password(password)
    user.save(update_fields=['password'])
    reset.used_at = now
    reset.save(update_fields=['used_at'])
    return Response({'detail': 'Password reset successfully. You can now sign in.'})
