from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from rest_framework import generics

from .models import TuneType, Tune, Recording
from .serializers import TuneTypeSerializer, TuneSerializer, RecordingSerializer

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
        results = []

        return JsonResponse({'results': results})