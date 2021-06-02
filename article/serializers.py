from rest_framework import serializers
from article import models


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to create/update/delete article"""
    class Meta:
        model = models.Article
        fields = ['title', 'created_at', 'author', 'body', ]
