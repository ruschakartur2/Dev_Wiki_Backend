from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer, \
    PublicProfileSerializer, PrivateProfileSerializer, SocialAuthSerializer
from pkg.articles.models import Article, Comment, Tag
from pkg.articles.api.serializers import ArticleListSerializer, ArticleCommentSerializer, ArticleTagSerializer


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
        profile = PrivateProfileSerializer(token.user)
        return Response({'token': token.key,
                         'profile': profile.data,
                         'user': user.data,
                         })


class ManageUserView(viewsets.ModelViewSet):
    """
    Endpoint to user profile system

    """
    serializer_class = UserDetailSerializer
    queryset = get_user_model().objects.all()

    authentication_classes = [authentication.TokenAuthentication, ]

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def my_profile(self, request):
        """
        Endpoint to get authenticated private user profile

        @return: user profile
        """
        serializer = PrivateProfileSerializer(self.request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_profile(self, request, pk):
        """
        Endpoint to get user profile

        @param pk: User id
        @return: User profile
        """
        profile = get_user_model().objects.get(id=pk)
        serializer = PublicProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_articles(self, request, pk):
        """
        Endpoint to get user articles

        @param pk: User id
        @return: User articles
        """
        articles = Article.objects.filter(author=pk)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_comments(self, request, pk):
        """
        Endpoint to get user comments

        @param pk: User id
        @return: User comments
        """
        comments = Comment.objects.filter(author=pk)
        serializer = ArticleCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_tags(self, request, pk):
        """
        Endpoint to get user tags

        @param pk: User id
        @return:
        """
        tags = Tag.objects.filter(author=pk)
        serializer = ArticleTagSerializer(tags, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post', ])
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
        profile = PrivateProfileSerializer(token.user)

        headers = self.get_success_headers(serializer.data)
        return Response({
            'token': token.key,
            'profile': profile.data,
            'user': serializer.data,
        }, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'])
    def github_login(self, request):
        """
        Endpoint to login user via github

        @return: user data
        """
        token = SocialAuthSerializer(data=request.data)
        token.is_valid(raise_exception=True)
        profile = PrivateProfileSerializer(token.user)
        user = UserDetailSerializer(token.user)
        self.perform_create(token)
        headers = self.get_success_headers(token.data)
        return Response(
            {'token': token.data['auth_token'],
             'profile': profile.data,
             'user': user.data
             }, status=status.HTTP_200_OK, headers=headers)
