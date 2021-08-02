from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Tag
from api.tags.serializers import TagsSerializer
from core.permissions import IsOwnerOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None

    permission_classes_by_action = {'create': [IsAuthenticated],
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