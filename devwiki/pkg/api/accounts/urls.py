from django.urls import path, include

from pkg.api.accounts.views import ManageUserView, ProfileView, CreateUserAPIView, UserLoginAPIView

me = ManageUserView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

profile_detail = ProfileView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('create/', CreateUserAPIView.as_view(), name='create'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('me/', me, name='me'),
    path('profile/<int:pk>', profile_detail, name='profile'),

    path('oauth/', include('rest_social_auth.urls_token')),
    path('oauth/', include('rest_social_auth.urls_session')),

]
