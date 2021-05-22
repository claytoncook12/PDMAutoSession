from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'
urlpatterns = [
    path('', include('autosession.urls', namespace='autosession')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]

# Folder for Local Media Files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)