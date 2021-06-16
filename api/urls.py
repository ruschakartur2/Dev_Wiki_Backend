from django.conf.urls.static import static
from django.urls import path, include
from DevWikiBackend import settings

from rest_framework_swagger.views import get_swagger_view
from api.views import articles
from api.views.users import SocialAuthView, ManageUserView, UserLoginAPIView, CreateUserAPIView

article_list = articles.ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
article_detail = articles.ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
        path('articles/', article_list, name='article_list'),
        path('articles/<int:pk>/', article_detail, name='article_detail'),

        path('accounts/create/', CreateUserAPIView.as_view(), name='create'),
        path('accounts/login/', UserLoginAPIView.as_view(), name='login'),
        path('accounts/me/', ManageUserView.as_view(), name='me'),

        path('auth/', include('social_django.urls', namespace='social')),
        path('auth/signup/', SocialAuthView.as_view(), name='signup-social')

              ] + static(settings.STATIC_URL)
