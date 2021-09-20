from django.urls import path
from pkg.api.comments import views

comment_list = views.CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

comment_detail = views.CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path(r'', comment_list, name='comment_list'),
    path(r'<id>/', comment_detail, name='comment_detail'),
]
