from rest_framework import serializers
from rest_framework.fields import SlugField

from api.models import Article
from api.serializers import users


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to create/update/delete article"""

    previous_version = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'slug', 'title', 'created_at', 'previous_version', 'body', ]
        lookup_field = 'slug'

    def to_representation(self, instance):
        self.fields['author'] = users.UserDetailSerializer(read_only=True)
        return super(ArticleSerializer, self).to_representation(instance)

    def get_previous_version(self, obj):
        if len(obj.previous_version.all())>1:
            h = obj.previous_version.all().values('id', 'title', 'body', 'created_at')[1]
            return h
        return []
