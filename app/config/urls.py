
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.pages.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
# handler403 = SystemView.as_view(
#     template_name="pages_misc_not_authorized.html", status=403
# )
# handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
# handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
