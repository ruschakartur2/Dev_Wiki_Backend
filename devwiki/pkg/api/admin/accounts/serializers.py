from django.contrib.auth import get_user_model
from rest_framework import serializers


class AdminAccountsSerializer(serializers.ModelSerializer):
    """Serializer for manage admin accounts"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'nickname', 'image', 'is_superuser',
                  'is_active', 'is_staff', 'is_banned', 'is_muted',
                  'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


