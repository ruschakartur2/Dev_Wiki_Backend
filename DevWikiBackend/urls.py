from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

from DevWikiBackend import settings

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
        path('admin/', admin.site.urls),
        url(r'docs/', schema_view),
        path(r'users/', include('users.urls')),
        path('auth/',include('rest_framework_social_oauth2.urls'), name='auth')

] + static(settings.STATIC_URL)
