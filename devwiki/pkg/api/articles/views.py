import django_filters.rest_framework
from django.db.models import F
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from pkg.core.utils.permissions import IsOwnerOrReadOnly, IsModer, IsBaned, IsMuted
from pkg.api.articles.serializers import ArticlePublicSerializer, ArticleSerializer, ArticleListSerializer

from pkg.core.models import Article
from rest_framework.reverse import reverse_lazy, reverse


class ArticleViewSet(viewsets.ModelViewSet):
    """View set to article model"""
    queryset = Article.objects.filter(status=1)
    serializer_class = Article

    permission_classes_by_action = {
        'create': [IsAuthenticated and IsBaned or IsMuted],
        'list': [AllowAny],
        'update': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
        'partial_update': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
        'retrieve': [AllowAny and IsBaned],
        'destroy': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = PageNumberPagination

    filterset_fields = ['tags__title', 'author__id']
    search_fields = ['title']
    ordering_fields = ['created_at', 'visits']

    lookup_field = "slug"

    @action(detail=False, methods=['get'])
    def deleted_articles_list(self, request):
        articles = Article.objects.filter(status=2)

        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'patch'])
    def deleted_article(self, request, slug):
        article = Article.objects.get(slug=slug)
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Auto added author of article from authorized user"""
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Override method to auto increment article visits"""
        instance = self.get_object()
        Article.objects.filter(pk=instance.id).update(visits=F('visits') + 1)
        serializer = ArticleSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Ovveride delete to change state of article"""
        article = self.get_object()
        article.status = 2
        article.save()
        reverse_lazy('deleted_article', request=request)
        data = {
            'article_url': reverse('articles/deleted_article', args=[article.slug], request=request)
        }
        return Response(data)

    def get_serializer_class(self):
        """Function to get serializer for viewset action"""
        if self.action == 'list':
            return ArticleListSerializer
        if self.action == 'retrieve' and self.request.user == self.get_object().author:
            return ArticleSerializer
        if self.action == 'partial_update' and self.request.user == self.get_object().author:
            return ArticleSerializer
        return ArticlePublicSerializer

    def get_permissions(self):
        """Fuction to get permisions for viewset action"""
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
