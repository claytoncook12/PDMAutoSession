"""Functions for Tune Creation

Functions for creating tunes and tune sets from individual
recordings in the autosession database
"""

from pathlib import Path
import os
from datetime import datetime

from django.conf import settings

from .models import Recording

import requests
from pydub import AudioSegment

# Setup location for media files
MEDIA_ROOT = Path(settings.MEDIA_ROOT)

class WrongFileType(Exception):
    pass

def mspb(beats_per_minute):
    """
    Calculates milliseconds per beat from beats per minute

    Parameters
    ----------
        beats_per_minute (int or float)

    Returns
    -------
        float: seconds per beat
    """

    bpm = float(beats_per_minute)

    return (60/bpm)*1000

def tune_played_time_start_stop(bpm,
                                beats_space,
                                beats_coutin,
                                pickup_beats,
                                played_num,
                                parts,
                                measures_in_parts=16,
                                beats_per_measure=2):
    """
    Calculates milliseconds for beginning and end of X time through tune

    Parameters
    ----------
        bpm (int): beats per minute
        beats_space (int): beats before countin
        beats_coutin (int): beats in countin
        pickup_beats (float): beats of pickup during start of tune
        played_num (int): time the tune had been played in recording
        parts (int): number of parts of tune (A,B,C,etc.)
        measures_in_parts (int)(optional): measure for parts of tune
            Default = 16
        beats_per_measure (int)(optional): beats per measure
            Default = 2

    Returns
    -------
        dict: list containing start and end of X time through in tune in miliseconds
    """

    if played_num == 1:
        start = mspb(bpm) * (beats_space + beats_coutin - pickup_beats)
        end = start + pickup_beats + parts * ( mspb(bpm) * (measures_in_parts * beats_per_measure))
        return {'start': start, 'end': end}
    else:
        time_passed = mspb(bpm) * ((beats_space + beats_coutin)
                                   + ((played_num -1) * parts * measures_in_parts * beats_per_measure))
        end = time_passed + parts * ( mspb(bpm) * (measures_in_parts * beats_per_measure))
        return {'start':time_passed, 'end': end}

def tune_end_start_stop(bpm,
                        beats_space,
                        beats_coutin,
                        pickup_beats,
                        played_num,
                        parts,
                        beats_ending,
                        measures_in_parts=16,
                        beats_per_measure=2):
    """
    Calculates milliseconds for beginning and end of ending of tune

    Parameters
    ----------
        bpm (int): beats per minute
        beats_space (int): beats before countin
        beats_coutin (int): beats in countin
        pickup_beats (float): beats of pickup during start of tune
        played_num (int): time the tune had been played in recording
        beats_ending (int): beats in ending
        parts (int): number of parts of tune (A,B,C,etc.)
        measures_in_parts (int)(optional): measure for parts of tune
            Default = 16
        beats_per_measure (int)(optional): beats per measure
            Default = 2

    Returns
    -------
        dict: list containing start and end of ending in tune in miliseconds
    """
    time_passed = mspb(bpm) * ((beats_space + beats_coutin)
                               + ((played_num) * parts * measures_in_parts * beats_per_measure))
    end = time_passed + (mspb(bpm) * beats_ending)
    return {'start':time_passed, 'end': end}

def url_to_download(tune_url):
    """
    Returns file object name locationed in autosession media folder

    Parameters
    ----------
        tune_url (str): url for tune

    Returns
    -------
        str: file name in autosession media folder
    """

    # File Name
    f_name = Path(tune_url).name
    # Download Path
    f_path = MEDIA_ROOT / f_name

    # Test If File Already Downloaded
    if f_path.exists():
        return f_name

    # Try to get object
    r = requests.get(tune_url)
    r.raise_for_status()

    # Check If .wav file
    if 'wav' not in r.headers['Content-Type']:
        raise WrongFileType(f'File at {tune_url} is not a wav file.')
    
    # Write File to Media Folder
    open(f_path, 'wb').write(r.content)
        
    return f_name

