from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings

from pkg.api.accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer, \
    ProfileSerializer, SocialAuthSerializer

from rest_framework.authtoken.models import Token

from pkg.core.utils.permissions import IsOwnerOrReadOnly, IsModer


class CreateUserAPIView(generics.CreateAPIView):
    """View to create a new user in the system"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Create and serialize new user and user's token"""
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
    """View to login user in system"""
    serializer_class = UserLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        """Function to authenticate user and return user's data and user's token """
        response = super(UserLoginAPIView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = UserDetailSerializer(token.user)
        profile = ProfileSerializer(token.user)
        return Response({'token': token.key,
                         'user': user.data,
                         'profile': profile.data,
                         })


class ManageUserView(viewsets.ModelViewSet):
    """View to user profile system"""
    serializer_class = UserDetailSerializer
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication,
                              authentication.BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class ProfileView(viewsets.ModelViewSet):
    """View to public profile"""
    serializer_class = ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication,
                              authentication.BasicAuthentication]

    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAdminUser and IsModer],
        'update': [IsOwnerOrReadOnly and IsAdminUser],
        'partial_update': [IsOwnerOrReadOnly and IsAdminUser],
        'retrieve': [AllowAny],
        'destroy': [IsOwnerOrReadOnly and IsAdminUser],
    }

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class SocialAuthView(generics.CreateAPIView):
    """View to authentication user with github"""
    serializer_class = SocialAuthSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        token = self.get_serializer(data=request.data)
        token.is_valid(raise_exception=True)
        profile = ProfileSerializer(token.user)
        user = UserDetailSerializer(token.user)
        self.perform_create(token)
        headers = self.get_success_headers(token.data)
        return Response({'token': token.data['auth_token'],
                         'profile': profile.data,
                         'user': user.data
                         }, status=status.HTTP_200_OK, headers=headers)
