from django.urls import path
from api.accounts import views

profile = views.ManageUserView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name='create'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('me/', profile, name='me'),

]
