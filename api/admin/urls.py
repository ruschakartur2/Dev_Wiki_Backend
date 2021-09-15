from django.urls import path, include

urlpatterns = [
    path(r'accounts/', include('api.admin.accounts.urls'), name='admin-articles'),
]
