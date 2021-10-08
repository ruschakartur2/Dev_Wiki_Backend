from rest_framework import serializers

from pkg.articles.models import Article, Tag, Comment

from pkg.users.api.serializers import UserDetailSerializer


class CommentRecursiveSerializer(serializers.Serializer):
    """Recursive serialize comment childrens"""

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

    class Meta:
        model = Comment
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer to CRUD articles if not author"""

    class Meta:
        model = Article
        fields = ['id', 'slug', 'title', 'created_at', 'updated_at',
                  'visits', 'body', 'status', 'tags', 'author']
        read_only_fields = ('created_at', 'updated_at')

    author = UserDetailSerializer(read_only=True)
    visits = serializers.SlugRelatedField(slug_field='number', read_only=True)


class ArticleCreateUpdateSerializer(ArticleListSerializer):
    class Meta:
        model = Article
        fields = ArticleListSerializer.Meta.fields + ['update_tags']

    update_tags = serializers.ListField(
        child=serializers.CharField(max_length=30, required=False),
        write_only=True, required=False)

    def add_tags(self, tag_names):
        tags = []
        request = self.context['request']
        for name in tag_names:
            if request.method == 'get':
                tag = Tag.objects.get(name=name)
            else:
                tag = Tag.objects.get_or_create(name=name, author=request.user)
            tags.append(tag)
        return tags

    def create(self, validated_data):
        instance = super().create(validated_data)
        if 'update_tags' in validated_data:
            instance.tags.set(self.add_tags(validated_data.pop('update_tags')))
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'update_tags' in validated_data:
            instance.tags.set(self.add_tags(validated_data.pop('update_tags')))
        return instance


class ArticleCommentSerializer(serializers.ModelSerializer):
    """Comment serializer with nested childrens"""

    class Meta:
        model = Comment
        fields = ['id', 'article', 'content', 'parent', 'created_at',
                  'status', 'updated_at', 'children', 'author']
        read_only_fields = ['children', 'created_at', 'updated_at', ]

    created_at = serializers.DateTimeField(format="%d, %b %Y - %H:%M", required=False)
    updated_at = serializers.DateTimeField(format="%d, %b %Y - %H:%M", required=False)
    children = CommentRecursiveSerializer(many=True, required=False)
    author = UserDetailSerializer(read_only=True)


class ArticleTagSerializer(serializers.ModelSerializer):
    """
    Tag serializer

    """

    class Meta:
        model = Tag
        fields = ['id', 'name', 'author']
