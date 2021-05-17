from django.contrib.auth import get_user_model
from rest_framework import generics

from accounts.serializers import UserRegSerializer


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = UserRegSerializer
    queryset = get_user_model().objects.all()
