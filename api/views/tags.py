from rest_framework import viewsets

from api.models import Tag
from api.serializers.tags import TagsSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
