from django.contrib import admin
from django.urls import path, include

app_name = 'core'
urlpatterns = [
    path('', include('autosession.urls', namespace='autosession')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]
