
# Create your views here.

from rest_framework import viewsets, filters, status
from article import serializers
from article import models
from article.models import Article
from users.serializers import UserDetailSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """Viewset to article model"""
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']



