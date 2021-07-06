from rest_framework import serializers

from api.models import Comment
from api.serializers import users
from drf_writable_nested import WritableNestedModelSerializer


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ResursiveSerializer(WritableNestedModelSerializer,serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    children = ResursiveSerializer(many=True, required=False)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ['id', 'article', 'content', 'parent', 'date_posted', 'children']

    def to_representation(self, instance):
        """Function to show author data"""
        self.fields['author'] = users.UserDetailSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)
