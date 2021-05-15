from django.urls import path

from .views import TuneTypeList, TuneTypeDetail, TuneList, TuneDetail

app_name='autosession'
urlpatterns = [
    path('tunetypes/', TuneTypeList.as_view()),
    path('tunetypes/<int:pk>', TuneTypeDetail.as_view()),
    path('tunes/', TuneList.as_view()),
    path('tunes/<int:pk>', TuneDetail.as_view())
]