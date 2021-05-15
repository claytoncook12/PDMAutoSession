from rest_framework import serializers

from .models import TuneType, Tune

class TuneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuneType
        fields = ('tune_type_id','tune_type_char')

class TuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tune
        fields = ('tune_id','name', 'parts','tune_type')