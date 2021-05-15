from django.urls import path

from .views import TuneList, TuneDetail

app_name='autosession'
urlpatterns = [
    path('tunes/', TuneList.as_view()),
    path('tunes/<int:pk>', TuneDetail.as_view())
]