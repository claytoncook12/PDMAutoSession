from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from rest_framework import generics

from .models import TuneType, Tune, Recording
from .serializers import TuneTypeSerializer, TuneSerializer, RecordingSerializer

from .creating import tune_played_time_start_stop, tune_end_start_stop

class TuneTypeList(generics.ListCreateAPIView):
    queryset = TuneType.objects.all()
    serializer_class = TuneTypeSerializer

class TuneTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TuneType.objects.all()
    serializer_class = TuneTypeSerializer

class TuneList(generics.ListCreateAPIView):
    queryset = Tune.objects.all()
    serializer_class = TuneSerializer

class TuneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tune.objects.all()
    serializer_class = TuneSerializer

class RecordingList(generics.ListCreateAPIView):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

class RecordingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

class GenerateJigSet(View):
    def get(self, request):
        # Get Random Tune
        recording = Recording.objects.order_by('?')[0]
        
        # Get Start and Stop Time of Whole Play Through
        played_time = 1
        tune_first_time = tune_played_time_start_stop(recording.bpm,
            recording.beats_space,
            recording.beats_countin,
            recording.pickup_beats,
            played_time,
            recording.tune.parts)

        results = []
        results.append({
            'recording_id' : recording.recording_id,
            'tune': recording.tune.name,
            'tune_first_time': tune_first_time
        })

        return JsonResponse({'results': results})