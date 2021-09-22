from django.urls import path
from pkg.api.tags.views import TagViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', TagViewSet, basename='tags')

urlpatterns = router.urls
