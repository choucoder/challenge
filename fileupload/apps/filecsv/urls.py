from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from .views import FileUploadView


urlpatterns = [
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
