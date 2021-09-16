import django_filters
from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


from .serializers import AdminAccountsSerializer


class AdminAccountsViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()

    serializer_class = AdminAccountsSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['nickname', 'email', 'id']
    pagination_class = None
    filterset_fields = ['is_banned', ]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_banned = True
        user.save()
        return Response(AdminAccountsSerializer(self.get_object()).data)

