from rest_framework import serializers
from pkg.core.models import Tag


class TagsSerializer(serializers.ModelSerializer):
    articles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')

    class Meta:
        model = Tag
        fields = "__all__"
