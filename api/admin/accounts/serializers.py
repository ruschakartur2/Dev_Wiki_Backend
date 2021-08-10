from django.contrib.auth import get_user_model
from rest_framework import serializers


class AdminAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
