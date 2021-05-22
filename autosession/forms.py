from django import forms
from django.forms import ModelForm, widgets
from .models import Tune

# Choice Options
repeats_choice = ((i,i) for i in range(1,11))
bpm_choice = ((i, i) for i in range(100,110,10))

class SetOptionsForm(forms.Form):
    """
    Form for selecting set options
    """
    tunes = Tune.objects.all()
    tunes = forms.ModelMultipleChoiceField(queryset=tunes,widget=widgets.SelectMultiple(attrs={'size': len(tunes)}))
    beats_per_minute = forms.ChoiceField(choices=bpm_choice)
    number_of_repeats = forms.ChoiceField(choices=repeats_choice)
    
