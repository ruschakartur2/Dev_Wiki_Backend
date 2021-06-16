from rest_framework import serializers

from api.models import Article
from api.serializers import users


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to create/update/delete article"""
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'created_at', 'author', 'body', 'history', ]

    def to_representation(self, instance):
        self.fields['author'] = users.UserDetailSerializer(read_only=True)
        return super(ArticleSerializer, self).to_representation(instance)
