from rest_framework import serializers

from api.models import Comment, Article
from api.serializers import users
from drf_writable_nested import WritableNestedModelSerializer


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return super().to_representation(data.filter(parent=None))


class RecursiveSerializer(WritableNestedModelSerializer, serializers.Serializer):
    """Recursive serialize comment childrens"""
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    """"""
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'content', 'parent', 'date_posted', 'children']

    def to_representation(self, instance):
        """Function to show author data"""
        self.fields['author'] = users.UserDetailSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)
