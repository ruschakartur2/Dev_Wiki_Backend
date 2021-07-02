from rest_framework import serializers

from api.models import Comment
from api.serializers import users


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'article', 'content', 'reply', 'date_posted']

    def to_representation(self, instance):
        """Function to show author data"""
        self.fields['author'] = users.UserDetailSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)