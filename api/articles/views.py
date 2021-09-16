import django_filters.rest_framework
from django.db.models import F
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from core.models import Article
from core.utils.permissions import IsOwnerOrReadOnly, IsModer, IsBaned, IsMuted
from api.articles.serializers import ArticleSerializer, ArticleListSerializer, ArticlePublicSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """View set to article model"""
    queryset = Article.objects.filter(status=1)
    serializer_class = ArticleSerializer

    permission_classes_by_action = {
        'create': [IsAuthenticated and IsBaned or IsMuted],
        'list': [AllowAny and IsBaned],
        'update': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
        'partial_update': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
        'retrieve': [AllowAny and IsBaned],
        'destroy': [IsOwnerOrReadOnly and IsAdminUser and IsModer],
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = PageNumberPagination

    search_fields = ['title']
    ordering_fields = ['created_at', 'visits']
    filterset_fields = ['tags__title', 'author__id']

    lookup_field = "slug"

    def perform_create(self, serializer):
        """Auto added author of article from authorized user"""
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Override method to auto increment article visits"""
        instance = self.get_object()
        Article.objects.filter(pk=instance.id).update(visits=F('visits') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Ovveride delete to change state of article"""
        article = self.get_object()
        article.status = 2
        article.save()
        return Response(ArticleSerializer(self.get_object()).data)

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
