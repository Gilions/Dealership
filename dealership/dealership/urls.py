from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = "dealership.views.page_not_found" # noqa
handler500 = "dealership.views.server_error" # noqa

urlpatterns = [
    # Регистрация/авторизация
    path("auth/", include("apps.users.urls")),
    path("auth/", include("django.contrib.auth.urls")),

    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('', include('apps.dealers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
