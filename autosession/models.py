from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class TuneType(models.Model):
    tune_type_id = models.AutoField(primary_key=True)
    tune_type_char = models.CharField('Tune Type', max_length=50, unique=True)

    def __str__(self):
        return self.tune_type_char

class Tune(models.Model):
    tune_id = models.AutoField(primary_key=True)
    name = models.CharField('Tune Name', max_length=300)
    parts = models.IntegerField('Number of Parts in Tune')
    tune_type = models.ForeignKey(TuneType, on_delete=models.CASCADE, verbose_name="Tune Type", null=True, blank=True)

    def __str__(self):
        return self.name

class Key(models.Model):
    key_id = models.AutoField(primary_key=True)
    key_type_char = models.CharField('Key', max_length=15, unique=True)

    def __str__(self):
        return f'{self.key_type_char}'

class Instrument(models.Model):
    instrument_id = models.AutoField(primary_key=True)
    instrument_name = models.CharField('Instrument', max_length=50, unique=True)

    def __str__(self):
        return f'{self.instrument_name}'

class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    note_char = models.CharField('Note', max_length=50, unique=True)

    def __str__(self):
        return f'{self.note_char}'

# TODO Extend User Models to Add Artist Fields
"""
- inturments
- location
- years playing irish music
"""

class Recording(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    recording_id = models.AutoField(primary_key=True)
    recording_url = models.URLField('Recording URL', null=True, blank=True)
    date_recorded = models.DateField(null=True, blank=True)
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE, verbose_name="Tune", null=True, blank=True)
    key = models.ForeignKey(Key, on_delete=models.CASCADE, verbose_name="Key of Tune", null=True, blank=True)
    insturment = models.ForeignKey(Instrument, on_delete=models.CASCADE, verbose_name="Instrument used during recording", null=True, blank=True)
    bpm = models.IntegerField('Beats Per Minute of Recording')
    bpm_note = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name="BPM Note", null=True, blank=True)
    beats_space = models.IntegerField('Beats Before Count-In')
    beats_countin = models.IntegerField('Beats That Are Count In Before Tune Plays')
    beats_ending = models.IntegerField('Beats After Tune Stops Playing')
    repeats = models.IntegerField('Number of Repeats of Tune On Recording')
    pickup_beats = models.FloatField('Number of Pick Up Beats Into First Beat of First A Part')
    #reference_recording = models.ForeignKey(recording, on_delete=models.CASCADE, verbose_name='Recording that was used to as'\ 
    #                                                                                           'reference during this recording')
    
    #TODO
    #date_updated = models.DateTimeField()

    def __str__(self):
        return f'{self.user.get_username()}_rid{self.recording_id}_{self.tune.name}_{self.insturment}'
    
    class Meta:
        ordering = ['recording_id']
