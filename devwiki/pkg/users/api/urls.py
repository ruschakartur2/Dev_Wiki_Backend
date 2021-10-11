from django.urls import path, include

from .views import ManageUserView, UserLoginAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', ManageUserView, basename='manage-profile')

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),

    path('oauth/', include('rest_social_auth.urls_token')),
    path('oauth/', include('rest_social_auth.urls_session')),
]
urlpatterns += router.urls