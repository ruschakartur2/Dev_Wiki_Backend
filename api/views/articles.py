from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import Article
from api.serializers.articles import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """Viewset to article model"""
    serializer_class = ArticleSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny, ],
                                    'update': [IsAuthenticated, ],
                                    'partial_update': [IsAuthenticated],
                                    'retrieve': [AllowAny],
                                    'delete': [IsAuthenticated], }
    queryset = Article.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
