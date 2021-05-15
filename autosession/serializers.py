from rest_framework import serializers

from .models import Tune

class TuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tune
        fields = ('tune_id','name', 'parts','tune_type')