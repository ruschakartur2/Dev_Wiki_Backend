from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from article import serializers
from article import models


class ArticleViewSet(viewsets.ModelViewSet):
    """Viewset to article model"""
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()
