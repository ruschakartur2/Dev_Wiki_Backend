from rest_framework import serializers
from article import models
from users.serializers import UserDetailSerializer


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to create/update/delete article"""
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'created_at', 'author', 'body', 'history', ]

    def to_representation(self, instance):
        self.fields['author'] = UserDetailSerializer(read_only=True)
        return super(ArticleSerializer, self).to_representation(instance)
