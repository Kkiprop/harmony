from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from harmony import views as harmony_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # custom image route
    path('media/hero.png', harmony_views.hero_image),

    # legacy image redirect
    re_path(
        r'^static/Hero_harmony\(1\)\.png$',
        harmony_views.hero_image
    ),

    # main app
    path('', include('harmony.urls')),
]

# serve static files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )