from django.conf.urls.static import static
from django.urls import path, include
from DevWikiBackend import settings
from api.accounts.views import SocialAuthView

urlpatterns = [
    path(r'articles/', include('api.articles.urls'), name='articles'),

    path(r'comments/', include('api.comments.urls'), name='comments'),
    path(r'tags/', include('api.tags.urls'), name='tags'),
    path(r'accounts/', include('api.accounts.urls'), name='accounts'),

    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', include('rest_social_auth.urls_token')),
    path('login/', include('rest_social_auth.urls_session')),
              ] + static(settings.STATIC_URL)
