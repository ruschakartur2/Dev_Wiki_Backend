from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated

from api.models import Article
from api.serializers.articles import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """Viewset to article model"""
    serializer_class = ArticleSerializer
    permission_classes = ()
    queryset = Article.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']



