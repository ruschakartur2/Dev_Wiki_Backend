from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.comments.serializers import CommentSerializer
from core.models import Comment
from core.paginations import LargeResultsSetPagination
from core.permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    pagination_class = LargeResultsSetPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    filterset_fields = ['article']
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny],
                                    'update': [AllowAny],
                                    'partial_update': [AllowAny],
                                    'retrieve': [AllowAny, IsOwnerOrReadOnly],
                                    'destroy': [IsOwnerOrReadOnly], }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        queryset = Comment.objects.get(pk=self.kwargs["id"]).delete()
        serializer = CommentSerializer(queryset)
        return Response("Deleted", status=status.HTTP_200_OK)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
