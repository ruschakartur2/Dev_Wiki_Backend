import django_filters.rest_framework
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.accounts.serializers import UserDetailSerializer
from core.models import Article
from core.permissions import IsOwnerOrReadOnly
from api.articles.serializers import ArticleSerializer, ArticleListSerializer, ArticlePublicSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """View set to article model"""
    serializer_class = ArticleSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny, ],
                                    'update': [IsOwnerOrReadOnly, ],
                                    'partial_update': [IsOwnerOrReadOnly],
                                    'retrieve': [AllowAny],
                                    'destroy': [IsOwnerOrReadOnly], }
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = PageNumberPagination
    search_fields = ['title']
    filterset_fields = ['tags__title', 'author__id']
    try:
        lookup_field = 'slug'
    except:
        lookup_field = 'pk'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Article.objects.filter(pk=instance.id).update(visits=F('visits') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        article.state = 2
        article.save()
        return Response(ArticleSerializer(self.get_object()).data)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        if self.action == 'retrieve' and self.request.user == self.get_object().author:
            return ArticleSerializer
        if self.action == 'partial_update' and self.request.user == self.get_object().author:
            return ArticleSerializer
        return ArticlePublicSerializer

    def dispatch(self, *args, **kwargs):
        return super(ArticleViewSet, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Article.objects.all()

        newest = self.request.query_params.get('new')
        popular = self.request.query_params.get('popular')

        if newest == '1':
            queryset = queryset.order_by('-id')
        if popular == '1':
            queryset = queryset.order_by('-visits')

        return queryset

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
