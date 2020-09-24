from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Profile

User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')


class AuthUserSerializer(serializers.ModelSerializer):

    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')

        def get_auth_token(self, obj):
            token = Token.objects.create(user=obj)
            return token.key


class EmptySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'password')


class PasswordChangeSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'current_password', 'new_password')

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(
                'Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=300, required=True)
    first_name = serializers.CharField(max_length=300, required=True)
    last_name = serializers.CharField(max_length=300, required=True)
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'password', 'first_name', 'last_name')

    # def validate_email(self, value):
    #   user = User.objects.filter(email= value.email)
    #   if user:
    #     raise serializers.ValidationError("Email is already taken")
    #   return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
