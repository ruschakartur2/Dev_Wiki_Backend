from django.conf.urls.static import static
from django.urls import path, include
from DevWikiBackend import settings
from api.articles import views

main_article_list = views.ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
main_article_detail = views.ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
        path(r'', main_article_list, name='article_list'),
        path(r'<slug>/', main_article_detail, name='article_detail'),

        ] + static(settings.STATIC_URL)
