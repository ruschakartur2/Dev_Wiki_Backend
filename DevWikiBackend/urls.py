from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

from DevWikiBackend import settings
from users import views

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
        path('admin/', admin.site.urls),
        url(r'docs/', schema_view),
        path(r'accounts/', include('users.urls')),
        path(r'articles/', include('article.urls')),
        url('auth/', include('social_django.urls', namespace='social')),
        path('auth/signup/', views.SocialAuthView.as_view(), name='signup-social')

              ] + static(settings.STATIC_URL)
