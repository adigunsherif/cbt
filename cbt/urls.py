from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

# Url Patters
urlpatterns = (
    [
        path("accounts/", include("django.contrib.auth.urls")),
        path("", include("apps.core.urls")),
        path("exam/", include("apps.exam.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

handler404 = 'apps.core.views.error_404'
handler500 = 'apps.core.views.error_500'
handler503 = 'apps.core.views.error_503'
handler401 = 'apps.core.views.error_401'
handler403 = 'apps.core.views.error_403'