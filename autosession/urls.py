from django.urls import path

from .views import TuneList

app_name='autosession'
urlpatterns = [
    path('', TuneList.as_view()),
]