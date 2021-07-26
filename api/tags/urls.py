from django.urls import path, include
from DevWikiBackend import settings
from api.tags import views

tag_list = views.TagViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

tag_detail = views.TagViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path(r'', tag_list, name='tag_list'),
    path(r'<pk>/', tag_detail, name='tag_detail'),
]
