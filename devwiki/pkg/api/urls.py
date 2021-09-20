from django.urls import path, include



urlpatterns = [
    path(r'articles/', include('pkg.api.articles.urls'), name='articles'),
    path(r'comments/', include('pkg.api.comments.urls'), name='comments'),
    path(r'tags/', include('pkg.api.tags.urls'), name='tags'),
    path(r'accounts/', include('pkg.api.accounts.urls'), name='accounts'),
    path(r'admin-panel/', include('pkg.api.admin.urls'), name='admin-panel'),

]
