from django.conf.urls import url
from django.urls import include
from rest_auth.registration.views import SocialAccountListView, SocialAccountDisconnectView

from users.views import GithubLogin, GithubConnect

urlpatterns = [
    url(r'rest-auth/', include('rest_auth.urls')),
    url(r'rest-auth/registration/', include('rest_auth.registration.urls'),name='registration'),
    url(r'rest-auth/social/', include('rest_framework_social_oauth2.urls')),
    url(r'rest-auth/github/$', GithubLogin.as_view(), name='github_login'),
    url(r'rest-auth/github/connect/$', GithubConnect.as_view(), name='github_connect'),
    url(r'socialaccounts/$',SocialAccountListView.as_view(),name='social_account_list'),
    url(r'socialaccounts/(?P<pk>\d+)/disconnect/$',SocialAccountDisconnectView.as_view(),name='social_account_disconnect'),
]