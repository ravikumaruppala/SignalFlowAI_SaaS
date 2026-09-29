from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('sales_rep', 'Sales Representative'),
        ('manager', 'Sales Manager'),
        ('admin', 'Admin'),
    ]
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales_rep')
    team_name = models.CharField(max_length=120, default='Demo Sales Team')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()  # Custom manager assignment

    def __str__(self):
        return self.email

class PasswordResetOTP(models.Model):
    email = models.EmailField(db_index=True)
    code_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'created_at']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f'{self.email} - {self.created_at}'
