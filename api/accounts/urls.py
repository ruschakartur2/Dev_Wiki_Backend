from django.urls import path
from api.accounts import views

me = views.ManageUserView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

profile_detail = views.ProfileView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name='create'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('me/', me, name='me'),
    path('oauth/', views.SocialAuthView.as_view(),name='oauth'),
    path('profile/<int:pk>', profile_detail, name='profile')

]
