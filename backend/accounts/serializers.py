from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    role_label = serializers.CharField(source='get_role_display', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'role_label', 'team_name')

from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'role', 'team_name')

    def create(self, validated_data):
        role = validated_data.pop('role', 'sales_rep')
        if role == 'admin':
            role = 'sales_rep'
            
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        return User.objects.create_user(
            email=email,
            password=password,
            role=role,
            **validated_data
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)
    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')
        attrs['user'] = user
        return attrs
