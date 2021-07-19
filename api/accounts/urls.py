from django.urls import path
from api.accounts import views

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name='create'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
