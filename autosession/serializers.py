from rest_framework import serializers

from .models import TuneType, Tune, Recording

class TuneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuneType
        fields = ('tune_type_id','tune_type_char')

class TuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tune
        fields = ('tune_id','name', 'parts','tune_type')

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = (
            'user',
            'added',
            'recording_id',
            'recording_url',
            'date_recorded',
            'tune',
            'key',
            'insturment',
            'bpm',
            'bpm_note',
            'beats_space',
            'beats_countin',
            'beats_ending',
            'repeats',
            'pickup_beats'
        )