def combine_tunes(tune_list, output_name):
    """
    Creates Combined wav file of tune list
    in autosession media folder

    Parameters
    ----------
        tune_list (list(dict)): custom dict in list
        out_name (str): name of file to be created
    """

    # Test If File Already Created
    if (MEDIA_ROOT / output_name).exists():
        return True

    # Create Empty audio segment to add too
    set_try = AudioSegment.empty()

    # Loop through tunes
    for tune in tune_list:
        file_location = MEDIA_ROOT / tune['file']
        audio = AudioSegment.from_wav(file_location)
        set_try += audio[tune['tune_time']['start']:tune['tune_time']['end']]

    # Export Files
    set_try.export(MEDIA_ROOT / output_name, format='wav')

def recordings_model_obj(tune_id_list, num_items):
    """
    Returns recording model objects of Tune.tune_id given
    and number of items specified in random order

    Parameters
    ----------
        tune_id_list (list): list of tune_id's
        num_items (int): number of items to return from tune_id_list

    Returns
    -------
        Recording objects of tune_id_list
    """

    return Recording.objects.filter(tune__tune_id__in=tune_id_list).order_by('?')[:num_items]

def tunes_list_start_stop(recordings_model_obj, num_repeats=1):
    """
    Creates special dict[list] for creating set and downloads 
    needed files into media folder

    Parameters
    ----------
        recordings_model_obj (obj): Recording objects of tune_id_list
        num_repeats (int): number of repeats of each tune

    Returns
    -------
        dict[list] in structure shown in example

    Example
    -------
    Example dict[list] structure for set with three tunes and ending
    with one repeat

    {"set": "Lilting Banshee_Kesh_Gallaghers Frolics.wav",
    "repeats_per_tune": 3, 
    "tunes": [
        {"recording_id": 5, 
        "tune": "Lilting Banshee", 
        "tune_time": 
            {"start": 9600.0, "end": 48000.0},
        "file": "05-LiltingBanshee-Flute.wav"},
        {"recording_id": 2,
        "tune": "Kesh",
        "tune_time":
            {"start": 9600.0, "end": 48000.0},
        "file": "02-KeshJig-Flute.wav"},
        {"recording_id": 1,
        "tune": "Gallaghers Frolics",
        "tune_time": 
            {"start": 86400.0, "end": 124800.0},
        "file": "01-GallaghersFrolics-Flute.wav"},
        {"recording_id": 1,
        "tune": "Gallaghers Frolics",
        "tune_time":
            {"start": 124800.0, "end": 127200.0},
        "file": "01-GallaghersFrolics-Flute.wav"}]}
    """
    
    # Tunes Empty String
    tunes = []

    # Number of tunes in recordings_model_obj
    num_items = len(recordings_model_obj)
    
    # Download those tunes and create tunes list
    for i, recording in enumerate(recordings_model_obj):
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

            # Add based on number of repeats
            for j in range(num_repeats):
                tunes.append({
                    'recording_id' : recording.recording_id,
                    'tune': recording.tune.name,
                    'tune_time': tune_time,
                    'file': file,
                })
        
        # Get Start and Stop Time of Last Play Through
        # If Last Tune in Set
        else i == (num_items - 1):
            
            # If Last Tune Is Played for more than once add played time
            # before last repeat
            if num_repeats > 1:
                # Get Start and Stop Time of Whole First Play Through
                    played_time = 1
                    tune_time = tune_played_time_start_stop(recording.bpm,
                        recording.beats_space,
                        recording.beats_countin,
                        recording.pickup_beats,
                        played_time,
                        recording.tune.parts)

                    # Add based on number of repeats
                    for j in range(num_repeats - 1):
                        tunes.append({
                            'recording_id' : recording.recording_id,
                            'tune': recording.tune.name,
                            'tune_time': tune_time,
                            'file': file,
                        })
            
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
    unduplicated_tune_names = []
    [unduplicated_tune_names.append(x['tune']) for x in tunes if x['tune'] not in unduplicated_tune_names]
    set_fname = str(num_repeats) + "_" + "_".join(unduplicated_tune_names) + ".wav"
    
    return {'set_file_name': set_fname, 'set_tunes': unduplicated_tune_names,
            'repeats_per_tune': num_repeats, 'tunes': tunes}