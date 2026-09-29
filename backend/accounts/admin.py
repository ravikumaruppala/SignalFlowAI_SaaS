from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PasswordResetOTP, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ('email',)
    list_display = ('email', 'full_name', 'role', 'team_name', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Profile', {'fields': ('full_name', 'role', 'team_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'full_name', 'role', 'password1', 'password2', 'is_staff')}),
    )


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'expires_at', 'attempts', 'used_at', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('code_hash',)
