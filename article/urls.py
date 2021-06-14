from django.urls import path
from rest_framework import routers, renderers
from article import views

article_list = views.ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
article_detail = views.ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('', article_list, name='article_list'),
    path('<int:pk>/', article_detail, name='article_detail'),
]
