from django.urls import path
from pkg.api.admin.accounts.views import AdminAccountsViewSet

admin_accounts_list = AdminAccountsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
admin_accounts_detail = AdminAccountsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', admin_accounts_list, name='admin-accounts-list'),
    path('<int:pk>', admin_accounts_detail, name='admin-accounts-detail'),
]
