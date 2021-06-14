from rest_framework import serializers
from article import models
from users.serializers import UserDetailSerializer


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to create/update/delete article"""

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'created_at', 'author', 'body',]

    def to_representation(self, instance):
        self.fields['author'] = UserDetailSerializer(read_only=True)
        return super(ArticleSerializer, self).to_representation(instance)