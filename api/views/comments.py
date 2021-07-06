from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import Comment
from api.permissions import IsOwnerOrReadOnly
from api.serializers.comments import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['article']
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny],
                                    'update': [AllowAny],
                                    'partial_update': [AllowAny],
                                    'retrieve': [AllowAny, IsOwnerOrReadOnly],
                                    'destroy': [IsOwnerOrReadOnly],}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]