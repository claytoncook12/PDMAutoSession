"""Functions for Tune Creation

Functions for creating tunes and tune sets from individual
recordings in the autosession database
"""

from pathlib import Path
import os
from datetime import datetime

from django.conf import settings

import requests
from pydub import AudioSegment

# Setup location for media files
media_root = Path(settings.MEDIA_ROOT)

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
    f_name = tune_url.split("/")[-1]
    # Download Path
    f_path = media_root / f_name

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
    if (media_root / output_name).exists():
        return True

    # Create Empty audio segment to add too
    set_try = AudioSegment.empty()

    # Loop through tunes
    for tune in tune_list:
        file_location = media_root / tune['file']
        audio = AudioSegment.from_wav(file_location)
        set_try += audio[tune['tune_time']['start']:tune['tune_time']['end']]

    # Export Files
    set_try.export(media_root / output_name, format='wav')
