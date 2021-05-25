from django import forms
from django.forms import ModelForm, widgets
from .models import Tune, Instrument

# Choice Options
repeats_choice = ((i,i) for i in range(1,11))
bpm_choice = ((i, i) for i in range(100,110,10))

class SetOptionsForm(forms.Form):
    """
    Form for selecting set options
    """
    tunes = Tune.objects.all() # Possible to have tune without recording and can cause error in creating form
                               # since could have a tune in the form that does not have a recording
                               # to use for audio creation
    insturment = Instrument.objects.all()

    number_of_tunes_in_set_choice = ((i,i) for i in range(1,len(tunes)+1))

    tunes_select = forms.ModelMultipleChoiceField(queryset=tunes,widget=forms.CheckboxSelectMultiple())
    number_of_tunes_in_set = forms.ChoiceField(choices=number_of_tunes_in_set_choice)
    insturment_select = forms.ModelMultipleChoiceField(queryset=insturment,widget=forms.CheckboxSelectMultiple())
    beats_per_minute = forms.ChoiceField(choices=bpm_choice)
    number_of_repeats = forms.ChoiceField(choices=repeats_choice)
    
