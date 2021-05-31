from django.urls import path
from autosession import views

from .views import TuneTypeList, TuneTypeDetail, TuneList, TuneDetail, RecordingList, RecordingDetail
from .views import GenerateSet

app_name='autosession'
urlpatterns = [
    path('', views.home, name='home'),
    path('SetSelection/', views.set_selection, name='set_selection'),
    path('GenerateSet/', GenerateSet.as_view()),
    path('api/recordings/', RecordingList.as_view()),
    path('api/recordings/<int:pk>', RecordingDetail.as_view()),
    path('api/tunetypes/', TuneTypeList.as_view()),
    path('api/tunetypes/<int:pk>', TuneTypeDetail.as_view()),
    path('api/tunes/', TuneList.as_view()),
    path('api/tunes/<int:pk>', TuneDetail.as_view()),
]