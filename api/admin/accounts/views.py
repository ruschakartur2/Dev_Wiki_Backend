import django_filters
from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import AdminAccountsSerializer


class AdminAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AdminAccountsSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = None
    filterset_fields = ['is_banned', ]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_banned = True
        user.save()
        return Response(AdminAccountsSerializer(self.get_object()).data)

    def get_queryset(self):
        queryset = get_user_model().objects.all()

        banned = self.request.query_params.get('banned')
        list = self.request.query_params.get('list')
        
        if banned:
            queryset = get_user_model().objects.filter(is_banned=True).order_by('id')
        if list:
            queryset = get_user_model().objects.filter(is_banned=False).order_by('id')

        return queryset