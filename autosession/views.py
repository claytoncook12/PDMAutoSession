from django.shortcuts import render

from rest_framework import generics

from .models import Tune
from .serializers import TuneSerializer

class TuneList(generics.ListAPIView):
    queryset = Tune.objects.all()
    serializer_class = TuneSerializer

class TuneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tune.objects.all()
    serializer_class = TuneSerializer