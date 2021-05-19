from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

from DevWikiBackend import settings

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'users/',include('users.urls')),
    url(r'docs/',schema_view)
] + static(settings.STATIC_URL)
