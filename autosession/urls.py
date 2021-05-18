from django.urls import path

from .views import TuneTypeList, TuneTypeDetail, TuneList, TuneDetail, RecordingList, RecordingDetail
from .views import GenerateSet

app_name='autosession'
urlpatterns = [
    path('', RecordingList.as_view()),
    path('<int:pk>', RecordingDetail.as_view()),
    path('tunetypes/', TuneTypeList.as_view()),
    path('tunetypes/<int:pk>', TuneTypeDetail.as_view()),
    path('tunes/', TuneList.as_view()),
    path('tunes/<int:pk>', TuneDetail.as_view()),
    path('GenerateSet/', GenerateSet.as_view()),
]