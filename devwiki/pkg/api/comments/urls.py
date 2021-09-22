from pkg.api.comments.views import CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', CommentViewSet, basename='comments')
urlpatterns = router.urls
