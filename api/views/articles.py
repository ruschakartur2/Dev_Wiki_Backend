from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny



from api.models import Article
from api.permissions import IsOwnerOrReadOnly
from api.serializers.articles import ArticleSerializer, ArticleListSerializer, ArticlePublicSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """View set to article model"""
    serializer_class = ArticleSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny, ],
                                    'update': [IsOwnerOrReadOnly, ],
                                    'partial_update': [IsOwnerOrReadOnly],
                                    'retrieve': [AllowAny],
                                    'delete': [IsAuthenticated], }
    queryset = Article.objects.all()
    filter_backends = [filters.SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ['title']
    try:
        lookup_field = 'slug'
    except:
        lookup_field = 'pk'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        if self.action == 'retrieve' and self.request.user == self.get_object().author:
            return ArticleSerializer
        return ArticlePublicSerializer

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

