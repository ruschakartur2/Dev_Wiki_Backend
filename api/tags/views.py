from rest_framework import viewsets

from core.models import Tag
from api.tags.serializers import TagsSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
