from django.shortcuts import render

# Create your views here.
from knox.models import AuthToken
from rest_framework import generics
from rest_framework.response import Response

from accounts.serializers import UserRegSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserRegSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserRegSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
