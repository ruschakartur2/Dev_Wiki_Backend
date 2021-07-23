from rest_framework import serializers

from api.accounts.serializers import UserDetailSerializer
from core.models import Comment, Article
from drf_writable_nested import WritableNestedModelSerializer


class RecursiveSerializer(WritableNestedModelSerializer, serializers.Serializer):
    """Recursive serialize comment childrens"""

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    """Comment serializer with nested childrens"""
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'content', 'parent', 'date_posted', 'children']

    def to_representation(self, instance):
        """Function to show author data"""
        self.fields['author'] = UserDetailSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)
