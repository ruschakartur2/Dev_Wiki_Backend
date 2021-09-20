from django.urls import path, include

urlpatterns = [
    path(r'accounts/', include('pkg.api.admin.accounts.urls'), name='admin-articles'),
]
