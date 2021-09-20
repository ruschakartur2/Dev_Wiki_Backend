import django_filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from pkg.core.utils.filters import TagFilter
from pkg.core.models import Tag
from pkg.api.tags.serializers import TagsSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().distinct()
    serializer_class = TagsSerializer
    pagination_class = None
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = TagFilter
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'retrieve': [AllowAny, IsAuthenticated],
        'destroy': [IsAuthenticated],
    }


    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
