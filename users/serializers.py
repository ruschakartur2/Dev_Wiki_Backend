import requests
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from social_core.exceptions import MissingBackend
from social_django.utils import load_strategy, load_backend
from social_django.views import NAMESPACE


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True,
                         'min_length': 5}
        }

    def create(self, validated_data):
        """Create a user with encrypted password and return it"""
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user profile  """

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'date_joined']


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ('auth_token',)


class SocialAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    provider = serializers.CharField()

    default_error_messages = {
        'invalid_provider': _('invalid auth provider'),
    }

    def __init__(self, *args, **kwargs):
        self.user = None
        super(SocialAuthSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
