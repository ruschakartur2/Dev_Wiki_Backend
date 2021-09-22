from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from pkg.api.comments.serializers import CommentSerializer
from pkg.core.models import Comment
from pkg.core.utils.paginations import LargeResultsSetPagination
from pkg.core.utils.permissions import IsOwnerOrReadOnly, IsBaned


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None, status=1)
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
        """
        Method to auto add author of article from authorized user

        @return serializer with author
        """
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Endpoint to change status of comment by 'Deleted'

        @return: Response with message
        """
        comment = self.get_object()
        comment.status = 2
        comment.save()
        return Response("Comment deleted", status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Method to get permissions per action

        @return: permissions
        """
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['get'])
    def deleted_comments_list(self, request):
        """
        Endpoint to get deleted comments

        @param request: default request
        @return: list of deleted comments
        """
        comments = Comment.objects.filter(status=2)
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'patch'])
    def deleted_comment(self, request, pk):
        """
        Endpoint to get and patch current deleted comment

        @param request: default reqest
        @param pk: comment pk
        @return: if get - comment data
                 if patch - new comment data
        """
        comment = Comment.objects.get(id=pk, status=2)
        if self.request.method == 'GET':
            serializer = self.get_serializer(comment)
            return Response(serializer.data)

        elif self.request.method == 'PATCH':
            serializer = self.serializer_class(comment, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Not allowed method', status=status.HTTP_405_METHOD_NOT_ALLOWED)
