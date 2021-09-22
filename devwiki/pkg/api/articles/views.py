import django_filters.rest_framework
from django.db.models import F
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from pkg.core.utils.permissions import IsOwnerOrReadOnly, IsModer, IsBaned, IsMuted
from pkg.api.articles.serializers import ArticlePublicSerializer, ArticleSerializer, ArticleListSerializer

from pkg.core.models import Article, Comment

from pkg.api.comments.serializers import CommentSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """View set to article model"""
    queryset = Article.objects.filter(status=1)
    serializer_class = ArticlePublicSerializer

    permission_classes_by_action = {
        'create': [IsAuthenticated and IsBaned or IsMuted],
        'list': [AllowAny],
        'update': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
        'partial_update': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
        'retrieve': [AllowAny and IsBaned],
        'destroy': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
    }

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = PageNumberPagination

    filterset_fields = ['tags__title', 'author__id']
    search_fields = ['title']

    lookup_field = "slug"

    def perform_create(self, serializer):
        """
        Method to auto add author of article from authorized user

        @return serializer with author
        """
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint to retrieve and auto increment visits

        If user read article, field visits auto increments by 1

        @return: Response with article and updated visits field
        """
        instance = self.get_object()
        Article.objects.filter(pk=instance.id).update(visits=F('visits') + 1)
        serializer = ArticleSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Endpoint to change status of article by 'Deleted'

        @return: Response with message
        """
        article = self.get_object()
        article.status = 2
        article.save()

        return Response({'message': 'Article successful deleted'}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        """
        Method to get serializer per action

        @return: serializer
        """
        if self.action == 'list':
            return ArticleListSerializer
        if self.action == 'retrieve' and self.request.user == self.get_object().author:
            return ArticleSerializer
        if self.action == 'partial_update' and self.request.user == self.get_object().author:
            return ArticleSerializer
        return ArticlePublicSerializer

    def get_permissions(self):
        """
        Method to get permissions per action

        @return: permissions
        """
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['get'])
    def article_comments(self, request, slug):
        """
        Endpoint for comments to selected article

        @param slug: article slug
        @param request: request
        @return: list of comments
        """
        article = Article.objects.get(slug=slug, status=1)
        comments = Comment.objects.filter(article=article.id, status=1)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def deleted_articles_list(self, request):
        """
        Endpoint for get deleted articles

        @param request: default request
        @return: Response with list of deleted articles
        """
        articles = Article.objects.filter(status=2)
        page = self.paginate_queryset(articles)

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'patch'])
    def deleted_article(self, request, slug):
        """
        Endpoint for get and patch current deleted article

        @param request: default request
        @param slug: article slug
        @return:
            if get - comment data
            if patch - new comment data
        """
        article = Article.objects.get(slug=slug, status=2)
        if self.request.method == 'GET':
            serializer = self.get_serializer(article)
            return Response(serializer.data)
        elif self.request.method == 'PATCH':
            serializer = self.serializer_class(article, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Not allowed method', status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'])
    def new_articles(self, request):
        """
        Endpoint to get list of newest articles

        @param request: default request
        @return: list of articles sorted by create time
        """
        articles = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Endpoint to get list of popular articles

        @param request: default request
        @return: list of articles sorted by visits
        """
        articles = self.get_queryset().order_by('-visits')
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
