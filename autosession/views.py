from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import redirect

from rest_framework import generics

from .models import TuneType, Tune, Recording
from .serializers import TuneTypeSerializer, TuneSerializer, RecordingSerializer

from .forms import SetOptionsForm

from .creating import tune_played_time_start_stop, tune_end_start_stop, url_to_download, combine_tunes

# HTML Page Views
def set_selection(request):
    """
    Select Used Tunes in Set Creation
    """

    if request.method == 'GET':
        form = SetOptionsForm

        # Get Data from form if present
        show_selected = None
        if request.GET:
            show_selected = True
            tunes_id_list = request.GET.getlist('tunes_select')
            insturment_id_list = request.GET.getlist('insturment_select')
            bpm = request.GET.get('beats_per_minute')
            repeats = request.GET.get('number_of_repeats')

            # Make Sure At Least One Tune and One Insturment is Selected
            if len(tunes_id_list) == 0 or len(insturment_id_list) == 0:
                form_error_message = "Please select at least one tune and one insturment."
                return render(request, 'autosession/set_selection.html', {'form': form, 
                                                                          'form_error_message': form_error_message})


            return render(request, 'autosession/set_selection.html', {'form': form, 
                                                                    'show_select': show_selected,
                                                                    'tunes_id_list': tunes_id_list,
                                                                    'insturment_id_list': insturment_id_list,
                                                                    'bpm': bpm,
                                                                    'repeats': repeats})
        
        return render(request, 'autosession/set_selection.html', {'form': form, 
                                                                  'show_select': show_selected})

    else:
        form = SetOptionsForm(request.POST)
        if form.is_valid():
            return render(request, 'autosession/set_selection.html')

def set_play(request):
    """
    Play Created Set
    """

    return render(request, 'autosession/set_play.html')

# API Views
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

class RecordingList(generics.ListCreateAPIView):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

class RecordingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

class GenerateSet(View):
    def get(self, request):
        # Tunes Empty String
        tunes = []
        
        # Get 3 Random Tunes
        num_items = 3
        recordings = Recording.objects.order_by('?')[:num_items]
        
        # Download those tunes and create tunes list
        for i, recording in enumerate(recordings):
            # download recording
            file = url_to_download(recording.recording_url)

            # Get Start and Stop Time of Whole First Play Through
            # If Not Last Tune In Set
            if i != (num_items - 1):
                played_time = 1
                tune_time = tune_played_time_start_stop(recording.bpm,
                    recording.beats_space,
                    recording.beats_countin,
                    recording.pickup_beats,
                    played_time,
                    recording.tune.parts)

                tunes.append({
                    'recording_id' : recording.recording_id,
                    'tune': recording.tune.name,
                    'tune_time': tune_time,
                    'file': file,
                })
            # Get Start and Stop Time of Last Play Through
            # If Last Tune in Set
            elif i == (num_items - 1):
                last_recording = recording # Save Last Recording for Ending Added
                played_time = recording.repeats
                tune_time = tune_played_time_start_stop(recording.bpm,
                    recording.beats_space,
                    recording.beats_countin,
                    recording.pickup_beats,
                    played_time,
                    recording.tune.parts)

                tunes.append({
                    'recording_id' : recording.recording_id,
                    'tune': recording.tune.name,
                    'tune_time': tune_time,
                    'file': file,
                })
                # Add Ending with Last Tune in Set
                tune_time_ending = tune_end_start_stop(last_recording.bpm,
                    last_recording.beats_space,
                    last_recording.beats_countin,
                    last_recording.pickup_beats,
                    played_time,
                    last_recording.tune.parts,
                    recording.beats_ending)
                
                tunes.append({
                    'recording_id' : last_recording.recording_id,
                    'tune': last_recording.tune.name,
                    'tune_time': tune_time_ending,
                    'file': file,
                })

        # Generate Set Name
        # Leave Last Name Out Since it Is Doubled For Ending
        set_fname = "_".join(x['tune'] for x in tunes[:-1]) + ".wav"

        # Create Set File
        combine_tunes(tunes, set_fname)

        # See results response
        # return JsonResponse({'set': set_fname, 'tunes': tunes})

        # Redirect to new file created
        return redirect(settings.MEDIA_URL + set_fname)