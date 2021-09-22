from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings

from pkg.api.accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer, \
    ProfileSerializer, SocialAuthSerializer, ProfileUpdateSerializer

from rest_framework.authtoken.models import Token

from pkg.core.utils.permissions import IsOwnerOrReadOnly, IsModer


class UserLoginAPIView(ObtainAuthToken):
    """
    Endpoint to login user in system

    """
    serializer_class = UserLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        """
        Endpoint to authenticate user

        @return: user data and user token
        """
        response = super(UserLoginAPIView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = UserDetailSerializer(token.user)
        profile = ProfileSerializer(token.user)
        return Response({'token': token.key,
                         'user': user.data,
                         'profile': profile.data,
                         })


class ManageUserView(viewsets.ModelViewSet):
    """
    Endpoint to user profile system

    """
    serializer_class = UserDetailSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication,
                              authentication.BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    @action(detail=False, methods=['POST', ], permission_classes=[AllowAny])
    def register(self, request):
        """
        Endpoint to create new user in system

        @param request: default request
        @return: new created user
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data['token'] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def get_user(self, request):
        """
        Endpoint to get authenticated user

        @param request: default request
        @return: User data
        """
        user = self.request.user
        if self.request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif self.request.method == 'PATCH':
            serializer = self.serializer_class(user, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Not allowed method', status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def get_profile(self, request):
        """
        Endpoint to get authenticated user profile

        @param request: default request
        @return: user profile data
        """
        user = self.request.user
        if self.request.method == 'GET':
            serializer = ProfileSerializer(user)
            return Response(serializer.data)

        elif self.request.method == 'PATCH':
            serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Not allowed method', status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SocialAuthView(generics.CreateAPIView):
    """
    Endpoint to create github user token

    """
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
