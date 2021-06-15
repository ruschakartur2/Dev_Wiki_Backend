from django.conf.urls import url
from django.urls import include, path

from users import views

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name='create'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
