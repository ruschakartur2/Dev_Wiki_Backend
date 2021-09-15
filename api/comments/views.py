from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.comments.serializers import CommentSerializer
from core.models import Comment
from core.utils.paginations import LargeResultsSetPagination
from core.utils.permissions import IsOwnerOrReadOnly, IsBaned


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    pagination_class = LargeResultsSetPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    filterset_fields = ['article']
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny and IsBaned],
        'update': [IsOwnerOrReadOnly and IsAdminUser],
        'partial_update': [IsOwnerOrReadOnly and IsAdminUser],
        'retrieve': [AllowAny and IsOwnerOrReadOnly],
        'destroy': [IsOwnerOrReadOnly],
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        queryset = Comment.objects.get(pk=self.kwargs["id"]).delete()
        CommentSerializer(queryset)
        return Response("Deleted", status=status.HTTP_200_OK)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
