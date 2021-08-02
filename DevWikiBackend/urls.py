from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.urls import include

from DevWikiBackend import settings
from .yasg import urlpatterns as doc_urls

urlpatterns = [
        url(r'admin/', admin.site.urls),
        url(r'api/', include('core.urls')),
]
urlpatterns += doc_urls
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

