from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Connects your public pages and authentication logic
    path('', include('portfolio.urls')),
    # Exposes API endpoints as required by your project goal
    path('api/', include('api_app.urls')),
]

# Serves profile images and project screenshots during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)