from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data['email'], validated_data['password'])

        return user
