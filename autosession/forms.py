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
    tunes_select = forms.ModelMultipleChoiceField(queryset=Tune.objects.all(),widget=forms.CheckboxSelectMultiple())
    number_of_tunes_in_set = forms.ChoiceField(choices=(1,1)) # using placeholder value
    insturment_select = forms.ModelMultipleChoiceField(queryset=Instrument.objects.all(),widget=forms.CheckboxSelectMultiple())
    beats_per_minute = forms.ChoiceField(choices=bpm_choice)
    number_of_repeats = forms.ChoiceField(choices=repeats_choice)

    def __init__(self, *args, **kwargs):
        super(SetOptionsForm, self).__init__(*args, **kwargs)
        # Need to move choices into __init__ so that it is
        # generated each time the form is called, not initialized on server (re)start
        # http://www.ilian.io/django-forms-choicefield-with-dynamic-values/
        # was causing error with makemigration showing no table names autosession_tune
        self.fields['number_of_tunes_in_set'] = forms.ChoiceField(choices=((i,i) for i in range(1,len(Tune.objects.all())+1)))

