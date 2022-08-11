from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("", RedirectView.as_view(pattern_name="sheets:index", permanent=True), name="index"),
    path("sheets/", include("sheets.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
