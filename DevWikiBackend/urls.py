from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from DevWikiBackend import settings

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
        url(r'docs/', schema_view),
        url(r'admin/', admin.site.urls),
        url(r'api/', include('api.urls'))
] + static(settings.STATIC_URL)
