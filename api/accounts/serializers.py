import requests
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from social_core.exceptions import MissingBackend
from social_django.utils import load_strategy, load_backend


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer to register new user with token"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")

    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        def __init__(self, *args, **kwargs):
            """Initialize serializer"""
            super(UserLoginSerializer, self).__init__(*args, **kwargs)
            self.user = None

        self.user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not self.user:
            """Statement to check result of authenticate"""
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = self.user
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user detail  """

    class Meta:
        model = get_user_model()
        fields = ['id', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'nickname', 'is_active', 'image']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TokenSerializer(serializers.ModelSerializer):
    """Serializer to authentication token"""
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ('auth_token',)


class SocialAuthSerializer(serializers.Serializer):
    """Serializer to authentication user with github"""
    access_token = serializers.CharField()
    provider = serializers.CharField()

    default_error_messages = {
        'invalid_provider': _('invalid auth provider'),
    }

    def __init__(self, *args, **kwargs):
        """Initialize serializer"""
        self.user = None
        super(SocialAuthSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        """Validate and authenticate user with OAuth providers"""
        provider = attrs.get('provider')
        access_token = attrs.get('access_token')
        strategy = load_strategy(request=self.context['request'])

        try:
            backend = load_backend(strategy, provider, reverse('social:complete', args=(provider,)))
        except MissingBackend:
            self.fail('invalid_provider')

        try:
            self.user = backend.do_auth(access_token=access_token)
        except requests.HTTPError as e:
            raise serializers.ValidationError(e.response.text)

        return super(SocialAuthSerializer, self).validate(attrs)

    def create(self, validated_data):
        return self.user

    def to_representation(self, instance):
        token, _ = Token.objects.get_or_create(user=self.user)
        return TokenSerializer(instance=token, context=self.context).data
