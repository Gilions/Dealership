from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Регистрация/авторизация
    path("auth/", include("apps.users.urls")),
    path("auth/", include("django.contrib.auth.urls")),

    path('admin/', admin.site.urls),
    path('', include('apps.dealers.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)