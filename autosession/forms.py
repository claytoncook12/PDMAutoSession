from django import forms
from django.forms import ModelForm
from .models import Tune

repeats_choice = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10),
)

bpm_choice = (
    (100, 100),
)

class SetOptionsForm(forms.Form):
    """
    Form for selecting set options
    """
    beats_per_minute = forms.ChoiceField(choices=bpm_choice)
    number_of_repeats = forms.ChoiceField(choices=repeats_choice)
    
