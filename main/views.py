from django.contrib.auth.models import User
from rest_framework import viewsets
from main.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
