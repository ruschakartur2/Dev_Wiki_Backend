from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.serializers import users
from rest_framework.authtoken.models import Token


class CreateUserAPIView(generics.CreateAPIView):
    """Create a new user in the system"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = users.UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data['token'] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = users.UserLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        response = super(UserLoginAPIView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        serializer = users.UserDetailSerializer(token.user)
        return Response({'token': token.key,
                         'user': serializer.data,
                         })


class ManageUserView(generics.RetrieveAPIView):
    """Manage the authenticated user"""
    serializer_class = users.UserDetailSerializer
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication,
                              authentication.BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class SocialAuthView(generics.CreateAPIView):
    serializer_class = users.SocialAuthSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)