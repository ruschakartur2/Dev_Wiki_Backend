from django.conf.urls.static import static
from django.urls import path, include
from DevWikiBackend import settings

from rest_framework_swagger.views import get_swagger_view
from api.views import articles
from api.views import comments
from api.views import tags
from api.views.users import SocialAuthView, ManageUserView, UserLoginAPIView, CreateUserAPIView

main_article_list = articles.ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
main_article_detail = articles.ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

comment_list = comments.CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

comment_detail = comments.CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

tag_list = tags.TagViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
tag_detail = tags.TagViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
urlpatterns = [
        path(r'articles/', main_article_list, name='article_list'),
        path(r'articles/<slug>/', main_article_detail, name='article_detail'),

        path(r'comments/', comment_list, name='comment_list'),
        path(r'comments/<id>/', comment_detail, name='comment_detail'),

        path(r'tags/', tag_list, name='tag_list'),
        path(r'tags/<id>/', tag_detail, name='tag_detail'),
        path('accounts/create/', CreateUserAPIView.as_view(), name='create'),
        path('accounts/login/', UserLoginAPIView.as_view(), name='login'),
        path('accounts/me/', ManageUserView.as_view(), name='me'),

        path('auth/', include('social_django.urls', namespace='social')),
        path('auth/signup/', SocialAuthView.as_view(), name='signup-social')

              ] + static(settings.STATIC_URL)
