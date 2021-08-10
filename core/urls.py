from django.conf.urls.static import static
from django.urls import path, include
from DevWikiBackend import settings

urlpatterns = [
    path(r'articles/', include('api.articles.urls'), name='articles'),

    path(r'comments/', include('api.comments.urls'), name='comments'),
    path(r'tags/', include('api.tags.urls'), name='tags'),
    path(r'accounts/', include('api.accounts.urls'), name='accounts'),
    path(r'admin-panel/', include('api.admin.urls'), name='admin-panel'),

    ] + static(settings.STATIC_URL)
