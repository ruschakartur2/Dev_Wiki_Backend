from rest_framework import serializers

from pkg.api.accounts.serializers import UserDetailSerializer

from pkg.core.models import Article, Tag


class ArticlePublicSerializer(serializers.ModelSerializer):
    """Serializer to CRUD Articles if not author"""
    created_at = serializers.DateTimeField(format="%d, %b %Y - %H:%M", required=False)
    updated_at = serializers.DateTimeField(format="%d, %b %Y - %H:%M", required=False, default=None)

    tags = serializers.SlugRelatedField(many=True,
                                        slug_field='title',
                                        read_only=True)
    update_tags = serializers.ListField(
        child=serializers.CharField(max_length=30),
        write_only=True, )

    class Meta:
        model = Article
        fields = ['id', 'slug', 'title', 'created_at', 'updated_at', 'visits', 'body', 'status', 'tags', 'update_tags']
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'update_tags': {
                'allow_empty': True
            }
        }

    def create(self, validated_data):
        tag_names = validated_data.pop('update_tags')
        instance = super().create(validated_data)
        tags = []
        for title in tag_names:
            print(title)
            tag, created = Tag.objects.get_or_create(title=title)
            tags.append(tag)
        instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('update_tags')
        instance = super().update(instance, validated_data)
        tags = []
        for title in tag_names:
            tag, created = Tag.objects.get_or_create(title=title)
            tags.append(tag)
        instance.tags.set(tags)
        return instance

    def to_representation(self, instance):
        """Function to show author data"""
        self.fields['author'] = UserDetailSerializer(read_only=True)
        return super(ArticlePublicSerializer, self).to_representation(instance)


class ArticleSerializer(ArticlePublicSerializer):
    """Serializer to create/update/delete article"""
    previous_version = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ArticlePublicSerializer.Meta.fields + ['previous_version']
        lookup_field = 'slug'

    def get_previous_version(self, obj):
        """Function to get previous Article version if that exist"""
        if (len(obj.previous_version.all()) > 1) and (obj.author.id == self.context['request'].user.id):
            h = obj.previous_version.all().values('id', 'title', 'body', 'created_at', 'author')[1]
            return h
        return None


class ArticleListSerializer(ArticlePublicSerializer):
    """Serializer to get short body field"""
    body = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ArticlePublicSerializer.Meta.fields + ['body', ]
        lookup_field = 'slug'

    def get_body(self, obj):
        return obj.body[:255]
