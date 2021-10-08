from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from django.urls import include
from .views import ArticleViewSet, ArticleCommentViewSet, ArticleTagViewSet

router = DefaultRouter()

router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'comments', ArticleCommentViewSet, basename='comments')
router.register(r'tags', ArticleTagViewSet, basename='tags')

urlpatterns = router.urls

