from django.shortcuts import render

from rest_framework import generics

from .models import TuneType, Tune
from .serializers import TuneTypeSerializer, TuneSerializer

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



