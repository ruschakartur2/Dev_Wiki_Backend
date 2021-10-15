from rest_framework import viewsets
from rest_framework import authentication, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from pkg.articles.permissions import IsBaned, IsMuted, IsModer, IsOwnerOrReadOnly
from pkg.articles.models import Article, Tag, Comment, ArticleVisits, ArticleRating
from .serializers import ArticleListSerializer, ArticleCreateUpdateSerializer, \
    ArticleCommentSerializer, ArticleTagSerializer, ArticleRatingSerializer


class PublicArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication, ]

    def get_permissions(self):
        """
        Method to get permissions per action
        @return: permissions
        """
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class ArticleViewSet(PublicArticleViewSet):
    """
    Manage articles in database
    """
    queryset = Article.objects.all()
    lookup_field = 'slug'

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsOwnerOrReadOnly or IsAdminUser],
        'partial_update': [IsOwnerOrReadOnly or IsAdminUser],
        'retrieve': [AllowAny],
        'destroy': [IsOwnerOrReadOnly or IsAdminUser],
    }

    def retrieve(self, request, *args, **kwargs):
        """
              Endpoint to retrieve and auto increment visits
              If user read article, field visits auto increments by 1
              @return: Response with article and updated visits field
        """
        instance = self.get_object()
        visits = ArticleVisits.objects.get(article__id=instance.id)
        visits.number += 1
        visits.save()
        serializer = ArticleListSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Create a new article"""
        serializer.save(author=self.request.user, visits=ArticleVisits.objects.create(number=1))

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'create' or self.action == 'update':
            return ArticleCreateUpdateSerializer

        return ArticleListSerializer

    @action(detail=True, methods=['get'])
    def article_comments(self, request, pk):
        """
        Endpoint to get article comments

        @param pk: Article id
        @return:
        """
        comments = Comment.objects.get(article=pk)
        serializer = ArticleCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        articles = self.queryset.order_by('visits')
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def newest(self, request):
        articles = self.queryset.order_by('-id')
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def vote(self, request, slug):
        """
        Endpoint to rating vote

        @param request:
        @param slug:
        @return:
        """
        article = self.get_object()
        rating = ArticleRating.objects.filter(user=self.request.user, article=article)
        star = int(request.data['rating'])
        if 0 <= star <= 5:
            if rating:
                rating.update(star=star)
            else:
                ArticleRating.objects.create(user=self.request.user, article=article, star=star)

            serializer = ArticleListSerializer(article)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid number, select value from 0 to 5'})


class ArticleRatingViewSet(PublicArticleViewSet):
    queryset = ArticleRating.objects.all()
    serializer_class = ArticleRatingSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsOwnerOrReadOnly or IsAdminUser],
        'partial_update': [IsOwnerOrReadOnly or IsAdminUser],
        'retrieve': [AllowAny],
        'destroy': [IsOwnerOrReadOnly or IsAdminUser],
    }

    def perform_create(self, serializer):
        """
        Create a new vote
        """
        serializer.save(user=self.request.user)


class ArticleCommentViewSet(PublicArticleViewSet):
    """
    Manage comments in database
    """
    queryset = Comment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsOwnerOrReadOnly or IsAdminUser],
        'partial_update': [IsOwnerOrReadOnly or IsAdminUser],
        'retrieve': [AllowAny],
        'destroy': [IsOwnerOrReadOnly or IsAdminUser],
    }

    def perform_create(self, serializer):
        """
        Create a new comment
        """
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        List of parent components
        """
        if self.action == 'list':
            return self.queryset.filter(parent__isnull=True)
        return self.queryset


class ArticleTagViewSet(PublicArticleViewSet):
    """
    Manage tags in database
    """
    queryset = Tag.objects.all()
    serializer_class = ArticleTagSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsOwnerOrReadOnly or IsAdminUser],
        'partial_update': [IsOwnerOrReadOnly or IsAdminUser],
        'retrieve': [AllowAny],
        'destroy': [IsOwnerOrReadOnly or IsAdminUser],
    }
    authentication_classes = [authentication.TokenAuthentication, ]

    def perform_create(self, serializer):
        """
        Create a new tag
        """
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def without_articles(self, request):
        tags = Tag.objects.filter(article__isnull=True)
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)
